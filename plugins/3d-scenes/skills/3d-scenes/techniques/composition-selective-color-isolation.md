---
id: composition-selective-color-isolation
domain: composition
status: Extracted
sources: [skool-rr-cinematic-composition@03:13, skool-rr-cinematic-composition@03:37, skool-rr-cinematic-composition@03:58, HBWYieo5RmU@07:45]
blender: "5.2"
---
# Selective color: grey world, colored subject

**Principle:** A saturated area on a neutral field is the strongest attention pull after value contrast. 3D documentaries render the surroundings in black & white or grey tones and keep only the subject (plus 1–2 directly related props) in color: a red man, a red house, Trump + desk + flags [skool-rr-cinematic-composition@03:37–04:18]. It works with both thirds and center framing.

**Steps / settings (starting points):**
1. Decide what stays in color (one subject; at most 2 linked props).
2. Cycles/EEVEE: View Layer Properties ▸ Passes ▸ Cryptomatte ▸ Object.
3. Compositor: Render Layers → Cryptomatte (pick the hero objects) → Matte → Invert → Factor of a Hue/Saturation/Value node set to Saturation 0.0–0.2 on the Image. Keep 0.1–0.2 instead of 0 for a less "effect" look.
4. Alternative without compositor: lower Saturation on non-hero materials (Hue/Saturation/Value node before Base Color), so it survives any pipeline.
5. Optional: push the hero's saturation slightly (+10–20%), never neon.

**Use when:** a story beat must hit in one glance (the reveal, the notification, the "one thing that matters"); stylised documentary sequences.
**Avoid when:** the sequence is realistic and the effect has no story reason; when the accent color already appears elsewhere in frame; on every shot (it becomes a gimmick).

**Failure signs:** colored fringe/halo at the matte edge (Cryptomatte edge, motion blur); several colored objects competing; skin left grey while clothes are colored (looks like a mistake); hero color not distinct from the grade.
**Cost:** low (one pass + compositor nodes). Cryptomatte with motion blur/DoF can give soft edges — check at 100%.
**Conflicts with other sources:** none; HBWYieo5RmU calls it "pop of color".
**Test to validate:** same frame, baseline vs isolation; blurred 160 px thumbnail; first-fixation guess by a viewer + Sobel/saturation map overlap with hero mask.
**Log:** 2026-11-07 — Extracted from skool-rr-cinematic-composition.
