---
id: rendering-light-path-bounce-tuning
domain: rendering
status: Extracted
sources: [cycles_20x_faster@12:45, cycles_20x_faster@13:15, cycles_20x_faster@13:27]
blender: "5.2"
---
# Tune Max Bounces per type by eye, then set Total to their sum

**Principle:** each bounce type only costs time on paths that still carry energy of that kind. Past the point where an extra bounce changes the image visibly, it is pure cost. Russian roulette already kills weak paths, so the saving is largest in bright, high-albedo interiors and glass-heavy shots, and smallest in dark rooms with low-albedo (black) walls.

**Steps / settings (starting points):**
1. Camera view › Rendered shading › viewport Denoise ✔ (so you judge light, not noise) [cycles_20x_faster@12:45].
2. Light Paths › Max Bounces: set **Diffuse, Glossy, Transmission, Volume = 1** (leave Total high for now).
3. Raise one type at a time until the viewport stops changing visibly. Check the areas that depend on that type: diffuse = corners, ceiling, shadowed sides; glossy = floor/desk reflections, chrome; transmission = glass, liquids, window panes (each surface = 1 in + 1 out); volume = only for thick multi-scatter media [cycles_20x_faster@13:00].
4. **Total = Diffuse + Glossy + Transmission + Volume** [cycles_20x_faster@13:15]. Transparent is separate (alpha cut-outs; 8 default, 16–32 for stacked leaves/hair).
5. Confirm on a final-quality still (full samples, 100% res), comparing a 200% crop of the darkest corner before/after.
- Author's result for a translucent cassette product shot: Total 8, Diffuse 1, Glossy 3, Transmission 4, Volume 0, Transparent 8 [cycles_20x_faster@13:27].
- Typical interiors land at Diffuse 3–4, Glossy 3–4 (see `knowledge/rendering.md` §4).

**Use when:** every Cycles final, once lighting and materials are approved (bounces depend on both).
**Avoid when:** lighting/material look-dev is still changing (re-tune after); judging only in a low-res viewport region — subtle bounce colour and dark-corner levels can shift.

**Failure signs (QA):** black or dark glass/liquids (transmission too low); shadow sides and corners darker and more contrasty than before; colour bleed (e.g. warm floor bounce on walls) disappears; mirrors-in-mirrors go black (glossy too low).

**Cost:** saves time proportional to the energy carried by the removed paths: large in white rooms and glass shots, small in dark/low-albedo rooms. Tuning takes ~5–10 min.

**Conflicts with other sources:** none on the method. Our §4 table gives fixed finals (Diffuse/Glossy 3–4); this card replaces "fixed numbers" with a measured per-scene procedure. Note the author keeps Clamping at defaults (Indirect 10) [cycles_20x_faster@13:15], consistent with ours.

**Test to validate:** a dark bedroom test scene (black walls, sun through blinds): Diffuse 8 → 4 → 2, Glossy 8 → 4. Same frame, same seed, final settings. Measure s/frame and mean luminance + 200% crops of the darkest wall corner and the glossy desk.

**Log:** 2026-11-07 — Extracted from cycles_20x_faster.
