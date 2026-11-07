---
id: compositing-pass-rebuild-back-to-beauty
domain: compositing
status: Extracted
sources: [vtdczoXVyvQ@01:00, vtdczoXVyvQ@02:45, vtdczoXVyvQ@04:45, vtdczoXVyvQ@06:15, vtdczoXVyvQ@07:15]
blender: "5.2"
---
# Rebuild the beauty from light passes ("back to beauty")

**Principle:** Cycles' beauty is a sum of light components. Each surface component = (Direct + Indirect) × Color. Rebuilding it yourself lets you adjust one component (fog colour, specular strength, diffuse darkness) without re-rendering.

**Steps / settings:**
1. View Layer › Passes › Light: Diffuse D/I/C, Glossy D/I/C, Transmission D/I/C, Volume D/I (if volumes), Emission, Environment. Data: Denoising Data.
2. Compositor: a node group "Pass Mixer" = (Direct **Add** Indirect) **Multiply** Color. Group defaults: Direct = black, Indirect = black, Color = white (hide values) [vtdczoXVyvQ@04:45].
3. Diffuse group + Glossy group + Transmission group + Volume (D+I) + Emission + Environment, chained with Add (Mix Color › Add, or Math on colour).
4. Verify: Difference against the Image pass ≈ 0 (noisy). Then **Denoise** (Image = rebuilt, Albedo, Normal) at the end [vtdczoXVyvQ@06:15].
5. Example edits: Hue on the volume branch; ×1.3 on the glossy branch for crisper speculars; darken Diffuse Color only.
6. Output: **Group Output** (5.x replaced the Composite node).

**Use when:** you want look-dev flexibility after the render, a client asks for revisions, or you need fog/spec control.
**Avoid when:** EEVEE (lacks the Transmission split and some passes); simple VSL shots; when memory/disk are tight (10+ passes per frame).

**Failure signs:** the rebuild is brighter or washed (a missing Direct/Indirect default is white); a missing component (holdout areas, Shadow Catcher, emission forgotten); double-denoise softness; mismatched alpha.

**Cost:** disk ×5–10; comp time with denoise ~1–2 s per frame on GPU.

**Conflicts with other sources:** none. vtdczoXVyvQ notes that per-pass denoising may help externally but is not proven in Blender.

**Test to validate:** a glass + volume + emissive dot scene. Rebuild difference < 0.5% of mean luminance before denoise.

**Log:** 2026-11-05 — Extracted from vtdczoXVyvQ.
