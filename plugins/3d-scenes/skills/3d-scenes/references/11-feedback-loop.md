# 11 — The feedback-loop protocol (why the project was fast)

The shot went from idea to a delivered full-quality render in one working session. The speed came from the loop below, more than from any setting.

## The loop
1. **User shows** (screenshot of the viewport, a cropped render, one sentence).
2. **You re-read the scene** — values may have changed in the UI (user tweaks, Ctrl+Z). Never assume the state from your last message.
3. **Diagnose in one tool call when possible**: solo a light, print aim error, print receiver collections, crop the render at 100%, sample a speed curve.
4. **One focused change** (or a tight bundle the user asked for). Small steps for "more/less" (20–30%).
5. **Look** through the camera in Rendered (EEVEE) at the frames that matter (before cut, after cut, end).
6. **Report**: table of before → after, which recipe it came from, what you could not verify. Keep it short.
7. User reacts → back to 1.

## What made rounds short
- Working **inside the user's open Blender** via MCP: the user sees changes live and can grab the result (select the light for them, tell them which field to drag).
- Giving the user **control handles** instead of asking them to describe values: "this light is selected; Power is the field; Alt-edit changes both".
- Translating editor language (`00-vocabulary.md`) instead of asking for Blender terms.
- Stating the cause in one line when something "doesn't work" — the user learns and the next request is precise.

## What slowed us (avoid)
- Lighting the whole scene globally and then trying to compensate per object with keyframed power drops → several rounds. Go straight to per-group light linking.
- Trusting viewport captures for noise/reflections → judge on a rendered frame.
- Estimating render time from tables → measure one frame.
- Acting on a garbled/ambiguous message (keyboard-layout typos such as "ogw hogw") → ask, or wait. The user stopped the action.
- Changing more than asked (e.g. reframing the camera) → offer it instead.

## Response format that worked
- Arabic (Gulf) for users who write Arabic; tool, node and file names in English.
- Start with the result, then a compact table, then one line of "not verified / next decision".
- One question at most, as a choice.
