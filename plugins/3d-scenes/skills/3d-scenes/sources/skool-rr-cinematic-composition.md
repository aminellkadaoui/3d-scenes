# Cinematic Composition (Render Room — 3D Documentary-Style Mastery › Scene Polish)
- url: https://www.skool.com/render-room-7187/classroom/a39a68c5?md=bf7a4ea2c28b46ea9238b06d9e192f74 (private Skool course, login needed)
- channel / duration / Blender version shown: Lucas Carrazana (Render Room) / 12:56 / no Blender UI shown — talking head + reference frames from film and 3D YouTube documentaries (Fern, Cipher, Thinker)
- domain(s): composition (primary), camera (angles, shot sizes), lighting (focus by light, key/fill/rim, angled practicals), art-direction (storytelling)
- evidence used: transcript (Skool English CC track, read in full) + one browser contact sheet of 23 frames (seen, not saved to disk; video download blocked by CDN). Frames seen: center+color example (Trump desk, 3:45), lighting-focus example (dark room, hackers lit, ~4:35), DoF phone example (~5:15), airport wide (~7:30), low-angle authority (~9:05), face portrait key light (~11:00), warm corner lamp room (~12:30). Rule-of-thirds and ATM/wealth examples were not captured.
- trust: medium. Clear, practical, beginner-level; every point backed by a real frame from a successful channel; no before/after inside Blender, no settings. Sells nothing except his own course. Speaker admits he skips depth ("won't bore you").

## 1. Problem it solves
Scenes that "look off" and boring although a lot of work went in — because composition was not planned and design principles were ignored [00:00–00:23]. Viewers who don't know where to look leave (retention/reach) [00:23–00:44].

## 2. Techniques

### T1 — Rule of thirds or center framing, chosen per shot `[00:44–02:08]`
- What: put the most important element on a thirds intersection [00:44]; or center it, but then remove distractions outside the center and aim for near-perfect symmetry [01:48] — blur the background or surround the subject with a plain mass (large body of water around a submarine) [01:48–02:08].
- Why: a known placement makes the frame instantly readable; center only works if nothing competes.
- Use when: thirds for character-in-environment; center for formal/authority/product/"one thing" shots.
- Avoid when: centering a subject in a busy frame.
- Blender 5.2: Camera ▸ Viewport Display ▸ Composition Guides (Thirds / Center). Already in `knowledge/composition.md §3`.
- Status: Extracted (confirms existing knowledge).

### T2 — Focus points: few elements (1–3) `[02:20–03:13]`
- What: compositions are like thumbnails; 1–3 elements on screen at a time [02:53].
- Why: cognitive load — if understanding costs effort, viewers leave [02:29].
- Status: Extracted (adds a number to `composition.md §2`).

### T3 — Focus by color: desaturate everything except the subject `[03:13–04:18]`
- What: emphasize the main point with a different or highly saturated color; documentary examples render the world black & white / grey and keep only the subject (and maybe 1–2 related props) in color — red man, red house, Trump + desk + flags [03:37–04:18]. Seen frame @3:45: center framing + desaturated surroundings.
- Why: pop of color on a neutral field is the strongest attention pull after value contrast.
- Blender 5.2 how (my translation, not shown): Cycles/EEVEE View Layer ▸ Cryptomatte (Object) → Compositor: Hue/Saturation/Value (Saturation 0–0.2) mixed by inverted Cryptomatte matte; or simply desaturate the non-hero materials. → card `composition-selective-color-isolation`.
- Avoid when: realism is the goal (this is a stylised documentary look), or when colors carry meaning elsewhere in the sequence.
- Status: Extracted.

### T4 — Focus by light: light the subject, keep the rest dark `[04:18–04:50]`
- Seen frame @~4:35: almost black room, only the central figures exposed. Already in `composition-focal-point-value-contrast` + `lighting.md`. Status: Extracted (confirmation).

### T5 — Focus by depth of field `[04:50–05:23]`
- Everything blurred except the main element (seen @~5:15: phone sharp, room soft). Already in `camera-dof-physical-scale`. Status: Extracted (confirmation).

### T6 — Wide shot to establish, then close-up to reveal `[05:23–08:20]`
- What: wide shot = context, "where the story takes place" (first shot of a video: house in the morning; airport interior) [05:46–06:30]. Close-up = emotion, reaction or the important detail [06:30]. Alternate: wide first, then close [07:14]. Example sequences: ATM wide → close reveals he is stealing; building exterior wide (wealthy) → close on gold + drugs (wealthy illegally) [07:34–08:20].
- Why: a close-up without the wide is unreadable [06:08–06:53]; the close adds the information that changes the meaning.
- → card `camera-wide-establish-then-close-reveal`.
- Status: Extracted.

### T7 — Camera angle by purpose `[08:24–09:14]`
- Most wides are high angle; most close-ups are straight-on (eye level); authority figure from a low angle (police from below = in control) [08:42–09:02]. Speaker: angles "not a huge deal", vary them when it makes sense [08:24].
- Already in `camera-lenses.md §4`; adds the wide=high / close=straight-on pairing.
- Status: Extracted.

### T8 — Figure–ground contrast (luminance or hue) `[09:14–10:09]`
- Luminance contrast (white dot on black) or hue contrast (opposites on the wheel). Main object must not blend with the background: dark clothes → light wall; dark background → lighter subject (white, red) [09:44–10:09].
- Added to `composition-focal-point-value-contrast`.
- Status: Extracted.

### T9 — Key/fill/rim, and the "cheat code": angled motivated light instead of flat overhead `[10:10–12:56]`
- Key at an angle, not straight above/below [10:53]; fill = weaker, lifts darks [11:13]; rim behind for separation [11:13–11:33]. Real documentaries rarely have a clean 3-point setup [11:33]. Cheat code: replace the big white top light of realistic rooms (flat, boring) with light at an angle — warm lamp in the corner, a sunset through the window, dramatic window light instead of office ceiling lights [11:56–12:56]. Seen @~12:30: dark room lit by one warm lamp pool in the corner.
- Already in `lighting-key-off-axis-rembrandt` and `lighting-night-warm-practicals-cool-ambient`; this adds a documentary-3D source.
- Status: Extracted.

## 3. Claims I doubt or must test
- "1–3 elements" is a heuristic; a wide establishing shot can contain many objects as long as one dominates in value.
- "Most wide shots are high angle" — common, not a rule; eye-level wides are just as usual in film.
- Selective color is a stylistic choice of Fern-type documentaries; in our VSL (realistic room) it would read as an effect — use only as a deliberate moment.
- Rim "creates separation" — in our dark-wall scene (ebony walls, dark clothes) it may be required rather than optional; test.

## 4. Anti-AI-slop lessons
- Plan composition at storyboard time, not after rendering [00:00–00:23].
- Flat overhead "realistic" room light = boring; one angled, motivated source makes the shot [11:56].
- Never open a sequence on a close-up with no context; never show a wide with no close that pays it off.
- If the subject's value/hue equals the background, nothing else will save the frame.

## 5. Candidate isolated test
(a) baseline current light vs (b) + subtle rim/back light (or lighter wall strip behind the head) — measure figure–ground separation on a grayscale thumbnail (luminance difference head/shoulder edge vs wall).
Second test: same frame with selective color (Cryptomatte desaturation of everything except monitor + character) for the "$50 notification" moment — judge if it reads as intent or as an effect.
