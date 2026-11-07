# Emulate film in Blender: colour, halation, grain, lens
- url: https://youtu.be/0M0-TESgB7E
- channel / duration / Blender version shown: Edin Spiegel / ~2:25 / roughly Blender 4.0–4.1 (AgX "Punchy" look; Glare node still has "Mix"; Texture node still exists)
- domain(s): compositing, color
- evidence used: transcript + contact sheet + 10 extracted frames (see §6). Halation node chain now read from frames; curve point values still too small to read at 480p.
- trust: **medium**. A competent, concise recipe, but few exact values and no before/after numbers. The grain math is sound. No product pitch.

## 1. Problem it solves
Clean CG looks digital: perfect blacks, neutral tones, razor-sharp edges, no grain. The goal is a film-like image: lifted blacks, warm/cyan split, red halation around highlights, soft glow, grain and lens imperfections.

## 2. Techniques

### T1 — Base: AgX + Punchy look `[00:00]`
- What: Color Management › View Transform **AgX**, Look **Punchy** (named "AgX - Punchy" in 4.x menus).
- Note: Punchy adds contrast and saturation. It's good for flat scenes, but makes already-saturated scenes look garish.
- Status: Extracted

### T2 — RGB Curves "film toe/shoulder" `[00:15]`
- What: RGB Curves node, Combined (C) curve. Raise the black point "by just a tiny bit" (lifted blacks / matte). Subtly boost the upper third and just below the mids. Round the shadow-to-mid transition.
- Why: film's toe never reaches pure black, and its shoulder compresses gently.
- Starting values (my interpretation, not visible): black output 0.02–0.04; a +0.02–0.03 lift around input 0.65–0.75.
- Status: Extracted

### T3 — Color Balance split tone `[00:30]`
- What: Color Balance node (Lift/Gamma/Gain). Lift "itsy bitsy" toward cyan. Gamma and Gain slightly orange.
- Why: the classic teal-shadow / warm-highlight complementary split. It separates skin and warm objects from the shadows.
- Blender 5.2 notes: in 5.0 Lift/Gamma/Gain **operates in linear space**, so old values look stronger or different. Re-tune by eye. The 5.0 assets **Split Toning** and **Tune Image** offer the same as built-ins.
- Status: Extracted

### T4 — Halation from Emission + Environment passes `[00:30]–[01:00]`
- What: enable **Emission** and **Environment** passes. Add them together. Feed into **Dilate/Erode** with mode **Feather**, **Distance 6, Falloff Smooth**. **Subtract** (Math, scalar) the original sum from the dilated one, which gives a ring around the bright sources. The ring goes into the **Fac** of a Mix **Add** node whose second Image input is the halation colour (red-orange picked by hand; overlay text suggests a blurred copy of the Add result to pick the colour automatically) [00:51] *(corrected from frames: the ring is a Fac mask, not a multiply)*. Control the amount with the colour brightness or the dilate distance. The pre-setup for small bright objects is a morphological **open**: Dilate/Erode **Steps, Distance −1** (erode) → Dilate/Erode **Steps, Distance 1** (dilate back) before the Feather node, which removes specks so they don't bloom into blobs [01:05] *(corrected from frames; was "not described")*.
- Why: in real film, bright light passes through the emulsion, reflects off the film base and re-exposes the red-sensitive layer. The result is a red/orange fringe *around* highlights, not a uniform glow.
- Use when: there are visible practical lights, emissive screens, or the sky against dark edges. Don't use for clean product/UI shots, or when the light sources aren't in frame.
- Blender 5.2 notes: Dilate/Erode is still in 5.x, and its Distance Threshold mode is much faster in 5.2. An alternative generic approach is a high threshold Glare (Bloom), tinted red, small Size, low Strength. Emission/Environment-only sources miss bright *speculars*. A luminance key of the beauty (threshold ~1.0+ in linear) catches those too.
- Status: Extracted

### T5 — Soft glow: Glare Fog Glow with very low threshold, negative mix `[01:00]`
- What: Glare › **Fog Glow**, Threshold very low, Mix **below 0**, which means mostly the original image with a little glow.
- Blender 5.2 notes: the Glare node **no longer has Mix**. Use **Strength** (low, e.g. 0.1–0.3) plus Threshold/Smoothness. Fog Glow was made "more realistic" in 5.0. Bloom is the cheaper alternative (4.2+).
- Status: Extracted

