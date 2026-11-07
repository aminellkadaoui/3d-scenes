---
id: materials-box-projection-object-coords
domain: materials
status: Extracted
sources: [8HfKtaDx6tM@04:30, 8HfKtaDx6tM@07:30, aUnpMrAYzGs@05:30, aUnpMrAYzGs@06:00]
blender: "5.2"
---
# Box (tri-planar) projection with Object coordinates instead of UVs
**Principle:** Box projection samples the texture from X, Y and Z and blends by surface normal, so any mesh gets undistorted texture without UVs. Object coordinates keep texture attached to the object (and in metres if scale is applied), giving consistent texel density across objects.

**Steps / settings (starting points):**
1. Ctrl+A ▸ Scale on the object first (otherwise texture stretches per axis) [8HfKtaDx6tM@07:45].
2. Node Wrangler: select Image Texture nodes → Ctrl+T (adds Texture Coordinate + Mapping). Connect **Object** output.
3. On every Image Texture: Projection **Flat → Box**, **Blend 0.2** (frames: 0.2 on wood PBR maps, 0.3 on grunge masks [8HfKtaDx6tM@10:33, 8HfKtaDx6tM@11:40]) (hold Alt while changing to set all selected) [8HfKtaDx6tM@07:30].
4. Mapping Scale: set so texture's real size matches (e.g. a 2 m × 2 m scan on a 1 m object → Scale 0.5). Keep same Mapping node for all maps of one material.
5. Normal maps in box projection: keep strength moderate (≤0.5–0.7) or use bump from height instead; tangents are not correct per face.

**Use when:** static props without good UVs, AI/scan/kitbash meshes, rocks, terrain chunks, architectural blocks, concrete, plaster, stone, rusted metal.
**Avoid when:** directional textures that must follow form (wood grain on curved parts, fabric weave, brushed metal direction), labels/decals/logos, deforming or animated-shape meshes (texture swims), objects moving through space if using **Generated/World** coords. Hero assets → proper UVs.
**Failure signs:** blurry smeared band at 45° surfaces (blend too high); hard seams at box edges (blend too low); texture "swims" on deformation; different texel size on different objects (unapplied scale).
**Cost:** 3× texture lookups per map (slower on many 4K maps; fine in Cycles/EEVEE for normal scenes).
**Conflicts with other sources:** none; both videos recommend it as the default for non-UV meshes — this card limits that.
**Test to validate:** sculpted rock/AI-generated statue with Smart UV Project vs Box projection blend 0.1/0.2/0.4; check seams and stretching at 3 camera distances.
**Log:** 2026-11-05 — Extracted from 8HfKtaDx6tM, aUnpMrAYzGs.
