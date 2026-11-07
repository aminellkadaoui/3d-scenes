# Lighting: 3D Scenes knowledge file
Read this before lighting any Blender scene. Target: Blender 5.2 (Cycles + EEVEE), scene units = metres, View Transform = AgX, Exposure 0 unless stated. All numbers are **starting points**. Verify with a clay render and the QA checklist (section 5). Claims from videos cite `[videoId@mm:ss]`. Uncited claims are general lighting and photography knowledge or the Blender 5.2 manual. Status of every video-derived technique: **Extracted** (not yet validated in our own tests).

Sources analysed: hQKJx1wXkfM (Extra 3d, character), Hyhew7kuhgA (Poly Playground, world hack), WreZ_VKDn4M (Extra 3d, product), ZYk3OOf-gBk (Digitalist, 8 product tricks), KgqyWeF09wE (Ducky 3D, bright lighting), a-IdD-RGb4Q (Ali Khadoor, Arabic fundamentals), CPZtbXTVdWs (Physical Addons, day/night, promo), bWSUxpJ8UHk (None Design 3D, night road). Analyses: `sources/<id>.md`. Cards: `techniques/lighting-*.md`.

---

## 0. The 10-second version
1. **One dominant, motivated source per area.** Know where the light comes from in the story world [KgqyWeF09wE@00:45][a-IdD-RGb4Q@18:30].
2. **Never key from the camera.** Key 30–60° off axis, 20–45° up [hQKJx1wXkfM@00:15].
3. **Keep the shadow. Fill it, don't erase it.** Bounce card or negative fill, not a second key [a-IdD-RGb4Q@01:15][ZYk3OOf-gBk@01:30][hQKJx1wXkfM@01:15].
4. **Separate the subject.** Rim/back light, or background brighter or darker than the subject's edge [WreZ_VKDn4M@01:45].
5. **Glossy/glass = design reflections** (gradient strips), not illumination [WreZ_VKDn4M@04:30][ZYk3OOf-gBk@07:00].
6. **Kelvin, not random RGB.** Warm/cool contrast with a reason [a-IdD-RGb4Q@18:45].
7. **Exposure in Color Management, not by cranking lights.** Keep highlights unclipped and shadows above black.
8. **Atmosphere makes light visible** (fog, haze, wet surfaces) [bWSUxpJ8UHk@05:00].
9. **Test in clay first**, then materials, then colour.
10. **Each light has one job.** If you can't name it, delete it.

---

## 1. Principles

### 1.1 Motivated light
Every significant light should be explainable by a source that exists in the scene's world, on or off screen: window, sun, lamp, screen, sky, a reflection off a wall. Unmotivated light (a rim from nowhere in a realistic room, coloured light with no emitter) is the strongest "CG / AI" tell. Stylised studio product work is the exception: its motivation is the photo studio itself (softboxes, strips, reflectors), so it must still behave like a studio.
- Practice: before adding a light, write its name as a role and a source ("KEY – window camera-left", "RIM – practical lamp behind"). Name Blender objects that way.
- Reference photos decide time-of-day lighting: noon is white-slightly-yellow, overhead, hard shadows; sunset is a low angle, softer and orange; night is dim and blue [a-IdD-RGb4Q@17:30]–[18:15].

### 1.2 Direction reveals form
Shape is perceived through the gradient from lit to shadow (the terminator) and through the cast shadow. Light along the camera axis kills both [hQKJx1wXkfM@00:15].
- Front (0°): flat, beauty-only. 45° side-top: classic modelling (Rembrandt triangle on faces) [hQKJx1wXkfM@00:15]. 90° side: dramatic split. 135–180° back: rim/silhouette.
- Elevation: 20–45° reads natural. Overhead (70–90°) = noon/interrogation, eye sockets go dark. Under-light = horror/unnatural (motivate it with a screen or fire).
- Grazing light (nearly parallel to a surface) exaggerates texture. Use it for fabric, embossing, terrain. Avoid it on skin you want smooth.
- Orbit lights around the subject with Pivot = 3D Cursor + R R so you change only the angle [hQKJx1wXkfM@00:00][WreZ_VKDn4M@03:00][ZYk3OOf-gBk@01:00].

### 1.3 Key / fill / rim and ratios
| Role | Job | Typical source |
|---|---|---|
| Key | defines direction, main shadow | area/sun/window |
| Fill | sets how dark the shadow side is (contrast) | bounce card, big dim area light, sky/world |
| Rim/back | separates silhouette from background | small area/spot behind, 120–170° from camera |
| Kicker / accent | a highlight on one edge, eye light, product glint | small area, low power |
| Background / set light | controls background value independently | area/spot on wall or cyc |
| Practical | visible source in frame (lamp, screen) | emissive mesh + real light |

