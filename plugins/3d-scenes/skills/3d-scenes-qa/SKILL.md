---
name: 3d-scenes-qa
description: Score a Blender scene, render or animation against a fixed anti-"AI slop" rubric (10 domains × 5 + motion) and write root-cause issues with the smallest fixes - concept, composition, camera, assets, materials, lighting, environment, color, render, finishing. Runs a read-only bpy scene audit first. Use when the user asks "قيّم المشهد", "وش المشكلة في الرندر", "ليش شكله AI", "ليش مو واقعي", "افحص الجودة", "review this render", "is this good enough", or at every gate of the 3d-scenes skill.
---

# 3D Scenes — visual QA

Knowledge lives in `../3d-scenes/`. Main reference: `../3d-scenes/knowledge/ai-slop-diagnosis.md` (§2 taxonomy, §3 minimum bar, §4 rubric, §5 bpy audit). Realism cues: `../3d-scenes/knowledge/photorealism.md`. Known symptoms: `../3d-scenes/references/09-troubleshooting.md`.

## Procedure
1. **Facts first** — run the read-only audit (§5) with Blender MCP `execute_blender_code`: unapplied scale, missing bevels, default materials, uniform roughness, light count/default lights, camera 50 mm at origin, floating/intersecting objects, empty world, view transform, colour spaces, light-linking receivers. List FAILs.
2. **Look** — the camera view at representative frames (start, key moment / cut, middle, hardest angle, end). Motion: `look` mode `frames` or a playblast.
3. **Image checks** on a rendered frame — grayscale value hierarchy (hero has the strongest contrast?), 160 px thumbnail, clipping (blown non-specular areas, crushed blacks), noise at a 100% crop (brighten dark crops for inspection only). `../3d-scenes/scripts/ref_stats.py` gives numbers; `scripts/flicker_check.py` for animation flicker.
4. **Score** — 10 domains 0–5 (+ Motion), one sentence of concrete evidence each. Cap at 3 any score you can't justify with evidence. Assume a hostile art director; self-scores inflate.
5. **Decide** — any domain ≤2 = blocker. Total ≥40 deliverable; 36–39 only with the user's sign-off; <36 iterate.
6. **Issues** — one `../3d-scenes/templates/qa-issue.yaml` entry per problem: observation → root cause → smallest fix → validation → needs full re-render? Order by influence: Concept → Composition/Camera → Lighting → Environment → Assets → Materials → Animation → Render → Grade.
7. **Re-score after each fix**; same issue failing 2–3 times → re-diagnose one layer higher.

## Report (user's language, short)
Score table (domain / score / evidence) · top 3 blockers with cause and fix · what's already good (protect it).

## Don't
Judge success by "rendered without errors" · add effects to hide structural problems · change several variables at once · compare against a reference side by side without measuring both.
