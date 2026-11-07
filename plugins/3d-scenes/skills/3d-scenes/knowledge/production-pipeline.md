# Production Pipeline — 15 stages with quality gates (agent edition)

> Status: Knowledge (synthesis of studio pipeline practice adapted for Claude Code + Blender MCP, Blender 5.x).
> Templates used: `templates/creative-brief.yaml`, `templates/qa-issue.yaml`. Related: `ai-slop-diagnosis.md` (rubric §4, audit §5), `art-direction.md` (spec), `environment-atmosphere.md`.

Why a pipeline: slop is mostly **skipped decisions**. Studios gate each stage so expensive work (materials, lighting, rendering) is never done on top of an unapproved cheap decision (concept, camera, blockout). The agent equivalent: **never polish what hasn't passed its gate**, and **render the cheapest image that can answer the gate's question**.

---

## 0. Overview

| # | Stage | Gate question | Gate render / artifact |
|---|---|---|---|
| 1 | Creative brief | Do we know purpose, audience beat, deliverable? | `brief.yaml` |
| 2 | Reference | Do we have a master ref + role-tagged refs? | `refs.md` + images |
| 3 | Art direction | Is the look specified numerically? | `art-spec.md` |
| 4 | Shot planning | Is every shot's camera/framing/timing defined? | Shot list + storyboard frames (sketch or blockout) |
| 5 | Asset planning | Do we know each asset's source, realism level, detail level? | Asset list |
| 6 | Blockout | Do composition, scale and camera work in grey? | Clay render (viewport/Workbench or EEVEE, 25–50%) |
| 7 | Asset assembly | Are final-shape assets in place, scaled, grounded? | Clay render + audit report |
| 8 | Materials | Do surfaces read correctly in neutral light? | Material lookdev frames (neutral HDRI) |
| 9 | Lighting / lookdev | Does the frame hit the spec's mood and value structure? | Representative frames (low-res, then 100%) |
| 10 | Animation | Does motion read and time to the edit? | Playblast (viewport render) |
| 11 | Preview validation | Does the whole shot pass rubric at preview quality? | Low-sample sequence or key frames |
| 12 | Rendering | Is the final output clean and complete? | Final frames (EXR/PNG sequence) |
| 13 | Compositing | Is finishing consistent with spec? | Comp'd key frames |
| 14 | Final QA | Does it pass rubric ≥ target and technical checks? | QA report |
| 15 | Delivery | Is the right file in the right place in the right format? | Delivered files + manifest |

---

## 1. Stage details: entry gate → work → exit gate

### 1. Creative brief
- **Entry**: user request.
- **Work**: fill `templates/creative-brief.yaml`: purpose, VSL beat, duration, aspect, fps, style, mood, *visual_priority* (the ONE thing), constraints, render budget. Ask the user only for what cannot be inferred (aspect/duration/brand assets).
- **Exit gate**: purpose and visual priority each fit in one sentence; aspect, fps, duration, and deadline/render budget known. No Blender work before this.

### 2. Reference
- **Entry**: approved brief.
- **Work**: collect 6–12 refs (master + lighting + composition + material + grade + 1–2 anti-refs); CTLT each; classify traits transferable/scene-specific/unsuitable (`art-direction.md` §6). Save to `projects/<p>/refs/` and `refs.md`. Check `<project>/refs/positive` and `<project>/refs/negative` in ROOT for reusable examples.
- **Exit gate**: one master reference chosen; every ref has a role and ≥ 1 transferable rule written.

### 3. Art direction
- **Entry**: refs approved (or user said "your call").
- **Work**: write `art-spec.md` from the template (`art-direction.md` §8): style, realism level, palette hexes with 60/30/10 roles, value key, camera/lighting/texture parameters, forbidden list, rubric targets.
- **Exit gate**: every vague adjective converted to a number or a checkable statement; user approval for anything client-facing.

