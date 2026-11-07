# How to animate anything in Blender (keyframes, graph editor, 12 principles, bouncing ball, backflip)
- url: https://youtu.be/JQT9sT1YuAI
- channel / duration / Blender version shown: SharpWind / ~44 min (transcript ends [44:00]) / **Blender 4.2.0** (status bar at [35:00], corrected from frames)
- domain(s): animation (primary), camera (indirectly: graph editor skills are the same for camera moves), qa
- evidence used: transcript + 10 extracted frames focused on the Graph Editor (see §6). Curve shapes for the ball and backflip now seen.
- trust: medium-high for fundamentals (keyframe colors, handle types, normalize, vector-for-contact, scale-from-2D-cursor retiming are all standard and correct). Medium for the character section (author admits it is "still not 100% there" [43:15]). Sponsored segment for the Graph Pilot add-on [31:15–32:15] — treat claims about the add-on as advertising; nothing in the lessons requires it [32:15].

## 1. Problem it solves
Beginners key poses and get floaty, uniformly eased, "computer-interpolated" motion: everything starts and stops softly, objects slide, rotations flip. The video teaches how to read the F-curve as the actual motion, how to choose interpolation/handle types per physical situation, and a pose-to-pose workflow (block → spline → polish).

## 2. Techniques

### T1 — Keyframing methods and the property color code `[01:15]–[03:45]`
- What: `I` keys all transform channels (in 4.x+ the channels inserted by `I` in the viewport follow *Preferences ▸ Animation ▸ Default Key Channels*); `K` opens the Keying Set menu; hover a field + `I` keys just that field; right-click field ▸ Insert Keyframes / Insert Single Keyframe. Auto-Keying (record button in the Timeline header) only keys channels that changed [02:00]. Field colors: yellow = on a key, green = animated but between keys, orange = changed but not keyed — will be lost on frame change [03:00–03:45].
- Why: Missing "hold" keys cause interpolation to span from the previous key, so objects drift early [02:15–03:00].
- Use when: always; orange fields are a QA red flag before scrubbing.
- Blender 5.2 notes: same colors; Auto-Keying still in Timeline header. In 4.4+ animation data uses *slotted Actions*; doesn't change the workflow here.
- Status: Extracted

### T2 — Read the F-curve as motion: X = time, Y = value, slope = speed `[04:00]–[05:45]`
- What: Graph Editor, isolate one channel (click it in the channel list or hide others with `H` / `Shift+H`). Default interpolation is Bezier with Auto-Clamped handles, giving an S-curve = ease in and out [04:00]. Steeper slope = faster; flat = stopped.
- Why: "this graph literally shows us the value of the attribute on every single frame" [05:15]. Speed problems (hitches, bumps, overshoot) are visible as slope discontinuities before you even play.
- Use when: diagnosing any motion, camera included.
- Status: Extracted

### T3 — Handle types (`V`) chosen by physics `[06:00]–[06:30]`, applied `[15:15]–[16:00]`, `[34:30]–[37:15]`
- What: `V` menu: Free (independent), Aligned (opposite, linked), Vector (points at neighbor key → linear segment, sharp corner), Automatic (smooth), Auto Clamped (smooth, no overshoot past neighbor values; default). Moving an auto handle converts it to Aligned [06:30].
- Applied: ball X channel: first key Vector so ball enters at full speed, last key eased to stop [15:15–15:45]; ball Z contact keys Vector so impacts are sharp [16:00]; in-air channels Vector/linear because "in the air you can't really slow down" [34:45]; landings Vector "because you don't just slow down before you land" [35:00]; feet snap with Vector [38:15].
- Why: Ease = acceleration from a force you control. Ground contacts, impacts and ballistic flight have no gentle deceleration, so default easing reads as floaty/robotic.
- Use when: impacts, cuts in camera speed that should feel mechanical, linear constant-speed travel (conveyors, drones, slow continuous camera drifts).
- Don't use when: things that genuinely accelerate from rest (camera dolly start, object pickup).
- Status: Extracted

### T4 — Graph navigation: Normalize, only-selected handles `[06:45]–[07:45]`
- What: `Ctrl+MMB` drag scales view per axis; Normalize toggle (Graph Editor header) maps every curve to −1..1 to compare channels with different units; View ▸ Only Selected Keyframes Handles to declutter; `Home` to frame all. Also used in dFK3C83k4Wo@03:00.
- Note: Normalize changes display only; editing still writes real values.
- Status: Extracted

