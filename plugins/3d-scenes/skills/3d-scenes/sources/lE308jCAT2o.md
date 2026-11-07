# Cinematic compositing for beginners (Blender compositor as a post-processing chain)
- url: https://youtu.be/lE308jCAT2o
- channel / duration / Blender version shown: Graffinity3D / ~9:15 / **Blender 4.5.0** (title bar; corrected from frames — the Glare node shown is the 4.5 redesign with Highlights/Adjust/Glare panels, Strength/Saturation/Tint; Gamma node still present; Cycles GPU)
- domain(s): compositing, color
- evidence used: transcript + 3 contact sheets + 7 extracted frames (see §6).
- trust: **medium**. A clear explanation of each node, but the chain has redundant and contradictory steps (darken with gamma, then re-brighten with brightness). Exact values are given, which is useful. Sells a procedural material add-on at the end.

## 1. Problem it solves
A raw render (Earth from space with a volumetric cloud layer) looks flat. A post chain adds exposure, contrast, tint, glow, sharpness and lens character.

## 2. Techniques

### T1 — Pre-flight: AgX, False Color exposure check, Denoising Data `[00:15]–[01:45]`
- What: View Transform **AgX**. Temporarily switch the view to **False Color** to read exposure [00:45]: mostly green/blue is good, a little yellow is OK, orange/red = overexposed. Adjust **Exposure** in Color Management [01:15]. Check render-visibility toggles (camera icon) for collections. View Layer › Passes › Data › **Denoising Data** on [01:30].
- Why: judging exposure by eye on an sRGB monitor is unreliable. False Color maps scene luminance bands to colours.
- Status: Extracted

### T2 — Compositor Denoise first `[02:00]–[02:45]`
- What: Denoise node: Image ← Noisy Image, Normal ← Denoising Normal, Albedo ← Denoising Albedo. "Denoising should be the very first operation."
- Why: every later op (sharpen, glare thresholds, curves) amplifies noise.
- Caveat: you get the same result with the render-time denoiser (Render › Sampling › Denoise) and no comp. The comp version is useful to keep the noisy pass in EXR and decide later.
- Status: Extracted

