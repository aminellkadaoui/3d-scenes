# Photorealism — what makes CG read as real vs fake (synthesis)

Status: **Extracted**. This file is the index of realism cues; details live in the linked pillar files.
Definition: photorealism = the viewer doesn't question whether it's a photo/video [J_mweAPcO4M@00:45]. It's an *illusion built from many small cues*; one strong fake cue breaks it, and no single "magic setting" creates it.

Core principles
1. **Reference over imagination.** Collect general mood → individual assets → lighting refs; match scale, imperfections, light [J_mweAPcO4M@01:00–02:00]. The eye knows reality; your memory doesn't.
2. **Controlled chaos.** The real world is random; CG defaults are perfect [R4sOG6OPioc@00:15]. Add chaos in proportion and with physical/story logic.
3. **Believability > beauty.** "Life can be ugly… the boring the lighting, the better the illusion" [J_mweAPcO4M@08:00–08:15]. Over-designed light/colour is a CG tell. (For VSL: stylised "cinematic" is fine — but every stylisation must sit on a physically plausible base.)
4. **Consistency.** Every element at the same level of realism, same scale logic, same light. One weak element breaks the frame.
5. **Subtlety.** Most realism cues are just above perception threshold. If you *notice* the effect (grunge, bloom, CA, vignette, DoF), it's probably too strong.

---

## The realism cue list
For each cue: what the eye checks → fake symptom → where to fix.

### A. Geometry & assets — `assets-modeling.md`
| Cue | Fake symptom | Fix |
|---|---|---|
| Bevelled edges catching light | razor-sharp edges, no rim highlight | Bevel modifier / Bevel node [SaZOuHQROIg@01:00; J_mweAPcO4M@03:30] |
| Believable scale | toy/miniature/giant | real dimensions, human reference, applied scale [J_mweAPcO4M@03:45] |
| Silhouette richness | primitives with a material | secondary forms, thickness, segments |
| Imperfect geometry | perfectly flat walls, straight lines | sculpt Grab waviness [R4sOG6OPioc@01:15] |
| Non-grid placement | aligned, evenly spaced objects | Randomize Transform 1–5° [R4sOG6OPioc@01:30], rigid body drops [J_mweAPcO4M@06:45] |
| Clutter & storytelling | empty, sterile spaces | story props at edges [R4sOG6OPioc@03:00] |
| Asset quality parity | one low-quality model among scans | replace or push to background |

### B. Materials — `materials-pbr.md`
| Cue | Fake symptom | Fix |
|---|---|---|
| Roughness variation | uniform highlights, plastic look | roughness maps + imperfections [SaZOuHQROIg@01:30; RfPro3hlOMg@06:00] |
| Physical albedo | pure black/white, saturated colours | albedo 0.02–0.9, desaturate |
| Correct metallic | grey-plastic metal | Metallic 0/1, bright F0 |
| Wear/dirt where physics says | clean or uniformly dirty | geometry masks × grunge [RfPro3hlOMg@09:30–13:30] |
| No visible tiling | grid of stains | macro variation, bombing [8HfKtaDx6tM@08:30; aUnpMrAYzGs@08:15] |
| Texture scale | wrong grain size = wrong object size | real-world texture size [LPCdpTcNXyM@04:45] |
| Relief at grazing angles | flat silhouettes on rough stone | displacement (adaptive) [aUnpMrAYzGs@04:30] |
| Real-photo chaos | sterile seamless textures | photo textures/overlays [R4sOG6OPioc@01:45–02:45] |

### C. Light & shadow — `lighting.md`
| Cue | Fake symptom | Fix |
|---|---|---|
| Contact shadows / occlusion | floating objects, no darkening where things touch | objects actually touching; Cycles/EEVEE raytracing/AO; check contact at 200% |
| Global illumination / bounce | black shadows, no colour bleed | Cycles path tracing or EEVEE raytracing; enough bounces |
| Soft, size-appropriate shadows | razor shadows from "point" lights | light size matching the real source (window, softbox, sun angle ~0.5°) |
| Real light colours | default pure white everything | colour temperature (warm practicals ~2700–3500 K, daylight 5500–6500 K, overcast/shade bluer) [SaZOuHQROIg@03:15; J_mweAPcO4M@08:15] |
| Motivated light | lights from nowhere, rim on everything | every light has a source in the world (window, lamp, screen); HDRI for environment [SaZOuHQROIg@00:15] |
| Interesting but natural shadows | flat even lighting | occluders / gobos [R4sOG6OPioc@03:30; J_mweAPcO4M@08:30] |
| Light-in-reflections hygiene | visible area-light rectangles in reflections | disable area light visibility for glossy/transmission where unmotivated [J_mweAPcO4M@08:45]; HDRI only for camera + transmission rays (window backdrop) via Light Path in World, lighting from the window area light [J_mweAPcO4M@08:05] |
| Atmosphere (subtle) | perfectly clear air in large spaces | light haze/volumetric only if motivated (`environment-atmosphere.md`) |

