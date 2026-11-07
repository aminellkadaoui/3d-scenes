---
id: rendering-adaptive-sampling-denoise
domain: rendering
status: Extracted
sources: [gmGMsKJ6xd8@01:30, gmGMsKJ6xd8@02:30, vtdczoXVyvQ@06:45, lE308jCAT2o@01:30, cycles_20x_faster@09:45, cycles_20x_faster@11:15, cycles_20x_faster@17:15, skool-rr-rendering@05:44, skool-rr-rendering@06:16, skool-rr-rendering@06:46]
blender: "5.2"
---
# Adaptive sampling + OIDN denoise, tuned per shot type

**Principle:** Cycles noise falls with √samples, so doubling quality costs 4× time. Adaptive sampling (Noise Threshold) stops each pixel once it is "clean enough". The denoiser, guided by Albedo and Normal feature passes, removes the residue without blurring texture edges. The goal is the *lowest threshold the deadline allows*, not the highest sample count.

**Steps / settings (starting points, 1080p, Apple Silicon Metal GPU):**
- Render Properties › Device: GPU Compute (Preferences › System › Cycles Render Devices › Metal; MetalRT on M3+ if offered).
- Sampling › Render: Noise Threshold ✔
  - Stills / static product: Threshold 0.02–0.05, Max Samples 256–512, Min Samples 0 (auto).
  - Animation: Threshold 0.01–0.03, Max Samples 512–1024 (lower threshold is the cure for denoiser flicker).
  - Time Limit: 0 (off), or set as a hard budget for previews.
- Denoise ✔ › Denoiser: OpenImageDenoise · Passes: Albedo + Normal · Prefilter: Accurate · Quality: High · Use GPU ✔.
- Viewport: Threshold 0.1, Max 64–256, Denoise OIDN (or Automatic).
- Advanced › Pattern: Automatic (blue-noise distribution with adaptive sampling); keep Seed animated (clock icon) for animation.
- **Min Samples floor:** when the threshold is high (≥ 0.03) or Max Samples low (≤ 1000), set Min Samples ~20 so no pixel stops after 1–2 samples [cycles_20x_faster@11:15]. With threshold 0.01 the automatic value (0) or a floor of 32–64 is enough.
- Compositor alternative: View Layer › Passes › Data › Denoising Data ✔; Denoise node (Prefilter Accurate, Quality High/Follow Scene, **HDR ✔** so highlights above 1.0 aren't clamped) fed Image + Denoising Normal + Denoising Albedo; mix with the noisy image to dial strength or denoise passes separately [cycles_20x_faster@17:15–17:45]. Timing ≈ equal to render-time denoise [cycles_20x_faster@18:00].
- If noise survives 512 spp, find the cause (volumes, caustics, small/strong lights, glossy reflections of lights) before raising samples [gmGMsKJ6xd8@02:00].

**Use when:** every Cycles final render.
**Avoid when:** you need the noisy passes for external denoising (Resolve/Nuke). Then disable the render denoiser, enable Denoising Data, and save the noisy EXR.

**Failure signs (QA):** waxy or painterly textures ("denoiser smear"); blotchy low-frequency patches in dark corners and volumes; fine detail (fabric, text on labels) melted; frame-to-frame boiling in shadows or DOF in playback; fireflies that the denoiser turns into blobs.

**Cost:** threshold 0.05 → 0.01 roughly 2–5× time. OIDN GPU adds ~0.2–1 s per 1080p frame.

**Conflicts with other sources:** gmGMsKJ6xd8 says "never above 512" and threshold 0.05–0.075. That is fine for stills, too aggressive for animation (my assessment). lE308jCAT2o denoises in the compositor instead. That gives an equivalent result but keeps the noisy data. cycles_20x_faster uses threshold 0.03 / Max 1000 / Min 20 as a default and up to 0.1 [cycles_20x_faster@09:45]; 0.03 matches our animation range, 0.1 does not (bright simple product shot only). It also prefers OIDN over OptiX for consistency in animation [cycles_20x_faster@16:45], matching ours.

**Test to validate:** a 48-frame slow push on a dark interior. Thresholds 0.075 / 0.03 / 0.01. Measure time per frame and temporal flicker (mean abs diff between consecutive frames in a static dark region), and judge texture retention at 200% crop.

**Log:** 2026-11-05 — Extracted from gmGMsKJ6xd8, vtdczoXVyvQ, lE308jCAT2o + Blender 5.2 manual (Sampling page option names).
2026-11-07 — Added Min Samples floor, compositor Denoise HDR option and threshold conflict from cycles_20x_faster.
**Log:** 2026-11-07 — skool-rr-rendering: threshold 0.01 and never 0.03 for animation (more flicker in his experience) [06:16], but Max Samples only 100–500 [06:46]. Conflict: at Max 100 the cap dominates and 0.01 is rarely reached; his real knob is Max Samples. Keep our profile; A/B on a dark bedroom test scene.
