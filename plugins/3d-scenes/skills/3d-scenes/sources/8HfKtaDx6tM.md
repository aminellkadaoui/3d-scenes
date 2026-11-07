# Photorealistic Texturing In Blender 5.0
- url: https://youtu.be/8HfKtaDx6tM
- channel / duration / Blender version shown: Extra 3d / 14:53 / Blender 5.0 (per title; uploaded 2026-01-19)
- domain(s): materials | assets-modeling
- evidence used: transcript (auto captions, 15s buckets) + contact sheets 02–04 + 11 extracted frames from the 480p mp4 (see §6).
- trust: medium. Intermediate artist, shows before/after on screen (not verified by me), but sponsored (AI 3D generator, 00:58–02:45) and funnels to Patreon / paid "micro details" and grunge packs. Workflow is sound industry practice (layered base → variation → dirt → edge wear → hand-painted detail); some specific claims are simplified.

## 1. Problem it solves
"Applying a Poly Haven material and calling it a day" gives clean, uniform, tiled surfaces. Real objects have colour variation, dirt, grunge, wear and chips [8HfKtaDx6tM@00:15]. The video builds a layered wood table (and a concrete statue, and a glass bonus) to get that variation.

## 2. Techniques

### T1 — Derive roughness + bump from a single photo  `[04:30–06:00]`
- What: Image Texture (photo) → Color Ramp → Principled **Roughness**; same image → **Bump** node **Height** → Principled **Normal**. Move the ramp stops until reflections follow the texture.
- Why: Real photos already contain the chaos of a real surface; luminance correlates loosely with wear (dark = dirt/grooves, light = worn). The ramp remaps luminance into a plausible roughness band.
- Use when: quick real-world surfaces (building façade from a photo) [05:45], background objects, no PBR set exists.
- Don't use when: the photo has baked lighting/shadows (they will show as "dirt" and fight scene light), hero close-ups (resolution), surfaces where colour ≠ roughness (e.g. painted logos).
- Values: ramp output for roughness should land inside ~0.3–0.9, never 0–1 full range (see RfPro3hlOMg@02:45). Bump Strength 0.1–0.3 to start.
- Blender 5.2 notes: unchanged.
- Status: Extracted

### T2 — Box (tri-planar) projection with Object coordinates instead of UVs  `[04:15–04:40, 07:30]`
- What: Node Wrangler Ctrl+T adds Texture Coordinate + Mapping; use **Object** output; set every Image Texture projection **Flat → Box** (hold **Alt** while changing to apply to all selected nodes) and **Blend = 0.2**. Apply object scale (Ctrl+A → Scale) so texture size is consistent.
- Why: Box projection projects from 3 axes and blends at seams, avoiding stretching on unwrapped/AI/scanned meshes. Object space keeps texture locked to the object when it moves.
- Use when: props without good UVs, AI-generated or kitbashed meshes, organic or architectural blocks, non-deforming objects.
- Don't use when: textures with strong direction that must follow the form (wood grain along a curved chair leg, fabric weave on a garment, labels/decals), deforming/rigged meshes, objects scaled differently per axis without applying scale. Normal maps in box projection get slightly wrong tangents — acceptable at low strength, visible at high strength.
- Values: Blend 0.1–0.3 (0.2 default suggestion). Scale in Mapping set from real dimensions (texel density), not by eye only.
- Blender 5.2 notes: unchanged; Node Wrangler shortcuts still Ctrl+T / Ctrl+Shift+T.
- Status: Extracted

### T3 — PBR set import and roughness re-tuning  `[06:00–08:15]`
- What: Download from Poly Haven / ambientCG; select Principled → **Ctrl+Shift+T** (narration says Ctrl+T) → select all maps. Insert Color Ramp after roughness; to make it glossier, lower the **white** stop rather than move handles [07:55–08:15]. Colour adjust with **Hue/Saturation/Value** and **RGB Curves** [08:15].
- Why: scanned sets are calibrated to an average condition; your reference (a "shiny" varnished table) differs → adjust roughness *range*, keep its *variation*.
- Use when: always gather a reference first and decide target gloss [06:45].
- Don't use when: don't crush roughness to a flat value — keep the map's variation.
- Status: Extracted

