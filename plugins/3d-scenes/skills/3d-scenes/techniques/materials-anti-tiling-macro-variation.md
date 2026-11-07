---
id: materials-anti-tiling-macro-variation
domain: materials
status: Extracted
sources: [8HfKtaDx6tM@08:30, 8HfKtaDx6tM@10:00, aUnpMrAYzGs@08:15, aUnpMrAYzGs@08:45, aUnpMrAYzGs@10:00]
blender: "5.2"
---
# Break texture tiling: macro colour/roughness variation + rotation bombing
**Principle:** The eye detects repetition when the same feature reappears at a fixed period with the same contrast. Adding a second, much larger-scale variation (2–10× the tile size) and/or randomising tile orientation destroys the period. Real surfaces also vary at large scale (sun fading, wear paths, stains).

**Steps / settings (starting points):**
1. Macro colour variation: Base Color → **Mix Color** (Mix/Overlay), B = same colour via **Hue/Saturation/Value** (Value 0.85–1.1, Saturation 0.8–0.9). Factor = Noise Texture (Scale so blobs are ~2–5× tile size, Detail 2–5, Roughness 0.5–0.6) → Color Ramp, or a grunge image (more natural) [8HfKtaDx6tM@08:45–09:45].
2. Stack 2–3 masks at different scales with Mix Color **Add**, using Factor as opacity [8HfKtaDx6tM@10:00].
3. Apply the same/related mask to roughness (± 0.05–0.1) — colour-only variation looks painted on.
4. Make variation follow structure (bricks/planks): second Mix Color **Color Burn** with base colour through a ramp [aUnpMrAYzGs@10:00]; or per-brick/plank random via Brick/Voronoi cell colour.
5. Stochastic textures (grass, soil, sand, gravel, concrete): rotation bombing — Object coords → **Voronoi** (Color out) → Mapping **Rotation** [aUnpMrAYzGs@08:30]. Doesn't work on structured patterns (seams at cells).
6. Also: mix two scales of the same texture (e.g. ×1 and ×0.37, non-integer ratio) with a large noise mask; add decals/dirt overlays that hide repeats.
7. Hide repetition with composition: props, set dressing, DoF, lighting falloff.

**Use when:** any texture repeated more than ~2–3 times in frame (floors, walls, terrain, large panels).
**Avoid when:** close-ups where one tile fills the frame (unnecessary); variation strong enough to become the dominant feature ("camouflage" blotches).
**Failure signs:** grid-like repeating dark spots across a floor (missing); visible blotchy noise pattern with clean round edges = procedural noise too strong/too smooth; seams at Voronoi cells on bricks.
**Cost:** low (extra lookups); Voronoi bombing breaks texture filtering slightly → possible aliasing at cell edges.
**Conflicts with other sources:** none; both Extra 3d videos agree grunge images beat default noise.
**Test to validate:** 10×10 m floor at ×8 repeats, low camera (1.6 m, 24–35 mm) looking across; A default, B macro variation, C + rotation bombing; count visible repeats in a blind check.
**Log:** 2026-11-05 — Extracted from 8HfKtaDx6tM, aUnpMrAYzGs.
