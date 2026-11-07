---
id: animation-asymmetric-ease-handle-length
domain: animation
status: Extracted
sources: [4Mf2hgb1tP0@00:45, 4Mf2hgb1tP0@01:30, 4Mf2hgb1tP0@01:45, dFK3C83k4Wo@03:15]
blender: "5.2"
---
# Asymmetric ease by scaling Bezier handles (fast-in / long settle)

**Principle:** Handle length controls how long velocity stays near zero around a key. Symmetric default ease is neutral and generic. A fast departure with a long, soft settle is the signature "premium" move used in product films and motion design; the reverse (slow build, fast arrival) creates anticipation and impact.

**Steps / settings (starting points):**
1. Graph Editor (`Ctrl+Tab` toggles from Dope Sheet) [4Mf2hgb1tP0@00:15]. Normalize on, `Home`.
2. Select the end key, `S` `X` to lengthen its handles (long settle). Select the start key and shorten its handles (fast start) [4Mf2hgb1tP0@01:45].
3. Ratio starting point: start handle ≈ 10–25 % of segment length, end handle ≈ 50–80 %. In Easing preset terms ≈ "Expo/Quart Ease Out".
4. Duration: same curve shape over more frames = calmer; check peak velocity not just shape [4Mf2hgb1tP0@01:30]. Too-long handles on both ends compress the middle and spike the speed [dFK3C83k4Wo@03:15].
5. Product/logo reveals: 1–2 s at 24/30 fps; camera push-ins: 3–6 s.

**Use when:** product reveal, UI/graphic element entrances, camera arrivals, settle on hero frame.
**Avoid when:** looping/continuous motion (use linear or pass-through), impacts (Vector), cases where the motion must feel mechanical/robotic deliberately.

**Failure signs:** object "creeps" for too long at the end (end handle too long relative to shot); visible jerk at start (start handle 0 on a heavy object); speed spike in the middle; every element in the scene using the identical curve (synthetic uniformity — vary slightly).
**Cost:** none.
**Conflicts with other sources:** naming of ease in/out in 4Mf2hgb1tP0@00:45 is ambiguous; use Blender's convention (Ease In = slow start, Ease Out = slow end).
**Test to validate:** 1.5 s logo slide: symmetric default vs 20/70 asymmetric; blind preference + velocity plot.
**Log:** 2026-11-05 — Extracted from 4Mf2hgb1tP0, dFK3C83k4Wo.
