# 42 composition techniques in 8 minutes
- url: https://youtu.be/HBWYieo5RmU
- channel / duration / Blender version shown: Liam S. Photography / ~8:40 (transcript ends [08:30]) / n/a (photography video, not Blender)
- domain(s): composition (primary), color, lighting (chiaroscuro / key), camera (point of view)
- evidence used: transcript + 3 contact sheets (one tile / 15 s) + 9 extracted frames (see §6); example photos now described there. Some technique names are garbled by captions ("Chiroso" = chiaroscuro, "Triic" = triadic, "Hukosition" = juxtaposition, "Center eye dominance" = centre-eye/dominant-eye placement).
- trust: medium. Accurate glossary-level definitions, but ~11 s per technique: no hierarchy of importance, no failure cases, presents rules of thumb (golden ratio "discovered in nature", rule of odds) as if equally valid. Treat as a checklist of vocabulary, not a method.

## 1. Problem it solves
Composition advice is scattered across dozens of named "rules". The video enumerates them. Value for us: a shared vocabulary for briefing and critiquing 3D frames, plus a few techniques that directly fix common CG problems (no depth layering, centered everything, no lead room, flat value structure).

## 2. Techniques (grouped; each is a vocabulary item with 3D applicability)

### T1 — Placement grids: golden ratio / phi grid, rule of thirds, golden triangle `[00:15]–[00:30]`, `[01:45]`
- What: place subject on intersections; golden triangle = diagonal + perpendiculars from corners; align elements with diagonals.
- Blender: Camera data ▸ Viewport Display ▸ Composition Guides: Thirds, Golden Ratio, Golden Triangle A/B, Harmonious Triangle A/B, Center, Center Diagonal, Safe Areas.
- Use as: tools to test off-center placement, not laws. The golden-ratio-in-nature claim [00:15] is popular myth-adjacent; its value here is simply "off-center ≈ 0.38/0.62".
- Status: Extracted

### T2 — Symmetry vs asymmetry `[00:30]–[00:45]`
- Symmetry (reflections as mirror) for formal/monumental/product hero; asymmetry balanced by equal visual interest.
- 3D: dead-center symmetry is legitimate for hero product/architecture but must be *exact* (camera on axis, Shift instead of tilt); near-symmetry reads as a mistake.
- Status: Extracted

### T3 — Rule of odds `[01:00]`
- Odd groups (3, 5) feel more dynamic than even. 3D: when scattering props (bottles, spheres), group in 3s with varied scale/spacing.
- Status: Extracted

### T4 — Fill the frame vs negative space `[01:00]–[01:30]`
- Fill = get closer; negative space = scale, isolation. 3D/VSL: negative space is also where titles go.
- Status: Extracted

### T5 — Rule of space (lead room / look room) `[01:30]`
- Leave space in the direction the subject looks or moves. Violating it creates tension [05:45].
- Status: Extracted

### T6 — Framing within the frame `[01:30]–[01:45]`
- Doors, windows, arches. 3D: cheap foreground geometry (door frame, foliage card, shelf edge) at the frame edge, often slightly defocused.
- Status: Extracted

### T7 — Centre-eye dominance (portraits) `[02:00]`
- Put the camera-nearer eye at horizontal centre. 3D: character close-ups.
- Status: Extracted

### T8 — Lines: leading, implied, converging, diagonal, horizontal, vertical, S/C curves `[02:15]–[03:15]`
- Leading lines point to subject; implied lines from arrangement/gaze; converging lines create depth even without subject; diagonals = movement (parallel) / tension (opposed); horizontals = calm; verticals = strength; S-curve = elegance/flow; C-curve = harmony.
- 3D: design set geometry (floor seams, cables, table edges, light streaks) to point at the product.
- Status: Extracted

### T9 — Geometric shapes / shape language `[03:15]`
- Triangles = stability or tension; circles = harmony; rectangles = order.
- Status: Extracted

### T10 — Point of view: high / low / eye level `[03:30]–[03:45]`
- From above = small/vulnerable; from below = huge/powerful; eye level = natural/connection.
- 3D: camera height is a storytelling choice; a random height is a slop sign.
- Status: Extracted

### T11 — Foreground / middle / background + overlapping elements `[03:45]–[04:00]`
- Using all three planes creates depth; overlap is another depth cue.
- 3D: the single biggest fix for "floating product in void" renders.
- Status: Extracted

### T12 — Scale contrast and leading foreground interest `[04:00]–[04:15]`
- Tiny vs huge; an interesting foreground object/pattern that guides the eye in.
- Status: Extracted

### T13 — Visual balance and visual weight `[04:30]–[05:00]`
- Balance ≠ mirror. Small bright/saturated area balances a large dark one; busy/detailed areas carry weight; elements near frame edges weigh more than at center ("even showing a little bit of a tree at the edge can balance the scene") [04:45].
- Status: Extracted

### T14 — Repetition, breaking the pattern, flow/visual path `[05:00]–[05:30]`
- Rhythm from repeated shape/color; the odd one out draws attention instantly (great for "the one product that's different" VSL shots); flow = combining tools into a path for the eye.
- Status: Extracted

