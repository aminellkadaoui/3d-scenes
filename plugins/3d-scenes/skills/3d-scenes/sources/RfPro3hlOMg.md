# How to Create PRO Materials in Blender
- url: https://youtu.be/RfPro3hlOMg
- channel / duration / Blender version shown: Kaizen / 17:29 / Blender 4.x–5.x (uploaded 2026-08-25; version not stated in captions)
- domain(s): materials
- evidence used: transcript (auto captions converted from VTT) + contact sheets 01, 03 + 10 extracted frames from the 480p mp4 (see §6).
- trust: medium-high. Clear, principle-oriented ("levels"), physically motivated masks (convex = scratches, occlusion = dirt). Sponsored by Odoo (04:30–05:45, unrelated) and promotes "Realistic Touch" add-on. Some values (soap IOR 3) are wrong.

## 1. Problem it solves
Default Principled BSDF is "dumb": uniform, single-layer. Six levels: basic BSDF → texture detail → value tuning → imperfections & multiple shaders → smart masks from geometry → reusable exposed controls.

## 2. Techniques

### T1 — Basic presets  `[00:30–01:15]`
- Rough plastic: Roughness 0.3–0.8 (+ a bit of Transmission per author — questionable for opaque plastic; Subsurface is the usual choice for thin/translucent plastics).
- Soap bubble: Roughness ~0, Transmission 1, Thin Film Thickness **191 nm**, Thin Film IOR **1.33** (corrected from frames [00:55]); author's base IOR is 3.0 (confirmed on screen) — physically soap film ≈1.33, base IOR for a bubble should be ~1.0–1.33 (Thin Wall in 5.x). Treat as wrong.
- Car paint: Metallic 1, Roughness 0.25, **Coat Weight 1** for clear-coat.
- Blender 5.2 notes: Principled panels: Diffuse, Subsurface, Specular (Distribution, IOR Level, Tint, Anisotropy…), Transmission, Coat (Weight, Roughness, IOR, Tint, Normal), Sheen, Emission, Thin Film (Cycles); **Thin Wall** option for thin sheets; 5.0 adds metallic thin film.
- Status: Extracted

### T2 — Metallic flakes via Voronoi → Normal Map  `[01:30–02:15]`
- What: Voronoi (Scale ~1000, for a car-sized object) → Color Ramp → **Normal Map** node (low strength) → Principled Normal (base, under the coat). Voronoi preferred over Noise because flakes are sharp-edged.
- Why: flakes are tiny tilted mirrors under clear-coat → sparkle that changes with angle.
- Values: Scale depends on object size and camera distance; flakes must be just at/below pixel size, else they look like glitter/noise. Keep Coat Normal clean (coat is smooth).
- Status: Extracted

### T3 — Never use full 0–1 ranges; remap with Map Range / Color Ramp  `[02:30–04:00]`
- What: texture outputs 0–1 → remap to plausible band (e.g. 0.5–0.8). "No material is fully reflective, not even a mirror, so roughness 0 makes no sense — same for 1" [02:45]. Map Range is a little faster than Color Ramp [03:15].
- Why: real surfaces' microfacet roughness lives in narrow bands; full-range noise gives patchy chrome/chalk = CG look.
- Status: Extracted

### T4 — Second shader for dirt + Mix Shader with mask  `[06:00–08:15]`
- What: dirt Principled: two noises → ramp (multiple dirt colours) for colour, another ramp for bump; separate noise for wet/dry roughness variation. Combine with **Mix Shader** (not Add Shader — Add sums energy; used only for effects like dispersion glass [07:15]). Mask through ramp/map range to get crisp, non-mushy transitions [08:00].
- Status: Extracted

### T5 — Imperfections in the correct layer  `[08:30–09:30]`
- What: seamless scratch/fingerprint texture → **Roughness**; for a clear-coated material plug into **Coat Roughness**, since scratches live in the top layer [09:15].
- Why: physical layer logic: what gets scratched is the outermost layer.
- Status: Extracted

### T6 — Smart masks from geometry  `[09:30–13:45]`
- Convex = more scratches; concave/occluded = more dirt; dirt more on bottom of car [09:45].
- **Pointiness** (Geometry node) finds convex/concave — Cycles only, mesh-density dependent [10:30].
- Geometry Nodes: **Store Named Attribute** (Float, **Point** domain per frame [11:15]; author runs Bevel + Catmull-Clark subdiv modifiers before GN to densify; name e.g. "edge_angle") ← **Edge Angle** (Signed Angle) → shader **Attribute** node with same name. Works in EEVEE too [11:00–11:45]. Concave black, convex white by default [12:00].
- Mix Color: A black, B scratch texture, Factor = edge attribute → scratches only on convex parts.
- Dirt: **Ambient Occlusion** shader node → Color Ramp → Mix Shader factor; noise into AO **Distance** for variation [12:45–13:30]. AO node is expensive.
- Blender 5.2 notes: edge-angle attribute is per edge → on low-poly meshes the mask is blocky; densify or blur (Blur Attribute node in GN). AO node in EEVEE is supported but approximate (screen-space horizon scan).
- Status: Extracted

