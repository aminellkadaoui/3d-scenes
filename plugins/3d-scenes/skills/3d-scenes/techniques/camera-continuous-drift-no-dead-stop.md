---
id: camera-continuous-drift-no-dead-stop
domain: camera
status: Extracted
sources: [dFK3C83k4Wo@06:30, dFK3C83k4Wo@07:15]
blender: "5.2"
---
# Continuous drift: never let the camera hit zero velocity mid-shot

**Principle:** Real camera operators rarely stop dead between moves; default Bezier auto-clamped keys make every intermediate key a stop (flat tangent). Chaining eased moves produces "start–stop–start" hiccups (the "bump" [dFK3C83k4Wo@07:30]). Keeping a slow residual drift and a continuous slope through pass-through keys makes the shot feel operated, not computed.

**Steps / settings (starting points):**
1. After the entry move, add a key ~40 frames later with a small extra amount (e.g. +10° orbit or +3–5 % push-in) [dFK3C83k4Wo@06:45].
2. Exit adds the transition amount on top (e.g. 10° + 40° = 50°) [dFK3C83k4Wo@07:15].
3. Graph Editor: select the middle (pass-through) key; set handle type Aligned (or Auto, not Auto Clamped) and rotate its handles (`R`) until the curve has no flat spot and no kink [dFK3C83k4Wo@07:45]. Alternatively delete intermediate keys and shape one long curve.
4. Check: View the curve — slope must never touch zero between the first and last key unless a hold is intended.

**Use when:** product showcases, establishing shots, any shot over ~3 s where the image would otherwise freeze.
**Avoid when:** a deliberate "landing" beat (logo lockup, end card, text needs to be read) — then let it settle completely and hold.

**Failure signs:** visible hesitation/pulse mid-move; Graph Editor shows a flat segment or a slope sign change on a pass-through key (unintended reverse = "moonwalk"); Auto Clamped handles on middle keys.
**Cost:** none.
**Conflicts with other sources:** JQT9sT1YuAI@05:45 explains default ease as "how most motion works" — true for start/stop from rest, not for pass-through keys.
**Test to validate:** 3-key camera move with Auto Clamped middle key vs aligned continuous handles; sample camera speed per frame; check minimum speed between first and last keys.
**Log:** 2026-11-05 — Extracted from dFK3C83k4Wo.
