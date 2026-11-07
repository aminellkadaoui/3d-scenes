---
name: 3d-scenes
description: Build cinematic Blender 3D scenes for videos (VSL, ads, reels, product shots) in record time with EEVEE, using field-tested recipes instead of re-discovering them - short feedback loop, light linking as "track matte" lighting, turntable spin + object match cut with an After-Effects-style speed graph, camera crane rig, polished floor/metal/paper materials, EEVEE noise and sharpness fixes, render-time estimates and delivery. Use whenever the user wants to build, light, animate, fix or render a Blender scene - "سوي مشهد", "مشهد 3D", "سوي لي سين في بلندر", "خل الإضاءة تأثر على الفلوس بس", "سوي له مات", "light sweep", "متش كت", "جراف الجبل", "النويز كثير", "الجودة ضعيفة", "الأرضية تعكس", "رندر", "turntable", "match cut", "product reveal", "make this look premium", "EEVEE noise", "light linking" - even if they don't say "skill".
---

# 3D Scenes — build premium Blender shots fast

This skill is distilled from real production work (Blender 5.2, EEVEE, Blender MCP). Every recipe here was **applied in a real shot and checked**, not copied from a tutorial. Status of each recipe is marked in the reference files: `Proven` (worked in a delivered shot) or `Candidate` (worked once, needs another project).

Reply in the user's language. Most users of this skill write Gulf Arabic and use editor words (After Effects terms) for 3D concepts — translate them (see `references/00-vocabulary.md`).

## The one idea
Quality came fast because of **a short, disciplined feedback loop**, not because of heavy settings:
1. Start from a scene that already looks good (the user's approved file), never from an empty file.
2. One change per round → check through the camera in Rendered → report value *before → after* → let the user react.
3. Diagnose before changing (solo the light, crop the render at 100%, measure pixels). Never "fix" by guessing.
4. Small steps (20–30%) when the user says "more/less" (زيد/نقّص).
5. Turn every solved problem into a rule (run `3d-scenes-retro` at the end).

## Workflow (gate before moving on)

| # | Stage | Read | Exit check |
|---|---|---|---|
| 0 | Safety & setup | `references/01-project-setup.md` | Working on a **copy** in its own folder; original untouched; unsaved work in other files checked |
| 1 | Brief in one place | `references/02-brief-and-references.md` | One brief (file + board): idea, each reference labelled by what it's for, measured tone numbers |
| 2 | Assets | `references/03-assets.md` | Real-scale, grounded, no intersections, inside the hero area; unwanted parts moved to `_HIDDEN_*` collections |
| 3 | Camera | `references/06-camera-and-motion.md` §Camera | User-approved angle captured as numbers; rig built |
| 4 | Materials | `references/04-materials.md` | Floor/metal/paper/screen recipes applied; colour spaces right |
| 5 | Lighting | `references/05-lighting-light-linking.md` | Each light has one job and an explicit receiver set (light linking) |
| 6 | Animation | `references/06-camera-and-motion.md` | Speed graph sampled (deg/frame table), cut on the peak frame, no dead stops |
| 7 | Quality | `references/07-eevee-quality-noise.md` | Final EEVEE profile, compositor denoise, no sparkle/grain at 100% crop |
| 8 | Render & delivery | `references/08-render-delivery.md` | 1 measured frame → time estimate → full render → PNG + ProRes |
| 9 | Retro | skill `3d-scenes-retro` | New lessons written to `lessons/LESSONS.md` |

Anything going wrong → `references/09-troubleshooting.md` (symptom → cause → fix). Blender 5.x Python traps → `references/10-blender5-api.md`. Ready code → `scripts/` (paste into Blender MCP `execute_blender_code`; each script has a CONFIG block at the top).

Full worked example with every number: `case-studies/laptop-to-money.md`. Read it once before your first scene with this skill — it is the fastest way to absorb the method.

## Feedback-loop protocol (the part that saves the most time)
Read `references/11-feedback-loop.md`. Short version:
- **Look before and after every change** (`look` camera + rendered, small `max_size`). If `look` can't show something (screen-space reflections, final noise), say so and ask for one rendered frame instead of guessing.
- **Report as a table**: what changed, before → after, which reference/recipe it came from.
- **Respect the user's manual edits**: re-read scene values at the start of every turn (they edit in the UI, press Ctrl+Z, move lights). Never overwrite a value they set without saying so.
- **When the user says "it doesn't work"**: solo the suspect (hide others), check aim angle, check light-linking membership, check exposure on *every* duplicate — then explain the cause in one line.
- **Ask only real decisions** (art direction, swapping a hero asset, anything that changes the user's chosen angle). Fix technical problems yourself.
- **No auto-render, no auto-save.** Saving a *copy* for a render job is fine when the user asked to render.

## Hard rules
- Ready-made assets only (Poly Haven, Sketchfab, user files). Never model props/characters from primitives; if something is missing, say so at once.
- Never delete user objects: move them to a hidden, excluded collection (`_HIDDEN_*`).
- Engine is EEVEE unless the user asks for Cycles. Don't switch engines silently.
- Never trust a time estimate from tables — render one frame and measure (estimates were 7–10× too low in practice).
- Deliver full quality (100% res, scene samples, PNG frames + ProRes). Previews only when asked.

## Growing the knowledge
After every project, run the `3d-scenes-retro` skill. It turns the session's problems and solutions into new rules in `lessons/LESSONS.md` and proposes upgrades to the reference files (with the user's approval). A rule that works in a second project is promoted from `Candidate` to `Proven`.
