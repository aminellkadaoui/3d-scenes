# Rendering — Cycles & EEVEE in Blender 5.x: engines, sampling, denoising, light paths, profiles, output, QA

> Status: Knowledge (research + expert synthesis + video extraction). Target: **Blender 5.2 LTS on macOS / Apple Silicon (Metal)**. Option names were checked against the 5.0–5.2 release notes and the 5.2 manual (Sampling, Light Paths, Video Formats pages). Defaults marked "(typ.)" come from experience; check them in the UI.
> Related: `color-management.md`, `compositing.md`, `ai-slop-diagnosis.md`, techniques `rendering-*`.
> Video sources: gmGMsKJ6xd8 (Cycles speed), vtdczoXVyvQ (passes/EXR), uO0GuFuGRQc (quick cinematic), 1MyARLB8KzY (volumes/dust), lE308jCAT2o (comp pre-flight), eevee_full_course (EEVEE Next interiors, probes, raytracing; local video, Blender 4.4), cycles_20x_faster (Kaizen, scene optimisation + settings + compositor denoise; Blender 4.5.3, RTX 4090).

---

## 0. The principles

1. **The render engine doesn't make an image look professional. The lighting, materials and camera do.** Render settings can only *ruin* a good image (noise, flicker, clipping, banding), or *afford* it (time). So the job of this file is: get artifact-free frames within the time budget, and keep the data needed for post.
2. **Judge in motion.** A denoised still can look perfect and still boil, crawl or flicker at 24/30 fps. Every final setting must pass a 2–3 second playback test.
3. **Find the cause of noise, don't overpower it.** If noise survives ~512 samples, the cause is in the scene (volumes, caustics, tiny hot lights, glossy reflections of lights, light through glass), not the sample count [gmGMsKJ6xd8@02:00].
4. **Render data, not pixels.** Keep scene-linear EXR when anything happens after the render (glow, grade, comp). Bake 8-bit only at the end.
5. **Three render profiles: blockout / look-dev / final.** Never iterate on composition with final settings, and never judge materials in blockout settings.

---

## 1. Cycles vs EEVEE in Blender 5.x — decision guide

EEVEE "Next" (the rewrite) replaced legacy EEVEE in 4.2. In 5.x the engine is just called **EEVEE**. It has screen-space + probe ray tracing, virtual shadow maps, volumetrics and displacement. Cycles is the path tracer.

| Question | Choose **Cycles** | Choose **EEVEE** |
|---|---|---|
| Is realism / product credibility the point (VSL "proof" shots, product hero)? | ✔ correct GI, soft shadows, caustic-free glass that still reads right, accurate reflections | only with careful probes and light setup |
| Glass, liquids, gems, refraction-heavy products | ✔ | ✗ (refraction is screen-space / probe-limited) |
| Interior GI, bounce colour, light through windows | ✔ | OK with thick walls + shadow Steps 12–16 + a baked Volume probe; leaks without them [eevee_full_course@03:00][eevee_full_course@42:40] |
| Glossy floors/desks, chrome, mirrors with a moving camera | ✔ | only with Plane/Sphere probes; screen-space alone ghosts and pops while panning [eevee_full_course@10:40] |
| HDRI/world outside a closed room | ✔ walls block it physically | world light floods the room unless a Volume probe is baked [eevee_full_course@36:00] |
| Lights/objects animating through the room (bounce must follow) | ✔ | weaker: the Volume probe bake is static, only screen-space Fast GI follows |
| Abstract motion graphics, stylised/toon, UI-in-3D, typography, emissive shapes on dark | overkill | ✔ seconds per frame |
| Many frames, tight deadline (≥ 1,000 frames overnight on a laptop) | only with aggressive settings | ✔ |
| Volumetric god rays | ✔ physically right (noisy, slow) | ✔ fast, softer and less accurate (World/Volume resolution) |
| Need Indirect Only, full light passes for pass rebuild, Shadow Catcher, light linking for comp | ✔ | partial |
| Animated noise-free deliverable without denoiser flicker | slow (needs a low threshold) | ✔ inherently noise-free (temporal accumulation) |

**Rule of thumb for VSL work:** product, realism and "proof" → Cycles. Graphic explainer scenes, icons, abstract loops and kinetic type → EEVEE. A mixed approach also works: block out and animate in EEVEE, then switch to Cycles for the final once lights are tuned. Expect to retune light powers and volumes, because they don't match 1:1 between engines.

