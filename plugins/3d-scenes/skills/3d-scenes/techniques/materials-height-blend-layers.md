---
id: materials-height-blend-layers
domain: materials
status: Extracted
sources: [aUnpMrAYzGs@10:45, aUnpMrAYzGs@12:00, aUnpMrAYzGs@13:00, aUnpMrAYzGs@14:45, aUnpMrAYzGs@15:15, 8HfKtaDx6tM@13:00]
blender: "5.2"
---
# Height-map-driven material blending (moss in crevices, plaster over brick, chips)
**Principle:** Secondary materials don't sit on a surface randomly: moss, dirt, water and dust fill low areas; plaster remains on high/flat areas and breaks along the underlying structure; chips expose material below. Using the base material's height map in the mask makes overlays obey the surface structure.

**Steps / settings (starting points):**
1. Expose **Height** output from your base material group [aUnpMrAYzGs@07:00].
2. Height → **Color Ramp** (contrasty: stops ~0.35/0.5) → Factor of Mix Color(A = noise mask, B = white) → Mix Shader Factor (factor 0 = first socket) [aUnpMrAYzGs@12:00–12:30].
3. Art-directable gradient: Gradient Texture (Linear) with Texture Coordinate ▸ **Object = Empty** → move/scale the Empty [aUnpMrAYzGs@13:15–14:00].
4. Make straight transitions follow structure: Mix Color **Color Burn**, B = base height (or noise with high Detail) [aUnpMrAYzGs@15:15–15:45].
5. Displacement: Mix Shader cannot mix displacement → mix the two heights with **Mix Color** using the same mask & order, into one Displacement node [aUnpMrAYzGs@14:45].
6. Chips: lower Displacement **Midlevel** of the chip layer to push it inward [8HfKtaDx6tM@13:00].

**Use when:** layered environment materials (walls, ground, ruins, old wood), any "material A partially covered by B".
**Avoid when:** clean modern surfaces; when the base has no meaningful height map (flat-photo textures).
**Failure signs:** moss/dirt on top of bricks instead of in mortar (inverted); perfectly straight or perfectly soft boundaries; displacement steps at material boundary (heights not mixed with same mask).
**Cost:** low for shading; displacement cost depends on subdivision (use adaptive subdivision, 5.0+).
**Conflicts with other sources:** none.
**Test to validate:** brick wall with moss: A noise-only mask vs B height-driven; blind believability.
**Log:** 2026-11-05 — Extracted from aUnpMrAYzGs, 8HfKtaDx6tM.