### 4. Shot planning
- **Entry**: art spec.
- **Work**: shot list (id, duration, beat, framing, lens, move, focus, transition in/out, caption-safe area). For a single still, this is the framing decision. Optional storyboard: quick blockout frames.
- **Exit gate**: every shot has lens, height, framing, move, duration; total duration matches the edit.

### 5. Asset planning
- **Entry**: shot list.
- **Work**: list every visible asset with: role (hero/secondary/dressing/BG), source (library, `search_assets`/`import_asset`, `generate_3d`, model, procedural), realism level, detail level by camera distance, real-world dimensions, material notes. Detail budget goes to what the camera sees closest and longest.
- **Exit gate**: no asset is "a primitive for now" unless it's architecture or will be replaced at stage 7 (mark it `placeholder`).

### 6. Blockout
- **Entry**: asset plan, shot list.
- **Work**: simple proxy geometry **at real scale**; set camera(s) per shot list; rough key light direction; world placeholder; tag hero (`obj["role"]="hero"`). Set scene units (metres, scale 1). Set output resolution/aspect/fps now.
- **Gate render**: **clay render** — single neutral material (light grey ~0.5–0.6, roughness 0.6), one soft key + dim environment, EEVEE or Workbench, 25–50% resolution. For animation: viewport playblast.
- **Exit gate**: composition (rubric domain 2) and camera (3) ≥ 3 in clay; scale cues correct; hero readable in silhouette and in a 10% thumbnail; user approval of framing for client work.

### 7. Asset assembly
- **Entry**: approved blockout.
- **Work**: replace proxies with final assets; apply scale; bevels; ground snapping; variation on repeats; set dressing (`environment-atmosphere.md` §2).
- **Gate render**: clay render from the shot camera(s) + run the bpy audit (`ai-slop-diagnosis.md` §5).
- **Exit gate**: audit has no FAIL; Assets domain ≥ 3 (≥ 4 for hero); no intersections/floating; silhouette detail hierarchy visible in clay.

### 8. Materials
- **Entry**: assets locked.
- **Work**: PBR materials per `materials-pbr.md`; imperfection layers on hero; palette roles applied (accent only on hero).
- **Gate render**: **material lookdev** under a neutral HDRI (overcast/studio), shot camera, 50% res, low samples + denoise; plus a close-up of the hero. Neutral light isolates material errors from lighting errors.
- **Exit gate**: Materials domain ≥ 3 (hero ≥ 4); no default materials; roughness varies; albedo within limits.

### 9. Lighting / lookdev
- **Entry**: materials approved.
- **Work**: lighting per spec (`lighting.md`); world/HDRI; atmosphere (`environment-atmosphere.md` §6); color management (AgX + Look) per spec; exposure.
- **Gate render**: **representative frames** — for a sequence: first, hero moment, last, and any frame with extreme camera position. First at 25–50% / low samples; when it looks right, one frame at 100% for detail and noise.
- **Exit gate**: Lighting ≥ 4, Color ≥ 3, Environment ≥ 3; value check in greyscale passes; no clipped non-specular areas.

### 10. Animation
- **Entry**: look approved on stills (animation can start in parallel after stage 6 for blocking, but finals after 9).
- **Work**: camera and object animation per shot list; easing; staggered timing; secondary motion; motion blur on (`animation.md`).
- **Gate render**: **playblast** (viewport render animation, Solid or Material Preview, 50% res) — fast, honest about timing.
- **Exit gate**: Motion ≥ 3; timing matches edit duration; no pops, intersections, or camera clipping across the full range.

### 11. Preview validation
- **Entry**: animation approved.
- **Work**: render a low-cost preview of the final look: either every Nth frame (e.g. every 6th) at 50% with low samples + denoise, or full sequence in EEVEE if final is Cycles (accepting lighting differences).
- **Exit gate**: rubric total ≥ target on 3 representative frames; no temporal problems (flicker, popping, noise crawl) in the sequence; estimated final render time fits budget (time a single final-quality frame × frame count).