### D. Camera & lens — `camera-lenses.md`
| Cue | Fake symptom | Fix |
|---|---|---|
| Human camera position | god's-eye / arbitrary height | eye height ~1.5–1.7 m standing, ~1.1–1.2 m seated; or a motivated device (drone, CCTV, phone) [J_mweAPcO4M@02:15] |
| Real focal lengths | extreme wide or tele without reason | 24–50 mm for "someone filmed this", 85–135 mm product/portrait |
| Depth of field from physics | everything sharp, or fake tilt-shift | real f-stop at real scale; focus on subject (`techniques/camera-dof-physical-scale.md`) |
| Lens imperfections | perfect pinhole image | very subtle distortion, CA/dispersion, vignette, bloom/glare on highlights [J_mweAPcO4M@11:30; LPCdpTcNXyM@04:30] (`compositing.md`) |
| Handheld / operator motion | robotic, perfectly smooth or linear moves | noise on rotation, eased moves (`techniques/camera-handheld-noise-modifier.md`, `animation.md`) |
| Motion blur | strobe-sharp moving objects | motion blur on (shutter ~180°: 0.5 frame) (`rendering.md`) |
| Focus behaviour | instant perfect focus | slight focus pulls/breathing on moves |

### E. Rendering, colour & finishing — `rendering.md`, `color-management.md`, `compositing.md`
| Cue | Fake symptom | Fix |
|---|---|---|
| Highlight roll-off | clipped hard whites, neon saturation | AgX (or ACES) view transform, not Standard; Filmic Log only as grade base [SaZOuHQROIg@02:15] |
| Photographic exposure | dark, contrasty "CG" look | expose like a camera; for daytime snapshot looks, slight overexposure/washed look [J_mweAPcO4M@11:00] |
| Clean but not sterile noise | denoiser smudge / waxy surfaces / fireflies | enough samples; denoise with albedo/normal passes; add fine grain in post |
| Grain & sharpening | plastic-smooth image | subtle film grain, light sharpen ~0.3 [J_mweAPcO4M@11:30] |
| Black/white levels | crushed pure black or pure white | grade with headroom; no 0/1 except speculars |
| Delivery resolution awareness | detail invisible or aliasing at 480–1080p | check at final size; avoid moiré on UI screens |

---

## The fast diagnostic (apply to any frame)
1. **Clay test**: override all materials to grey (~0.18–0.5 albedo, rough 0.5). Does it still look like a real space/object (forms, bevels, scale, light, contact)? If not, fix A/C/D before materials.
2. **Squint test** (blur/downscale): readable value structure? visible tiling grid? focal point clear?
3. **Edge/highlight test** at 200%: rim highlights on edges, roughness breakup in reflections.
4. **Contact test**: every object touching the ground/support has contact occlusion.
5. **Reference A/B**: put a real photo of the same subject next to the frame; list the 3 biggest differences; fix the biggest one only, re-render, compare.
6. **Motion test** (for video): camera motion feels operated, motion blur present, no flicker/boiling noise.
Log problems with `templates/qa-issue.yaml`; rubric in `ai-slop-diagnosis.md`.

## Things that are NOT photorealism (common slop)
- Heavy fog + bloom + teal/orange + extreme shallow DoF stacked by default (see CLAUDE.md).
- Over-dirty "grunge filter" on everything — imperfection must have a cause.
- Perfect symmetry, centered everything, pure white seamless background with no contact shadow (unless it's an intentional studio packshot with a proper cyclorama and soft light).
- HDRI backgrounds at low resolution visible behind sharp foreground [J_mweAPcO4M@09:00].
- Saturated, glowing emission everywhere.

## Cross-references
`assets-modeling.md` · `materials-pbr.md` · `lighting.md` · `camera-lenses.md` · `environment-atmosphere.md` · `rendering.md` · `color-management.md` · `compositing.md` · `ai-slop-diagnosis.md` · `composition.md` · `art-direction.md`.

## Sources
J_mweAPcO4M, R4sOG6OPioc, SaZOuHQROIg, 8HfKtaDx6tM, aUnpMrAYzGs, RfPro3hlOMg, LPCdpTcNXyM (`sources/<id>.md`); expert synthesis; numbers are starting points (metres, Blender 5.2, AgX).
