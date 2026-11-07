# Assets & Modeling Quality (Blender 5.2)

Status: **Extracted**. Cards: `techniques/assets-bevel-every-edge.md`, `techniques/assets-real-world-scale.md`, `techniques/assets-controlled-chaos-imperfection.md`. Related: `materials-pbr.md`, `photorealism.md`, `composition.md`.
"Most of the scene depends on the models and the textures" [J_mweAPcO4M@03:15]. A great light can't rescue a primitive-looking asset; a great asset survives mediocre light.

---

## 1. What makes an asset read as real
1. **Silhouette** — the first thing the eye reads (and the only thing at distance). Real objects have secondary forms: lips, chamfers, seams, screws, handles, thickness, slight sag. Primitive look = silhouettes of cubes/cylinders/spheres with no secondary or tertiary shapes.
2. **Edges catch light** — bevels (§3).
3. **Correct scale & proportions** (§2).
4. **Thickness** — no zero-thickness walls, screens, leaves for hero use (Solidify; or Thin Wall material for genuinely thin sheets).
5. **Shading quality** — clean normals, no smoothing artifacts (§4).
6. **Imperfection & asymmetry** (§9).
7. **Material quality** — `materials-pbr.md`.
Detail hierarchy: primary forms (big shapes, silhouette) → secondary (bevels, panels, seams, handles) → tertiary (scratches, pores, grain — mostly in textures). Fix in that order.

## 2. Real-world scale
- Units Metric, Unit Scale 1.0. Set **Dimensions** (N ▸ Item) in metres from real specs, not Scale; then **Ctrl+A ▸ Scale** [J_mweAPcO4M@03:45].
- Human reference: Add ▸ Armature ▸ Human (Meta-Rig) ≈ 1.8 m [J_mweAPcO4M@03:30]. Known sizes: door 2.0–2.1 × 0.8–0.9 m; table height 0.72–0.76 m; chair seat 0.45 m; kitchen counter 0.9 m; ceiling 2.5–3.0 m; light switch 1.1–1.2 m high; A4 paper 0.21×0.297 m; smartphone ~0.072×0.15×0.008 m; coffee mug ~0.08–0.1 m tall; laptop ~0.30–0.36 m wide.
- Why it matters: DoF, light falloff, SSS, displacement depth, bevel size, physics (rigid body / cloth), texture scale all assume metres.
- Unapplied scale symptoms: uneven bevels [SaZOuHQROIg@01:15], stretched box-projected textures, weird physics, wrong modifier widths.
- Imported/library/AI assets arrive at arbitrary scale: read world bounding box, scale to known dimension, origin to bottom-centre, place on ground (Z=0 or surface), apply transforms.

