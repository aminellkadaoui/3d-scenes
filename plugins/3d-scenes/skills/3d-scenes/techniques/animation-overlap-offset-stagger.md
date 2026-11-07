---
id: animation-overlap-offset-stagger
domain: animation
status: Extracted
sources: [JQT9sT1YuAI@11:00, JQT9sT1YuAI@30:00, JQT9sT1YuAI@33:00, JQT9sT1YuAI@41:30]
blender: "5.2"
---
# Overlap and stagger: nothing starts or stops on the same frame

**Principle:** Follow-through and overlapping action: parts attached to or following a main mass start later and settle later. Everything moving in perfect sync is the clearest tell of computer interpolation.

**Steps / settings (starting points):**
1. Dope Sheet/Graph Editor: select keys of secondary elements (child parts, second product, text, light, camera) and `G` by 2–6 frames (24/30 fps) after the driver [JQT9sT1YuAI@30:00].
2. For multiple items entering (icons, bottles, cards): stagger 3–5 frames each; vary by ±1 frame so it isn't mechanical.
3. Camera vs subject: let the camera start its move 4–12 frames *after* the subject starts (operator reacts), and settle slightly after.
4. Rotation channels can lag position by 1–3 frames for heavier feel.

**Use when:** multi-element reveals, product + packaging, character limbs, camera follow.
**Avoid when:** mechanically linked parts (gears), deliberate unison graphic beats on a music hit.

**Failure signs:** all keys aligned in one column in the Dope Sheet; elements arriving simultaneously; stagger so large it reads as separate unrelated events (>~0.5 s).
**Cost:** none.
**Conflicts with other sources:** none.
**Test to validate:** 5 icons entering: A all same frame; B 4-frame stagger. Preference test.
**Log:** 2026-11-05 — Extracted from JQT9sT1YuAI.
