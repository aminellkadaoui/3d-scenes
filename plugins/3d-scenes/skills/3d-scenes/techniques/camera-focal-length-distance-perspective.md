---
id: camera-focal-length-distance-perspective
domain: camera
status: Extracted
sources: [dFK3C83k4Wo@00:45, HBWYieo5RmU@03:30, expert knowledge]
blender: "5.2"
---
# Choose focal length and camera distance deliberately (perspective = position)

**Principle:** Perspective (how big near things look relative to far things) is set only by camera *position/distance*. Focal length only sets field of view (how much is cropped). Long lens + far camera = compressed, flattering, low-distortion (premium product, portraits) [dFK3C83k4Wo@00:45 uses 90 mm for a product orbit]. Wide lens + close camera = exaggerated depth, dynamic, immersive, distorts objects near frame edges. Blender's default 50 mm placed wherever the viewport happened to be is a slop signature.

**Steps / settings (starting points, 36 mm sensor, Sensor Fit Auto):**
| Shot | Focal | Horizontal FOV |
|---|---|---|
| Wide environment / establishing / interior | 18–28 mm | 90°–65° |
| Natural "you are here" / medium wide | 28–40 mm | 65°–48° |
| Medium / person waist-up | 40–60 mm | 48°–33° |
| Portrait / product hero | 70–105 mm | 29°–19° |
| Telephoto compression / detail / stacked background | 135–300 mm | 15°–7° |
1. Decide the perspective you want first, place the camera at that distance, then pick focal length to frame.
2. Camera height: eye level 1.5–1.7 m for human-perspective scenes; tabletop products: camera slightly above product top (10–30° down-angle) — or at product mid-height for heroic.
3. FOV formula: hFOV = 2·atan(36 / (2·f)).
4. Keep camera roll 0 unless deliberate (Dutch angle).

**Use when:** setting up every camera.
**Avoid when:** n/a.

**Failure signs:** stretched/"bulging" objects near frame edges (wide lens too close); background showing too much empty world (lens too wide for product); flat lifeless environment (too long for a space that should feel immersive); camera at a strange height (e.g. 0.8 m in a room, or floating at 3 m) with no story reason; lens changes between consecutive shots with no motivation.
**Cost:** none.
**Conflicts with other sources:** none.
**Test to validate:** same framing of a product from 0.5 m @24 mm vs 2.5 m @100 mm; compare distortion and background.
**Log:** 2026-11-05 — Extracted from dFK3C83k4Wo + expert knowledge.
