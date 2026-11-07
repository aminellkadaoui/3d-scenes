# 06 — Camera & motion (Proven)

## Camera
- Let the user frame the final angle themselves in the viewport, then **read it back as numbers**: aim point (closest point of the view ray to the hero axis), distance, azimuth, elevation. Build the move around that end pose — the last frame must equal their angle exactly.
- Lens that worked for a hero on a stand in a dark space: 35 mm at ≈1.26 m from the top (subject fills the frame, little distortion).
- DOF: turn **off** unless asked. In EEVEE it adds noise and the user found it reduced perceived quality.

### Crane up ("start low in front, rise slowly")
`scripts/camera_crane.py`
- `CAM_Rig` empty at the aim point; camera child at (0, −D, 0), rotation (90°,0,0); rig rotation Z = azimuth, X = −elevation.
- Animate rig X from −10° (near table level) to −31° (user's angle) over the whole shot.
- Ease: Bezier, handles = 1/3 segment with **half the average slope** (gentle, never 0 speed), Linear extrapolation → no dead stop at either end.

## Turntable spin ("المعدنة تدور والأوبجكت معها")
`scripts/turntable_rig.py`
- Separate the top that spins (03 §Splitting). `Turntable_Pivot` empty at the top surface centre; top + heroes parented to it.
- **Two layers**:
  1. `Turntable_Drift` (parent): constant slow spin, LINEAR keys + Linear extrapolation, 0.5°/frame (one turn per 24 s at 30 fps). Never stops, before or after the shot.
  2. `Turntable_Pivot` (child): the "mountain" speed graph — 2 keys, FREE handles of **75% segment length** on both (the After Effects Speed graph In/Out 75%). Speed peaks in the middle.
- Sample speed per frame and print a table (deg/frame) — this is how you verify the graph, not by looking at curves.

Numbers that were approved:
| Turn | Segment | Peak speed | Felt |
|---|---|---|---|
| 720° | 100 frames | 29 °/f | too much, user halved it |
| **360°** | **100 frames** (130→230) | **14.8 °/f at the middle** | approved |

## Object match cut ("متش كت")
`scripts/match_cut.py`
- Cut frame = peak-speed frame of the pivot curve (verify from the speed table, e.g. frame 180).
- Object A (all descendant meshes): `hide_render` + `hide_viewport` keyed visible at cut−1, hidden at cut. Object B: the opposite. **CONSTANT** interpolation.
- Object B lives under a `<Swap>_SLOT` empty parented to the pivot, so it spins with the same motion.
- Motion blur on (shutter 0.5, EEVEE steps 3) hides the swap.
- Moving the cut later: shift the spin keys **and** every hide key by the same offset; move the timeline marker.
- Equal halves: user asked the "after" part to last as long as the "before" (80 + 80 frames). Extend the end frame and move the camera's last key to it.

## Other animation
- Existing animation in the copied project (laptop lid opening) can be retimed: shift its keys so the shot starts as it opens (shot start = lid start).
- Per-light energy keys at the cut (CONSTANT) are possible but were a weak fix — prefer separate light linking per group (05).