**EEVEE 5.x key settings (Render Properties):** Sampling › Render samples (64 typ.; raise to 128–256 for clean DOF/motion blur/soft shadows), **Raytracing** ✔ (Method: Light Probe or Screen-Trace; Resolution 1:1 or 1:2 for finals; Denoise ✔), Fast GI Approximation for bounce, Shadows (Rays/Steps, Resolution Limit), Volumes (Resolution 1:4 or 1:2 for finals vs 1:8 typ., Steps 64–128), Clamping (Surface Direct/Indirect), Motion Blur, Film (Filter Size 1.5 px, Transparent, Overscan to avoid screen-space edge artifacts). Light probes: Volume probe (irradiance) baked for interiors, Sphere probe for reflective surfaces, Plane probe for flat mirrors/floors.

**EEVEE → Cycles-match recipe (two sources combined, Extracted):** Shadows Rays 2–4 / Steps 12–16 / Volume Shadows ✔ [eevee_full_course@07:40][eevee_next_like_cycles@00:05]; Raytracing Screen-Trace 1:2, Max Roughness 0.5, Precision 1.0 [eevee_next_like_cycles@00:15]; Fast GI Rays 8 / Steps 12–16 / Precision 1.0 [eevee_next_like_cycles@00:25][eevee_full_course@48:40]; Volumes max resolution + Custom Range tight around the fog [eevee_next_like_cycles@00:32]; Overscan 20–40 % for screen-space GI at the frame edges [eevee_next_like_cycles@00:45]; glass = Transparent Shadows + Raytraced Transmission, Thickness Sphere/Slab [eevee_next_like_cycles@01:45]; world either camera-ray-only (lights replace HDRI) [eevee_next_like_cycles@02:00] or a baked Volume probe that blocks world light inside [eevee_full_course@36:00]; EEVEE renders slightly darker → match light strength/exposure against a Cycles frame [eevee_next_like_cycles@02:40]. Conflict: Plane probes recommended for floors [eevee_full_course@15:20] vs "weird, not recommended" [eevee_next_like_cycles@03:35] → test per scene. Speed-first order: lower resolutions (raytrace, Fast GI, volumes) before rays/steps [eevee_next_like_cycles@01:00].


