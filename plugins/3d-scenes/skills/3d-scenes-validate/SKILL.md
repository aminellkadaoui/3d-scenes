---
name: 3d-scenes-validate
description: Test a technique card from the 3D Scenes knowledge base in a small isolated Blender scene - baseline vs technique, same camera/samples, measure quality and render time - then promote it (Extracted → Reproduced → Validated → Production-ready) or reject it with evidence. Use when the user says "اختبر التقنية", "جرّب هذا في بلندر", "هل هذي الطريقة تشتغل فعلاً", "validate this technique", "does this actually work", or before relying on an untested technique in a real project.
---

# 3D Scenes — knowledge validation

Cards: `../3d-scenes/techniques/`. Experiments go to `../3d-scenes/experiments/<card-id>/` in the **source repository** (the clone with `.git` and `tools/publish.sh`, not the installed cache). Requires Blender MCP and the user's OK to use Blender.

## Protocol (one technique at a time)
1. **Pick** a card; write the hypothesis: "Applying X improves Y in condition Z without costing more than W".
2. **Test scene** — the smallest scene that isolates the variable; real-world scale; fixed camera, seed, samples and resolution; decent assets/materials so the test isn't judged on a slop base. Save the .blend in the experiment folder.
3. **Baseline render** — without the technique (e.g. 960×540, enough samples to judge, denoised). Record time.
4. **Technique render** — change ONLY the technique's settings. Same frame. Record time.
5. **Compare** — side by side; score the affected pillar(s) with `../3d-scenes/knowledge/ai-slop-diagnosis.md` §4; measure where possible (`scripts/ref_stats.py`, `scripts/eevee_vs_cycles.py`, `scripts/flicker_check.py`). Did it improve what it claims? Side effects? Cost?
6. **Vary** — 1–2 other conditions the card claims to fit (scale, EEVEE vs Cycles) and 1 it should NOT fit.
7. **Log** — `experiments/<card-id>/log.md`: hypothesis, settings, image paths, times, scores, verdict. Update the card: `status`, a `Log:` line, corrected starting values.
8. **Publish** — run `3d-scenes-retro` step "Publish" (or `bash tools/publish.sh "<note>"` from the repo root).

## Promotion rules
- `Reproduced`: steps work in the current Blender as described (maybe renamed settings).
- `Validated`: measurable improvement vs baseline in the stated condition, acceptable cost.
- `Production-ready`: validated in ≥2 real shots/projects.
- Rejected / narrowed: write why — a failed test is valuable knowledge, keep it.
- Never promote on "looks nice" alone; never change two variables at once.
