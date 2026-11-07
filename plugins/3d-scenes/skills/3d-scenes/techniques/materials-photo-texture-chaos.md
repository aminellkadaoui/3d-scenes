---
id: materials-photo-texture-chaos
domain: materials
status: Extracted
sources: [R4sOG6OPioc@01:45, R4sOG6OPioc@02:15, 8HfKtaDx6tM@04:45, 8HfKtaDx6tM@05:45, J_mweAPcO4M@02:45]
blender: "5.2"
---
# Real-photo textures & photographed debris overlays (capture real chaos)
**Principle:** A photograph contains real-world randomness (grime, leaks, discoloration) that procedural or seamless PBR sets smooth away. Using photos — as albedo plus derived roughness/bump, or as alpha debris overlays — imports believable chaos cheaply.

**Steps / settings (starting points):**
1. Non-seamless photo (e.g. whole wall) → UV-unwrapped/projected so it doesn't tile [R4sOG6OPioc@02:00].
2. Derive roughness: photo → Color Ramp (to ~0.4–0.9) → Roughness; bump: photo → Bump Height (Strength 0.1–0.3) [8HfKtaDx6tM@04:45–05:45].
3. Debris overlay: photograph dirty dark surface → crush blacks → alpha; plane with colour → Base Color, matte → **Alpha**; duplicate, F3 **Randomize Transform** (Z rotation) [R4sOG6OPioc@02:30–02:45]; offset 1–2 mm above floor.
4. Prefer flat, overcast-lit photos (no hard shadows); de-light (high-pass/flatten in an image editor) if needed.

**Use when:** environments, backgrounds, old/inhabited spaces, quick photoreal façades.
**Avoid when:** photos with baked directional light or perspective; close-ups beyond the photo's resolution; when copyright of the photo is unclear (use own photos or CC0).
**Failure signs:** shadows in the texture contradicting scene light; blurry close-up; overlay planes floating or z-fighting; repeated identical debris patches.
**Cost:** low.
**Conflicts with other sources:** seamless-PBR-first workflow of 8HfKtaDx6tM/aUnpMrAYzGs; resolve: PBR for structure, photos for unique grime.
**Test to validate:** room floor: PBR-only vs + 5 debris overlay planes; blind check.
**Log:** 2026-11-05 — Extracted from R4sOG6OPioc, 8HfKtaDx6tM, J_mweAPcO4M.
