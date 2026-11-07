# Smooth camera animations in Blender (product showcase, multi-camera)
- url: https://youtu.be/dFK3C83k4Wo
- channel / duration / Blender version shown: Blender To Browser / ~11:45 (transcript ends [11:30]) / **Blender 5.0.0** (title bar, corrected from frames); scene 25 fps, 1080×1920 vertical, Cycles GPU
- domain(s): camera, animation, (minor) lighting, environment (cyclorama backdrop)
- evidence used: transcript + 3 contact sheets + 8 extracted frames (see §6).
- trust: medium-high for workflow (structured, numeric, repeatable "notes" system [04:15]–[04:45]); low for lighting ("nothing fancy" [10:45]). Mentions a free add-on (Relative Ease) [06:00]; not required.

## 1. Problem it solves
Product showcase animations made by moving/rotating the camera directly are jerky, inconsistent between shots and hard to edit. The video builds a repeatable rig + timing system that produces smooth orbiting shots that cut together seamlessly.

## 2. Techniques

### T1 — Cyclorama/infinity backdrop larger than the camera path `[00:15]–[00:45]`
- What: Plane, extrude back edge up, Bevel the corner; scale it large "so it covers the whole scene because when we move the camera around, it might go out of the frame" [00:30].
- Why: no visible horizon line; continuous gradient behind the product. Check every frame of an orbit for backdrop edges.
- Status: Extracted

### T2 — Telephoto focal length for product hero `[00:45]–[01:00]`
- What: camera in front of product, product centered, Focal Length 90 mm ("use whatever works for you").
- Why: long lens = less perspective distortion of the product, flatter, more "catalog/premium" rendering, background shows less area (easier to keep clean). Requires the camera to be far away (perspective is set by distance).
- Don't use when: you need environment context or immersion (use 24–35 mm).
- Status: Extracted

### T3 — Naming + one collection per shot `[01:00]–[01:15]`, `[04:00]`
- Camera "shot one", Empty, both in collection "shot one". Duplicate for each shot. Essential for agent-driven scenes (MCP scripts find objects by name).
- Status: Extracted

### T4 — Orbit rig: camera parented to an Empty at the subject `[01:30]–[01:45]`
- What: Add Empty at the area of interest, parent camera to it (`Ctrl+P` ▸ Object), animate the Empty's Z rotation for orbit, and the camera's local location (pull back/push in) for dolly. "I'm not going to rotate the camera directly" [01:30].
- Why: separates orbit (Empty rotation) from dolly (camera local Y/Z) → each channel has one clean F-curve; orbit is a perfect circle around the subject; moving the Empty re-targets the whole shot [09:30–09:45].
- Status: Extracted

### T5 — Entry (push-in) + exit (rotation) structure `[01:45]–[02:45]`
- What: Key end position at frame ~40–50, go to frame 1, pull camera back, key → slow push-in reveal. Exit: rotation key on Empty at frame 40, +30° at frame 55 (15 frames) — later revised to 40° over 20 frames [03:30–03:45].
- Why: every shot has an arrival and a departure; the exit motion is what the next shot will continue.
- Status: Extracted

### T6 — Lock unused channels, Normalize, scale handles by eye `[03:00]–[03:30]`
- What: In Graph Editor lock/hide X and Y rotation channels; Normalize + `Home`; select the two keys' handles and `S` `X` to scale them; play and adjust. "if you scale them too much, the motion becomes too fast" [03:15] (longer handles at both ends compress the middle → higher peak speed).
- Status: Extracted

### T7 — Write down a motion spec and reuse it `[04:15]–[04:45]`, `[06:30]`
- What: Notes: transition rotation = 40°, transition duration = 20 frames, transition starts 40 frames into the shot, shot length = 50 frames between camera switches [08:30].
- Why: consistent rhythm across shots = edit feels designed; values become a style guide for the whole video.
- Status: Extracted

### T8 — Cut at the moment of peak speed with camera markers `[04:45]–[05:15]`
- What: Put the playhead mid-transition (fastest point, e.g. frame 50), select the next camera, `Ctrl+B` in the Timeline (Marker ▸ Bind Camera to Markers) to switch active camera there. Bind shot 1 at frame 1.
- Why: motion and motion blur hide the cut; this is a "whip/match-move" cut. In Blender 5.x Bind Camera to Markers is still `Ctrl+B` in Timeline/Dope Sheet.
- Status: Extracted

### T9 — Entry of next shot mirrors the exit of the previous `[05:30]–[06:15]`
- What: shot two starts at −40° and resolves to 0° over 20 frames, same easing copied from shot one (add-on or Graph Editor `Ctrl+C`/`Ctrl+V` of keys, then fix values). Result: rotation continues across the cut.
- Why: matched direction + matched speed = continuity of motion across cuts.
- Status: Extracted

