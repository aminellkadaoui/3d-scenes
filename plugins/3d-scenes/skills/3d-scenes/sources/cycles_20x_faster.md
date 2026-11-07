# 20X Faster Rendering in Cycles (Blender Render Guide)
- url: local file `~/Movies/4K Video Downloader+/20X Faster Rendering in Cycles (Blender Render Guide).mp4` (YouTube URL not recorded)
- channel / duration / Blender version shown: Kaizen ("kaizen RENDERING" branding on the benchmark asset) / 19:30 / **Blender 4.5.3** (status bar [11:50]) on an **RTX 4090 + Ryzen 9 7900X + 64 GB RAM** [01:45]
- domain(s): rendering
- trust: **medium**. Practical artist, shows real render-time readouts in the Image Editor for the benchmark (1:20.00 → 13.54 s), a tile-size benchmark and an HDRI texture-limit benchmark. But: the title says "20X"; the only end-to-end number shown is **80 s → 13.5 s ≈ 5.9×**. Several changes are made at once without per-setting timings. Sponsored segment (Skillshare, [05:45–06:45]) and a paid render-preset file plug [12:30]. The benchmark scene is a simple product shot with 5 lights, so some advice (Light Tree off, caustics on) is specific to that scene.

## 1. Problem it solves
Cycles animation renders that take hours: default settings give 1 min 20 s per frame for the benchmark, i.e. ~10.5 h for 5 s at 30 fps [01:00–01:15]. The author's order of work: **optimise the scene first (no quality loss), then tune settings, then denoise** [00:30–00:45]. Settings tuning is "mainly relevant for animations"; for a single still, just raise samples and let it render [15:15–15:30].

## 2. Techniques

### T1 — GPU device check `[01:15–01:30]`
- What: Preferences › System › Cycles Render Devices (CUDA/OptiX for NVIDIA, HIP for AMD, oneAPI for Intel, Metal for Mac; flowchart on screen [01:30]); Render Properties › Device = GPU Compute.
- Already in `knowledge/rendering.md` §2. Nothing new.
- Status: Extracted

### T2 — Instance duplicates instead of copying them `[02:00–02:30]`
- What: two identical copies of the hero asset each load their own mesh + textures. Replace the copy with **Add (Shift+A) › Collection Instance** of the source collection (menu shown [02:30]). Claim: this "halves our poly and texture count". Scene had ~12.4 M verts before [02:00].
- Why: an instance shares mesh data and images in memory and in the BVH (instanced BVH), so memory and scene-sync time drop. Path-tracing time per sample changes little.
- Use when: the same object appears more than once (props, chairs, books, cables, lights).
- Don't use when: the copies need different modifiers, shape keys or materials (use linked-data duplicates Alt+D with per-object material slots set to Object instead).
- Blender 5.2: unchanged.
- Status: Extracted

### T3 — Simplify: cap subdivision and texture size `[02:30–03:45]`
- What: Render Properties › **Simplify** ✔ › Viewport and Render › **Max Subdivision 6 → 2–3** (scene went to ~1 M verts because the asset had a Subdivision modifier) [02:45]; **Texture Limit** (e.g. 1024) [02:45–03:30]. Frame at [02:45] shows the Simplify panel being enabled with Render Max Subdivision 0 and Texture Limit "No Limit".
- Benchmarks shown: alley scene 2 min → 38.97 s with Simplify [03:15]; default cube with a **16K HDRI: ~49 s → ~15 s** with Texture Limit 1024 [03:15–03:30] (frame shows "Time:00:48.80").
- Why: Simplify is global, so it also hits objects and textures out of frame that still cost memory, upload time and BVH build [03:00].
- Don't use when: the HDRI or a texture is seen sharply (in the background or in a mirror-like reflection): it loses detail [03:30–03:45]. Re-render and check at 100%.
- Values: starting points. Max Subdivision is a cap, not a level: it only matters for objects whose render subdivision level is above it.
- Blender 5.2: Simplify › Texture Limit still exists; 5.2 adds **Texture Resolution %** and the **Texture Cache** (Performance › Texture Cache, `.tx` files), the finer, native version of this idea (see `knowledge/rendering.md` §5).
- Status: Extracted

### T4 — Camera culling `[04:00–05:30]`
- What: Simplify › **Culling › Camera Culling** ✔ (margin 0.10 shown [04:20], 0.72 shown [05:30]); Distance Culling optional. It does nothing until objects opt in: select them, Object Properties › Visibility › **Use Camera Cull**, **Alt+click** to apply to all selected [04:15–04:30] (Visibility panel seen [04:30]). Works in Rendered view and final render, not Solid view [04:30]. Demonstrated on ~11,000 scattered objects [04:45].
- Why: objects outside the camera frustum still cost BVH, memory and sync time.
- Don't use when: off-screen objects must still appear in reflections, shadows or bounce light. Then raise the margin [05:15]. **In a closed interior almost everything off-screen contributes light, shadow or reflection, so culling is risky there** (my assessment).
- Status: Extracted

