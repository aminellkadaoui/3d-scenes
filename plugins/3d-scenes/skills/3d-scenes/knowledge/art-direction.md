# Art Direction — defining a visual identity for a shot

> Status: Knowledge (research + expert synthesis). Engine-agnostic; Blender hooks noted.
> Related: `ai-slop-diagnosis.md`, `composition.md`, `lighting.md`, `color-management.md`, `production-pipeline.md` (stage 3).

Art direction is the set of decisions made **before** building that make every later decision easy and consistent. Slop happens when these are left implicit; the agent then falls back on defaults (50 mm, grey, neon, centered). The output of this stage is a short written **Art-Direction Spec** (§8) that every later stage is checked against.

---

## 1. The questions art direction must answer

1. **Purpose**: what must the viewer feel/understand in this shot, and in which part of the VSL (hook, problem, agitation, mechanism, proof, offer, CTA)?
2. **Style category** (§2) and **realism level** (§3).
3. **Value structure** (where is light/dark) — before color.
4. **Palette** — dominant / secondary / accent and temperature logic.
5. **Lighting philosophy** — motivated by what, contrast ratio, hard/soft.
6. **Camera language** — lens family, height, movement, DOF.
7. **Texture/surface language** — clean vs worn, glossy vs matte, detail density.
8. **What is forbidden** — explicit anti-goals (e.g. "no neon, no floating text, no teal-orange").

---

## 2. Style categories (pick one primary; at most one modifier)

| Style | Visual signature | Camera | Light | Materials/texture | Palette | Typical VSL use | Slop risk |
|---|---|---|---|---|---|---|---|
| **Photoreal documentary 3D** | Looks shot on location; imperfect, lived-in | 24–50 mm, eye level, handheld drift, deep-ish DOF | Motivated by sun/windows/practicals, natural ratios | Real wear, dirt, scanned assets | Naturalistic, low-mid saturation | Problem/agitation, "real world" proof | Too clean; CG-perfect surfaces |
| **Product cinematography** | Hero object worshipped; controlled studio | 85–135 mm, macro, slow push/slider, shallow DOF | Large soft sources, strip-light rims, gradient sweeps; reflections designed | Pristine but with micro-variation, perfect bevels | Brand-led, 2–3 colors, neutral BG | Mechanism, offer, packshot | Sterile void, uniform gloss |
| **Archviz** | Believable spaces, architecture-first | 18–35 mm, level camera, vertical correction (shift) | Daylight + interior practicals, balanced exposure | Real material scales, furnishing | Natural, slightly warm | Context, lifestyle, "after" states | Converging verticals, empty rooms |
| **Stylized cinematic** | Film-like but designed (Pixar/Arcane-ish realism level) | Classic film lenses, composed shots, motivated moves | Strong key/rim, colored light motivated by story | Simplified, painterly or hand-crafted detail | Bold limited palette | Storytelling, metaphor scenes | Mixing realism levels; generic "game" look |
| **Minimalist motion-graphic 3D** | Clean shapes, solid colors, graphic composition | Ortho or long lens, locked or precise moves | Soft even studio light, gentle AO, subtle gradients | Matte/clay, soft plastic, frosted glass | Brand palette, 2–4 colors, high value control | Data, process, explainer beats | Default primitives without design, no bevels, harsh light |
| **Dark & moody** | Low-key, mystery, luxury or tension | 35–85 mm, slow moves, shallow DOF | High ratio (8:1+), single dominant source, rim separation, haze | Rich blacks, specular accents | Dominant near-black + one accent | Agitation, premium reveal | Pure black void, invisible hero, neon "for mood" |

Modifiers (choose ≤ 1): *retro-film* (grain, halation, lifted blacks), *clinical* (cool, high-key), *warm nostalgic*, *high-energy* (fast cuts, wide lenses, saturated accent).

---

## 3. Realism level (decide explicitly; never mix accidentally)

