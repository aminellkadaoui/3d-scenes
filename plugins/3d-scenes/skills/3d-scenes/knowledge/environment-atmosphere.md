# Environment & Atmosphere — sets, scale, ground contact, air

> Status: Knowledge (research + expert synthesis). Blender 5.x (target 5.2). Setting names verified against the Blender 5.2 manual sources and the 5.0 Cycles release notes where cited; always re-read API identifiers at runtime (see §9).
> Related: `ai-slop-diagnosis.md` (E1–E4), `lighting.md`, `composition.md`, `photorealism.md`, `rendering.md`, `compositing.md`.

---

## 1. Why environment matters more than the hero

A hero object in a void is the single most recognizable slop pattern. The environment does four jobs the hero cannot do itself:
1. **Context** — where and when are we? (era, price class, climate, time of day)
2. **Scale** — how big is the hero? (known-size objects, texture density, atmosphere, DOF)
3. **Value framing** — a background that is deliberately darker/lighter/less saturated than the hero makes the hero read.
4. **Light** — the environment is a light source (bounce, sky, HDRI, practicals) and a shadow receiver.

Rule: **dress only what the camera sees**, and judge everything through the camera, removing what pulls focus. A few well-chosen props in tight clusters, with some wear and a few things out of line, read as more real than clutter spread evenly (environment-art practice; see sources).

---

## 2. Set dressing & environmental storytelling

**Process (after blockout and camera are locked):**
1. Write the "occupant brief": who uses this space, how long, how careful, how rich? (e.g. "Night-shift trader, 3 years in this flat, tidy desk but overflowing bin".)
2. Big → medium → small: architecture & large furniture → secondary objects (lamps, shelves, devices) → small story props (mug ring, sticky notes, cable, receipt, dust).
3. Cluster props in 2–3 "story islands" near the hero; leave rest areas (negative space).
4. Each prop must answer *why is it here?* and match the spec's era, wear level, palette.
5. Imply time: worn steps, faded paint, overgrowth, rust, a half-drunk coffee. Props are micro-stories that support the larger world.
6. Break the grid: rotate items 2–15°, offset from edges, let one item overlap another.
7. Check the silhouette and value read at thumbnail size; remove props that create tangents or compete with the hero.

**VSL/marketing-specific:** the environment should support the message frame (problem/agitation = cold, cluttered, cramped; solution = clean, open, warm; proof = believable real-world setting). Keep text-safe negative space where the editor will place captions.

**Common critiques:** props plausible but no coherent occupant story; evenly distributed clutter; all props pristine; props at the wrong scale; detail spent where the camera doesn't look.

---

## 3. Scale cues (checklist)

The eye judges scale from:
- **Known objects**: door (2.0–2.1 m), chair seat (0.45 m), desk (0.73–0.76 m), stair riser (0.17–0.19 m), A4 paper, coffee mug (≈ 9.5 cm tall), power socket, hand, car (≈ 1.5 m tall).
- **Texture density**: wood grain, brick (≈ 21.5×6.5 cm UK / 20×6 cm EU), tiles, fabric weave must be at real size — unapplied scale is the classic killer.
- **Depth of field**: shallow DOF on a big scene = miniature (tilt-shift effect). DOF must match real lens + real distance — so scene must be in real metres.
- **Atmosphere**: distant objects get hazier; a 3 m object with heavy haze reads as huge and far; a crisp one reads small and near.
- **Camera height**: human eye height (1.5–1.7 m) reads "human scale"; table-top height reads "product"; low wide reads "monumental".
- **Bevel size & detail density**: tiny bevels and fine detail = large object seen up close; chunky bevels = toy.

Rule: model in metres with `scene.unit_settings.scale_length = 1.0`, apply object scale, keep a hidden 1.8 m human reference.

---

## 4. Avoiding the void — background options

