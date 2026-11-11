---
id: rendering-soft-render-checklist
domain: rendering
status: Proven
sources: [laptop-to-money v2 session 2026-11-11]
blender: "5.2"
---
# "The final render is soft" — checklist (same resolution, nothing that can break the image)

**Problem:** The viewport looks crisp, the rendered frames look soft and the details do not read. The user does not want a higher resolution and does not want risky sharpening. Fix the causes of blur instead of adding sharpening on top.

**Check in this order (each one was a real cause in one shot):**
1. **Output size is exactly the project size.** Read a rendered PNG's size. `Render Region` + `Crop to Render Region` with a border of 0.99999994 gave **1920×1079** on every frame. Any editor then stretches the frame by one line → the whole picture is resampled and soft. Fix: `render.use_border = False`, `use_crop_to_border = False`. Old frames must be rendered again.
2. **Compositor Denoise on an EEVEE render.** OIDN on an already clean 256-sample EEVEE frame only smears texture detail. Mute it; keep it for noisy Cycles frames.
3. **Pixel filter.** `render.filter_size` 1.5 px (default) → 1.0 px. Below 1.0 starts to alias — do not go there when the user wants "nothing that can break".
4. **Motion blur always on.** Key `motion_blur_shutter` so it is 0 on the calm parts and 0.5 only around the fast move / match cut (ramp ~14 frames each side).
5. **Screen / UI textures shown smaller than their size** (a 2000 px screenshot drawn ~600 px wide). `Linear` uses mipmaps → trilinear blur. In EEVEE set the Image Texture to **`Closest`**: no mipmaps, and the render's TAA samples (256) average the texels correctly. Measured on the screen area: +10 % mean gradient, +14 % Laplacian variance, same noise in dark areas. `Cubic` is nearly the same. The viewport looks grainy until samples converge — judge on a rendered frame. No effect on large 8K model textures seen at normal size.
6. **Anisotropic filtering** (Preferences ▸ Viewport ▸ Texture) 2× → 16×. It is a per-machine preference, not saved in the file: set it on the render machine too (in a background render: `bpy.context.preferences.system.anisotropic_filter = 'FILTER_16'` in the job script).
7. **Perception:** on a Retina/HiDPI display the viewport draws at 2× pixel density, so a 1080p render shown scaled always looks softer than the viewport. Compare at 100 % zoom.

**How to test without guessing:** render ONE representative frame per variant in a background Blender (never inside the user's open session), then measure the same crops: mean gradient and Laplacian variance for sharpness, standard deviation of a dark flat area for noise. Keep a change only if sharpness rises and noise does not.

**Avoid:** a Sharpen filter node or filter size < 1.0 when the user asked for safe fixes; raising resolution to hide a blur cause; judging from the viewport or from a compressed preview.
**Honest limit:** detail is capped by how many frame pixels the screen covers, not by the screenshot size — here the laptop screen filled only about 480×410 px of the 1080p frame, so small UI text cannot be readable at that framing. For more: a closer shot of the screen or larger UI elements; a bigger source image does not help.
**Log:** 2026-11-11 — laptop-to-money: 1079-line frames found and fixed; Denoise muted, filter 1.0, motion blur keyed around the cut, screen texture Closest, anisotropic 16×. The user confirmed a big difference after the first three.
