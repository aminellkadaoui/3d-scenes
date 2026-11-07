---
id: materials-eevee-archviz-glass
domain: materials
status: Extracted
sources: [eevee_full_course@56:40, eevee_full_course@60:20, eevee_full_course@61:00, eevee_full_course@62:20]
blender: "5.2"
---
# EEVEE "archviz glass" (Transparent + Glossy by Layer Weight) and render methods
**Principle:** EEVEE refraction is screen-space and probe-based, so real refractive glass looks clearly worse than Cycles (side-by-side [eevee_full_course@56:40]) and liquids inside glass break. For windows and most glassware the eye mainly reads **edge reflections (Fresnel) + see-through**, which a non-refractive shader gives cleanly.

**Steps / settings (starting points):**
1. Nodes [eevee_full_course@60:20]: Layer Weight (Blend 0.5) **Facing** → Mix Shader Fac; Shader A = **Transparent BSDF** (white); Shader B = **Glossy BSDF** (Multiscatter GGX, Roughness 0) → Surface.
2. Material › Settings › **Render Method**: **Blended** works with sphere probes; **plane probes only show through Dithered** (bug report shown [eevee_full_course@61:00]); Dithered is noisier — raise samples [eevee_full_course@62:20]. Keep Transparent Shadows ✔ so sun passes through windows.
3. Real refractive glass (Principled Transmission) only for hero glass with a Sphere probe around it, or render that shot in Cycles.
4. Put window glass in the "hide before baking" collection when baking the volume probe.

**Use when:** windows, glass panes, background glassware in EEVEE.
**Avoid when:** hero product glass / liquids / lens-like refraction (use Cycles, see `materials-glass-realism`).
**Failure signs:** glass invisible (Fac inverted), black/cut-out glass, sorting errors with Blended over other transparent objects, missing floor reflection behind Blended glass.
**Cost:** cheaper than refraction; Dithered needs more samples.
**Conflicts with other sources:** `materials-glass-realism` (Cycles) uses Light Path Is Shadow Ray → Glass/Transparent for windows. Same idea (cheap see-through window), different engine path. Both valid; pick by engine.
**Test to validate:** window + glass of water: Principled refraction vs archviz glass in EEVEE vs Cycles ground truth; ΔE and artifact count.
**Log:** 2026-11-06 — Extracted from eevee_full_course (Blender 4.4).
