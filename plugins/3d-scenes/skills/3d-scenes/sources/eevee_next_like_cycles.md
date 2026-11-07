# How to make EEVEE Next look like Cycles
- url: local file `~/Movies/4K Video Downloader+/How to make EEVEE Next look like Cycles.mp4` (repo id `eevee_next_like_cycles`)
- channel / duration / Blender version: single presenter (channel not identified) / 4:01 / Blender 4.2-era EEVEE Next UI (panel layout seen [00:22]).
- domain(s): rendering | materials | lighting
- trust: **medium**. Quick recipe, one classroom scene, final side-by-side shown [02:51] (EEVEE visibly darker and flatter than Cycles there). Plugs a paid film-emulation node group [01:20] (ignored). Some spoken numbers don't match the panels on screen (says Fast GI rays 8 / steps 12; panel at 03:11 shows 2 / 8), so spoken values are his final choice, frames show an earlier state.

## Techniques (all Extracted)
- **T1 Shadows** [00:02–00:10]: Rays **4**, Steps **9**, Volume Shadows ✔. (eevee_full_course uses Rays 2 / Steps 16 for wall bleed — combine: Steps 12–16 when soft suns enter through windows.)
- **T2 Raytracing** [00:10–00:23]: on; Resolution **1:2** "enough"; Max Roughness **0.5**; Screen Tracing **Precision 1.0**.
- **T3 Fast GI** [00:23–00:28]: Rays **8**, Steps **12**, Precision **1.0**.
- **T4 Volumes** [00:28–00:41]: highest resolution and most steps the GPU allows; **Custom Range** start/end as tight as possible without clipping volumes (precision is spread over that depth range).
- **T5 Overscan 20–40%** [00:41–00:58]: screen-space GI/reflections need pixels beyond the frame edge; costs render time.
- **T6 Performance order** [00:58–01:15]: first lower Raytracing/Fast GI/Volume resolution (least visible), only then shadow/Fast GI rays and steps (more visible).
- **T7 Materials** [01:15–01:56]: bump/displacement can look too strong in EEVEE → reduce. Glass: material Settings › **Transparent Shadows ✔ + Raytraced Transmission ✔**, Thickness **Sphere** (round objects) / **Slab** (flat panes).
- **T8 World** [01:56–02:24]: HDRI washes out interiors → World: Light Path **Is Camera Ray** → Mix Shader Fac (HDRI in the bottom socket) so the world is only seen, not lighting; replace its light with real lamps. (eevee_full_course solves the same leak with a baked Volume probe.)
- **T9 Light artifacts** [02:24–02:37]: Light › Shadow › lower **Resolution Limit** (preferred) or raise Filter. Jitter/overblur made no difference for him.
- **T10 Exposure/strength** [02:37–02:57]: EEVEE renders a little darker than Cycles; he raised the sun and/or exposure to match.
- **T11 Probes** [02:57–03:50]: Volume probe(s) for off-screen bounce (resolution matters most; bake each). Sphere reflection probe (no bake needed); he found **Plane probes "weird", doesn't recommend them** (conflicts with eevee_full_course, which uses them on floors). Box-shaped cubemap can be better for rooms.

## Doubts
- Rays 4 / Fast GI rays 8 roughly doubles shadow/GI cost; not measured.
- "Camera-ray-only world" removes HDRI light completely; physically wrong for rooms where the window really lets sky light in — must be replaced by lights (we already have window area lights).
- Plane probe advice conflicts with eevee_full_course; test on our glossy floor.

## Applied
2026-11-07 — applied to `3D/EEVEE Test/01 - الكرسي - EEVEE.blend` with eevee_full_course; compared against a Cycles frame at the same camera (see experiments log).
