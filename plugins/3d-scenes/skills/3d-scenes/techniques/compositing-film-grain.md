---
id: compositing-film-grain
domain: compositing
status: Extracted
sources: [0M0-TESgB7E@01:15, 0M0-TESgB7E@01:30]
blender: "5.2"
---
# Animated, luminance-weighted film grain as the very last step

**Principle:** CG is unnaturally clean. Fine, *moving* grain adds texture, hides banding and denoiser smear, and unifies CG with filmed footage in a VSL edit. Zero-mean noise (×2−1) doesn't shift exposure much. Weighting by the image puts grain where film shows it [0M0-TESgB7E@01:15].

**Steps / settings:**
- **Easiest in 5.2:** Compositor Asset Shelf › **Film Grain** asset (added 5.2) or **Sensor Noise** (5.0). Start at a low amount and judge at 100% on the final delivery resolution.
- **Manual (5.x; the Texture node was removed in 5.0):** White Noise Texture (or Noise Texture, scale high) in the compositor, with the W/seed driven by `#frame` → Math Multiply 2 → Subtract 1 → Multiply by Image (or by a luminance mask) → Mix Add onto the image, Factor **0.02–0.06**.
- Grain size: 1–1.5 px at the delivery resolution. If rendering at 4K for a 1080p delivery, add grain *after* downscaling (in the editor) or it averages away.
- Order: after grade, after sharpening, last before output.
- **Alternative:** add grain in Premiere/Resolve (Resolve Film Grain) so the whole edit shares one grain.

**Use when:** cinematic/film looks; dark gradients that band; matching to camera footage.
**Avoid when:** ultra-clean product or tech/SaaS looks; heavily compressed delivery platforms at low bitrate (grain eats bitrate and turns into macroblocks); before handing EXR to a colourist (they add it).

**Failure signs:** grain frozen between frames (seed not animated → "dirty lens"); grain visible as coloured confetti (too strong chroma); exposure shift; blocking artifacts after H.264 export; grain on top of baked UI/text overlays.

**Cost:** negligible.

**Conflicts with other sources:** 0M0 calls the simple monochrome noise "physically accurate". It is a simplification.

**Test to validate:** a dark gradient shot. Grain 0 / 0.03 / 0.08. Export H.264 at 10 Mbps. Count visible banding vs blocking.

**Log:** 2026-11-05 — Extracted from 0M0-TESgB7E + Blender 5.0 / 5.2 compositor release notes.
