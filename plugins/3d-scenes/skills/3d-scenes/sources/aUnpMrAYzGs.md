# Photorealistic Textures In Blender
- url: https://youtu.be/aUnpMrAYzGs
- channel / duration / Blender version shown: Extra 3d / 20:47 / Blender 4.x (uploaded 2025-06-30; version not stated in captions)
- domain(s): materials
- evidence used: transcript (auto captions) + contact sheets 01, 05 + 9 extracted frames from the 480p mp4 (see §6).
- trust: medium. Practical, step-by-step; pushes the author's Patreon micro-details pack and "Cinematic Compositor" add-on. Some value choices are arbitrary (subdiv level 8, AO multiply 0.5).

## 1. Problem it solves
PBR sets look great on a cube/plane but "fall apart" on real models: stretching, repetition, flat look [aUnpMrAYzGs@00:00]. Goal: robust PBR setup, repetition fixes, height-based blending (moss, plaster on brick), vertex-painted masks, decals and micro-detail overlays.

## 2. Techniques

### T1 — Texture resolution by camera distance  `[02:00–02:45]`
- What: extreme close-up → 8K; foreground → 4K; background → 2K. JPG is fine for colour/roughness; download **displacement as EXR** when available (Poly Haven) to avoid 8-bit stepping.
- Why: texel density must match screen pixels; beyond ~1 texel per pixel adds memory, not detail. 8-bit height maps cause terracing under true displacement.
- Values assume 1080p output. For 480–1080p VSL delivery, 2K–4K covers almost everything; 8K only for full-frame macro.
- Status: Extracted

