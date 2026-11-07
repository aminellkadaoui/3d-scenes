---
name: 3d-scenes-learn-tutorial
description: Turn a Blender/3D tutorial (YouTube link, free course lesson, project file) into structured, timestamped knowledge for the 3D Scenes system - transcript + frames → source analysis → technique cards → knowledge files, all marked Extracted until tested. Use whenever the user sends Blender tutorial links and says "ادرس", "حلل", "تعلم من هذا", "ضيفه للنظام", "learn this technique", "add this to the knowledge base".
---

# 3D Scenes — learn from a tutorial

Work in the **source repository** of the plugin (the clone with `.git` and `tools/publish.sh`), folder `plugins/3d-scenes/skills/3d-scenes/` — call it KB. Never edit the installed cache under `~/.claude/plugins/`.

## Goal
Not a summary. Extract **decisions + why + exact Blender steps + when NOT to use**, so a future session can build a professional, non-slop scene. Every claim gets a timestamp.

## Steps
1. **Fetch** — `zsh KB/scripts/ingest_video.sh <url> [en|ar]` → `KB/sources/raw/<id>/` (git-ignored): `transcript.txt` (15 s buckets), `info.json`, 480p mp4, `frames/f_###.jpg` (every 20 s), `frames/sheet_##.jpg`. Needs `yt-dlp`, `imageio-ffmpeg`, `certifi` (pip).
   - YouTube 429 on captions: wait and retry; never fake a transcript. If impossible, use description + frames and mark evidence `partial`.
   - Many links: batches of ≤6; split analysis by domain (lighting / materials+assets / render+color+comp / camera+composition+animation).
   - Course platforms (e.g. Skool): use the captions/frames the user can access; summarise in your own words with timestamps.
2. **Look** — contact sheets first, then the frames where settings are shown (node trees, panels, before/after). Extract more with `ffmpeg -ss mm:ss`. Never claim to have seen frames you didn't open.
3. **Analyse** — `KB/sources/<id>.md` from `KB/templates/source-analysis.md`: problem solved, each technique (what / why / use when / avoid when / starting values with assumed scale / Blender-version differences), doubtful claims, anti-slop lessons, candidate isolated test, trust rating (before/after shown? selling an add-on? clickbait?).
4. **Cards** — one `KB/techniques/<domain>-<slug>.md` per reusable technique (`KB/templates/technique-card.md`). If a card exists, add the source + any conflict instead of duplicating.
5. **Integrate** — update the matching `KB/knowledge/*.md` section, cite `[id@mm:ss]`. When sources disagree, record both with conditions.
6. **Privacy** — no local paths, IPs, personal names, client names, machine details. Use "(local file)".
7. **Report** (user's language, short): what's new, what contradicts existing knowledge, top candidates to test (`3d-scenes-validate`).
8. **Publish** — `bash tools/publish.sh "learned: <tutorial title>"` from the repo root.

## Rules
- Status is always `Extracted`; only `3d-scenes-validate` or a real project promotes.
- Translate magic numbers into principles + starting points (e.g. "f/0.1" → DOF depends on focal length, focus distance and scene scale).
- Note version gaps (tutorial on 3.x/4.x vs current 5.x: AgX default, EEVEE Next, compositor node groups, "Smooth by Angle").
- Don't touch Blender during ingestion.
