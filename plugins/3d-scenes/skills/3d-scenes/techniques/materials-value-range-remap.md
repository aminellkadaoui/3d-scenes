---
id: materials-value-range-remap
domain: materials
status: Extracted
sources: [RfPro3hlOMg@02:30, RfPro3hlOMg@03:15, 8HfKtaDx6tM@05:00, 8HfKtaDx6tM@08:00]
blender: "5.2"
---
# Remap texture values into physically plausible ranges (Map Range / Color Ramp)
**Principle:** Procedural and grayscale textures output 0–1. Real material properties live in narrow bands (roughness of one surface rarely spans more than ~0.3; albedo of real materials sits ~0.03–0.9 linear). Feeding raw 0–1 into roughness/colour creates chrome-and-chalk patches and pure black/white areas that don't exist physically.

**Steps / settings (starting points):**
1. Texture (Fac) → **Map Range** (Linear, Clamp on): From 0–1 → To e.g. 0.45–0.7 for a semi-matte surface. Use **Color Ramp** when you need shaping/visual feedback (author prefers it; Map Range computes slightly faster [RfPro3hlOMg@03:15]).
2. To make a scanned roughness glossier while keeping variation, lower the ramp's white stop / To Max instead of overwriting the map [8HfKtaDx6tM@08:00].
3. For masks between two materials that cannot coexist (paint vs mud), compress the ramp (stops close together) to get crisp transitions [RfPro3hlOMg@07:45].
4. Check with Node Wrangler Ctrl+Shift+Click preview: the mask/value should not be pure 0/1 over large areas unless intended.

**Use when:** every procedural texture → shader input; every downloaded roughness map that doesn't match reference gloss.
**Avoid when:** binary properties (Metallic for a clean metal/dielectric split should be 0 or 1 — remap *to* binary there).
**Failure signs:** mirror-like and chalky spots on the same surface; contrast in roughness much higher than reference; "noise" visible as blotches in highlights.
**Cost:** negligible.
**Conflicts with other sources:** none; RfPro3hlOMg's "roughness 0 makes no sense" is too absolute — polished glass/chrome ~0.02–0.08 is valid.
**Test to validate:** noise into roughness raw vs remapped 0.3–0.6 on a sphere in HDRI; blind preference.
**Log:** 2026-11-05 — Extracted from RfPro3hlOMg, 8HfKtaDx6tM.
