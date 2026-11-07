---
id: animation-block-constant-then-spline
domain: animation
status: Extracted
sources: [JQT9sT1YuAI@10:30, JQT9sT1YuAI@23:00, JQT9sT1YuAI@28:45, JQT9sT1YuAI@42:00]
blender: "5.2"
---
# Pose-to-pose: block in Constant, retime, then spline and polish

**Principle:** Smooth interpolation hides bad timing. Judge poses/framings and their timing first with stepped (Constant) interpolation, fix timing against the VO/music, and only then convert to Bezier and polish curves channel by channel.

**Steps / settings (starting points):**
1. Key main poses/camera framings only (story beats). Graph Editor `A`, `T` ▸ Constant [JQT9sT1YuAI@23:00].
2. Play against the VO audio (Sequencer strip or Speaker). Retime: `M` marker, Pivot (`.`) ▸ 2D Cursor, select range, `S X` scale, `G X` slide rest [JQT9sT1YuAI@42:15].
3. Convert: `A`, `T` ▸ Bezier, `V` ▸ Auto Clamped [JQT9sT1YuAI@28:45].
4. Polish one channel at a time (hide others, `Shift+H` isolate) [JQT9sT1YuAI@32:45]: handle types by physics, overlaps.
5. For camera: block framings as still frames; approve composition per beat before animating between them.

**Use when:** any shot longer than a simple 2-key move; multi-beat VSL sequences timed to narration.
**Avoid when:** idle/ambient loops, procedural motion (straight-ahead or modifiers fine) [JQT9sT1YuAI@10:45].

**Failure signs:** polished curves but beats land off the VO; animation re-done after composition change; Bezier conversion flips rotations (quaternion shortest path — switch to Euler for >180° turns [JQT9sT1YuAI@29:00]).
**Cost:** saves iterations.
**Conflicts with other sources:** none.
**Test to validate:** time-to-approval and number of revisions for a 10 s VO-timed sequence, block-first vs spline-first.
**Log:** 2026-11-05 — Extracted from JQT9sT1YuAI.
