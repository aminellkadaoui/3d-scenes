# Case study — screen/UI shots in a dark editor's room (VSL, EEVEE)

**Purpose:** a 30-second sequence in which the camera lives on a monitor that plays a Premiere-style UI animation made of 5 clips (compare, frame by frame, sound design, effects, cut detection), plus fixing the rest of a multi-scene project and switching it from Cycles to EEVEE.

## Decision timeline
| Step | What the user asked | What worked |
|---|---|---|
| Engine | "Cycles takes too long" | EEVEE tuned to Cycles: Shadow Jitter, fitted light strengths, fake-bounce fills, compositor OIDN → 34 s vs 223 s/frame |
| Noise/flicker | "there is noise / shaking" | Measured: render stable; shake = camera float. Kept settings; removed ideas that measured worse (Jittered DOF) |
| Quality complaints | "final quality is weak" | It was the compressed MP4 preview → deliver PNG + ProRes 4444 XQ only |
| Scene order | Merge/rename scenes in English, leave others in Arabic | Linked copies for new scenes; delete only after checking no shared objects |
| Screen colours | "the screen is too dark" | Separate shader path for plain videos vs LUT-baked videos |
| Camera language | "mountain graph", "peak at the click", "peak on the cut" | Peak Zoom: 30 f mountain move centred on the key frame; across cuts on both cameras |
| Framing | User framed in camera view and said "كذا" | Read transform immediately; apply as the hold pose; transitions into/out of it |
| Tracking | "track the cursor, keep the clip centred" | Cursor-tip delta, parallel to the screen, per-axis clamp |
| Timing | "cut the screen here" | Trim the UI clip itself with ffmpeg (concat -c copy), shift later cameras |
| Previews | "render in this mode, flat, but I need the screen" | Workbench FLAT + Texture + sRGB movie in a copy, ~1 min for 900 frames |

## What we'd do from minute one
1. Analyse the UI video with agents (cuts, cursor tip per frame, panels) before touching cameras.
2. Ask the user to frame each shot by hand in camera view; capture each pose immediately.
3. Build one camera per clip: Peak Zoom on the cut → hold or cursor tracking → Peak Zoom on key clicks.
4. Fast Workbench preview after every change; final EEVEE only when approved.
5. Deliver ProRes 4444 XQ.
