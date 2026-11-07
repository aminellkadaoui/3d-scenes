# How to use Eevee - Full Blender Course
- url: local file (local file) (no YouTube id; this repo id = `eevee_full_course`)
- channel / duration / Blender version shown: channel not identified from frames (single presenter, webcam overlay) / **1:16:54** (ffmpeg) / **Blender 4.4.0** (status bar, every settings crop). EEVEE "Next" UI. Our target is 5.2: panel names below must be re-checked in the 5.2 UI.
- domain(s): rendering | lighting | materials | environment
- evidence used: user-pasted transcript, summarised by the caller (no timestamps in it) + **frames I viewed**: 15 contact sheets (231 frames, every 20 s, `raw/eevee_full_course/frames/sheet_00–14.jpg`) and 25 full-res crops in `raw/eevee_full_course/frames/detail/` (list in §6). **Timestamps are frame-derived and approximate (±20 s)**; values marked "(transcript)" were not visible in any frame I opened.
- trust: **high-medium**. Methodical, shows each problem then its fix, many on-screen before/after and an EEVEE-vs-Cycles glass comparison; honest about limits (shows a Blender bug report). Sponsor segment (Poliigon add-on, ~44:00–46:20) = promo, ignored. Test scenes are simple (cube room + Suzannes, then one furnished room), so numbers are scene-specific.

## 1. Problem it solves
EEVEE (4.2+) interiors look wrong out of the box: light bleeds through walls, soft shadows are grainy, reflections/bounce vanish when objects leave the screen ("lights switch on/off" while panning), world light floods closed rooms, glass refraction breaks, and render times balloon. The course explains *why* each happens (screen space vs probes vs shadow maps) and gives the setting that fixes it.

## 2. Techniques

### T1 — Light bleed through walls: wall thickness + shadow Steps `[~03:00]–[~09:20]`
- What: give walls real thickness (Solidify modifier seen at ~03:00); Render › Sampling › Render › **Shadows › Steps** raised from default to **16** (seen 07:40 and 09:20: Rays 1→2, Steps 16, Resolution 1.000). Transcript: default 6 → 12–16; bleed grows with light size/softness and sun angle.
- Why: EEVEE shadows are shadow maps traced in steps; thin geometry + few steps + a wide (soft) light lets the shadow "miss" the occluder.
- Use when: any interior with sun/large lights. Don't overshoot Steps on scenes without bleed (cost).
- Status: Extracted → card `rendering-eevee-shadow-bleed`.

### T2 — Soft-shadow noise: Render Samples + shadow Rays `[~05:20]–[~09:20]`
- What: Render Samples **64** (seen); shadow **Rays** 1 → 2 (seen 09:20). Rays only multiply samples for soft shadows; raise samples when DOF/motion blur also need them.
- Status: Extracted → in `rendering-eevee-shadow-bleed`.

### T3 — Turn Raytracing ON (off by default) `[~09:20]–[~11:00]`
- What: Render › **Raytracing ✔**; Method **Screen-Trace**, Resolution **1:2**, Denoising ✔, Fast GI Approximation ✔ (seen 09:20 off → 10:00/15:30/21:00 on). Diagram "What the camera sees / what happens to the scene" (~10:40) explains screen space: only on-screen pixels can be reflected/bounced.
- Status: Extracted → card `rendering-eevee-raytracing-fastgi`.

### T4 — Plane probe for flat glossy surfaces `[~14:40]–[~17:20]`
- What: Add › Light Probe › **Plane**, place it *exactly* on the floor/mirror (check with **Viewport Display › Capture**). Panel seen at 17:20: Distance **0.1 m**, Clipping Offset **0.001 m**. Fixes ghosting/missing reflections of objects partly off-screen.
- Status: Extracted → card `rendering-eevee-reflection-probes`.

### T5 — Sphere probe for chrome/glass `[~18:40]–[~20:00]`, `[~53:20]–[~56:20]`, `[~73:20]`
- What: chrome Suzanne (Metallic 1, Roughness 0, seen 18:40) only reflects itself correctly with a **Sphere** probe around it. Panel seen at 55:40: Radius **0.43 m**, Falloff 0.2, **Clipping Start 0.19 m** (must clear the object itself), End 20 m. Probes can't see other probes (transcript). Scene › Light Probes › **Spheres Resolution** (1024 px seen 75:00; 2048 px seen ~65:40).
- Status: Extracted → `rendering-eevee-reflection-probes`.

