# Camera & lenses — knowledge (Blender 5.2)

Status: everything here is **Extracted** (sources + expert knowledge), untested in our pipeline. Cards: `techniques/camera-*.md`.
Sources in this file: dFK3C83k4Wo (camera rigs/transitions), HBWYieo5RmU (point of view), JQT9sT1YuAI (graph/rig principles), 4Mf2hgb1tP0 (eased transitions), Blender manual (Cameras page, F-Curve Modifiers page).

---

## 1. Core idea: the camera is the first creative decision, not the last
A generic CG frame happens when the camera is wherever the viewport was: 50 mm, ~1–2 m up, looking slightly down at a centered object. A professional frame starts from *what the viewer should feel and look at*, then sets **position (perspective) → focal length (crop) → height/angle (meaning) → focus (attention) → motion (energy)**.

## 2. Focal length, field of view, and perspective
- **Perspective is set by camera position, not focal length.** Size ratio between near and far objects depends only on their distances to the camera. Focal length crops. Zooming from 24 → 100 mm without moving = cropping the center of the 24 mm image. Moving back and using 100 mm to keep the subject the same size *changes* perspective: background appears larger/closer ("compression"), subject features flatten.
- Horizontal FOV on Blender's default 36 mm sensor: `hFOV = 2·atan(36 / (2·f))` → 18 mm 90°, 24 mm 74°, 35 mm 54°, 50 mm 40°, 85 mm 24°, 100 mm 20°, 135 mm 15°, 200 mm 10°.
- Panel: Camera Properties ▸ **Lens**: Type (Perspective / Orthographic / Panoramic & Custom are Cycles-only), Focal Length (or Lens Unit = Field of View), Shift X/Y, Clip Start/End.

### Starting points by shot type (starting points, not rules)
| Purpose | Focal (36 mm sensor) | Camera distance idea | Notes |
|---|---|---|---|
| Wide environment / establishing | 18–28 mm | close to foreground, show space | keep verticals straight (Shift); watch edge stretch on objects near frame corners |
| Natural documentary / walk-through | 28–40 mm | human distance | feels "being there" |
| Medium shot (person, product in context) | 40–60 mm | 2–4 m from person | neutral |
| Product hero / portrait | 70–105 mm | far enough that whole product fits | dFK3C83k4Wo uses 90 mm for a chair orbit [dFK3C83k4Wo@00:45]; minimal distortion, clean background |
| Telephoto compression / stacked background / detail | 135–300 mm | far | background appears huge and close; small camera moves = big screen motion; shake amplified |
| Macro / extreme detail | 60–105 mm close focus | very close | DoF already thin — use higher f-stop |
Wide lens close = energy, scale, distortion. Long lens far = calm, premium, flattened, isolated.

## 3. Sensor size and Sensor Fit
- Camera Properties ▸ **Camera**: Sensor Fit (Auto / Horizontal / Vertical) and Size (Width/Height). Default 36 mm, Auto.
- **Auto** applies the sensor size to the *larger* image dimension. So with 1080×1920 (9:16) the 36 mm is applied vertically: a 50 mm lens gives the *vertical* FOV that 16:9 gives horizontally — the horizontal view becomes very narrow (~23°). When re-framing a 16:9 shot to 9:16, expect to lower focal length (often ×0.55–0.65) or step back, and rebuild composition rather than crop.
- Matching a real camera (Super 35 ≈ 24.9×18.7 mm, full frame 36×24) only matters when matching footage/tracking; otherwise keep 36 mm and think in "full-frame equivalent" focal lengths.

