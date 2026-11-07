# Animation & camera motion — knowledge (Blender 5.2)

Status: **Extracted**. Sources: JQT9sT1YuAI (keyframes, Graph Editor, 12 principles, physics), 4Mf2hgb1tP0 (easing via handle scaling, eased camera transitions), dFK3C83k4Wo (camera orbit rigs, multi-camera transitions), Blender manual (F-Curve Modifiers), expert knowledge. Cards: `techniques/animation-*.md`, `techniques/camera-*.md`.

---

## 1. Timing, spacing, easing — the vocabulary
- **Timing** = how many frames an action takes (duration). **Spacing** = how far it moves between consecutive frames (velocity distribution). Easing = changing spacing near keys. In the Graph Editor: X = time, Y = value, **slope = speed**, curvature = acceleration [JQT9sT1YuAI@04:15–05:30].
- Same motion, different timing = different meaning/weight [JQT9sT1YuAI@13:00]. Same curve over more frames = calmer; over fewer = snappier [4Mf2hgb1tP0@01:30–01:45].
- Ease In (Blender/Penner convention) = slow start, accelerating; Ease Out = slow end, decelerating. (4Mf2hgb1tP0 uses the terms loosely [00:30–01:15].)
- Always set fps first (Output Properties ▸ Format ▸ Frame Rate) — durations in frames mean nothing without it. VSL: 24, 25 or 30 fps.

## 2. Keyframing basics that prevent errors
- `I` (insert, viewport: channels per Preferences ▸ Animation ▸ Default Key Channels), `K` keying set menu, hover-field `I` for one property, right-click ▸ Insert Single Keyframe [JQT9sT1YuAI@01:15–01:45].
- Field colors: yellow keyed on this frame, green animated, orange changed-not-keyed (will be lost) [JQT9sT1YuAI@03:00–03:45].
- Missing "hold" keys make a channel interpolate across a long span and drift early — key all channels at holds or copy/paste the hold key [JQT9sT1YuAI@02:15–03:00].
- Auto-Keying only keys changed channels [JQT9sT1YuAI@02:00].
- Rotation mode: Quaternion takes the shortest path (flips >180° go the wrong way); use XYZ Euler for flips/orbits >180°; Euler can gimbal-lock when the middle axis nears ±90° — choose rotation order so the axis that turns most (usually Z for orbits) is the outer one [JQT9sT1YuAI@22:00–22:45].

## 3. Graph Editor essentials
- `Ctrl+Tab` toggles Dope Sheet ↔ Graph Editor [4Mf2hgb1tP0@00:15]. `Home` frame all; `Ctrl+MMB` scale view; **Normalize** (display −1..1 only) [JQT9sT1YuAI@07:15]; View ▸ Only Selected Keyframes Handles; hide `H`, isolate `Shift+H`, unhide `Alt+H`; lock channels you don't want to touch [dFK3C83k4Wo@03:00].
- **Interpolation** (`T`): Constant, Linear, Bezier; Easing presets (Sine, Quad, Cubic, Quart, Quint, Expo, Circ, Back, Bounce, Elastic) with Ease In/Out/In-Out.
- **Handle types** (`V`): Free, Aligned, Vector, Automatic, Auto Clamped (default) [JQT9sT1YuAI@06:00–06:30]. Moving an auto handle turns it Aligned.
  - Auto Clamped: no overshoot; every extreme key becomes flat = a stop.
  - Automatic: smooth pass-through, can overshoot (natural settle).
  - Vector: sharp corner/linear segment — impacts, ballistic flight, entering at speed [JQT9sT1YuAI@15:30], [16:00], [34:45], [35:00].
- **Handle length = ease strength**: `S X` on selected keys/handles; long end handle = long soft settle; short start handle = fast departure [4Mf2hgb1tP0@00:45–02:00], [dFK3C83k4Wo@03:15].
- Retiming: marker `M`, Pivot `.` ▸ 2D Cursor, `S X` scale range, `G X` slide [JQT9sT1YuAI@42:15–43:00]. Alternatively Dope Sheet scale with `S` from current frame.
- Defaults: Preferences ▸ Animation ▸ F-Curves ▸ Default Interpolation / Default Handles (change only if a project wants e.g. Linear defaults for mechanical motion).
- Cleanup of baked/mocap/noisy curves: Key ▸ Clean Channels, Decimate, Smooth (Gaussian/Butterworth) filters; Smooth (Gaussian) also exists as an F-Curve modifier.