| Level | Description | Implications |
|---|---|---|
| R5 Photoreal | Indistinguishable from photo | Real scale, scanned/PBR assets, physical light, camera artifacts (DOF, MB, grain), imperfection everywhere |
| R4 Cinematic real | Real but idealized (commercials) | Same physics; cleaner surfaces; designed lighting allowed |
| R3 Stylized real | Real lighting on simplified shapes | Physical light + simplified, consistent forms/material set; bevels still mandatory |
| R2 Stylized | Designed shapes/colors, believable light | Limited palette, toon-ish materials allowed, consistent rules |
| R1 Graphic | Flat/clay/abstract 3D | Shape language and color system dominate; lighting soft and simple |

Rule: every asset must match the chosen level within ±1 step. A photoscanned rock next to a primitive cube is a realism break.

---

## 4. Palette design

### 4.1 Value first
Design in greyscale before color. A frame with good values works in black & white; color cannot rescue bad values.
- Pick a **value key**: high-key (mostly light), mid-key, low-key (mostly dark).
- Group the frame into **3–4 value masses** (e.g. dark BG, mid environment, light hero face, brightest accent). The hero sits at the point of **maximum value contrast** in the frame.
- Check: desaturate the render (or view the luminance) and squint — the hero must still win.

### 4.2 60-30-10 (dominant / secondary / accent)
A widely used design proportion adopted by filmmakers: ~60% dominant color sets mood, ~30% secondary adds depth so the image isn't flat, ~10% accent draws the eye (e.g. small pops of red against desert and sky in *Mad Max: Fury Road*, per No Film School). Percentages are approximate guides, not measured laws; some films go to two colors (*The Batman*).
- **Dominant (60%)**: environment/background; usually lower saturation.
- **Secondary (30%)**: supporting objects, mid-ground; related hue or temperature contrast.
- **Accent (10% or less)**: reserved for the hero / the message (product, CTA object). **Never spend the accent on background decoration.**

### 4.3 Limited palettes
- 3–5 hues total including neutrals. Define them as hex + role in the spec.
- Neutrals carry most of the frame (warm grey, cool grey, off-white, near-black); pure #000 and #FFF are not neutrals in a lit 3D scene.
- Unify with a shared temperature: light warm / shadows slightly cool (or the reverse) gives coherence without a LUT.
- Saturation hierarchy: highest saturation only at the focal point; desaturate with distance.

### 4.4 Complementary accents — without the teal-orange reflex
Teal-orange works because skin is orange and complementary teal separates it — but as a default it's the most recognizable "generic CG/YouTube grade". Alternatives:
- **Analogous + one complement**: e.g. warm browns/ambers + a single deep green accent.
- **Split-complementary**: dominant blue-grey; accents in amber and coral on hero only.
- **Monochrome + accent**: near-monochrome navy world, one gold product.
- **Brand-derived**: take the brand's primary as the accent, design the dominant as a desaturated neighbor or neutral.
- **Story-derived temperature**: problem = cold/desaturated, solution = warm/clean, proof = natural.

### 4.5 Palette-to-Blender translation
- Colors in the spec are **display (sRGB) hex**; Blender color pickers take scene-linear values internally — enter hex in the picker's Hex field (gamma-corrected) or convert (`srgb → linear`). Remember view transform (AgX) and grade will shift final appearance; validate on render, not on swatches.
- Albedo limits for non-emissive surfaces: avoid linear base color > ~0.9 or < ~0.02.
- Light color is part of the palette: use Blackbody (Kelvin) for natural sources; colored gels only when motivated.

---

## 5. CTLT — Camera, Tone, Lighting, Texture (analysis lens)

Use CTLT to analyze any reference frame and to specify our own shot. It forces you to describe *why* an image works in transferable, buildable terms.

