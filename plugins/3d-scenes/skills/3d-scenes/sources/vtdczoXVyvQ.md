# Render like a pro: passes, view layers, linear/ACES colour, compositing in Resolve
- url: https://youtu.be/vtdczoXVyvQ
- channel / duration / Blender version shown: Robin Squares / 34:20 (re-upload) / **Blender 4.1 (4.1.1 in status bar, corrected from frames)**; DaVinci Resolve Studio 18.6 for the Fusion part
- domain(s): rendering, compositing, color
- evidence used: transcript (auto captions) + 2 contact sheets + 9 extracted frames (see §6).
- trust: **high** on the concepts (studio pipeline, a competent and honest presenter). He explicitly says "if you don't know why you need this, you don't need it" [vtdczoXVyvQ@32:30]. **Medium** on the colour specifics: he uses a "gamma 2.2 view LUT" shortcut in Resolve and the CST settings are rushed. Sponsored (Skillshare) segment at [08:15]–[09:15].

## 1. Problem it solves
A beauty-only 8-bit render is a dead end. You can't recolour the fog, darken only diffuse, swap a background, or re-render one element without re-rendering everything. The video teaches the studio method: **separate light components (passes), separate elements (view layers), store linear data (EXR), recombine and grade later**.

## 2. Techniques

### T1 — Light passes and "back to beauty" rebuild `[01:00]–[08:00]`
- What: View Layer Properties › Passes › Light: **Diffuse** (Direct, Indirect, Color), **Glossy** (Direct, Indirect, Color), **Transmission** (Direct, Indirect, Color), **Volume** (Direct, Indirect) if volumes are used, **Emission**, **Environment** [01:30]. The rebuild formula per component is `(Direct + Indirect) × Color`. Then sum all components + Volume + Emission + Environment = Beauty [02:45]–[05:45].
- He builds a "Pass Mixer" node group (Ctrl+G) with inputs Direct, Indirect, Color. In the group's N panel, the defaults are Direct = black, Indirect = black, Color = white, so unused slots don't add white [04:45]. Use Node Wrangler Alt+RMB drag for fast chains.
- Check: a split viewer against the Image (beauty) output. The rebuild matches but is **noisy**, so add a Denoise node with Normal + Albedo (View Layer › Passes › Data › **Denoising Data**) at the end of the chain [06:15]–[06:45]. Denoising each pass separately may be more accurate in external compositors; in Blender, test it [07:00].
- Payoff: change the fog hue alone (Mix Color › Hue after the Volume branch) [07:15]–[07:30], or boost thin glossy details (marionette strings) without touching the rest.
- Use when: you need per-component control, or the client asks for changes after rendering. Don't use for a quick VSL shot that goes straight into Premiere. The beauty pass + a few utility passes is enough.
- Blender 5.2 notes: the Composite node is replaced by **Group Output**. "Use Nodes" was removed. Node groups work the same way. Pass names are unchanged in Cycles. EEVEE has fewer light passes (no Transmission split).
- Status: Extracted

### T2 — OpenEXR MultiLayer, Half, DWAA saved as startup default `[01:45]–[02:30]`
- What: Output › File Format **OpenEXR MultiLayer**, Color Depth **Half**, Codec **DWAA**. File › Defaults › Save Startup File. If compositing is enabled, route the passes into a File Output node [02:00].
- Note: for data passes (Cryptomatte, Depth, Position, Normal) prefer lossless (ZIP/PIZ) and Full float.
- Status: Extracted

### T3 — View layers per element + Indirect Only + Holdout `[09:15]–[18:00]`
- What: sort elements into collections (background, haze, mountain, dust, vehicle). Make an "everything" view layer with **Use for Rendering** off as the work layer [10:45]. Then make one view layer per element (copy settings from the previous one). In the Outliner filter, enable the **Indirect Only** and **Holdout** restriction toggles [12:45], [16:30].
  - Indirect Only: the collection casts shadows and bounce light into the layer but isn't visible [12:45]–[13:15].
  - Holdout: the collection cuts a mask (alpha 0) in this layer, so objects hidden behind it stay hidden when re-composited [16:45]–[17:30]. Rule: "things that both go in front of and behind other things need holdouts" [17:30].
- Recombine back to front with **Alpha Over** (Render Layers node dropdown per view layer) [14:30]–[15:00]. Re-render only one layer with "Render Single Layer" [17:45].
- Why: decoupling elements lets you fix or re-render one element, and some elements (fog, dust) can be graded separately.
- Blender 5.2 notes: the Alpha Over inputs are renamed **Background / Foreground** and gain Disjoint/Conjoint modes (5.0). Holdout and Indirect Only remain collection restriction toggles in the View Layer (Cycles; Indirect Only is Cycles-only).
- Status: Extracted

