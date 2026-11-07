---
id: lighting-gobo-motivated-patterns
domain: lighting
status: Extracted
sources: [ZYk3OOf-gBk@09:30, ZYk3OOf-gBk@10:00, KgqyWeF09wE@03:00, KgqyWeF09wE@03:30]
blender: "5.2"
---
# Gobos / cookies: motivated light patterns (window, foliage, blinds)
**Principle:** A patterned light implies an off-screen world (window, trees) and breaks uniform illumination into shapes, which creates visual interest, depth and a brightness hierarchy. Sun patches are the brightest value in a real sunny interior. Ducky keeps them "almost overexposed… brighter than the establishing light" [KgqyWeF09wE@03:30].

**Steps / settings (starting points):**
A) Physical cookie (both engines, recommended): a plane with the window/leaf alpha mask (or real geometry: window frame, blinds, branches) placed between a Sun/Spot and the subject. Camera visibility OFF. Shadow ON. Edge softness = light size (Sun Angle 0.5–2°, Spot Radius 0.05–0.2 m) and cookie-to-surface distance. Always physically consistent.
B) Cycles node gobo: Spot light [ZYk3OOf-gBk@09:30], widen spot size to cover the area, light nodes: Texture Coordinate (Normal) → Mapping → Image Texture (gobo) → Emission Color [ZYk3OOf-gBk@09:45]. Increase light Radius slightly to soften [ZYk3OOf-gBk@10:00].
B2) Cycles projector variant (frame-verified in Ducky [KgqyWeF09wE@03:40]): an **Area light with Spread = 0°** + light nodes Emission Color = animated window gobo video/image, about 22.5 W in a living-room scale scene. Spread 0° keeps the projected texture coherent.
C) Intensity: set the gobo patch about 1–2 stops brighter than the main establishing light, just under clipping [KgqyWeF09wE@03:30]. Use the False Color view to check.
D) Animate slightly (moving leaves, drifting cloud) for life [KgqyWeF09wE@03:15].
E) Temperature: sun patch 4500–5500 K against a cooler skylight fill (7000–10000 K) for natural interiors.

**Use when:** interiors that need sunlight, flat matte products, backgrounds that are too even, mood shots (blinds = noir).
**Avoid when:** the pattern has no plausible source in the scene's world (leaf shadows in a windowless studio product shot can still work stylistically, but not in realism). Too many patches = busy.
**Failure signs:** gobo pattern sharpness inconsistent with sun size. Pattern doesn't match the visible window shape/direction. Patches clipped to flat white with lost texture. Repeated identical patterns.
**Cost:** physical cookie: low. Alpha cutouts in Cycles add transparent bounces (keep Transparent bounces ≥ 8).
**Conflicts with other sources:** none. The node-gobo method [ZYk3OOf-gBk@09:45] is Cycles-only. Prefer A for engine independence.
**Test to validate:** room corner + chair. A: window light only. B: + sun through a cookie at +1.5 stops. Check the histogram hierarchy (patch > fill > shadow) and that the shadow direction matches the window.
**Log:** 2026-11-05 — Extracted from ZYk3OOf-gBk, KgqyWeF09wE.
