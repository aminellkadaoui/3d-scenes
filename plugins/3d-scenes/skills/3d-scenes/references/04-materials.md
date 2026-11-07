# 04 — Material recipes (values that worked)

General rules (PBR practice, confirmed here): albedo never pure black/white; roughness is the realism map and must vary inside a narrow band (remap with **Map Range**, never feed raw 0–1); colour maps sRGB, data maps Non-Color; disconnect Poly Haven displacement in EEVEE shots.

## Black reflective floor (polished epoxy look) — Proven
- Base texture: Poly Haven `smooth_concrete_floor` (2 m); mapping from **Geometry ▸ Position** (world) × 0.5 = real scale on a scaled plane.
- Base Color → Hue/Sat: Saturation **0**, Value **0.06** → albedo ≈ 0.025.
- Roughness: texture → Map Range From 0.58–0.76 (measure the map) → To **0.02–0.10**.
- **Coat Weight 1.0**, Coat Roughness from the same map → **0.02–0.06**, Coat IOR 1.5.
- Normal Map strength **0.15** (0.3 sparkled under hard light).
- EEVEE: Plane light probe exactly on the floor (z 0.001) covering the visible area; Raytracing on.
- Floor plane scaled ×4 so its edge never shows; dark world backdrop (05 §World).

## Polished black metal turntable top — Proven
- Scratched black metal PBR set, Object coords × 2.
- Roughness Map Range → **0.18–0.30** (min 0.12 gave blotchy sparkle); Metallic from map.
- Normal strength **0.15**. Alpha input unlinked (opacity maps cut holes).
- Keep strong coloured lights **off** this surface with light linking, or it becomes a noisy blue disc.

## Polished stone / marble top — Candidate
Poly Haven `grey_cartago_03` (0.93 m tile: a 37 cm top fits in one tile, no grout). Object coords, Scale 1/0.93, Roughness → 0.05–0.18, Normal 0.25, displacement off.

## Banknotes / paper bundles — Proven
Problem: bundles looked like white soap bars (clipped, bluish, no paper layers).
- Base texture → Hue/Sat Value **0.75** → Multiply **(0.88, 0.92, 0.82)** = warm green-grey.
- Roughness **0.75**.
- **Sheet lines on side faces** (procedural, no UVs): Object Y (stack axis) + Noise(scale 0.08)×0.6 wobble → ×(2π/0.35 object units) → Sine → Map Range −1..1→0..1. Mask = |object normal.Y| < 0.5. Lines → Bump (0.15, distance 0.0005); inverted lines × mask × 0.5 → Multiply darken (0.72,0.72,0.70). ≈85 sheets per bundle. Code: `scripts/paper_stack_material.py`.
- Lighting matters more than the material: see 05 §Hero with white surfaces.

## Laptop body — Proven
Downloaded MacBook materials had Normal strength 1.0 → glittery grain on aluminium under a hard light. Large-body materials → **0.5**; leave keys and small parts.

## Screen
Image Texture → Emission (keep the approved strength, here 0.8), sRGB. If the mapping already has Scale (1,−1) + Location (0,1), orientation is correct — don't "fix" it.
