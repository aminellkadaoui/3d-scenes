---
name: 3d-scenes
description: Lead any Blender 3D scene/shot from idea to delivered render so it looks professional and cinematic (not AI slop), fast, using a deep knowledge base - art direction, composition, camera & lens, assets, PBR materials, motivated lighting, light linking ("track matte" lighting), environment & atmosphere, animation (turntable, match cut, AE-style speed graphs, camera rigs), EEVEE/Cycles rendering, noise & sharpness fixes, color management, compositing, QA - built from 30 analysed tutorials, 61 technique cards and field-tested production recipes. Use whenever the user wants to build, light, texture, animate, fix or render a Blender scene - "سوي مشهد", "مشهد 3D", "سوي لي سين في بلندر", "خل المشهد احترافي", "المشهد شكله AI", "حسّن الإضاءة/الخامات/الكمرة", "سوي له مات", "light sweep", "متش كت", "جراف الجبل", "النويز كثير", "الجودة ضعيفة", "الأرضية تعكس", "رندر", "cinematic shot", "product render", "turntable", "make this look real/premium" - even if they don't say "skill".
---

# 3D Scenes — the director

Everything lives next to this file. Two layers of knowledge:

| Layer | Folder | Trust | Use it for |
|---|---|---|---|
| **Proven recipes** | `references/` (00–11), `case-studies/`, `lessons/LESSONS.md` | Applied in delivered shots, with numbers | First choice. Copy the values. |
| **Knowledge library** | `knowledge/` (14 pillars), `techniques/` (61 cards), `sources/` (30 tutorial analyses), `looks/` | `Extracted` from tutorials (YouTube + Skool Render Room), cited `[id@mm:ss]`; a few cards `Reproduced`/`Validated` | Principles, starting values, options, what to avoid. Verify on a representative frame before relying on it. |

Read only what the current stage needs. Reply in the user's language (often Gulf Arabic; translate editor words with `references/00-vocabulary.md`).

## The core idea
Slop = every decision left at its default or made without intent. The cure is not "more effects": **replace every default with a decision, and make every decision serve one shot-level idea.** Fix in order of influence: Concept → Composition/Camera → Lighting → Environment → Assets → Materials → Animation → Render → Grade. A perfect material can't save a frame with no idea and a bad camera.

Speed comes from a **short feedback loop** (`references/11-feedback-loop.md`): start from an approved scene, one change per round, look through the camera, report before → after, diagnose before fixing.

## Workflow (gate before moving on)

| # | Stage | Proven recipe | Library | Exit check |
|---|---|---|---|---|
| 0 | Setup | `references/01-project-setup.md` | `knowledge/production-pipeline.md` | Working on a copy; original untouched |
| 1 | Brief | `references/02-brief-and-references.md` | `knowledge/art-direction.md`, `templates/creative-brief.yaml`, `looks/` | Purpose, one hero, aspect/fps/duration, refs labelled by job, measured tone |
| 2 | Shot plan + camera | `references/06-camera-and-motion.md` | `knowledge/composition.md`, `knowledge/camera-lenses.md`, `techniques/camera-*`, `techniques/composition-*` | Lens/height/move per shot with a reason |
| 3 | Blockout | — | `knowledge/composition.md` | Grayscale/thumbnail test: hero reads, depth layers, space for titles |
| 4 | Assets | `references/03-assets.md` | `knowledge/assets-modeling.md`, `techniques/assets-*` | Real scale, grounded, no intersections, no primitive props |
| 5 | Materials | `references/04-materials.md` | `knowledge/materials-pbr.md`, `techniques/materials-*` | Plausible albedo, varied roughness, imperfection on hero, colour spaces right |
| 6 | Lighting & look-dev | `references/05-lighting-light-linking.md` | `knowledge/lighting.md`, `knowledge/environment-atmosphere.md`, `knowledge/color-management.md`, `techniques/lighting-*`, `techniques/environment-*`, `techniques/color-*` | Motivated key/fill/rim, hero separated, light linking per group, no clipping |
| 7 | Animation | `references/06-camera-and-motion.md` | `knowledge/animation.md`, `techniques/animation-*` | Speed table checked, no dead stops, motion serves the edit |
| 8 | Render quality | `references/07-eevee-quality-noise.md` | `knowledge/rendering.md`, `techniques/rendering-*` | No grain/sparkle at 100% crop |
| 9 | Compositing & grade | — | `knowledge/compositing.md`, `techniques/compositing-*` | Subtle, motivated, adjustable |
| 10 | QA | skill `3d-scenes-qa` | `knowledge/ai-slop-diagnosis.md`, `knowledge/photorealism.md` | No domain ≤2, total ≥40/50 |
| 11 | Render & delivery | `references/08-render-delivery.md` | `knowledge/rendering.md` §7–8 | 1 measured frame → estimate → full render → PNG + ProRes |
| 12 | Retro | skill `3d-scenes-retro` | — | Lessons written, repo published |

Problems → `references/09-troubleshooting.md` first, then the matching `knowledge/` file. Blender 5.x Python traps → `references/10-blender5-api.md`. Ready code → `scripts/` (CONFIG block at the top of each).

## How to search the library fast
- Find cards: `ls techniques/ | grep <domain>` (domains: animation, assets, camera, color, compositing, composition, environment, lighting, materials, rendering).
- Find a topic across everything: `grep -ril "<keyword>" knowledge techniques sources references`.
- Each card: Principle → Steps (starting values) → Use when / Avoid when → Failure signs → Cost → Conflicts → Test. Respect "Avoid when".
- When sources disagree, the card records both; choose by the stated condition, and say which you chose.
- Prefer `Validated`/`Proven` over `Extracted`. Using an `Extracted` value: check it on a representative frame.

