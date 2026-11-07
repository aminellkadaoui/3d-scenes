---
id: lighting-negative-fill-flag
domain: lighting
status: Extracted
sources: [hQKJx1wXkfM@01:15, hQKJx1wXkfM@01:30, hQKJx1wXkfM@01:45]
blender: "5.2"
---
# Negative fill / light blocking (black flag invisible to camera)
**Principle:** Under an even environment (bright HDRI, overcast sky, white studio) the subject goes flat because light arrives equally from all sides. Removing light from one side creates the key/fill ratio. On set this is "negative fill" (black flag / duvetyne).

**Steps / settings (starting points):**
1. Plane facing the subject on the side that should fall into shadow (usually the side away from the brightest HDRI area) [hQKJx1wXkfM@01:15].
2. G Z Z (local axis) to slide it out. Distance about 0.5–1.5× subject height. Size about 1–2× subject height [hQKJx1wXkfM@01:30].
3. Material: Diffuse/Principled, Base Color black (0.0–0.02), Roughness irrelevant (the tutorial leaves Diffuse BSDF at 0.5 [hQKJx1wXkfM@01:40]) [hQKJx1wXkfM@01:30].
4. Object Properties > Visibility: Camera OFF [hQKJx1wXkfM@01:45]. Shadow ON (it must block). Glossy: OFF if it shows as a black blob in reflections. ON if a dark reflection helps define chrome/glass edges (a black card in product photography).
5. Scale it until the shadow side is about 1–2 stops under the lit side. Then rotate the HDRI to set the key direction [hQKJx1wXkfM@01:45].
6. Variant: a flag above (top negative) for "single source" moodiness under open sky.

**Use when:** HDRI-lit characters/products that look flat. Overcast exteriors. Glossy products that need dark reflection lines.
**Avoid when:** the scene is key-light dominated (little effect). The blocker would have to be enormous (then lower the HDRI and add a key instead).
**Failure signs:** visible black shape in reflections or refractions. Shadow side becomes black with no detail (too big or too close). Colour shift (blocked the coloured part of the HDRI).
**Cost:** none.
**Conflicts with other sources:** ZYk3OOf-gBk advises minimising HDRI use for products because of limited control [08:30]. Negative fill is how you regain control with an HDRI, so the two are complementary.
**Test to validate:** head model, uniform white world 1.0. A: no flag. B: flag 2×2 m at 0.8 m. Measure the cheek ratio (target ≥ 2:1) and confirm it is absent from the camera and from glossy surfaces.
**Log:** 2026-11-05 — Extracted from hQKJx1wXkfM.