### T6 — Raytracing roughness threshold + Fast GI `[~21:00]–[~29:00]`, `[~48:20]`, `[~75:20]`
- What (seen 26:20): Fast GI **Threshold 0.5** (Max Roughness: rays below, Fast GI above), Method **Global Illumination**, Resolution 1:2, Rays 2, **Steps 8 (default)**, Precision 0.25, **Distance 0 m**, Thickness Near 0.25 m / Far 45°, Bias 0.05. Later (seen 48:40, 75:20): **Steps 16**, **Distance 1.42 m** (after a volume probe exists). Denoising sub-panel: Spatial Reuse, **Temporal Accumulation**, Bilateral Filter (48:40); ON/OFF wood-floor comparison at ~48:20 — temporal accumulation off = sharper texture (transcript). 75:20–75:40: tests Raytracing 1:4 and Fast GI 1:16/1:1; tooltip "Render this effect at 6.25% render resolution". Transcript: lowering resolution saves little and flickers; he used 1:1 and 1:2.
- Status: Extracted → `rendering-eevee-raytracing-fastgi`.

### T7 — Volume probe (baked irradiance) for bounce light `[~29:20]–[~43:40]`
- What: Add › Light Probe › **Volume**, scale to the room so the grid points sit *just inside* the walls (ortho views ~32:00, ~38:00). Seen at 42:40: Resolution **8 × 19 × 5** (≈ cubic cells for an elongated room), Bake Samples **2048**, **Surfel Resolution 100** (default 20 seen at 43:40). Capture: Distance 20 m, Contributions World ☐ / Indirect Light ✔ / Emission ✔ (40:20). Offset: Surface Offset **0.050**, Search Distance **0.100** (40:20; ~0.288 tried around 39:40). Bias panel: Normal Bias **0.30**, View Bias 0.00, Facing Bias 0.50, Validity Threshold 0.40, Dilation Threshold 0.50, Radius 1.00 (43:40). Then **Bake Light Cache**. Transcript: raise Surface Offset against banding; Normal/View bias against bleed under objects.
- Render cost seen: simple room **0.93 s/frame** at 43:40 (render result header).
- Status: Extracted → `rendering-eevee-volume-probe-bake`.

### T8 — World/HDRI light leaking into closed rooms + Sun Threshold `[~35:20]–[~38:00]`, `[~49:20]–[~52:40]`
- What: blue world colour floods the closed room (35:20–37:00; a tweet from a known Blender educator asking the same question at ~36:00). The volume probe is what blocks world light inside. World › Settings › **Sun › Threshold** extracts a sun from the HDRI (values 10.0 → 28.2, Angle 0.526° seen at 50:20–51:00; World Light Probe Resolution 1024). Author's preference (transcript, frames at ~52:00 show Threshold 0.000 with the Sun lamp re-enabled): **Threshold 0 + a real Sun lamp** for control.
- Status: Extracted → `rendering-eevee-volume-probe-bake`.

### T9 — Glass in EEVEE; "archviz glass" `[~53:00]–[~62:20]`
- What: Principled glass refraction is screen-space, needs a sphere probe, looks clearly worse than Cycles (side-by-side at ~56:40). A liquid inside a glass breaks. Archviz glass (node tree seen at 60:20): **Layer Weight (Blend 0.5) › Facing → Mix Shader Fac; Shader 1 = Transparent BSDF (white); Shader 2 = Glossy BSDF (Multiscatter GGX, Roughness 0)**. Material › Settings › **Render Method**: Blended works with sphere probes; **plane probes only work with Dithered** (Blender bug report shown ~61:00; Plane.001 set to Dithered at 62:20; also Transparent Shadows ✔, Light Probe Volume ✔, Thickness Sphere).
- Status: Extracted → `materials-eevee-archviz-glass`.

