---
id: materials-smart-masks-edge-wear-dirt
domain: materials
status: Extracted
sources: [RfPro3hlOMg@09:30, RfPro3hlOMg@10:30, RfPro3hlOMg@11:00, RfPro3hlOMg@12:45, 8HfKtaDx6tM@11:30, 8HfKtaDx6tM@11:00]
blender: "5.2"
---
# Geometry-aware masks: edge wear on convex, dirt in occluded/concave areas
**Principle:** Damage and dirt follow physics: protruding edges get hit and polished/chipped; crevices and occluded areas collect dust and grime (no wind/rain/cleaning); lower parts collect splash dirt; upward faces collect dust. Masks derived from geometry place imperfections where they belong on any mesh — random noise masks place them everywhere = fake.

**Steps / settings (starting points):**
- Edge (convex) mask, options:
  a. **Bevel** shader node (Radius ~ 1–3 mm on human-scale props) · **Geometry ▸ Normal** → Vector Math **Dot Product** → Map Range (invert: 1 at edges) [8HfKtaDx6tM@11:30]. Cycles only.
  b. **Geometry ▸ Pointiness** → Color Ramp (stops ~0.48–0.55). Cycles only, depends on mesh density [RfPro3hlOMg@10:30].
  c. Geometry Nodes: **Store Named Attribute** (Float, Edge domain→ Point via interpolation, name "edge_angle") ← **Edge Angle ▸ Signed Angle** (frames: author stacks Bevel 30° + Catmull-Clark subdiv before GN so the mask isn't blocky [RfPro3hlOMg@11:15]; AO dirt: noise→AO Distance, Samples 32, Map Range From 0.82–0.94 unclamped [RfPro3hlOMg@13:45]); optional **Blur Attribute**; shader **Attribute** node "edge_angle". Works in EEVEE [RfPro3hlOMg@11:00–11:45].
  d. Baked curvature/AO map (best for game-style hero assets and for speed).
- Cavity/occlusion mask: **Ambient Occlusion** node (Only Local on, Distance 0.05–0.3 m for props) → Color Ramp; noise → Distance input for irregularity [RfPro3hlOMg@12:45–13:30]. Expensive in Cycles.
- Directional masks: Geometry ▸ Normal → Separate XYZ → Z → ramp (top dust); Object-space Z position gradient (dirt rising from ground, ~0–0.3 m).
- ALWAYS multiply the geometric mask by a grunge/noise texture and remap so it breaks up — pure geometric masks look like outlines.
- Use the mask as Factor in **Mix Shader** (different materials: paint vs bare metal; varnish vs raw wood; base vs dirt) — Mix Color only when properties are identical except colour.

**Use when:** used/aged objects, environments, industrial props, storytelling (an old office desk, a worn tool).
**Avoid when:** brand-new products in marketing hero shots (at most dust in crevices of the *environment*, not the product); stylised clean looks; low-poly meshes where edge angle is blocky (densify/bevel first).
**Failure signs:** uniform "outlined" edges (no breakup); wear on concave edges (inverted mask); dirt floating mid-surface with no geometric reason; same strength on every object in the scene; EEVEE vs Cycles mismatch (Pointiness/Bevel missing in EEVEE).
**Cost:** Bevel & AO nodes add noticeable Cycles cost (extra rays; ~10–30% on heavy scenes, untested); attribute method is free at render.
**Conflicts with other sources:** 8HfKtaDx6tM uses edge mask for moss on a statue — physically moss prefers cavities & up-facing damp areas; use AO × up-normal mask instead.
**Test to validate:** bevelled metal box with paint over bare metal; A noise mask, B edge mask × grunge, C + AO dirt; compare believability and Cycles render time; repeat in EEVEE with attribute method.
**Log:** 2026-11-05 — Extracted from RfPro3hlOMg, 8HfKtaDx6tM.