## Non-negotiables per pillar (details in `knowledge/`)
- **Concept & composition** — one hero readable in 3 s; not dead-centre by accident (unless symmetric product); FG/MG/BG; value contrast puts the eye on the hero (grayscale + squint + 160 px thumbnail); negative space for captions.
- **Camera** — never the default 50 mm aimed at origin. Position sets perspective, focal length crops. Wide 24–35, medium 35–50, product hero 85–105, telephoto 135+. Realistic f-stop at real scale (or DOF off). 9:16 needs its own camera. Motion blur shutter 0.5.
- **Assets** — real metres, scale applied; bevel hard edges; silhouette detail big/medium/small; vary repeats (1–5°); objects touch the ground. Ready-made assets only — never primitives for props/characters; say at once if something is missing.
- **Materials** — albedo never pure black/white, lower saturation than you think; metallic 0 or 1; roughness always varied in a narrow band; base → macro variation → dirt → wear → story detail; colour maps sRGB, data maps Non-Color.
- **Lighting** — one dominant motivated source per area; key 30–60° off axis, 20–45° up; keep shadows, fill don't erase; separate the hero (rim/background contrast); glossy/glass get designed reflections (gradient cards); each light one job — enforce with **light linking**; exposure in Color Management, not by cranking watts.
- **Environment** — never a flat grey/black void: designed dark backdrop, cyc, HDRI or set; scale cues; atmosphere scaled to scene units.
- **Animation** — **Default speed graph for EVERY move = "mountain" (جراف الجبل): AE Speed In 75% / Out 75%** — flat tangents, FREE handles at 0.75 × segment on both keys (`scripts/mountain_ease.py`; HTML/JS `cubic-bezier(0.75,0,0.25,1)`). Use it unless the user asks otherwise; exceptions: holds, constant drift, frame tracking (linear). Auto-Clamped stops at every key = robotic. Choose handles per key; asymmetric ease for reveals; camera on a rig; slow drift instead of dead stops. **Turntable + match cut = two layers:** constant linear drift (parent, never stops) + mountain spin (child) peaking on the cut; a camera move that crosses the cut is symmetric around it so its peak lands there too. Camera angle follows the hero: one hand-framed station per hero state (`techniques/camera-hero-framed-stations.md`). Product in a black void → `techniques/environment-endless-floor-void.md` + `scripts/endless_floor.py` (no horizon edge, soft diffuse floor light, roughness like the hero top).
- **Render & colour** — AgX (Khronos PBR Neutral for exact brand colours); preview → look-dev → final profiles; denoise appropriately; deliver PNG16/ProRes, EXR for comp. **Render looks soft at the right resolution** → `techniques/rendering-soft-render-checklist.md`: check the frame size first (a cropped Render Region gave 1079 lines), mute Denoise on clean EEVEE frames, filter 1.0, motion blur only around the fast move, screen/UI textures `Closest`, anisotropic 16× on the render machine. Measure one frame; no Sharpen node unless asked.
- **Compositing** — glare, vignette, grain, lens effects: each needs a reason, starts subtle, stays adjustable.

## Engine choice
Default EEVEE (fast, proven here with the profile in `references/07-eevee-quality-noise.md`). Use Cycles when the shot needs physically correct glass/refraction, interior GI through windows, or Cycles-only features (`knowledge/rendering.md` §1 decision table). Don't switch silently.

## Iteration discipline
Issue → root cause → smallest change → cheapest validation → compare → keep/revert. Log with `templates/qa-issue.yaml`. After 2–3 failed attempts: re-diagnose from a higher layer (composition problems often look like lighting problems), check `techniques/`, or ask the user.

## Ask the user only for
Art direction or story changes, swapping a hero asset, changing an angle they approved, paid assets/renders. Fix technical issues yourself.

## Blender MCP practice
`get_addon_status` + `get_scene_info` first. Find shader nodes by `type`. Read enum identifiers, don't hardcode. Size imported assets from bounding boxes / vertices. `look` with small `max_size` often; `look` can't show final noise or all screen-space reflections — render a frame for those. Run the audit in `knowledge/ai-slop-diagnosis.md` §5 after major stages. Blender 5.x breaks old tutorial code (compositor node groups, slotted actions, EEVEE Next names) — `references/10-blender5-api.md`.

## Rules
No auto-render, no auto-save (saving a copy for a requested render is fine). Never delete user objects — hide them in `_HIDDEN_*` collections. Full-quality deliveries only. Measure render time on one frame before promising a time.

## Screen effects
If asked for a screen effect (تأثير السكرين، LED، RGB pixels، شاشة واقعية): ask which pixel shape — **stripes** (approved default, RGB bars like an LCD), **dots**, **circles** or **squares** (LED style) — then build it with `scripts/screen_fx.py` as in `techniques/materials-screen-display-effects.md`: test on a scene duplicate, one graded frame for approval, then apply to all screen materials. Never change the original scene before approval.

## Growing the system
- New tutorial → skill `3d-scenes-learn-tutorial` (adds `sources/` + `techniques/` + updates `knowledge/`).
- Test a card in isolation → skill `3d-scenes-validate` (promotes Extracted → Reproduced → Validated).
- After every project → skill `3d-scenes-retro` (lessons, case study, publish).
