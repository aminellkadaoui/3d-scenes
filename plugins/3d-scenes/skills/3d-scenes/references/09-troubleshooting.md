# 09 — Troubleshooting: symptom → cause → fix

Every row happened in a real session. Check the cause before applying the fix.

| Symptom (user words) | Cause found | Fix | See |
|---|---|---|---|
| "The light doesn't affect it" after the user raised it a lot | Light aimed 55° away after the user moved it; extreme power also washes to white under AgX | Re-aim, solo-test, then *lower* power | 05 |
| "I lowered the exposure and it still affects" | UI edit applied only to the **active** light; the duplicate stayed at full power | Set both (Alt-edit or code) | 05 |
| Money/paper looks like white soap bars | White albedo + scene lights + rims; no paper detail | Exclude hero from scene lights; weak fill + edge lights; warm green-grey multiply; sheet lines | 04, 05 |
| Coloured rim shows on the metal stand as a noisy disc | Stand in the rim's receivers | Remove the stand from that collection | 05 |
| Floor doesn't reflect in `look` captures | Screen-space reflections not captured by the tool | Check the user's real viewport or a rendered frame | 07 |
| Softbox rectangles in background/floor after removing walls | HDRI visible to camera and glossy rays | World Light Path mix: camera/glossy rays see a dark colour | 05 |
| "Lots of noise", "quality is weak" | Fast GI defaults, 128 samples, DOF, normal-map sparkle | Final EEVEE profile + OIDN; normal 0.15–0.5 | 07 |
| "Resolution feels low" at 1080p | Small dark subject, only soft lights, temporal denoise | Temporal off, hard raking light, DOF off | 07 |
| Legs vanish into the black background | No separation light | Table-only rim behind (≈40 W) | 05 |
| Object sits inside the table | bbox was fine but vertices were 7.7 mm below | Snap by vertex min-Z | 03 |
| Keyed values turned 0 after editing keyframes | Edited `k.co[1]` on an existing curve badly | Clear the datablock's animation and re-key cleanly | 10 |
| An object you created disappeared | User pressed Ctrl+Z | Re-check `bpy.data.objects.get(name)`; recreate | 11 |
| Render log says samples=128 | Log prints Cycles samples | Check `scene.eevee.taa_render_samples` | 08 |
| Time estimate wildly low | Table-based estimate | Measure one frame | 08 |
| `look` rendered fails | Tool only captures EEVEE/Workbench rendered mode | Use EEVEE or render a frame | 10 |
| Design board shows empty image frames | WebP not displayed | Upload JPG/PNG | 02 |
| Can't download reels | Private/age-gated account | Ask the user to send the files | 02 |
