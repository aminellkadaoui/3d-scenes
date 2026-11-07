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
| Screen animation looks very dark on the monitor | Plain video sent through a chain built for a LUT-compensated video | Separate path: Sat 1.15 → AgX curve → Emission, switched at the cut | 07 |
| Camera "X-rays" through a lamp/character near the monitor | clip_start driver cuts objects between camera and screen | Move the prop out of frame / lower clip_start | 06 |
| User's hand framing lost | Unkeyed camera snapped back on refresh | Read transform immediately, or key it (I) | 06 |
| Tracking stops mid-shot | Frame clamp on an axis the cursor keeps moving along | Clamp per axis; remove the clamp for that shot | 06 |
| New scene copy shows an empty viewport | `scene.copy()` result not displayed | Use Scene ▸ New ▸ Linked Copy (`bpy.ops.scene.new(type='LINK_COPY')`) | 10 |
| EEVEE fill light gives no light at all | Area light centre inside an occluder | Shadow Jitter on | 07 |
| Quality "looks bad" in a delivered clip | Compressed MP4 preview | Deliver ProRes 4444 XQ / PNG | 08 |