| Lens | Questions | Buildable parameters |
|---|---|---|
| **C — Camera** | Lens length? Height & angle? Distance to subject? DOF depth? Movement? Aspect? Where is the subject in frame? | `lens` (mm), sensor, camera height (m), tilt, f-stop & focus distance, move type/speed, aspect ratio, framing (thirds/centre/negative space) |
| **T — Tone** (value + color + grade) | Key (high/mid/low)? Contrast? Black level (crushed/lifted)? Palette & proportions? Temperature split? Saturation? Grain/halation? | Value key, palette hexes with 60/30/10 roles, view transform + Look, exposure, curves, vignette, grain amount |
| **L — Lighting** | Where is the key (clock position + height)? Hard/soft? Ratio? Rim? Practicals? Motivation? Atmosphere? Time of day? | Light types, positions, sizes, Kelvin, power ratios, world/HDRI strength, volume density |
| **T — Texture** (surface & detail) | Clean or worn? Glossy or matte? Detail density? Micro-surface? Organic vs hard-surface? | Roughness ranges, wear/dirt layers, bevel sizes, asset realism level, detail hierarchy |

Write CTLT for each reference (5–10 lines), then a merged CTLT for our shot.

---

## 6. Reference analysis protocol

For each reference image/clip:
1. **Identify**: source, shot type, why it was chosen (what we like in one sentence).
2. **CTLT breakdown** (§5).
3. **Classify each trait** into one of three bins:
   - **Transferable** — principles we can reuse in any shot: value structure, key direction, ratio, lens family, palette proportion, rim separation, haze for depth, negative-space composition.
   - **Scene-specific** — depends on the reference's content and shouldn't be copied literally: their props, location, specific color of their product, their character's pose, a specific logo.
   - **Unsuitable** — conflicts with our brief/medium/budget: e.g. 30-second VDB explosion when we have 2 hours; anamorphic 2.39 when delivery is 9:16; a horror grade for a finance trust message; things that need assets we don't have.
4. **Extract a rule** from each transferable trait, phrased as an instruction ("key light 90° camera-left, above eye level, 4:1 ratio, warm 3200 K; BG two stops under hero").
5. **Note conflicts** between references and resolve them (pick one).

Never copy a reference wholesale — copyright and coherence both suffer; combine principles from 3–6 references into one identity.

---

## 7. Building the moodboard / reference set

- **Size**: 6–12 images per shot family; 1 **master reference** (defines the look), 2–4 lighting refs, 2–3 composition/camera refs, 2–3 material/texture refs, 1–2 color/grade refs.
- **Sources**: film stills (ShotDeck, FilmGrab), photography (product, architecture), ArtStation/Behance 3D (only for craft, not as a look to copy), real-world photos for materials and scale, the brand's own assets.
- **Annotate** every image with its role and the 1–2 traits to transfer.
- **Contrast set**: include 1–2 "anti-references" (what we must not look like — e.g. a generic neon AI render).
- **Store**: `projects/<project>/refs/` with a `refs.md` index (image path, role, CTLT notes, transferable/specific/unsuitable).
- In Blender, references can be loaded as Reference Images (Add → Image → Reference) in a hidden collection, or compared side by side with renders via the `look` tool.
- The user's own `brand-moodboard` / `style-moodboard` skills can produce the board; this file defines what the 3D agent extracts from it.

---

## 8. Writing an Art-Direction Spec Claude will follow

Keep it **short, numeric, testable**. Vague words ("cinematic", "premium", "moody") must be translated into parameters. Each line should be checkable against a render or the scene data.

### Template

