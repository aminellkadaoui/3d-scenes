---
id: camera-handheld-noise-modifier
domain: camera
status: Extracted
sources: [expert knowledge + Blender manual (Graph Editor ▸ F-Curve Modifiers ▸ Noise); no video in this batch demonstrates it]
blender: "5.2"
---
# Subtle handheld / "operated" feel with the F-Curve Noise modifier

**Principle:** Perfectly stable, mathematically smooth CG cameras read as synthetic. A real handheld or even tripod/slider camera has low-frequency drift and micro-rotation. Small, low-frequency rotational noise (not positional jitter) mimics an operator. It must be subtle: viewers should feel it, not see "shake".

**Steps / settings (starting points, assume 24–30 fps, camera 2–5 m from subject):**
1. Put the noise on a separate layer so it doesn't fight your main move: camera → child of a `Shake` Empty → child of the move rig (or add noise directly to the camera's rotation channels if the camera itself has no rotation keys).
2. The channel needs an F-curve: key Rotation X and Z once (or Y for roll) on the shake Empty.
3. Graph Editor ▸ Sidebar (`N`) ▸ Modifiers ▸ Add Modifier ▸ Noise, on Rotation X (tilt) and Z (pan); optional very small on Y (roll).
4. Values: Blend Type Replace or Add; Scale 30–80 (frames per wobble — larger = slower); Strength 0.005–0.02 rad for rotation (~0.3–1°) — start at the low end; Phase different per channel (e.g. 1, 7, 13) so axes don't move in sync; Depth 0–1 (adds finer detail; Lacunarity/Roughness only matter when Depth > 0).
5. Restrict Frame Range with Blend In/Out to fade shake in/out at shot boundaries; Influence to dial overall amount.
6. For "breathing" tripod feel: Scale 100+, Strength 0.002–0.005 rad, only on tilt/pan.
7. With long lenses the same angular noise looks larger on screen — reduce Strength roughly in proportion to focal length (e.g. half at 100 mm compared to 50 mm).

**Use when:** documentary/real-world feel, environments meant to look filmed, POV, tension beats; also to break the "frozen" look of a static hero frame.
**Avoid when:** clean product/tabletop commercial (those are shot on motion-control rigs — stable is correct); orthographic/infographic shots; while text overlays must be read (noise behind text makes it look jittery relative to the graphic layer unless the graphic is tracked).

**Failure signs:** visible jitter at frame level (Scale too low → high frequency); seasick drift (Strength too high); horizon wobbling via roll; noise identical on all axes (diagonal "nodding"); shake that starts/stops abruptly at the cut; motion blur absent so jitter strobes.
**Cost:** zero render cost.
**Conflicts with other sources:** none in batch.
**Test to validate:** 5 s static shot, A no noise vs B noise (Scale 50, Strength 0.008). Blind viewers rate "filmed vs CG"; measure max screen-space offset of subject (should stay < ~1 % of frame width).
**Log:** 2026-11-05 — Extracted from expert knowledge + Blender manual F-Curve Modifiers page.
