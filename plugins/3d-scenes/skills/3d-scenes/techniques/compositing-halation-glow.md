---
id: compositing-halation-glow
domain: compositing
status: Extracted
sources: [0M0-TESgB7E@00:30, 0M0-TESgB7E@01:00, lE308jCAT2o@06:15, 1MyARLB8KzY@10:45, uO0GuFuGRQc@01:45]
blender: "5.2"
---
# Motivated glow: Bloom/Fog Glow from true highlights + red halation fringe

**Principle:** real lenses scatter a small fraction of very bright light into the surroundings (veiling glare/bloom). Film adds **halation**, a red-orange fringe around highlights from light reflecting off the film base. Both scale with *highlight energy*. Only regions far above diffuse white (linear > 1) should glow noticeably.

**Steps / settings (5.x compositor, on linear data before any curves):**
- **Bloom/glow:** Glare node · Type **Bloom** (cheap, wide) or **Fog Glow** (more physical in 5.0) · Quality High for finals · Threshold **1.0** (0.8–2.0) · Smoothness 0.1–0.3 · Strength **0.1–0.3** · Size 6–9 (relative scale) · Saturation 1 · Tint white or a slight warm tone.
- **Halation (generic):** a second Glare (Bloom) with Threshold 1.5–3 (only the hottest), small Size, Tint red-orange (≈ #FF4A1A), Strength 0.05–0.15. Or the 0M0 method: (Emission + Environment) → Dilate/Erode **Steps −1** → **Steps +1** (opens away small specks) → Dilate/Erode **Feather, Distance 6, Smooth** → Math Subtract the original → use the ring as the **Fac** of a Mix **Add** whose 2nd input is the halation colour [0M0-TESgB7E@00:51, 01:05] (corrected from frames: ring is a mask, not a multiply).
- Put each in a frame with a **Mix/Switch** for on/off (make the effect optional and adjustable).

**Use when:** visible practical lights, emissive screens, sun/sky in frame, metallic specular glints, night/neon scenes; film look.
**Avoid when:** product packshots on white (glow lowers perceived sharpness and contrast); UI/text renders; scenes without sources brighter than diffuse white (then glow is unmotivated haze).

**Failure signs:** everything glows (threshold too low, e.g. 0.01 [lE308jCAT2o@07:15], corrected from frames); a milky low-contrast image; glow on white walls/backgrounds; halation visible on non-light edges; halos cut off at the frame edge; glare streaks/ghosts without a point source; glow computed on clipped PNG (flat, uniform blobs).

**Cost:** Fog Glow High is slow on large frames (5.1 sped it up). Bloom is cheap.

**Conflicts with other sources:** lE308jCAT2o uses Fog Glow Threshold 0.01 + Ghosts 0.025, blue tint (corrected from frames [lE308jCAT2o@07:45]); the result is visibly milky — an anti-example. 0M0 uses a "very low threshold, mix < 0". In 5.x Mix is replaced by Strength.

**Test to validate:** a night scene with a lamp. Thresholds 0.1 / 1.0 / 2.0 × Strength 0.2. Measure contrast (p95–p5 luminance) loss and blind ranking.

**Log:** 2026-11-05 — Extracted from 0M0-TESgB7E, lE308jCAT2o, 1MyARLB8KzY, uO0GuFuGRQc + Blender 5.2 manual (Glare node).