### T4 — Anti-tiling colour variation with a mask  `[08:30–10:10]`
- What: Base Color → **Mix Color** (factor = mask) with B = same colour through **Hue/Saturation/Value** (Saturation lowered / Value shifted). Mask = Noise Texture → Color Ramp, or better a **grunge image** → Color Ramp. Stack several masks with Mix Color in **Add** mode, using Factor as opacity [10:00].
- Why: tiling is detected by the eye as repeating features at the same contrast; a low-frequency variation at a different scale breaks the period.
- Use when: any tiled material visible across >2–3 repeats.
- Don't use when: variation becomes the visible feature (blotchy "camouflage"). Keep it subtle: ΔValue ~5–15%, ΔSat ~10–20%.
- Status: Extracted

### T5 — Displacement as bump vs true displacement; mixing height/normal  `[10:15–11:00]`
- What: Keep Material ▸ Settings ▸ Surface ▸ **Displacement = Bump Only** by default; switch to **Displacement and Bump** for true displacement (needs geometry). Mix two height maps with Mix Color **Add**; mix normal maps with **Overlay** (approximation).
- Why: true displacement changes silhouette and self-shadowing; bump only changes shading.
- Blender 5.2 notes: the "uncheck bump correction" step [10:30] is unclear — I could not map it to a 5.2 control without frames; treat as unverified. In 5.0+ **adaptive subdivision is no longer experimental** — it's in the Subdivision Surface modifier (Cycles) (developer.blender.org 5.0 Cycles notes). Normal maps: mixing in "Overlay" is not mathematically correct (proper method: Reoriented Normal Mapping, or convert to height/bump chain: Normal Map → Bump node's Normal input).
- Status: Extracted

### T6 — Dirt layer via Mix Shader  `[11:00–11:30]`
- What: Group the base (Ctrl+G). New Principled: dark brown, Roughness = 1 ("max"). **Mix Shader** with a grunge mask as Factor.
- Why: dirt is a different material (different roughness/spec), so mixing shaders (not just colours) is physically more correct.
- Don't: roughness exactly 1.0 for dirt is unnecessary; 0.8–0.95 is more natural; dirt colour must not be near-black (albedo ≥ ~0.04 sRGB-linear) .
- Status: Extracted

### T7 — Edge wear mask from Bevel · Geometry normals  `[11:30–11:50]`
- What: **Vector Math (Dot Product)** of **Bevel** node Normal and **Geometry ▸ Normal** → low on edges (where bevel bends the normal) → Map Range / Color Ramp → multiply with grunge → factor between base and "worn" (orange wood) shader.
- Why: edges get handled, bumped and abraded first in reality; breaking the mask with grunge avoids uniform "outline" wear.
- Blender 5.2 notes: **Bevel shader node is Cycles-only** (EEVEE ignores it). For EEVEE use a stored Edge Angle attribute (see RfPro3hlOMg) or baked curvature.
- Status: Extracted

### T8 — Hand-painted detail via Texture Paint + stencil  `[12:00–13:00]`
- What: Add a new 4K Image Texture as a mask (non-color, black fill), Texture Paint mode, brush Texture Mask = wood/chip image in **Stencil** mapping ("Image Aspect"), Alt+RMB move stencil, Shift/Ctrl+RMB scale/rotate. Paint according to reference. Combine with displacement mix and lower **Midlevel** to push chips inward [13:00].
- Why: procedural masks can't know story-specific damage (where people grab, a corner that got hit). Hand placement = intent.
- Needs UVs (paint is stored in UV space).
- Status: Extracted

### T9 — Statue: concrete + variation + moss via edge-wear mask  `[13:30–14:00]`
- Concrete with displacement → RGB Curves → colour variation layers → moss using the edge-wear mask (moss would more physically use AO / upward-facing normal mask — see doubts).
- Status: Extracted

### T10 — Realistic glass = fingerprints/scratches into roughness + shadow-ray cheat  `[14:15–14:30]`
- (corrected from frames) The shown glass material is Light Path **Is Shadow Ray** → Mix Shader(Glass BSDF Roughness 0 / IOR 1.5, Transparent BSDF) [14:25]; the fingerprint ramp is then linked into the Glass BSDF [14:33].
- What: Fingerprint or scratch image → Color Ramp → Glass/Principled **Roughness** (low range, e.g. 0.0–0.15).
- Why: perfectly smooth glass is the most "CG" surface; real glass shows smudges only in reflections.
- Status: Extracted

