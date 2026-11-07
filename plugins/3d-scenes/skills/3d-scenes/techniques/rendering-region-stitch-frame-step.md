---
id: rendering-region-stitch-frame-step
domain: rendering
status: Extracted
sources: [gmGMsKJ6xd8@09:30, gmGMsKJ6xd8@10:15, gmGMsKJ6xd8@11:00]
blender: "5.2"
---
# Render-time hacks: Render Region stitching and every-other-frame + interpolation

**Principle:** don't render pixels that don't change. For a locked-off camera, render a static plate once and only the moving region per frame. Frame Step 2 + optical-flow interpolation halves the frames at the risk of warping.

**Steps / settings:**
- Region stitch: render one full frame (plate). Camera view › Ctrl+B to draw the Render Region. Output RGBA, Film › Transparent if needed, "Crop to Render Region" ✗ so the frame size stays full. Render the animation. In the VSE or Premiere: plate on V1, the region sequence on V2 [gmGMsKJ6xd8@10:15].
- Frame step: Output › Frame Step **2**. Encode at half fps, interpolate back to full fps in an external optical-flow tool [gmGMsKJ6xd8@11:15].

**Use when:** region: locked camera, static lighting, a small moving object, with no shadows/reflections/GI changes outside the region. Frame step: slow, smooth motion, no occlusion, emergency deadlines.
**Avoid when:** a moving camera; moving lights; animated noise, grain or volumes; reflections of the moving object on other surfaces; fast motion, motion blur, thin parts, particles, text (interpolation artifacts).

**Failure signs:** a visible rectangle seam (noise pattern mismatch, shadow/bounce change outside the region); "jelly" warping at occlusion edges; ghosting of thin objects; doubled motion blur.

**Cost:** saves render time proportionally; adds comp and QA time.

**Conflicts with other sources:** none. The video claims interpolation "looks almost identical" (unverified).

**Test to validate:** a 48-frame locked shot of a cube sliding. Full render vs stitch: difference map. Frame step: compare the interpolated frame 13 with a true frame 13 (SSIM, visual inspection at the object edges).

**Log:** 2026-11-05 — Extracted from gmGMsKJ6xd8.