### 12. Rendering
- **Entry**: validated preview + render-time estimate approved.
- **Work**: final settings (`rendering.md`): samples/noise threshold, denoiser, motion blur, passes needed for comp (Mist, Cryptomatte, AO/Denoising data as needed), EXR multilayer for comp or PNG 16-bit; frame-sequence output (never a single video file from Blender for long renders — a crash loses everything). Output path inside `projects/<p>/renders/<shot>/v###/`.
- **Exit gate**: all frames present (count check), no black/corrupt frames (file-size outliers), spot-check 3 frames at 100%.

### 13. Compositing
- **Entry**: complete frames.
- **Work**: finishing per spec (`compositing.md`): exposure/curves, mist-based depth grading, glare, vignette, grain, lens distortion/CA if allowed. Blender 5.x compositor uses node groups — verify API at runtime. Keep comp subtle; much grading may happen in the user's editor (Premiere/AE) — deliver a clean, flexible image if so.
- **Exit gate**: Finishing ≥ 3; consistent across shots (compare side by side).

### 14. Final QA
- **Entry**: comp'd output.
- **Work**: score rubric on 3+ frames; check spec line-by-line; technical checks (resolution, fps, frame count, color space of output, file naming, alpha if required); log issues with `templates/qa-issue.yaml`.
- **Exit gate**: all domains ≥ 3, total ≥ 40 (or user-approved exception); no open blocker/high issues.

### 15. Delivery
- **Entry**: QA passed.
- **Work**: export in requested format (e.g. ProRes 422 HQ / H.264 high bitrate / PNG/EXR sequence), correct color space (Rec.709 sRGB for most editing; note AgX output is display-referred), naming convention, manifest (shot id, version, frame range, settings, notes), save the approved `.blend` as `_APPROVED`.
- **Exit gate**: user confirms receipt/import works in their NLE.

---

## 2. What to render at each gate (cost ladder)

Cheapest first; only climb when the cheaper image can't answer the question.

| Level | Image | Typical cost | Answers |
|---|---|---|---|
| 0 | `look` tool viewport capture / `get_scene_info` | seconds | Is the object there, roughly where? |
| 1 | Workbench/Solid viewport render, 25–50% | seconds | Composition, silhouette, scale, timing (playblast) |
| 2 | Clay render (EEVEE, single material) 50% | seconds | Form, bevels, contact shadows, light direction |
| 3 | EEVEE material preview 50% | seconds–tens | Materials and palette roughly |
| 4 | Cycles 25–50%, 16–64 samples + denoise | tens of seconds | Lighting mood, GI, volumes (approx.) |
| 5 | Cycles 100%, final samples, single frame | minutes | Noise, fine detail, final approval |
| 6 | Full sequence | hours | Delivery only |

---

## 3. Checkpoint & versioning policy

- **Folder layout per project**: `projects/<project>/{brief.yaml, refs/, art-spec.md, shots.md, blend/, renders/, comp/, qa/, delivery/, log.md}`.
- **Save a new version at every gate exit**, never overwrite: `blend/<project>_<shot>_s<stage>_v###.blend` (e.g. `vsl01_sh03_s06_v002.blend`). Use `bpy.ops.wm.save_as_mainfile(filepath=..., copy=True)` to write a checkpoint without changing the working file's path, or save-as to move forward.
- **Approved versions are read-only by convention**: append `_APPROVED` and never write to them again; branch from them (`..._v004_from_APPROVED_v003`).
- **Before any destructive or bulk script** (deleting objects, applying modifiers, joining, bulk material replacement): save a checkpoint first.
- **Renders are versioned with the .blend that produced them** (`renders/<shot>/v###/`), plus a `settings.txt` (engine, samples, resolution, view transform, time per frame).
- **Log** every gate decision and every rubric score in `log.md` (date, version, scores, changes, next step).
- Never delete old versions or renders; archive if space is an issue (and only with user consent).

---

## 4. Iteration policy

