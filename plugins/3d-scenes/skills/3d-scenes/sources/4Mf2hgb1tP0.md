# Smooth animations in Blender: easing & the Graph Editor (Blender Essentials)
- url: https://youtu.be/4Mf2hgb1tP0
- channel / duration / Blender version shown: ArtSyndrom3 / ~3:45 (transcript ends [03:30]) / **Blender 5.1.0** (title bar, corrected from frames); 30 fps, frames 1–84, vertical 9:16 render
- domain(s): animation, camera (camera-to-camera transition)
- evidence used: transcript (en-orig auto captions fetched by this agent with yt-dlp on 2026-11-05 and converted to 15 s buckets; the `en` track hit HTTP 429). Plus contact sheet + 6 extracted frames (see §6): curve shapes now seen.
- trust: medium-low. Very short beginner video; terminology is loose (calls the start key "in" and end key "out" [00:30], and the labels for ease in / ease out / in-out are described inconsistently [00:45]–[01:15]). Promotes a free add-on (Easer) [02:45]. Core idea (handle length = ease strength; duration × ease = feel; matched ease across a camera cut) is correct and useful.

## 1. Problem it solves
A two-key animation with default or linear interpolation "looks like trash" [00:00]. The video shows that the feel of a move comes from the shape of the speed curve (handle length), not from adding more keys.

## 2. Techniques

### T1 — Scale Bezier handles to control ease strength `[00:30]–[01:15]`
- What: Graph Editor (`Ctrl+Tab` from Dope Sheet toggles to Graph Editor [00:15]). Select a key (or its handles) and `S` `X` to lengthen the handles horizontally: longer handle = longer, gentler acceleration/deceleration near that key. Lengthening the end key's handles = soft landing; lengthening the start key's handles = slow start, fast end.
- Why: the handle defines how long the curve stays near-flat (near-zero velocity) around the key. Long handle at the end = most of the travel happens early, then a long settle — reads as "premium/expensive" product motion.
- Use when: any hero move, camera push-ins, logo/product settles.
- Don't use when: impacts and ballistic flight (use Vector, see JQT9sT1YuAI@16:00).
- Blender 5.2 notes: same hotkeys. Note Auto/Auto-Clamped handles convert to Aligned once you scale them.
- Status: Extracted

### T2 — Duration and ease interact `[01:30]–[01:45]`
- What: Same handle shape over more frames = smooth and slow; same shape over few frames = still smooth but quick. Retime with `G` on the key, then re-tune handles.
- Why: perceived smoothness depends on peak velocity, not just curve shape.
- Status: Extracted

### T3 — Asymmetric ease: near-full on one end, near-zero on the other `[01:45]–[02:00]`
- What: Start key handle very long, end key handle almost zero → slow build then sudden arrival (or the reverse). This is the building block for whip transitions.
- Status: Extracted

### T4 — Camera-to-camera whip transition with mirrored easing `[02:00]–[02:45]`
- What: Camera A: start slow (long handle), end at full speed (≈zero handle). Camera B: start at full speed (≈zero handle), end slow (long handle). Cut between them at the point of max speed (see dFK3C83k4Wo@04:45 for cut placement with Bind Camera to Markers).
- Why: Motion blur and speed at the cut hide the edit; the eye reads one continuous accelerating-decelerating gesture across two cameras. Velocity must match at the cut, otherwise the cut "bumps".
- Use when: energetic VSL section changes, product feature-to-feature transitions.
- Don't use when: calm/trust-building sections — use a straight cut or a slow dissolve instead.
- Status: Extracted

### T5 — Easing preset add-ons (Easer) `[02:45]–[03:30]`
- Presets "super smooth", "overshoot", "spring". Optional. Overshoot/spring presets on a camera usually look gimmicky; keep for UI/graphic elements.
- Status: Extracted (add-on not evaluated)

## 3. Claims I doubt or must test
- The in/out naming: in standard motion vocabulary "ease in" = slow start (accelerating), "ease out" = slow end. The video's description at [00:45]–[01:15] is ambiguous. Blender's own `T` ▸ Easing labels (for Sine/Quad/... interpolation) follow the Robert Penner convention: Ease In = slow start, Ease Out = slow end.
- "creates a quick whip-like animation" for ease in-out [01:00] — depends on duration, not the curve type alone.

## 4. Anti-AI-slop lessons
- Default symmetric ease on two keys = generic. Choose asymmetric eases with intent (fast start + long settle is the classic "premium" product move).
- Match speeds across cuts; don't cut between two cameras that are both at rest unless it's a deliberate hard cut.

## 5. Candidate isolated test
Two cameras on a product, 48-frame move each, cut at frame 48. A: default ease both. B: A fast-out (handle≈0 at end), B fast-in (handle≈0 at start), long settle, motion blur shutter 0.5. Viewport-render both; check for visible "bump" at cut (velocity plot of camera location per frame) and blind preference.

## 6. Visual verification (frames viewed)
- [00:32] Graph Editor, one Z-location channel 240→415 over ~20 frames with default Auto Clamped handles; on-screen labels "IN" at the first key and "OUT" at the last — confirms his (non-standard) naming: "in" = start key, "out" = end key. Scene: 30 fps, frames 1–84, output MPEG-4/H.264.
- [00:50] Title bar **Blender 5.1.0**; overlay "S + X = scale on" while lengthening the end-key handle — confirms T1 (`S` `X`).
- [01:05] Dope Sheet with two keys (0, 48); "Ctrl+Tab" overlay toggles to the Graph Editor — confirms T1 hotkey.
- [01:50] Normalize on: curve rises steeply from the start and lands with a long flat ease into the end key (~frame 38) — the asymmetric "fast start, long settle" of T3, seen.
- [02:20] Transition: Camera.001 / Camera.002 in the Dope Sheet with camera markers bound in the timeline (switch at ~frame 15); the frame shows the motion-blurred hand-off. Confirms T4 + Bind Camera to Markers.
- [03:10] Easer add-on panel (Symmetric / Asymmetric / One-sided / Advanced presets: Overshoot, Anticipation, Spring Back, Bouncy...). Promo only; not evaluated.
- Quality judgement: **clean but simple** — a single pocket-watch on a blue gradient; motion is smooth and intentional, no slop, but it's a teaching scene, not a portfolio shot. Trust stays medium for terminology, medium-high for the handle-scaling technique (now seen).