```markdown
# Art-Direction Spec — <project> / <shot id>
Purpose: <what the viewer must feel/understand; VSL beat>
Shot intent (one line): <e.g. "A worn leather wallet, empty, on a kitchen table at 2am — quiet anxiety">
Style: <category> + <modifier?>     Realism level: R<1-5>
Master reference: <path>  | Supporting refs: <paths with roles>
Anti-references / forbidden: <e.g. neon strips, floating 3D text, teal-orange grade, pure black void, centered symmetry>

CAMERA
- Lens: <mm> | Height: <m> | Angle: <°> | Distance: <m> | f-stop: <f/x>, focus on <object>
- Framing: hero at <thirds pos>, negative space <side> for captions | Aspect: <16:9 / 9:16>
- Movement: <type, distance, duration, easing>

TONE
- Value key: <low/mid/high>; hero is the brightest/most contrasty element; BG ≈ <n> stops under hero
- Palette: dominant <hex, role> ~60% | secondary <hex> ~30% | accent <hex> ≤10% (hero only)
- Temperature logic: <warm key / cool ambient>, Kelvin key <K>, fill <K>
- View transform: AgX, Look: <e.g. Medium High Contrast>; grade: <notes>; grain <amount>; vignette <%>

LIGHTING
- Motivation: <window / practical / sun / studio>
- Key: <type, size, position (clock + elevation), Kelvin>; Fill: <ratio key:fill>; Rim: <yes/where>
- Practicals: <list>; Atmosphere: <none / haze density target> 

TEXTURE
- Surface language: <clean / lived-in / worn>; gloss range <roughness min-max>
- Hero imperfections: <list>; bevel standard: <mm>
- Asset sources: <library / generate_3d / modeled>

ENVIRONMENT
- Setting/occupant brief: <one line>; background type: <cyc / set / HDRI+geo>
- Scale cues: <list>; time of day/weather: <...>

ACCEPTANCE
- Rubric targets (ai-slop-diagnosis §4): all domains ≥ 3, Lighting ≥ 4, Concept ≥ 4; total ≥ 40
- Must-pass checks: <e.g. hero readable at 10% thumbnail; caption-safe area clear>
```

### Rules for the agent following a spec
1. Read the spec before every stage; quote the relevant lines in your plan.
2. When a choice isn't covered, decide in the spirit of the master reference and **write the decision back into the spec** (it is a living document).
3. If the spec conflicts with the render (e.g. palette looks wrong under AgX), adjust the scene, not the spec — unless the user approves a spec change.
4. Every QA pass compares render vs spec line by line, then scores the rubric.

---

## 9. Quick palette starters (not defaults — starting points to adapt)

| Mood | Dominant | Secondary | Accent | Notes |
|---|---|---|---|---|
| Trust / finance | Deep navy-grey #1E2733 | Warm stone #BDB5A6 | Muted gold #C9A24B | Avoid neon green "money" |
| Anxiety / problem | Desaturated cool grey-green #4A5550 | Sodium amber practical #B07A3A | Warning red (small) #A63A2E | Low-key, high ratio |
| Clean health / solution | Off-white #EEEAE3 | Sage #9AAE9A | Fresh coral #E07A5F | High-key, soft light |
| Luxury / premium | Near-black warm #141110 | Bronze #6B5038 | Champagne highlight #E8D3A8 | Specular accents, haze |
| Tech / mechanism (non-neon) | Graphite #2B2E33 | Cool silver #A7AEB6 | Single brand hue | Light the forms, not glowing strips |

---

## 10. Sources consulted

- No Film School — "What Is The 60-30-10 Color Rule in Filmmaking?": https://nofilmschool.com/60-30-10-color-rule
- Wolfcrow — "Why Great Movies use the 60-30-10 percent Color Rule" (search excerpt): https://wolfcrow.com/why-great-movies-use-the-60-30-10-percent-color-rule/
- No Film School — Wes Anderson "3 color rule" (search excerpt): https://nofilmschool.com/wes-anderson-color-palatte
- Archvis Insider — "Avoid These 5 CGI Mistakes" (planned lighting, camera layers, post): https://archvisinsider.substack.com/p/avoid-these-5-cgi-mistakes-and-improve
- Blender Artists — "What makes a render look like a world, and not a render?" (reference photos, mood via season/light): https://blenderartists.org/t/what-makes-a-render-look-like-a-world-and-not-a-render/593291
- Environment-art reference practice (main reference defines the scene; search excerpts): https://80.lv/articles/building-uncharted-inspired-environment-in-blender-with-storytelling-focus
- CTLT, realism levels and the spec template are synthesized for this knowledge base (no single external source).