Each iteration loop:
1. **Observe**: render the cheapest image that shows the problem; score the affected domain.
2. **Hypothesis**: one sentence — "The hero doesn't separate because BG value equals hero value; lowering world strength 40% should create ~1.5 stop separation."
3. **Smallest change**: change one variable (or one tightly coupled set). Record old → new values.
4. **Compare**: same camera, same frame, same render settings; side-by-side before/after (`look` both images or composite them). Re-score.
5. **Decide**: keep, revert, or refine.

**Rules**
- After **2–3 failed attempts** on the same issue, stop tweaking and **re-diagnose** one level up the influence order (concept → composition/camera → lighting → environment → assets → materials → render → grade). A "materials problem" that won't fix is often a lighting problem; a lighting problem that won't fix is often a composition problem. Track attempts in the QA issue (`attempts` field).
- Don't change multiple domains at once unless a gate requires it — you lose attribution.
- Prefer reversible changes (modifiers, node values, light power) over destructive ones.
- If the fix requires the user's taste (e.g. palette direction), present 2–3 options as low-res frames rather than iterating blindly.

---

## 5. Token & render efficiency rules

- Query scene data with **targeted Python** that returns compact text (counts, names, flagged items) — not full `get_scene_info` dumps after the first one.
- Use the `look` tool with a **small max_size** (e.g. 512–768 px) for routine checks; full size only for detail/noise checks. Images stay in context — fewer, smaller, purposeful images.
- **Batch edits** into one `execute_blender_code` call per logical step; return a summary string, not verbose logs.
- Render low-res (25–50%), low samples, denoised, single frames for decisions; use render border/region (`render.use_border`) to check a detail region.
- Use **EEVEE for iteration** and Cycles only for gates that need GI/volume truth; or Cycles with adaptive sampling + low max samples + denoise.
- Cache what doesn't change: bake simulations, keep heavy volumes hidden (`hide_render`/disabled in viewport) while working on other stages.
- Time one final-quality frame before committing to a sequence; estimate total = time × frames × 1.1.
- Reuse validated technique cards from `techniques/` rather than re-deriving setups.
- Don't re-read large knowledge files every turn; quote the specific section you need.

---

## 6. Blender MCP practical notes for agents

**Start of session**
- `get_addon_status` (Blender version, available libraries/generators) then `get_scene_info` once.
- Confirm units/scene scale, render engine, resolution, fps, view transform before building.

**Writing robust bpy**
- **Shader nodes: find by type, never by name** (names are localized and user-renamable):
  `bsdf = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')`; output: `n.type == 'OUTPUT_MATERIAL'`; world background: `'BACKGROUND'`.
- **Read enum identifiers, don't hardcode**:
  `[i.identifier for i in bpy.types.RenderSettings.bl_rna.properties['file_format'].enum_items]`; same for `view_transform` (`scene.view_settings.bl_rna.properties['view_transform'].enum_items` — the list depends on the OCIO config), Sky types, phase functions, etc.
