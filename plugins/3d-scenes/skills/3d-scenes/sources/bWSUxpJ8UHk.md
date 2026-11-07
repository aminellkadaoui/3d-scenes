# Liminal Space NIGHT ROAD Realistic Tutorial / Blender 3.4
- url: https://youtu.be/bWSUxpJ8UHk
- channel / duration / Blender version shown: None Design 3D / 8:35 / Blender 3.4 (title; status bar **3.4.0** seen) — rendered in **EEVEE (Legacy)**, not Cycles (corrected from frames [06:05])
- domain(s): environment | lighting | materials | compositing | camera/animation
- evidence used: transcript (auto captions, many mis-transcriptions, e.g. "Fork" = fog, "citrate lamp" = street lamp, "Roll" = road) + yt-dlp metadata + frames viewed: raw/bWSUxpJ8UHk/frames/fog_5m35.jpg, fognodes_crop_5m35.jpg (final_6m25.jpg was a blank render window, so not useful) + 2 contact sheets + 6 frames viewed in §6.
- trust: low–medium. Beginner-level workflow that is mostly asset assembly. Lighting is only a small section and no light power values are stated. Useful as a recipe skeleton for night road/street scenes (practical lamp emission + real light + volumetric fog + lens/grade).

## 1. Problem it solves
Building a foggy, liminal night road (an empty highway with street lamps) that feels realistic and eerie, and animating a handheld camera.

## 2. Techniques

### T1: Large-scale scene: camera and viewport clip end 2000  `[00:15]`
- What: Camera > Clip End = 2000 m, and View > Clip End = 2000 (N panel) [00:15].
- Why: long roads exceed the 100 m default clip, so distant geometry and lamps vanish. Note: very large clip ranges reduce depth precision in EEVEE/viewport. Keep Clip Start reasonable (0.1 m).
- Status: Extracted

### T2: Wet road via noise-driven roughness  `[00:45]`–`[01:15]`
- What: ambientCG road material. Noise Texture → Color Ramp → (roughness), black stop = more watery/shiny, white = opposite. Tune noise Scale/Detail [00:45]–[01:15].
- Lighting relevance: at night, wet low-roughness patches create long specular streaks of the street lamps on the road. That is THE classic night-street look, and it is what makes a few point sources read as "cinematic". Without puddles, night lamps light only small pools.
- Status: Extracted (materials, cross-ref)

### T3: Practical street lamps: emissive lamp head + area light under it  `[03:30]`–`[04:45]`
- What: imported street-lamp model (Sketchfab). Give the lamp glass faces an Emission material (select faces in Edit Mode, assign) [03:30]–[03:45]. Array modifier to repeat lamps along the road, with a duplicate for the other side [04:00]. Then add Area lights under each lamp head, Shape = Disk, raise the Power and change the colour, Shift+D to duplicate along the scene [04:15]–[04:30].
- Why: the emissive mesh makes the source visible (a practical in frame). The area light does the efficient illumination with controllable falloff. This separation (look vs light) is standard for practicals.
- Values seen in frame [04:35] (not stated in narration): Area **Disk 1 m, Power ≈250 W** (a leading digit may be hidden under the cursor), Spread 180°, near-white colour. Our starting point for a 6–8 m pole: Disk area 0.4–0.6 m, 300–1500 W, Temperature 2000–2700 K (sodium/old) or 4000–5000 K (LED), Spread about 120–150° to keep light under the lamp. Lamp-head emission strength 10–50 so it reads brighter than anything it lights.
- Caution: arrayed lights. The Array modifier duplicates the emissive mesh but NOT the area lights (lights are objects). Duplicate them manually, with linked duplicates (Alt+D) so one edit changes all, or instance them via a collection.
- Status: Extracted

### T4: Volumetric fog cube with noise breakup  `[04:45]`–`[05:30]`
- What: a cube scaled over the scene. Material: delete Principled BSDF, add Principled Volume → Material Output Volume. Density 0.02 [05:00]. Noise Texture (Fac) → Color Ramp (Linear, black stop moved right) → **Principled Volume Emission Strength**. CONFIRMED in frame fognodes_crop_5m35.jpg: Density field = 0.020, Emission Color white, ramp Color wired into Emission Strength. Dark stop controls fog density variation. Tune Scale/Detail [05:15]–[05:30].
- Why: fog reveals light. Lamps become visible cones and halos, depth separates into planes (aerial perspective), and darkness gets texture instead of pure black. Noise prevents a uniform "grey soup".
- Values: density 0.02 per metre (scene in metres) = noticeably foggy over 50–100 m distances. For close interiors use about 0.005–0.05. The author really does plug noise into Emission Strength, so the fog self-glows in patches. That brightens the fog without any light. It reads as "lit mist" but flattens contrast and is unmotivated. Our recommendation: noise → Density (keep emission 0) and let the lamps light the fog.
- Blender 5.2 notes: EEVEE: Render Properties > Volumes (Resolution/tile size, Steps, Distance, Light Clamping, and in 5.x volumetric shadows). For lights to show shafts in EEVEE, lights need Volume Scatter influence > 0 (default 1). Cycles: volume bounces are 0 by default (fine). Volumes are slow, so use a bounded cube, not world volume, for large scenes.
- Status: Extracted

