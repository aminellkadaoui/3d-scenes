---
id: animation-handle-type-by-physics
domain: animation
status: Extracted
sources: [JQT9sT1YuAI@06:00, JQT9sT1YuAI@15:15, JQT9sT1YuAI@16:00, JQT9sT1YuAI@34:30, JQT9sT1YuAI@35:00, JQT9sT1YuAI@38:15]
blender: "5.2"
---
# Choose keyframe handle type per physical situation (not default ease everywhere)

**Principle:** The F-curve slope is velocity. Bezier + Auto Clamped (Blender's default) puts zero velocity at every key = every key is a stop. Real motion only decelerates where a controlling force acts. Impacts, ballistic flight, objects already in motion and constant-speed travel have no ease.

**Steps / settings (starting points):**
- Graph Editor, select keys, `V`:
  - **Vector** — at impacts/contacts (ball hits floor, product lands on table, feet strike) [JQT9sT1YuAI@16:00]; at the start of a move that enters already at speed [JQT9sT1YuAI@15:30]; in-air ballistic segments [JQT9sT1YuAI@34:45].
  - **Auto Clamped** — default; good for starts/stops from rest, prevents overshoot.
  - **Automatic** — smooth pass-through on intermediate keys (can overshoot; useful for natural settle).
  - **Aligned** — after you hand-shape a handle; keeps tangent continuous.
  - **Free** — deliberate kinks (sudden direction change).
- `T` ▸ Interpolation: Linear for constant-speed (conveyor, slow continuous drift whose ends are off-screen), Constant for blocking/stepped, Bezier for most; Easing presets (Sine/Quad/Cubic/Expo/Back/Bounce/Elastic with Ease In/Out/In-Out) for graphic motion.
- Handle types are **per side**: a landing key can be Left = Vector (arrives at speed) / Right = Auto Clamped (settles) — N panel › F-Curve › Active Keyframe [JQT9sT1YuAI@35:00, seen in frame]. The author's curves also use F-Curve › Handle Smoothing = **Continuous Acceleration** (4.x option; smoother auto handles across keys).
- Arc rule: horizontal channel linear, vertical channel eased at the apex → parabola [JQT9sT1YuAI@12:00].
- Default can be changed in Preferences ▸ Animation ▸ F-Curves (Default Interpolation, Default Handles).

**Use when:** every animation, reviewing each key.
**Avoid when:** n/a — the avoidance is "don't leave everything Auto Clamped".

**Failure signs:** floaty landings (ease into an impact); objects "hover" at the top of a jump too long or not at all (apex not centered); camera hesitations at intermediate keys; overshoot/wobble past a target (Automatic handles where Auto Clamped needed); sudden linear starts on a heavy object.
**Cost:** none.
**Conflicts with other sources:** 4Mf2hgb1tP0 and dFK3C83k4Wo shape handles by scaling (`S X`) rather than changing types — compatible: type sets the rule, scaling sets strength.
**Test to validate:** product drop onto table: A default auto-clamped keys; B Vector at contact + short 2-frame settle. Viewer test "does it feel heavy?".
**Log:** 2026-11-05 — Extracted from JQT9sT1YuAI.