### T10 — Room volumetrics `[~62:40]–[~65:40]`, `[~76:20]`
- What: a cube enclosing the room, Surface None, **Volume Scatter, Henyey-Greenstein, Density 0.050, Anisotropy 0.000** (seen 63:30). Near-real-time in the viewport. Put the fog object and fake-glass window into a collection **"hide before baking"** (seen 65:20, 71:20, 75:40) — hide it, bake the volume probe, unhide.
- Status: Extracted → `environment-eevee-room-volume-fog`.

### T11 — Performance hygiene `[~69:00]–[~75:40]`
- What: furnished room (Poliigon assets) render **4.27 s/frame, 15.8 GB memory** (seen 71:20). Transcript: removing unnecessary texture maps 11 s → 4 s; each probe costs time (delete plane probes you don't need); Spheres Resolution is in Scene properties; fog adds ~0.5 s.
- Status: Extracted → `knowledge/rendering.md` §1.

## 3. Claims I doubt or must test
- "Lowering raytracing resolution saves little" — true for his 1080p scene on his GPU (likely high-end; 15.8 GB used). On an a 12 GB mid-range GPU at 1080p the curve may differ. Measure.
- Shadow Steps 12–16 as a universal fix: bleed also comes from single-sided walls; Steps only helps once geometry is closed.
- Temporal Accumulation off = sharper: in animation it may add flicker/noise. Check in motion, not on a still.
- Surfel Resolution 100 and Bake Samples 2048 are tuned for one 8×19×5 room; bake time/VRAM scale with them.
- Blender 4.4 → 5.2: Raytracing/Fast GI/probe panels may have moved or been renamed (e.g. "Light Probe" naming, Fast GI method names). Read RNA identifiers at runtime; don't hardcode.

## 4. Anti-AI-slop lessons
- EEVEE "gamey" tells — light leaks at wall corners, reflections that pop as the camera pans, flat world-tinted interiors, cut-out glass — are each a missing probe or setting, not "EEVEE can't do realism".
- Judge reflections **while moving the camera**: screen-space failures are invisible on a still.
- Fewer texture maps / probes is a quality-neutral speedup; only keep what the camera reads.

## 5. Candidate isolated test
Cube room 6×3×3 m, Solidify 0.2 m walls, window + Sun 2° angle, glossy floor, chrome sphere, glass, 0.05 fog box. Baseline EEVEE defaults vs full recipe (Steps 16, Rays 2, Raytracing 1:2, Fast GI 16 steps/1.5 m, plane + sphere + volume probes). Measure: wall-corner leak (luminance at the occluded corner), reflection pop over a 60-frame pan (frame-to-frame diff in the floor reflection region), s/frame, VRAM. Then the same frames in Cycles 512 spp as ground truth (ΔE / SSIM).

## 6. Visual verification (frames viewed)
Contact sheets 00–14 (all). Detail crops (`frames/detail/`): 07:40 Shadows Rays 1 / Steps 16 / Samples 64; 09:20 Rays 2 / Steps 16, Raytracing unchecked; 15:30 Raytracing ✔ Screen-Trace 1:2, Denoising ✔, Fast GI ✔; 17:20 plane probe Distance 0.1 m, Clipping Offset 0.001 m, Capture/Influence; 18:40 chrome material Metallic 1 Rough 0; 21:00 + 26:20 Fast GI defaults (Threshold 0.5, GI, 1:2, Rays 2, Steps 8, Precision 0.25, Distance 0 m, Thickness 0.25 m/45°, Bias 0.05); 40:20 volume probe Capture + Offset 0.05/0.1; 42:40 volume probe 8×19×5, 2048 samples, Surfel 100; 43:40 bias values + Surfel 20 + render time 0.93 s; 48:40 Denoising sub-options + Fast GI Steps 16 / 1.42 m / 1:4; 51:00 World Sun Threshold 28.2, Angle 0.526°, Light Probe Res 1024, World strength 6; 55:40 sphere probe Radius 0.43 / Clip Start 0.19 m; 60:20 archviz glass nodes; 62:20 Render Method Dithered; 63:30 Volume Scatter 0.050; 65:20 "hide before baking" collection with "fog"; 71:20 render 4.27 s, 15.8 GB; 75:20 / 75:40 Raytracing 1:4 + Fast GI 1:16 / 1:1 tests.
Not seen in frames (transcript only): shadow Steps default "6", the Normal/View bias fix narration, "11 s → 4 s", "fog +0.5 s", Max Roughness wording.
