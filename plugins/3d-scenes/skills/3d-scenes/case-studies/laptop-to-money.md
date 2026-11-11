# Case study — "Laptop → Money" turntable match cut (EEVEE)

Purpose: a 5.3 s shot for a sales video. A laptop with an editing timeline spins on a small turntable stand, speeds up, and at peak speed becomes stacks of dollars, then settles. One working session from idea to full-quality render.

## Timeline of decisions (what happened, in order)
| # | Request / problem | Decision | Result |
|---|---|---|---|
| 1 | Idea frames had bad lighting (void background 0.000, floor brighter than hero) | Use them for the idea only; take quality from a turntable reel and a gallery photo | Brief with labelled refs |
| 2 | Need speed + good lighting | Copied the user's existing laptop project (approved model + lights) instead of a new file | Hours saved |
| 3 | Spin "like the reference stand" | Side table from Poly Haven, split the top as its own mesh, pivot empty | Turntable rig |
| 4 | Floor should reflect like the gallery | Black polished concrete + coat + plane probe; world hidden from camera/glossy | Dark mirror floor |
| 5 | Laptop hung off the edge | Group empty, scale 0.8, centre, snap by vertex min-Z (+8.2 mm) | Fits inside Ø 36.7 cm |
| 6 | Remove back slat wall | Moved to hidden collection; HDRI softboxes appeared → world light-path backdrop | Clean black space |
| 7 | "Mountain" graph + match cut | 2 keys, 75% handles; cut on the peak frame; CONSTANT hide keys | Invisible swap |
| 8 | Money model (user GLB) duplicated | 10 linked duplicates, jittered, 2 leaning on the sides, inside radius | Natural pile |
| 9 | Top should be metal like the reference | Black scratched metal, roughness 0.18–0.30 | Matches ref |
| 10 | Blue back light "light sweep" | Area rims behind, linked to heroes only | Sweep while spinning |
| 11 | Never stop spinning | Drift parent 0.5°/f linear + extrapolation | No dead stops |
| 12 | Half the turns, cut later | 720°→360°, cut 150→180 | Peak 29→14.8 °/f |
| 13 | Camera: low front → rise to my angle | Read user's final pose, crane rig 10°→31° | End pose exact |
| 14 | Screen content | One clean Premiere frame, aspect 1.547 = screen | Correct UI |
| 15 | Shot starts when lid opens | Shifted lid keys to shot start | — |
| 16 | Remove lower shelf | Island split, moved to hidden | — |
| 17 | Money segment as long as laptop segment | 80 + 80 frames, camera end key moved | 160 frames |
| 18 | "Noise / weak quality" | Final EEVEE profile + OIDN; normal maps down; DOF off; temporal off; hard side light | Clean, sharp |
| 19 | Money burnt white, bluish, soap-like | Exclude money from all scene lights; own weak fill 4 W + white sweeps; green-grey paper; sheet lines | Print readable |
| 20 | "Light doesn't work" ×2 | Active-light-only edit; aim error 55°; AgX white-out | Explained + fixed |
| 21 | Render | Copy saved, full quality on a GPU render machine | ≈35–49 s/frame |

## Final numbers
- 1920×1080, 30 fps, frames 100–259 (cut at 180 = 2.67 s).
- EEVEE 256 samples, raytracing 1:1, Fast GI 1:1 × 8 rays, shadows 3 rays/16 steps, motion blur 0.5 × 3 steps, overscan 20%, OIDN.
- Camera 35 mm, 1.26 m from the top, elevation 10° → 31°.
- Spin: drift 0.5 °/f + 360° mountain over frames 130–230, handles 75%.
- Render cost: 35 s/frame (laptop part) → 49 s/frame (fast spin + money) on a 12 GB mid-range GPU. Estimates from tables (2–5 s) were 10× too low.

## What we would do from minute one next time
1. Copy an approved scene; brief in one place.
2. Build the turntable + match cut with the scripts, cut on the measured peak.
3. Light per group with light linking **from the start** (scene / hero A / hero B / table rim).
4. Apply the final EEVEE profile and render one frame early to measure time and noise.
5. Then iterate only on look with the user.

## Session 2 (v2) — the user's revisions and why
| # | Request / problem | Decision | Result |
|---|---|---|---|
| 22 | Camera direction | Reverse the crane: start HIGH on the laptop, come DOWN on the money (swap key values, mirror handle slopes) | Laptop seen from above, money low and heroic |
| 23 | Shots too short | Each shot +25 % (80 → 100 frames); stretch every key around the cut so the spin peak stays on it | 100–199 laptop, 200–299 money |
| 24 | Band of trees / line at the top | Not the render: Material Preview HDRI + floor edge seen by the low camera. Fix = endless floor fade (see `environment-endless-floor-void`) | No horizon edge |
| 25 | Floor invisible | Soft diffuse-only fills; then "less strong, very diffused, fade a lot" | Floor hints, fades to black |
| 26 | "Reflective like the table top" | Keep texture; roughness ≈ the hero top (0.36–0.48). Marble swap + strong round spot were rejected | Soft sheen |
| 27 | Camera framed per element | Stations: closed laptop 100, open laptop 153, money; user framed each by hand (see `camera-hero-framed-stations`) | Hero centred, headroom when the lid opens |
| 28 | Money part longer | Money side +30 % (200–329); split the spin curve at the cut and stretch only the after part | — |
| 29 | Spin "must never stop, linear like a null" | Mistake: replaced the match-cut curve with a linear spin → user: the match cut is gone. Correct = TWO layers: constant slow linear drift (parent, 0.4 °/f, extrapolated) + the mountain match-cut spin (child) with its peak on the cut | Never stops AND whips through the cut |
| 30 | Camera move after the cut | Make the crossing move symmetric around the cut (153 → 247 for cut 200) so its mountain peak lands on the cut, like the spin | Camera + spin peak together at 199.5 |

### v2 numbers
- 100–329 @30 fps, cut 200. Laptop 100 f, money 130 f.
- Spin: drift 0.007 rad/f linear extrapolated + 360° mountain 137.5–262.5 (peak 0.207 rad/f at 199–200).
- Camera: stations 100 / 153 / 247 (rig tilt + camera local position), mountain handles 75 %.
- Floor: 200 m plane, angle fade 0.30→0.02 + radial fade 1.5→8 m to the backdrop colour, roughness 0.36–0.48.