### T2 — Clean Node Wrangler PBR setup  `[03:15–04:30]`
- What: Ctrl+Shift+T, select all maps; on ambientCG **deselect the _NormalDX map** (DirectX), keep _NormalGL (Blender is OpenGL Y+). If NW adds a Bump node and you also have normal/displacement, set its Strength to ~0.1 or 0. AO map: Mix Color **Multiply**, AO in B, Factor 0.5.
- Why: DX normals have inverted green → lighting looks inverted (dents look like bumps). AO in albedo double-counts occlusion the renderer already computes — keep low or skip (author agrees it's optional [04:15]).
- Values: AO multiply ≤0.3–0.5, only for micro-cavities the geometry doesn't contain.
- Status: Extracted

### T3 — True displacement  `[04:30–05:00]`
- What: Material Properties ▸ Settings ▸ Displacement = **Displacement and Bump**; Displacement node **Object Space, Midlevel 0.5, Scale 0.03** (on the default 2 m cube, corrected from frames [04:50]); add Subdivision Surface (author used **Simple** mode, 8 levels viewport+render [05:00], and 10 levels on the moss plane [11:40] — very heavy).
- Blender 5.2 notes: use the Subdivision Surface modifier's **Adaptive Subdivision** (Cycles; no longer experimental in 5.0) instead of a fixed level 8; dicing rate ~1 px at final render. Displacement scale is in object/world units → depends on scene scale; set Midlevel to 0.5 for most scans (check vendor).
- Status: Extracted

### T4 — Object coordinates + Box projection on unwrapped meshes  `[05:15–06:15]`
- Same as 8HfKtaDx6tM T2. Author's justification: big complex objects (mountains, monuments) don't move [05:45].
- Status: Extracted

### T5 — Node groups with exposed Scale / Displacement scale / Height output  `[06:15–07:15]`
- What: Ctrl+G, expose Scale and Displacement Scale as inputs; expose **Height** as an output for later masking. Rename groups.
- Why: makes materials reusable and lets you drive masks from the height map.
- Status: Extracted

### T6 — Anti-tiling: random rotation via Voronoi  `[08:15–08:45]`
- What: Object coords → **Voronoi Texture** → its Color → Mapping **Rotation** (texture bombing light). Works for stochastic surfaces (grass, dirt, sand); fails for structured patterns (bricks) [08:45].
- Why: each Voronoi cell gets a different rotation → no repeating period. Seams appear at cell borders on structured textures.
- Status: Extracted

### T7 — Colour variation that follows the pattern  `[08:45–10:30]`
- What: Noise Texture (Detail max, 4D with W for variants) → Color Ramp → Mix Color **Screen** over base (darkened so subtle). Then to make variation "belong" to the bricks: second Mix Color in **Color Burn** mode with base colour (through a ramp) so variation respects brick/mortar structure.
- Why: a noise unrelated to the texture's structure looks like a projected stain; modulating it by the texture's own values ties it to the material.
- Status: Extracted

### T8 — Height-based material blending (moss in crevices)  `[10:45–12:45]`
- What: Mix Shader(moss, brick). Factor = Mix Color: A = noise mask, B = white, Factor = brick **height** through a contrasted Color Ramp. Result: moss only in the low areas (mortar) and only where noise allows. Remember: factor 0 → first socket shown [11:45].
- Why: in reality, moss/dirt/water collect in low cavities; using the height map grounds the overlay in the surface structure.
- Status: Extracted

### T9 — Gradient mask driven by an Empty  `[13:00–14:15]`
- What: Gradient Texture (Linear) ← Mapping ← Texture Coordinate with **Object = Empty**. Move/scale the empty to slide/sharpen the transition. Combine with noise (Mix Color, colour B black).
- Use when: art-directable transitions (plaster falling off lower part of a wall, rising damp, dust gradient on top).
- Status: Extracted

### T10 — Blending displacement of two materials  `[14:15–15:00]`
- What: Mix Shader can't mix displacement → mix the height outputs with **Mix Color** using the *same mask* and same socket order, feed one Displacement node. Use Shift+RMB-drag to add reroutes.
- Status: Extracted

### T11 — Breaking straight blend seams with Color Burn + height  `[15:00–16:00]`
- What: gradient → Mix Color **Color Burn**, B = main texture height → transition follows bricks. Same with noise (Detail high) for uneven plaster edges.
- Why: real material boundaries follow surface structure; straight/soft gradients read as CG.
- Status: Extracted

### T12 — Vertex-painted masks  `[16:00–17:45]`
- What: apply subdivision (vertex paint needs vertices), Vertex Paint, read via **Color Attribute** node (narration: Attribute node with the name). Use as mask into Hue/Saturation/Value grunge with displacement-derived inverted ramp.
- Blender 5.2 notes: colour attributes appear in Object Data ▸ Color Attributes; use "Color Attribute" node.
- Use when: art-directed placement on dense meshes; no UVs needed.
- Status: Extracted

### T13 — Decals and micro-detail overlays  `[17:45–19:15]`
- What: decal Image Texture with extension **Clip** (not Repeat), Object coords from an Empty, location offset 0.5 on all axes so it centres, decal **Alpha** → (inverted) → Mix Shader Factor; then height map ramp to create a "corrosion" edge. Micro particles: same but Repeat, no empty.
- Status: Extracted

## 3. Claims I doubt or must test
- Subdivision level 8 for displacement [04:45] — 4^8 ≈ 65k× faces per quad; use adaptive subdivision.
- AO multiply 0.5 in albedo [04:15] — double occlusion; in path tracing it's mostly wrong; small values or skip.
- "Since I hate UV unwrapping…" — box projection doesn't replace UVs for hero assets.
- Colour Burn blending tricks are art tricks (non-physical); results vary with texture contrast.

## 4. Anti-AI-slop lessons
- A PBR set alone is not a finished material [00:00].
- Overlays (moss, plaster, dirt) must follow the surface structure (height/crevices), not a random noise [11:45, 15:15].
- Material boundaries should be irregular, not linear gradients [15:30].
- Micro details (particles, decals) push realism [17:45].

## 5. Candidate isolated test
Brick wall 4×2.5 m, camera 35 mm at 1.6 m height, sun + HDRI. A: brick PBR default (tiled ×4). B: + T7 variation. C: + T8 moss in mortar. D: + T11 plaster with irregular edge. Metrics: repetition visible (yes/no in blind check), believability rating, render time (displacement adaptive vs bump).

## 6. Visual verification (frames viewed)
Frames viewed: contact sheets 01 and 05, plus extracted frames below. UI shows **Blender 4.4.0** (status bar) in every frame checked.
- [00:40] "CH#2 Variation" intro: brick plane with displacement, scene uses **EEVEE** (viewport 16 / render 64 samples, Raytracing on). Clean, plausible brick close-up.
- [04:10] Node Wrangler PBR setup on Bricks075A_4K (ambientCG): AO (Non-Color), Base Color (sRGB), Roughness in a "Textures" frame; Principled IOR 1.5. **Confirms T2** layout; AO multiply node not yet visible in this frame.
- [04:50] **Confirms T3 values:** Displacement node **Object Space, Midlevel 0.500, Scale 0.030**; Material ▸ Settings ▸ Surface ▸ Displacement = **Displacement and Bump**. (corrected from frames) the object is the **default 2 m cube** with a rock/stone texture, not a wall.
- [05:00] **Confirms the subdivision claim with detail:** Subdivision modifier in **Simple** mode, **Levels Viewport 8, Render 8** on the cube.
- [08:35] "Tiling" frame: Texture Coordinate → **Voronoi Texture** → Mapping (feeding the brick maps) — confirms T6 topology; Voronoi values unreadable at 480p.
- [09:50] **Adds T7 values:** Noise Texture **4D, fBM, Normalize on, W 0, Scale 14, Detail 15, Roughness 0.5, Lacunarity 2, Distortion 0** → Color Ramp (black → white stop at **0.700**) → Mix Color **Screen** (Clamp Factor on, B = light grey) → Base Color. Principled IOR 1.45 here.
- [11:40] Moss mask: same noise (Scale 14, Detail 15) on a plane with Subdivision **Simple, Levels 10/10** — even heavier than the "8" in the transcript.
- [16:50] Vertex Paint on a subdivided plane; Object Data ▸ Attributes shows a **"Grunge" Face Corner byte-colour attribute**, read in the node tree by an input node (red header) — confirms T12.
- Final quality judgement (sheet 05, [19:00]–[19:15]): brick close-ups are good (convincing scan + displacement); the plaster/graffiti decal shot at [19:15] is demo-level (flat white plaster, cartoon graffiti, grey void background). Techniques are sound; demo scenes are not portfolio-grade. Trust medium.