### T5 — Combined result of scene optimisation `[05:30]`
- 1:20 → **1:10** per frame after instancing + Simplify + culling (the benchmark scene is small; scattered/heavy scenes gain far more).
- Status: Extracted

### T6 — Resolution as a budget `[07:00–09:00]`
- What: pick resolution by purpose (flowchart, [08:30]); 1080p is "plenty" for most, he uses 1440p; render time scales with pixel count (4K ≈ 4× 1080p pixels) [07:45]. Benchmark kept at **1280×1440** for clarity [08:45].
- Already in `knowledge/rendering.md` §6. Nothing new.
- Status: Extracted

### T7 — Adaptive sampling: threshold 0.03, Max 1000, **Min 20** `[09:00–11:30]`
- What: Noise Threshold **0.03** as his default, up to 0.1 for some projects; kept low here because of translucency [09:45–10:00]. Range 0.001–1; on the default cube 0.001 ≈ 5 s vs 1.0 < 1 s [09:30]. Max Samples **1000** instead of 4096: "visually hardly a difference" between 4096/2000/1000 when denoising [10:15–10:45] (comparison of 1000/2000/4096 shown on Suzanne [~10:30]). **Min Samples 0 → 20** "to compensate for the higher noise threshold and the lower sample count", so every pixel gets some samples [11:00–11:30]. Frame [11:50]: Render › Noise Threshold 0.0300, Max 1000, Min 20, Time Limit 0, render Denoise unticked (denoising moved to the compositor).
- Why: adaptive sampling stops a pixel when its estimated error is under the threshold. With a high threshold, some pixels stop after very few samples and the error estimate itself is unreliable there; a minimum floor protects dark or late-converging areas.
- Use when: animation where render time matters and a denoiser follows.
- Don't use when: dark gradients, DOF bokeh or volumes in motion: 0.03–0.1 is where spatial denoisers start to boil (see conflicts §3).
- Status: Extracted

### T8 — Light Tree off in few-light scenes `[11:45–12:10]`
- What: Sampling › Lights › **Light Tree** off when the scene has few lights (benchmark has 5); keep it on for "dozens or hundreds" of lights (Christmas-tree example [12:00]). Frame [11:50] shows it ticked before the change; later frames show it unticked.
- Why: Light Tree adds per-sample overhead to choose a light by estimated contribution; with very few lights, uniform light selection is nearly as good and cheaper.
- Don't use when: many lights, emissive meshes, LED strips, small practicals. No timing shown for this change alone.
- Status: Extracted (claim untested; contradicts our default, see §3)

### T9 — Animated seed `[12:15–12:30]`
- What: Sampling › Advanced › Seed › clock icon (**Use Animated Seed**) on (frame [12:20], Pattern Automatic). Noise changes each frame "like a camera would produce" and denoises better over animation; also cited against denoising blotches [18:15–18:30].
- Already in `knowledge/rendering.md` §3.1. Nothing new.
- Status: Extracted

### T10 — Tune bounces in the viewport, one type at a time `[12:45–13:15]`
- What: camera view, Rendered shading, **viewport denoising on**. Set every Max Bounce type except Total to **1**. Raise each type separately until the viewport stops changing visibly. Then set **Total = Diffuse + Glossy + Transmission + Volume** [12:45–13:15]. Result for the benchmark (frame [13:27]): **Total 8, Diffuse 1, Glossy 3, Transmission 4, Volume 0, Transparent 8**.
- Why: each bounce type only matters when there is energy left on that kind of path. Glass needs transmission bounces (each surface in and out), mirrors need glossy, bright interiors need diffuse. Past the visible point, extra bounces cost time with no visual change.
- Use when: every final, per scene.
- Don't use when: judging only from a denoised, low-sample viewport on a tiny region. Dark corners and the colour of bounce light in interiors can change subtly. Check a final-quality still before committing.
- Status: Extracted

### T11 — Clamping left alone; caustics on for transparent/glossy subjects `[13:15–13:30]`
- What: he doesn't touch Clamping ("I don't like the effects") — defaults Direct 0, Indirect 10 (frame [13:15]). Caustics: off "in a lot of projects", but **on here because of transparent and glossy materials** [13:15–13:30]. (Frame [13:27] shows both caustic boxes being toggled off; frame [14:30] shows Reflective and Refractive ticked again, matching the transcript.)
- Status: Extracted

### T12 — Performance panel: GPU compositor, Tile Size 2048, Persistent Data `[13:30–14:45]`
- What: Compositor Device **GPU**, Denoise Nodes device GPU, Preview Quality Balanced / Final Quality High (frame [14:30]). **Tile size**: benchmark card **128 → 5 min 40 s; 2048 → 1 min 10 s; 4096 → 1 min 10 s** [14:05] — keep the default 2048. **Persistent Data** ✔ [14:15–14:45]: keeps BVH and importance maps in RAM between frames; only helps from the second frame on. All settings together → **13.54 s/frame, memory 1070 MB (peak 1183 MB)** vs 1:20.00 and 3609 MB (peak 3722 MB) at the start (frames [14:45] and [01:15]).
- Status: Extracted