**Key:fill ratios** (measured as luminance on the subject's lit vs shadow side, not as wattage):
- 2:1 (1 stop): bright, commercial, e-commerce, explainers.
- 4:1 (2 stops): standard cinematic, most VSL hero shots.
- 8:1–16:1 (3–4 stops): low-key drama, thriller hooks, night.
- Rim power start: about 1/5 of the key at similar distance (key 25 W / rim 5 W) [ZYk3OOf-gBk@04:15]–[05:00]. It must read as a thin bright edge, not a second key.

### 1.4 Contrast and exposure
- Set exposure in **Render Properties > Color Management > Exposure** (stops) and choose the **View Transform = AgX** (default since 4.0) with a **Look** (e.g. Base Contrast, Medium High Contrast, Punchy) for contrast. Don't reach exposure by multiplying all light powers. Blender 5.2 lights also have an **Exposure** field (power × 2^exposure) for per-light stops.
- AgX rolls highlights off to white and desaturates them. Near-clipped coloured lights turn pastel/white. "Standard" view transform clips hard and skews hues. Use it only for graphics/UI matching.
- Keep a full range: a few specular highlights near white, the subject's lit side around 50–75% display value, shadows 5–20%, true black only in small accents (deep crevices). Ducky's rule: highlights "almost overexposed but still have data" [KgqyWeF09wE@03:30], and in post don't make the dark portions darker [KgqyWeF09wE@07:00].
- Check with **View Transform = False Color** (5.2 Color Management) or Image Editor > Scopes (Histogram / Waveform).

### 1.5 Falloff (inverse square)
Irradiance from a small source falls with 1/d². Doubling the distance = ¼ = −2 stops.
- **Light close to the subject** = strong falloff across the subject and into the background. Background drops dark, dramatic (portrait/product chiaroscuro).
- **Light far away (and stronger)** = even across the subject and background (sun-like). This is why moving a light away makes a scene look "flatter" even at the same exposure.
- Area lights follow inverse square at distances beyond about 3–5× their size. Up close they are more even.
- The Sun light has no falloff (parallel rays). Its Strength is irradiance in W/m² (with Normalize), so position doesn't matter, only rotation [a-IdD-RGb4Q@03:15].
- Point/Spot **Soft Falloff** (on by default) smooths the intensity near surfaces close to the light. Leave it on [a-IdD-RGb4Q@02:30].
- Use falloff as a composition tool: light falling off toward the frame edges = a natural vignette pointing the eye at the subject.

### 1.6 Light size → shadow softness
Softness depends on the **apparent (angular) size** of the source as seen from the subject, not its absolute size.
- Bigger and/or closer = softer shadows, wrapping, broader highlights. Smaller and/or farther = crisp shadows, small specular glints [hQKJx1wXkfM@00:45][ZYk3OOf-gBk@06:00].
- Blender controls: Point/Spot **Radius** [a-IdD-RGb4Q@02:00]; Area **Size / Size X / Size Y**; Sun **Angle** (real sun ≈ 0.53°; 1–3° = hazy; 5–15° = soft/overcast-ish) [ZYk3OOf-gBk@09:15][a-IdD-RGb4Q@03:30]; World > Sun > Angle for EEVEE sun extraction.
- Area **Spread** (Cycles; default 180°) narrows the emission angle like a honeycomb grid. Low spread = harder, more directional pool with sharper shadows, without changing the reflection size [WreZ_VKDn4M@03:15][a-IdD-RGb4Q@03:45]. EEVEE: verify support.
- **Normalize** (5.2): on = total power constant when you resize, so a bigger light gets dimmer per area. Off = a bigger light emits more. Keep it on so changing size only changes softness.
- A zero-radius point light gives no reflection highlight on smooth surfaces, so products lose their edge definition. Give spots/points a radius [a-IdD-RGb4Q@04:30][a-IdD-RGb4Q@15:45].

### 1.7 Colour temperature and complementary contrast
Use **Light > Temperature (K)** (5.2) or a Blackbody node for emissive materials/world, so colour comes from physics, not arbitrary RGB [Hyhew7kuhgA@01:00].

| Source | K |
|---|---|
| Candle / fire | 1800–1900 |
| Sodium street lamp | about 2000–2200 (very orange-yellow) |
| Household tungsten / warm LED | 2700–3000 |
| Halogen / studio tungsten | 3200 |
| Golden hour sun | 3000–4000 |
| Cool white LED / fluorescent office | 4000–5000 |
| Noon sun (direct) | 5000–5500 |
| Overcast sky / studio daylight | 6000–7000 |
| Blue-sky shade, skylight | 8000–12000 |
| Moonlight (rendered by convention) | cool blue, about 7000–10000 + low saturation |

- In Blender about 6500 K renders near-neutral white on an sRGB/D65 display, so 5500 K already looks slightly warm and 3200 K is clearly orange.
- **Complementary contrast:** warm key vs cool ambient (or the reverse) separates subject and environment. Night example: blue ambient + orange spot on the product "adds balance" [a-IdD-RGb4Q@18:45]–[19:15].
- **Keep saturation modest.** Natural temperature differences are modest in saturation. Fully saturated cyan/magenta lights read "neon slop" unless motivated by neon tubes in frame.
- Coloured light on a complementary-coloured surface goes dark/grey (surfaces only reflect their own colour) [a-IdD-RGb4Q@13:00]. Light colours mix additively (R+B = magenta, R+G = yellow, G+B = cyan) [a-IdD-RGb4Q@13:45].
- Colour also carries meaning: blue + darkness = mystery, purple = romance, red + blue = tension [a-IdD-RGb4Q@15:45]–[16:30]. Lighting the background from above reduces mystery [a-IdD-RGb4Q@16:00].

### 1.8 Negative fill
Removing light is as important as adding it. A black, camera-invisible plane on the shadow side of a subject under a bright HDRI restores modelling [hQKJx1wXkfM@01:15]–[01:45]. On chrome/glass, black cards create the dark reflection lines that define edges. Card: `lighting-negative-fill-flag`.

### 1.9 Practical lights
A visible light source in frame (lamp, screen, neon, candle, street lamp).
- Build as **emissive mesh (the look) + real light (the illumination)** [bWSUxpJ8UHk@03:30][bWSUxpJ8UHk@04:15]. The emissive part must be the brightest thing locally (emission strength 10–50+), and the light it casts must share its colour.
- Screens: emission 2–8 with the actual screen image. Add a Rectangle area light the size of the screen, 6500 K bluish, low power, facing outward, to light the face/keyboard.
- Lamp shades: emission on the inner shade at low strength + Point light (radius = bulb size) inside, so shade transmission and pool on the table both read.
- Array-modified emissive meshes don't duplicate light objects. Duplicate lights with Alt+D (linked data) or instance a collection.

### 1.10 Bounce / global illumination
- Indirect light is weaker after each bounce and scaled by albedo [a-IdD-RGb4Q@00:45]–[01:00]. Bright materials = bright scene [KgqyWeF09wE@01:45]. Realistic albedos: fresh snow 0.8–0.9, white paint 0.8, concrete 0.3–0.4, asphalt 0.05–0.1, charcoal 0.03. Never use pure 1.0 white or 0.0 black albedo.
- Colour bleeding (red wall tints the floor) is a realism cue. Don't kill it with excessive fill lights.
- Cycles budget: Render > Light Paths > Max Bounces (defaults Total 12, Diffuse 4, Glossy 4, Transmission 12, Volume 0, Transparent 8). Dark glass with black shadows = too few transmission bounces. A black transparent object = too few transparent bounces [a-IdD-RGb4Q@06:30]–[11:15].
- **Bounce card** fill: `lighting-bounce-card-fill` [ZYk3OOf-gBk@01:30][KgqyWeF09wE@01:30][a-IdD-RGb4Q@01:30].

### 1.11 Light shaping: gobos, cookies, blockers, spill control
- **Gobo/cookie**: a pattern in the beam (window frame, leaves, blinds) implies an off-screen world and creates highlight spots [ZYk3OOf-gBk@09:30][KgqyWeF09wE@03:00]. Prefer a physical cutout plane (works in both engines). Node gobos are Cycles-only: either a Spot with an image in its light nodes (frame-verified: Spot Size 80°, Blend 0.15 [ZYk3OOf-gBk@10:00]) or an Area light with Spread 0° acting as a projector with an animated window texture (frame-verified, about 22.5 W [KgqyWeF09wE@03:40]). Card: `lighting-gobo-motivated-patterns`.
- **Spot Blend** softens the cone edge (0 = hard edge) [a-IdD-RGb4Q@03:00]. Radius softens shadows.
- **Light linking** (Object Properties > Shading > Light Linking: Receiver collection; Shadow Linking: Blocker collection) to keep rims off floors [WreZ_VKDn4M@06:45][ZYk3OOf-gBk@02:15]. Card: `lighting-light-linking-spill-control`.
- **Ray visibility** (Object Properties > Visibility > Ray Visibility: Camera, Diffuse, Glossy, Transmission, Volume Scatter, Shadow) to make cards, flags and emitters invisible to the camera but active in lighting [hQKJx1wXkfM@01:45][ZYk3OOf-gBk@01:45][WreZ_VKDn4M@05:15].
- **Per-light influence** (EEVEE: Diffuse/Glossy/Transmission/Volume Scatter factors; Cycles: light Ray Visibility) to make a light that only creates specular glints or only lights the volume. Values ≠ 1 break physical rules (manual 5.2), so use them deliberately.

### 1.12 Atmosphere interaction
- Participating media (fog, haze, dust) make light visible (beams, halos), add aerial perspective (distance gets lighter and lower in contrast), and fill shadows with scattered light, which kills pure black.
- Bounded volume (cube with Principled Volume) is better than world volume for control and speed. Density 0.005–0.03 per metre for scenes 10–100 m deep. 0.02 used for a foggy night road [bWSUxpJ8UHk@05:00]. Break it up with Noise → Color Ramp → Density. (bWSUxpJ8UHk wires the ramp into Principled Volume **Emission Strength**, frame-verified [bWSUxpJ8UHk@05:15]. That makes self-glowing fog: stylised and unmotivated, so use it sparingly.)
- Anisotropy 0.3–0.7 makes fog glow brightly when looking toward the light (backlit beams). Use it for god rays through windows/trees.
- Wet/low-roughness ground stretches point lights into long reflections, the key night-street signature [bWSUxpJ8UHk@00:45].
- Mist pass (EEVEE/Cycles World > Mist Pass) + compositor gives cheap depth haze when volumes are too slow.

---

## 2. Light sources: when to use which

| Source | Best for | Strengths | Weaknesses / gotchas |
|---|---|---|---|
| **HDRI** (World > Environment Texture) | realistic exteriors/interiors, integration, believable reflections on metal/glass, fast "photo-real" base | real-world complexity, consistent reflections | less control [ZYk3OOf-gBk@08:30]; built-in sun may clip; generic look if used as-is; sun direction must match any added lights; low-res HDRIs give blurry reflections |
| **Sky Texture + Sun light** | exterior day, time-of-day animation, architecture | physically linked sun/sky colour, animatable | 5.0+: model "Multiple Scattering" (new default) or "Single Scattering" (old Nishita) [web: 5.0 release notes]; physically scaled brightness, so expect to lower Exposure or Strength; don't double up a sky sun disc + a Sun light without intent |
| **Sun light** | hard directional light, sunlight through windows, flat-colour products [ZYk3OOf-gBk@08:45] | parallel shadows, no falloff, cheap | needs ambient (world) or shadows go black; Angle controls softness |
| **Area light** | key/fill/rim in studio and interiors, window fills, softboxes | size controls softness, Spread controls direction (Cycles), cheap to sample | uniform rectangle in reflections [WreZ_VKDn4M@04:00]: texture it (Cycles) or use gradient emissive cards |
| **Spot light** | stage/pools, gobos, accents, flashlight, street lamp | Angle + Blend shape the beam, works with volumes | hard cone edge looks theatrical; Radius 0 = no specular |
| **Point light** | bulbs, candles, practicals, small kickers | omnidirectional, Radius = bulb size | radius 0 = CG pin highlights and razor shadows |
| **Emissive geometry** | visible practicals, neon, screens, gradient reflection cards, strip lights on products [WreZ_VKDn4M@04:30] | any shape, appears in reflections exactly as modelled | Cycles: noisier than lights (keep Emission Sampling = Auto); EEVEE: lights the scene only through raytracing/GI, with no proper shadows, so back it with a real light; light linking for emissive meshes is Cycles-only |

Decision rules:
- **Realism in an environment** → HDRI or Sky+Sun as the base, then shape with negative fill, bounce cards and 1–2 motivated lights.
- **Studio product/character** → world dark or very low (0–0.1), area lights / gradient cards with full control [ZYk3OOf-gBk@08:30]. Optional low-strength studio HDRI just for reflections (Light Path > Is Glossy Ray mix [Hyhew7kuhgA@01:15]).
- **Glossy/glass hero** → emissive gradient cards or textured area lights designed as reflections.
- **Stylised mograph** → a dramatic HDRI or "area light map" HDRI as the single light + bounce board is fine [KgqyWeF09wE@05:30].
- When combining an HDRI with a Sun light: rotate the HDRI (Mapping Z) so its sun aligns with the Sun light. Match the temperature. Either remove the HDRI sun (clamp or paint it out) or set the Sun light to replace it, not add to it. Mismatched shadow directions is a top failure.
- Want different backgrounds vs lighting? World: Mix Shader with Light Path > Is Camera Ray: camera sees a backdrop colour, everything else sees the HDRI. Glossy rays can get their own environment the same way [Hyhew7kuhgA@01:15]–[01:30].

---

## 3. Recipes per scene type (Blender 5.2 starting setups)
Assumptions: real-world scale in metres, AgX + Look "Base Contrast" (or "Medium High Contrast" for punch), Exposure 0, Normalize on, Cycles unless noted. Numbers are first-render guesses. Expect ±1–2 stops of correction via Exposure.

### 3.2 Character / portrait
Character 1.8 m, camera 50–85 mm at eye level or slightly below.
- World: dark while blocking [hQKJx1wXkfM@00:15]. Final: HDRI 0.1–0.5 or a dim sky colour.
- **Key:** Area 1.2×1.2 m (or Disk), 45° off axis, about 35° up, 2–2.5 m away, 300–600 W, 4500–5600 K. Rotate until the Rembrandt triangle appears [hQKJx1wXkfM@00:15].
- **Fill:** bounce card or negative fill depending on world brightness. Ratio 4:1 drama / 2:1 commercial.
- **Rim:** Area 0.5×1.5 m behind, opposite side to key, 200–500 W, slightly cooler (+1000 K) [hQKJx1wXkfM@00:30] (the tutorial itself uses a 1 m square area at only 5 W for the backlight on a head bust [hQKJx1wXkfM@00:40] — watts depend on distance/scale).
- **Hair/top light:** small (0.2–0.3 m) area above and behind, tilted back, small size for a crisp edge [hQKJx1wXkfM@00:30]–[00:45].
- **Eye light:** tiny area near the camera, 1–5 W, Glossy-only (Cycles ray visibility, or EEVEE Diffuse factor 0), for catchlights.
- Bright HDRI case: keep the HDRI, add a black flag on the shadow side [hQKJx1wXkfM@01:15].
- Variations: **Split light** (key at 90°, no fill) for villain/tension. **Butterfly** (key high on the camera axis + a bounce from below) for beauty. **Under-light** only if motivated (phone screen, fire).

### 3.3 Interior day (window-lit)
- Window opening: **Area light** filling the opening (Size = window), pointing inward, 200–1000 W, 6500–8000 K (skylight). Optionally add a light portal setup instead if using an HDRI outside (Cycles: an area light with Portal enabled in the window).
- **Sun** through the window: Strength 3–5, Angle 0.5–1°, 5000–5500 K, elevation 25–45°, making 1–2 sun patches on the floor/furniture about 1–2 stops above the base [KgqyWeF09wE@03:30]. Use a window-frame cookie or the real frame geometry for the pattern [KgqyWeF09wE@03:15].
- Materials albedo 0.6–0.8 for bright/airy [KgqyWeF09wE@01:45]. Cycles Diffuse bounces ≥ 4.
- Bounce board or simply white walls opposite the window [KgqyWeF09wE@01:30].
- EEVEE: Raytracing on (Method: Screen-Trace with Light Probe fallback), Fast GI on, bake a Volume probe covering the room + Sphere probe(s) for reflections. Thick walls + shadow Steps 12–16 against sun bleed at window edges; bake the Volume probe with fog/window glass hidden; it also stops the world/HDRI from flooding the room [eevee_full_course@07:40][eevee_full_course@36:00][eevee_full_course@65:20]. Full order: `rendering.md` §1.1.
- Variation **overcast**: no sun, larger soft window light 7000 K, stronger negative fill on the far side for modelling.

### 3.4 Interior night / moody
- World: very low blue (strength 0.01–0.05, about 9000 K equivalent) or moonlight through the window (Sun 0.05–0.2, 8000–10000 K, low saturation).
- **Practicals** do the lighting: table lamp (Point radius 0.05 m, 20–60 W, 2700 K inside the shade + emissive shade), ceiling pendant, TV/monitor (screen emission + area light 6500 K). Each practical makes a pool. Leave darkness between the pools [a-IdD-RGb4Q@19:00].
- Subject accent: a warm spot or the practical's own light. The background gets a separate dim warm/cool light so it doesn't go black [a-IdD-RGb4Q@19:15].
- Ratio 8:1+. Exposure +1 to +2 instead of more lights.
- Light haze: room volume density 0.002–0.01, so the lamp beams barely show.
- Card: `lighting-night-warm-practicals-cool-ambient`.

### 3.5 Exterior day (sun + sky)
- World: **Sky Texture** (5.2: Multiple Scattering, or Single Scattering for the old Nishita look). Drive sun elevation/rotation, or use **Sun Position** extension with a real latitude/longitude/time [CPZtbXTVdWs@00:15]–[00:45].
- **Sun light** aligned with the sky's sun (Sun Position can sync both), Angle 0.53° (crisp) to 2° (hazy), Strength 3–5 if the sky sun disc is off, or let the sky provide the sun. Don't use both at full strength.
- The physical sky is bright: expect Exposure about −2 to −4 (or reduce sky Strength). Check with False Color.
- Elevation drives mood: 5–15° golden hour (long warm shadows, rim-lit subjects facing away from the sun), 30–50° pleasant day, 70–90° harsh noon [a-IdD-RGb4Q@17:45]–[18:00].
- Shape characters with large negative flags, or position the camera so the sun is a side/back light.
- Add aerial perspective: a volume with very low density (0.0005–0.002) over large distances, or a mist pass.
- Animation: keyframe the time with LINEAR interpolation [CPZtbXTVdWs@01:00]–[01:15] and animate Exposure across sunrise/sunset.

### 3.6 Exterior night / street
- Ambient: dark blue sky/world (strength 0.02–0.05), or a moon Sun (0.05–0.2, cool, Angle 0.5°). Never rely on zero ambient [a-IdD-RGb4Q@18:15].
- Street lamps: emissive lamp heads (10–50) + Disk area lights 0.4–0.6 m under each head (source used Disk **1 m ≈250 W, Spread 180°, near-white, in EEVEE Legacy + Filmic Medium High Contrast** [bWSUxpJ8UHk@04:35, 05:45], seen in frames), 300–1500 W, 2000–2700 K sodium or 3500–4500 K LED, Spread 120–150° [bWSUxpJ8UHk@03:30]–[04:30]. Vary intensities ±20%. One flickering or dead lamp adds realism.
- Wet road (roughness noise 0.05–0.3) for streaks [bWSUxpJ8UHk@00:45]. Fog cube density 0.01–0.03 with noise [bWSUxpJ8UHk@05:00].
- Secondary sources: shop windows (warm area lights), car headlights (spots, 5000–6000 K), signs (emissive, saturated colour allowed because it's motivated).
- Post: slight lens distortion/dispersion (0.05/0.03) and a green/blue grade for a liminal/found-footage feel [bWSUxpJ8UHk@05:45]–[06:15].

### 3.7 Abstract / motion-graphic studio
- One big establishing light: a dramatic HDRI or a large area light (2–4 m) at 45–60° [KgqyWeF09wE@05:30][KgqyWeF09wE@00:45].
- Bright, colour-coordinated materials first. Lighting decisions follow them [KgqyWeF09wE@04:45].
- Bounce board(s) to open the shadows [KgqyWeF09wE@06:00]. Rim strips to outline shapes. Gobo spots to break up big flat surfaces [KgqyWeF09wE@03:00].
- Coloured lights allowed, but keep a hierarchy: one neutral or warm key + one complementary accent, with the accent saturation at about 0.4–0.7 rather than 1.0.
- Infinite cyc (floor curved into the wall) with a gradient from a background light, to avoid a visible horizon line [ZYk3OOf-gBk@06:15].

---

## 4. EEVEE (5.x, "EEVEE Next") vs Cycles: differences and gotchas
| Topic | Cycles | EEVEE 5.2 |
|---|---|---|
| GI / bounce | Path traced; Light Paths bounces control it [a-IdD-RGb4Q@06:30] | Render > Raytracing (Method: Light Probe or Screen-Trace), Fast GI Approximation, plus Light Probes (Volume = baked irradiance, Sphere/Plane = reflections). Off-screen bounce depends on probes. Bounce cards work only with raytracing/probes. **Raytracing is off by default**; screen-space bounce/reflection "switches on/off" while panning until probes exist [eevee_full_course@09:20][eevee_full_course@10:40]. Fast GI Steps 16, Distance ~1–2 m with a baked Volume probe (Surfel Resolution ~100) [eevee_full_course@48:40][eevee_full_course@42:40]. |
| Soft shadows | Exact from light size | Virtual shadow maps. Shadow softness from light radius/size. **Jitter** (light > Shadow) for accurate soft shadows (costly, viewport off by default). **Filter**, **Resolution Limit** to fix aliasing/leaks. Render > Shadows: Rays/Steps. Bigger/softer lights and wider sun Angle leak more through walls: Steps 12–16, Rays 2, Solidify walls [eevee_full_course@07:40][eevee_full_course@09:20]. |
| Light nodes (gobos, textured area lights) | Supported [ZYk3OOf-gBk@09:45][WreZ_VKDn4M@04:15] | **Not supported.** Use physical cookies / emissive gradient planes |
| Emissive meshes as light | Sampled (Emission Sampling Auto), noisier than lights | Contribute only via raytracing/GI, no proper shadows. Back them with a real light. |
| Area Spread | Supported | Verify (may be ignored) |
| Light linking | Yes (receivers + shadow blockers) | Light linking supported (manual sets it up in EEVEE panels). Emissive-mesh linking Cycles-only. Verify shadow linking. |
| World sun | Importance-sampled automatically | World > Sun > **Threshold** extracts the HDRI/sky sun into a real sun light with **Angle** and **Use Shadow**. Without it, HDRI suns give no crisp shadows. World > Light Probe > Resolution for world lighting quality. World light ignores walls (floods closed rooms) unless a Volume probe is baked [eevee_full_course@36:00]. Conflict: one source prefers **Threshold 0 + a real Sun lamp** for control [eevee_full_course@51:00]; use the lamp when you need direction/animation/light linking, Threshold when the sun must match the HDRI background. |
| Light range | Physically unlimited | Render > Lights > Light Threshold (or per-light Custom Distance) cuts lights off. Dim large-range lights can pop or cut. |
| Volumes | Accurate, slow. Volume bounces default 0 | Render > Volumes: resolution, steps, distance, volumetric shadows. Light's Volume Scatter factor. Low resolution = blocky, flickering beams |
| Caustics / glass shadows | Shadow caustics: enable on light + caster + receiver [a-IdD-RGb4Q@05:30] | Glass shadows approximated. Use transparent shadow settings / material Render Method "Dithered" vs "Blended". Plane probes show only through Dithered; Blended works with sphere probes [eevee_full_course@61:00]. Windows: archviz glass (`materials-eevee-archviz-glass`) |
| Light Path node tricks in the world | Fully work [Hyhew7kuhgA@01:30] | Partially (world probe). Verify |

Practical rule: **look-dev and final in the same engine.** If the final is EEVEE, never rely on light textures, emissive-only lighting, or Spread. If you preview in EEVEE for a Cycles final, expect softer GI and brighter or darker corners in Cycles.

---

## 5. "AI slop" lighting failures: detect and fix
Each failure shows its signature in a render and the fix. Detection can be done by eye, or programmatically: render a low-res frame, load pixels with numpy (linear luminance Y = 0.2126R + 0.7152G + 0.0722B), and use object/material index masks (Cryptomatte or simple per-object holdout renders) to measure the subject.

| # | Failure | How to detect | Fix |
|---|---|---|---|
| 1 | **Flat front light** | Lit/shadow-side ratio of the subject < 1.4:1. Cast shadow hidden behind the object. Specular hotspot centred on the face toward the camera | Move the key 30–60° off axis and 20–45° up [hQKJx1wXkfM@00:15]. Remove camera-position lights |
| 2 | **Everything evenly lit** (no hierarchy) | Histogram is a narrow hump in the mids. Background as bright as the subject. Std-dev of luminance low. Squinting shows no focal area | One dominant source [KgqyWeF09wE@00:45]. Let the falloff darken the edges. Light the background separately and lower. Delete lights without a job [a-IdD-RGb4Q@18:30] |
| 3 | **No shadow anchoring** (floating objects) | No darkening at contact. Floor under the object same value as the floor around it. Lights linked off the floor | Ensure the key lights the floor (don't light-link it off). Use a key with some size for a contact gradient. Keep AO/bounce. Check the contact shadow in the clay render |
| 4 | **Neon teal/orange by default** | Light colours with HSV saturation > 0.8. Hues around 180–200° and 20–35° with no visible emitter of that colour | Use Temperature (K). Keep saturation low. Allow saturated colours only from in-frame sources (neon signs, screens) |
| 5 | **Blown highlights** | > 0.5% of subject pixels clipped (display ≥ 0.98) or large areas desaturated to white under AgX. False Color shows big white/red areas | Lower Exposure. Reduce the rim/key. Make sources larger (lower peak). Use textured or gradient lights on glossy objects [WreZ_VKDn4M@04:00] |
| 6 | **Pure black shadows** | > 2–3% of frame pixels < 0.002 linear outside intentional accents. Shadow side shows no texture | Bounce card [ZYk3OOf-gBk@01:30]. World ambient ≥ a small value. More diffuse/transmission bounces [a-IdD-RGb4Q@07:30]. Brighter albedos [KgqyWeF09wE@01:45] |
| 7 | **Lights don't match the HDRI** | Shadows from the added Sun point a different way from the HDRI's sun. Reflections show a sunny sky but lighting is overcast (or the reverse). Colour mismatch | Rotate the HDRI (Mapping Z) to match. Match temperature. Use EEVEE Sun Threshold extraction instead of a mismatched Sun |
| 8 | **No motivated source** | Can't name a source for a light. Rim in a realistic room with no lamp/window behind. Coloured light with no emitter | Add a practical or window to motivate it, or remove the light. Name lights by role + source |
| 9 | **Multiple competing shadows** | 2+ cast shadows of similar density at different angles | Keep one shadow-casting key. Fills: bounce cards (no shadow) or Cast Shadow off on large fill lights (Cycles), sparingly |
| 10 | **CG rectangles in reflections** | Uniform white rectangles on glossy surfaces | Gradient/textured lights, round/strip shapes [ZYk3OOf-gBk@07:00] |
| 11 | **Razor shadows from tiny sources everywhere** | Hard, aliased shadow edges with no penumbra variation | Give lights size/radius/angle. Sun Angle ≥ 0.5° [Hyhew7kuhgA@00:00] |
| 12 | **Grey fog soup** | Global contrast collapsed. Distant and near objects equal in contrast | Lower density. Add noise breakup. Bound the volume. Backlight the fog |
| 13 | **Sharp CG edges** | Hard-surface objects show no edge highlights | Bevel modifier [ZYk3OOf-gBk@03:45] |

**QA checklist (run on every lighting pass):**
- [ ] I can name each light's job and its in-world source.
- [ ] Clay render (View Layer > Override > Material = grey 0.5 diffuse) reads clearly: one direction, shape visible, contact shadows present.
- [ ] Subject lit:shadow ratio is within the intended range (2:1 / 4:1 / 8:1).
- [ ] Subject separated from the background (rim or value contrast) when squinting / at thumbnail size.
- [ ] False Color: no unintended clipping on the subject. Shadows not at pure black (except small accents).
- [ ] Shadow directions consistent between all lights, the HDRI and the sun.
- [ ] Colour temperatures plausible. Saturated colours only from visible emitters.
- [ ] Glossy surfaces show designed reflections (no white rectangles, no dead black metal).
- [ ] Brightest area = where the viewer should look (the brand/product), within about the centre 2/3 of frame or on a third.
- [ ] Animated shots: no light popping (EEVEE Light Threshold), no flicker in volumes/GI, exposure adapted for time-of-day changes.

---

## 6. Step-by-step lighting workflow (with cheap validation renders)
0. **Lock camera, scale and materials' albedo range.** Real-world scale in metres. Long lens for products [ZYk3OOf-gBk@00:30]. Albedos realistic and on the bright side when "airy" is wanted [KgqyWeF09wE@04:45].
1. **Kill everything:** World strength 0, disable existing lights [hQKJx1wXkfM@00:15][a-IdD-RGb4Q@14:30]. Set AgX, Exposure 0.
2. **Clay override:** View Layer Properties > Override > Material = Principled grey (Base Color 0.5, Roughness 0.5). Shows lighting independent of textures.
3. **Block the key.** One light, motivated. Orbit with 3D Cursor pivot + R R [hQKJx1wXkfM@00:00]. Validation render: 25–50% resolution, Cycles 32–64 samples + denoise (OpenImageDenoise), or EEVEE. Check direction, shadow shape and contact shadow.
4. **Set the shadow level:** bounce card or negative fill, or raise the world/sky to the desired ratio [ZYk3OOf-gBk@01:30][hQKJx1wXkfM@01:15]. Measure the ratio.
5. **Separation:** rim/back light or background light. Light-link it off the floor if it spills [ZYk3OOf-gBk@02:15].
6. **Remove the override**, check with real materials. Glossy/glass → redesign the reflections (gradient cards) [WreZ_VKDn4M@04:30]. Matte → shadows and gobos [ZYk3OOf-gBk@08:45].
7. **Exposure:** Color Management Exposure + Look. Use the False Color check. Highlights near but under clipping [KgqyWeF09wE@03:30].
8. **Colour:** set temperatures (key vs ambient complementary if motivated) [a-IdD-RGb4Q@18:45]. Keep saturation modest.
9. **Accents:** gobo patches, practicals, eye lights, specular glints [KgqyWeF09wE@03:00][ZYk3OOf-gBk@06:00].
10. **Atmosphere:** volume/mist, wet surfaces. Re-check exposure (fog lifts the shadows) [bWSUxpJ8UHk@05:00].
11. **Final QA** (section 5), then render settings: Cycles samples/noise threshold, Clamp Indirect about 10 to tame fireflies, Filter Glossy about 0.5–1. EEVEE: shadow resolution, Jitter for hero shots, raytracing resolution, volume resolution.
12. **Post:** light grade only. Curves lifting mids without crushing shadows [KgqyWeF09wE@07:00], glare/bloom subtle. Lens effects to taste [bWSUxpJ8UHk@06:00].

---

## 7. Conflicts between sources and how we resolve them
| Topic | Source A | Source B | Resolution |
|---|---|---|---|
| HDRI use | "Use HDRIs sparingly, no control" [ZYk3OOf-gBk@08:30] | HDRI as the establishing light [KgqyWeF09wE@01:15]; HDRI + negative fill [hQKJx1wXkfM@01:45] | Studio product = lights first. Realism/environments = HDRI base + shaping (flags, bounce). |
| Fill method | Bounce card [ZYk3OOf-gBk@01:30][a-IdD-RGb4Q@01:30] | Soft fill light with high Spread [WreZ_VKDn4M@03:30] | Bounce card by default (no extra shadow, keeps the ratio). Fill light when you need a different colour or a bigger lift. |
| Bounce-board brightness | Value 2–20 hack [KgqyWeF09wE@06:15] | Physical albedo | Grow or move the board first. Albedo > 1 only as a last resort; check fireflies. |
| Glass lighting | Gradient emissive planes [WreZ_VKDn4M@04:30] / gradient on area light [ZYk3OOf-gBk@07:00] | Light the environment behind [a-IdD-RGb4Q@15:00] | Complementary: gradient strips for edges and reflections + a lit backdrop for the body. |
| Light linking scope | All lights to product only [WreZ_VKDn4M@07:00] | Only exclude the floor from rims [ZYk3OOf-gBk@02:30] | Exclude the floor from rims and backlights only. The key must light the floor (grounding). |
| Night ambient | Scene-sized blue area light [a-IdD-RGb4Q@18:15] | (none) | Prefer a blue world/sky (correct reflections). Area hack only for small sets. |
| Soft daylight | Two sky textures 30°/32°, sizes 5/1 [Hyhew7kuhgA@00:45] | Single sun with larger Angle [ZYk3OOf-gBk@09:15][a-IdD-RGb4Q@03:30] | Single sun Angle first (simpler, EEVEE-safe). The dual-sky graph is untested. |
| "Real light isn't harsh" | [Hyhew7kuhgA@00:00] | Sun gives hard shadows for summer looks [ZYk3OOf-gBk@09:00]; noon = hard shadows [a-IdD-RGb4Q@17:45] | Hardness is a story choice. Clear sun is hard. Overcast/haze is soft. |
| Sun light usage | "Rarely use it" [a-IdD-RGb4Q@03:15] | Sun for matte flat-colour products [ZYk3OOf-gBk@08:45] | Product artists vs scene artists. Exteriors always need it. |
| EEVEE HDRI sun | §5 #7: World Sun Threshold extraction to match the HDRI | Threshold 0 + a real Sun lamp [eevee_full_course@51:00] | Lamp for control/animation/light linking; Threshold when the visible HDRI sun must match exactly. |
| Paid tools | "Cinematic compositor" [hQKJx1wXkfM@02:00][WreZ_VKDn4M@07:15], PSA addon [CPZtbXTVdWs@00:00] | Native Blender | Treat them as promos. Reproduce with native compositor (Glare, Lens Distortion, Curves) and the 5.x Sky Texture + Sun Position. |

Numbers stated in videos: key 25 W / rim 5 W [ZYk3OOf-gBk@04:15][ZYk3OOf-gBk@05:00]; bevel modifier 5 segments, 0.03 (default-cube scale) [ZYk3OOf-gBk@03:45]; 120 mm lens [ZYk3OOf-gBk@00:30]; sky 30°/32°, intensity 0.5, sizes 5/1, elevation 15° both; glossy-ray Background cream at Strength 10 [Hyhew7kuhgA@01:42, seen in frame]; fog density 0.02 [bWSUxpJ8UHk@05:00]; lens distortion 0.05 / dispersion 0.03 [bWSUxpJ8UHk@06:00]; Cycles default bounces 12 total / diffuse 4 / glossy 4 / transmission 12 [a-IdD-RGb4Q@11:00]. All other numbers in this file are our own starting points (metres, AgX, Exposure 0) and need validation.

---

## 8. Blender 5.2 setting map (quick reference)
- Light: Object Data (green bulb) > Type, **Temperature**, Color, **Exposure**, Power (W) / Strength (Sun, W/m²), **Normalize**, Radius / Size / Shape / **Spread** (Area) / Angle + Blend + Show Cone (Spot) / Angle (Sun), Soft Falloff (Point/Spot). Cycles: Cast Shadow, Multiple Importance, Shadow Caustics, Max Bounces, Is Portal (area). EEVEE: Shadow (Jitter, Overblur, Filter, Resolution Limit), Influence (Diffuse/Glossy/Transmission/Volume Scatter), Custom Distance. (Manual 5.2: light_object, eevee/light_settings.)
- Object > Visibility > Ray Visibility (Camera, Diffuse, Glossy, Transmission, Volume Scatter, Shadow). Object > Shading > Light Linking / Shadow Linking. Object > Shading > Caustics (Cast/Receive Shadow Caustics).
- World: Surface (Background / Environment Texture / Sky Texture: Multiple Scattering or Single Scattering, the former Nishita). EEVEE: World > Sun (Threshold, Angle, Use Shadow), Light Probe Resolution, Mist Pass (Start, Depth, Falloff).
- Render (Cycles) > Light Paths: Max Bounces, Clamping, Caustics, Fast GI. Sampling > Lights > Light Tree, Light Threshold.
- Render (EEVEE) > Raytracing, Fast GI, Shadows, Volumes, Lights (Light Threshold).
- Color Management: Display, View Transform (AgX, Standard, Filmic, False Color, Khronos PBR Neutral), Look, Exposure, Gamma, Curves. 5.0 added wide-gamut/HDR display and working-space options; verify the menu names in 5.2.
- Sun Position extension (Get Extensions) for real sun direction [CPZtbXTVdWs@00:15].

## 9. Open questions to validate (feed to experiments/)
1. Does Area Spread render in EEVEE 5.2?
2. Does shadow linking work in EEVEE 5.2?
3. Sky Texture Multiple Scattering: what Exposure gives a "normal" daylight with Sun Strength 1 vs a sun disc?
4. Bounce card albedo 0.8 vs 5: noise and fireflies at equal samples (Ducky hack).
5. Dual-sky vs single-sun Angle (Hyhew7kuhgA). Is there any visible benefit?
6. Programmatic QA thresholds (ratios, clip %, black %): calibrate on 5 good reference renders.