| Option | When | How | Cost |
|---|---|---|---|
| **Studio cyclorama (infinity curve)** | Product, minimalist, motion-graphic 3D | Curved sweep mesh (L-profile with a large-radius fillet), bevel/subdiv; light a gradient on it (brighter behind hero, falling off to edges); slight roughness variation | Very cheap |
| **Designed dark backdrop** | Dark & moody, luxury | Not black: background at 2–8% value with a pool of light or rim gradient; atmosphere to catch light | Cheap |
| **HDRI as backplate** | Exteriors, quick realism, distant BG | Environment Texture in World; match sun; blur/defocus via camera DOF is *not* applied to the world in Cycles — use a geometry backplate or comp blur if needed | Cheap render, limited parallax |
| **HDRI lighting + separate backplate** | Hero needs HDRI light but different visible BG | Light Path → *Is Camera Ray* mixes world for camera vs lighting; or World Ray Visibility → Camera off + backplate geometry | Cheap |
| **Geometry environment** | Camera moves, parallax needed, interiors | Real walls/props; mid-ground geometry; far BG can be cards/HDRI | Moderate–high |
| **Matte-painting card / image plane** | Distant skyline, static or slow camera | Image on plane far away, emission or diffuse + atmosphere in front | Cheap |
| **Mixed (recommended default)** | Most cinematic shots | Geometry for FG/MG (parallax and contact), HDRI/sky or cards for BG, volume/mist to blend the seam | Balanced |

**HDRI backplate pitfalls:** HDRI horizon must match camera height (a ground-level HDRI behind a camera at 10 m looks wrong); HDRI resolution must be high enough for the visible portion (≥ 8K for visible backgrounds at 1080p with normal lenses; 16K for tele); the HDRI's ground does not receive your objects' shadows — add a **shadow catcher** plane (Cycles: Object Properties → Visibility → *Shadow Catcher*, API `obj.is_shadow_catcher`) or real ground geometry that blends into the HDRI.

---

## 5. Ground contact (the most-missed realism cue)

