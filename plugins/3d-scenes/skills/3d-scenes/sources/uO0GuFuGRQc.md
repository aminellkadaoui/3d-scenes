# Cinematic renders (quick tips: dark world, area lights, haze, particles, glare, dispersion)
- url: https://youtu.be/uO0GuFuGRQc
- channel / duration / Blender version shown: Extra 3d / ~2:35 / not stated (4.x UI implied by the "Always" viewport compositor)
- domain(s): lighting, environment, rendering, compositing
- evidence used: transcript + contact sheet 01 + 8 extracted frames from the 480p mp4 (see §6).
- trust: **low** (lowered after frames: final result is the generic dark-void/glow/particles look; render settings noise threshold 0.5 / 100 samples). Short, generic, and mainly an advert for the creator's asset packs [uO0GuFuGRQc@01:15], [02:15]. Some advice is valid, some is a recipe for "AI slop" if copied blindly.

## 1. Problem it solves
A flat, evenly lit render becomes moody and "cinematic" by darkening the world, adding haze, floating particles and glow.

## 2. Techniques

### T1 — Black world + area lights, never frontal `[00:15]–[00:30]`
- What: World colour/strength → 0 (full dark). Use area lights from the top or the side. "Never place it at front, it makes your image look washed out."
- Why: frontal light kills shape (no shadow side), while side or top light gives modelling and contrast.
- Don't: use a pure black world for products that need reflections. You get dead black reflections. Use a dim HDRI or bounce cards instead.
- Status: Extracted (lighting domain; summarised here)

### T2 — Global haze cube: Principled Volume density 0.01 `[00:30]–[00:45]`
- What: a cube covering the scene with a material using only **Principled Volume**, Density **0.01**.
- Scene scale assumed: a few metres. Density is per metre, so a 50 m scene with 0.01 is much foggier.
- Cost: volumes are the biggest noise and time cost (see gmGMsKJ6xd8 T5). In Cycles 5.x, test Biased volumes. In EEVEE, World/Volume settings (Resolution, Steps).
- Status: Extracted

### T3 — Pixel Filter width 1 for sharpness `[01:45]`
- What: Render › Film › **Pixel Filter** width **1.0** px (default 1.50 Blackman-Harris).
- Why: a narrower reconstruction filter gives a crisper image.
- Risk: aliasing, moiré on fine patterns and sparkle on thin highlights, especially in motion. For animation, keep 1.2–1.5. Sharpen in comp instead if needed.
- Status: Extracted

### T4 — Glare node + viewport compositor "Always" `[01:45]–[02:00]`
- What: Compositor › Glare ("play with the settings"). In the 3D viewport shading popover › Compositor › **Always** (or Camera) to preview the comp live.
- Blender 5.2 notes: the viewport compositor exists (GPU). The Compositor dropdown options are Disabled / Camera / Always.
- Status: Extracted

### T5 — Lens Distortion dispersion 0.5 `[02:15]`
- What: a Lens Distortion node, Dispersion **0.5**.
- Doubt: 0.5 is extreme. Typical tasteful values are 0.01–0.05. See lE308jCAT2o (0.1, which is already visible) and the compositing knowledge file.
- Status: Extracted (value flagged)

## 3. Claims I doubt or must test
- Dispersion 0.5 is a strong RGB split, which is a classic "AI/beginner" tell.
- Pixel filter 1 "makes render sharp" — true, but at the cost of temporal aliasing.
- "Cycles for best results" — true for GI-heavy scenes. EEVEE is fine for many motion-graphics shots (see rendering.md).

## 4. Anti-AI-slop lessons
This video is mostly a **counter-example**: dark world + haze cube + floating dust + glare + chromatic aberration, applied as a preset to anything, is exactly the generic "cinematic" look that reads as template or AI. Use each element only when motivated: haze when there is a light beam to reveal, dust when there is a backlight to catch it, dispersion only at the frame edges and barely visible.

## 5. Candidate isolated test
A product on a plinth. A: one key area light from the side. B: + a haze cube at 0.01. C: + dispersion 0.5. D: + dispersion 0.03. Blind-rank B/C/D for "premium" vs "cheap". Expected: C ranks lowest.

## 6. Visual verification (frames viewed)
Frames viewed: contact sheet 01, plus extracted frames below. Version not legible (letterboxed 480p); Glare node has the older single "Fog Glow / quality / Mix / Threshold / Size" layout, i.e. **pre-5.0 (4.x)** UI.
- [00:03] Intro: a glowing ring-light portrait (stock intro, not the tutorial's scene).
- [00:33] **Confirms T1:** World Background colour black, **Strength 0.000**. Scene = "Gigabyte AMD 6700XT" GPU model on a "Mossy Outcrop 01" rock scan, plus "bg particles", "front particles" and a "Cube" (haze volume).
- [00:40] **Adds T1 values:** Area.001 — **Power 100 W, Square, Size 3.4 m**, placed to the side/behind the GPU, Cast Shadow + Multiple Importance on.
- [00:48] Kinetic-typography interstitial — the haze-cube density 0.01 was not caught on screen in the frames I viewed (remains transcript-only).
- [02:05] **Adds T4 values:** Glare **Fog Glow, Medium→High quality**; Render settings: Cycles, **CPU**, viewport noise threshold 0.5 / 10 samples, **render noise threshold 0.5, Max Samples 100**, Denoise on — very low-quality sampling settings for a "cinematic render" tip.
- [02:20]/[02:22] Glare final: **Fog Glow, High, Mix 0.000, Threshold 1.000, Size 8** → Lens Distortion (Projector/Jitter/Fit off, Distortion 0.000, **Dispersion field being typed, value not yet visible**) → Composite. Dispersion 0.5 remains transcript-only.
- [02:15]/[02:25] End product page: the "Cinematic Particles Asset Pack" (Gumroad, $0+/paid tier) — the video is an ad for it.
- Final quality judgement (sheet 01 [00:00], [02:30]): a GPU with glowing blue fans on a dark rock with floating specks and fog glow — the **textbook generic "cinematic" look** (dark void, haze, particles, glow, blue accent). It reads as template/slop, which confirms §4: use this video as a counter-example, not a style reference. Trust: low.
