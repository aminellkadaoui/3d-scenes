# Photorealism in Blender: Unlocked
- url: https://youtu.be/R4sOG6OPioc
- channel / duration / Blender version shown: Scenefiller / 4:18 / Blender 3.x–4.0 era (uploaded 2023-11-04)
- domain(s): assets-modeling | materials | environment | lighting
- evidence used: transcript (auto captions converted from VTT) + contact sheet 01 + 7 extracted frames from the 480p mp4 (see §6).
- trust: medium-high. Short, no sponsor, one strong principle ("chaos") with before/after (claimed in narration, not seen by me). Small-channel; techniques are standard environment-art practice.

## 1. Problem it solves
Even with high-res textures, HDRI, imperfections and post, a render "still has that CG look" [R4sOG6OPioc@00:00]. Answer: **chaos** — the real world is random; CG creates perfect lines and straight edges [00:15–01:00].

## 2. Techniques

### T1 — Break perfect geometry with sculpt Grab  `[01:00–01:30]`
- What: subdivide the blocked-out geometry a few times, Sculpt Mode, **Grab** brush at low strength, randomly push/pull vertices; breaks straight edges (walls, door frames, skirting).
- Why: real buildings and objects are never perfectly planar or straight; light grazing reveals waviness.
- Values: deviations of a few mm to ~1 cm on a room-scale set; don't make it look melted.
- Don't use on: precision manufactured hero products (phones, packaging) — there use bevels/surface imperfections instead.
- Status: Extracted

### T2 — Slight random rotations  `[01:30]`
- Rotate objects a few degrees (furniture, frames, props). Use F3 ▸ **Randomize Transform** (rotation 1–5°, small location jitter).
- Status: Extracted

### T3 — Real-photo image textures (non-seamless) instead of clean PBR  `[01:45–02:15]`
- A real photograph snapshots grime, leakage and imperfections; replacing a too-clean seamless plaster with a photo texture breaks perfection; align UVs so it doesn't tile [02:00].
- Don't when: photo has strong directional light baked in.
- Status: Extracted

### T4 — Photographed debris overlay with alpha  `[02:15–03:00]`
- Photograph a dirty dark doormat/surface, crush blacks to make an alpha matte, map on a plane: colour → Base Color, matte → **Alpha** (narration says "transparency socket"; frames show Image → RGB Curves crush → Principled Alpha, colour via Hue/Sat/Value [02:42]); duplicate planes over the floor, **Randomize Transform** Z rotation to avoid repetition.
- Blender 5.2 notes: EEVEE 5.x handles alpha via the Alpha socket without blend-mode setup (Render Method Dithered by default); shadows from alpha planes are usually fine.
- Status: Extracted

### T5 — Storytelling clutter off the walkable path  `[03:00–03:30]`
- Think how someone inhabits the space: thrown shirts, plastic, bottles, the broken stool, old backpacks, shoes — at the sides, not where characters walk. "We want our audience to believe somebody lives here" [03:15]. Takes longest but matters most.
- Status: Extracted

### T6 — Occluders/gobos to sculpt light  `[03:30–04:00]`
- Objects in front of light source and gobo planes with cut-outs for interesting shadows and to direct attention (lighting.md).
- Status: Extracted

## 3. Claims I doubt or must test
- Few. "One rule" framing oversimplifies — chaos without control (random clutter everywhere) becomes noise; composition still needs hierarchy.

## 4. Anti-AI-slop lessons
- The core anti-slop principle: **controlled chaos**. Perfect straight edges, perfectly aligned objects, empty clean floors = CG.
- Story-driven props > random props.

## 5. Candidate isolated test
Simple room (walls, floor, door frame, chair, shelf). A: clean blockout with PBR. B: + grab-sculpt waviness + 1–3° rotations. C: + photo overlays + 6–10 story props at edges. Blind CG/real ranking + time spent.

## 6. Visual verification (frames viewed)
Frames viewed: contact sheet 01, plus extracted frames below. UI is **Blender 3.x** (3.6-era Principled with Subsurface Random Walk / Specular / Clearcoat, view transform **Filmic**) — older than the 5.2 target.
- [00:05] (cropped from a vertical layout) final render: school desk + chair against a beige wall, hard warm sun slash across wall and floor, rug, framed prints. Clean, believable, nicely lit; a modest interior vignette rather than a dense environment.
- [01:20] Sculpt Mode, **Grab** brush, Radius 50 px, strength being typed (≈0.4); the wall plane "beige_wall_001" uses a Hue/Saturation/Value into Base Color. Important context **not in the transcript (added from frames):** the scene uses the **MattePainter add-on** with real photo layers (IMG_4025.JPG, IMG_4021.JPG, a fabric pattern) — i.e. parts of the set are **camera-projected photographs**, which explains much of the realism.
- [02:35] The photographed doormat debris image (black background, white fibres/specks) — confirms T4 source material.
- [02:42] **Confirms T4 node chain:** Image (IMG_3722_edited.JPG, sRGB) → **RGB Curves** (contrast crush) → Hue/Saturation/Value → Base Color, and the Curves output also → Principled **Alpha**. Applied on duplicated planes over the desk/floor area.
- [02:50] B-roll photo (wooden school chair on red herringbone brick) used as a "real-world chaos" reference — not a render.
- [03:50] Gobo segment is a **clip from another channel ("Blender Secrets – More Realistic Eevee Renders with Gobos")** — spot light through a leafy gobo image plane; the author does not demonstrate it in his own scene.
- [04:10] "Before" version: same composition, cleaner floor and fewer props; at 480p the before/after difference is **subtle** (mainly floor debris and small props), not dramatic.
- Final quality judgement: professional-looking for a simple vignette, mostly thanks to strong single-source sunlight and photo-projected textures; the "chaos" additions are small. Techniques are valid, but the visible improvement attributable to them is modest. Trust medium-high for principles, low for "this alone fixes CG look".
