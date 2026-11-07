# أساسيات الإضاءة في البلندر | Lighting in Blender 3D (Lighting basics)
- url: https://youtu.be/a-IdD-RGb4Q
- channel / duration / Blender version shown: Ali Khadoor / 20:12 / Blender 4.3.0 (stated in description; status bar 4.3.0 confirmed in frames); Cycles used throughout [01:45]
- domain(s): lighting | rendering (light paths) | materials (diffuse/glossy/transmission/volume/SSS) | color
- evidence used: Arabic transcript (auto captions, Levantine dialect; translated by me) + info.json description and chapters + final_19m40.jpg (earlier agent) + 3 contact sheets + 5 frames viewed in §6.
- trust: high for fundamentals. A methodical, physically grounded explanation of rays, bounces, light types and their options, with before/after comparisons described, a reference-photo workflow, and "less is more". Few numeric light powers.

Chapters (from description): 00:00 intro · 00:13 lighting basics · 01:53 light types · 04:05 light render settings · 07:01 light & surfaces · 12:34 light & colour · 14:13 art of lighting (problem solving) · 15:35 colour meanings · 17:14 references · 18:35 less is more · 19:49 outro.

## 1. Problem it solves
Beginners place lights without understanding how Blender (Cycles) transports light, so they can't diagnose dark glass, dead shadows, missing highlights, or flat mood. The video builds the mental model (rays, direct vs indirect, bounces per surface type) and then a design method (problem solving, colour meaning, references, minimal lights).

## 2. Techniques

### T1: Light model: direct vs indirect rays; the shadow is as important as the light  `[00:15]`–`[01:30]`
- What: rays leave the source, hit objects and scatter. Part reaches the camera. Zones: highlight, light half-tone, dark half-tone, shadow, and unlit (black) [00:30]–[00:45]. Adding a floor brightens the sphere's underside through indirect rays, which are weaker after each bounce [00:45]–[01:00].
- Key design rule [01:15]–[01:30]: a product lit from the right has a too-dark left side. Option 1, a second light on the left, kills the shadow, "and the shadow is as important as the light because it gives the sense of the product's dimensions". Option 2, weaken the key. Preferred option 3: put a white surface (bounce card) on the left, outside the frame [01:30]–[01:45].
- Why: fill by bounce preserves shadow direction and a single-shadow look.
- Status: Extracted

### T2: Light types and their options (Cycles)  `[01:45]`–`[04:00]`
- Shift+A > Light: Point, Spot, Sun, Area [01:45]–[02:00].
- Point: emits in all directions. Color, Power. Radius = source size: bigger radius → light spread over a bigger area → softer shadows [02:00]–[02:15]. Soft Falloff: matters only when the light is close to or intersecting a surface. Off = harsh, ungraded; on = smooth. "Generally leave it on" [02:15]–[02:45].
- Spot: a point light confined to a cone. Same Power/Radius/Soft Falloff, plus spot Size (cone angle) and Blend (edge softness of the cone: 0 = hard edge, 1 = gathered toward the centre/softer), Show Cone [02:45]–[03:15].
- Sun: lights the whole scene from a direction, so position is irrelevant and only rotation matters. Strength, and Angle: larger = softer shadows. "I rarely use it" [03:15]–[03:30].
- Area: the author's favourite. Power, Colour, Spread (default 180°; at 0° the lit area equals the light's footprint, like a collimated beam), Shape Rectangle/Square/Disk/Ellipse [03:30]–[04:00].
- Blender 5.2: also Temperature (Kelvin), Exposure (×2^exposure) and Normalize (power independent of size) on lights (manual 5.2). Spot cone property is named "Angle" in the 5.2 manual (UI label "Size" in older versions).
- Status: Extracted

