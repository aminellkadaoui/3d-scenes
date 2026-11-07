---
id: camera-peak-speed-cut-transition
domain: camera
status: Extracted
sources: [dFK3C83k4Wo@04:45, dFK3C83k4Wo@05:30, 4Mf2hgb1tP0@02:00]
blender: "5.2"
---
# Camera-to-camera cut at peak speed with mirrored easing

**Principle:** A cut hidden inside fast, same-direction motion reads as one continuous gesture (a whip/match cut). It works when velocity and direction match on both sides and motion blur smears the frames around the cut.

**Steps / settings (starting points):**
1. Shot A camera: exit move (e.g. pivot Z +40° over 20 frames). Ease: long handle at the start of the exit, near-zero handle at its end (accelerating into the cut) [4Mf2hgb1tP0@02:15].
2. Shot B camera: entry move continuing the same direction (−40° → 0° over 20 frames), near-zero handle at start, long settle at end [dFK3C83k4Wo@05:30], [4Mf2hgb1tP0@02:30].
3. Place the cut at the middle of the transition = fastest frame (e.g. frame 50 when A's exit runs 40–60) [dFK3C83k4Wo@04:45].
4. Timeline: at the cut frame select camera B, `Ctrl+B` (Marker ▸ Bind Camera to Markers). Bind camera A at frame 1.
5. Render Properties ▸ Motion Blur ON, Shutter 0.5 (or up to 1.0 for a stronger whip).
6. Write the spec (degrees, frames, start offset, shot length) and reuse it on every transition [dFK3C83k4Wo@04:15]. The source spec (40° / 20 f / start after 40 f / 50 f shots / +10° drift) was made at **25 fps**, 1080×1920 vertical [dFK3C83k4Wo@03:20, 06:50] (seen in frames) — scale frame counts for other fps.

**Use when:** energetic VSL section changes, feature-to-feature product sequences, montage beats on music.
**Avoid when:** calm/credibility sections (testimonials, explanation) — use a straight cut on a held frame or a slow push. Don't use on every cut; 1 whip per 3–5 cuts keeps it special.

**Failure signs:** visible jump/stutter at the cut (speeds don't match: compare angular velocity on frames cut−1 and cut+1); direction reverses; subject jumps across frame (screen-direction break); no blur → looks like a glitch.
**Cost:** motion blur adds some render time (Cycles: small; EEVEE: Steps setting).
**Conflicts with other sources:** none.
**Test to validate:** A = hard cut between two resting cameras; B = this technique. Velocity plot across the cut; viewer judgement on "one continuous move?".
**Log:** 2026-11-05 — Extracted from dFK3C83k4Wo and 4Mf2hgb1tP0.
