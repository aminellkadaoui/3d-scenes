---
id: rendering-render-farm-submission
domain: rendering
status: Extracted
sources: [skool-rr-rendering@18:43, skool-rr-rendering@20:51, skool-rr-rendering@21:52, skool-rr-rendering@22:25, skool-rr-rendering@26:11, skool-rr-rendering@29:23, skool-rr-rendering@30:29, skool-rr-rendering@32:38]
blender: "5.2"
---
# Submitting a Blender animation to a render farm without wasting money

**Principle:** A farm splits frames across many GPUs; you pay per node-hour, so every extra camera, scene, frame range or forgotten session costs. The .blend must be self-contained (packed textures, add-ons included) or frames come back wrong.

**Steps / settings (starting points):**
1. Before upload: final settings in the .blend (engine, samples, output format = image sequence EXR/PNG, frame range, active camera). File › External Data › Pack Resources; check video textures (screen footage) are supported/packed.
2. Include add-ons that change the result (e.g. camera shake add-ons) in the farm add-on's "include add-ons" list [skool-rr-rendering@26:11][32:38]. Drivers/scripts: check auto-run is allowed on the farm.
3. GarageFarm (RenderBeamer): copy the job link before "submit" [20:51]; run a Test job (skips frames) when unsure, then Full job; priority Low is cheapest [21:22]; multi-scene jobs use the ACTIVE scene's Cycles settings for all [21:52]; select no extra cameras (each camera = a separate full render) [22:25]; skip "create video from frames" (extra cost) [22:25].
4. OctaRender: cheapest; nodes rented by the hour (e.g. 6× RTX 3090 ≈ $0.5/h shown); requeue red/stuck frames after reading task logs [29:23]; **Stop all sessions** when done or it keeps billing [30:29]. Top-up is crypto only.
5. SuperLuminal: easiest; create a project first; "use scene frame range / image format", include enabled add-ons; download through the add-on's Render Jobs [30:29–34:09].
6. After download: check frame count, first/last frame, a mid frame at 100%, and playback for flicker before converting to ProRes.

**Use when:** the local box can't meet the deadline (client work, long Cycles animations).

**Failure signs:** pink textures (missing files), missing camera shake, wrong camera, cost higher than estimate (extra cameras/scenes), frames with different noise (mixed settings across scenes).
**Cost:** money; GarageFarm > SuperLuminal > OctaRender (per the source; prices change).
**Conflicts with other sources:** none. The "10 h → 20 min" speed claim is unmeasured.
**Log:** 2026-11-07 — Extracted from skool-rr-rendering.