### T3 — Exposure 0.1, Gamma 1.1 `[02:45]–[03:30]`
- What: an Exposure node +0.1. A Gamma node 1.1. He says >1 darkens the mids (opposite to the CM Gamma convention, which follows the node's behaviour).
- Blender 5.2 notes: the compositor **Gamma node was removed in 5.0**. The release notes point to the shader Gamma node, which is now usable in the compositor. Prefer RGB Curves or Color Balance anyway.
- Status: Extracted

### T4 — Color Balance Offset/Power/Slope: slope tinted green-blue; offset/power contrast `[03:45]–[04:45]`
- What: Color Balance, mode **Offset/Power/Slope (ASC-CDL)**. Slope (≈ highlights) toward green-blue for a "spacey" tint, then reduce the saturation [04:15]. On screen: **Offset 0.000, Power 1.200, Slope 0.800**, Slope colour a pale green-cyan [05:30] (corrected from frames: it is Power 1.2 / Slope 0.8, not "offset 1.2").
- Blender 5.2 notes: Lift/Gamma/Gain is now computed in linear (5.0). Offset/Power/Slope behaves as ASC-CDL.
- Status: Extracted

### T5 — RGB Curves Film-Like S-curve with lifted black and lowered white `[04:45]–[05:45]`
- What: RGB Curves (Film Like tone option). Add two points: upper-mid up, lower-mid down (one point reads **(0.2, 0.1)** [05:30]). Raise the black point slightly and lower the white point to **(1.0, 0.9)** [07:15] (matte).
- Status: Extracted

### T6 — Brightness/Contrast brightness 1 (to undo darkening) `[05:45]`
- Doubt: a symptom of a chain fighting itself. Better: fewer nodes, with exposure set once.
- Status: Extracted

### T7 — Sharpen: Filter "Diamond Sharpen" factor 0.2 `[06:00]–[06:15]`
- What: Filter node, type **Diamond Sharpen**, Fac **0.2** (1.0 is "overkill").
- Use when: the output is downscaled or soft from denoising. Don't use on top of grain (it amplifies it), or on noisy renders.
- Blender 5.2 notes: the **Unsharp Mask** asset (5.0) gives a more controllable radius/amount.
- Status: Extracted

### T8 — Glare Fog Glow (threshold 0.1, blue tint, quality High) + Ghosts (iter 2, color mod 0.5, threshold 0.25) `[06:15]–[07:30]`
- What: Fog Glow, Threshold **0.010**, Smoothness 0, Strength 1.0, Saturation 1.0, Tint light blue, Size 1.0, Quality Medium→**High** [07:15], [07:45]. A second Glare **Ghosts**: Threshold **0.025**, Strength 1.0, Tint same blue, Iterations 2, Color Modulation 0.5 [07:45] (corrected from frames: thresholds are 0.01 / 0.025, not 0.1 / 0.25).
- Why: the threshold selects which luminance contributes. A low threshold makes almost everything glow (a dreamy, low-contrast haze).
- Doubt: Threshold 0.01 in linear means essentially the whole image glows — confirmed visually: the final is milky. Motivated here (atmosphere scattering) but a slop recipe for general scenes. Ghosts imply a strong light source in frame.
- Blender 5.2 notes: Glare has Strength / Saturation / Tint / Size inputs (no Mix).
- Status: Extracted

### T9 — Lens Distortion −0.01, Dispersion 0.1 `[07:30]–[08:45]`
- What: Lens Distortion (type **Radial**): Distortion **−0.010** [08:30], which is tiny. Whether negative means barrel or pincushion in Blender is not verified, so check it visually. Dispersion **0.1**, visible as RGB split growing toward the corners.
- Doubt: 0.1 dispersion is noticeable. For a premium look use 0.01–0.03.
- Status: Extracted

## 3. Claims I doubt or must test
- The order "exposure → gamma → balance → curves → brightness" with mutually cancelling steps.
- Glow after sharpen and grade: glow should operate on linear HDR values *before* curves that compress highlights. Otherwise the threshold behaves unpredictably.
- "Glare simulates lens flare from bright objects exceeding the dynamic range" — that is roughly correct conceptually.

## 4. Anti-AI-slop lessons
- Use False Color to set exposure objectively instead of brightening in comp.
- Many effects with low threshold glow, strong dispersion and sharpening produce the "over-processed" look. Keep each node justified, and A/B it against bypass (M to mute).

## 5. Candidate isolated test
The same render, chain A (as in the video) vs chain B (Denoise → Glare Bloom threshold 1.0 strength 0.2 → Curves mild → Lens Distortion dispersion 0.02 → Vignette asset). Compare the histogram (clipping %), mean saturation and blind ranking.

## 6. Visual verification (frames viewed)
- [04:05] Chain start: Exposure **0.100** → Gamma **1.100** → Color Balance (Offset/Power/Slope). Render settings visible: Cycles GPU, render noise threshold 0.03, max samples 350, denoise on. Raw render here is already well exposed and punchy.
- [05:30] Color Balance **Offset 0 / Power 1.2 / Slope 0.8**, Slope pale green; RGB Curves **Film Like**, S-curve with point (0.2, 0.1), black point slightly lifted. Title bar: **Blender 4.5.0**.
- [07:15] RGB Curves white point (1.0, 0.9) → Brightness/Contrast (Bright 1.0, Contrast 0) → Filter **Diamond Sharpen Fac 0.200** → Glare **Fog Glow**, Quality Medium, Threshold **0.010**, Smoothness 0, Strength 1, Saturation 1, Tint light blue, Size 1.0.
- [07:45] + crop: second Glare **Ghosts**, Quality High, Threshold **0.025**, Iterations 2, Color Modulation 0.5, same blue tint.
- [08:30] Lens Distortion **Radial**, Distortion **−0.010**, Dispersion being raised from 0 (tooltip shown); final 0.1 per transcript, not seen on screen.
- [08:50] Final result.
- Quality judgement: **slop-leaning**. The final [08:50] is hazier, flatter and bluer than the raw at [04:05]; the near-zero glow threshold makes a milky veil over the whole planet. The individual node explanations are fine; the chosen values are a cautionary example of "over-processed". Treat values as anti-examples, not defaults.
