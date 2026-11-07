# Lessons log

Short rules learned from real projects. Newest at the top. `3d-scenes-retro` appends here; rules confirmed in a second project get promoted into the reference files and marked `Proven`.

Format: `- [YYYY-MM-DD] [area] Rule — evidence (project) — status`

- [2026-11-07] [motion] "Peak Zoom" (زوم القمة): 30-frame mountain move whose speed peak lands exactly on the key frame (a click, a cut, or a frame the user names); half before, half after, then hold — screen-ui-shots — Proven
- [2026-11-07] [motion] Moves across cuts: put the same two keys (cut−15 old pose, cut+15 new pose) on BOTH cameras so the peak lands on the cut and the shot reads continuous; join check = camera position difference 0 at every cut — screen-ui-shots — Proven
- [2026-11-07] [motion] Peak slightly BEFORE the action (≈8 frames before the click) when the user wants the frame settled on the target as the click happens — screen-ui-shots — Candidate
- [2026-11-07] [camera] Screen shots: the user frames by hand in camera view (Lock Camera to View). Read the camera transform IMMEDIATELY after "كذا" — any depsgraph refresh snaps an unkeyed camera back to its curve and the pose is lost — screen-ui-shots — Proven
- [2026-11-07] [camera] Screen tracking = follow the CURSOR arrow tip, not the playhead line; keep the user's framing/zoom/tilt and only offset the camera parallel to the screen by the cursor delta — screen-ui-shots — Proven
- [2026-11-07] [camera] Clamp tracking so the frame never leaves the monitor (half-view = dist × sensor/lens / 2); clamp only the axis that would leave, otherwise tracking "stops" mid-shot — screen-ui-shots — Proven
- [2026-11-07] [camera] Camera close to a monitor with a character/lamp in between: drive clip_start from the camera–screen distance (x − screen − 0.12 m); move props out of frame rather than letting clip_start cut them (X-ray look) — screen-ui-shots — Proven
- [2026-11-07] [setup] Cut/trim screen animations at the user's frames by re-joining ProRes clips with ffmpeg concat -c copy (no re-encode); trim from the start with trim=start_frame=N then re-encode ProRes 422 HQ only that clip — screen-ui-shots — Proven
- [2026-11-07] [quality] Screen video looks dark: a video made for the old AgX-compensation chain (LUT-baked) and a plain video need different paths; give the plain video its own Sat 1.15 → AgX curve → Emission path, switched by a Mix Shader keyed at the cut — screen-ui-shots — Proven
- [2026-11-07] [quality] EEVEE large area lights shadow from the CENTRE: a fill whose centre sat inside a fan rod gave 0 light; enable Shadow Jitter. Jitter on a light that reflects in a glossy floor sparkles → split into diffuse-only jittered + specular-only non-jittered copy — interior-eevee-match — Proven
- [2026-11-07] [quality] EEVEE motion "flicker" was camera float + motion, not render noise: freeze the scene and diff identical frames before changing samples/denoise; Jittered DOF made it 3× worse — interior-eevee-match — Proven
- [2026-11-07] [quality] Never judge quality from a compressed MP4 preview; deliver PNG frames + ProRes 4444 XQ — interior-eevee-match — Proven
- [2026-11-07] [render] EEVEE matched to Cycles in a dark interior: 88 % brightness, noise ≈ Cycles, 34 s vs 223 s per frame (RTX 3060); recipe: jitter + per-group strengths fitted by least squares + 4 fake-bounce fills + compositor OIDN — interior-eevee-match — Proven
- [2026-11-07] [process] Fix only the scene the user points at; never spread a fix to other scenes/files without asking — interior-eevee-match — Proven
- [2026-11-07] [process] Fast motion preview: Workbench FLAT + Texture colour, 50 %, no MB, movie images forced to sRGB for the preview only (correct screen colours), from a copy of the file — screen-ui-shots — Proven
- [2026-11-07] [lighting] Light white/bright heroes with their own linked lights; exclude them from scene lights. Keyframing scene-light power at the cut was not enough — laptop-to-money — Proven
- [2026-11-07] [lighting] A saturated light on a white object turns white under AgX when pushed; to get colour, lower whites, don't raise the colour — laptop-to-money — Proven
- [2026-11-07] [lighting] UI edits touch only the active light; with duplicates, set all — laptop-to-money — Proven
- [2026-11-07] [lighting] After the user moves a light, check aim error; 55° off made a 1000 W light useless — laptop-to-money — Proven
- [2026-11-07] [motion] AE Speed graph In/Out 75% = two Bezier keys with FREE handles at 75% of the segment; cut on the measured peak frame — laptop-to-money — Proven
- [2026-11-07] [motion] Separate constant drift (linear, extrapolated) from the accent curve so the object never stops — laptop-to-money — Proven
- [2026-11-07] [quality] Viewport grain ≠ render grain; judge noise on a rendered frame cropped at 100% — laptop-to-money — Proven
- [2026-11-07] [quality] "Resolution feels low" = sharpness: temporal denoise off, DOF off, small hard raking light — laptop-to-money — Proven
- [2026-11-07] [quality] Downloaded model normal maps at 1.0 sparkle under hard light; 0.15–0.5 — laptop-to-money — Proven
- [2026-11-07] [render] Measure one final-quality frame before promising a time; tables underestimated ~10× — laptop-to-money — Proven
- [2026-11-07] [setup] Starting from the user's approved scene is the biggest time saver — laptop-to-money — Proven
- [2026-11-07] [process] Don't act on garbled messages; ask — laptop-to-money — Proven
- [2026-11-07] [motion] DEFAULT for every move = mountain speed graph In 75 / Out 75 (user rule, not only turntables) — scripts/mountain_ease.py — Proven
