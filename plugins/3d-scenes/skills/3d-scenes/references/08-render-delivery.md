# 08 — Render & delivery (Proven)

## Estimate by measuring, never by tables
| Source | Estimate per frame | Reality |
|---|---|---|
| Knowledge-base table (simple/furnished room, EEVEE, 128 samples) | 1–5 s | — |
| This scene at 128 samples (before quality pass) | "2–5 s" | not measured |
| **Final profile** (07) on a 12 GB mid-range GPU, 1080p | — | **≈34–36 s/frame** (first frame 47 s: shader compile) |

160 frames ≈ 95 min + ProRes encode. The quality profile (256 samples, Fast GI 1:1 ×8 rays, motion-blur 3 steps, raytracing 1:1, plane probe) multiplied cost ~10×.
Rule: render **one** frame with the final profile, read its time, multiply, add ~5% and encode time. Tell the user the clock time it will finish (`date`).

## Running the render
- The user asks → save a **copy** of the scene (`save_as_mainfile(copy=True)`), submit the copy; the user's open file stays as is.
- EEVEE needs an OpenGL/GPU session. Headless farms often only do Cycles — check. On a remote Windows box with a logged-in session EEVEE worked (OPTIX device listed but EEVEE uses the GPU via OpenGL).
- Logs may print the **Cycles** sample count even for EEVEE jobs — verify `scene.eevee.taa_render_samples` instead.
- Frames as PNG sequence (resumable), then encode.

## Deliverables
- Full quality only: 100% resolution, the scene's samples, **PNG frames + ProRes 4444 XQ** (or 422 HQ). MP4 only as a preview link.
- Frame range and fps must match the edit (30 fps here). Shot length in seconds = frames / fps; tell the editor the cut frame in seconds too (frame 180 of 100–259 = 2.67 s in).
