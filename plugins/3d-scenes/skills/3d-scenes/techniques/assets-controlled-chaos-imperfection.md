---
id: assets-controlled-chaos-imperfection
domain: assets-modeling
status: Extracted
sources: [R4sOG6OPioc@00:15, R4sOG6OPioc@01:15, R4sOG6OPioc@01:30, R4sOG6OPioc@03:00, J_mweAPcO4M@06:30, J_mweAPcO4M@06:45]
blender: "5.2"
---
# Controlled chaos: break perfect geometry, alignment and emptiness
**Principle:** "The real world is chaotic" [R4sOG6OPioc@00:15]: walls aren't perfectly flat, frames aren't perfectly aligned, objects aren't placed on a grid, inhabited spaces contain clutter. CG defaults (perfect planes, 0° rotations, symmetric arrangement, empty floors) are the strongest scene-level slop signal.

**Steps / settings (starting points):**
1. Geometry waviness: subdivide, Sculpt **Grab** brush low strength, push/pull a few mm–1 cm on room-scale walls/frames [R4sOG6OPioc@01:15]. Or Displace modifier with large-scale noise, Strength 2–10 mm.
2. Rotation/placement jitter: select props → F3 **Randomize Transform** (Rotation 1–5°, Location 0–2 cm) [R4sOG6OPioc@01:30]; never two identical instances at identical rotation.
3. Physics drop for random piles: Rigid Body Active (props) / Passive (ground), apply scale, bake, apply transforms [J_mweAPcO4M@06:45].
4. Storytelling clutter: ask "who lives/works here? what happened just before?" → 5–15 props at the edges, off walk paths [R4sOG6OPioc@03:00–03:30]; group in clusters (odd numbers, varied sizes), leave negative space around the subject.
5. Keep hierarchy: chaos in secondary areas; hero object clean and readable.

**Use when:** environments, lived-in interiors, product-in-context shots.
**Avoid when:** minimal studio packshots, clean-brand aesthetics (here, chaos = subtle surface imperfections and natural light only); when clutter competes with the subject.
**Failure signs:** everything axis-aligned and evenly spaced (missing); scene looks messy with no focal point (too much); melted/jelly walls (sculpt too strong); clutter in the subject's silhouette.
**Cost:** time; modest polycount.
**Conflicts with other sources:** marketing/brand clean look vs. chaos — resolved by shot purpose (see art-direction.md).
**Test to validate:** room A clean vs B chaos pass; blind "photo or CG" rating; check focal clarity with a squint/blur test.
**Log:** 2026-11-05 — Extracted from R4sOG6OPioc, J_mweAPcO4M.
