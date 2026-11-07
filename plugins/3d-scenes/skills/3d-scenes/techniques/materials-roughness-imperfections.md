---
id: materials-roughness-imperfections
domain: materials
status: Extracted
sources: [8HfKtaDx6tM@04:45, 8HfKtaDx6tM@14:15, SaZOuHQROIg@01:30, RfPro3hlOMg@08:30, RfPro3hlOMg@09:15, LPCdpTcNXyM@02:45]
blender: "5.2"
---
# Roughness variation & surface imperfections (smudges, fingerprints, scratches)
**Principle:** Roughness is what the eye reads first on glossy/semi-glossy surfaces: real surfaces have uneven micro-roughness (finger grease, wiping streaks, dust, micro-scratches). A single roughness value gives perfectly even highlights — the strongest "CG/plastic" tell. Imperfections are only visible *in reflections/highlights*, so they cost nothing in albedo realism and are very forgiving.

**Steps / settings (starting points):**
1. Keep the material's own roughness map (or a base value) → **Map Range** into a plausible band (e.g. plastic 0.35–0.55, varnished wood 0.25–0.45, glass 0.0–0.08).
2. Add a seamless imperfection texture (smudges/fingerprints/scratches, Non-Color) → **Map Range** to a narrow delta (e.g. To Min 0, To Max 0.15–0.3).
3. Combine: **Math ▸ Add** (base + delta, clamp) — or **Mix (Float/Color) Overlay/Lighten**, factor 0.3–0.6. Avoid plain *Multiply* unless the map was remapped around 1.0 (Multiply with a mostly-dark smudge map makes the whole surface glossier) [SaZOuHQROIg@02:00].
4. Coated materials (car paint, varnish, lacquered phone backs): feed imperfections into **Coat ▸ Roughness**, not base Roughness [RfPro3hlOMg@09:15].
5. Glass: imperfection/fingerprint → ramp → Roughness in 0–0.1 range [8HfKtaDx6tM@14:15]; droplets → Bump → Normal [LPCdpTcNXyM@00:30].
6. Optionally mask scratches to convex edges (see materials-smart-masks-edge-wear-dirt).
7. Mapping: imperfection textures should be at real-world scale (a fingerprint ≈ 1.5–2 cm) — Object coords + Mapping Scale from dimensions.

**Use when:** almost every visible glossy or semi-glossy surface: screens, glass, metal, plastic, varnished wood, ceramics, car paint.
**Avoid when:** fully matte materials (raw concrete, fabric) where it's invisible; hero "brand-new product" packshots — keep it extremely subtle (smudges only near grip areas) so the product doesn't look dirty.
**Failure signs (how QA detects it went wrong):** highlights perfectly uniform (missing); or reflections look "dirty/greasy" and blotchy (too strong); visible repeating fingerprints (scale too small, tiling); imperfections visible in diffuse colour (plugged into albedo by mistake).
**Cost:** negligible (one/two texture lookups).
**Conflicts with other sources:** SaZOuHQROIg uses Multiply; RfPro3hlOMg plugs the texture straight into roughness. Both work only with specific map ranges — remap first.
**Test to validate:** sphere + rounded box, studio HDRI with a softbox strip; A uniform roughness vs B with imperfections at 3 strengths; judge highlight breakup at 1080p and 480p (VSL delivery).
**Log:** 2026-11-05 — Extracted from 8HfKtaDx6tM, SaZOuHQROIg, RfPro3hlOMg, LPCdpTcNXyM.
