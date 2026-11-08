---
id: materials-screen-display-effects
domain: materials
status: Reproduced
sources: [blender-tasty-tutorials-led-screen-2.93, realistic-rgb-screen-shader]
blender: "5.2"
---
# Screen display effects: LED bulbs vs RGB subpixels (vs plain)

**Rule:** when the user asks for a "screen effect" (تأثير السكرين / LED / RGB pixels / realistic screen), do NOT invent a new look. Offer these options, build them in a **duplicate of the shot's scene** (one option per copy, e.g. `<scene> LED`, `<scene> Screen 2`), render the same frame of each, apply the project grade, and let the user pick. Never touch the original scene.

| Option | What it looks like | Best for | Cost |
|---|---|---|---|
| **A. LED bulbs** (geometry) | every pixel is a real glowing dome with dark gaps; picture pixelated per bulb | stylised close-ups, billboards, "LED wall" look, hero inserts | ~138k instances at 480×288 (44-tri bulb); frame change ~0.01 s in EEVEE |
| **B. RGB subpixels** (shader) | the real image stays sharp; R/G/B stripes show up on close-ups like a real monitor | realistic monitors/TVs, macro push-ins on UI | almost free (one texture + math) |
| **C. Plain emission** (current default) | flat clean screen | wide shots where pixels can't be seen | free |

## A. LED bulbs (Geometry Nodes version of the particle tutorial)
1. New object in its own collection linked only to the copy scene. GN: `Grid` sized to the screen face (W × H), Vertices X/Y as modifier inputs. **Size the LEDs for the real screen, not the tutorial's billboard**: on a 0.62 m desktop monitor start at **480 × 288** (≈1.3 mm pitch) so UI details still read; 160 × 96 was rejected as far too coarse. Put LEDs at cell centres: grid size × (n−1)/n.
2. Store the 0–1 UV on the points as named attribute `led_uv` (u = (i+0.5)/n). Check it isn't mirrored/flipped with `look`.
3. `Instance on Points` → a low-poly bulb (cube, 1-segment bevel, flat base, ~50 tris; hidden source object). Scale = pitch × `LED Size` (0.85). Don't realize.
4. Bulb material: `Attribute` (type **Instancer**, `led_uv`) → the same movie Image Texture (same datablock + frame settings, **Closest**) → the screen's existing colour chain (copy the HueSat/curve nodes so colours match) → Emission. Rim: Mix(Fac = Fresnel IOR 1.12) of Emission and Glossy (rough 0.073). The tutorial's Principled glass (Transmission 1, IOR 1.45) is the Cycles version.
5. Original screen surface becomes the dark backing: multiply its emission by a `LED_Gap_Glow` value (0.03). Delete nothing.
6. Emission ≈ 1.5× the plain screen's strength (5.08 → 8) under AgX High Contrast, then compare brightness with `look` at the same frame/camera.
   (Tutorial original: Hair particles from vertices of a Simple-subdivided plane, Instance Object, Texture Coordinate **From Instancer** → Generated, Emission 30 in Filmic.)

## B. RGB subpixel mask (shader only)
1. Mask image: square, black background, three vertical rounded bars red / green / blue each ~29 % wide (Non-Color, Linear). Generate it if missing.
2. `Texture Coordinate.UV` → `Mapping` Scale = (pixels across, pixels down) keeping square cells: e.g. 640 × 383 on a 0.617 × 0.369 m screen → mask Image Texture.
3. Separate Color(screen colour after its colour chain) × Separate Color(mask) per channel (3 Math Multiply) → Combine Color → Emission Color.
4. **Keep it subtle — the content must stay the hero.** Mix the mask with white: `Mix(A = white, B = mask, Fac = RGB Effect Strength)` before the Separate node, start **0.5** (1.0 was rejected: the effect became more eye-catching than the screen). Compensate emission = base / (1 − strength × (1 − mask mean)); mask mean ≈ 0.27 → 5.08 → 8.0 at 0.5.
5. Add Shader: Emission + Glossy (rough 0.05, colour 0.04) for the glass layer.
   Tutorial original: mapping ~670 × 250, emission 10.

**Failure signs:** moiré bands on wide shots (B: lower the count or keep option C for wides; A: lower Vertices or rely on DOF/motion blur); image mirrored (fix UV direction); colours off vs the old screen (colour chain not copied); screen too dark after mask (emission not compensated).
**Log:** 2026-11-08 — user feedback: LED cells must be much smaller (scale to the real screen), RGB effect at full strength is too loud → strength 0.5.
2026-11-08 — built both on a copy of a VSL Analytics screen shot (EEVEE, AgX HC), rendered frame 570 of each for the user to choose.
