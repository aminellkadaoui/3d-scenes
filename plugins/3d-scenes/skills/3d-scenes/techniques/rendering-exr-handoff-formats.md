---
id: rendering-exr-handoff-formats
domain: rendering
status: Extracted
sources: [gmGMsKJ6xd8@07:45, gmGMsKJ6xd8@09:00, vtdczoXVyvQ@01:45, vtdczoXVyvQ@22:00]
blender: "5.2"
---
# Output format strategy: EXR for comp, ProRes/PNG for the edit

**Principle:** an 8-bit display-referred file (PNG, H.264) throws away everything above display white and quantises gradients. Glow, exposure changes and grading then clip and band. EXR keeps scene-linear floating-point data, so post effects behave like optics. The edit, however, needs a file Premiere or Resolve can play with the look already baked in.

**Steps / settings:**
- **Comp master (archival):** Output › File Format **OpenEXR MultiLayer**, Color Depth **Half (16-bit float)**, Codec **DWAA** for beauty and light passes [vtdczoXVyvQ@01:45]. Use a *separate* File Output (or a second render) with **ZIP/PIZ + Float (Full)** for Cryptomatte, Depth/Z, Position, Normal, Vector (lossy codecs corrupt IDs and depth).
- **Edit-ready (Premiere/Resolve timeline):** render a PNG 16-bit RGB(A) image sequence (safest, resumable after a crash) and convert to **ProRes 422 HQ** (or 4444 when alpha is needed, via Resolve/Media Encoder). Or render FFmpeg › QuickTime › ProRes directly. Blender's manual lists ProRes as 8/10-bit, no alpha in Blender's table, so use PNG RGBA for alpha.
- **Never** render animation straight to H.264 for editing: a crash loses everything, and it is lossy and 8-bit.
- Always render **image sequences** for long renders (resume with Overwrite off + Placeholders).
- In the VSE re-assembly path [gmGMsKJ6xd8@08:45]: match the scene's resolution, fps and Color Management, add the image strip, add the **Compositor** strip modifier (5.0+) for glare.

**Use when:** EXR for any shot that will get glow, grade or comp work, or client revisions. PNG/ProRes for "final pixels" delivery to the editor.
**Avoid when:** EXR multilayer for an editor without a comp step. Premiere handles EXR slowly and without the view transform, so it will look dark and flat.

**Failure signs:** EXR in Premiere looks washed out or too dark (no view transform applied); banding in sky gradients from 8-bit; Cryptomatte mattes with garbage edges (DWAA used); colour or gamma shift between Blender and QuickTime player (macOS ColorSync tag issue; check in Resolve instead).

**Cost:** EXR half DWAA ≈ PNG 8-bit size; EXR full ZIP ≈ 4–8× larger.

**Conflicts with other sources:** gmGMsKJ6xd8 claims EXR is faster to save than PNG. Plausible (PNG compression is slow at high levels), but unmeasured.

**Test to validate:** render one frame to PNG8, PNG16 and EXR-half. Apply Glare (Bloom, threshold 1.0) and +2 stops exposure to each. Compare highlight bloom shape and banding.

**Log:** 2026-11-05 — Extracted from gmGMsKJ6xd8, vtdczoXVyvQ + Blender 5.2 manual (Video formats table).
