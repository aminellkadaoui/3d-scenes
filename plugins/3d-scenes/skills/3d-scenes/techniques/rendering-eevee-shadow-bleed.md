---
id: rendering-eevee-shadow-bleed
domain: rendering
status: Extracted
sources: [eevee_full_course@03:00, eevee_full_course@07:40, eevee_full_course@09:20]
blender: "5.2"
---
# EEVEE light bleed and soft-shadow noise (wall thickness, shadow Steps/Rays)
**Principle:** EEVEE shadows are virtual shadow maps sampled by stepping along the ray. A wide/soft light (large size, big sun Angle) plus thin, single-sided walls plus too few steps lets the light "leak" through the occluder at corners and window edges. Soft-shadow grain is under-sampling of that same soft light.

**Steps / settings (starting points):**
1. Close and thicken occluders: Solidify on walls/ceiling (≥ 0.1–0.2 m at real scale) [eevee_full_course@03:00]. No gaps at corners.
2. Render › Sampling › Render › Shadows › **Steps 12–16** (shown 16; transcript: default 6) [eevee_full_course@07:40].
3. Shadows › **Rays 2** for soft-shadow noise (multiplies samples only for soft shadows) [eevee_full_course@09:20]; Render Samples 64 baseline, raise for DOF/motion blur.
4. If bleed persists: reduce sun Angle / light size a little, check Light › Shadow › Resolution Limit, then the volume-probe bias settings (`rendering-eevee-volume-probe-bake`).

**Use when:** any EEVEE interior with sun or large area lights entering through openings.
**Avoid when:** exteriors / no occluders (extra steps = wasted time).
**Failure signs:** bright fringe on the inside of a wall next to a window; light patch "bleeding" under a wall; grainy penumbra that shimmers in motion.
**Cost:** Steps/Rays scale shadow cost roughly linearly; small vs GI/probes.
**Conflicts with other sources:** `knowledge/rendering.md` §7 said "Shadow rays 2–3 / steps 6+". This source shows 16 is needed for soft interior suns. Resolution: Steps 12–16 for interiors with soft suns, 6–8 elsewhere.
**Test to validate:** closed room, sun 2° through a window; Steps 6 vs 16, thin plane walls vs Solidify 0.2 m; measure corner luminance where the shadow should be black; s/frame.
**Log:** 2026-11-06 — Extracted from eevee_full_course (Blender 4.4).
