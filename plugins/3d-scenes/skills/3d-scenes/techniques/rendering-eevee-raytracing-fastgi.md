---
id: rendering-eevee-raytracing-fastgi
domain: rendering
status: Extracted
sources: [eevee_full_course@09:20, eevee_full_course@10:40, eevee_full_course@26:20, eevee_full_course@48:40, eevee_full_course@75:20]
blender: "5.2"
---
# EEVEE Raytracing + Fast GI (roughness threshold, steps, distance, denoise)
**Principle:** EEVEE raytracing is screen-space first: it can only reflect/bounce what is visible in the frame, so objects behind/beside the camera ghost or vanish, and bounce "switches on/off" while panning [eevee_full_course@10:40]. Below the roughness threshold surfaces get traced rays; above it they get Fast GI (a cheap screen-space GI/AO). Probes fill in what the screen can't see.

**Steps / settings (starting points):**
1. Render › **Raytracing ✔** (OFF by default!) [eevee_full_course@09:20]. Method **Screen-Trace** (falls back to probes); Resolution **1:2** (final 1:1 if fine glossy detail) [eevee_full_course@15:30].
2. Fast GI Approximation ✔ — required for rough surfaces to get bounce. **Threshold 0.5** = max roughness for real rays (default) [eevee_full_course@26:20].
3. Fast GI **Steps 8 → 16**; **Distance 0 (infinite) → ~1–2 m** once a volume probe exists (shown 1.42 m) so far-field bounce comes from the baked probe, not noisy screen tracing [eevee_full_course@48:40]. Leave Rays 2, Precision 0.25, Thickness 0.25 m / 45°, Bias 0.05.
4. Denoising ✔, but consider **Temporal Accumulation OFF** for sharper textures (wood floor ON/OFF comparison) [eevee_full_course@48:20] — check in motion.
5. Keep Resolution at 1:1–1:2 for raytracing and Fast GI; 1:4–1:16 saves little and flickers (transcript; tested on screen [eevee_full_course@75:20]).
6. Film › Overscan a few % to reduce screen-edge artifacts (repo knowledge, not this source).

**Use when:** any EEVEE shot with glossy floors, metals or interior bounce.
**Avoid when:** flat-shaded/toon looks where GI isn't wanted.
**Failure signs:** reflection of an object disappears as it leaves the frame; dark/light pumping while panning; smeared wood grain (temporal denoise); blocky GI (resolution too low).
**Cost:** largest EEVEE cost after volumes; Steps and resolution are the levers.
**Conflicts with other sources:** rendering.md said "Resolution 1:1 or 1:2 for finals" — agrees. Fast GI in Cycles (Light Paths) is a different feature with the same name.
**Test to validate:** 60-frame camera pan past a chrome object over a glossy floor: Raytracing off / on / on + probes. Metric: frame-to-frame reflection-region difference + s/frame. Temporal accumulation on/off: texture sharpness (Laplacian variance) and flicker.
**Log:** 2026-11-06 — Extracted from eevee_full_course (Blender 4.4; re-check names in 5.2).
