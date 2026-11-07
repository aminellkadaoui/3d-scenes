---
id: lighting-gradient-reflection-cards
domain: lighting
status: Extracted
sources: [WreZ_VKDn4M@04:00, WreZ_VKDn4M@04:30, WreZ_VKDn4M@05:45, ZYk3OOf-gBk@07:00, ZYk3OOf-gBk@07:45, ZYk3OOf-gBk@08:15, hQKJx1wXkfM@01:00, a-IdD-RGb4Q@15:00]
blender: "5.2"
---
# Gradient strip lights / emissive cards for glass, metal and glossy products
**Principle:** On glass, chrome and glossy surfaces you see reflections of the lights, not their illumination. A uniform white rectangle reflected = instant CG tell [WreZ_VKDn4M@04:00][ZYk3OOf-gBk@07:00]. Real studio strip boxes have gradients (diffusion falloff). Reflected in a curved surface, a gradient strip gives the smooth "edge-to-dark" contour that defines the shape.

**Steps / settings (starting points):**
A) Cycles: textured area light. Light selected > Shader Editor > (5.x: light node tree) Emission Color ← Image Texture (softbox / "elliptical sharper" gradient) [ZYk3OOf-gBk@07:15], or procedural: Texture Coordinate (UV) → Mapping → Gradient Texture (Quadratic/Spherical) → Color Ramp (Spline) → Emission Color.
B) Both engines: emissive plane. Plane → material: Emission (or Principled Emission) colour ← Texture Coordinate (Generated/UV) → Mapping (rotate Z to orient) → Gradient Texture → Color Ramp set to Spline, soft black-to-white [WreZ_VKDn4M@05:45]. Bright side toward the BACK of the product [WreZ_VKDn4M@06:00]. Object > Visibility > Camera OFF [WreZ_VKDn4M@05:15].
C) Layout for a bottle (about 25 cm): two tall strips (about 0.15 × 0.8 m, scaled in Z) behind-left and behind-right at about 120–150° from the camera axis, 0.4–0.7 m away, emission strength 5–20. Optional two front-side strips so metal doesn't go "too black" [ZYk3OOf-gBk@08:15]–[08:30]. Back plane for a glass silhouette (bright-field) [WreZ_VKDn4M@05:00].
D) Glass that "won't light": light the backdrop behind it instead [a-IdD-RGb4Q@15:00].

**Use when:** glass, liquids, chrome, glossy plastic, car paint, phones/screens, cosmetics.
**Avoid when:** matte subjects (no benefit). Physically matched HDRI-integration scenes (non-physical light shapes may conflict). EEVEE with option A (light nodes are ignored, so use B).
**Failure signs:** hard-edged rectangles in reflections. Highlights with no falloff. Bottle edges disappearing into the background (no contour). Metal mostly black or mostly white. Cards visible in the camera or refraction.
**Cost:** emissive meshes are sampled less efficiently than lights in Cycles (keep Emission Sampling = Auto). Little cost in EEVEE.
**Conflicts with other sources:** the "not physically accurate" admission [ZYk3OOf-gBk@07:30] is fine for commercial product work. The gradient is an art-directed diffusion simulation.
**Test to validate:** chrome cylinder + glass bottle. A: plain area lights. B: gradient strips at the same positions. Judge contour continuity (both silhouette edges show a bright line) and absence of rectangle reflections.
**Log:** 2026-11-05 — Extracted from WreZ_VKDn4M, ZYk3OOf-gBk, hQKJx1wXkfM, a-IdD-RGb4Q.
