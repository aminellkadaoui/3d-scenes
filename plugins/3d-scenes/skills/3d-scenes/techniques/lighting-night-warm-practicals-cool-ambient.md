---
id: lighting-night-warm-practicals-cool-ambient
domain: lighting
status: Extracted
sources: [a-IdD-RGb4Q@18:15, a-IdD-RGb4Q@18:45, a-IdD-RGb4Q@19:15, bWSUxpJ8UHk@03:30, bWSUxpJ8UHk@04:15, bWSUxpJ8UHk@05:00, bWSUxpJ8UHk@00:45]
blender: "5.2"
---
# Night: weak cool ambient + warm motivated practicals + atmosphere
**Principle:** Night is not "a dark render". It is low ambient (moon/sky, cool) plus a few strong, warm, visible sources (practicals) whose light pools shape the frame. Warm vs cool is complementary contrast that separates subject from environment [a-IdD-RGb4Q@18:45]. Fog and wet surfaces carry light through space (cones, halos, specular streaks) [bWSUxpJ8UHk@05:00][bWSUxpJ8UHk@00:45].

**Steps / settings (starting points)** (metres, AgX, adjust Exposure, not light count):
1. Ambient: World colour deep blue (about 7000–12000 K equivalent, RGB about 0.02–0.05 strength) or a Sky at night/moon. Author hack: one scene-sized blue Area light, weak [a-IdD-RGb4Q@18:15]. Shadows should stay readable (not RGB 0).
2. Practicals: the visible source mesh gets Emission (strength 10–50, so it's the brightest thing) [bWSUxpJ8UHk@03:30], plus a real light that does the illumination: Disk Area 0.4–0.6 m under a street-lamp head [bWSUxpJ8UHk@04:15] (source: Disk 1 m, ≈250 W, Spread 180°, EEVEE Legacy [bWSUxpJ8UHk@04:35], seen in frame), 300–1500 W, Temperature 2000–2700 K (sodium/tungsten) or 3500–4500 K (LED), Spread 120–150°. Interior lamp: Point Radius 0.05–0.1 m, 20–80 W, 2700 K.
3. Subject accent: warm spot on the hero (orange vs blue ambient) [a-IdD-RGb4Q@18:45] — source values seen in frame: Spot, peach colour, **50 W, Radius 0.067 m, Spot Size 12.6°, Blend 0.15** on a ~10 cm jar [a-IdD-RGb4Q@19:20]. Separate warm light on the background so it doesn't go black [a-IdD-RGb4Q@19:15].
4. Atmosphere: bounded cube with Principled Volume, Density 0.005–0.03 (0.02 in the source [bWSUxpJ8UHk@05:00]) with Noise → Color Ramp → Density for breakup. Note: the source actually wires the ramp into Emission Strength (frame-verified), i.e. self-glowing fog patches. Use that only for stylised "lit mist", and prefer lamp-lit density variation.
5. Wet ground: roughness 0.05–0.2 patches via noise → ramp [bWSUxpJ8UHk@00:45] so lamps streak on the road.
6. Exposure: set Color Management Exposure (+1 to +3) instead of boosting every light. Keep the darkest important areas about 2–4% display value, not 0.

**Use when:** night streets, moody interiors, thrillers, hooks needing tension.
**Avoid when:** the brand look is clean/bright (use dusk instead). A saturated teal+orange cliché without a motivated source.
**Failure signs:** shadows pure black (no ambient). Every light the same intensity/colour. Lamp heads not the brightest thing in frame. Light pools without visible sources. Neon cyan/magenta with no in-scene emitters. Fog uniform grey "soup" (density too high, no noise).
**Cost:** volumes are expensive (Cycles especially). Use bounded cubes. EEVEE: tune Volumes resolution/steps.
**Conflicts with other sources:** scene-sized blue area light [a-IdD-RGb4Q@18:15] vs world/sky ambient. Prefer the world (correct reflections/sky). Use the area hack only for small product sets.
**Test to validate:** street with two lamps. A: lamps only. B: + blue ambient. C: + fog. D: + wet road. Check shadow detail (no 0 values), the hierarchy (lamp > pool > ambient), and render time per step.
**Log:** 2026-11-05 — Extracted from a-IdD-RGb4Q, bWSUxpJ8UHk.
