# Vocabulary — what the user says vs what to do in Blender

Users often come from video editing (Premiere / After Effects) and describe 3D ideas with editor words or Gulf Arabic. Translate, don't ask them to learn Blender terms.

| User says | Means | Blender action |
|---|---|---|
| «مات» / «تراك مات» / track matte for a light | A light that affects only some objects | **Light Linking** → Object ▸ Shading ▸ Light Linking ▸ Receiver collection (Include). "Exclude from everything else" = add the object to each light's receiver collection with link state `EXCLUDE` |
| «light sweep» / «لايت سويب» / «تلسع الجوانب» | A highlight that travels across edges | Rim/edge lights behind-side (±115–145° from camera) + the object rotating (turntable). The light stays still; rotation makes the sweep |
| «جراف الجبل» / «جراف حاد» / speed graph In/Out 75% | Ease-in → peak → ease-out speed curve | 2 Bezier keys, FREE handles, length = 75% of the segment on both keys (`scripts/turntable_rig.py`). Peak speed is in the middle |
| «متش كت» / match cut | Swap object A → B inside motion | Hide A / show B on the **peak-speed frame**, CONSTANT keys on `hide_render` + `hide_viewport` (`scripts/match_cut.py`) |
| «يدور بطء طول الوقت» | Never stop spinning | Parent "drift" empty with LINEAR keys + Linear extrapolation under the main animation |
| «برونت ع الاوبجكت وترتفع» | Start low in front, crane up | Camera rig: empty at subject, camera child at fixed distance, animate rig X rotation (elevation) |
| «الريزوليوشن نازل» / «التفاصيل ضعيفة» | Lack of sharpness/micro-detail, not pixel count | See `07-eevee-quality-noise.md` §Sharpness |
| «نويز» | Grain | `07-eevee-quality-noise.md` §Noise — find *which* surface first |
| «محروقة» / «أبيض زيادة» | Clipped highlights / washed out | Lower the light first. Saturated light on white paper turns white under AgX |
| «زيد» / «نقّص» | Small step | 20–30% change, report before → after |
| «فوكس» | Depth of field | Camera ▸ Depth of Field on/off |
| «اكسبوجر» | Light Exposure field (stops) | Effective power = Power × 2^Exposure; −10 ≈ off |
| «كنترول زد» | Undo | Objects you created may be gone — re-check existence |
| «حددها لي» | Select it so I can tweak | Select + make active, Properties ▸ Data tab, reveal in Outliner; remind about Alt-edit for multi-selection |
