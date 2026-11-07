# 07 — EEVEE quality: noise & sharpness (Proven)

## Final EEVEE profile (1920×1080, dark glossy product scene)
`scripts/eevee_quality.py` applies it and prints before → after.
| Setting | Value | Why |
|---|---|---|
| Render samples | **256** | 128 left grain in darks / soft shadows |
| Raytracing | on, Screen-Trace, resolution **1:1** | glossy floor/metal |
| Ray denoise | on, **temporal OFF** | temporal accumulation smears texture detail |
| Fast GI | on, resolution **1:1**, rays **8**, precision **1.0**, steps 16 | biggest source of grain in dark areas at defaults (1:2, 2 rays, 0.25) |
| Shadows | rays **3**, steps 16 | soft area-light shadows |
| Motion blur | shutter 0.5, steps **3** | hides the match cut; 1 step looked stuttery |
| Overscan | on, 20% | screen-space edge artifacts |
| DOF | off (unless asked) | noise + "soft" look |
| Compositor | **OIDN Denoise** with Normal + Diffuse Color passes, Prefilter Accurate, HDR | removes residual grain without waxiness at these samples |

Compositor in 5.x: `scene.compositing_node_group` (a CompositorNodeTree node group with a Group Output). Enable View Layer passes `use_pass_normal`, `use_pass_diffuse_color`. Denoise options are **input sockets** (HDR, Prefilter, Quality), not node properties.

## Diagnose noise before fixing
1. Crop the render at 100% in 2–3 regions (hero, floor, background). For dark regions, brighten the crop only for inspection (`eq=brightness=0.12:contrast=2.2:gamma=1.8`).
2. Identify the source:
| Looks like | Real cause | Fix |
|---|---|---|
| Blue/white sparkle on metal or floor | Normal map too strong under hard light + low roughness | Normal 0.15, raise roughness min (0.12→0.18) |
| Glitter on laptop aluminium | Downloaded material normal 1.0 | 0.5 on large parts |
| Grain in dark floor/background | Fast GI / few samples | Fast GI 1:1, 8 rays; samples 256; OIDN |
| Speckled coloured disc on the stand | Strong coloured light on glossy metal | Light linking: remove the stand from that light |
| Everything slightly mushy | DOF + temporal denoise | DOF off, temporal off |
3. **Viewport preview grain ≠ render grain** (viewport has few samples and no compositor denoise). Judge noise only on a rendered frame.

## "Low resolution" that isn't resolution (sharpness)
User said "the resolution looks low" at full 1080p. Real causes: subject small and dark in frame, all lights large and soft, temporal denoise, DOF. Fixes in order:
1. Temporal denoise off, DOF off.
2. Add a **small hard raking light** (0.3 m area, ≈50 W, low angle, opposite the key, linked to the hero only) — micro detail (keys, paper edges, wood grain) appears.
3. Bring detailed materials' normal back to a moderate value (not 0).
4. Only if still soft: frame the subject larger (lens/distance) — ask, it changes the approved angle. 4K was declined by the user (time).

## Over-denoise warning
Too much denoise = waxy paper, melted print, plastic wood. Keep samples high enough that OIDN only polishes.
