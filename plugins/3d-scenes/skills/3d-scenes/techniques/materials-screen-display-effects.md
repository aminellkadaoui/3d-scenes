---
id: materials-screen-display-effects
domain: materials
status: Reproduced
sources: [blender-tasty-tutorials-led-screen-2.93, realistic-rgb-screen-shader]
blender: "5.2"
---
# Screen display effects: LED bulbs vs RGB subpixels (vs plain)

**Approved look (2026-11-08):** RGB subpixel stripes over the screen video at full strength, applied to every computer screen in the project. This is the default — reproduce it with `scripts/screen_fx.py`.

**Always ask the user first which pixel shape they want** (one short question, show the options):
| Shape | Look | How |
|---|---|---|
| **Stripes** (default, approved) | red/green/blue bars like a real LCD | `screen_fx.apply(mats, shape="stripes")` |
| **Dots** | red/green/blue round subpixels | `shape="dots"` (mask is dim → emission is boosted ×13 automatically) |
| **Circles** | one full-colour round cell per pixel, LED-wall feel | cheap: `shape="circles"`; true LED (each bulb one colour, real gaps): option A below |
| **Squares** | one full-colour rounded-square cell per pixel | cheap: `shape="squares"`; true LED with square bulbs: option A |
| Plain | no effect | wide shots where pixels can't be seen |

Then also ask (or use the defaults): how fine — `cells` across the screen (default 640 for a 0.62 m monitor, keep cells square: cells_y = cells_x × H / W), and strength (default 1.0).

**Workflow:** test the chosen shape on a duplicate of one scene, render one graded frame on the Mac for the user, then on approval apply the same node group to every screen material in every scene with one `apply()` call. Delete the test scenes afterwards (only when the user says). Never change the originals before approval.

```python
import sys; sys.path.insert(0, "<skill>/scripts"); import screen_fx as fx
fx.apply(["Win11_Screen.005", "Win11_Screen_Revisions"], shape="stripes", cells=(640, 383), strength=1.0)
```
`apply()` inserts group `RGB_Screen_FX` before every Emission Color input (all video paths), compensates Emission Strength for the mask's average (stripes ×3.8), and adds the soft faint glass (Glossy rough 0.25, colour 0.022). The mask is generated and packed inside the .blend — no texture file. One group = one slider (`RGB Effect Strength`) for all scenes.

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
4. Expose the strength: `Mix(A = white, B = mask, Fac = RGB Effect Strength)` before the Separate node. **Default 1.0 (full)** — the user liked the strong look; don't lower it unless asked. Compensate emission = base / (1 − strength × (1 − mask mean)); mask mean ≈ 0.27 → 5.08 → 17.8 at 1.0.
5. Add Shader: Emission + Glossy for the glass layer — keep the reflection soft and faint: roughness **0.25**, colour **0.022** (0.05 / 0.04 gave a hard white patch the user rejected).
   Tutorial original: mapping ~670 × 250, emission 10.

**Failure signs:** moiré bands on wide shots (B: lower the count or keep option C for wides; A: lower Vertices or rely on DOF/motion blur); image mirrored (fix UV direction); colours off vs the old screen (colour chain not copied); screen too dark after mask (emission not compensated).
**Log:** 2026-11-08 — approved: stripes, strength 1.0, applied to all four scenes' monitor screens; user wants to be asked for the shape (stripes / circles / squares) each time.
2026-11-08 — user feedback: LED cells must be much smaller (scale to the real screen), the glass reflection must be soft and faint (rough 0.25, colour 0.022); the strong RGB effect (1.0) is liked — don't reduce it unasked. Ask before reading feedback as "reduce" when the user may be praising.
2026-11-08 — built both on a copy of a VSL Analytics screen shot (EEVEE, AgX HC), rendered frame 570 of each for the user to choose.