### T5: Lens distortion + tinted curves in the compositor  `[05:45]`–`[06:15]`
- What: Compositor (Use Nodes): Lens Distortion with Distort 0.05, Dispersion 0.03, Fit on. Seen [06:05]: chain is Render Layers → Lens Distortion → RGB Curves → Composite/Viewer (EEVEE scene: Render 100 / Viewport 100 samples, AO, Bloom, Screen Space Reflections on). RGB Curves pushing greenish or blue [06:00]–[06:15].
- Why: night footage from real cameras has chromatic aberration and a colour cast (sodium vs LED vs moonlight look). The greenish cast is typical of liminal/found-footage aesthetics.
- Blender 5.2: compositor was reworked in 4.x/5.x (node groups as modifiers, nodes renamed). Lens Distortion still exists. Check the field names.
- Status: Extracted

### T6: Handheld camera via Camera Shakify  `[06:30]`–`[07:45]`
- Camera domain. Shakify "Handycam Run" too much → reduce Influence/Scale/Speed [07:30]–[07:45].

## 3. Claims I doubt or must test
- "Realistic" is mostly asset-driven. No exposure strategy, no moonlight/sky fill mentioned. With only lamps the far road will be black.
- Fog density 0.02 + noise into Emission Strength (confirmed visually) = self-lit fog. Test it against noise → Density with lamp-lit fog.
- Frame fog_5m35.jpg shows the World as a grey Background, Strength 1.000. ~~The scene reads as overcast dusk/grey~~ (corrected from frames): the render view at [05:45] and the hero frame [00:03] read as genuinely dark night — black sky, isolated lamp cones in fog, wet streaks; the grey look was only the unlit viewport before fog/grade. The far road does fall off to black, as predicted.

## 4. Anti-AI-slop lessons
- Night ≠ dark render. Night needs motivated pools of light, a weak cool ambient so shadows keep shape, wet speculars, and fog to carry the light.
- Practicals: the visible source must be the brightest thing and must actually emit light consistent with its colour (warm head, warm pool).
- Repetition reads fake. Vary lamp intensities slightly and add one flickering or dead lamp for liminal realism.

## 5. Candidate isolated test
100 m road strip, two lamp poles 30 m apart, camera at 1.6 m. A: emissive heads only. B: + disk area lights 800 W 2200 K. C: + fog cube density 0.02 with noise. D: + wet roughness. Compare readability of the road edge at 50 m, presence of light cones, and specular streaks. Check render time per step (EEVEE vs Cycles).

## 6. Visual verification (frames viewed)
(fog_5m35.jpg, fognodes_crop_5m35.jpg described earlier; not redone.)
- Sheets 01–02: road from an ambientCG material [00:45]–[01:15], guard rails and embankment assets [01:30]–[02:30], lamp model with orange emissive head [03:45], arrayed lamps [04:00]–[04:15].
- [00:03] Hero frame: cool blue-cyan night, fog cones under the lamps receding in perspective, wet road speculars, a traffic cone on the right. Mood is convincing.
- [04:22] Overview: lamps arrayed on both sides of a ~straight road on a rock embankment; first Area light added at Z 6.3 m. Windows 11 desktop; status bar 3.4.0.
- [04:35] + crop: Area light **Disk, 1 m, ≈250 W, Spread 180°**, Cast Shadow on; viewport (no fog yet) shows lit lamp heads on a grey dusk background.
- [05:45] Render view with fog: dark scene, volumetric cones; Render properties: Shadows Cube/Cascade **2048 px**, Soft Shadows, Light Threshold 0.010; Colour Management **Filmic, Look Medium High Contrast**, Exposure 0, Gamma 1.
- [06:05] Compositor: Render Layers → Lens Distortion → RGB Curves → Composite; Render Engine **Eevee**, Render/Viewport samples 100/100, Ambient Occlusion, Bloom, Screen Space Reflections on.
- Quality judgement: **good mood, mid technical quality**. The final frame is atmospheric and could pass as a liminal-aesthetic still; up close it is asset-assembly with uniform lamps and EEVEE-legacy fog. Trust: medium for the recipe skeleton; values are EEVEE-legacy specific (bloom, SSR) and need re-tuning for EEVEE Next/Cycles in 5.2.