## 3. Bevels on every hard edge
Card: `techniques/assets-bevel-every-edge.md`.
- Why sharp CG edges look fake: a mathematically sharp edge has zero area facing the light → no highlight line, so the object reads as a flat cut-out with no material thickness. Real edges (moulded, machined, sanded) have radii 0.2–5 mm and produce a bright rim line along the form — one of the strongest unconscious realism cues [J_mweAPcO4M@03:30; SaZOuHQROIg@01:00].
- Bevel modifier starting points (metres): electronics/small props 0.0005–0.002, furniture 0.002–0.005, architecture 0.005–0.02; Segments 2–3; Limit Method Angle 30°; Clamp Overlap; **Harden Normals** + smooth shading (or Profile ~0.7).
- Shader alternative: **Bevel** node (Radius 0.001–0.003) → Normal input (Cycles only; doesn't change silhouette) — good for heavy/imported meshes.
- Exceptions: blades, paper, thin sheet metal (tiny or no bevel).

## 4. Normals & shading
- Blender 4.1+: legacy "Auto Smooth" mesh setting was removed. Use **Object ▸ Shade Auto Smooth** (adds a "Smooth by Angle" geometry-nodes modifier, angle ~30°) or **Shade Smooth by Angle** (applies sharp edges directly). Keep "Smooth by Angle" modifier **last** in the stack (after Bevel, Subdivision etc.).
- Custom normals: Weighted Normal modifier (Keep Sharp, Face Influence) for hard-surface with large flat faces + small bevels.
- Check: Viewport Overlays ▸ **Face Orientation** (blue = outward, red = flipped → Mesh ▸ Normals ▸ Recalculate Outside, Shift+N); Overlays ▸ Display Normals; matcap with strong highlight to reveal dents/pinching.
- Shading artifacts to catch: black gradients on large flat faces (n-gons + smooth shading), pinching around poles, faceting on curved surfaces (too few segments), seams of duplicate vertices (Merge by Distance).

## 5. Topology and subdivision
- Topology only needs to support: the silhouette at the closest camera distance, deformation (if animated), clean shading, and UVs. Not more.
- Silhouette test: render a black silhouette (holdout / Workbench flat) at the closest framing — any visible polygon facets on curved edges → add segments (cylinders 32–64+ for hero, 16–24 midground) or subdivision.
- Subdivision Surface: support/holding edges or bevel-then-subdiv; Levels Viewport 1, Render 2 for hero hard-surface. **Adaptive subdivision** (Cycles, non-experimental since 5.0) for displacement.
- AI-generated / scan meshes: often dense triangles — fine for static props; use **Decimate** (Collapse ratio) for distant use [8HfKtaDx6tM@02:30]; don't subdivide triangulated scans.

## 6. LOD by camera distance / screen size
| Tier | Screen coverage | Geometry | Textures | Detail effort |
|---|---|---|---|---|
| **Hero** | subject, close-up, >30% frame | full bevels, real thickness, 2–3 bevel segments, subdivision | 4K (8K macro), unique UVs, hand-placed imperfections | max; match reference exactly |
| **Midground** | 5–30% frame | bevel 1–2 segments, decent silhouette | 2K–4K, box projection OK | moderate; good materials, imperfections via masks |
| **Background** | <5% frame | low-poly / decimated, shader bevel or none | 1K–2K | silhouette + colour + value only; scattering/instancing |
Rule from [aUnpMrAYzGs@02:00]: close-up 8K, foreground 4K, background 2K (for 1080p). For VSL delivery at 1080p or lower, budget accordingly. Spend modelling time where the camera spends screen time.

## 7. Library vs procedural vs modelled vs AI-generated
Project policy (CLAUDE.md): prefer good library assets over primitive approximations for hero/foreground.

| Source | Strengths | Licence / caveats | Use for |
|---|---|---|---|
| **Poly Haven** (polyhaven.com) | high-quality scans, real scale, PBR, HDRIs; **CC0** (no attribution, commercial OK) | limited catalogue | props, textures, HDRIs — first choice |
| **ambientCG** | CC0 PBR textures (and some models) | use _GL normals | textures, decals |
| **Sketchfab** | huge catalogue, many free downloads | **check each licence**: CC BY (attribution required), CC BY-SA, CC BY-ND (no modification!), **CC BY-NC (no commercial use — VSL/marketing is commercial)**, CC0; store purchases have moved to Fab — check current terms; quality, scale and UVs vary widely | specific objects not elsewhere; inspect carefully |
| **Fab / Quixel Megascans** | photoscanned assets/surfaces, top realism | licence tiers changed in 2024–25 (Fab Standard / Personal) — verify for commercial use | hero nature/rocks/props |
| **BlenderKit** | in-Blender browser, materials + models | free + paid tiers; Royalty Free or CC0 per asset; account needed (user signs in themselves) | quick set dressing, materials |
| **Poly Pizza** | low-poly | CC0/CC-BY; stylised | stylised scenes only, not photoreal |
| **Procedural (GN/shaders)** | infinite variation, scalable, light | time to build; can look "mathematical" | scatter, cables, repeated architecture, patterns, terrain |
| **Modelled by us** | exact product/brand accuracy | time; quality depends on skill — "result isn't guaranteed" [J_mweAPcO4M@03:15] | the client's hero product (from CAD/photos), simple custom props |
| **AI-generated 3D** (image→3D: e.g. Hitem3D, Tripo — sponsors of [8HfKtaDx6tM@01:00], [J_mweAPcO4M@04:15]; MCP `generate_3d`) | minutes, decent for organic/irregular objects | baked lighting in albedo, mushy small details, melted text/logos, triangle soup topology, arbitrary scale, weak UVs; check provider terms | **acceptable**: background/midground props, organic irregular objects (statues, rocks, food, plants), when nothing suitable exists in libraries. **Not acceptable**: client hero product, brand logos/text, mechanical precision objects, close-ups of thin parts |

Download models for small objects rather than modelling everything — you either give up or each looks less real [SaZOuHQROIg@03:00].

## 8. Asset inspection checklist (run on every imported/generated asset)
1. **Licence** recorded (source URL, licence, attribution text) in `projects/<name>/assets.md`; NC/ND excluded for commercial work.
2. **Scale**: dimensions match real object; scale applied (1,1,1); origin at base; sits on ground.
3. **Orientation**: up axis correct (+Z), front faces −Y if relevant; rotation applied.
4. **Normals**: Face Orientation all blue; no flipped/duplicate faces; Merge by Distance done; shading smooth/auto-smooth correct.
5. **Silhouette** at hero distance: no faceting.
6. **Edges**: bevelled or shader-bevelled.
7. **UVs**: present, non-overlapping where unique textures are used, no extreme stretching (UV checker texture); texel density consistent with neighbours.
8. **Textures**: resolution fits screen size; colour maps sRGB, data maps Non-Color; normal map OpenGL; no baked lighting/shadows in albedo (AI assets especially); paths packed or relative.
9. **Materials**: re-check roughness/metallic plausibility (`materials-pbr.md` §10); replace FBX/GLB auto-materials' flat values.
10. **Polycount**: appropriate for tier (hero OK up to a few million tris in Cycles; instance repeated objects; decimate background).
11. **Naming/collections**: clean names, one collection per asset, no stray cameras/lights from the file.
12. **Visual check**: `look` render under neutral light next to a human-scale reference.

## 9. Imperfection, asymmetry, avoiding the "primitive shapes" look
Card: `techniques/assets-controlled-chaos-imperfection.md`.
- "The real world is chaotic" [R4sOG6OPioc@00:15]: walls aren't flat, edges aren't straight, nothing aligned to a grid.
- Geometry: subtle sculpt Grab waviness on walls/frames (a few mm) [R4sOG6OPioc@01:15]; cushions with sag and wrinkles; cables that droop with gravity; paper with curl; slight dents on metal.
- Placement: Randomize Transform rotation 1–5°, location jitter 0–2 cm [R4sOG6OPioc@01:30]; rigid-body drops for piles [J_mweAPcO4M@06:45]; no identical instances side by side (vary scale 0.9–1.1, rotation, material random).
- Asymmetry: break mirror symmetry on organic/used objects (one worn corner, one dent).
- "Primitive shapes" detector: if an object can be described as "a cube/cylinder/sphere with a material", it's not finished. Add: bevels, secondary shapes (lips, insets, feet, handles, seams), thickness, and real proportions from reference.
- Kitbash consistency: all assets in a shot must share the same level of realism — one low-quality asset next to scans breaks the whole shot.

## 10. Set dressing & storytelling props
- Ask: who lives/works here, what happened just before, what does the viewer need to believe? [R4sOG6OPioc@03:00–03:30].
- Story props at the edges, off walk paths and outside the subject's silhouette; clusters in odd numbers with size variety; leave negative space around the subject (`composition.md`).
- For VSL/marketing: props support the message (e.g. "busy entrepreneur": laptop with real UI, coffee ring stains, notebook, phone) — but never compete with the product. Brand easter eggs (real logos) [J_mweAPcO4M@01:30] carry trademark risk — use generic or client-owned brands.
- Small "proof of life": a slightly pulled-out chair, an open book, a cable plugged in, a jacket on a chair, crumbs, dust on the top shelf.
- Debris/dirt overlays on floors (photo alpha planes) [R4sOG6OPioc@02:30].

## 11. Failure signs (QA)
| Sign | Cause | Fix |
|---|---|---|
| Faceted curves | too few segments | more segments/subdiv for hero tier |
| No edge highlights | no bevels | bevel modifier/shader |
| Uneven bevels | unapplied scale | Ctrl+A Scale, re-bevel |
| Black blotches/gradients | bad normals/n-gons with smooth | Shade Auto Smooth, Weighted Normal, triangulate problem n-gons |
| Toy/miniature feel | wrong scale or texture scale | real dimensions, human reference |
| Floating objects | not on ground / no contact | snap to surface, check contact shadows (`lighting.md`) |
| Grid-perfect placement | no jitter | Randomize Transform, hand placement |
| Mixed realism levels | one weak asset | replace/upgrade or push it out of focus/background |
| Melted logos/text | AI-generated mesh | model/decal the logo; use real asset |

## Sources
Videos: J_mweAPcO4M, SaZOuHQROIg, R4sOG6OPioc, 8HfKtaDx6tM, aUnpMrAYzGs, LPCdpTcNXyM (see `sources/<id>.md`). Blender 4.1 release notes (Auto Smooth → Smooth by Angle), Blender 5.0 Cycles notes (adaptive subdivision). Licence notes: Poly Haven (CC0), Creative Commons licence definitions; Sketchfab/Fab/BlenderKit terms change — verify at download time.
