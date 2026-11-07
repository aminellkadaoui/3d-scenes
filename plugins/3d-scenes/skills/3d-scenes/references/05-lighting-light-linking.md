# 05 — Lighting & light linking (Proven)

## The core lesson
One global lighting setup cannot serve a dark glossy set **and** a white paper hero. What finally worked: **light every group separately with light linking** ("track matte" lighting). Each light has one job and an explicit list of what it touches.

## Light linking — how it works (Blender 5.x, EEVEE & Cycles)
- Object ▸ Shading ▸ Light Linking ▸ **Receiver Collection**. Objects in that collection with state **Include** are the only ones lit — if at least one Include exists.
- **Exclude** a hero from a light: add it to the light's receiver collection and set its state to EXCLUDE. Python: `coll.collection_objects` does **not** support name lookup; iterate `zip(coll.objects, coll.collection_objects)` and set `item.light_linking.link_state = 'EXCLUDE'`.
- A light may already have a receiver collection (e.g. an old `Haze Exclude`). Don't replace it — add the hero to that collection as EXCLUDE.
- Several lights can share a collection. **Don't share a collection between lights with different jobs**: adding the money to a "hero" collection also brought back the hard side light on it. One collection per job: `LL_Laptop`, `LL_Money_Only`, `LL_Blue_Rim` (laptop+money), `LL_Table`, `LL_Exclude_Money`.
- Changing light settings in the UI edits **only the active light**. Two selected lights + a field change = one changed. Use Alt+Enter / Alt-drag, or set both in code. This caused "I lowered it and it still affects".

## Final light structure that worked (dark set, spinning hero)
| Light | Type / size | Power | Where | Receivers | Job |
|---|---|---|---|---|---|
| Original project lights | as approved | as approved | as approved | all except money | Base mood |
| Key_Hero | Area 0.5×0.35 | 55 W, cool white | 40° off camera, 30° up | all except money | Shape |
| Hard_Side | Area 0.3 square | 50 W | 75° from camera, low (≈9° up), opposite the key | laptop only | Raking light → keys/edges detail |
| Rim_Blue ×2 | Area 1.0×0.58 | 600 W (user tuned exposure) | ±145° from camera, z 1.3 m | laptop + money | Blue edge, light sweep while spinning |
| Rim_Table | Area 0.25×1.0 | 40 W cool | behind table, 150°, z 0.55 | table only | Separate dark legs from black background |
| Money_Fill | Area 0.6 | **4 W** white | front-top | money only | Read the print without clipping |
| Money_Sweep L/R | Area 0.15×0.8 | 65–90 W white | ±115°, at hero height | money only | White light sweep on bundle edges |

## Hero with white surfaces (paper, white plastic)
- White albedo + strong scene lights = clipped soap bars. Lowering the scene lights in steps (−30%, −25%, keyed at the cut) was **not enough**.
- Fix: exclude the hero from every scene light, give it a **very weak** fill (≈4 W at 0.9 m) + narrow edge lights. Print and paper layers appeared immediately.
- **Coloured light on a white object under AgX**: raising the blue light (1038 W, +2.8 EV) made the money *whiter*, not bluer — AgX desaturates very bright saturated light toward white. To get colour: lower the white lights, keep the coloured light moderate.

## Rim lights must be visible from the camera
Rims at hero height behind the object lit back faces a high camera never sees. Raising them to ≈1.3 m (above the hero) at ±145° put the blue on top edges. Always aim lights at the hero (`to_track_quat('-Z','Y')`) and **re-check aim** after the user moves them: a 55° aim error made a 1000 W light "do nothing". A Track-To constraint to an empty prevents this.

## Spill control
- Coloured light hitting a glossy metal top → noisy coloured disc. Remove the top from that light's receivers.
- Rim on table legs only (`LL_Table`), so the floor doesn't glow.

## World / backdrop
Removing walls exposed the HDRI's softboxes in camera and in floor reflections. Keep HDRI lighting but hide it from camera and glossy rays: World ▸ Mix Shader, Fac = max(Is Camera Ray, Is Glossy Ray), shader 2 = Background dark blue-black (0.006, 0.007, 0.010). Code: `scripts/world_backdrop.py`.

## Practical checks
- Solo a light (hide others in viewport) to see exactly what it does.
- `light.data.spread` is ignored by EEVEE for area lights — use size/aim.
- Effective power = Power × 2^Exposure.
