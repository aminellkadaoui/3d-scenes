# AI-Slop Diagnosis — why agent-built Blender scenes look generic, and how to fix them

> Status: Knowledge (research + expert synthesis). Applies to Blender 5.x (tested target 5.2), Cycles and EEVEE.
> Companion files: `lighting.md`, `materials-pbr.md`, `assets-modeling.md`, `photorealism.md`, `rendering.md`, `color-management.md`, `compositing.md`, `camera-lenses.md`, `composition.md`, `animation.md`, `environment-atmosphere.md`, `art-direction.md`, `production-pipeline.md`.

---

## 0. The one-paragraph theory

"Slop" is what an image looks like when **every decision was left at its default or made without intent**. Professional critique communities say the same thing in different words: *perfection reads as fake* (real life is messy and imperfect — Toolfarm summary of Darren Thomas), *blocky geometry, flat textures, lighting without a plan, weak camera, no post* (Archvis Insider's five CGI mistakes), *add foreground detail, atmospheric perspective, soft shadows, reference photos* (Blender Artists "world, not a render" thread). Agent-built scenes add a second layer of failure on top of the classic amateur ones: an LLM driving Blender through Python naturally reaches for **primitives, round numbers, the origin, symmetric placement, and saturated "cool" colors**, because those are the easiest things to express in code. As one Blender MCP review puts it, the agent is "an excellent operator of Blender and a poor modeller" — organic shapes come out as stretched spheres and boxes.

So the cure is never "add more stuff". The cure is: **replace every default with a decision, and every decision must serve one shot-level idea.**

### The 7 highest-impact slop failure modes (fix these first)
1. **No concept / no hero** — the frame shows "objects", not a moment; nothing is clearly the subject. (C1)
2. **Primitive assembly with razor-sharp edges** — cubes/cylinders/spheres glued together, no bevels, no silhouette detail. (A1, A2)
3. **Default or uniform materials** — 0.8 grey / pure saturated colors, every surface roughness 0.5, no variation, no wear. (M1, M2)
4. **Default lighting** — one sun or one point light at default power, or flat even light; no key/fill/rim ratio, no shaped shadows. (L1, L2)
5. **Default camera** — 50 mm, eye height, aimed at origin, subject dead-centre, no depth layers. (K1, K2, P1)
6. **Void environment & no ground contact** — grey/black world, objects floating or intersecting the floor, no contact shadow, no atmosphere. (E1, E2, E3)
7. **Neon / emissive overuse + wrong view transform** — random glowing strips, saturated cyan-magenta, clipped highlights, `Standard` view transform, no grade. (M5, R2, G1)

---

## 1. How to use this file

- **Before building**: read §3 (Minimum Bar). Every item there is a hard requirement for any shot leaving the blockout stage.
- **While building**: run the bpy audit (§5) after each major stage; fix FAIL items before polishing.
- **After every look-check render**: score with the rubric (§4). Anything < 3 in any domain is a blocker; total < 36/50 is not deliverable.
- **When something "looks off" but you can't name it**: walk the taxonomy (§2) top-down — concept problems masquerade as lighting problems; fix higher layers first.

Order of influence (fix in this order): **Concept → Composition/Camera → Lighting → Environment → Assets → Materials → Animation → Render → Grade**. A perfect material cannot save a frame with no idea and a bad camera.

---

## 2. Taxonomy of slop failure modes

Format per entry: **Symptom** → **Detect (image)** / **Detect (bpy)** → **Root cause** → **Fix**.

### 2.1 Concept & storytelling (C)

**C1. No hero / no idea**
- Symptom: The frame is an inventory of objects; the eye wanders; you cannot say in one sentence what the shot is "about".
- Detect (image): Squint test / 32 px thumbnail: no single area wins in contrast + saturation + sharpness. Ask "what is the first thing I see?" — if the answer is "nothing in particular" or "the background", fail.
- Detect (bpy): No object flagged as hero (custom prop `role="hero"`); camera DOF focus object is None; all objects have similar bounding-box size.
- Root cause: The agent started modelling before writing a shot intent.
- Fix: Write a one-line shot intent ("A lone vintage microphone, lit like a confession, in a dark radio booth"). Choose one hero; everything else is supporting (smaller, darker, less saturated, softer focus).

**C2. Literal / clip-art concept**
- Symptom: "Money" = gold coin cylinder; "growth" = arrow; "security" = padlock floating in space. Reads as stock icon, not cinema.
- Detect: Main subject is a symbol rather than a physical object in a place.
- Root cause: Translating the script word-by-word.
- Fix: Put the idea **in a world**: the padlock on an old server-room door, the coins on a worn desk next to a calculator receipt. Metaphors need context and scale.

**C3. Incoherent world / random props**
- Symptom: Props plausible individually but tell no story about who lives there (a Polycount critique phrasing of "plausible but incoherent" set dressing).
- Detect: Props don't share era, wear level, price class, or palette.
- Fix: Define the occupant/brand/era in the art-direction spec; every prop must answer "why is this here?". See `environment-atmosphere.md` §1.

**C4. Wrong realism level mixing**
- Symptom: photoreal HDRI + toy-like primitives; stylized character on photoscanned ground.
- Fix: Pick one realism level per shot (`art-direction.md` §3) and audit every asset against it.

### 2.2 Composition (P)

**P1. Dead-centre symmetric layout**
- Symptom: Subject at frame centre, horizon at mid-height, objects arranged in a row or ring around the origin.
- Detect (image): Hero centroid within 5% of frame centre when the intent isn't deliberate symmetry; horizon line at 50% height.
- Detect (bpy): Objects' X positions symmetric around 0 (e.g. ±1, ±2), all Y equal; hero at `(0,0,0)`; `world_to_camera_view(scene, cam, hero_loc)` ≈ (0.5, 0.5).
- Root cause: Origin is the agent's default anchor; symmetric numbers are "clean" in code.
- Fix: Place hero on a thirds intersection or use intentional symmetry (Wes Anderson style) *only* when the art spec says so. Break rows: vary spacing, depth, rotation by small irregular amounts (not `random()` everywhere — curated offsets).

**P2. No depth layers**
- Symptom: Everything sits on one plane at one distance; no foreground, no background.
- Detect (image): Depth/mist pass histogram is one narrow spike.
- Detect (bpy): Camera-distance spread of visible objects < 2× (nearest vs farthest).
- Fix: Build FG (out-of-focus frame element), MG (hero), BG (context + atmosphere). Archvis Insider: "use foreground and background layers to create depth".

**P3. Tangents & crowding**
- Symptom: Edges of objects kiss frame edges or each other; hero cropped awkwardly; dead space on one side.
- Fix: Overlap clearly or separate clearly; leave lead room in the direction the subject faces/moves; check silhouette read in a black/white mask.

**P4. Text/logo floating in space**
- Symptom: 3D text hovering in front of everything, unlit, no shadow, no relation to environment, usually default `Text` font Bfont.
- Detect (bpy): `obj.type == 'FONT'` with default font (`data.font.name == 'Bfont'` / "Bfont Regular"), no bevel/extrude, emission material, no surface beneath it.
- Fix: Usually type belongs in the edit (After Effects/Premiere), not the 3D render. If it must be in 3D: real typeface, extrude + bevel (`data.extrude`, `data.bevel_depth`), physically placed (engraved, printed, signage, neon *installed* on a wall), lit and shadowed by the scene.

### 2.3 Assets & modeling (A)

**A1. Primitive assembly**
- Symptom: "Robot" = cube + spheres; "tree" = cylinder + icosphere; "building" = stretched cube.
- Detect (bpy): Many meshes with primitive vertex counts: 8 (cube), 4 (plane), 482 (default UV sphere 32×16), 42/162 (icosphere sub 2/3), 64 (default cylinder 32 verts ×2), names `Cube.###`, `Sphere`, `Cylinder`.
- Root cause: Primitives are the only geometry an LLM can reliably write in a few lines.
- Fix: Prefer real assets (Poly Haven / asset library / `search_assets` → `import_asset`), `generate_3d` for single hero props, or proper modeling (profiles + Screw/Solidify/Array/Curve, geometry nodes). Keep primitives for architecture and hard-surface where they *are* the right tool (walls, plinths, stairs).

**A2. Razor edges (no bevels)**
- Symptom: Perfectly crisp corners that catch no light; CG look on every box. (Classic Packt/3D Environment Design point: "the importance of the bevel modifier"; beveled cube catches light on its corners, sharp cube looks fake.)
- Detect (bpy): Mesh with angles ≈ 90° and no `BEVEL` modifier and no bevel in shader (`ShaderNodeBevel` in node tree).
- Fix: Bevel modifier, Amount ≈ 0.5–3% of the object's smallest dimension (real-world: 1–5 mm on furniture, 0.2–1 mm on electronics), Segments 2–3, Limit Method = Angle (30°), Harden Normals on + shade smooth / auto-smooth. In Cycles a Bevel shader node on the normal is a cheap fallback for distant objects.

**A3. Scale errors**
- Symptom: Door 1.2 m tall, cup the size of a chair; volumetrics/DOF/subsurface behave wrongly; lights look too strong or weak.
- Detect (bpy): `obj.scale != (1,1,1)` (unapplied), `obj.dimensions` outside expected real-world range, `scene.unit_settings.scale_length != 1`.
- Root cause: Agents scale primitives instead of editing them; imported models arrive at arbitrary scale.
- Fix: Model at real-world size in metres; apply scale (`bpy.ops.object.transform_apply(scale=True)` with correct selection/context, or via mesh data transform). Keep a 1.8 m human scale reference (hidden from render) in every scene.

**A4. Uniform scale / clones**
- Symptom: Ten identical chairs, same rotation; same rock repeated.
- Detect (bpy): Many objects sharing one mesh datablock with identical rotation/scale.
- Fix: Variation: ±2–8% scale, small rotation jitter (1–5° for man-made, any for organic), 2–3 mesh variants, per-object material variation via Object Info → Random.

**A5. Over-subdivided / lumpy**
- Symptom: Subsurf on low-poly boxes → blobby, melted shapes.
- Detect (bpy): `SUBSURF` modifier on mesh without support loops/creases.
- Fix: Support loops or bevel before subsurf, or use creases; or drop subsurf and use bevel + weighted normals.

**A6. Intersections**
- Symptom: Objects visibly cutting through each other (cup through table, feet through floor).
- Detect (bpy): BVH overlap test (snippet §5).
- Fix: Snap to surfaces (bounding-box min Z = support top Z), use raycast down for placement.

### 2.4 Materials (M)

**M1. Default material values**
- Symptom: Grey 0.8 plastic everywhere; or a single flat saturated color per object.
- Detect (bpy): Principled BSDF with Base Color ≈ (0.8,0.8,0.8), Roughness = 0.5, Metallic = 0; or objects with no material; or material names `Material`, `Material.001`.
- Root cause: Agent creates material, sets only Base Color.
- Fix: Every material needs: plausible albedo (no pure white > ~0.9 or pure black < ~0.02 linear for non-emissive surfaces), roughness chosen from reference, variation map, and correct metallic (0 or 1, not 0.5). See `materials-pbr.md`.

**M2. Same roughness everywhere / no breakup**
- Symptom: Every surface has identical spec response; reflections perfectly uniform ("CG-perfect", over-glossy — CG Cookie critique).
- Detect (bpy): Roughness inputs unlinked and equal across many materials; no texture/noise node feeding Roughness.
- Fix: Roughness spread across scene (e.g., chrome 0.05–0.15, plastic 0.3–0.5, wood 0.4–0.7, concrete 0.8–0.95) and breakup within each surface: Noise/Musgrave-style textures, grunge maps, AO/curvature masks; ±0.05–0.15 variation.

**M3. No wear, dust, edge highlights**
- Symptom: Showroom-new everything, even in a "lived-in" scene. ("No surface is perfectly clean; add subtle dust, scratches, dirt or edge wear.")
- Fix: Edge wear via Geometry Pointiness (Cycles) or Bevel-node normal difference, AO-masked dirt in crevices, dust on upward faces (Geometry Normal Z), fingerprints/smudges in roughness on glossy hero surfaces. Product shots: minimal but nonzero.

**M4. Wrong physics**
- Symptom: Glass with no thickness, metal with colored diffuse, 0.5 metallic, emission used as lighting fill, IOR 1.0, subsurface on hard plastic.
- Fix: Follow PBR rules in `materials-pbr.md`; glass needs solid geometry; metals tint reflection via Base Color.

**M5. Random emissive strips / neon overuse**
- Symptom: Glowing cyan/magenta lines on every edge "to look futuristic", emission strength 10–50, bloom haze.
- Detect (bpy): Count of materials with Emission Strength > 0 and saturated emission color (HSV S > 0.8); emissive objects > ~10% of visible objects.
- Detect (image): Large % of pixels with saturation > 0.85 and value > 0.9.
- Root cause: Emission is the cheapest way for code to make something "look cool" without lighting.
- Fix: Emissives must be **motivated** (a screen, a sign, a lamp) and rarely the dominant light. Max 1–2 emissive motifs per shot, sized and placed by the art spec. Keep emissive color in the palette's 10% accent.

**M6. Stretched / tiled textures**
- Symptom: Wood grain stretched on one axis (unapplied scale), obvious tiling grid across a floor.
- Fix: Apply scale before UV/box mapping; use Box projection with blend 0.1–0.3 for imported meshes; break tiling with a second texture scale and noise mask, or use Blender's texture-tiling-hiding approaches (e.g. Voronoi-randomized UV offsets).

### 2.5 Lighting (L)

**L1. Single default light**
- Symptom: One Sun (strength 1) or one Point light (1000 W) — hard, flat, characterless; or default "Light" from the startup file at (4.08, 1.0, 5.9).
- Detect (bpy): `len([o for o in scene.objects if o.type=='LIGHT']) <= 1` and no meaningful HDRI; light named `Light` at default location; energy at default (Point 1000 W, Sun 1.0).
- Fix: Design lighting from the art spec: motivated key, controlled fill (or negative fill), rim/kicker for separation, practicals. Ratios: key:fill 2:1 (bright commercial) to 8:1+ (moody). See `lighting.md`.

**L2. Flat, shadowless, or everything-lit**
- Symptom: No dark areas; histogram bunched in the midtones; no shape on forms.
- Detect (image): < 5% of pixels below 10% luminance in a "dramatic" style; luminance std dev low.
- Fix: Light from the side/back (not from the camera), let areas fall off into shadow, use large area lights for soft shape on hero; reduce world strength.

**L3. Unmotivated light**
- Symptom: Bright rim from nowhere, colored lights without sources, sun direction inconsistent with sky HDRI.
- Fix: Every light should have a plausible source or be a cinematographic convention used consistently. Align Sun with HDRI's sun.

**L4. Wrong light size / falloff**
- Symptom: Tiny point lights → harsh pinpoint highlights on everything; shadows razor sharp indoors.
- Fix: Area lights with physically plausible size (softbox 0.6–1.5 m), Sun angle 0.5° (clear) to 5–10° (hazy), Point radius > 0.

**L5. Clipped highlights / crushed blacks**
- Detect (image): > 0.5% pixels at 1.0 in all channels (excluding intended speculars/light sources), > 10% at 0 in non-noir styles.
- Fix: Exposure adjust under Color Management; AgX handles highlights better than Standard; adjust light ratios rather than brute-forcing exposure.

### 2.6 Camera (K)

**K1. Default lens & position**
- Symptom: 50 mm, camera at (7.36, −6.93, 4.96) default startup position or at eye height looking at origin, rotated with a "Track To" on (0,0,0).
- Detect (bpy): `cam.data.lens == 50`, `cam.data.sensor_width == 36`, camera location equals the startup default, Track-To target at origin / empty at (0,0,0).
- Fix: Choose lens by intent (24–35 mm environment/immersion, 50 mm neutral, 85–135 mm product/portrait compression, 100 mm macro). Choose height by intent (low = power, high = vulnerability/overview, table-top height for products). See `camera-lenses.md`.

**K2. No depth of field or fake-strong DOF**
- Symptom: Everything razor-sharp at all depths (CG tell) — or tilt-shift-miniature blur on a full-scale scene.
- Detect (bpy): `cam.data.dof.use_dof == False`; or f-stop < 1.4 on a wide shot.
- Fix: Enable DOF with a focus object; f-stop driven by real-world logic (f/2–f/4 product/portrait, f/5.6–f/11 environment). Correct real-world scale is required for DOF to look right.

**K3. Lifeless static or robotic movement**
- Symptom: Perfectly locked camera or perfectly linear dolly; constant-speed orbit around the origin (the "turntable slop").
- Fix: Motivated moves (push-in for emphasis, lateral parallax for depth), eased curves, subtle handheld noise (very small, 0.2–1°, low-frequency) where the style allows. See `animation.md`.

**K4. Tilted verticals / extreme wide distortion**
- Symptom: Buildings converge, 14 mm on a product.
- Fix: Keep camera level for archviz (use shift_y instead of tilting); avoid < 24 mm unless intentional.

### 2.7 Environment (E)

**E1. Void background**
- Symptom: Default grey world (0.05) or pure black/white endless nothing; objects in "space".
- Detect (bpy): `scene.world is None`; World Background color ≈ (0.05,0.05,0.05) with no Environment Texture / Sky; no background geometry within camera frustum.
- Detect (image): Background corners have very low pixel variance (flat gradient).
- Fix: Either a deliberate **studio sweep (cyclorama)** with gradient lighting, a real environment (geometry + HDRI), or a stylized but designed backdrop. A "dark background" is fine if it has value gradation, light falloff, and maybe atmosphere — not a flat 0. See `environment-atmosphere.md`.

**E2. Floating objects / no contact**
- Symptom: Objects hover millimetres above the floor; no contact shadow; or sink into it.
- Detect (bpy): For each grounded object, `min(world bbox z) - ground_top_z` not ≈ 0 (tolerance ~1 mm at real scale).
- Fix: Raycast-snap to ground; ensure contact shadows (Cycles gives them naturally; EEVEE: enable shadows/raytracing, check Light's `use_shadow`, small soft area light, or add an AO-driven contact darkening). Add small grounding details (dust, slight imprint, a shadow-catching rug).

**E3. No atmosphere / no aerial perspective**
- Symptom: Distant objects as crisp and saturated as near ones.
- Fix: World volume or Mist pass grade; distance desaturation and value lift toward the sky color.

**E4. Missing scale cues**
- Symptom: Can't tell if the object is 10 cm or 10 m.
- Fix: Add known-size objects (door, chair, hand, cable, text on label), correct DOF, correct texture density.

### 2.8 Animation (N)

**N1. Linear / constant-speed motion**
- Detect (bpy): fcurve keyframes `interpolation == 'LINEAR'` or two-key moves with default Bezier auto-clamped handles everywhere.
- Fix: Ease in/out designed in the graph editor; anticipation/overshoot for motion-graphic styles; variable timing.

**N2. Everything moves at once / nothing moves**
- Fix: Staggered timing (offsets 2–6 frames), primary motion + secondary motion (dust, light flicker, slight camera drift).

**N3. Physics-violating motion**
- Symptom: Objects stop dead, no weight, spin forever.
- Fix: Reference real motion; use simulation where cheap (rigid body drop) and bake.

### 2.9 Render (R)

**R1. Noise / fireflies / EEVEE artifacts**
- Detect (image): Speckle in dark areas; shimmering in sequences.
- Fix: Adequate samples + denoiser (OpenImageDenoise), clamp indirect (≈10) for fireflies, light tree on, avoid tiny bright emitters. EEVEE: raytracing, shadow resolution, volume tile size. See `rendering.md`.

**R2. Wrong view transform / Standard**
- Symptom: Hard clipped highlights, oversaturated light sources, "video game" look.
- Detect (bpy): `scene.view_settings.view_transform == 'Standard'` for photoreal work; Look = None with no grade.
- Fix: AgX (Blender 4.x/5.x default) or Filmic; set Look (contrast) by style. See `color-management.md`.

**R3. Missing motion blur**
- Symptom: Staccato, strobing animation.
- Fix: `scene.render.use_motion_blur = True`, shutter 0.5 (180°).

**R4. Wrong resolution / aspect for delivery**
- Detect (bpy): `resolution_percentage < 100` on final; aspect not matching edit (1920×1080, 1080×1920, 3840×2160).

### 2.10 Compositing & color (G)

**G1. Default teal-orange or neon palette**
- Symptom: Teal shadows + orange highlights everywhere regardless of story; or cyan/magenta cyberpunk palette on a finance VSL.
- Fix: Palette from the art-direction spec (`art-direction.md` §4).

**G2. No grade / no finishing**
- Symptom: Raw render: flat, no vignette, no subtle glare, no grain.
- Fix: Minimal finishing stack: exposure/contrast curve, subtle vignette (5–15%), restrained glare on true highlights, fine film grain at delivery resolution, slight chromatic aberration only if style allows. "Overusing filters or lens flares destroys believability" — subtle.

**G3. Overprocessing**
- Symptom: Heavy bloom halos, giant lens flares, oversharpening, HDR look.
- Fix: Each effect must be at a level where removing it is noticed but adding it isn't.

---

## 3. Professional scene minimum bar (checklist)

A shot may not leave lookdev without every box ticked (or a written exception in the art spec):

**Intent**
- [ ] One-line shot intent written; one hero identified (`hero["role"]="hero"`).
- [ ] Art-direction spec exists (style, palette, realism level, references).

**Composition & camera**
- [ ] Lens chosen deliberately (not 50 mm by default); camera not using the default startup location.
- [ ] Hero not dead-centre unless symmetry is specified; horizon not at 50% unless specified.
- [ ] At least 2 depth layers visible (FG/MG/BG); DOF enabled with focus object.
- [ ] Frame aspect matches delivery.

**Assets**
- [ ] All object scales applied (scale == 1) or intentionally instanced; real-world dimensions.
- [ ] Every hard-edged visible mesh has bevel (modifier or shader).
- [ ] No unmodified primitive is a recognizable hero/supporting prop.
- [ ] No unintended intersections; grounded objects touch the ground (±1 mm).
- [ ] Repeated objects varied (scale/rotation/material).

**Materials**
- [ ] No object without a material; no default `Material` values.
- [ ] Roughness varies across materials and within hero materials.
- [ ] Hero has at least one imperfection layer (wear/dust/smudge/variation).
- [ ] Emissives are motivated and count ≤ spec.

**Lighting**
- [ ] ≥ 2 deliberate light contributions (key + fill/env/rim); no default `Light` object.
- [ ] Clear key direction; visible shadow shape on hero; hero separated from background (rim, value or color contrast).
- [ ] No clipped non-specular areas; deep shadows present where style requires.

**Environment**
- [ ] World is set (HDRI, sky, or designed gradient); no default grey void.
- [ ] Background has value variation and supports the hero (darker/lighter/less saturated).
- [ ] Scale cues present; atmospheric depth where distance > ~20 m.

**Render & color**
- [ ] View transform AgX/Filmic (or a justified alternative) with chosen Look/exposure.
- [ ] Noise acceptable at delivery size; motion blur on for animation.
- [ ] Finishing: grade + subtle vignette/grain per spec.

---

## 4. Visual QA scoring rubric (0–5 per domain, 10 domains, max 50)

Score a single rendered frame (or 3 representative frames for animation). Be consistent: **anchor on the descriptions, not on effort spent**. Write one sentence of evidence per score.

Scale meaning: 0 = absent/broken, 1 = slop, 2 = weak, 3 = competent/acceptable, 4 = strong, 5 = professional/portfolio.

| Domain | 1 — slop | 3 — competent | 5 — professional |
|---|---|---|---|
| **1. Concept & story** | Objects shown, no idea; symbol in a void. | Clear subject and setting; idea readable in ~3 s; some props lack purpose. | Instantly readable moment; every element supports one idea; implied before/after (story in the frame). |
| **2. Composition** | Subject dead-centre by accident, row/ring layout, tangents, empty halves. | Thirds/leading lines used, readable silhouette, minor dead space. | Deliberate eye path (contrast → hero → secondary), layered depth, framing devices, negative space used intentionally. |
| **3. Camera** | Default 50 mm at origin, no DOF, eye-level by habit. | Lens/height chosen and sensible, DOF present, verticals controlled. | Lens/height/DOF express the intent (compression, scale, intimacy); feels like a real camera operator chose it. |
| **4. Assets/modeling** | Primitives, sharp edges, wrong scale, clones, intersections/floating. | Proper forms, bevels, correct scale, grounded; some low-detail areas. | Convincing silhouettes and detail hierarchy (big/medium/small), variation, perfect contact, nothing breaks under scrutiny. |
| **5. Materials** | Default grey/flat colors, uniform roughness, no breakup, glowing strips. | Plausible PBR values, roughness differs per material, some variation. | Rich layered surfaces: breakup, wear, dust, edge response, correct physics; materials read at thumbnail and close-up. |
| **6. Lighting** | Single default light or flat even light; no shape, no separation; unmotivated colors. | Key/fill/rim structure, hero separated, shadows shaped, no clipping. | Light tells the mood; deliberate ratios, falloff and motivated sources; value structure guides the eye; shadows as compositional shapes. |
| **7. Environment & atmosphere** | Grey/black void; floating objects; no context or scale. | Coherent backdrop or set, ground contact correct, basic depth cue. | World feels inhabited and specific; atmospheric perspective/volumetrics in service of depth; set dressing tells a story; background supports hero value-wise. |
| **8. Color & palette** | Default saturated primaries/neon, teal-orange by reflex, no hierarchy. | Limited palette, accent reserved for hero, no clashes. | Designed palette (dominant/secondary/accent ~60/30/10), value structure first, color temperature contrast that means something. |
| **9. Render quality** | Noise/fireflies, Standard view transform clipping, aliasing, wrong res. | Clean at delivery size, AgX/Filmic, correct res and motion blur. | Technically invisible: no artifacts at 100% crop, controlled highlights roll-off, consistent across frames. |
| **10. Finishing / comp** | Raw render or overprocessed (giant bloom, flares, oversharpen). | Grade + subtle vignette/glare; consistent with spec. | Finishing feels like a camera + colorist: grain, lens character, grade matched to references; no effect calls attention to itself. |

For animation add **Motion (bonus domain, 0–5)**: 1 = linear/robotic or all-at-once; 3 = eased, staggered, motion blur; 5 = motivated camera language, weight and secondary motion, rhythm matched to edit.

**Decision rules**
- Any domain ≤ 2 → **blocker**; fix before anything else (start with the lowest, highest-influence domain).
- Total ≥ 40 → deliverable for VSL/marketing. 36–39 → deliverable only with user sign-off. < 36 → iterate.
- When scoring yourself, cap a domain at 3 if you cannot name the specific evidence for 4–5. Self-scores inflate; assume a hostile art director.
- Re-score after each change; record score history in the shot log (`production-pipeline.md` §5).

**Image-level quick checks (can be automated on a saved render)**
```python
# run outside Blender or inside with numpy; img = float RGB 0..1 display-referred (the saved PNG/JPEG)
import numpy as np
def quick_stats(img):
    lum = 0.2126*img[...,0] + 0.7152*img[...,1] + 0.0722*img[...,2]
    mx, mn = img.max(-1), img.min(-1)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    h, w = lum.shape; c = max(4, min(h, w)//10)
    corners = np.concatenate([lum[:c,:c].ravel(), lum[:c,-c:].ravel(), lum[-c:,:c].ravel(), lum[-c:,-c:].ravel()])
    return {
        "clipped_%": float((img.min(-1) >= 0.995).mean()*100),     # >0.5% outside light sources = suspect
        "crushed_%": float((lum <= 0.005).mean()*100),              # >10% in non-noir = suspect
        "lum_mean": float(lum.mean()), "lum_std": float(lum.std()), # std < 0.12 → flat
        "neon_%": float(((sat > 0.85) & (mx > 0.9)).mean()*100),    # >3% → neon slop suspect
        "corner_std": float(corners.std()),                         # < 0.01 → flat void background
    }
```
These are flags, not verdicts — a moody noir frame may legitimately have 30% crushed blacks.

---

## 5. Scene-data audit (bpy) — run via `execute_blender_code`

Read-only; prints a report. Thresholds are starting points.

```python
import bpy, math
from mathutils import Vector
from mathutils.bvhtree import BVHTree

sc = bpy.context.scene
deps = bpy.context.evaluated_depsgraph_get()
report = []
def flag(level, msg): report.append(f"[{level}] {msg}")

vis = [o for o in sc.objects if o.visible_get() and not o.hide_render]
meshes = [o for o in vis if o.type == 'MESH']

# --- Assets
PRIM_VCOUNTS = {4: "plane", 8: "cube", 482: "uv_sphere", 42: "ico2", 162: "ico3", 64: "cylinder32", 33: "cone32"}
for o in meshes:
    if any(abs(s - 1) > 1e-4 for s in o.scale):
        flag("WARN", f"{o.name}: unapplied scale {tuple(round(s,3) for s in o.scale)}")
    n = len(o.data.vertices)
    if n in PRIM_VCOUNTS and not o.modifiers:
        flag("WARN", f"{o.name}: looks like raw primitive ({PRIM_VCOUNTS[n]})")
    has_bevel_mod = any(m.type == 'BEVEL' for m in o.modifiers)
    has_bevel_node = any(n.type == 'BEVEL' for s in o.material_slots if s.material and s.material.node_tree
                         for n in s.material.node_tree.nodes)
    if not (has_bevel_mod or has_bevel_node) and n < 5000:
        flag("INFO", f"{o.name}: no bevel (modifier or shader)")
    if not o.material_slots or not any(s.material for s in o.material_slots):
        flag("FAIL", f"{o.name}: no material")
if sc.unit_settings.scale_length != 1.0:
    flag("WARN", f"unit scale_length = {sc.unit_settings.scale_length}")

# --- Grounding (assumes ground top at z=0; adapt)
GROUND_Z = 0.0
for o in meshes:
    zs = [(o.matrix_world @ Vector(c)).z for c in o.bound_box]
    zmin = min(zs)
    if zmin < GROUND_Z - 0.002 and o.get("role") != "ground":
        flag("WARN", f"{o.name}: below ground by {GROUND_Z - zmin:.3f} m")
    elif 0.002 < zmin - GROUND_Z < 0.05:
        flag("WARN", f"{o.name}: floating {zmin - GROUND_Z:.3f} m above ground (no contact?)")

# --- Intersections (pairwise BVH, only small scenes)
if len(meshes) <= 60:
    trees = {}
    for o in meshes:
        ev = o.evaluated_get(deps); me = ev.to_mesh()
        me.transform(o.matrix_world)
        trees[o.name] = BVHTree.FromPolygons([v.co.copy() for v in me.vertices], [p.vertices[:] for p in me.polygons])
        ev.to_mesh_clear()
    names = list(trees)
    for i, a in enumerate(names):
        for b in names[i+1:]:
            if trees[a].overlap(trees[b]):
                flag("INFO", f"intersection: {a} x {b} (ok if intended, e.g. object resting in ground mesh)")

# --- Materials
roughs = []
for m in bpy.data.materials:
    if not m.users or not m.use_nodes: continue
    p = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if not p: continue
    bc, r, mt = p.inputs['Base Color'], p.inputs['Roughness'], p.inputs['Metallic']
    if not bc.is_linked and all(abs(c - 0.8) < 1e-3 for c in bc.default_value[:3]) and not r.is_linked and abs(r.default_value - 0.5) < 1e-3:
        flag("FAIL", f"material {m.name}: default Principled values")
    if not r.is_linked: roughs.append(round(r.default_value, 2))
    if not mt.is_linked and 0.1 < mt.default_value < 0.9:
        flag("WARN", f"material {m.name}: metallic {mt.default_value:.2f} (should be ~0 or ~1)")
    es = p.inputs.get('Emission Strength')
    if es and not es.is_linked and es.default_value > 0:
        ec = p.inputs['Emission Color'].default_value
        mx, mn = max(ec[:3]), min(ec[:3])
        if mx > 0 and (mx - mn) / mx > 0.8:
            flag("INFO", f"material {m.name}: saturated emission strength {es.default_value}")
if roughs and len(set(roughs)) <= 1 and len(roughs) > 2:
    flag("FAIL", f"all unlinked roughness identical ({roughs[0]})")

# --- Lights
lights = [o for o in vis if o.type == 'LIGHT']
if len(lights) <= 1:
    flag("WARN", f"{len(lights)} light(s) in scene")
for l in lights:
    if l.name.startswith("Light") and (l.location - Vector((4.0762, 1.0055, 5.9039))).length < 0.01:
        flag("FAIL", f"{l.name}: default startup light")
    if l.data.type == 'POINT' and l.data.shadow_soft_size == 0:
        flag("INFO", f"{l.name}: zero-radius point light (harsh)")

# --- Camera
cam = sc.camera
if not cam:
    flag("FAIL", "no scene camera")
else:
    if abs(cam.data.lens - 50) < 0.01 and cam.data.type == 'PERSP':
        flag("WARN", "camera lens 50mm (default) – was this chosen?")
    if (cam.location - Vector((7.3589, -6.9258, 4.9583))).length < 0.01:
        flag("FAIL", "camera at default startup location")
    if not cam.data.dof.use_dof:
        flag("INFO", "DOF off")
    for c in cam.constraints:
        if c.type in {'TRACK_TO', 'DAMPED_TRACK'} and c.target and c.target.location.length < 1e-4:
            flag("WARN", f"camera tracks target at origin ({c.target.name})")

# --- World
w = sc.world
if not w:
    flag("FAIL", "no world")
elif w.use_nodes:
    nodes = w.node_tree.nodes
    has_env = any(n.type in {'TEX_ENVIRONMENT', 'TEX_SKY'} for n in nodes)
    bg = next((n for n in nodes if n.type == 'BACKGROUND'), None)
    if bg and not has_env and not bg.inputs['Color'].is_linked:
        c = bg.inputs['Color'].default_value
        if all(abs(c[i] - 0.0508) < 0.01 for i in range(3)):
            flag("WARN", "default grey world (void)")

# --- Color & render
vs = sc.view_settings
if vs.view_transform == 'Standard':
    flag("WARN", "view transform Standard (use AgX/Filmic for CG lighting)")
r = sc.render
if r.resolution_percentage != 100:
    flag("INFO", f"resolution at {r.resolution_percentage}%")
if sc.frame_end > sc.frame_start and not r.use_motion_blur:
    flag("INFO", "animation without motion blur")

# --- Composition: hero position
from bpy_extras.object_utils import world_to_camera_view
heroes = [o for o in vis if o.get("role") == "hero"]
if not heroes:
    flag("WARN", "no object tagged role='hero'")
elif cam:
    p = world_to_camera_view(sc, cam, heroes[0].matrix_world.translation)
    if abs(p.x - 0.5) < 0.05 and abs(p.y - 0.5) < 0.05:
        flag("INFO", "hero at exact frame centre (ok only if symmetry is intended)")

print("\n".join(report) or "clean")
```
Notes: shader node lookups use `n.type` (never localized names); input names like `'Emission Color'` are API identifiers stable across 4.x/5.x — if one raises KeyError, list `[i.name for i in p.inputs]` and adapt. Default-location constants are from the factory startup file and only catch untouched defaults.

---

## 6. Typical "agent scene" fingerprint (what to recognize instantly)

If ≥ 4 of these are true, the scene is slop regardless of how much effort went in:
- Objects named `Cube`, `Cylinder.002`, `Material.003`.
- Everything placed at integer or .5 coordinates, mirrored across X.
- Floor = a single scaled plane (scale 10–50), no material variation, edge visible in frame.
- Background = default world or pure black.
- Camera Track-To an empty at the origin; 50 mm; orbiting turntable animation.
- 1 sun + 1 colored point light (often blue/purple) "for mood".
- Saturated base colors (1,0,0) / (0,0.5,1), roughness 0.5 everywhere.
- Emission strips or glowing spheres used as decoration.
- 3D text in Bfont floating above the object.
- No DOF, no motion blur, no grade, Standard view transform.

---

## 7. Sources consulted

- Toolfarm — "Why Your 3D Renders Look Fake – 5 Tips" (Darren Thomas summary): https://www.toolfarm.com/?p=32693
- Archvis Insider — "Avoid These 5 CGI Mistakes and Improve Your Renders": https://archvisinsider.substack.com/p/avoid-these-5-cgi-mistakes-and-improve
- Blender Artists — "What makes a render look like a world, and not a render?": https://blenderartists.org/t/what-makes-a-render-look-like-a-world-and-not-a-render/593291
- Blender Artists — "How do i make this scene look less fake?": https://blenderartists.org/t/how-do-i-make-this-scene-look-less-fake/1190703 (search result summary)
- CG Cookie — "Feedback: Why does this nice table look CGI?" (search excerpt: over-high glossiness reads as computer-generated perfection): https://cgcookie.com/community/21534-feedback-why-does-this-nice-table-look-cgi
- Packt, *3D Environment Design with Blender*, ch. "Most common modeling mistakes that prevent photorealism" (bevel modifier section, search excerpt): https://subscription.packtpub.com/book/business-and-other/9781803235851/B18697_03.xhtml
- 3D AI Studio — "Blender MCP honest guide" (agent strengths/limits; "excellent operator, poor modeller"): https://www.3daistudio.com/3d-generator-ai-comparison-alternatives-guide/blender-mcp
- arXiv 2601.05016 — Planner–Actor–Critic framework for agent-augmented 3D modeling (LLM-as-critic loops; SceneCraft self-critique): https://arxiv.org/html/2601.05016v1
- Polycount / environment-art discussions on set dressing coherence (search excerpts): https://polycount.com/discussion/comment/2804449
- Blender Manual 5.2 (passes, view layers): https://docs.blender.org/manual/en/latest/