### T6 — Film grain: noise texture, multiply by 2, subtract 1, × image, add back `[01:15]–[01:45]`
- What: a Noise texture (Texture tab) → compositor **Texture** node. Math ×2 − 1 → zero-mean noise in [-1, 1]. Multiply by the image, so grain scales with brightness (signal-dependent, like film). Add onto the image with a Mix Factor for the amount. Re-correct exposure afterwards.
- Why: zero-mean noise doesn't shift the average brightness much. Multiplying by the image puts more grain in the mids and highlights, less in deep black.
- Blender 5.2 notes: the **Texture node was removed in 5.0**, so this exact setup breaks. Replace it with the **Film Grain** compositor asset (added in 5.2) or **Sensor Noise** (5.0), or with procedural texture nodes (Noise/White Noise Texture) inside the compositor. **Animate the seed/offset per frame** (e.g. driver `#frame`), or the grain is "stuck on the lens".
- Status: Extracted

### T7 — Lens: soften, extra glare, Lens Distortion + dispersion, vignette `[01:45]–[02:15]`
- What: soften the image a little (a small Blur at the start). More glare. A small **Lens Distortion** + dispersion ("chromatic"). Vignette: **Ellipse Mask** → huge Blur → Alpha Over (image over black) → Color Ramp with flipped handles to set the size. Lower the white brightness to set the darkness.
- Blender 5.2 notes: the **Vignette** and **Chromatic Aberration** assets ship in 5.0 (Asset Shelf in the compositor), so prefer those over hand-built graphs.
- Status: Extracted

## 3. Claims I doubt or must test
- "Physically accurate" grain: real film grain is also size-dependent and per-channel. A single monochrome noise is a simplification. Fine for VSL.
- The order is not stated as important, but it is. Grain must be **last**, after the grade and after the view transform's equivalent. Glow and halation must be **first**, on linear values.
- ~~"Halation… the setup is not described"~~ — resolved from frames [01:05]: erode −1 / dilate +1 (Steps) before the Feather dilate.

## 4. Anti-AI-slop lessons
- "Film look" is a stack of *tiny* effects. Each must be barely visible on its own. The video repeatedly says "tiny bit", "subtly", "itsy bitsy".
- Halation is motivated by light sources. Glowing everything is slop.
- Static grain (same noise each frame) or grain on top of baked text overlays reads fake.

## 5. Candidate isolated test
A dark room with one visible practical bulb and a bright window. Compare the baseline (AgX, no comp) with the stack (curves + split + halation + grain + vignette), with each effect toggled. Measure: does any single effect change the mean luminance by more than 3%? Blind A/B judgement at 100% and at 50% scale. Check grain is animated (consecutive-frame difference > 0 in flat regions).

## 6. Visual verification (frames viewed)
- [00:17] RGB Curves at default (Standard mode, C channel) next to the raw render; overlay text says the node group is sold on Gumroad for $1–2 (small upsell, no sponsor).
- [00:22] + status-bar crop: curve with one control point at **(0.7, 0.7)** being dragged; Cycles noise threshold 0.0100, OIDN "Albedo and Normal", Prefilter Accurate; the "Super Denoiser" add-on is installed. Blender **4.x** (status-bar version digits illegible at 480p; 4.0/4.1 era UI confirmed: compositor has Composite node + "Use Nodes").
- [00:31] Curve after edit (crop): a very gentle S — black point lifted slightly, mid-high point raised a hair. Exact numbers not legible; the "0.02–0.04" values in T2 remain my interpretation. Color Balance node in **Lift/Gamma/Gain** mode; wheel offsets tiny (not readable).
- [00:28], [00:38] presenter only. [00:28] overlay: "If the effect is too strong, mix it with the original image" (i.e. global Fac/mix-back as a strength control).
- [00:44] Add node (Emission + Environment) and the Divide/Mix search — confirms the sum of the two passes.
- [00:46] Dilate/Erode mode menu: Steps / Threshold / Distance / **Feather** chosen.
- [00:51] **Correction:** Dilate/Erode Feather (Distance 6, Smooth) → Math Subtract → into **Fac** of Mix Add; second input = halation colour. Not "multiply by colour".
- [01:05] **Addition:** pre-chain Add → Dilate/Erode Steps −1 → Dilate/Erode Steps +1 → Feather 6. Fire scene shows the warm fringe on smoke edges — subtle.
- [01:35] Grain: Texture (Noise type, Texture properties tab) → Math Multiply 2.0 → Math Subtract 1.0 → Mix **Multiply** (Fac 1.0) with the image. Confirms T6.
- [01:52] Final graded frame (knight by campfire at dusk): lifted blacks, warm halation around the fire, gentle vignette, fine grain.
- [02:02] presenter only (no vignette node visible at this time).
- Quality judgement: **good hobbyist-to-pro**. The final frame is tasteful and restrained (not slop): effects are barely visible individually, which matches the "tiny bit" narration. Asset/scene quality is decent but the knight scene is simple. Trust: medium→medium-high for the node recipes now that the chain is seen.