### T3: Per-light render settings: Cast Shadow, Multiple Importance, Shadow Caustics, Max Bounces  `[04:00]`–`[06:45]`
- Cast Shadow off = no shadow. Unrealistic but sometimes useful [04:00]–[04:15].
- Multiple Importance: a light with size (radius > 0) makes a specular highlight on smooth surfaces. With MIS on, the highlight appears in render. Off, it disappears. Example: a point light behind and a spot on a product both giving highlights [04:15]–[05:00]. The author leaves it on. (Technically MIS is a sampling strategy that reduces noise for glossy reflections of lights, and turning it off makes those reflections noisy or missing.)
- Shadow Caustics: glass normally blocks light like an opaque object in Cycles' shadow rays. Enable on the Light (Shadow Caustics), on the glass object (Object > Shading > Caustics > Cast Shadow Caustics) and on the receiver (Receive Shadow Caustics). More realistic, slower [05:15]–[06:00].
- Max Bounces per light (1024 default, effectively unlimited) vs Render > Light Paths > Max Bounces. Total 0 = no indirect; 1 = the environment gets brighter. Default Total 12 [06:00]–[06:45].
- Status: Extracted

### T4: Bounce budget per surface type  `[07:00]`–`[11:15]`
- Diffuse (rough surfaces scatter in all directions): Light Paths > Diffuse bounces 0 means indirect light doesn't reach other parts even if Total = 12 [07:00]–[07:30]. Glossy (mirror-like, redirects rays; roughness spreads them) [07:45]–[08:30]. Transmission (glass): with 0 transmission bounces glass casts black shadows and doesn't show the environment. Raising it gives light through the glass [08:30]–[09:30]. Volume: volume bounces brighten volumes [09:45]–[10:00]. Transparent: 0 = black transparent sphere, 2+ = see-through [10:00]–[10:30].
- Defaults the author keeps: diffuse 4, glossy 4, transmission 12. More bounces = more render time [11:00]–[11:15].
- Lighting relevance: "dark glass", "black interior corners", "dead metal" are often bounce budget problems, not light problems.
- Status: Extracted

### T5: SSS for organic materials  `[11:15]`–`[12:30]`
- Principled BSDF > Subsurface Weight > 0. Radius = RGB scatter distances. Example: cream product looks like hard stone without SSS [12:15]–[12:30]. Lighting relevance: backlighting SSS materials (skin, wax, food, cream) gives a glow that sells realism.
- Status: Extracted (materials cross-ref)

### T6: Colour of light: subtractive surface colour, additive light colour  `[12:30]`–`[14:15]`
- An apple is "everything except red": surfaces absorb all but their colour [12:30]–[13:15]. Coloured light tints everything it hits (a tungsten bulb is orange) [13:30]. Lights mix additively: R+B = magenta/purple, R+G = yellow, G+B = cyan [13:45]–[14:00].
- Why it matters: a coloured light on a surface of complementary colour turns it dark/grey (no energy to reflect). Saturated lights on saturated materials behave in non-intuitive ways.
- Status: Extracted

### T7: Problem solving: glass that won't light → light the environment behind it  `[14:15]`–`[15:30]`
- What: perfume bottle. World set to 0 for full control [14:30]. A spot aimed at the glass doesn't light it, because glass transmits and you only see light after it hits a diffuse surface [14:30]–[15:00]. Solution: remove the point light, add an Area light aimed mainly at the elements BEHIND the product, slightly orange, and a second Area light to light the background more [15:00]–[15:15].
- Why: transparent objects are visible through what they refract and reflect. Light the backdrop and the glass reads (bright-field / dark-field glass photography).
- Status: Extracted

### T8: Colour meaning and mood via light colour and angle  `[15:35]`–`[17:14]`
- Three spot lights aimed at the product, dark environment + blue = mystery [15:45]. Seen [16:05]: a cyan Spot at **3.5 W, Radius 0 m, Spot Size 12.9°, Blend 0.15** on a ~10 cm perfume bottle — tiny powers because the subject is small and close. Keep a Radius on the spots so the product edges get highlights. With radius 0 the highlight vanishes and the product merges with the black background [15:45]–[16:00]. Less mystery: a top spot lighting the background [16:00]–[16:15]. Romance: purple point light [16:15]. Mixed: blue point lights at the product's sides + red point light in the background [16:30]. Method: design the light on the product in a simple environment, then change the environment while keeping the lighting [16:30]–[16:45]. The background point light was replaced by an emissive red sphere (Emission is treated as a material) [16:45]–[17:00].
- Status: Extracted

