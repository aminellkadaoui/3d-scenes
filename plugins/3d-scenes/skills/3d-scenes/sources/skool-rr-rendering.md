# Rendering (Render Room — 3D Documentary-Style Mastery › Rendering & Workflows)
- url: https://www.skool.com/render-room-7187/classroom/a39a68c5?md=2df4271de9be44a5afc08fca0b545266 (private Skool course)
- channel / duration / Blender version shown: Lucas Carrazana (Render Room) / 34:15 / Blender 4.x UI (default cube scene; exact version not readable)
- domain(s): rendering (primary), color, pipeline/output, render farms
- evidence used: transcript (Skool English CC, read in full) + browser contact sheet of 12 frames (4:25–15:05, seen, not saved) + 3 enlarged panel crops (Fast GI panel @10:15, Sampling @5:55, Light Paths @9:10). Lesson page note: "use ProRes 422 HQ if you export for editing software".
- trust: medium-low on settings, medium on workflow. Speaker says himself "I don't really know what samples is", "I don't understand Fast GI", "I asked GPT" for bounces. Settings are personal habits without A/B proof. Render-farm walkthroughs are practical; he has an affiliate code for SuperLuminal (10%) — disclosed.

## 1. Problem it solves
Render 3D animations for clients without crashing, losing a night of rendering, or frying the PC; choose formats, engine settings, and when to use a render farm.

## 2. Techniques

### T1 — Render image sequences, never a video file directly `[00:00–01:31]`
- Crash/power loss → resume from frame N; re-render only a bad range (e.g. 150–250). Already in `rendering.md §8` / `rendering-exr-handoff-formats`. Status: Extracted (confirmation).

### T2 — Format quick guide `[01:31–02:02]`
- Alpha, no comp → PNG RGBA, compression 15%. Alpha + comp → OpenEXR RGBA, Float (Half), DWA lossy. No alpha, no comp → JPEG 90%.
- Our note: JPEG is 8-bit lossy and bakes the look — fine for previews only; our deliverable stays PNG16/EXR/ProRes per `rendering.md §8`. Status: Extracted.

### T3 — Resolution/fps decisions `[02:02–03:39]`
- 4K industry standard; 24–30 fps; if the client gives face footage, match its resolution and fps; faceless → ask the client, else 24–30. Cinematic option: 21:9 instead of 16:9 (Fern, Cipher, Thinker).
- Our project: 1920×1080, 30 fps, 16:9 fixed by the brief (CLAUDE.md) — 21:9 would be a letterbox inside 16:9 only if art direction asks. Status: Extracted.

### T4 — Cycles setup habits `[03:39–13:36]` (frames @4:25, 5:55, 6:50, 9:10, 10:15, 10:45, 11:20, 12:55)
- Feature Set Experimental; Device GPU; for previewing a very heavy scene he switches to CPU so Blender doesn't crash (GPU VRAM limit — on Apple Silicon unified memory this distinction mostly disappears).
- Viewport: Noise Threshold 0.1, Max Samples 50, denoise on (seen @5:55).
- Render: Noise Threshold **0.01**, do not raise to 0.03 for animation (more noise/flicker in his experience) [06:16]; Max Samples 100–500 (100 usually, 500 if flicker) [06:46]; 1080p needs more samples than 4K [07:16]; OptiX on NVIDIA [07:16].
- Light Paths: tune bounces per material types present; defaults have Volume 0 → raise if volumes [07:49–09:55].
- Fast GI Approximation ON, bounces 2/2 — "difference not noticeable, renders faster" [09:55] (panel @10:15 shows Method Replace, AO Factor 1, AO Distance 10 m).
- Simplify › Texture Limit 4K for 8K textures [10:28]; Culling › Camera Cull distance 2 + per-object Use Camera Cull only for small objects that don't affect light/shadow — never on walls (sun leaks) [11:02–12:34].
- Performance › Persistent Data ON [12:34].
- Color management: AgX + High Contrast (sometimes Medium High); Standard / Khronos PBR Neutral for stylised saturated looks [13:05–13:36].
- Status: Extracted. Mostly already covered (`rendering-adaptive-sampling-denoise`, `rendering-light-path-bounce-tuning`, `rendering-scene-optimization-simplify-culling`, `color-view-transform-exposure`).

### T5 — EEVEE habits `[13:36–15:08]`
- Samples default/100; Raytracing on, Resolution 1:1, Precision 0.8; Fast GI resolution 1:1, raise rays/steps while watching render view. Covered by `rendering-eevee-raytracing-fastgi`. Status: Extracted.

### T6 — Image sequence → video in a separate, clean .blend (VSE) `[16:08–18:43]`
- Open a NEW General file (so the compositor isn't applied a second time), Video Editing, Shift+A › Image Sequence, select all frames (A), trim strip to the last frame, Output FFmpeg: for editing → QuickTime + ProRes (page note: ProRes 422 HQ); for social → MPEG-4 + H.264, quality High.
- Why separate file: the compositor (Post Processing) would re-apply glare/grade to already-graded frames. Equivalent safe alternative in the same file: Output › Post Processing › untick Compositing.

### T7 — Render farms `[18:43–34:15]` → card `rendering-render-farm-submission`
- Why: a 10 h local job ≈ 20 min on a farm (claim, not measured) [18:43].
- GarageFarm (RenderBeamer add-on; $50 trial via Solutions › Blender; copy the job link before submitting; Full job vs Test job; priority Low is cheapest; multi-scene jobs take the active scene's Cycles settings; don't tick extra cameras (each = separate render, extra cost); don't tick "create video" (extra cost)) [19:15–23:30].
- OctaRender (cheapest; crypto top-up; rent nodes sorted by score, e.g. 6× RTX 3090 ≈ $0.5/h; include add-ons that affect the camera e.g. Camera Shakify; requeue red/stuck frames; STOP all sessions after, or it keeps billing) [23:30–30:29].
- SuperLuminal (easiest, pricier; per-project; include enabled add-ons; download via add-on › Render Jobs) [30:29–34:09].
- Status: Extracted.

## 3. Claims I doubt or must test
- "Threshold 0.01 + 100 samples" is internally inconsistent: at Max 100 the cap stops most pixels long before 0.01 is reached, so the threshold barely matters — his real quality knob is Max Samples. Conflicts with our 0.01–0.03 / 512–1024 animation profile and with cycles_20x_faster (0.03 / 1000 / Min 20).
- "0.03 gives more flicker" — plausible for animation, but untested by him in isolation; consistent with our §3 warning.
- "Fast GI: no noticeable difference" — conflicts with our note that it can flatten bounce color in interiors (our bedroom is a dark interior). Must A/B.
- "4K needs fewer samples" — per-pixel noise is the same; it only looks less noisy after downscaling to 1080p delivery. Not a reason to render 4K when delivering 1080p.
- "GPU always faster" — on Apple Silicon test Metal vs CPU.
- "10 h → 20 min" farm claim: marketing-level, no data.

## 4. Anti-AI-slop lessons
- Flicker in animation comes from too few samples / high threshold — check playback, not one still.
- Don't let the compositor apply twice when converting frames to video.
- Camera culling on room walls makes light leak — closed interiors stay fully visible.

## 5. Candidate isolated test