### T15 — Dynamic tension `[05:30]–[05:45]`
- Opposing diagonals, violated lead room, shapes about to collide.
- Status: Extracted

### T16 — Light-structure compositions: chiaroscuro, high key, low key, silhouette `[06:00]–[06:45]`
- Chiaroscuro = strong local light/dark contrast; high/low key = overall brightness, not extreme contrast; silhouette = backlight with dark subject.
- Status: Extracted (cross-ref lighting)

### T17 — Color compositions: complementary, analogous, triadic, warm/cool, color dominance, monochrome, pop of color `[06:45]–[07:45]`
- Pop of color = mostly neutral image + one saturated accent → strongest eye magnet. Color dominance/monochrome shift attention to shape and light.
- 3D/VSL: brand accent color reserved for the subject only.
- Status: Extracted (cross-ref color)

### T18 — Juxtaposition, storytelling, minimalism `[08:00]–[08:15]`
- Juxtapose opposites (old/new); arrange elements to imply narrative; minimalism = remove anything that doesn't add.
- Status: Extracted

## 3. Claims I doubt or must test
- Golden ratio "discovered in nature ... even galaxies" [00:15]: oversold; no evidence phi placement beats thirds perceptually. Treat both as "off-center".
- Rule of odds [01:00]: weak heuristic; real effect is avoiding pairs that split attention equally.
- "Elements near the edge of the frame feel heavier" [04:45]: established in visual-weight literature (Arnheim's lever principle) — useful.
- Complementary colors "on the RYB color wheel" [06:45]: painters' wheel; in RGB/digital, complements differ (e.g. blue ↔ yellow vs blue ↔ orange). Use as rough guide.

## 4. Anti-AI-slop lessons
- AI-slop frames tend to be centered, mid-height, evenly lit, all-in-focus, single-plane, with saturated color everywhere. Nearly every item in this list is a counter: off-center placement, lead room, fore/mid/background, overlap, value contrast, one pop of color, negative space.
- Pick 2–3 techniques per shot deliberately; stacking 10 is its own kind of slop.

## 5. Candidate isolated test
Product on table, same lighting. A: camera at default height centered, subject in middle, no foreground. B: subject on right third with lead room, defocused foreground prop on left edge, background wall darker than subject, accent color only on product. Metrics: grayscale squint test (is the brightest-contrast region on the subject?), 5-second "what do you look at first" test with 3 viewers, thumbnail at 160 px readability.

## 6. Visual verification (frames viewed)
Format seen: talking head in a forest alternating with full-screen example photos on a crumpled-paper background and black title cards ("18. S & C CURVES", "28. FLOW / VISUAL PATH", "29. DYNAMIC TENSION", "32. SILHOUETTE", "36. WARM VS COOL COLORS"). Examples are mostly stock-style photos; no diagrams beyond a red thirds grid and red circles.
- Sheet tiles: [00:30] hedgehog with red rule-of-thirds grid (T1); [00:45] symmetric vs asymmetric tree icons (T2); [01:00] hills with three trees (rule of odds, T3); [01:30] chamois facing right with a box labelled "EXTRA SPACE" (T5); [02:00] portrait (T7); [02:15] red railing leading to a walking figure (T8 leading lines); [02:45] power pole diagonal (T8); [04:00] pyramids (shapes/scale); [04:15] glowing tree with circled flowers (T12); [04:30] lone rock against a star field (T13 visual weight); [05:00] Flatiron building low angle (diagonal/dynamic); [05:45] hooded figure on a B&W beach (minimal/negative space); [07:00] colour wheel; [07:30] teal fog forest and [07:45] blue fog landscape with a 4-swatch monochrome palette (T17); [08:15] dark brick corridor (low key).
- [01:40] Motorbike drag racer, panning shot with blurred background, bike placed left with lead room to the right (T5). 
- [03:55] Valley photo with the "Foreground" band outlined in red (T11).
- [04:20] Mountain lake with white flowers circled as leading foreground interest (T12).
- [04:40] Two identical rocks on a star field — balance demo (T13).
- [07:25] Three swatches blue / green / purple = analogous colours (T17).
- [08:15] Red-sailed junk boat in front of a desaturated Hong Kong skyline — juxtaposition (old/new) + pop of colour (T18/T17).
- [05:45], [06:20], [06:35] talking head only (no example on screen at those exact times).
- Quality judgement: examples are **competent stock-level photography**, clear but generic; it's a vocabulary list, not a deep method. Trust unchanged (medium).
- **Best translations to 3D VSL shots:** (1) lead room + panning motion blur [01:40] → product/vehicle moving across frame with camera tracking, motion blur on, space ahead for the overlay text; (2) FG/MG/BG layering [03:55] and leading foreground interest [04:20] → a defocused foreground prop in the lower band of a product shot (cheap depth for any 3D set); (3) pop of colour / juxtaposition [08:15] → desaturated environment with the single accent colour reserved for the product or brand; (4) monochrome fog palette [07:30]–[07:45] → atmospheric establishing shots with one value family (easy volume + grade); (5) leading lines [02:15] → set geometry (rails, table edges, light strips) pointing at the product. Weak for VSL: rule of odds, centre-eye dominance, golden-ratio overlays.
