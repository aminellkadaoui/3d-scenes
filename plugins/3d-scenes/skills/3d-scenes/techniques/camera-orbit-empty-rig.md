---
id: camera-orbit-empty-rig
domain: camera
status: Extracted   # Extracted | Reproduced | Validated | Production-ready
sources: [dFK3C83k4Wo@01:30, dFK3C83k4Wo@09:30, JQT9sT1YuAI@17:15]
blender: "5.2"
---
# Orbit / dolly rig: camera parented to a pivot Empty

**Principle:** One transform per job. The Empty at the subject owns orbit (Z rotation) and optional tilt (X rotation); the camera's *local* position owns dolly distance and height. Each F-curve then describes one physical motion, orbits are perfect circles around the subject, and re-targeting a shot = moving one Empty. Same logic as animating a parent control instead of geometry [JQT9sT1YuAI@17:15].

**Steps / settings (starting points):**
1. `Shift+A` ▸ Empty ▸ Plain Axes, name `SH01_Pivot`, place at the visual center of interest (not necessarily the object origin).
2. Add camera, name `SH01_Cam`, place it in front at the desired distance/height. Focal length chosen first (e.g. 85–100 mm product hero, 35–50 mm environment).
3. Parent: select camera, then Empty, `Ctrl+P` ▸ Object (Keep Transform).
4. Aim: either rotate the camera once to face the pivot, or add a Track To / Damped Track constraint on the camera targeting the pivot (Track Axis −Z, Up Axis Y for Track To). Constraint keeps aim even when you dolly.
5. Animate: pivot Rotation Z for orbit (rotation mode XYZ Euler; values >360° are fine), camera Location (local) Y/Z for push-in/crane. Lock channels you won't animate (padlock in Graph Editor) [dFK3C83k4Wo@03:00].
6. One collection per shot (`SH01`, `SH02`...) [dFK3C83k4Wo@01:15].
7. Starting motion: orbit 15–40° per 2–3 s shot; push-in 5–15 % of camera distance per shot.

**Use when:** product turntables, hero reveals, architectural orbits, any shot that should feel like a slider/turntable/crane.
**Avoid when:** handheld/documentary feel (use noise on a separate rig layer), follow-cams of moving subjects (use Follow Path or Child Of on a moving target), or when the shot needs a straight dolly with parallax across the frame (animate a "dolly" Empty along a line instead).

**Failure signs (how QA detects it went wrong):** horizon tilts during orbit (pivot not upright, or camera rolled); subject drifts in frame (pivot not at center of interest); camera passes through backdrop edge or clips geometry (check all frames); orbit speed visibly pulses (handles not matched).
**Cost:** zero render cost; 2 objects per shot.
**Conflicts with other sources:** none. Add Camera Rigs extension (Dolly/Crane rigs; bundled/available on extensions.blender.org) offers the same idea with bones and an Aim control.
**Test to validate:** same 72-frame orbit keyed (A) directly on camera loc+rot vs (B) pivot rig. Compare per-frame distance camera→subject (B should be constant ±0) and number of F-curves edited.
**Log:** 2026-11-05 — Extracted from dFK3C83k4Wo, JQT9sT1YuAI.