Contact is what tells the brain an object has weight.
- **Geometry**: object bottom exactly on the support (raycast-snap; tolerance ≤ 1 mm at real scale). Soft objects (cushion, bag) should deform slightly.
- **Contact shadow**: a dark, tight occlusion line where object meets ground — even under soft overcast light. Cycles produces it physically. EEVEE (5.x): make sure lights cast shadows, raytracing/screen-space features are enabled, and consider a small contact-darkening (AO node driven) on the ground material. Shadow softness widens with distance from the contact point.
- **Ground response**: dust ring, slight dent in carpet/sand/snow, reflection on glossy floors (with roughness so it isn't a mirror), color bleeding from a saturated object onto the floor (indirect light).
- **Ground material**: never a flat single-color plane. Needs albedo variation, roughness variation, and an edge that is not visible in frame (extend or fade it, or curve it into a cyc).

---

## 6. Atmospheric perspective

Air between camera and subject adds light (in-scattering, toward sky/fog color) and removes light (extinction). Effects with distance: **contrast drops, values move toward the fog color (usually lighter), saturation drops, detail softens**, and hue shifts toward the sky (blue in clear daylight, warm in golden hour, grey in overcast, colored by practicals at night).

Three ways to get it in Blender:
1. **World volume** (physical, interacts with light) — most realistic, most expensive, affects everything incl. light shafts.
2. **Object volume** (a box/domain with Volume Scatter/Principled Volume) — local fog, ground fog layers, god-ray beams; controllable extent.
3. **Mist pass in compositing** (fake, cheap, no light interaction) — perfect for distance haze, depth grading, and fixing an image after render.

### 6.1 World volume vs object volume

| | World volume (World Output → Volume) | Object volume (domain mesh) |
|---|---|---|
| Extent | Infinite; everything incl. distant BG | Only inside the mesh |
| Control | One density everywhere (can't easily layer) | Shape it; gradient density with textures (e.g. height-based via Gradient/Separate XYZ) |
| Light shafts | Yes from any light | Only inside domain |
| Cost | Highest; noise everywhere | Lower; confined |
| Gotchas | Sun/world light gets attenuated over huge distances; HDRI background gets fogged; Cycles world volume darkens the scene if density is high | Camera inside domain vs outside matters; domain edges can show (feather density with a gradient) |
| Best use | Exterior haze, uniform room haze in Cycles | Ground fog, beam-only haze, haze in front of a window, localized smoke |

Practical default: **object volume box enclosing the shot** (not infinite), density shaped to fade at edges, plus mist pass for distant depth grading.

### 6.2 Volume Scatter — settings (Blender 5.2)

Volume Scatter node inputs/properties (manual 5.2): **Color**, **Density**, and per-phase inputs — **Anisotropy** (Henyey-Greenstein, Draine), **IOR** and **Backscatter** (Fournier-Forand), **Alpha** (Draine), **Diameter** in µm (Mie). Property **Phase**: Henyey-Greenstein (all engines), Fournier-Forand, Draine, Rayleigh, Mie (Cycles only). Rayleigh = particles smaller than light wavelength (clear sky blue); Mie = larger particles (clouds, fog). Phase functions can be combined via Mix Shader. Volume output goes into the **Volume** socket of Material Output or World Output. Pair with Volume Absorption for smoke. Principled Volume bundles scatter + absorption + emission + temperature/blackbody.

### 6.3 Why density (and the look of anisotropy) depends on scene scale

Density is an **extinction coefficient per scene unit of distance** (effectively 1/metre if the scene is in metres — the UI shows no unit; Devtalk discussion "Physical units on Volume Scatter and Volume Absorption"). Light through a homogeneous volume follows Beer–Lambert:

```
transmittance T = exp(-density × distance)
mean free path  = 1 / density            (average distance before light scatters)
density needed  = -ln(T_target) / d
```

Consequences:
- **Scaling the whole scene changes the fog.** If the scene was built 10× too big (a 1.8 m human modelled as 18 units), the same density gives 10× more optical depth → the scene becomes 10× foggier. Scaling a *volume object* does **not** change its density per unit; the path through it just gets longer. (Blender Artists users report the same: density is relative to the scene, not the object size.)
- **Density targets by intent** (scene in metres):
  - Half-visibility at 20 m (thick interior haze): `0.693 / 20 ≈ 0.035`
  - Half-visibility at 200 m (outdoor haze): `≈ 0.0035`
  - Half-visibility at 2 km (light aerial perspective): `≈ 0.00035`
  - Product shot "air" in a 3 m studio volume (subtle beam visibility, T ≈ 0.9 across 3 m): `-ln(0.9)/3 ≈ 0.035`
  So a density of 0.1–1.0 — values often typed by default — is fog-bank/smoke territory for a real-scale scene.
- **Very low densities**: users report the field's practical floor around ~0.00002 for multi-km scenes; for very long distances, prefer a Sky texture/HDRI background + a low fog layer, or mist-pass compositing (Blender Artists "Simulating accurate atmosphere over 5–10 km").
- **Anisotropy (g, −1…1) is dimensionless** — it doesn't change with scale by itself. It controls *where* the scattered light goes: g > 0 forward (bright when looking toward the light: halos around sun/lamps, visible beams back-lit), g = 0 isotropic (even glow), g < 0 backward (rare). **But how strong a beam reads depends on optical depth** (density × path length), which is scale-dependent: too thin → beams invisible; too thick → multiple scattering washes out the directionality and everything goes milky. Typical values: haze/fog g ≈ 0.3–0.6; strong god rays with backlight g ≈ 0.6–0.85; smoke g ≈ 0–0.3.
- **Light shafts need contrast**: volume + an occluder (window frame, blinds, foliage, gobo) + a light behind/beside the volume relative to camera. No occluder = uniform glow, not rays.

### 6.4 Engine settings (5.x)

**Cycles (5.0+)**: volume rendering defaults to an **unbiased null-scattering** method that removes the need for step size/max steps tuning and reduces artifacts in overlapping volumes. *Render Properties → Volumes → Biased* re-enables legacy ray marching with **Step Rate Render**, **Viewport** step rate and **Max Steps** (5.0 release notes; manual "Volumes" render settings). Light Paths → **Volume** bounces: 0 = single scattering (faster, darker, more contrasty beams); 1–2 for milky realistic fog. Noise in volumes: increase samples or use denoiser; clamp indirect for fireflies.

**EEVEE (5.x)** Render Properties → Volumes: **Resolution** (tile size — smaller tiles = higher quality, more VRAM), **Steps**, **Distribution** (blend between linear and exponential samples; higher = more samples near camera), **Max Depth** (surface intersection count for accurate volume intersection), **Custom Range → Start/End**. EEVEE volumes are froxel-based: thin features (thin beams) can look blocky — reduce tile size, increase steps, shorten the End distance to concentrate samples. Light → **Volume** factor (`light.volume_factor`) scales a light's contribution to volumes — useful to make a key light create shafts without washing the scene.

**EEVEE room fog box (Extracted, eevee_full_course):** a cube enclosing the room, Surface None, Volume Scatter (Henyey-Greenstein) **Density 0.05, Anisotropy 0** gives near-real-time shafts [eevee_full_course@63:30] (same density as the Cycles source [1MyARLB8KzY@07:00]). Enable Render › Shadows › **Volume Shadows** for shafts. Put the fog box (and fake window glass) in a "hide before baking" collection and hide it while baking the Volume light probe, or the fog gets baked into the irradiance [eevee_full_course@65:20]. Cost ≈ +0.5 s/frame in a furnished room (transcript). Card: `environment-eevee-room-volume-fog`. Volumetrics are where EEVEE is closest to (and much faster than) Cycles; the gap is shaft-edge sharpness (froxel resolution) and flicker in motion.

### 6.5 Mist pass alternative (cheap & controllable)

Enable *View Layer → Passes → Data → **Mist*** (Cycles and EEVEE). Settings appear in *World Properties → **Mist Pass***: **Start** (where mist begins), **Depth** (distance over which it ramps to full), **Falloff** (Quadratic, Linear, Inverse Quadratic). The pass is camera distance mapped 0–1. The manual itself suggests the World Volume slot as the physical alternative.

Comp recipe: Mist → (Map Range/ColorRamp to shape) → Mix (factor) between the render and a fog color (sampled from the sky/BG). Add slight desaturation and blur in far planes. Doesn't create shafts or light interaction; perfect for aerial perspective, layered silhouettes, and fixing depth after render. For transparency/hair, mist is antialiased in Cycles; the Depth (Z) pass isn't — prefer Mist for compositing fog.

**Choosing**: shafts/glow around lights needed → volume. Only distance haze → mist pass (zero render cost). Both → object volume (local) + mist (global).

### 6.6 Cost tradeoffs (rough, Cycles)

| Technique | Relative render cost | Noise risk |
|---|---|---|
| Mist pass comp | ~0% | none |
| Object volume, thin, small domain, 0 volume bounces | +20–60% | low |
| World volume, 1+ bounces | +100–400% | high |
| Heterogeneous (noise-texture density) volume | +50–200% over homogeneous | medium–high |
| VDB smoke/clouds | high, memory | medium |

Always test a volume at 25–50% resolution with low samples before committing (see `production-pipeline.md` render-efficiency rules).

---

## 7. Weather & time of day — recipes

| Look | Sun / sky | Atmosphere | Grade cues |
|---|---|---|---|
| **Clear midday** | Sun high (elev. 50–70°), Sun angle ~0.5°, strong; sky blue | Thin haze, aerial blue in distance | Hard shadows, high contrast, neutral WB — generally least cinematic; use for "honest/documentary" |
| **Golden hour** | Sun elev. 3–10°, warm (≈ 3000–3500 K look), long shadows; sky warm near horizon, cooler above | Light warm haze; backlit forward-scatter g ≈ 0.6 | Warm highlights, cooler shadows (complementary, not teal-orange cliché), rim light on hero |
| **Blue hour** | Sun below horizon; cool sky dome; practicals on | Low, cool haze | Cool ambient with warm practical accents (windows, lamps) |
| **Overcast** | Sun off or angle 10–20°; bright soft sky | Grey-white haze, low contrast | Soft wrap light, rich saturation in mids, great for product truthfulness |
| **Fog/mist morning** | Low sun, diffused | Dense object/world volume near ground (height gradient) | Lifted blacks, low contrast, desaturated distance — conveys cold/quiet |
| **Night urban** | Moon as weak cool key (or none); practicals key | Haze to catch street lights; wet ground for reflections | Deep blacks with controlled accents; avoid neon overload |
| **Rain** | Overcast or night | Haze + particle streaks (motion blur), wet materials (darker albedo, lower roughness, puddle masks) | Reflections are the main cue — wet = darker + glossier |
| **Cold/winter** | Low sun, flat diffuse | Fog, desaturate toward grey | Cooler WB; bare trees, sparse grass (Blender Artists critique) |

Sky: Sky Texture (Nishita/multiple-scattering sky model in recent versions — read the enum at runtime) for physically linked sun+sky; HDRI for real-world complexity. Always match Sun lamp rotation to the HDRI's sun.

---

## 8. Environment checklist (per shot)

- [ ] Occupant/brand brief written; props chosen from it.
- [ ] Background type chosen from §4 table deliberately.
- [ ] Ground contact verified (bbox bottoms, contact shadow visible in render).
- [ ] At least two known-size scale cues in frame (unless minimalist spec).
- [ ] Depth cue present: atmosphere, mist grade, DOF, or value recession.
- [ ] Background value/saturation subordinate to hero.
- [ ] Time of day/weather consistent across sun, sky, practicals, materials (wetness), and grade.
- [ ] Volumes: density computed from intended visibility distance (§6.3), tested at low res.
- [ ] No visible floor edge, HDRI seam, or domain edge.

---

## 9. Runtime API lookups (don't hardcode)

```python
import bpy
sc = bpy.context.scene
# EEVEE volume properties available in this build
print([p.identifier for p in sc.eevee.bl_rna.properties if 'volum' in p.identifier])
# Cycles volume properties
print([p.identifier for p in sc.cycles.bl_rna.properties if 'volume' in p.identifier])
# Mist settings
w = sc.world; print(w.mist_settings.start, w.mist_settings.depth, w.mist_settings.falloff)
print([i.identifier for i in type(w.mist_settings).bl_rna.properties['falloff'].enum_items])
# enable mist pass
bpy.context.view_layer.use_pass_mist = True
# Volume Scatter phase enum identifiers
print([i.identifier for i in bpy.types.ShaderNodeVolumeScatter.bl_rna.properties['phase'].enum_items])
# Sky texture types
print([i.identifier for i in bpy.types.ShaderNodeTexSky.bl_rna.properties['sky_type'].enum_items])
```

---

## 10. Sources consulted

- Blender Manual source — Volume Scatter node (5.2): https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/shader_nodes/shader/volume_scatter.rst
- Blender Manual source — EEVEE World settings (Mist Pass, Light Probe, Sun): https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/eevee/world_settings.rst
- Blender Manual source — EEVEE Volumes render settings: https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/eevee/render_settings/volumes.rst
- Blender Manual source — Cycles Volumes render settings: https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/cycles/render_settings/volumes.rst
- Blender Manual source — Render passes (Mist, Cryptomatte): https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/layers/passes.rst
- Blender 5.0 Cycles release notes (null-scattering volumes): https://developer.blender.org/docs/release_notes/5.0/cycles/
- Blender Devtalk — "Physical units on Volume Scatter and Volume Absorption": https://devtalk.blender.org/t/physical-units-on-volume-scatter-and-volume-absorption/28572 (search excerpt)
- Blender Artists — "Simulating accurate atmosphere over about 5–10 km distance": https://blenderartists.org/t/simulating-accurate-atmosphere-over-about-5-10km-distance/1221269
- Blender Artists — "What makes a render look like a world, and not a render?": https://blenderartists.org/t/what-makes-a-render-look-like-a-world-and-not-a-render/593291
- Environment-art set-dressing practice (search excerpts): Polycount https://polycount.com/discussion/comment/2804449 ; 80.lv storytelling environment in Blender https://80.lv/articles/building-uncharted-inspired-environment-in-blender-with-storytelling-focus ; Outpost VFX tips https://outpost-vfx.com/en/news/22-pro-tips-and-tricks-for-environment-artists