## 3. Claims I doubt or must test
- "Object coordinates is the best method" [04:30] — only for static, non-directional materials; UVs remain best for hero, directional, deforming assets.
- Moss using the *edge-wear* mask [14:00] — physically moss grows in crevices/up-facing damp areas: AO/cavity × Z-up normal mask is more plausible.
- Normal maps mixed with Overlay [10:45] — approximate; can tilt normals wrongly. Test vs bump-chaining.
- "Uncheck bump correction" [10:30] — unverified control in 5.2.
- AI-generated statue (sponsor) — quality/topology/UVs unverified; see assets-modeling.md for when AI models are acceptable.

## 4. Anti-AI-slop lessons
- Start from a photo reference and break the material into layers (base, variation, dirt, wear, painted detail) [06:45].
- Roughness must be driven by texture, never a single slider value [04:45].
- Repetition shows when tiled PBR is scaled up — break it with macro variation [08:30].
- Damage placed with intent (hand-painted) reads as story, procedural-only wear reads as filter.

## 5. Candidate isolated test
Table/box mesh (~1 m, scale applied), one HDRI, fixed camera 50 mm. A: Poly Haven wood with defaults. B: + roughness remap + colour variation (T4). C: + dirt + edge wear (T6–T7). Measure: blind A/B/C preference, visible repetition count across the top, render time delta. Also test mask strength at 2 levels to find the "too much" threshold.

## 6. Visual verification (frames viewed)
Frames viewed (480p source, so small numbers are read with some uncertainty): contact sheets 02–04, plus extracted frames below.
- [00:10] DEFAULT vs REALISTIC split screen — the "realistic" side only adds soft macro colour variation and a ragged wall/floor edge; a modest, believable difference, not a dramatic one.
- [04:35] **Confirms T2.** Blender **5.0.1** (status bar), Cycles, GPU Compute, Noise Threshold 0.05, Max Samples 512. Texture Coordinate **Object** → Mapping (Type Point, Scale 0.5/0.5/0.5) → Image Texture with projection **Box**; Blend field being typed. Test objects: sphere / cube / Suzanne.
- [10:33] Wood PBR maps all Box, **Blend 0.200**, Non-Color for roughness/normal/disp; Normal Map (Tangent Space, Strength 1.0); **Displacement node Midlevel 0.5, Scale ≈0.03 (Object Space)**; the viewport shows a wireframe overlay of the table (dense, triangulated Sketchfab mesh). The "uncheck bump correction" control is **not visible** in this frame — still unverified.
- [11:28] Base wood collapsed into a "Wood Base" group; a second Principled is being given an orange/brown colour (worn wood), Roughness still at default 0.5 at that moment — the "roughness = max" step is not confirmed visually.
- [11:40] **Adds exact dirt/wear mask values:** two grunge JPGs (081.jpg, 008.jpg), both Object coords → Mapping (Scale 1.38) → **Box, Blend 0.300** → Mix Color **Add**, Factor 1.0, Clamp Result off / Clamp Factor on → Color Ramp with stops at **0.0 and 0.025** (a very hard, near-binary threshold).
- [12:40] Texture Paint: Brush ▸ Texture Mask = wood-chip image, Mask Mapping **Stencil**, "Image Aspect" button, Size 1/1/1 — **confirms T8**. Wood Chip.001 image texture → Mix Shader Factor (Flat projection, Generated coords shown in node).
- [13:50] Statue: grunge 007.jpg, Box, Blend 0.300, Mapping scale driven by a Value node (1.19), Color Ramp stop at 0.215, then RGB Curves — **confirms T9 layering**. Statue mesh is "tmp34jb11lb.obj" (AI-generated sponsor model) in a dark black-background viewport.
- [14:25] **Correction to T10:** the glass node tree is **Light Path ▸ Is Shadow Ray → Mix Shader (Glass BSDF Multiscatter GGX, Roughness 0.000, IOR 1.500 / Transparent BSDF)** — i.e. the classic transparent-shadow cheat (caustic-free shadows), not just a roughness trick.
- [14:33] A fingerprint/smudge image → Color Ramp (stop at ~0.58) is being linked into the Glass BSDF (link dragged to the Color/Roughness socket area — exact socket ambiguous at 480p); viewport previews the smudge mask on the glass.
- Final quality judgement (sheet 04, [12:15]–[13:15], [14:30]): the table with dirt + chips reads **over-grunged** — a high-contrast white speckle/scratch layer covers the whole top uniformly (classic "grunge filter" look); the wine glass render at [14:30] is decent but shown at small size. Overall intermediate/YouTube quality; the *workflow* is right, the *dosage* is heavier than professional. Treat values (esp. the 0–0.025 ramp) as "too hard" starting points.
