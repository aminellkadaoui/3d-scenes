---
id: camera-hero-framed-stations
domain: camera
status: Proven
sources: [laptop-to-money v2 session 2026-11-11]
blender: "5.2"
---
# Camera stations framed on what is in the frame (hero-driven keys)

**Principle:** The camera angle changes with the hero. Each state of the subject gets its own framed "station": the subject sits in the middle of the frame, with space above it when it grows upward (a laptop lid opening). Between stations the camera moves with the mountain speed graph, and the move that crosses a cut puts its speed peak exactly on the cut.

**Steps (as approved by the user):**
1. List the hero states: e.g. laptop closed → laptop open → money on the table.
2. The user frames each state by hand in camera view (move the camera, not the rig). **Read the live transform before changing frame** — unkeyed edits are lost on frame change. If the camera object itself is not animated, its edits persist across frames: check its location against the earlier value to find what the user changed.
3. Key that pose at the state's frame:
   - closed state → shot start (frame where the lid starts opening),
   - open state → a few frames after the lid is fully open (lid done 146 → station 153),
   - final hero → after the cut.
4. Key BOTH the rig (orbit tilt) and the camera's local position, so per-state height differences are kept.
5. Mountain graph on every key: Bezier, FREE flat handles = 0.75 × the neighbouring segment.
6. The move that crosses the cut must be **symmetric around the cut** (station before = cut − N, station after = cut + N). With symmetric mountain handles the speed peak lands on the cut. Check: sample the camera world position per frame; the max step must sit at cut − 0.5.
7. After the last station the camera holds; motion continues in the subject (turntable drift).

**Check:** project the hero's bounding box with `world_to_camera_view`; centre y ≈ 0.50 for closed/open, ≈ 0.55 for a pile on a table (the table fills the lower part).

**Use when:** turntable / product reveals where the hero changes size or shape (lid opens, object swaps at a match cut).
**Avoid when:** a single locked framing is wanted for the whole shot.

**Failure signs:** hero drifts off-centre as it changes; camera still moving long after the cut (move not symmetric → peak late); a stop-go bump at a middle station.
**Log:** 2026-11-11 — laptop-to-money: stations 100 / 153 / 247, cut 200, measured camera speed peak 199.5.