### T10 — Never let the camera stop: continuous drift between transitions `[06:30]–[07:15]`
- What: after entry, keep rotating +10° over the 40 "hold" frames, then exit adds another 40° (total 50°).
- Why: a camera that comes to a full stop then restarts looks robotic; a slow drift keeps the image alive.
- Status: Extracted

### T11 — Remove the velocity "bump" by rotating the middle handle `[07:15]–[08:00]`
- What: after chaining ease-in → drift → ease-out, there's "a literal bump right after the transition" [07:30]. Select the middle key and rotate its handles until the curve slope is continuous (no flat spot / no kink).
- Why: the bump is a moment where velocity dips toward zero (a flat-ish spot in the F-curve) then accelerates again; the eye reads it as a hiccup. A continuous slope through a pass-through key = constant velocity through it.
- Status: Extracted

### T12 — Use Scene ▸ Full Copy to show other sides without changing animation `[09:15]–[10:00]`
- Full Copy the scene, rotate the product, keep the camera rigs; only move Empties to new focus areas.
- Note: Full Copy duplicates object data; edits to the product won't propagate. Alternative: Linked Copy or a separate rotation Empty under the product.
- Status: Extracted

### T13 — Two side area lights, light linking to model only `[10:45]–[11:15]`
- Two area lights left/right, the second "linked to the model only" so it doesn't affect shadows on the backdrop (Object ▸ Shading ▸ Light Linking in Cycles; EEVEE Next also supports light linking since 4.2... verify per engine in 5.2).
- Out of my domain; cross-reference lighting.
- Status: Extracted

## 3. Claims I doubt or must test
- 90 mm as default — fine for a chair hero from ~3–5 m away; not universal.
- Fixed 40° / 20 frames / 40 frames depend on fps — **25 fps** in the project (corrected from frames [03:20]); 20 f = 0.8 s. At 50/60 fps double the frame counts.
- Cutting at peak speed works best with motion blur on; with blur off it can look like a glitch.

## 4. Anti-AI-slop lessons
- Rig the camera; don't keyframe a free-floating camera's rotation.
- A motion spec (degrees, frames) shared across all shots creates a designed rhythm; random per-shot moves look generated.
- Never let a camera hit zero velocity mid-shot unless it's a deliberate hold.
- Check backdrop coverage through the whole move.

## 5. Candidate isolated test
Chair on cyclorama, 90 mm, two shots of 50 frames. A: camera keyed directly (location+rotation), default eases, hard cut. B: Empty orbit rig, spec 40°/20 f, cut at peak with mirrored ease, +10° drift, bump removed. Metrics: per-frame angular velocity of the camera around the subject (no zeros in B except shot end), viewer preference, and number of F-curves edited.

## 6. Visual verification (frames viewed)
- [00:50] Title bar **Blender 5.0.0**; Cycles GPU Compute; grey cyclorama (Plane) behind an imported Office Chair; timeline 1–250.
- [03:20] Graph Editor on "shot1 movement" (the Empty): **X and Y Euler Rotation channels locked**, Z shown with Normalize; S-curve over frames ~40–56 with handles being scaled (`S` `X`). Output panel: **1080×1920, 25 fps** — answers the fps doubt. Empty scale 0.352 (scene small-scale).
- [05:00] Camera marker bound mid-transition (sheet + frame), the cut happening inside the move — confirms T8.
- [06:50] Text Editor "notes" visible: `shot change rotation = 40d / shot change duration = 20frames / shot change start = after 40 frames / SHOT DURATION = 50 frames` — confirms T7 verbatim. Dope Sheet shows keys at ~0/20 and ~50/60 per shot, markers shot1 @0, shot2 @~50.
- [07:30] Shot 2 entry: Empty Z = −40° at frame 49 → resolves forward; Normalize on.
- [07:50] The "bump": shot2 Z curve flattens at a middle key (~frame 60) before continuing — he selects that key to rotate its handles. Confirms T11 visually; [08:00] sheet shows the smoothed curve.
- [11:03] Lighting: **Area light, Square 1 m, Power 543 W**, white, placed at the side (rotation Y 90°), Normalize on; then duplicated for the other side (sheet [11:00]) and light-linked to the model only. Note list gains "5. after shot change default rotation = 10d".
- [11:44] Final frame: black-and-white chair on near-white cyc, tight 9:16 crop, soft side light, clean contact shadows.
- Quality judgement: **clean commercial-catalogue level** — tasteful, minimal, no slop; lighting is basic (two side areas) but appropriate. Motion system is the real value. Trust medium-high confirmed.
