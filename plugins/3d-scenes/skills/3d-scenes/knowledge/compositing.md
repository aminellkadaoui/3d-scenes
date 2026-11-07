# Compositing — Blender 5.x compositor, passes, and "subtle and motivated" post effects

> Status: Knowledge (research + expert synthesis + video extraction). Target Blender 5.2 LTS. Node names were checked against the 5.0/5.1/5.2 compositor release notes and the 5.2 manual (Glare).
> Related: `rendering.md`, `color-management.md`, `ai-slop-diagnosis.md`, techniques `compositing-*`.
> Video sources: 0M0-TESgB7E (film emulation), lE308jCAT2o (beginner comp chain), vtdczoXVyvQ (passes/view layers), 1MyARLB8KzY (light comp), uO0GuFuGRQc (quick glare/dispersion), gmGMsKJ6xd8 (EXR + VSE compositor modifier).

---

## 0. The governing principle: subtle and motivated

Every post effect imitates a **real optical or photochemical cause**. Use it only when that cause would exist in the shot, at a strength where removing it is *felt* rather than *seen*.

| Effect | Real-world cause → motivation required |
|---|---|
| Glow / bloom | scatter in the lens/atmosphere from very bright sources → a light source or specular brighter than diffuse white in frame |
| Halation | film-base reflection → a film look plus bright sources against dark |
| Fog/haze (mist) | atmosphere between camera and distant objects → depth in the scene, outdoor/large spaces |
| Chromatic aberration | lens dispersion, worse at the edges → a "camera" or vintage aesthetic; never on UI/text |
| Distortion | lens geometry → wide lenses/vintage; never with straight graphic overlays |
| Vignette | lens falloff → directing the eye; not when the editor will reframe |
| Grain | film/sensor noise → film/camera aesthetic, matching footage, hiding banding |
| Sharpening | compensates softness from denoise/downscale → only to restore, not to "enhance" |
| Grade | the mood and separation of subject from background → always intentional, never a preset |

**Two tests for every node:** (1) mute it (M) and toggle, and the image must be worse without it but not "different-looking"; (2) view at 50% (phone size) and at 100%. If the effect is the first thing you notice, it's too strong.

**Effects must be optional and adjustable:** build each effect as a **node group in a Frame** with a `Strength` (0–1) input and an on/off switch (Switch / Mix with factor). Then Claude can dial each one from Python without rewiring, and the user can disable any of them.

---

## 1. Blender 5.x compositor — what changed (verify before writing bpy)

- The compositing node tree is now its **own data-block** (a node group), reusable across files. **"Use Nodes" was removed** (5.0).
- **Composite node removed**. The final image goes to a **Group Output** whose first input must be a Color socket. Viewer node still exists.
- Most options are now **input sockets** (menus as Menu sockets), like Geometry Nodes. bpy code from 4.x that sets `node.glare_type = ...` may need `node.inputs[...]` instead. **Read the node's inputs before setting** (MCP rule: never hardcode enums).
- Removed in 5.0: **Texture** node (use procedural texture nodes in the compositor), compositor **Gamma** node (the shader Gamma node is usable), Normal node dot output, Displace scale inputs. **Z Combine → Depth Combine**. **Alpha Over** inputs are now **Background/Foreground** with Disjoint/Conjoint modes. **Color Balance Lift/Gamma/Gain operates in linear**. Color Correction "Lift" → "Offset". **File Output** redesigned (Directory + File Name split).
- New in 5.0: **Convolve**, **Convert to Display**, **Switch Menu**. Glare gains **Sun Beams** and **Kernel** modes; Fog Glow is more realistic; Low/Medium quality is more stable over frames. **Asset Shelf** with built-in assets: **Chromatic Aberration, Sensor Noise, Vignette, Sepia, Split Toning, Tune Image, Unsharp Mask, Retime**, Separate/Combine Spherical/Cylindrical. A sequencer **Compositor strip modifier**.
- 5.1: Mask To SDF, Index Switch, Radial Tiling, Input nodes; Glare/Blur/Lens Distortion up to ~2× faster; Mix (Mix colour) blends alpha; Image/File Output metadata.
- 5.2: **Film Grain asset**, 3D↔Screen space assets, Blank Image, String To Image, a much more responsive interactive compositor with animation playback, faster Dilate/Erode Distance Threshold, socket value inspection.
- **GPU compositor:** Render › Performance › Compositor › Device **GPU** [gmGMsKJ6xd8@03:15]. **Viewport compositor**: 3D Viewport shading popover › Compositor: Disabled / Camera / Always [uO0GuFuGRQc@02:00]. Use it to see glow/grade live while lighting.

