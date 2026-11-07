---
id: color-view-transform-exposure
domain: color
status: Extracted
sources: [lE308jCAT2o@00:30, lE308jCAT2o@00:45, 0M0-TESgB7E@00:00, 1MyARLB8KzY@10:00, gmGMsKJ6xd8@08:15]
blender: "5.2"
---
# Pick the view transform first, set exposure with False Color, then choose a look

**Principle:** the renderer computes scene-linear light with unbounded range. The view transform is the "film stock" that maps it to the display. **Standard** clips anything above 1.0 to flat white and keeps saturated colours saturated to the end. That is why bright lights become blown, cyan/yellow-skewed blobs. **AgX** (default since 4.0) rolls highlights off over ~16.5 stops and desaturates toward white like film. **Khronos PBR Neutral** keeps product/base colours accurate in well-exposed scenes. **ACES 1.3 / 2.0** (built in since 5.0) suit photoreal and pipeline matching.

**Steps / settings:**
1. Render Properties › Color Management › Display: **sRGB** (for web/VSL; see color-management.md about Rec.1886).
2. View Transform:
   - Default/cinematic/mixed lighting → **AgX**, Look **None** or **Base Contrast**; **Punchy** only if the scene is flat [0M0-TESgB7E@00:00].
   - Product hero shots with brand colours → **Khronos PBR Neutral** (brand red stays red).
   - Photoreal or matching ACES footage → **ACES 2.0** (gentler) or **ACES 1.3**.
   - UI, flat graphics, colour-exact logos in a 3D scene → **Standard**, but only if no light source exceeds 1.0.
3. Temporarily switch the View to **False Color** [lE308jCAT2o@00:45]. Set exposure so the subject is in the green/grey middle band, highlights only yellow/orange in small specular areas, and no large red/white areas. Then switch back.
4. Exposure: adjust **Color Management › Exposure** (stops) or better, the light power. Don't fix exposure with Brightness/Contrast in comp.
5. Gamma in Color Management: leave at 1.0.

**Use when:** before any lighting judgement. Lighting under the wrong view transform leads to wrong light powers.
**Avoid when:** don't switch the view transform late in a project. All lighting and material decisions shift.

**Failure signs:** Standard + emissive/strong lights = hard clipped highlights with hue skew (orange lights turn yellow, blue turns cyan); AgX + Punchy on saturated scenes = garish and over-contrasty; AgX on saturated brand colours = slightly desaturated or shifted logo colour (switch to PBR Neutral); grey, washed scene under AgX (underexposed and boosted in comp; fix exposure instead).

**Cost:** none.

**Conflicts with other sources:** gmGMsKJ6xd8@08:15 uses "AgX or Filmic". Filmic is deprecated in 5.x and superseded by AgX. 1MyARLB8KzY uses a "Medium High Contrast" look; its name depends on the view transform.

**Test to validate:** one scene with an emissive orange lamp plus a red logo. Render under Standard / AgX / PBR Neutral / ACES 2.0. Measure clipping % (pixels at 1.0 in any channel), logo ΔE against the brand hex, and lamp hue shift.

**Log:** 2026-11-05 — Extracted from lE308jCAT2o, 0M0-TESgB7E, 1MyARLB8KzY, gmGMsKJ6xd8 + Blender 5.2 manual (Displays & Views page).
