# Render faster in Cycles (render-time optimisation, "up to 4,000%")
- url: https://youtu.be/gmGMsKJ6xd8
- channel / duration / Blender version shown: Extra 3d / ~12:10 / **Blender 5.1.2 on Windows** (status bar, corrected from frames [05:13]); AMD Radeon 740M iGPU via HIP
- domain(s): rendering
- evidence used: transcript (auto captions) + contact sheets 01–02 + 8 extracted frames from the 480p mp4 (see §6).
- trust: **medium-low**. The basic settings are sound. But the headline "4,000%" mixes several changes at once (samples, threshold, denoiser, a paid add-on and an iGPU benchmark) with no isolated before/after per setting. It promotes an affiliate add-on (RenderMind) [gmGMsKJ6xd8@04:00] and a "frame interpolation" app. Some statements are wrong for macOS (see §3).

## 1. Problem it solves
Cycles renders taking hours (1 h 25 min → 3 min 52 s claimed on an iGPU [gmGMsKJ6xd8@05:15]). Default sampling (4096 max samples, threshold 0.01) is overkill for most motion-graphics and VSL shots. The goal is "crisp, artifact-free, fast".

## 2. Techniques

### T1 — Use the GPU device `[00:30]–[01:30]`
- What: Preferences › System › Cycles Render Devices: OptiX (NVIDIA, enable RT), HIP (AMD, enable HIP RT), oneAPI (Intel), Metal (Mac). Then Render Properties › Device = GPU Compute. The video also says to set the graphics backend to Vulkan [01:30].
- Why: path tracing is massively parallel, so the GPU is usually 5–20× faster than the CPU.
- Use when: always on Apple Silicon (Metal). **Don't** enable the CPU together with the GPU on a Mac laptop. It adds heat and gives little gain.
- Blender 5.2 notes: on **macOS the only backend is Metal**. Vulkan does not apply on Mac, so ignore that step. On Apple Silicon, MetalRT (hardware ray tracing on M3 and newer) is a Preferences option. HIP RT is on by default for AMD in 5.1.
- Status: Extracted

### T2 — Sampling range + noise threshold `[01:30]–[02:30]`
- What: Max samples 128 for normal renders → 256 if noisy → max 512. Noise Threshold 0.05–0.075 [02:30].
- Why: adaptive sampling stops pixels once their estimated noise falls under the threshold. The denoiser removes the rest. If noise survives 512 samples, the problem is the scene (volumes, caustics, tiny bright lights), not the sample count [02:15].
- Use when: denoised stills and motion-graphics shots. **Don't** use 0.075 for animation with dark gradients, volumes or DOF. Denoised low-sample frames flicker and "boil", so use 0.01–0.03 there.
- Values: starting points for 1080p product or abstract shots.
- Status: Extracted

### T3 — Denoiser choice `[02:30]–[03:00]`
- What: OpenImageDenoise (OIDN) for final ("generally does a better job"), with **Use GPU** on. OptiX for the viewport only (NVIDIA).
- Why: OIDN is the higher-quality, cross-vendor denoiser. OptiX is faster and suits interactive use.
- Blender 5.2 notes: Denoiser options are Automatic / OpenImageDenoise / OptiX. Passes: None / Albedo / Albedo + Normal. OIDN Prefilter: None / Fast / Accurate. Quality: High / Balanced / Fast. OIDN on the GPU works on Apple Silicon.
- Status: Extracted

### T4 — Persistent Data, BVH options, GPU compositor `[03:00]–[03:30]`
- What: Performance › Final Render › **Persistent Data** on. Spatial Splits and Curves options. Compositor device = GPU.
- Why: Persistent Data keeps the BVH, shaders and textures in memory between animation frames, so static scenes skip resync.
- Don't use Persistent Data when RAM or VRAM is tight (unified memory on Mac is shared with the OS), or when geometry changes every frame (no gain).
- Status: Extracted

### T5 — Disable unused light-path features, biased volumes `[03:15]–[04:00]`
- What: turn off Caustics (Reflective/Refractive) if the shot doesn't need them. Render › Volumes › **Biased** to return to the old ray marching [03:45].
- Why: caustic paths are the main source of fireflies. In 5.0 the unbiased null-scattering volume method became the default, and its noise and performance are scene-dependent.
- Blender 5.2 notes: confirmed in the 5.0 Cycles release notes ("Biased" restores step size and max steps).
- Status: Extracted

### T6 — Memory hygiene `[05:45]–[07:45]`
- What: exclude off-camera collections (checkbox in View Layer, not just the eye icon). Mute (M) unused texture nodes. File › Clean Up › Purge Unused Data. Use instances (Alt+D) instead of duplicates (Shift+D). Use camera culling. Decimate distant objects (factor ~0.1), with Ctrl+L › Copy Modifiers. Downsize far textures.
- Blender 5.2 notes: Cycles 5.2 adds **Texture Cache** (Performance › Texture Cache + Auto Generate, writes `.tx` files) and Simplify › Texture Resolution %. These are the native versions of the "texture manager" the add-on sells.
- Status: Extracted