Typical 5.x skeleton:
```
Render Layers ─► Denoise (if not denoised at render) ─► [Glow group] ─► [Halation group] ─► [Mist/Depth haze group]
             ─► [Grade group: Curves + Color Balance] ─► [Lens group: Distortion/CA + Vignette] ─► [Sharpen] ─► [Grain] ─► Group Output
                                                                                                                  └► Viewer
```
Order rationale: optical effects (glow, haze, lens) operate on **linear light before** tonal curves. The grade operates after. Grain is **last** (it's a capture artifact, sits on top of everything). Sharpen before grain (never sharpen grain).

---

## 2. Render passes, view layers, Cryptomatte

### 2.1 Passes (View Layer Properties › Passes)
- **Data:** Combined, Z/Depth, Mist, Position, Normal, Vector (for Vector Blur), UV, Object/Material Index, **Denoising Data** (Albedo + Normal for the Denoise node) [lE308jCAT2o@01:30].
- **Light (Cycles):** Diffuse/Glossy/Transmission (Direct, Indirect, Color), Volume (Direct, Indirect), Emission, Environment, Ambient Occlusion, Shadow Catcher [vtdczoXVyvQ@01:30].
- **Cryptomatte:** Object / Material / Asset, Levels 6 typ.
- **Shader AOV / Light Groups:** custom outputs; Light Groups (View Layer › Light Groups, assign lights/world) let you rebalance key/fill/rim **after** the render. Very useful for VSL revisions ("make the product brighter").
- Rebuild formula (Cycles): `Beauty = Σ (Direct + Indirect) × Color` for Diffuse, Glossy, Transmission + Volume Direct + Indirect + Emission + Environment [vtdczoXVyvQ@02:45–05:45]. See technique `compositing-pass-rebuild-back-to-beauty`.

### 2.2 View layers
- Per element (background, hero, fog, dust, UI-safe foreground). Use **Indirect Only** to keep shadows and bounce from absent elements, and **Holdout** to keep occlusion [vtdczoXVyvQ@12:45, 16:45]. Recombine with **Alpha Over** back to front. Re-render one layer with Render Single Layer [17:45]. See `compositing-view-layers-holdout-indirect`.
- For a VSL editor: a hero-product layer with alpha + a background layer lets the editor slide text **between** them (a premium "text behind product" effect).

### 2.3 Cryptomatte
- Enable Object (and/or Material). In the compositor: **Cryptomatte** node (Image ← Combined, layer per crypto pass). Pick mattes with the eyedropper (Add/Remove), Matte output → a mask for grading a single object (brighten the product, desaturate the background).
- Save in EXR **without lossy compression** (ZIP/PIZ, Full float). DWAA breaks the ID hashes.
- Cryptomatte gives anti-aliased, motion-blur/DOF-aware mattes, unlike Object Index (aliased).

---

## 3. Per-effect reference

Each entry: **purpose · 5.x node(s) · starting values (1080p, AgX, linear input) · skip when · overdone signs**.

### 3.1 Denoise (compositor)
- Purpose: clean the render while keeping the noisy pass in EXR.
- Node: **Denoise** (Image ← Noisy Image, Normal ← Denoising Normal, Albedo ← Denoising Albedo). Prefilter Accurate, Quality High, HDR ✔ [lE308jCAT2o@02:15].
- Start: always the **first** node [lE308jCAT2o@02:45].
- Skip when the render was already denoised (double denoise = mush).
- Overdone: plastic textures, smeared fine detail.

### 3.2 Mist pass / depth haze (atmospheric perspective)
- Purpose: distant objects get lighter, lower-contrast and tinted toward the sky/fog colour. That's a key depth cue, cheaper and noise-free compared with volumetrics.
- Setup: View Layer › Passes › Data › **Mist**. World Properties › **Mist Pass**: Start (where haze begins, e.g. just behind the subject), Depth (distance to full haze), Falloff (Quadratic typ. / Linear / Inverse Quadratic). Comp: Mist → Map Range or Color Ramp (shape and limit, e.g. max 0.3–0.5) → **Mix (Mix)** Factor between the image and a haze colour (sampled from the sky/background, slightly desaturated) [general practice].
- Start: max haze 20–40% at the far background. Colour = background/sky colour, never pure white or grey.
- Skip: macro/product tabletop (no air at that scale); space scenes; graphic/flat styles.
- Overdone: the foreground subject haze-washed; everything milky and low-contrast; haze colour not matching the environment light (looks like a grey overlay).
- Note: Mist is anti-aliased in Cycles. The Z pass isn't (use Z for Defocus, Mist for haze).

### 3.3 Glare: bloom / fog glow / streaks / ghosts / sun beams
- Purpose: light scatter from very bright highlights.
- Node: **Glare**. Types Bloom, Fog Glow, Streaks, Ghosts, Simple Star, Sun Beams, Kernel. Inputs: Threshold, Smoothness, Clamp/Maximum, **Strength**, Saturation, Tint, Size, Quality (no "Mix" in 5.x).
- Start (Bloom/Fog Glow): Threshold **1.0** (0.8–2.0), Smoothness 0.1–0.3, Strength **0.1–0.3**, Size medium, Quality High for the final, Saturation ≤ 1. Linear input (before curves).
- Streaks: only with point lights or specular stars in frame (jewellery, car headlights). Streaks 4–6, Fade 0.85–0.95, Strength ≤ 0.2.
- Ghosts (lens flare): only when a strong light is *in frame* and the camera faces it. Iterations 2–3, Color Modulation 0.25–0.5, low strength [lE308jCAT2o@07:15].
- Sun Beams: only from a real sun/window position; set Sun Position to the source.
- Skip: white-background product shots, UI/text renders, scenes without highlights > 1.0.
- Overdone: threshold ≤ 0.3 (everything glows; lE308 uses 0.01 for an atmosphere effect and the result is visibly milky — an anti-example) [lE308jCAT2o@07:15] (corrected from frames); milky contrast loss; glow on walls; ghosts with no source; star filters on everything.

### 3.4 Halation
- Purpose: a film-like red-orange fringe around bright sources.
- Nodes: Emission + Environment → Dilate/Erode Steps −1 then +1 (remove specks) → **Dilate/Erode (Feather, ~6 px)** → Subtract the original → ring as **Fac** of Mix Add with the halation colour [0M0-TESgB7E@00:51, 01:05] (corrected from frames). Or a Glare Bloom with high threshold (1.5–3), red-orange tint, small size, Strength 0.05–0.15.
- Skip: clean commercial/tech looks; no visible light sources.
- Overdone: red outlines on everything; halation on non-light edges; pink/orange cast over the whole image.

### 3.5 Lens distortion & dispersion (chromatic aberration)
- Node: **Lens Distortion** (Radial; Distortion, Dispersion, Jitter, **Fit**) [1MyARLB8KzY@11:15], or the **Chromatic Aberration** asset (5.0).
- Start: Distortion ±0.005–0.02; Dispersion **0.01–0.03**; Fit on when distorting; Jitter off.
- Skip: UI/screens/text in 3D, product geometry with straight lines, shots the editor will reframe.
- Overdone: visible RGB fringes beyond the corners; 0.1 already obvious [lE308jCAT2o@08:30]; 0.5 is a beginner/AI tell [uO0GuFuGRQc@02:15]; black/stretched corners.

### 3.6 Vignette
- Node: the **Vignette** asset (5.0), or Ellipse Mask → large Blur → Multiply [0M0-TESgB7E@02:00].
- Start: edge darkening 10–25% (≈ 0.15–0.4 stop), very soft, centred on the subject (offset if the subject is off-centre).
- Skip: when the editor adds a vignette or reframes/zooms; bright high-key product scenes.
- Overdone: visible oval, near-black corners, "tunnel" look.

### 3.7 Film grain
- Nodes: the **Film Grain** asset (5.2) or **Sensor Noise** (5.0). Manual: White Noise/Noise Texture (seed animated) ×2−1 × image → Add, Factor 0.02–0.06 [0M0-TESgB7E@01:15–01:45]. The 4.x Texture node method doesn't work in 5.x.
- Start: barely visible at 100% on a mid-grey area; grain size ~1–1.5 px at the delivery resolution; luminance (mono) grain, little chroma.
- Skip: ultra-clean tech/product looks; low-bitrate delivery (grain turns into compression blocks); EXR handed to a colourist (they add grain).
- Overdone: obvious "dirty" noise; static (non-animated) grain; coloured confetti; grain on overlaid text.

### 3.8 Color grading — in Blender vs DaVinci
- In Blender: **RGB Curves** (gentle S, lifted black 0.01–0.03), **Color Balance** (Lift/Gamma/Gain, linear in 5.x; or Offset/Power/Slope ASC-CDL), **Hue Saturation Value**, **Split Toning / Tune Image** assets. Teal shadow / warm highlight split only as a hair [0M0-TESgB7E@00:15–00:30], [lE308jCAT2o@03:45–05:45].
- Grade in Blender when: delivering final pixels to a non-colourist editor, or the look must be locked per shot.
- Hand off to DaVinci when: the shot is cut with live footage, several 3D shots must match, or a colourist exists. Then deliver a **neutral** render (AgX, no grade, no grain, no vignette) as EXR or 16-bit [vtdczoXVyvQ@30:45–32:00].
- Overdone: teal/orange everything, crushed blacks, faded milky blacks, saturation > +15%, nodes fighting each other (exposure up, gamma down, brightness up) [lE308jCAT2o@05:45].

### 3.9 Sharpening
- Nodes: **Unsharp Mask** asset (5.0, radius/amount control) or Filter › Sharpen / **Diamond Sharpen**, Fac 0.1–0.2 [lE308jCAT2o@06:00–06:15].
- Use when: denoise softness, downscaled 4K → 1080 outputs needing crispness.
- Skip: noisy renders; before grain (sharpen first, then grain); when the editor/platform will sharpen.
- Overdone: halos/white outlines on edges, crunchy textures, crawling edges in motion.

### 3.10 Glow vs DOF vs motion blur in comp
- Defocus (Z-based) and Vector Blur in comp are fallbacks. They produce edge halos and artifacts at depth discontinuities. Prefer in-render DOF and motion blur for finals. Use comp versions only for fast previews or when re-rendering is impossible.

---

## 5. QA checklist for comps

1. Mute-toggle every group. Each one must earn its place.
2. Check the histogram/False Color: no new clipping introduced by glow or grade.
3. Look at the glow source: is there a real highlight under every glow, halo or flare?
4. Check text/UI regions: no CA, no distortion, no grain on graphics that the editor overlays.
5. Play back 3 s: grain is animated, glow is stable (no flicker on Low/Medium quality; use High or 5.0+ improvements), mist doesn't pop.
6. Brand colours are still within ΔE < 3 after the grade.
7. Export as the editor will receive it and view it in Premiere/Resolve.

## Sources
- Videos: 0M0-TESgB7E, lE308jCAT2o, vtdczoXVyvQ, 1MyARLB8KzY, uO0GuFuGRQc, gmGMsKJ6xd8 (see `sources/`).
- Blender 5.0 compositor release notes: https://developer.blender.org/docs/release_notes/5.0/compositor/
- Blender 5.1 compositor release notes: https://developer.blender.org/docs/release_notes/5.1/compositor/
- Blender 5.2 compositor release notes (Film Grain asset etc.): https://developer.blender.org/docs/release_notes/5.2/compositor/
- Blender 5.2 manual — Glare node: https://docs.blender.org/manual/en/latest/compositing/types/filter/glare.html