- **Render engine**: `scene.render.engine` may under-report; read current value, assign new one inside `try/except TypeError` — the error message lists valid identifiers (EEVEE's identifier changed across 4.x/5.x).
- **Material colors** go on shader node inputs; `material.diffuse_color` only affects the viewport.
- **Input sockets**: access by name works for the Principled BSDF (`'Base Color'`, `'Roughness'`, `'Metallic'`, `'Emission Color'`, `'Emission Strength'`), but if a KeyError occurs, list `[s.name for s in node.inputs]` and adapt — names changed in 4.0.
- **Apply scale** after creating/importing/resizing meshes: select the object, make it active, `bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)`; operators need correct context — alternatively apply via data: `o.data.transform(Matrix.Diagonal((*o.scale, 1))); o.scale = (1,1,1)` (not for shared meshes/instances).
- **Imported/generated models arrive at arbitrary scale**: use the reported `world_bounding_box` to scale to real dimensions, then snap bottom to ground.
- **Avoid `bpy.ops` where data API works** (more reliable, no context errors): `bpy.data.objects.new`, `obj.modifiers.new(type='BEVEL')`, `mat.node_tree.nodes.new('ShaderNodeTexNoise')`.
- **Use evaluated depsgraph** for bounding boxes/meshes after modifiers: `obj.evaluated_get(depsgraph)`.
- **Tag roles** with custom properties (`obj["role"] = "hero" | "dressing" | "ground" | "bg"`) so audits and QA scripts can find them.
- **Names**: give meaningful names (`Hero_Wallet`, `Key_Softbox`, `Set_TableTop`) — `Cube.004` is both slop and untraceable.
- **Idempotent scripts**: check if an object/material exists before creating; re-running a step shouldn't duplicate the scene.
- **Collections**: organize as `CAM`, `LGT`, `HERO`, `SET`, `DRESS`, `FX`, `REF` (hidden) — makes visibility toggling and render layers easy.

**Seeing the work**
- Use `look` after every meaningful change at small size; compare to the master reference.
- For gate renders, render to file (`scene.render.filepath` under `projects/<p>/renders/...`) and `look`/Read the file; keep the image for before/after comparisons.
- Check from the **shot camera**, not the viewport perspective.

**Assets**
- `search_assets` / `import_asset` (Poly Haven, Sketchfab, Poly Pizza) before modeling from primitives; check license and realism level match.
- `generate_3d` = one object (1–3 min, may cost a credit — ask the user before spending credits), never a whole scene or ground; scale and ground it afterwards.

**Safety**
- Checkpoint before destructive operations; never delete user data or files; don't overwrite `_APPROVED` files.
- Keep long-running renders as frame sequences; report progress rather than blocking.

---

## 7. Gate checklist (copy into `log.md` per shot)

```
[ ] 1 Brief            purpose / visual priority / aspect / fps / duration / budget
[ ] 2 Reference        master + roles + transferable rules
[ ] 3 Art spec         numeric, forbidden list, rubric targets
[ ] 4 Shot plan        lens / height / framing / move / duration
[ ] 5 Asset plan       source / realism / dims per asset
[ ] 6 Blockout         clay: comp ≥3, camera ≥3, scale OK        -> save s06_v###
[ ] 7 Assembly         audit no FAIL, assets ≥3 (hero ≥4)        -> save s07_v###
[ ] 8 Materials        neutral HDRI lookdev, materials ≥3 (hero ≥4)
[ ] 9 Lighting         lighting ≥4, color ≥3, env ≥3, B/W value check
[ ] 10 Animation       playblast, motion ≥3, timing matches edit
[ ] 11 Preview         rubric ≥ target on 3 frames, time estimate OK
[ ] 12 Render          frame count / corrupt check / 3 spot checks
[ ] 13 Comp            finishing ≥3, cross-shot consistency
[ ] 14 Final QA        all ≥3, total ≥40, no open blockers
[ ] 15 Delivery        format / color space / naming / manifest / _APPROVED saved
```

---

## 8. Sources consulted

- Blender MCP server instructions (shader lookup by type, enum reading, engine assignment, material colors on nodes, asset scaling) — provided with the MCP integration.
- 3D AI Studio — "Blender MCP honest guide" (agent limits: context degradation in long sessions, risk of wrong-selection edits → save copies): https://www.3daistudio.com/3d-generator-ai-comparison-alternatives-guide/blender-mcp
- arXiv 2601.05016 — Planner–Actor–Critic framework for agent-augmented 3D modeling (critic loops improve generation quality): https://arxiv.org/html/2601.05016v1
- Archvis Insider — "Avoid These 5 CGI Mistakes" (refine geometry early, planned lighting, post-processing): https://archvisinsider.substack.com/p/avoid-these-5-cgi-mistakes-and-improve
- Blender Manual source — Render passes (Mist, Cryptomatte): https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/layers/passes.rst
- Blender 5.0 Cycles release notes: https://developer.blender.org/docs/release_notes/5.0/cycles/
- Stage/gate structure, cost ladder, versioning and iteration policies are synthesized from standard VFX/animation studio practice (blockout → layout → lookdev → lighting → comp with dailies/approvals) and the project's own templates.
