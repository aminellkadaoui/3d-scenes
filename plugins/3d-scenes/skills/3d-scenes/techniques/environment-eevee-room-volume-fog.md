---
id: environment-eevee-room-volume-fog
domain: environment
status: Extracted
sources: [eevee_full_course@62:40, eevee_full_course@63:30, eevee_full_course@65:20, eevee_full_course@76:20]
blender: "5.2"
---
# EEVEE room fog box (near-real-time volumetric shafts)
**Principle:** Volumetrics are EEVEE's strength: froxel volumes give visible sun shafts in near real time, where Cycles volumes are slow and noisy. A box enclosing the room limits the fog to where the camera looks.

**Steps / settings (starting points):**
1. Cube enclosing the room interior; Surface **None**; Volume = **Volume Scatter**, Henyey-Greenstein, **Density 0.05**, Anisotropy 0 (shown) [eevee_full_course@63:30]. Anisotropy 0.3–0.6 for stronger forward-scattered shafts toward camera (repo knowledge `environment-atmosphere.md` §6.3).
2. Render › Volumes: Resolution 1:4 → 1:2 for thin shafts, Steps 64–128, and Shadows › **Volume Shadows ✔** (needed for shafts; it's a checkbox next to the shadow Steps [eevee_full_course@07:40]).
3. Put the fog object in a **"hide before baking"** collection; hide → bake volume probe → unhide [eevee_full_course@65:20].
4. Cost note (transcript): fog added ~0.5 s/frame in his furnished scene.

**Use when:** god rays through blinds/windows, atmospheric interiors, previews of volume looks before a Cycles final.
**Avoid when:** haze is not motivated (dusty air, sun, smoke); haze-everywhere = slop (`ai-slop-diagnosis.md`).
**Failure signs:** blocky/stair-step shafts (volume resolution too coarse); shafts that crawl/flicker in motion; milky lifted blacks (density too high); fog baked into the probe (forgot to hide).
**Cost:** low in EEVEE vs Cycles; resolution 1:2 costs VRAM.
**Conflicts with other sources:** 1MyARLB8KzY uses the same Volume Scatter 0.05 (Cycles) [1MyARLB8KzY@07:00] — agrees.
**Test to validate:** sun through blinds, density 0.02/0.05, volume res 1:4 vs 1:2; shaft edge sharpness vs Cycles reference, flicker over 30 frames.
**Log:** 2026-11-06 — Extracted from eevee_full_course (Blender 4.4).