### T7 — OpenEXR half + DWAA for animation output; finish in the VSE `[07:45]–[09:15]`
- What: Output › File Format **OpenEXR**, Color Depth **Float (Half)**, Codec **DWAA** (lossy). Use RGBA if the background is transparent. Afterwards, load the sequence in a Video Editing file with the same colour management, and add glare via a Compositor modifier strip [10:15].
- Why: EXR stores scene-linear values above 1.0, so glare and bloom still react correctly to real highlights after the render. DWAA keeps files small.
- Don't: use DWAA for data passes (Cryptomatte, depth, position, normals). Lossy compression corrupts ID and depth values. Use ZIP/PIZ and Float (Full) for those.
- Blender 5.2 notes: the **Compositor** sequencer strip modifier was added in 5.0.
- Status: Extracted

### T8 — Render Region "stitching" for locked-off shots `[09:30]–[10:45]`
- What: render one full frame as the background plate, then animate only a Render Region (Ctrl+B in the camera view) with RGBA and "Crop to Render Region" unchecked. Stack the two in the VSE.
- Use when: the **camera is locked** and the moving part is small. Don't use when there is a moving camera, moving light, GI or shadow changes outside the region, or animated noise/grain. These cause visible seams.
- Status: Extracted

### T9 — Render every 2nd frame + optical-flow interpolation `[11:00]–[11:45]`
- What: Output › **Frame Step** 2, encode at half fps, then interpolate back with an external tool (the video links one; likely Flowframes/RIFE-type).
- Use when: there is slow, smooth motion with no occlusion edges. Don't use with fast motion, thin objects crossing, motion blur, particles or text. Interpolation warps edges and shimmers.
- Status: Extracted (high risk; test before use)

## 3. Claims I doubt or must test
- "Up to 4,000%" — the speed-up comes from cutting samples (4096 → 128), not from optimisation. There is no per-step benchmark.
- "Never go above 512 samples": fine for denoised stills. Denoised animation, DOF, volumes and caustics often need more, or a lower threshold.
- "Switch to Vulkan" — not applicable on macOS.
- "Spatial splits + curves with CUDA": these BVH options mainly concern CPU/Embree builds. The effect on GPU is unclear; benchmark before believing it.
- Frame interpolation "looks almost identical" [11:45] — unverified, and fails with occlusion.
- AI add-on that "trains" render settings: unverifiable and sponsored.

## 4. Anti-AI-slop lessons
- Speed settings must not create *temporal* artifacts. A clean still can turn into boiling noise and denoiser smear in motion. Always check a 2–3 second playback, not one frame.
- Find the cause of the noise (volumes, caustics, tiny lights) instead of raising samples blindly.
- Keep the render in EXR so glow and grade respond to real highlight energy. Glow made from clipped 8-bit PNGs looks flat and fake.

## 5. Candidate isolated test
Scene: a product on a table, one area light, a glossy material, light volume haze, a 48-frame slow push-in. Compare A: defaults (4096 / 0.01 / OIDN) against B: 128 / 0.05 / OIDN Accurate + Persistent Data, and against C: B + Biased volumes. Measure: time per frame, PSNR/SSIM of B and C against A on frame 24, and flicker = mean absolute difference between consecutive frames in flat dark areas.

## 6. Visual verification (frames viewed)
Frames viewed: contact sheets 01–02, plus extracted frames below. **Blender 5.1.2 on Windows** (status bar at [05:13], [08:20]; "Microsoft Store installation" in Preferences) — (corrected from frames) more precise than the "5.0+" inference.
- [01:10] Preferences ▸ System: Cycles devices **HIP, AMD Radeon 740M Graphics** (an integrated GPU) checked, Ryzen 7 7445HS CPU unchecked, **HIP RT on**; Display Graphics Backend **OpenGL** with "restart required" (the Vulkan switch is being made). Confirms the benchmark machine is a low-end iGPU laptop.
- [02:40] **Confirms T2/T3:** Cycles GPU Compute, **Noise Threshold 0.0500, Max Samples 256**, Min 0, Denoise **OpenImageDenoise, Passes Albedo and Normal, Prefilter Accurate, Quality High**, Use GPU (unchecked at this moment, checked at [05:13]); Max Bounces Total 12.
- [03:20] **Confirms T4:** Performance ▸ Threads Auto-Detect (12), Memory **Tile Size 2048**, Acceleration Structure **Use Spatial Splits ✔, Use Curves BVH ✔**, Final Render **Persistent Data ✔**, Viewport Pixel Size Automatic.
- [03:50] **Confirms T5 and adds values:** Bounces Volume 0, Transparent 8; Clamping **Direct 0.00, Indirect 10.00**; Filter Glossy 1.00; **Caustics Reflective/Refractive off**; Fast GI off; Volumes **Biased ✔, Step Rate Render 1.00 / Viewport 1.00, Max Steps 1024**.
- [05:13] Full light-path set: Total 12, Diffuse 4, Glossy 4, Transmission 12, Volume 0, Transparent 8; the paid **RenderMind Pro v6.0** add-on panel is open over the viewport (sponsor).
- [05:22] "RENDER TEST" bar chart (AMD Radeon 740M vs Default) — no numeric per-setting breakdown visible; supports my doubt that "4,000%" is not decomposed.
- [08:20] **Confirms T7:** Output **OpenEXR, RGB, Color Depth Float (Half), Codec DWAA (lossy), Quality 90%**, frames 1–120 at 24 fps, Render Region on / Crop to Render Region off (T8 set-up). Scene = candles/jars still life.
- Final quality judgement: the test scenes (crystal cluster, candle still life at [08:20], sheet 02 [06:15] volumetric shot) are decent moody demos; the rendering advice is settings-level and the visible values are sane for denoised stills. Trust stays medium-low because of the iGPU-only, non-isolated benchmark and the sponsor add-on.
