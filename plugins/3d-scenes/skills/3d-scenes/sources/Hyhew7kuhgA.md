# Easy Blender Lighting HACK [Blender Tutorial]
- url: https://youtu.be/Hyhew7kuhgA
- channel / duration / Blender version shown: Poly Playground / 2:00 / **Blender 4.0.2** (status bar, corrected from frames); Sky Texture Nishita
- domain(s): lighting | environment
- evidence used: transcript + yt-dlp metadata + nodes_1m32.jpg (earlier agent) + contact sheet + 4 frames/crops viewed in §6.
- trust: low–medium. Clickbait framing ("good to stunning"), no rationale given for the values, and some claims are generalisations. The node graph itself is reproducible and the idea behind it (separating what diffuse rays see from what glossy rays see) is legitimate.

- Frame evidence (nodes_1m32.jpg): the demo scene is an archviz interior (dining table, chairs, plant, large glass doors to a patio) lit by the world through the windows, not a product. The World node tree shows Sky Texture nodes, a Light Path node and Mix nodes, with the user adding a Mix Shader. So the "hack" is meant for sky-lit interiors.

## 1. Problem it solves
A single Sun or a single sky gives one sharp, "too precise" shadow [00:00]. The author wants softer, layered shadows and a "richer" world, all from the World node tree with no extra lights.

## 2. Techniques

### T1: Two Sky Textures with slightly different sun direction and size  `[00:30]`–`[00:45]`
- What: Shading tab > World. Add two Sky Texture nodes (Nishita). Set the sun rotation to match the scene but offset one by a couple of degrees (example 30° and 32°). Sun Intensity = 0.5 on both. Sun Size = 5 on one and 1 on the other [00:45].
- Why: two sun disks at nearly the same direction, one small and one large, give a hard core shadow plus a wider penumbra (layered shadow edges, like a sun partly diffused by haze). The same could be done with one Sun light at a larger Angle.
- Use when: you want softer daylight shadows and are locked into a world-only setup. Don't use when: shadow precision matters (product contact shadows can double or blur), or one sun with Angle 1–3° would do. That is simpler and physically clearer.
- Values: 30°/32° rotation, intensity 0.5 each, size 5° / 1°, **Sun Elevation 15° on both**, Altitude 0 m, Air/Dust/Ozone 1.0 [01:42 crop] (elevation added from frames). These are author values with no stated scale or exposure.
- Blender 5.2 notes: Blender 5.0 reworked the Sky Texture. The new default is a Multiple Scattering model, and the old Nishita is kept as "Single Scattering". Parameter names may differ. Hosek/Preetham are older models. In EEVEE, sun disks in the world are handled through World > Sun > Threshold (sun extraction to a real shadow-casting sun). Two sky suns will NOT give two crisp EEVEE shadows reliably. Verify.
- Status: Extracted

### T2: Blackbody tint mixed into the sky  `[01:00]`–`[01:15]`
- What: Mix Color node with the two skies in A and B. Add a Blackbody node (0–10,000 K: lower = warmer). Mix the first Mix's result with the Blackbody colour in a second Mix Color, then into Background Color [01:00]–[01:15].
- Why: it grades the whole world warmer or cooler with a physically meaningful temperature control instead of a random RGB tint.
- Use when: stylised warm/cool shifts of the ambient. Don't use when: you need a physically plausible sky. Tinting a physical sky with a multiply/mix breaks its own colour gradient. Prefer adjusting sun elevation (which naturally warms) or grading in the compositor.
- Note: Blackbody below about 1000 K is deep red. Values about 3000–6500 K are the useful range.
- Status: Extracted

### T3: Different world colour for reflections (Light Path > Is Glossy Ray)  `[01:15]`–`[01:30]`
- What: Add a Light Path node, a Mix Shader, and a second Background node. Background 1 (the sky mix) and Background 2 (a chosen hue that "complements your scene") go into the Mix Shader. Seen [01:42]: Background 1 Strength 1.0; Background 2 = pale cream colour at **Strength 10.0** (so reflections see a world ~10× brighter than the lighting sky); the Mix nodes use Fac 0.5; Blackbody temperature reads ≈2500 K (low-res). (Added from frames.) Is Glossy Ray drives Fac. Output to World Surface [01:15]–[01:30].
- Why: glossy rays see Background 2, while camera/diffuse rays see the sky. You can control the reflection colour and brightness separately from the illumination, a classic "art-directed reflections" trick.
- Use when: products and cars that need cleaner or more colourful reflections without changing the lighting. Don't use when: you need realism. Reflections that don't match the visible environment look subtly fake. EEVEE handles Light Path in the world only partially (world probe), so verify.
- Status: Extracted

## 3. Claims I doubt or must test
- "Real world lighting isn't usually this harsh" [00:00]: false as a generalisation. Clear-day sun is harsh. Softness is a creative choice (haze, overcast, diffusion), not a default.
- The two-sun stack is mostly equivalent to one sun with a wider angular size. Test whether it adds anything over Sun Size = 3 alone.
- Mixing two skies + blackbody with Mix Color (default factor 0.5) halves each input's contribution. Overall exposure changes unpredictably.

## 4. Anti-AI-slop lessons
- Control shadow edge quality deliberately (sun angular size). Razor-sharp default sun shadows read as CG.
- Colour temperature should come from a Kelvin control (Blackbody / light Temperature), not random saturated RGB.
- Caution: "complementary colour reflection" is an easy route to the teal/orange slop look if overdone.

## 5. Candidate isolated test
Cube + sphere on a plane, camera at 35 mm. A: one Sky Texture, sun size 1°. B: one sky, sun size 4°. C: the author's dual-sky graph. Compare penumbra width at the cube's contact shadow and total exposure (histogram mean). Expected: C ≈ B visually, with more nodes.

## 6. Visual verification (frames viewed)
(nodes_1m32.jpg described earlier; not redone.)
- [00:50] Two Sky Texture nodes (Nishita, Sun Disc on) present but **not yet connected**; the Background node feeding World Output is a plain white Background; viewport interior is dark, lit by wall sconces. So the dark "before" is not a fair baseline for the hack — it is a scene without the sun connected.
- [01:10] Skies mixed (Mix Color) and the Blackbody node being added; still dark viewport (preview not yet showing the sky).
- [01:42] + crop: full graph — Sky1 (size 5°, intensity 0.5, elevation 15°, rotation 30°) + Sky2 (size 1°, intensity 0.5, elevation 15°, rotation 32°) → Mix Color (Fac 0.5, Clamp Factor) → Mix Color with Blackbody (~2500 K) → Background (Strength 1) → Mix Shader input 1; Background 2 cream, **Strength 10** → input 2; Fac = Light Path **Is Glossy Ray**. Status bar 4.0.2. The interior is now warm and sunlit with soft floor patches.
- [01:55] End card (logo).
- Quality judgement: the final archviz frame is **attractive** (warm, soft daylight, convincing materials — likely a purchased/BlenderKit scene), but the before/after is **misleading**: most of the improvement is simply connecting a sun-lit sky. The strength-10 glossy world is an aggressive reflection boost. Trust stays low–medium; the dual-sky claim remains untested.