### T13 — Denoise in the compositor with Denoising Data `[16:00–18:45]`
- What: OIDN now preferred over OptiX, "extremely consistent", runs on GPU [16:45]. View Layer › Passes › Data › **Denoising Data** ✔; Compositor: Render Layers (Image, Denoising Normal, Denoising Albedo) → **Denoise** node (Prefilter **Accurate**, Quality **High**/Follow Scene, **HDR** ✔) → Composite/Viewer (frame [17:30]) [17:00–17:30]. Mix the denoised result back with the noisy image to control strength; denoise passes separately (mist, light passes) [17:30–17:45]. Cost: "hardly any" here — the denoised render was slightly faster, just under 13 s [18:00]. Claim: 20,000 samples without denoising still looks worse than 1000 + denoising [16:15–16:30].
- Artifacts: blotches, worst in animation; fought with animated seed + albedo/normal guidance; still appear if samples too low or threshold too high [18:15–18:45].
- Blender 5.2: the compositor became node-group based in 5.0 (no "Use Nodes" checkbox; output via the group output). Check node and socket names in 5.2.
- Status: Extracted

## 3. Claims I doubt or must test
- **"20X faster"**: the only full measurement shown is 80 s → 13.5 s (≈5.9×). No per-step timings except tiles and the HDRI test.
- **Light Tree off for speed**: contradicts our default (ON). Plausible only for very few lights and no emissive meshes; no isolated timing given. Our VSL room (~28 lights + emissive monitor + LED strips) is the opposite case.
- **Threshold up to 0.1 for animation**: too high for dark scenes with DOF/volumes (denoiser boiling). His own scene is a bright, simple product shot.
- **Caustics on for glass/glossy**: the right call only when caustic light is visible (light through glass onto a surface). Glossy reflections of lights are not caustics; caustics are paths that end on diffuse surfaces after glossy/refraction bounces. They are the biggest firefly source.
- **HDRI 16K → 1024 saves 34 s**: much of that is likely image load/upload and importance-map build, which is per-frame cost only without Persistent Data. Expect much smaller gains with 4K HDRIs and Persistent Data on.
- **Tile 128 is 5× slower**: plausible on a 4090 at 1440p (GPU underfilled); no reason to go below the default anyway.
- **"1000 + denoise beats 20k samples"**: depends on what "better" means (smoothness vs detail). Not measured.
- **Camera culling "at no difference to the final product"** [05:15]: false in general for interiors (shadows, bounce, reflections from off-screen objects).

## 4. Anti-AI-slop lessons
- Optimise the scene before reducing quality settings: instancing, Simplify and culling cost no image quality when used carefully, while threshold/samples do.
- Tune bounces by *seeing* when a change stops being visible, not by copying a preset (presets are sold, scenes differ) [15:45].
- Denoising is "not a fix-all" [19:00]: low samples + high threshold leave the denoiser guessing, which shows up as blotches and boiling in motion. Judge finals in playback.

## 5. Candidate isolated test
Bedroom VSL scene, 3 representative frames (face close-up f/1.4 + fog, wide shot, glossy desk): (a) current final settings; (b) Persistent Data on, render 5 consecutive frames, compare per-frame time after frame 1 and check the monitor video texture advances; (c) Diffuse/Glossy 8 → 4, Transmission 12 → 8; (d) threshold 0.01 → 0.02 on the wide shot only. Measure s/frame, a 200% crop of shadows/skin/fog, and temporal flicker (mean abs diff in a static dark region across 24 frames). Promote only what passes.

## 6. Frames viewed
Contact sheets `frames/sheet_01–05.jpg` (frames `f_000–f_077`, every 15 s, timestamp-accurate seeks). Full-resolution frames: `x_0245` (Simplify), `x_0420` (Camera Culling 0.10), `x_0530` (Culling 0.72), `x_1150` (Sampling 0.03/1000/20, Light Tree, status bar 4.5.3), `x_1220` (Seed animated), `x_1315` (bounces being edited), `x_1327_crop` (final bounces 8/1/3/4/0/8, caustics), `x_1405` (tile size benchmark), `x_1430` (Performance: GPU compositor, Persistent Data), `x_1445` (13.54 s, 1070 MB), `x_1730` (compositor Denoise node). Others extracted but not useful (talking head / B-roll): `x_0330`, `x_0845`, `x_1050`, `x_1120`, `x_1250`, `x_1415`, `x_1700`, `x_1705`, `x_0950`, `x_1435`, `x_1635`, `x_1850`, `x_1205`, `x_1210`, `x_1515` — of these I opened only `x_0950`, `x_1435`, `x_1705`; the rest were not viewed individually (their moments are covered by the contact sheets).
