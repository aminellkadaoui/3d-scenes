# 02 — Brief & references (Proven)

## One brief, one place
Users send ideas in pieces across many messages (an idea image, a motion reference, a lighting reference, "the floor should reflect like this"). Before building, consolidate **everything** into one brief and put it where they look (a design board such as Figma + a `brief.md` in the project folder). This stopped contradictions later (e.g. lens choice changed once the space reference arrived).

Brief sections: idea in 2 lines · each reference with **what it's for / what NOT to take from it** · measured numbers · decisions (each with the recipe it came from) · open questions · gaps in the knowledge base.

## Label every reference by its job
Typical split that worked:
| Reference | Use for | Don't use for |
|---|---|---|
| Idea frames (often low quality) | Story, animation beats | Lighting/materials |
| Motion reference (turntable reel) | Spin behaviour, render quality bar | Set dressing |
| Space reference (gallery, studio) | Floor reflection, room scale, light distribution | Props |

## Measure, don't eyeball
Convert references to numbers with ffmpeg + numpy (`scripts/ref_stats.py`):
- Luminance p1 / p50 / p99, region means (top third = background, bottom third = floor, centre box = hero), mean RGB.
- Diagnoses we made from numbers: background = 0.000 → "void" (needs a designed dark backdrop); floor brighter than hero (0.40 vs 0.38) → focal point lost; p99 0.42 → under-exposed; gallery p50 0.68 → high-key target.

## Pulling frames from video references
- Download via the user (private/age-gated Instagram needs their login; don't scrape with their session — ask them to send the file).
- Many 3D reels show Viewport / Render / Timeline stacked: crop **only the render panel** (find it on one full frame, then `crop=w:h:x:y`).
- Contact sheet to choose frames: `ffmpeg -i in.mp4 -vf "fps=2,scale=360:-2,tile=7x4" sheet.jpg`.
- Design boards: Figma does not display WebP uploads — convert to JPG/PNG first.
- ffmpeg not installed? `python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"` gives a bundled binary.

## Screen content (UI on a laptop/monitor)
- Use **one clean frame** (no cursor drag, empty or full timeline as the story needs). Frame 0 of a UI animation is usually clean.
- Match aspect ratio of the screen's UVs (a MacBook screen mapped for 3456×2234 = 1.547). Check `img.size` ratio vs screen; mismatch = stretched UI.
- Keep the screen's existing emission strength from the approved project.
