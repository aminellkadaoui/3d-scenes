---
id: materials-displacement-adaptive
domain: materials
status: Extracted
sources: [aUnpMrAYzGs@02:30, aUnpMrAYzGs@04:30, aUnpMrAYzGs@04:45, 8HfKtaDx6tM@10:15, LPCdpTcNXyM@00:00]
blender: "5.2"
---
# Normal vs bump vs true displacement (and adaptive subdivision in 5.x)
**Principle:** Normal/bump change only shading — silhouettes and contact edges stay flat, which is obvious at grazing angles and on edges of stone/brick/terrain. True displacement moves geometry → real silhouette, self-shadowing and parallax. It's expensive and only matters where the camera can see it.

**Steps / settings (starting points):**
1. Default: Material ▸ Settings ▸ Surface ▸ Displacement **Bump Only** with height → Displacement node or normal map.
2. Combine normal map + extra detail: Normal Map node → **Bump ▸ Normal** input, detail texture → Bump Height [LPCdpTcNXyM@00:00] (better than overlay-mixing normals).
3. For grazing/close surfaces (ground, walls at shallow angle, rocks, bricks in close-up): **Displacement and Bump** [aUnpMrAYzGs@04:30]; Displacement node **Scale** in metres (e.g. 0.02–0.05 for a brick wall of 2 m, i.e. real relief depth), **Midlevel** 0.5 (check vendor; some 0).
4. Geometry: Subdivision Surface modifier, enable **Adaptive Subdivision** (Cycles; non-experimental since Blender 5.0), dicing rate ~1 px render; or Simple subdivision levels until features resolve. Don't use fixed level 8 [aUnpMrAYzGs@04:45] (frames: author uses Simple subdiv 8/8 on a 2 m cube with Scale 0.03, Midlevel 0.5 [aUnpMrAYzGs@05:00], and 10/10 on a plane [aUnpMrAYzGs@11:40]).
5. Use 16/32-bit height (EXR) to avoid terracing [aUnpMrAYzGs@02:30].
6. Normal maps: Non-Color, OpenGL (ambientCG "_GL", not "_DX") [aUnpMrAYzGs@03:30]; strength 0.5–1.0, rarely >1.

**Use when:** surfaces with relief > ~5 mm seen at grazing angles or in silhouette.
**Avoid when:** distant objects, flat-ish materials (fabric, plaster) — bump is enough; EEVEE heavy scenes.
**Failure signs:** flat silhouette on obviously rough material (missing); "melting" or stretched spikes (scale too high / midlevel wrong); terraced steps (8-bit height); shading acne/black spots (normal map set to sRGB or DX inverted).
**Cost:** high memory and BVH time for displacement; adaptive reduces.
**Conflicts with other sources:** 8HfKtaDx6tM mentions unchecking a "bump correction" option — unverified in 5.2.
**Test to validate:** stone ground, camera 1.6 m at grazing angle; bump-only vs adaptive displacement; time + visual.
**Log:** 2026-11-05 — Extracted from aUnpMrAYzGs, 8HfKtaDx6tM, LPCdpTcNXyM.