### T9: References for time of day  `[17:14]`–`[18:30]`
- Noon (from reference photos): white light with a little yellow, sun nearly overhead, hard shadows [17:30]–[17:45]. Sunset: lower sun angle, more spread (softer), orange [17:45]–[18:00]. Night: dim; atmosphere reads blue. Make the area light as big as the whole scene, blue, weak [18:15]–[18:30].
- Status: Extracted

### T10: Less is more + complementary balance  `[18:30]`–`[19:30]`
- Don't add a light unless needed; minimise the light count [18:30]. The same single light did noon and sunset. At night the product became unclear, so add a Spot (easier than an area here) with a little orange on the product, (seen [19:20]: peach Spot **50 W, Radius 0.067 m, Size 12.6°, Blend 0.15**) "because it's the opposite of blue, which adds balance" [18:45]–[19:00]. The background was too dark, so add an orange point light on it, and reduce the blue area light [19:15]. Iterate light + environment until it works [19:30].
- Frame evidence (final_19m40.jpg): final render of a dark amber cosmetic jar ("LARA") on scanned coastal rocks. Warm orange light rakes across the rocks and the jar, the background falls to deep shadow, and the jar label stays readable. A low-key, warm-dominant result, with the blue ambient subtle.
- Why: warm key / cool ambient is the natural night/dusk contrast (tungsten vs sky). Complementary temperature contrast separates the subject.
- Status: Extracted

## 3. Claims I doubt or must test
- "Multiple Importance off removes the highlight": the actual behaviour is noisier or missing highlights depending on roughness. Test.
- The scene-sized blue area light for night is a quick hack. A dim blue world/sky is more natural (directional skylight + correct reflections).
- "Sun rarely used" is a personal (product-artist) preference. For exteriors the sun is essential.

## 4. Anti-AI-slop lessons
- Preserve the shadow. Fill with bounce or by weakening the key, not by adding a second key.
- Light glass through its environment, not by pointing lights at it.
- Night = dim cool ambient + warm motivated accents, not just "dark + neon".
- Use references for sun angle, colour and shadow hardness per time of day.
- Minimal light count. Every light must have a job.

## 5. Candidate isolated test
Perfume bottle (glass) on a plinth, world 0. A: spot on the bottle. B: area light on the backdrop behind the bottle (warm, 2700 K). Measure edge contrast of the bottle silhouette and visible liquid/glass detail. Also a bounce test: transmission bounces 0 vs 12 on the same scene.

## 6. Visual verification (frames viewed)
(final_19m40.jpg described earlier; not redone.)
- Sheets 01, 04, 05: clean explanatory diagrams (camera, rays, light source) [00:15]–[01:00]; handbag shot for the "fill by bounce" example [01:15]–[01:45]; light-type demos in a grey box [02:15]–[03:45]; apple/RGB light-mixing demos [12:30]–[14:00]; rock + perfume glass problem [14:15]–[15:15]; mood variants (teal mystery, pink romance, pink sunset with emissive red sphere) [15:45]–[17:00]; Behance reference search [17:15]; reference photos [17:30], [18:15]; "LARA" jar result [17:45], night version [18:45]; final bust [19:45].
- [03:50] Area light demo: **10 W, Square 0.25 m, Spread 180°**, Cast Shadow + Multiple Importance on, small sphere in a grey box (soft pool + soft shadow).
- [15:10] Glass problem: World Background **Strength 0.000** (confirms "world 0 for full control"); render preview black before lights are added; status bar 4.3.0.
- [16:05] Mystery variant: cyan Spot **3.5 W, Radius 0, Size 12.9°, Blend 0.15** on the perfume bottle (a real brand's bottle model) on a dark glossy floor.
- [18:50] "Result after editing" (warm version): amber jar on sunlit rocks, raking warm light, readable label, deep shadows — reads like a real cosmetics ad.
- [19:20] Night version setup: peach Spot **50 W, Radius 0.067 m, Size 12.6°, Blend 0.15**; preview shows blue ambient rocks with a warm pool on the jar and rock.
- Quality judgement: **professional**. The LARA jar renders (warm and night) are ad-quality: motivated raking light, controlled falloff, complementary warm/cool, restrained grade. Diagrams are clear. High trust stands; the light values are small-scene values (10 cm products, 1–50 W) — scale with distance².