## 4. Avoiding robotic default-ease-on-everything motion
The unedited CG signature: every key Auto Clamped → every key a stop → "move–stop–move" with symmetric S-curves, all objects starting/stopping on the same frame, linear-feeling speeds, no weight.
Fixes:
1. **Per-key handle decision** by physics (§3; `techniques/animation-handle-type-by-physics.md`).
2. **Asymmetric eases** (fast out / long settle for premium reveals; slow build / hard stop for impact) (`techniques/animation-asymmetric-ease-handle-length.md`).
3. **Pass-through keys with continuous slope** — no velocity dips mid-move; rotate the middle handles to remove the "bump" [dFK3C83k4Wo@07:30–08:00] (`techniques/camera-continuous-drift-no-dead-stop.md`).
4. **Overlap/stagger** 2–6 frames; follow-through for hanging parts [JQT9sT1YuAI@11:00], [30:00], [33:00] (`techniques/animation-overlap-offset-stagger.md`).
5. **Arcs**: living/organic motion travels in arcs; for jumps animate horizontal linear + vertical eased at apex [JQT9sT1YuAI@11:45–12:15].
6. **Anticipation** before big moves (longer for heavier objects) [JQT9sT1YuAI@09:00–09:15]; **secondary action** that doesn't steal focus [12:15–12:45].
7. **Block in Constant first, spline later** [JQT9sT1YuAI@23:00], [28:45] (`techniques/animation-block-constant-then-spline.md`).
8. Animate **controls (Empties/bones)**, not geometry; put pivots where the physics happens (e.g. squash from the contact point) [JQT9sT1YuAI@14:45–19:30].
9. Slight variation: don't copy identical curves to 10 objects; vary timing ±1–2 frames and amplitude ±5–10 %.

## 5. F-Curve modifiers (Graph Editor ▸ Sidebar `N` ▸ Modifiers)
From the Blender manual: Generator, Built-in Function, Envelope, **Cycles** (Repeat / Repeat with Offset / Repeat Mirrored; must be first; for loops and turntables), **Noise**, Limits, Stepped Interpolation (on-twos/stop-motion look), Smooth (Gaussian).
- **Noise**: Blend Type (Replace ±0.5 range, Add/Subtract/Multiply 0..1), Scale (horizontal stretch — bigger = slower wobble), Strength (amplitude), Offset, Phase (seed), Depth, Lacunarity & Roughness (only when Depth > 0). Every modifier has Restrict Frame Range (Start/End, Blend In/Out) and Influence.
- Handheld starting point (24–30 fps): rotation X/Z noise, Scale 30–80, Strength ≈0.005–0.02 rad, different Phase per axis, Depth 0–1, roll tiny or none; fade via Blend In/Out. Reduce with longer lenses. Put it on a separate parent/child layer from the main move (`techniques/camera-handheld-noise-modifier.md`).
- **Cycles + Linear** extrapolation (Channel ▸ Extrapolation Mode ▸ Linear) for infinite constant turntables.

## 6. Camera rigs
| Rig | How (Blender 5.2) | Use for |
|---|---|---|
| **Pivot orbit** | Camera parented to Empty at subject; Empty Z rot = orbit; camera local loc = dolly/crane [dFK3C83k4Wo@01:30–01:45] | product turntables, reveals |
| **Aim target** | Object Constraint **Track To** (Track Axis −Z, Up Y) or **Damped Track** (−Z) on camera → `SH##_Aim` Empty; animate the aim separately | following subject while camera travels; smooth reframes |
| **Dolly / truck on a line** | Parent camera to a `Dolly` Empty, animate only its local Y (push) or X (truck/slide) | push-ins, parallax slides |
| **Follow Path** | Bezier curve + camera Follow Path constraint (Animate Path, or keyed Offset/Offset Factor; Follow Curve optional) + Track To aim | long fly-throughs, smooth spline travel |
| **Crane / Dolly rigs** | Add Camera Rigs extension (Add ▸ Camera ▸ Dolly / Crane / 2D rig; Crane has Arm Height/Length) | physically plausible crane/dolly moves |
| **Shake layer** | Extra Empty in the hierarchy with Noise modifiers | handheld feel without touching the main move |
| **Focus Empty** | Camera DoF Focus Object = `SH##_Focus` Empty; animate it | rack focus |
Hierarchy example: `SH01_Pivot` → `SH01_Dolly` → `SH01_Shake` → `SH01_Cam` (+ Track To `SH01_Aim`, DoF focus `SH01_Focus`). One collection per shot; descriptive names [dFK3C83k4Wo@01:00–01:15].
Multi-camera: Timeline markers + `Ctrl+B` Bind Camera to Markers [dFK3C83k4Wo@05:00]; or render shots separately and cut in the editor (more flexible for VSL editors).

