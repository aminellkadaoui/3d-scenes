---
id: compositing-lens-imperfections
domain: compositing
status: Extracted
sources: [0M0-TESgB7E@01:45, 0M0-TESgB7E@02:00, lE308jCAT2o@07:30, lE308jCAT2o@08:15, uO0GuFuGRQc@02:15, 1MyARLB8KzY@11:15]
blender: "5.2"
---
# Lens imperfections: distortion, dispersion (CA), vignette, softness

**Principle:** real lenses have a little barrel distortion, lateral chromatic aberration growing toward the corners, and light falloff (vignetting). A *trace* of these tells the eye "photographed". Strong amounts read as a cheap filter.

**Steps / settings (starting points, 1080p):**
- Lens Distortion node: Type Radial · Distortion **±0.005–0.02** · Dispersion **0.01–0.03** · **Fit** ✔ when distortion pushes the edges inward (avoids black corners) [1MyARLB8KzY@11:30] (frames: that tutorial ships Distortion 0.020, Dispersion 0.000, Fit on [1MyARLB8KzY@11:40]). Jitter off (it adds noise).
- Or use the **Chromatic Aberration** asset (5.0) for CA alone.
- Vignette: the **Vignette** asset (5.0), or Ellipse Mask (≈ frame size) → Blur (huge, ~200–400 px) → Mix Multiply onto the image. Darken edges by **10–25%** (≈ 0.15–0.4 stop), not to black [0M0-TESgB7E@02:00].
- Softening: a very small Blur (0.5 px) or a lower-strength Bloom; never as a substitute for DOF.
- Wrap as a node group with a master "Lens amount" input and per-effect toggles.

**Use when:** cinematic/vintage, handheld-styled, or "shot on camera" looks; focusing attention toward the centre (vignette).
**Avoid when:** product turntables with exact geometry; screen/UI replacements (distortion bends text); overlays with straight graphic lines; shots that the editor will reframe or zoom in the edit (vignette and distortion move with the punch-in; let the editor add the vignette).

**Failure signs:** visible RGB fringes in the frame centre or on text; dispersion ≥ 0.1 (obvious) or 0.5 [uO0GuFuGRQc@02:15] (glaring); black or stretched corners (Fit off); vignette with a visible oval edge or near-black corners; vignette that "breathes" when the editor scales.

**Cost:** negligible.

**Conflicts with other sources:** uO0GuFuGRQc: dispersion 0.5; lE308jCAT2o: 0.1; my recommendation: 0.01–0.03. 1MyARLB8KzY: only when motivated (vintage scene).

**Test to validate:** a grid + white text card. Dispersion 0.01/0.03/0.1/0.5. Measure fringe width in px at the corner and centre. Blind "premium" ranking.

**Log:** 2026-11-05 — Extracted from 0M0-TESgB7E, lE308jCAT2o, uO0GuFuGRQc, 1MyARLB8KzY.