### 1.1 EEVEE interior recipe (Extracted, eevee_full_course; shown in Blender 4.4 — re-check names in 5.2)
Why EEVEE interiors look "gamey": raytracing is **off by default**, reflections/bounce are **screen-space** (only what's in frame), shadows are stepped shadow maps, and world light ignores walls. Fix in this order:
1. **Geometry:** close and thicken walls (Solidify) [eevee_full_course@03:00].
2. **Shadows:** Steps 6 → **12–16**, Rays **2**, Render Samples 64+ (more for DOF/motion blur) [eevee_full_course@07:40][eevee_full_course@09:20]. Card `rendering-eevee-shadow-bleed`.
3. **Raytracing ✔**, Screen-Trace, Resolution 1:2 (1:1 for hero glossy), Denoising ✔, Fast GI ✔ with Threshold 0.5, **Steps 16**, **Distance ~1–2 m** once a Volume probe exists; try **Temporal Accumulation off** for sharper textures, judged in motion [eevee_full_course@26:20][eevee_full_course@48:40]. Card `rendering-eevee-raytracing-fastgi`.
4. **Probes:** Plane probe exactly on glossy floors/mirrors; Sphere probe around chrome/glass with Clipping Start beyond the object; Volume probe filling the room (cubic cells, **Surfel Resolution 20 → ~100**, Surface Offset up against banding, World contribution off), baked with fog and window glass hidden [eevee_full_course@17:20][eevee_full_course@42:40][eevee_full_course@55:40][eevee_full_course@65:20]. Cards `rendering-eevee-reflection-probes`, `rendering-eevee-volume-probe-bake`.
5. **World sun:** World Sun Threshold 0 + a real Sun lamp (author's preference) or Threshold extraction when the HDRI sun must match the background [eevee_full_course@51:00].
6. **Glass:** archviz glass (Transparent + Glossy by Layer Weight Facing); Blended works with sphere probes only, Dithered needed for plane probes [eevee_full_course@60:20][eevee_full_course@61:00]. Card `materials-eevee-archviz-glass`.
7. **Performance:** drop texture maps the camera can't read (author: 11 s → 4 s/frame, transcript), delete unneeded plane probes, Spheres Resolution in Scene properties; fog ≈ +0.5 s. Seen: simple room 0.93 s/frame, furnished room 4.27 s/frame with 15.8 GB memory [eevee_full_course@43:40][eevee_full_course@71:20]. Lowering raytracing/Fast GI resolution below 1:2 saves little and flickers (transcript).

**Conflicts recorded:** (a) §10 used to say "avoid Fast GI in tight interiors"; this source keeps Fast GI on but limits its Distance to ~1–2 m and lets the Volume probe carry far bounce. Resolution: Fast GI on + short Distance + baked probe; turn it off only if it causes visible leaks after the probe is baked. (b) The decision table credits EEVEE's temporal accumulation for noise-free animation; the author turns Temporal Accumulation off for sharpness. Resolution: off for stills/slow moves if no flicker appears in a playback test, otherwise keep it on. (c) Shadow Steps floor 6 (§7) → 12–16 for soft-sun interiors.

---

## 2. Cycles device setup on macOS (Apple Silicon)

- Preferences › System › Cycles Render Devices › **Metal**, tick the GPU. **MetalRT** (hardware ray tracing) is useful on M3/M4 and newer. On older chips it may be slower, so benchmark both.
- Render Properties › Device: **GPU Compute**.
- Don't add the CPU to a Metal GPU render on laptops. It's little gain plus thermal throttling, and the GPU slows down.
- The display backend on macOS is **Metal**. The "switch to Vulkan" advice [gmGMsKJ6xd8@01:30] applies to Windows/Linux only (the video's "4,000%" benchmark ran on an AMD Radeon 740M iGPU, Windows, Blender 5.1.2 [gmGMsKJ6xd8@01:10]).
- Unified memory: the GPU shares RAM with macOS. With 16 GB machines, watch Activity Monitor during big renders. Use Persistent Data only when memory allows. In 5.2 use the **Texture Cache** (Performance › Texture Cache + Auto Generate → `.tx` files) for texture-heavy scenes.
- OIDN denoising runs on the GPU on Apple Silicon (Denoise › Use GPU).
- Thermals: long animation renders on a MacBook throttle. Render image sequences so you can stop and resume, and plug in power.

---

## 3. Sampling (Render Properties › Sampling)

Option names (5.2): Viewport / Render › **Noise Threshold** (checkbox + value), **Max Samples**, **Min Samples**, **Time Limit**. Denoise › **Denoiser** (Automatic / OpenImageDenoise / OptiX), **Passes** (None / Albedo / Albedo + Normal), **Prefilter** (None / Fast / Accurate; OIDN), **Quality** (High / Balanced / Fast; OIDN), **Use GPU**. Path Guiding (CPU only). Lights › **Light Tree**, **Light Threshold**. Advanced › Pattern (Automatic / Classic / Blue-Noise), Seed (+ animated clock), Scrambling Distance, Min Light Bounces, Layer Samples.

### 3.1 How adaptive sampling works
Cycles estimates per-pixel noise. Once a pixel's error is under the **Noise Threshold**, it stops sampling. Max Samples is the cap for difficult pixels. **Min Samples** (0 = automatic, based on the threshold) prevents early stopping in areas that look clean early but aren't (dark regions, small lights found late).

| Threshold | Meaning | Use |
|---|---|---|
| 0.1 | very noisy, relies on the denoiser | viewport, blockout |
| 0.05–0.075 | clean stills after denoise [gmGMsKJ6xd8@02:30] | look-dev, simple stills |
| 0.02–0.03 | good animation baseline | most finals |
| 0.01 (typ. default) | high quality | dark scenes, DOF, volumes, close-ups |
| 0.005 | very high | hero stills, print |

- Max Samples: 128 → 256 → 512 is the ladder [gmGMsKJ6xd8@02:00]. cycles_20x_faster uses **0.03 / Max 1000** as a default and sees little visible difference between 1000, 2000 and 4096 once denoised [cycles_20x_faster@09:45][cycles_20x_faster@10:30]; it allows up to 0.1 for some projects — not for dark/DOF/volume animation (see §3.2 flicker).
- **Min Samples floor:** with a high threshold (≥ 0.03) or reduced Max Samples, set Min Samples ~20 so every pixel gets a base of samples and the noise estimate is reliable [cycles_20x_faster@11:15]. At 0.01, 0 (auto) or 32–64 is enough. For animation finals 512–1024 with threshold 0.01–0.03 is a common sweet spot. If you need > 2048, fix the scene instead.
- **Time Limit** (seconds per frame) is a hard budget, useful for previews. For finals prefer a threshold, because time limits produce different noise per frame when frame complexity varies (flicker).
- **Seed:** keep **animated seed** on for animation. A fixed seed produces a static noise pattern that the eye reads as "dirt on the lens" while the camera moves. Animated noise plus a denoiser at a low threshold reads like fine grain.
- **Pattern:** Automatic (uses blue-noise distribution) gives more pleasing residual noise. Scrambling Distance trades correlation (blotches) for GPU speed; leave Automatic.

### 3.2 Denoising
- **OpenImageDenoise (OIDN):** the best quality, works on Apple Silicon GPU. Prefilter **Accurate** (the albedo/normal passes are themselves denoised before guiding, which keeps texture detail) and Quality **High** for finals. Balanced/Fast for previews.
- **OptiX:** NVIDIA only. Fast, good for the viewport [gmGMsKJ6xd8@02:45]. Not available on Mac.
- **Passes Albedo + Normal** always. They tell the denoiser where texture and geometric edges are, so it doesn't smear them.
- **Render-time vs compositor denoise:** the Denoise node (Image, Normal, Albedo inputs; Prefilter, Quality, HDR options) in the compositor gives the same result but lets you keep the *noisy* pass in the EXR [lE308jCAT2o@02:15]. Enable View Layer › Passes › Data › **Denoising Data**. Denoise **first**, before any sharpen/glare/curves [lE308jCAT2o@02:45]. Tick the node's **HDR** option so values above 1.0 aren't clamped, and mix the denoised result back with the noisy image to dial strength [cycles_20x_faster@17:30–17:45]. Cost on an RTX 4090 ≈ none vs render-time denoise [cycles_20x_faster@18:00]. If you rebuild from passes, denoise the rebuilt beauty with albedo+normal [vtdczoXVyvQ@06:15].
- **Denoising animation flicker:** OIDN is a per-frame (spatial) denoiser. At low sample counts its guesses differ each frame, so dark gradients, DOF bokeh, volumes and soft shadows shimmer or "boil". Fixes, in order:
  1. Lower the noise threshold (0.03 → 0.01) and raise max samples. This is the real fix.
  2. Raise light sizes or fix the noise sources (§4, §9).
  3. Enable Light Tree (default) for many-light scenes.
  4. Render without denoising, saving noisy + albedo + normal, and use a temporal denoiser in post (DaVinci Resolve Studio Temporal NR, or Neat Video). Better than the spatial denoise for slow camera moves.
  5. Add fine animated grain in post to mask residual shimmer (see compositing.md).
  6. EEVEE for that shot, if style permits.
- **Over-denoising slop:** waxy skin, plastic wood, melted label text, "oil painting" textures. Lower the threshold or use Prefilter Accurate. Don't sharpen afterwards (it amplifies blotches).

### 3.3 Light Tree
**Light Tree** (Sampling › Lights) chooses which light to sample based on its likely contribution. It's essential with many lights (emissive strips, LED arrays, city windows) and mesh emitters. Leave it ON (default). Turn it off only to debug or compare.
**Conflict recorded:** cycles_20x_faster turns Light Tree **off** for a 5-light product shot to save its per-sample overhead, and keeps it on for "dozens or hundreds" of lights [cycles_20x_faster@11:45–12:00] (no isolated timing shown). Resolution: OFF is a candidate only for ≤ ~5 lamp lights with no emissive meshes/strips, and only after an A/B timing at equal noise; any interior with practicals, LED strips or emissive screens keeps it ON. **Light Threshold** culls lights whose contribution is below the threshold; 0 disables it. Raise it slightly for scenes with hundreds of weak lights.

---

## 4. Light Paths (Render Properties › Light Paths)

Option names: Max Bounces › **Total, Diffuse, Glossy, Transmission, Volume, Transparent**. Clamping › **Direct Light, Indirect Light**. Caustics › **Filter Glossy, Reflective, Refractive**. **Fast GI Approximation** › Method (Replace / Add), AO Factor, AO Distance, Viewport Bounces, Render Bounces.

| Setting | Typ. default | Preview | Final (typical VSL) | Notes |
|---|---|---|---|---|
| Total | 12 | 4 | 8–12 | caps all |
| Diffuse | 4 | 1–2 | 3–4 | interiors with bounce light need 3–4; exteriors 2 |
| Glossy | 4 | 1–2 | 3–4 | mirrors facing mirrors need more |
| Transmission | 12 | 4 | 8–12 | glass: each surface is 1 bounce in, 1 out. Too low → black glass |
| Volume | 0 | 0 | 0–2 | 0 = single scatter (fine for haze); >0 for clouds/thick smoke |
| Transparent | 8 | 8 | 16–32 | alpha-mapped leaves/hair/particles stacked turn black if too low |
| Clamp Direct | 0 (off) | 0 | 0 | rarely needed; clamping direct kills highlight energy |
| Clamp Indirect | 10 | 5 | 3–10 | lower = fewer fireflies, but darker/duller bounces and dimmer reflections of lights |
| Filter Glossy | 1.0 | 1.0 | 0.5–1.0 | blurs sharp glossy paths in indirect light to reduce fireflies; too high = blurred reflections |
| Caustics Reflective / Refractive | on | off | off unless needed [gmGMsKJ6xd8@03:30] | the biggest firefly source; glass/water shot with visible caustics = keep, raise samples. cycles_20x_faster keeps them **on** for a transparent/glossy product [cycles_20x_faster@13:30]; resolution: on only when caustic light on a diffuse surface is visible and wanted — glossy reflections of lights are not caustics and don't need it |

**Tuning procedure (per scene, card `rendering-light-path-bounce-tuning`):** Rendered viewport with viewport denoise, set Diffuse/Glossy/Transmission/Volume to 1, raise each until the image stops changing, then Total = their sum [cycles_20x_faster@12:45–13:15]. Author's translucent product shot ended at 8/1/3/4/0, Transparent 8 [cycles_20x_faster@13:27]. Gains are largest in bright high-albedo rooms and glass; small in dark rooms with black walls (paths die early). Confirm on a final-quality still. Clamping: the author leaves defaults (Indirect 10) [cycles_20x_faster@13:15], consistent with the table.

**Fast GI Approximation:** replaces deep diffuse bounces with AO-style approximation after N bounces. Useful for big exteriors and preview. In interiors it can flatten bounce colour, so compare it with the full GI before committing. **Conflict:** skool-rr-rendering keeps it always ON (Viewport/Render bounces 2, Replace, AO 1, 10 m) and says the difference is not noticeable [skool-rr-rendering@09:55–10:28] — no A/B shown, author admits not understanding it. Resolution: A/B per interior shot.

**Volumes (Render › Volumes):** Blender 5.0 made **unbiased null-scattering** the default. **Biased** restores the old ray marching with Step Rate / Max Steps. It's often faster and less noisy for uniform haze boxes (gmGMsKJ6xd8@03:45 says the same). Scene scale matters: Principled Volume Density 0.01 per metre gives light haze in a 5 m room, fog in a 100 m landscape [uO0GuFuGRQc@00:30]; 0.05 for visible god rays indoors [1MyARLB8KzY@07:00].

---

## 5. Performance (Render Properties › Performance)

- **Persistent Data** (Final Render): keeps the BVH, shaders and textures between frames. Big win for animations where only the camera/objects move and geometry topology doesn't change. Costs memory [gmGMsKJ6xd8@03:00]. It only helps from the **second frame** of a render job (the first frame builds the data) [cycles_20x_faster@14:45]. Check that animated image/movie textures still advance frame to frame when it's on (one short test).
- **Tiles:** since Cycles X tiling is automatic. 5.0 removed the "Use Tiling" toggle. Tiling is always on, and a larger **Tile Size** effectively disables it. Leave 2048 typ. Lower it (e.g. 512) only to reduce memory on huge resolutions. Measured on an RTX 4090 at 1280×1440: Tile 128 → 5 min 40 s, 2048 → 1 min 10 s, 4096 → 1 min 10 s [cycles_20x_faster@14:05]: small tiles starve a fast GPU. In 5.2, Tile Size also limits which textures the Texture Cache loads.
- **Acceleration structure:** Spatial Splits / Compact BVH / curve options. Effects on GPU are scene-dependent; don't enable blindly (claim in gmGMsKJ6xd8@03:15 untested).
- **Compositor device:** Render › Performance › Compositor › Device **GPU** [gmGMsKJ6xd8@03:15]. Precision Auto (Full only for very wide-range data).
- **Simplify** (Render › Simplify): Max Subdivision, Child Particles %, Texture Limit / **Texture Resolution %** (5.2). Use these for blockout/preview profiles.
- **Scene optimisation first** (card `rendering-scene-optimization-simplify-culling`): collection instances instead of copies [cycles_20x_faster@02:15]; Simplify Max Subdivision 2–3 [cycles_20x_faster@02:45]; Texture Limit — a 16K HDRI went 49 s → 15 s at 1024 [cycles_20x_faster@03:15] (not for HDRIs/textures seen sharply); camera culling via Simplify › Culling + per-object Use Camera Cull [cycles_20x_faster@04:15] (**not in closed interiors**: off-screen geometry shapes light and shadow). End-to-end on the author's benchmark, all optimisations + settings: 1:20 / 3.6 GB → 13.5 s / 1.1 GB per frame (≈6×, despite the "20×" title) [cycles_20x_faster@01:15][cycles_20x_faster@14:45].
- **Scene hygiene** [gmGMsKJ6xd8@05:45–07:45]: exclude off-screen collections (View Layer checkbox), instance with Alt+D (linked data), Purge Unused Data, Decimate distant meshes (ratio ~0.1–0.3 for far background), downsized textures for distant objects, camera culling (Geometry Nodes or particle display).

---

## 6. Film, resolution, motion blur

- **Resolution:** set the delivery resolution (1920×1080, 1080×1920 vertical for social, 3840×2160 when the editor punches in). The **Resolution %** slider is the fastest preview lever: 50% = ¼ the pixels ≈ ¼ the time.
- **Render at a higher resolution for punch-in:** VSL editors often scale 110–130% in the edit, so render 4K or 1.25× when zooms are planned.
- **Pixel Filter (Film › Pixel Filter, Blackman-Harris 1.50 px typ.):** narrower (1.0 px) = crisper, but aliasing/moiré/crawling edges in motion [uO0GuFuGRQc@01:45]. Keep 1.5 for animation. For crisp stills 1.0–1.2 is OK. Prefer subtle sharpening in comp over a narrow filter.
- **Transparent (Film › Transparent):** renders alpha for comping over backgrounds in Premiere/AE. Needs PNG RGBA, EXR, or ProRes 4444 via conversion. "Transparent Glass" option for glass over background (Cycles). Watch for premultiplied/straight alpha mismatches (dark fringes) in the editor.
- **Motion blur (Render › Motion Blur):** on for anything moving fast. Shutter **0.5** (= 180° shutter, cinematic default). 0.25 for crisp, staccato action; 1.0 for dreamy streaks. Position Center on Frame. Cycles: costs little time, but deformation blur needs per-object Motion Blur steps. EEVEE: Steps 1–4 (more = better for curved paths). Without motion blur, fast CG motion strobes. That is a strong "CG" tell.
- **Overscan (EEVEE):** avoids screen-space reflection/AO artifacts at frame edges.

---

## 7. Render preview profiles (concrete settings)

Name them and switch via scripts or presets. For Cycles:

| Setting | **Blockout** (composition, timing) | **Look-dev** (lights, materials) | **Final** (delivery) |
|---|---|---|---|
| Engine | EEVEE or Workbench (or Cycles at very low quality) | Cycles (or EEVEE if final is EEVEE) | Cycles/EEVEE |
| Resolution % | 25–50% | 50–100% | 100% |
| Noise threshold / Max samples | 0.1 / 16–32 | 0.05 / 128–256 | 0.01–0.03 / 512–1024 (stills 0.01 / 1024–2048) |
| Denoise | OIDN Fast/Balanced, prefilter Fast | OIDN High, Accurate | OIDN High, Accurate (or off + Denoising Data for post denoise) |
| Bounces Total/Diff/Gloss/Trans | 4/1/1/4 | 8/3/3/8 | 12/4/4/12 (raise only if needed) |
| Clamp Indirect | 3 | 5–10 | 5–10 |
| Caustics | off | off | only if story needs it |
| Volumes | off or Biased large step | Biased | Biased or unbiased per test |
| Simplify | Subdiv 0–1, children 10%, textures 512 | Subdiv 2, textures 2048 | off |
| Motion blur | off | off (check on a few frames) | on, 0.5 shutter |
| Persistent Data | n/a | off | on (animation) |
| Output | FFmpeg H.264 preview / PNG 8-bit | PNG 8-bit / EXR half for comp tests | EXR multilayer half (comp) + PNG16 / ProRes 422 HQ (edit) |
| Typical time/frame (M-series, 1080p, mid scene) | < 5 s | 20–60 s | 1–5 min |

EEVEE finals: Render samples 128–256; Raytracing on, Resolution 1:1–1:2; Volume resolution 1:2–1:4, Steps 128; Shadow rays 2–3 / steps 6+ (**interiors with soft suns: steps 12–16** [eevee_full_course@07:40] — this source raises our old floor of 6); Motion Blur steps 2–4; Filter 1.5.

---

## 8. Output formats (Output Properties)

| Purpose | Format | Settings | Why |
|---|---|---|---|
| Comp master / archival | **OpenEXR MultiLayer** | Half, **DWAA** for beauty/light passes [vtdczoXVyvQ@01:45]; separate File Output with **ZIP/PIZ, Full float** for Cryptomatte/Z/Position/Normal/Vector | Linear HDR; glare/exposure still behave correctly afterwards [gmGMsKJ6xd8@09:00]; lossy codecs corrupt data passes |
| Single-layer beauty for VSE glow | OpenEXR | Half, DWAA, RGB(A) [gmGMsKJ6xd8@08:00] | small, linear |
| Edit-ready, look baked | **PNG 16-bit** RGB(A) sequence → convert to ProRes in Resolve/Media Encoder | Compression 15–50% | Safe, resumable, alpha capable, no banding |
| Edit-ready video directly | FFmpeg › QuickTime › **ProRes** (422 HQ), or DNxHD | per the 5.2 manual Blender lists ProRes 8/10-bit, no alpha | Premiere/Resolve friendly, scrub-fast |
| Preview / review link | FFmpeg › MPEG-4 › H.264, Quality High | even dimensions required | small; never for editing masters |
| HDR delivery (rare for VSL) | H.265/AV1 10-bit, Display Rec.2100 PQ | per manual | 5.0+ supports HDR video |

- Always render long jobs as **image sequences** (Overwrite off + Placeholders for resume/multiple machines).
- Colour: PNG/ProRes/H.264 bake the **view transform** (AgX…). EXR stores scene-linear values (view transform not applied). See color-management.md.
- Frame range and fps must match the edit timeline (24, 25, 29.97 or 30). Changing fps after animating changes motion timing.

---

- **Frames → video manually** [skool-rr-rendering@16:08–18:43]: a fresh General .blend › Video Editing › Shift+A Image Sequence (select all with A) › trim to last frame › FFmpeg: QuickTime + ProRes 422 HQ for editing, MPEG-4 H.264 High for social. Fresh file (or Post Processing › Compositing off) so the compositor isn't applied twice.
- **Render farms** (GarageFarm, OctaRender, SuperLuminal) → card `rendering-render-farm-submission` [skool-rr-rendering@18:43].
- **Samples vs resolution:** skool-rr-rendering says 4K needs fewer samples than 1080p [skool-rr-rendering@07:16]. Per-pixel noise is the same; it only averages out when downscaled. Don't render above delivery size for that reason.

## 9. Render time budgeting

1. Count frames: duration × fps (e.g. 8 s × 30 fps = 240 frames).
2. Available machine time (e.g. overnight 10 h = 36,000 s) → budget = 150 s/frame. Keep a 30% margin for re-renders → **~100 s/frame**.
3. Render 3 representative frames (start, the most complex, end) with final settings. Use the slowest one × frames.
4. If over budget, reduce in this order: (a0) optimise the scene without quality loss — instances, Simplify caps, Persistent Data, per-scene bounce tuning [cycles_20x_faster@00:30]; (a) fix noise sources (lights, caustics, volumes Biased); (b) raise the threshold 0.01 → 0.02; (c) Resolution % to 100% of delivery only (don't overshoot); (d) layers: render static background once (region/plate tricks, gmGMsKJ6xd8@09:30, test seams); (e) EEVEE for graphic shots; (f) Frame Step 2 + optical-flow interpolation as a last resort [gmGMsKJ6xd8@11:00] (artifacts on fast motion/occlusion).
5. Log the time per frame in the project notes for future estimates.

---

## 10. Render artifact QA — causes and fixes

| Artifact | Looks like | Common causes | Fixes |
|---|---|---|---|
| **Fireflies** | isolated white/coloured hot pixels; denoiser turns them into blobs | caustic paths, tiny bright lights seen via glossy, sharp glossy + rough diffuse combos, emissive meshes, HDRI sun | Caustics off; Clamp Indirect 3–10; Filter Glossy 0.5–1; enlarge light sizes; Light Tree on; replace the HDRI sun with a Sun lamp; Roughness ≥ 0.05 on near-mirror surfaces |
| **Noise / grain** | uniform speckle, worst in shadows/indirect areas | threshold too high, light only through small openings, volumes | lower the threshold; portals (area light at windows, Portal option); Biased volumes; more light power in dark areas |
| **Denoiser splotches / blotches** | low-frequency mottled patches in flat dark areas or volumes | too few samples for the denoiser; Scrambling Distance; missing albedo/normal | lower the threshold, Min Samples up; Prefilter Accurate; Albedo+Normal |
| **Flicker / boiling (animation)** | shadows, GI, DOF or volumes shimmer frame to frame | spatial denoise at low spp; fixed seed vs animated mixing; EEVEE probes updating; Time Limit | §3.2 list; consistent threshold, no Time Limit; bake EEVEE probes; temporal denoise in post |
| **Banding** | stair-steps in gradients (sky, vignette, glow, dark backgrounds) | 8-bit output, heavy grading after 8-bit, H.264 compression | render 16-bit PNG/EXR; Post Processing › **Dither** (1.0 typ.); add grain in post; grade before quantisation |
| **Light leaks** | light bleeding under walls/corners, glowing seams | single-sided thin walls, gaps in geometry, EEVEE probe/irradiance leaking, Fast GI | solidify walls (thickness); close gaps; EEVEE: shadow Steps 12–16, volume probe bake (Surfel Resolution ~100, Surface Offset up for banding, Normal/View Bias for leaks under objects), object Light Probe visibility [eevee_full_course@07:40][eevee_full_course@43:40]; Fast GI Distance ~1–2 m so far bounce comes from the probe |
| **Z-fighting / coplanar flicker** | interlaced striped patterns switching per frame | two faces in the same plane (decals, duplicated floors) | offset 0.1–1 mm, delete duplicates, use a mix shader/decal method instead |
| **Shadow terminator** | faceted dark stepping on low-poly smooth-shaded curved surfaces | smooth normals vs actual geometry | subdivide or Smooth by Angle; Object Properties › Shading › **Shadow Terminator** › Geometry Offset (0.1–0.3), Shading Offset |
| **Black glass / black transparency** | glass or leaves turn black | Transmission/Transparent bounces too low | raise Transmission (12+) and Transparent (16–32) |
| **Self-intersection / bad normals** | dark triangles, inverted shading | flipped normals | Recalculate normals; Face Orientation overlay |
| **Clipped highlights** | flat white blobs, hue-shifted lights | Standard view transform, overexposure | AgX/ACES, exposure via False Color (color-management.md) |
| **Aliasing / crawling edges** | stair-stepped thin lines, shimmering speculars in motion | narrow pixel filter, too-thin geometry, high-frequency textures | filter 1.5; mipmaps/texture filtering; thicken lines |
| **Motion strobing** | jerky fast motion | no motion blur | enable motion blur, shutter 0.5 |

QA procedure for every final: (1) a full-res still at 100% and 200% crops of shadows, gradients and textures; (2) a playback of ≥ 3 s at speed (Image Editor or VSE); (3) a histogram/False Color check for clipping; (4) the export checked in the target editor (Premiere/Resolve), not only in Blender.

---

## 11. Slop signs in rendering (quick list)

- Visible denoiser smear (plastic textures) or boiling in motion.
- No motion blur on fast moves.
- Blown, clipped, hue-shifted lights (Standard view transform).
- 8-bit banding in dark gradient backgrounds, which is very common in dark "cinematic" VSL scenes.
- Over-sharpened render (Pixel Filter 1.0 + sharpen) with crawling edges.
- Volumetric haze everywhere with noisy, splotchy fog.

---

## Sources
- Videos: [gmGMsKJ6xd8], [vtdczoXVyvQ], [uO0GuFuGRQc], [1MyARLB8KzY], [lE308jCAT2o], [eevee_full_course], [cycles_20x_faster], [skool-rr-rendering] (see `sources/*.md`).
- Blender 5.0 Cycles release notes (volumes null-scattering default, Biased option, Use Tiling removed): https://developer.blender.org/docs/release_notes/5.0/cycles/
- Blender 5.1 Cycles notes (HIP RT default, denoising quality for transparency/roughness): https://developer.blender.org/docs/release_notes/5.1/cycles/
- Blender 5.2 Cycles notes (Texture Cache, Texture Resolution %, World Cast Shadows): https://developer.blender.org/docs/release_notes/5.2/cycles/
- Blender 5.2 manual — Sampling, Light Paths, Supported Video formats: https://docs.blender.org/manual/en/latest/render/cycles/render_settings/sampling.html · …/light_paths.html · https://docs.blender.org/manual/en/latest/files/media/video_formats.html
