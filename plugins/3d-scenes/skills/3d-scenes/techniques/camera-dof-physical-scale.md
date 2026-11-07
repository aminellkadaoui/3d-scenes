---
id: camera-dof-physical-scale
domain: camera
status: Extracted
sources: [expert knowledge + Blender manual (Cameras ▸ Depth of Field); no video in batch]
blender: "5.2"
---
# Depth of field that matches real-world scale (avoid miniature look)

**Principle:** Blender's DoF is physically based: blur depends on F-Stop, focal length, focus distance and the *scene scale in meters* (sensor 36 mm default). A real 1.8 m person at 3 m with 50 mm f/2.8 has a modest background blur. Very low F-Stops (0.1–0.8) on a correctly-scaled scene simulate apertures that don't exist on normal lenses and produce extremely thin focus planes — the eye reads that as a macro shot of a *small* object → "tilt-shift miniature" look. Same happens if the scene is built at wrong scale (a 10 cm "car").

**Steps / settings (starting points):**
1. Verify scale first: Unit Scale 1.0, objects at real dimensions (N panel ▸ Dimensions).
2. Camera ▸ Depth of Field ON. Focus Object = an Empty placed at the point that must be sharp (eyes, product logo) — animate the Empty for rack focus. Or Focus Distance (use the eyedropper).
3. F-Stop starting points: people/environment medium shot f/2.8–5.6; product hero at 0.5–1 m f/2.8–8 (product must be fully sharp front-to-back unless stylized); wide environment f/5.6–11 (essentially deep focus); extreme close-up/macro f/4–16 (thin focus is already strong). Real cinema lenses rarely go below f/1.4.
4. Bokeh: Aperture ▸ Blades 6–9 (0 = perfect circle), Rotation to avoid axis-aligned polygons, Ratio 1 (spherical); Ratio < 1 / > 1 simulates anamorphic oval bokeh — only for an intentional anamorphic look, then also use 2.39:1 aspect.
5. Viewport: Camera view + Viewport Shading Rendered (EEVEE shows DoF; Cycles viewport too) to judge.

**Use when:** to separate subject from background, to guide the eye, rack focus beats.
**Avoid when:** product shots where the whole product must read; wide establishing shots; when text/UI is the focus; "everywhere by default".

**Failure signs:** miniature/toy look; only a sliver of the hero in focus (front of product sharp, back mushy); focus on the wrong object (nose instead of eyes, background instead of product); DoF breathing/popping during focus pulls; hard halo edges in EEVEE around foreground objects; very blurred foreground cards with visible geometry edges.
**Cost:** Cycles: almost free (converges with samples). EEVEE: DoF jitter/samples increase cost.
**Conflicts with other sources:** many tutorials recommend f/0.1–1 for a "cinematic" look; that only works when the scene is unrealistically scaled or for macro intent. Record when encountered.
**Test to validate:** 1.8 m figure at 3 m, 50 mm: render f/0.4, f/1.4, f/2.8, f/8. Blind "is this a miniature?" check; compare with real-photo references of same framing.
**Log:** 2026-11-05 — Extracted from expert knowledge + Blender manual Cameras page.
