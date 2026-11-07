# 7 Tips & Tricks to CONQUER PHOTOREALISM I wish I had known!
- url: https://youtu.be/SaZOuHQROIg
- channel / duration / Blender version shown: Blender Breakdown / 5:29 / Blender 3.x (uploaded 2023-08-07)
- domain(s): materials | assets-modeling | lighting | color
- evidence used: transcript + contact sheet 01 + 6 extracted frames from the 480p mp4 (see §6).
- trust: low-medium. Beginner-level list; correct basics (HDRI, bevels, imperfections, PBR, light temperature) but one outdated tip (Filmic Log in place of a view transform); the "HDRI strength 1000" was a caption error — screen shows 1.000 (corrected from frames).

## 1. Problem it solves
"Something gives away that it's a render": flat textures, bad lighting, computer-generated look [SaZOuHQROIg@00:00].

## 2. Techniques

### T1 — HDRI lighting  `[00:15–00:45]`
- Poly Haven HDRI 4–8K, World ▸ Color ▸ Environment Texture. "Strength 1000" [00:45] — (corrected from frames [00:47], [01:55]) the on-screen World Strength is **1.000**; "1000" is a caption misreading. Set exposure by camera/Film exposure.
- Status: Extracted

### T2 — Bevel modifier everywhere; apply scale first  `[01:00–01:30]`
- Sharp edges are rare except knives [01:00]. If bevels vary per edge, it's non-uniform object scale → **Ctrl+A ▸ Scale** then bevels become even [01:15].
- Status: Extracted

### T3 — Surface imperfections multiplied into roughness  `[01:30–02:15]`
- Imperfection image (Megascans) → Mix node (**Color** type, **Multiply**): A = roughness map, B = imperfection → Principled Roughness.
- Note: Multiply only darkens → only makes surfaces *glossier* where the imperfection map is dark. Most smudge maps are dark background + light smudges, so Multiply mostly lowers roughness everywhere except smudges. Better: Map Range the imperfection into e.g. 0.9–1.3 and multiply, or use Mix (Lighten/Overlay) with factor 0.3–0.6. Test.
- Status: Extracted

### T4 — Tonal range / Filmic Log  `[02:15–03:00]`
- Explains dynamic range / clipping well; recommends Filmic Log + manual exposure/gamma. Blender 5.2: **AgX** (default since 4.0) already provides wide range and graceful highlight roll-off; use Look (e.g. Medium/High Contrast or Punchy) instead of Log + gamma. Filmic Log is a grading base, not a final look.
- Status: Extracted

### T5 — Download assets for small objects  `[03:00–03:15]`
- Modelling every small object yourself → you give up or each looks less real. Free assets often equal paid quality.
- Status: Extracted

### T6 — Light temperature via Blackbody  `[03:15–04:00]`
- Light nodes ▸ Blackbody → Emission colour. Warm ~4000 K, cool ~6000 K+ [03:45]. Blender 4.x/5.x: lights have a native **Temperature** colour mode in light properties — no nodes needed (and works in EEVEE).
- Status: Extracted

### T7 — PBR maps explained  `[04:00–05:00]`
- Albedo, roughness (black = glossy, white = rough), normal (purple = flat) maps from Poly Haven / Megascans.
- Status: Extracted

## 3. Claims I doubt or must test
- ~~HDRI strength 1000~~ (frames: 1.000); Filmic Log as final look [02:45]; Multiply-only imperfection blend.

## 4. Anti-AI-slop lessons
- Bevels + imperfections + PBR + non-white light are baseline hygiene. Uneven bevels = unapplied scale (a QA check).

## 5. Candidate isolated test
Rounded cube & phone-like slab, HDRI. A: no bevel, uniform roughness 0.4. B: bevel 2 mm (2–3 segments, scale applied). C: B + imperfection roughness (Multiply vs Overlay variant). Measure highlight on edges, believability.

## 6. Visual verification (frames viewed)
Frames viewed: contact sheet 01, plus extracted frames below. **Blender 3.6.0** (status bar at [02:50]).
- [00:47] World ▸ Surface: Use Nodes, Background, Color socket being set via the node menu (Environment Texture), Strength field shows **1.000**.
- [01:55] HDRI loaded (blurred outdoor HDRI in viewport), World **Strength 1.000**. (corrected from frames) The "HDRI strength 1000" in the transcript is almost certainly the auto-caption reading "1.000" as "one thousand"; on screen the strength is the default 1.0. A Node Wrangler PBR setup is visible below (values unreadable at 480p), so the Multiply-into-roughness step remains transcript-only.
- [02:50] **Confirms T4:** Color Management View Transform **Filmic Log**, Look None, Exposure 0.000, Gamma 1.000 — the image is shown washed-out (the Log base, before any exposure/gamma tweak).
- [03:02] "FILMIC LOG" result: console table, lamp, plant, abstract painting — clean archviz still, neutral grey palette. Looks professional but is a stock-asset arrangement with soft, low-contrast light.
- [03:50] Light node tree: Emission → Light Output, node search open to add Blackbody — confirms T6 (node-based method, 3.6 era).
- Final quality judgement (sheet 01 [00:00] stool, [03:00] bedroom, [03:02]): clean, competent beginner/intermediate archviz; nothing slop-ish but nothing beyond basics. Trust stays low-medium; tips are hygiene, not technique.