## 8. Motion speed relative to shot length and edit
- Shot length in VSL is driven by the VO line. Rule of thumb: the camera should cover its move over the whole shot (not finish halfway and freeze) unless a hold is needed for reading text.
- Speed in screen space matters, not meters: a subject should not cross more than ~1/3–1/2 frame width per second in calm sections (judder/strobing risk at 24–30 fps with fast pans, especially with long lenses).
- Faster cuts → stronger, shorter moves; long shots → slower, longer moves. Keep a **motion spec** per video (degrees, frames, offsets) and reuse it [dFK3C83k4Wo@04:15–04:45]; consistency = designed rhythm.
- Leave handles: render 12–24 extra frames at head/tail so the editor can trim and the move is already "in motion" at the cut point.

## 9. Continuity across cuts
- Screen direction: keep subject moving/looking the same direction across cuts unless reversing is the point (180° rule).
- Motion continuity: direction and speed match at cut points [dFK3C83k4Wo@05:30–06:15]; don't cut from a fast move to a static shot unless it's a deliberate hard stop on a beat.
- Lighting, lens and camera height consistency within a scene; deliberate shot-size progression (wide → medium → close).
- Staging: reveal information in sequence, one idea per shot [JQT9sT1YuAI@09:30–10:00].

## 10. Preview before final (playblast)
- View ▸ **Viewport Render Animation** in Camera view (Solid or Material Preview, simplify on) at final fps and aspect; or EEVEE low-sample preview. Output to MP4 (FFmpeg) in a `previews/` folder with version suffix.
- Judge motion only from a played-back file at real speed, never from scrubbing. Watch once full-screen, once at thumbnail size, once frame-by-frame at cuts.
- Turn on motion blur in the preview when judging whip/fast moves (EEVEE).
- Gate rule (CLAUDE.md): no final render of an unchecked motion.

## 11. Motion QA checklist (fail = fix before render)
- [ ] **Jitter**: frame-to-frame wobble from noisy keys, constraint fights, or Noise Scale too small. Check Graph Editor for zig-zags; check camera at 100 % zoom.
- [ ] **Popping**: sudden jumps from missing hold keys, interpolation through a key with wrong value, IK/FK switch, parent switch, or quaternion flip [JQT9sT1YuAI@22:00]. Scrub frame by frame where it happens.
- [ ] **Gimbal / flips**: Euler axes locking near 90°, or Track To flipping when the camera passes over the aim (Up axis aligns with track axis) — keep aim off the vertical or use Damped Track.
- [ ] **Overshoot**: Automatic/Free handles pushing past targets (camera bobbing past final framing; product passing through table) — use Auto Clamped or shape handles.
- [ ] **Bumps/hesitations**: velocity dips at pass-through keys [dFK3C83k4Wo@07:30] — continuous slopes.
- [ ] **Floaty**: eased impacts, too-slow fall, apex not centered [JQT9sT1YuAI@16:00–16:30].
- [ ] **Synchrony**: everything starting/stopping on the same frame — stagger.
- [ ] **Unmotivated moves**: camera moves that don't reveal, follow or emphasize anything; spins and swoops without story reason.
- [ ] **Speed**: too fast for the shot length (strobing) or so slow it reads as a still with drift error.
- [ ] **Frame integrity**: backdrop edges, clipping, empty world, or text-safe zones broken anywhere in the move [dFK3C83k4Wo@00:30].
- [ ] **Cuts**: matched direction/speed at whip cuts; motion blur on.
- [ ] Previewed at final fps & aspect as a played file.

## 12. Doubts / to test
- Handheld noise values here are expert starting points (no source in this batch demonstrated them).
- Velocity guideline "≤1/3–1/2 frame width per second" is a heuristic from cinematography panning tables; test at 24 vs 30 fps.
- Whether cutting at peak speed beats cutting at near-rest for VSL audiences — candidate test in `techniques/camera-peak-speed-cut-transition.md`.
