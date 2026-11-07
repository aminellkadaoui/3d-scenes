---
id: compositing-grade-curves-split-tone
domain: compositing
status: Extracted
sources: [0M0-TESgB7E@00:15, 0M0-TESgB7E@00:30, lE308jCAT2o@03:45, lE308jCAT2o@04:45, 1MyARLB8KzY@10:30]
blender: "5.2"
---
# Minimal in-Blender grade: gentle S-curve, lifted blacks, subtle split tone

**Principle:** a grade should *organise* the image (separation of subject from background, warm vs cool), not decorate it. Complementary split toning (cool shadows, warm highlights) adds depth. A slight black lift (film toe) avoids dead digital black. Do it *after* the view transform conceptually. In Blender's compositor the nodes act on scene-linear data before the display transform, so keep moves small.

**Steps / settings:**
1. RGB Curves (C curve): a soft S, around ±0.02–0.04 at the quarter points. Black output 0.01–0.03, white output 0.97–1.0 (optional) [0M0@00:15], [lE308@04:45].
2. Color Balance (Lift/Gamma/Gain; linear in 5.0+): Lift a hair toward cyan/teal; Gain a hair toward orange; Gamma neutral or slightly warm [0M0@00:30]. Or Offset/Power/Slope (ASC-CDL) [lE308@03:45]. Or the **Split Toning** / **Tune Image** assets (5.0).
3. Keep saturation ≤ +10%. Check skin, logo and product colours stay true.
4. A/B with Mute (M) every node. Each node must improve the image on its own.
5. If the editor or colourist grades in Resolve, **skip this** (or keep it to the bare minimum) and deliver a neutral render.

**Use when:** delivering final pixels from Blender, or a mood that must be locked in 3D.
**Avoid when:** footage will be graded with live action in Resolve/Premiere (double grade); brand colours must be exact.

**Failure signs:** teal-orange everywhere, including product colours; crushed blacks (no detail < 2%); milky, faded blacks from too much lift; nodes fighting each other (gamma darkens, brightness re-brightens [lE308@05:45]); posterisation/banding from steep curves.

**Cost:** negligible.

**Conflicts with other sources:** lE308 uses Exposure + Gamma + Brightness, which partially cancel each other. Prefer exposure at the light/Color Management level.

**Test to validate:** a portrait/product scene. No grade vs grade. Measure: brand-colour ΔE < 3, % pixels < 0.02 luminance, blind preference.

**Log:** 2026-11-05 — Extracted from 0M0-TESgB7E, lE308jCAT2o, 1MyARLB8KzY.