### T5 — 12 principles mapped to 3D `[07:45]–[14:30]`
- Squash/stretch mostly for cartoony work (shape keys / smear frames) [08:30]; anticipation scales with weight [09:15]; **staging = controlling where the audience looks; "make your idea obvious"; reveal information in sequence** [09:30–10:00]; pose-to-pose for complex, straight-ahead OK for idle loops [10:15–10:45]; follow-through/overlap: hanging parts start late and stop late [11:00]; slow in/slow out is the default curve but skip the ease where something is already moving (hit) [11:15–11:30]; arcs: animate X linear, Z eased → parabola [11:45–12:15]; secondary action must not steal attention [12:15–12:45]; timing = key spacing, use reference and fresh eyes [12:45–13:15]; avoid mirrored/symmetrical poses [13:45]; appeal includes set design [14:00].
- 3D/VSL relevance: staging + timing + overlap are the three that matter most for product/camera work (stagger elements, don't move everything on the same frame).
- Status: Extracted

### T6 — Separate controls: animate an Empty/bone, not geometry `[14:45]–[19:30]`
- What: Rotation on the child, translation/scale on a parent Empty whose origin sits at the ball's contact point, so squash happens from the floor and doesn't spin with the ball. Cleaner version: armature with root bone at bottom + child bone at center; Maintain Volume constraint on the root bone (Free axis Z) for automatic squash/stretch [19:15–19:30].
- Why: each transform layer does one job; pivots placed where the physics happens.
- Same idea for cameras: camera parented to Empty(s) so orbit, dolly and tilt live on different objects (see dFK3C83k4Wo@01:30).
- Status: Extracted

### T7 — Bounce physics rules `[16:00]–[16:45]`
- Constant bounce factor (each bounce height = same % of previous), parabolic arcs, peak centered in time, rotation matched to travel distance so it doesn't skid.
- Status: Extracted

### T8 — Pose-to-pose blocking in Constant, then Bezier `[23:00]–[23:30]`, `[28:45]`
- What: Select all keys in Graph Editor, `T` ▸ Constant to judge poses and timing without interpolation; retime; then `T` ▸ Bezier and `V` ▸ Auto Clamped to spline [28:45]. Then polish channel by channel with others hidden [32:45].
- Why: timing errors are masked by smooth interpolation; stepped playback forces you to fix timing first.
- Status: Extracted

### T9 — Rotation mode: Quaternion vs Euler `[22:00]–[22:45]`, `[29:00]`
- What: Quaternion interpolation takes the shortest path, so flips >180° reverse; switch the bone/object to XYZ Euler for full flips (and re-key). Euler can gimbal lock; quaternion avoids that.
- Camera relevance: orbit Empties with large Z rotations should be Euler; keying Euler Z with values beyond 360° is fine.
- Status: Extracted

### T10 — Overlap by offsetting keys a few frames `[30:00]`, `[33:00]`, `[41:15]`
- Shift child-part keys a few frames later than the driver so not everything starts/stops on the same frame. "overlapping action is always good" [33:00].
- Status: Extracted

### T11 — Retiming a section: marker + 2D cursor pivot + `S` `X` `[42:00]–[43:00]`
- What: `M` adds a marker; set Pivot (`.`) to 2D Cursor; select keys up to cursor frame; `S` then `X` to scale timing; `G` `X` to slide the rest. Then scale everything to slow globally.
- Use: tightening a shot to match the VO edit.
- Status: Extracted

## 3. Claims I doubt or must test
- "Default interpolation is ease in and out ... because most motion actually works this way" [04:00], [05:45]: true for things starting/stopping from rest; for camera drifts and continuous motion it causes the robotic "start-stop every key" look. Blender's default is set in Preferences ▸ Animation ▸ F-Curves (Default Interpolation / Default Handles).
- Bounce "60% smaller" [16:15] is an illustrative number, not physics data.
- "Ease out after an ease out ... looks good here" [41:15] — explicit artistic cheat; fine.
- Interpolation naming: Blender's ease-in/out naming in the `T` menu (Easing: Ease In / Ease Out / In and Out) refers to the *segment after the key*; tutorials are inconsistent. Verify in-app.

## 4. Anti-AI-slop lessons
- Default auto-clamped ease on every key is the signature of unedited CG motion. Decide per key: ease, vector or linear.
- Nothing should start and stop on the same frame; stagger (overlap) by 2–6 frames.
- Block timing with Constant interpolation first; smoothness is the last step.
- Animate controls (Empties), not meshes; put pivots where the physics is.
- Staging: one idea at a time, revealed in sequence.

## 5. Candidate isolated test
Cube moves 0→5 m over 48 frames, then stops; camera static. A: default Bezier auto-clamped both keys. B: first key Vector (enters at speed), last key long ease (handle scaled ×2). C: B + 3-frame-delayed child object. Render viewport playblasts; show to a fresh viewer; measure velocity curve (Graph Editor ▸ View ▸ show curve's derivative via a driver or by sampling location per frame) and ask which reads "natural".

## 6. Visual verification (frames viewed)
- [04:30], [07:10] presenter talking head only (no graph visible at those times).
- [06:10] Graph Editor `V` menu "Set Keyframe Handle Type": Free / Aligned / Vector / Automatic / Auto Clamped — confirms T3 list and order.
- [15:40] Ball X-location curve: first key at frame 0 has a short straight (Vector-like) handle so the ball **enters at speed**; the last key (~frame 200) has a **very long horizontal handle (~85 frames)** giving a long ease-out stop. Confirms T3 application and the asymmetric-handle idea (see `animation-asymmetric-ease-handle-length`).
- [16:20] Ball Z curve with Normalize on: **sharp V corners at every floor contact** (Vector), rounded peaks with flat handles, bounce heights decaying and bounce durations shortening (contacts at ~f43, 77, 103, ~125, ~140). Confirms T7 physics visually.
- [23:20] Rig (Rigify-style mannequin), Pose mode, Normalize on, Graph Editor blocking; Output PNG RGBA 8-bit; resolution 1920×1080.
- [35:00] + crop: torso Y Location key at frame 109: Interpolation Bezier, **Left handle Vector / Right handle Auto Clamped** (mixed per side), F-curve **Handle Smoothing: Continuous Acceleration**; Graph Pilot add-on panel (sponsor) open. Status bar **4.2.0**. (Added: handle types are set per side.)
- [41:20] Backflip arm channels, Normalize on: dense overlapping curves with offset timings (overlap) — confirms T10 in practice; rotation mode visible as Quaternion on this bone.
- [42:30] Pivot Point pie (Bounding Box Center / 2D Cursor / Individual Centers) during retiming — confirms T11 (2D Cursor pivot).
- Quality judgement: fundamentals demo (ball) is **clean and correct**; the mannequin backflip is a mid-level learning piece (author says so) — not a portfolio-grade result. Trust the Graph Editor technique, not the character polish.