### T4 — Linear / ACEScg export and OCIO transform in DaVinci Resolve `[19:00]–[21:00]`, `[22:30]`, `[29:15]–[30:15]`
- What: Output Properties › Color Management › **Override** › choose a linear space or **ACEScg** [19:30]. The saved image "should look awful", which means you did it right [19:45]. In Resolve Fusion, add an **OCIO ColorSpace** node and point it at Blender's `config.ocio` (in the Blender install: `<version>/datafiles/colormanagement/config.ocio`) [20:00]. Source = what you saved (ACEScg); Output = what you viewed in Blender (e.g. **AgX Base sRGB**) [20:30], [29:30]. In Blender itself: an image's colour-space dropdown or the **Convert Colorspace** node [20:45].
- Then grade in Resolve: a CST into DaVinci Wide Gamut / Intermediate ("film log"), grade with offset/gain/contrast/mid-detail, then a CST out to Gamma 2.4 [30:45]–[32:00].
- Why: compositing math (add, multiply, blur, glow) is only physically correct on linear values. Applying the view transform (AgX) last reproduces the Blender look. ACEScg is widely understood by other apps.
- Blender 5.2 notes: Blender 5.0 added a scene **Working Space** (Linear Rec.709 default / Linear Rec.2020 / ACEScg) and built-in **ACES 1.3 / ACES 2.0** view transforms. EXR files are always written scene-linear. The Override mainly chooses *which* linear space. On macOS the config is at `/Applications/Blender.app/Contents/Resources/5.2/datafiles/colormanagement/config.ocio`.
- Status: Extracted

### T5 — Fusion recombine (Channel Booleans, Merge, alpha from background lightness) `[23:15]–[29:15]`
- What: Reactor › "Split EXR Ultra" script to explode the layers [24:30]. Channel Boolean Add/Multiply to rebuild the passes. Merge nodes back to front. Add the volume layer with an Add rather than a Merge [29:00]. Denoise (Noise Reduction) before the colour-space node [30:45].
- Status: Extracted (Resolve-side; out of Blender scope)

## 3. Claims I doubt or must test
- A "Gamma 2.2 view LUT" in Resolve to preview linear [24:00] is a rough approximation and doesn't match AgX. Use it only for previewing. He corrects himself later [30:00].
- "Denoising each pass separately might be more accurate" — true in some compositors. In Blender, test it. Denoising the rebuilt beauty with Albedo + Normal is the safe default.
- "Resolve is much better than the Blender compositor" [23:15] is opinion. Blender 5.x's GPU compositor has closed much of the gap for grading-free comp.
- Output colour space names (e.g. "AgX Base sRGB") depend on the config version. Verify in 5.2's config.

## 4. Anti-AI-slop lessons
- Pro images are *assembled* deliberately. Each element's light and colour can be balanced independently instead of accepting one auto-generated frame.
- Linear data plus a proper view transform at the end is why pro glows, fog and grades look natural. Grading a baked sRGB PNG gives crunchy, plasticky results.
- Restraint: use the heavy pipeline only when there is a reason (revisions, multi-department work). Complexity for its own sake is also slop.

## 5. Candidate isolated test
A scene with a cube, glass, a volume box and an emissive dot. Render Multilayer EXR with Diffuse/Glossy/Transmission/Volume/Emission passes. Rebuild with the Pass Mixer group and compute the difference against the Image pass (expect ≈0 before denoise). Then retint only the volume and confirm the other channels are unchanged.

## 6. Visual verification (frames viewed)
- [04:02] Group Interface panel (Blender 4.1 node-group sidebar): sockets typed **Color**, Default white. Confirms the Pass Mixer is built as a Color-socket group.
- [04:50] Pass mixer node in use on a MultiLayer EXR loaded as Image node, **Color Space = Linear Rec.709, Alpha = Premultiplied**, "Half Float Precision" ticked. Direct/Indirect swatches are still white here and he annotates them; at [05:00] (sheet) the Color socket has **Hide Value** ticked. I did **not** see the Direct/Indirect defaults set to black on screen — the "Direct/Indirect = black" claim in T1 stays transcript-only.
- [05:10] Group collapsed with all three values hidden (only socket names in the N panel) — so in practice he hides the values rather than relying on defaults.
- [06:40] Full rebuild tree confirmed: 3+ Pass mixer groups → chained **Add** (Mix, Fac 1.0) → Mix → **Denoise (Prefilter: Accurate, HDR on)** → Viewer + Composite. Matches T1. The rebuilt beauty (marionette) is clean and convincing.
- [12:50] Dust view layer: Use for Rendering on, Render Single Layer visible, Outliner filter popover with restriction toggles. Confirms T3 UI location (Outliner › Filter › Restriction Toggles).
- [19:30] Explanatory graphic: the "awful looking" linear image vs a display curve — illustration only, no settings.
- [19:40] + crop: Racecar demo render settings (Blender 4.1.1): Render Noise Threshold **0.05**, Max Samples **5000**, **Min Samples 500**, Denoise on, Motion Blur on, Film Exposure **0.27**, Pixel Filter Blackman-Harris 1.50 px. Viewport noise threshold 0.01. (Added: high min-samples floor with adaptive sampling — a studio habit for animation stability; not discussed in transcript.)
- [29:35] Resolve 18.6 Fusion: **OCIOColorSpace** node, Controls tab with OCIO Config "Browse", Source/Output Space dropdowns. Confirms T4/T5 workflow; exact source/output names not legible at 480p.
- [33:00] Closing EEVEE production shot (robot, Blender 4.1, collections prefixed LGT-/CA-/SE-/PR-). Shows a studio naming convention for lights/camera/set/props.
- Quality judgement: **professional**. Marionette, dune/ornithopter and racecar frames have motivated lighting, restrained grade, real atmosphere — not slop. Trust in the concepts stays high; colour-space names still need checking against 5.2.