## 4. Camera height and angle (meaning)
- Eye level ≈ 1.5–1.7 m standing (1.2 m seated) = neutral, natural, connection [HBWYieo5RmU@03:30–03:45].
- Low angle (camera below subject's center, looking up) = power, size, heroic; high angle (looking down) = small, vulnerable, overview [HBWYieo5RmU@03:30].
- Tendency in documentaries: wides slightly high, close-ups straight-on, authority from low [skool-rr-cinematic-composition@08:42–09:02]. Pair shots wide → close: the wide gives context, the close reveals the detail that changes the meaning → `techniques/camera-wide-establish-then-close-reveal.md` [skool-rr-cinematic-composition@05:23–08:20].
- Tabletop product: camera around product mid-height to slightly above (10–30° down) reads as "on a table in front of you"; at product base height = heroic/monumental.
- Horizon placement follows camera tilt: camera level → horizon at frame center. To put the horizon on a third without tilting, use **Shift Y** (see §7).
- Roll must be exactly 0 unless a Dutch angle is motivated. A 1–3° accidental roll is a classic error.
- Slop sign: camera height that matches no human/rig position (e.g. 2.7 m floating in a room, or 0.4 m for a normal interior) without story reason.

## 5. Depth of field (DoF) in Blender
- Camera Properties ▸ **Depth of Field**: Focus Object (or Focus Distance; object overrides distance), Aperture: **F-Stop**, Blades, Rotation, Ratio (manual: Ratio < 1 / > 1 stretches bokeh for anamorphic look; Blades ≥ 3 for polygonal bokeh, 0 = circular).
- **Physically based**: blur = f(F-Stop, focal length, focus distance, scene scale in meters, sensor). Therefore:
  - Scene must be at real scale (Unit Scale 1, object Dimensions real). A wrongly small scene + "normal" f-stop = miniature; a correct scene + f/0.1–0.8 = miniature too, because those apertures only produce that thin a focus plane on small subjects at short distance (macro) — the brain infers the subject is tiny ("tilt-shift" effect).
  - Realistic f-stops: f/1.4–2.8 for strong portrait separation; f/2.8–5.6 for natural cinema; f/5.6–11 for products that must be fully sharp, wide environments; macro f/8–16.
  - Long lenses at the same f-stop and framing blur backgrounds more (background is magnified). So 100 mm f/4 can look "shallower" than 35 mm f/2.
- Focus target: an Empty named `FOCUS_<shot>` as Focus Object; animate it for rack focus (§ animation.md). Focus on eyes (people) or on the product's brand/feature face.
- Bokeh: 7–9 Blades with slight Rotation reads like a real lens; Blades 0 is the "perfect CG circle". Ratio only for intentional anamorphic look.
- Slop signs: ultra-shallow DoF on every shot; half the product soft; focus on background; blur used to hide weak environments.

## 6. Shutter and motion blur
- Render Properties ▸ **Motion Blur**: Position (Start / Center / End), **Shutter** in frames. The 180° shutter rule (exposure = half the frame interval, i.e. 1/48 s at 24 fps) → **Shutter 0.5** (Blender's default). 0.25 = crisper/staccato (action, "Saving Private Ryan" look); 1.0 = smeary/dreamy. Cycles also offers Rolling Shutter; EEVEE has Steps for blur accuracy on curved/rotational motion.
- Keep motion blur ON for any moving camera or fast objects; whip transitions depend on it [dFK3C83k4Wo@04:45 cut placement relies on speed].
- Render at the delivery fps (usually 24/25/30 for VSL; 60 only if the platform/brand needs it). Blur and timing must be judged at the final fps.
- Slop signs: razor-sharp frames during fast camera moves (strobing), or blur added in post on CG with obvious edge errors.

## 7. Lens shift vs tilt (architecture & products)
- Tilting a camera up/down makes vertical lines converge (keystoning). Real architecture photographers use shift lenses: keep the camera level and shift the image.
- Blender: keep Rotation X = 90° (level), use Lens ▸ **Shift Y** (fraction of sensor; 0.1–0.3 typical) to move the horizon/subject up or down in frame without converging verticals. Shift X for lateral framing in symmetric shots.
- Use for: interiors, buildings, tall products (bottles, devices), any shot with strong verticals. Don't over-shift with wide lenses (edge stretch increases).
- Deliberate convergence (low angle up a skyscraper) is fine when it's the point.

## 8. Aspect ratio by platform
- 16:9 (1920×1080 / 3840×2160): YouTube, VSL landing pages. 9:16 (1080×1920): Reels/TikTok/Shorts — UI covers bottom ~20–25 % and right edge. 1:1 / 4:5: feed ads.
- **Letterbox ≠ cinematic.** Black bars over a 16:9 render of a weakly composed frame add nothing. If a 2.39:1 look is intended, set the render resolution to it and compose for it; for VSL delivered in 16:9, prefer real 16:9 composition.
- For multi-format deliveries, make one camera per format (not a crop) or compose a "protected" central area and check both guides (Camera ▸ Viewport Display ▸ Safe Areas; and Composition Guides).

## 9. Synthetic stability vs operated camera
- Pure keyframes = perfectly stable, perfectly level — correct for motion-control product commercials, wrong for "filmed in the world" scenes.
- Add operated feel with subtle F-curve **Noise** modifier on a separate shake layer, low frequency (Scale 30–80), low rotation strength (~0.3–1°), different Phase per axis, fade with Restrict Frame Range Blend In/Out. See `techniques/camera-handheld-noise-modifier.md`.
- Reduce noise as focal length grows (angular noise is magnified at long lenses).

## 10. Camera rigs (summary; details in animation.md)
- Pivot Empty orbit rig (camera parented to an Empty at the subject) [dFK3C83k4Wo@01:30]; Track To / Damped Track to an aim Empty; Follow Path for long travel; Add Camera Rigs extension (Dolly, Crane with Arm Height/Length, 2D rig).
- Naming: `SH##_Cam`, `SH##_Pivot`, `SH##_Focus`, one collection per shot [dFK3C83k4Wo@01:15]. Multiple cameras switched with Timeline markers (`Ctrl+B` Bind Camera to Markers) [dFK3C83k4Wo@05:00].

## 11. Clip start/end
- Clip Start too small (0.001 m) on large scenes causes Z-fighting in viewport/EEVEE; too large clips nearby foreground. Typical: 0.05–0.1 m start, end just beyond farthest needed geometry.

## 12. Slop signs (camera) — checklist
- [ ] Default 50 mm from a random viewport angle (no decided distance/perspective).
- [ ] Camera at a height no person/rig would be at, no story reason.
- [ ] Accidental roll / tilted horizon / converging verticals on architecture.
- [ ] Ultra-shallow DoF everywhere (f/0.1–1), miniature look, or focus on the wrong thing.
- [ ] Subject dead-centered in every shot with identical framing.
- [ ] Same focal length and height on every shot (no shot-size variety: wide → medium → close).
- [ ] Wide lens too close to products (bulging packaging/edges).
- [ ] No motion blur on moving cameras; or extreme blur hiding everything.
- [ ] Perfectly smooth "drone-in-vacuum" moves in scenes meant to feel filmed.
- [ ] Letterbox bars as a substitute for composition.
- [ ] 16:9 render cropped to 9:16 losing the subject or putting it under platform UI.

## 13. Quick decision recipe
1. What does the viewer feel? (power → low angle; intimacy → eye level, 50–85 mm close; scale → wide, far, small subject; premium product → 85–105 mm, slightly above, f/5.6–8.)
2. Place camera at the distance that gives that perspective; set focal to frame.
3. Height and level; Shift for verticals.
4. Focus Empty + realistic F-Stop.
5. Motion blur 0.5 at delivery fps.
6. Check composition guides at final aspect + overlay plan (composition.md).
