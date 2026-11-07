---
id: assets-bevel-every-edge
domain: assets-modeling
status: Extracted
sources: [SaZOuHQROIg@01:00, SaZOuHQROIg@01:15, J_mweAPcO4M@03:30]
blender: "5.2"
---
# Bevel every hard edge (modifier or shader), with applied scale
**Principle:** Real manufactured edges are rounded (0.2–5 mm typically). A rounded edge catches a thin highlight line that defines form; a mathematically sharp CG edge has no highlight and reads as a cut-out/fake. "No object in real life has sharp edges" [J_mweAPcO4M@03:30], except blades [SaZOuHQROIg@01:00].

**Steps / settings (starting points):**
1. Ctrl+A ▸ **Scale** first (otherwise bevels differ per axis) [SaZOuHQROIg@01:15].
2. **Bevel modifier**: Amount (Width) in metres: small props 0.5–2 mm, furniture 2–5 mm, architecture 5–20 mm; **Segments 2–3** (3 for hero close-ups); Limit Method **Angle** (30°); **Harden Normals** on (requires smooth shading) or Profile 0.5–0.7. Clamp Overlap on.
3. Shading: **Shade Auto Smooth** (4.1+: adds "Smooth by Angle" modifier; keep it *after* Bevel in stack) or Shade Smooth + Harden Normals.
4. Alternative for heavy/imported meshes: **Bevel shader node** (Radius 1–3 mm) → Principled Normal (Cycles only; shading only, silhouette unchanged).
5. Check on silhouette and with a highlight: the edge should show a thin bright line facing the key light.

**Use when:** every manufactured hard-surface object visible in frame.
**Avoid when:** objects are truly sharp (blades, paper edges, thin sheet metal — use tiny bevel 0.1 mm or none); very distant objects (invisible; save polys); already-bevelled library assets.
**Failure signs:** no edge highlights (missing); "pillowy/inflated" look (too large); uneven bevels (unapplied scale); shading artifacts/black gradients around bevel (Auto Smooth/Harden Normals missing); overlapping geometry (Clamp Overlap off).
**Cost:** low-moderate polycount (segments × edges).
**Conflicts with other sources:** none.
**Test to validate:** cube/phone slab; no bevel vs 1 mm/3 segments vs shader bevel; check highlight in studio HDRI at 1080p.
**Log:** 2026-11-05 — Extracted from SaZOuHQROIg, J_mweAPcO4M.
