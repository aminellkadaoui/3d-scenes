---
id: materials-glass-realism
domain: materials
status: Extracted
sources: [8HfKtaDx6tM@14:15, LPCdpTcNXyM@00:30, LPCdpTcNXyM@01:15, LPCdpTcNXyM@02:45]
blender: "5.2"
---
# Believable glass (imperfections, thickness, light-path shortcut)
**Principle:** Perfect glass = invisible or CG-looking. Real glass reveals itself through reflections, edge thickness (green-ish tint in thick soda-lime glass), smudges/fingerprints/dust visible in reflections, and droplets/condensation.

**Steps / settings (starting points):**
1. Principled: Transmission Weight 1, IOR 1.45–1.52, Roughness 0–0.05 base; Base Color very light (≈ 0.95–1.0, slight green/blue for thick glass).
2. Model thickness (Solidify 3–6 mm for windows/glasses); never a single plane for hero glass (or use **Thin Wall** in 5.x for thin sheets).
3. Fingerprints/smudges → Color Ramp → Roughness (0–0.1) [8HfKtaDx6tM@14:15, LPCdpTcNXyM@02:45] (frames: 8HfKtaDx6tM's glass also uses Light Path Is Shadow Ray → Mix(Glass R0 IOR1.5, Transparent) [8HfKtaDx6tM@14:25]); droplets → Bump → Normal [LPCdpTcNXyM@00:30].
4. Interior windows (non-hero): Mix Shader(Glass, Transparent) with Light Path **Is Shadow Ray** as factor → less noise, light enters room [LPCdpTcNXyM@01:15]. Loses caustics.
5. Liquids in glass: overlap liquid volume slightly into glass (≈0.1 mm) and use liquid IOR (water 1.33).

**Use when:** windows, bottles, phone screens' cover glass, product glassware.
**Avoid when:** shortcut (step 4) on hero glass/product caustic shots.
**Failure signs:** glass invisible or black (no thickness / too few transmission bounces — Light Paths Transmission ≥ 8–12); noise/fireflies behind windows; perfectly clean reflection.
**Cost:** transmission is expensive in Cycles; shortcut reduces noise.
**Conflicts with other sources:** none for Cycles. In EEVEE, Principled refraction is screen-space and a liquid inside glass breaks [eevee_full_course@56:40]; use `materials-eevee-archviz-glass` (Transparent + Glossy by Layer Weight Facing) there.
**Test to validate:** interior with window: real glass vs shortcut — noise at equal time.
**Log:** 2026-11-05 — Extracted from 8HfKtaDx6tM, LPCdpTcNXyM.
