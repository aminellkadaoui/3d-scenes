# Lessons log

Short rules learned from real projects. Newest at the top. `3d-scenes-retro` appends here; rules confirmed in a second project get promoted into the reference files and marked `Proven`.

Format: `- [YYYY-MM-DD] [area] Rule — evidence (project) — status`

- [2026-11-07] [lighting] Light white/bright heroes with their own linked lights; exclude them from scene lights. Keyframing scene-light power at the cut was not enough — laptop-to-money — Proven
- [2026-11-07] [lighting] A saturated light on a white object turns white under AgX when pushed; to get colour, lower whites, don't raise the colour — laptop-to-money — Proven
- [2026-11-07] [lighting] UI edits touch only the active light; with duplicates, set all — laptop-to-money — Proven
- [2026-11-07] [lighting] After the user moves a light, check aim error; 55° off made a 1000 W light useless — laptop-to-money — Proven
- [2026-11-07] [motion] AE Speed graph In/Out 75% = two Bezier keys with FREE handles at 75% of the segment; cut on the measured peak frame — laptop-to-money — Proven
- [2026-11-07] [motion] Separate constant drift (linear, extrapolated) from the accent curve so the object never stops — laptop-to-money — Proven
- [2026-11-07] [quality] Viewport grain ≠ render grain; judge noise on a rendered frame cropped at 100% — laptop-to-money — Proven
- [2026-11-07] [quality] "Resolution feels low" = sharpness: temporal denoise off, DOF off, small hard raking light — laptop-to-money — Proven
- [2026-11-07] [quality] Downloaded model normal maps at 1.0 sparkle under hard light; 0.15–0.5 — laptop-to-money — Proven
- [2026-11-07] [render] Measure one final-quality frame before promising a time; tables underestimated ~10× — laptop-to-money — Proven
- [2026-11-07] [setup] Starting from the user's approved scene is the biggest time saver — laptop-to-money — Proven
- [2026-11-07] [process] Don't act on garbled messages; ask — laptop-to-money — Proven
- [2026-11-07] [motion] DEFAULT for every move = mountain speed graph In 75 / Out 75 (user rule, not only turntables) — scripts/mountain_ease.py — Proven
