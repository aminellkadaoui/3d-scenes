# 20+ Blender Tricks That Made Me Pro
- url: https://youtu.be/LPCdpTcNXyM
- channel / duration / Blender version shown: Extra 3d / 5:57 / Blender 4.0–4.1 era (uploaded 2024-04-08)
- domain(s): materials | environment | rendering | compositing | camera
- evidence used: transcript (sparse auto captions) + contact sheets 01–02 + 6 extracted frames from the 480p mp4 (see §6). Evidence: partial→improved.
- trust: medium-low. Rapid-fire tips with almost no explanation; heavy promotion of the author's "starter pack".

## 1. Problem it solves
Workflow time savers and quick realism tricks.

## 2. Techniques (materials-relevant ones in detail, others listed)

### T1 — Add detail to a normal map via a Bump node in between  `[00:00–00:15]`
- Image(Normal) → Normal Map node → **Bump** node's *Normal* input; extra detail texture → Bump *Height*; Bump → Principled Normal. This is the correct way to combine a normal map with an additional height detail (better than Overlay-mixing normals).
- Status: Extracted

### T2 — Extrude texture stretching → "Correct Face Attributes"  `[00:15–00:30]`
- In Extrude/Move operator redo panel (or Tool settings ▸ Options) enable **Correct Face Attributes** to keep UVs from stretching while editing geometry.
- Status: Extracted

### T3 — Droplets on glass  `[00:30–00:45]`
- Droplet image/video texture → Bump Height → Glass Normal; also into roughness.
- Status: Extracted

### T4 — Glass with Light Path trick  `[01:15–01:30]`
- Mix Shader(Glass, Transparent), Factor = **Light Path ▸ Is Shadow Ray** (confirmed from frames [01:26]: Glass Roughness 0.01, IOR 1.45, Multiscatter GGX) → light passes through for shadows while camera sees glass. Faster, less noise in interiors behind windows.
- Caveat: removes caustics and coloured shadows — physically wrong but usually invisible; don't use for hero glass product shots where caustics are the point. In Blender 4.x+, Principled/Glass have no "shadow" option; this trick still works in Cycles.
- Status: Extracted

### T5 — Imperfection textures into glass roughness  `[02:45–03:00]`
- Same principle as 8HfKtaDx6tM T10.
- Status: Extracted

### T6 — Rock with displacement modifier + subdivision, scale UVs to look large  `[04:45]`
- Scale of texture features signals object size — scaling UV down makes a rock read as a cliff.
- Status: Extracted

### Others (non-material, listed for other domains)
Fake god rays: cylinder + emission in volume + gradient [00:45]; lens flare via Glare node [01:30]; free smoke/fire [01:45]; DoF bokeh blades 8, ratio 2 (anamorphic) [02:00]; BlenderKit add-on [02:15]; tree sway via Simple Deform + noise modifier [02:30]; ambientCG [03:00]; built-in fur geometry nodes [03:15]; Images as Planes (now built-in "Import Images as Planes" — in 4.2+ under File ▸ Import / Add ▸ Image ▸ Mesh Plane) [03:30]; snow add-on [04:00]; handheld camera via noise modifier on rotation f-curves [04:15]; Lens Distortion 0.01 & dispersion 0.02 [04:30]; blackbody/temperature for fire [05:15].

## 3. Claims I doubt or must test
- Glass + transparent light-path mix: OK in interiors, wrong for hero glass.
- Lens distortion dispersion values are scene-independent? Mostly yes (screen-space), but should stay subtle.

## 4. Anti-AI-slop lessons
- Glass and metal need imperfection maps in roughness; texture feature scale tells the viewer object size.

## 5. Candidate isolated test
Window glass in interior: A real glass; B glass/transparent light-path mix. Measure noise at same samples, render time, and whether difference is visible.

## 6. Visual verification (frames viewed)
Frames viewed: contact sheets 01–02, plus extracted frames below. **Blender 4.0.2** (status bar at [01:05], [01:20]); EEVEE Legacy panels (Bloom checkbox) at [04:48].
- [00:05] Intro graphic (icons over a blurred render) — nothing to verify.
- Sheet 01 [00:00]–[00:15]: the first tip is demonstrated on a **sand-dune plane** (bump detail over a normal map), not a generic material — topology of T1 not readable at 480p.
- [01:05] Fake god-ray: cone/cylinder under a "Square spot light" rig (Cube…, Spot, Spot.001), node search adding a **Gradient Texture** to the cylinder material; World Strength 0 (black) — confirms the god-ray tip set-up.
- [01:20]/[01:26] **Confirms T4 exactly:** Suzanne "Default Glass": **Light Path ▸ Is Shadow Ray → Mix Shader Fac**, Shader 1 = **Glass BSDF (Multiscatter GGX, Roughness 0.010, IOR 1.450)**, Shader 2 = **Transparent BSDF**. Subdivision 1/2. The material comes from the author's paid "Premium Cinematic Starter Pack" asset library.
- [02:05] **Confirms DoF tip:** Depth of Field on, Distance 1.7 m, **F-Stop 1.9, Blades 8, Ratio 2.000** (anamorphic oval bokeh); a **Camera Shakify** panel is visible under the camera properties (so the handheld tip likely uses the Shakify add-on rather than only a Noise modifier — unverified further).
- [04:48] Compositor with a **Lens Distortion** node selected; its values are not visible in this frame — the 0.01/0.02 values remain transcript-only.
- Final quality judgement: almost all demos are Suzanne / grey planes / single props over an HDRI — tip-level, not finished shots. Nothing to judge as "professional result"; trust stays medium-low, but the glass and DoF values are now confirmed.
