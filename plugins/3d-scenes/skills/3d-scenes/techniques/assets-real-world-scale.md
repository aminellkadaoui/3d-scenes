---
id: assets-real-world-scale
domain: assets-modeling
status: Extracted
sources: [J_mweAPcO4M@03:30, J_mweAPcO4M@03:45, J_mweAPcO4M@02:15, LPCdpTcNXyM@04:45]
blender: "5.2"
---
# Real-world scale (metres, applied scale, human reference)
**Principle:** Light falloff, DoF, SSS, displacement scale, bevel size, texture feature size, physics and camera height are all scale-dependent. A cup 3 m tall lit like a cup reads like a toy/miniature or a giant — viewers detect scale through DoF, texture grain and light behaviour.

**Steps / settings (starting points):**
1. Scene Units: Metric, Unit Scale 1.0, Length metres.
2. Set object size via **N-panel ▸ Item ▸ Dimensions** in metres from real product specs (not Scale) [J_mweAPcO4M@03:45]; then **Ctrl+A ▸ Scale** (scale returns to 1).
3. Reference human: Add ▸ Armature ▸ Human (Meta-Rig) (Rigify add-on) ≈ 1.8 m [J_mweAPcO4M@03:30]; door 2.0–2.1 m, table 0.72–0.76 m, chair seat 0.45 m, counter 0.9 m, phone ~0.15 m.
4. Imported assets: read world bounding box, scale to known dimension, set origin at bottom, put on ground (Z=0).
5. Texture scale must match: brick ~0.215×0.065 m, floor plank 0.1–0.2 m wide, tile 0.3–0.6 m; scaling textures down makes rocks read as cliffs [LPCdpTcNXyM@04:45] — use this deliberately, never accidentally.

**Use when:** always, at blockout stage.
**Avoid when:** never; for intentional miniature/tilt-shift look change camera DoF, not object scale.
**Failure signs:** non-1 scale values; bevel/displacement inconsistent between objects; DoF too strong/weak for the lens; texture grain wrong size relative to objects; Rigid body behaving floaty.
**Cost:** none.
**Conflicts with other sources:** none.
**Test to validate:** same desk scene at 1× and 10× scale with the same light/camera settings → document what changes (DoF, light falloff, SSS).
**Log:** 2026-11-05 — Extracted from J_mweAPcO4M, LPCdpTcNXyM.