### T7 — Reusable controls through attributes (Geometry Nodes modifier)  `[14:00–16:45]`
- What: Attribute nodes in shader (Base Color, Normal strength, AO control, Voronoi scale) fed by Store Named Attribute in GN, exposed as Group Inputs → controlled from the modifier panel.
- Alternative (simpler): material node group with exposed inputs, or **Attribute node type "Object"** with custom properties; for materials shared across objects, attributes give per-object variation (very useful: one material, varied instances).
- Status: Extracted

## 3. Claims I doubt or must test
- Soap bubble IOR 3 [00:45]: wrong physically.
- Transmission on rough plastic [00:30]: makes it glassy; for opaque plastic use none.
- "Roughness 0 makes no sense" — true in aggregate, but polished chrome/glass ~0.02–0.08 is fine; problem is *uniformity*, not 0 per se.
- Pointiness "doesn't work in EEVEE" — correct.

## 4. Anti-AI-slop lessons
- Imperfections are "the single reason this material looks so much better" [06:00].
- Masks must have physical logic (where would damage/dirt actually occur?) [09:30–10:00].
- Mixed values between two materials that can't coexist (paint vs mud) should be crisp — remap masks [07:45].

## 5. Candidate isolated test
Car-paint sphere + rounded box (bevelled), HDRI studio. A: Metallic 1, Roughness 0.25, Coat 1. B: + Voronoi flakes. C: + scratches in Coat Roughness masked by edge angle. D: + AO-masked dirt. Compare in EEVEE vs Cycles for mask parity and render time.

## 6. Visual verification (frames viewed)
Frames viewed: contact sheets 01 and 03, plus extracted frames below. **Blender 5.2.0** is visible in the status bar ([11:15], [13:45], [16:50]); Cycles, GPU Compute.
- [00:47] Rough-plastic "Puppy": Principled Roughness ≈0.84, IOR 1.5, **Transmission Weight 0.282** (confirms the questionable transmission-on-plastic), Thin Wall checkbox present.
- [00:55] **Correction to T1 soap bubble:** Roughness 0.014, **IOR 3.000** (confirmed — still wrong physically), Transmission 1.0, **Thin Film Thickness 191 nm, Thin Film IOR 1.330** (the earlier "~500 nm / 1.6" was wrong; the on-screen film values are actually physically sensible). Render is very noisy (low samples preview).
- [01:02] Car paint Level 1: Base Color **#E75F00** (H 0.069, S 1, V 0.906, Perceptual) on a Ford Bronco model, black studio with a reflective floor.
- [01:50] Level 2 illustration only (random-colour noise cubes) — no flake values readable; Voronoi Scale ~1000 remains transcript-only.
- [11:15] **Adds T6 detail:** GN modifier stack = **Bevel modifier (Offset 0.1 m, 1 segment, Limit Angle 30°) → Subdivision Catmull-Clark (viewport 3 / render 2) → Geometry Nodes**; Store Named Attribute **Float, domain Point** ← Edge Angle (Signed Angle link being made). So the edge-angle mask relies on bevel + subdivision densifying the mesh first (157k verts on the shaderball) — confirms my "blocky on low-poly" note.
- [13:45] **Adds T6 dirt values:** two Noise Textures (3D fBM, Normalize; Scale ≈1.36 and 3.55, Detail ≈15, Roughness ≈0.57) → Color Ramp (stop at 0.695) → **AO node Distance** input (confirmed; AO **Samples 32**, Inside/Only Local off) → AO → **Map Range, Clamp off, From 0.820–0.940 → To −21.5…21.08** (an extreme, deliberately overdriven contrast to get a hard mask) → Mix Shader Factor. Render settings visible: viewport noise threshold 0.1 / 2048 max; render noise threshold **0.01, Max Samples 500**, Motion Blur on.
- [13:10] Real-footage B-roll (truck in a river) used as reference for "dirt lower on the car" — not a render.
- [16:50] Level 6: GN modifier panel exposes Base Color (#E75D06), **Speckle Scale 2.75, Speckle Strength 0.24, Dirt Level 3.57** — confirms T7 (controls exposed via modifier).
- Final quality judgement: the car look-dev at [16:50] / sheet 01 [01:30] is genuinely good (studio product-shot level), though the car model is a purchased high-quality asset doing much of the work; the speckle/dirt layer is fairly uniform across the body. Instructional graphics are clean. Trust stays medium-high; the physics errors (IOR 3, transmission plastic) are real but values elsewhere are reasonable.
