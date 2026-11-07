# Materials & PBR — practical guide (Blender 5.2)

Status: **Extracted** (sources + expert knowledge; nothing here is Validated yet). Numbers are *starting points* with stated assumptions: scene in metres, scale applied, Cycles or EEVEE (5.x), AgX view transform unless noted.
Cards: `techniques/materials-*.md`. Sources: 8HfKtaDx6tM, aUnpMrAYzGs, RfPro3hlOMg, SaZOuHQROIg, LPCdpTcNXyM, R4sOG6OPioc, J_mweAPcO4M.

---

## 0. The 10-second version
1. Reference first; decide the material's *condition* (new / used / abused) [8HfKtaDx6tM@06:45].
2. Roughness carries realism. Never one flat value on a visible glossy surface.
3. Albedo in physical ranges: no pure black, no pure white, lower saturation than you think.
4. Metallic is 0 or 1. Mixed values only in transition masks.
5. Real scale: texture feature size, bevel size, displacement depth in metres.
6. Layer: base → macro variation → dirt/dust (cavities) → wear (edges) → story details (hand-placed).
7. Subtle. Imperfections should be *felt* in highlights, not *seen* as patterns.

---

## 1. PBR theory you actually need

### 1.1 Energy split: diffuse vs specular
Every surface reflects some light at the surface (specular, Fresnel-governed) and — if dielectric — scatters the rest under the surface (diffuse colour = albedo). Metals have no diffuse; their colour lives in the specular reflection. That's why Metallic is a *material class switch*, not a "shininess" slider.

### 1.2 Albedo (Base Color) ranges
Albedo = colour with **no lighting, no shadow, no AO, no highlights**. Physical range for non-metals ≈ **0.02–0.9 linear** (≈ 30–240 sRGB 8-bit).

| Material | Approx. albedo (linear, luminance) | sRGB 8-bit approx. |
|---|---|---|
| Charcoal, black rubber, black paint | 0.02–0.05 | 30–60 |
| Asphalt (fresh/worn) | 0.04–0.12 | 50–95 |
| Dark wood, soil | 0.05–0.15 | 60–110 |
| Bare concrete | 0.15–0.35 | 110–160 |
| Human skin (range) | 0.1–0.5 | 90–190 |
| Light wood / sand | 0.3–0.5 | 150–190 |
| White paint / plaster | 0.65–0.85 | 210–235 |
| Fresh snow | 0.8–0.9 | 230–245 |

- **No pure black** (0.0): absorbs all light → renders as a hole, no form, no bounce. Darkest real: ~0.02–0.03.
- **No pure white** (1.0): every bounce keeps 100% energy → blown-out, slow-converging, glowing look, and it brightens the whole room's GI. Use ≤0.85–0.9.
- **Saturation:** real materials are surprisingly desaturated. A "red" car paint or brand colour still has saturation well below 100% in linear. Over-saturated albedo is a classic slop sign (toy/plastic look), and AgX will desaturate bright saturated values anyway (see §9).
- Colour picker gotcha: **Hex is sRGB display-encoded**, the RGB/HSV fields are scene-linear. Typing a brand hex is correct; typing sRGB numbers into RGB fields is not.
- Remove baked lighting: photo textures with shadows/highlights are not albedo (see `techniques/materials-photo-texture-chaos.md`).

### 1.3 Metallic is binary
- 0 = dielectric (plastic, wood, paint, stone, skin, glass, rubber, fabric). 1 = bare conductor (steel, aluminium, chrome, gold, copper).
- Values in between are physically meaningless except as **anti-aliased transitions** in masks (paint chipping revealing metal) or dust/oxide layers over metal.
- Painted metal is **not** metal — it is paint (Metallic 0) until it chips.
- Rust is not metal (Metallic 0, rough, orange-brown albedo ~0.1–0.25).
- Metal "colour" (Base Color at Metallic 1) = reflectance at normal incidence (F0), and it is **bright**:

| Metal | Base Color (linear RGB, approx.) |
|---|---|
| Silver | 0.97, 0.96, 0.91 |
| Aluminium | 0.91, 0.92, 0.92 |
| Chrome | 0.55, 0.56, 0.55 |
| Iron / steel | 0.53–0.56, 0.54–0.57, 0.54–0.58 |
| Gold | 1.0, 0.77, 0.34 |
| Copper | 0.96, 0.64, 0.54 |
| Brass | 0.91, 0.78, 0.42 |

Dark metal base colours (<0.5) look like dirty plastic. Metals look "dark" mostly because they reflect a dark environment — fix the environment, not the albedo.
- In 5.x, Principled **Specular ▸ Tint** on metals tints the **edges** (grazing reflection) to simulate complex IOR (gold, copper) (docs.blender.org 5.2 manual, Principled BSDF).

### 1.4 Roughness — the most important map
- Controls microfacet spread: 0 = mirror, 1 = fully diffuse-looking highlight.
- Why it matters most: highlights and reflections are the brightest, most attention-grabbing part of a rendered surface; roughness *variation* is how eyes read use, touch, grease, dust, age. Uniform roughness = "plastic CG".
- Typical bands (variation inside the band, not a single value):

| Surface | Roughness band |
|---|---|
| Mirror, polished chrome, clean glass | 0.0–0.08 |
| Car clear-coat (Coat Roughness) | 0.02–0.1 |
| Glossy plastic, glazed ceramic, varnish | 0.1–0.3 |
| Satin paint, brushed metal | 0.25–0.45 |
| Matte plastic, worn metal, leather | 0.4–0.65 |
| Wood (unfinished), skin | 0.45–0.7 |
| Concrete, plaster, fabric, paper | 0.7–0.95 |

- Always remap texture outputs into the band (`techniques/materials-value-range-remap.md`) [RfPro3hlOMg@02:45].
- Roughness map convention: white = rough, black = glossy [SaZOuHQROIg@04:30]. If a vendor ships **Gloss/Smoothness**, invert it.

### 1.5 Specular, IOR, Fresnel (Blender 4.0+/5.x model)
- Dielectric reflectance is driven by **IOR** (default 1.5 ≈ 4% at normal incidence). The old "Specular 0.5" slider is gone; **Specular ▸ IOR Level** scales it: **0.5 = no change**, 0 = no reflections, 1 = double at normal incidence (manual 5.2).
- IOR starting values: water 1.33, ice 1.31, skin/organic ~1.4, plastic 1.46–1.5, glass 1.45–1.52, car paint coat 1.5, sapphire 1.77, diamond 2.42.
- Fresnel: all surfaces get more reflective at grazing angles — this is automatic; don't fake rim reflections with Fresnel nodes on the base.
- Use IOR Level < 0.5 only for materials that seem too "wet": cloth, chalk, dusty surfaces; or drive it with a cavity mask (micro-occlusion of specular in crevices).

### 1.6 Normal vs bump vs displacement
| | What it changes | Cost | Silhouette | Use for |
|---|---|---|---|---|
| **Normal map** | shading normal from RGB tangent-space map | cheap | no | baked or scanned mid/fine detail |
| **Bump** (height → Bump node) | shading normal from grayscale height | cheap | no | fine detail, procedurals, extra detail on top of normal map |
| **Displacement** (true) | moves vertices | expensive (geometry) | **yes** | relief seen at grazing angle / silhouette: bricks, stone, terrain, close-up bark |

- Normal maps: Image Texture **Non-Color** → **Normal Map** node (Tangent space) → Principled Normal. Use **OpenGL** (Y+) maps; ambientCG "_NormalDX" is DirectX — skip it or invert G [aUnpMrAYzGs@03:30]. Strength 0.5–1.0; >1.5 almost always looks fake.
- Combine normal + extra detail: Normal Map → **Bump ▸ Normal** input; detail → Bump Height [LPCdpTcNXyM@00:00]. Overlay-mixing two normal maps [8HfKtaDx6tM@10:45] is an approximation.
- If Node Wrangler adds a Bump node *and* a Normal map from the same set, set Bump Strength to 0–0.1 to avoid double detail [aUnpMrAYzGs@03:45].
- True displacement: Material ▸ Settings ▸ Surface ▸ **Displacement and Bump**; Displacement node Scale in metres (real relief depth, e.g. 0.01–0.05), Midlevel per vendor (usually 0.5). Geometry from Subdivision Surface with **Adaptive Subdivision** (Cycles; non-experimental since 5.0, has an Object-space option) — not "level 8" [aUnpMrAYzGs@04:45]. Use EXR/16-bit heights [aUnpMrAYzGs@02:30].
- 5.0 change: with displacement, the Normal Map node uses the undisplaced normal/tangent (matches EEVEE).
- Card: `techniques/materials-displacement-adaptive.md`.

### 1.7 Ambient Occlusion maps
- Path tracers (Cycles) and EEVEE (5.x, with horizon scan/raytracing) compute occlusion. An AO map multiplied into albedo **double-darkens** and bakes occlusion that doesn't respond to light direction.
- Use AO maps only: (a) at low strength (Mix Color Multiply, factor 0.2–0.5) [aUnpMrAYzGs@04:00] for micro-cavities the geometry/normal map can't produce; (b) as a **mask** for dirt/dust accumulation (better use).
- The **Ambient Occlusion shader node** (Only Local) is a live cavity mask — great for dirt, but costly (`techniques/materials-smart-masks-edge-wear-dirt.md`).

---

## 2. Principled BSDF in Blender 5.x — current inputs (from docs.blender.org 5.2 manual)
Top-level: **Base Color, Metallic, Roughness, IOR, Alpha, Normal**, plus **Thin Wall** toggle (thin-walled mode for paper, leaves, window sheets — Subsurface radius/scale/method irrelevant in thin-walled mode).
- **Diffuse** panel: Roughness (Cycles only; 0 = Lambert, >0 Oren-Nayar) — useful for dusty/clay/fabric/moon-like surfaces 0.3–0.8.
- **Subsurface**: Method (Christensen-Burley; Random Walk; Random Walk (Skin); Random Walk (Legacy)), Weight (typically 0 or 1), Radius (RGB mean free path), Scale (in scene units), IOR (Cycles), Anisotropy (Cycles). 5.0: random-walk SSS supports multiple bounces (less darkening).
- **Specular**: Distribution (GGX / Multiscatter GGX), IOR Level (0.5 neutral), Tint, Anisotropy (Cycles), Anisotropic Rotation (Cycles), Tangent.
- **Transmission**: Weight.
- **Coat**: Weight, Roughness, IOR (1.0–2.0), Tint, Normal (separate normal for coat).
- **Sheen**: Weight, Roughness, Tint.
- **Emission**: Color, Strength (1.0 = exactly the colour, "shadeless").
- **Thin Film** (Cycles): Thickness (nm; strongest ~100–1000 nm), IOR (default 1.33). 5.0: thin film also on metals (oxide iridescence on titanium, heated steel).
- Scripting: look nodes up by `type == "BSDF_PRINCIPLED"`, and inputs by their English identifiers ("Base Color", "Coat Weight", "Specular IOR Level", "Transmission Weight", "Emission Strength", "Subsurface Weight"…) — verify in 5.2 with `[i.name for i in node.inputs]` before setting.
- Old tutorials (≤3.6): "Specular 0.5" → IOR Level 0.5; "Clearcoat" → Coat Weight; "Transmission" → Transmission Weight; "Subsurface" + Subsurface Color → Subsurface Weight (colour comes from Base Color); "Sheen Tint" semantics changed.

---

## 3. Surface imperfections (the realism layer) — SUBTLE
Card: `techniques/materials-roughness-imperfections.md`, `techniques/materials-smart-masks-edge-wear-dirt.md`.

| Imperfection | Where it physically occurs | Mask source | Channel |
|---|---|---|---|
| Fingerprints, smudges, grease | touch areas (handles, screens, glass, glossy plastic) | smudge texture × hand-painted/positional mask | Roughness (±0.05–0.2), Coat Roughness if coated |
| Micro-scratches | glossy hard surfaces, convex zones | scratch texture × edge/convexity mask | Roughness (Coat Roughness for coated), tiny bump |
| Dust | upward-facing surfaces, cavities, untouched areas | Normal Z ▸ ramp × AO × noise | Albedo lighten (+desat), Roughness up, IOR Level down |
| Dirt/grime | cavities, lower parts, contact with ground | AO node / curvature / Z-gradient × grunge | Mix Shader to dirt material |
| Edge wear / chipping | convex edges, corners, handles | Bevel·Normal dot, Pointiness, Edge Angle attribute, baked curvature × grunge | Mix Shader to underlying material; height dip |
| Water stains, rising damp | bottom of walls, under windows/drips | Z-gradient / Empty-driven gradient + noise | Albedo darken, Roughness down |
| Fading | sun-exposed faces | Normal toward window/sun | Albedo desaturate/lighten |

Rules:
- **Physics before noise**: every imperfection needs a reason to be *there* [RfPro3hlOMg@09:30].
- **Break geometric masks** with grunge — pure curvature masks look like outlines.
- **Subtlety test**: at final delivery resolution (often 1080p or less for VSL), imperfections should be visible mainly in highlights/reflections. If you notice the pattern in diffuse areas, halve it.
- **Hero products in ads**: brand-new condition — fingerprints/dust *very* sparse (or only on surroundings: table, glass), never grunge on the product.
- **Hand-paint the story**: texture paint masks for where people grab things, where something was hit [8HfKtaDx6tM@12:00]; vertex paint for UV-less dense meshes [aUnpMrAYzGs@16:00].
- Sources for imperfection maps: Poly Haven / ambientCG (CC0), Megascans via Fab (licence-dependent), own photos; add-ons (Realistic Touch) mentioned by [RfPro3hlOMg@08:45] — paid.

---

## 4. Texture scale & texel density
- **Real-world scale first**: object dimensions in metres, scale applied (`techniques/assets-real-world-scale.md`). Then texture scale = real size of the scan. A Poly Haven texture page lists its physical size (e.g. "2 × 2 m"); Mapping Scale = object-space metres / scan size.
- Reference feature sizes: brick 21.5×6.5 cm (+1 cm mortar); floor plank 10–20 cm wide; floor tile 30–60 cm; concrete formwork panels 1.2×2.4 m; wood grain rings ~2–10 mm; fabric weave 0.5–2 mm; fingerprint ~1.5–2 cm.
- Wrong texture scale changes perceived object size (scaled-down rock texture → cliff [LPCdpTcNXyM@04:45]) — the #1 "toy/miniature" cause after DoF.
- **Texel density**: aim ~1 texel per screen pixel at the closest framing. Rule from [aUnpMrAYzGs@02:00]: extreme close-up 8K, foreground 4K, background 2K (assumes 1080p). For 1080p VSL output, a surface filling half the frame width needs only ~1–2K across it. Keep consistent across neighbouring objects — mismatched sharpness reads as composite/CG.
- Colour maps sRGB; all data maps (roughness, metallic, normal, height, AO, masks) **Non-Color**.

## 5. UV vs Box/Tri-planar vs Generated/Object projection
| Method | Pros | Cons | Use for |
|---|---|---|---|
| UV unwrap | exact control, directional textures, painting, baking, decals | needs good topology/seams; time | hero assets, wood grain, fabric, labels, characters, anything painted |
| Box (tri-planar), Object coords | no UVs, consistent density, robust on scans/AI meshes | 3× lookups; blend smear at 45°; normal maps approximate; swims on deformation | rocks, concrete, plaster, terrain chunks, background props |
| Generated coords | quick | stretches with object bounds | rarely; procedural previews |
| World coords | seamless across many objects (walls/floors continuing) | texture slides when object moves | static architecture |
- Box blend 0.1–0.3 (0.2 default) [8HfKtaDx6tM@07:30]; Alt-change to set all nodes.
- Smart UV Project is fine for many props; follow with Average Islands Scale + Pack Islands [8HfKtaDx6tM@04:15].
- Editing modelled geometry with UVs: enable **Correct Face Attributes** to avoid UV stretching [LPCdpTcNXyM@00:15].
- Card: `techniques/materials-box-projection-object-coords.md`.

## 6. Avoiding visible tiling
Card: `techniques/materials-anti-tiling-macro-variation.md`.
1. Macro colour + roughness variation from a large-scale grunge/noise (2–10× tile size) [8HfKtaDx6tM@08:30].
2. Variation that follows structure (Color Burn with base, per-brick random) [aUnpMrAYzGs@10:00].
3. Rotation bombing via Voronoi → Mapping Rotation for stochastic textures [aUnpMrAYzGs@08:30].
4. Mix two scales (non-integer ratio) of the same texture with a large mask.
5. Height-driven overlays (dirt/moss/dust) and decals that break the grid [aUnpMrAYzGs@11:00].
6. Scene-level: props, rugs, light falloff, DoF hide repeats.
Detection: squint at the frame / downscale it — repeating dark spots in a grid = tiling.

## 7. Layered material workflow (node organisation)
- Base material per node group, expose Scale, Displacement scale, and **Height** output [aUnpMrAYzGs@06:15].
- Layers combined with **Mix Shader** when materials differ physically (paint vs metal, base vs dirt); **Mix Color** when only colour changes; heights mixed separately with the same mask [aUnpMrAYzGs@14:45].
- Never **Add Shader** for layering opaque materials — it adds energy (use only for effects) [RfPro3hlOMg@07:15].
- Masks: remap/crisp them so incompatible materials don't blend in a 50/50 mush [RfPro3hlOMg@07:45].
- Per-object variation from one material: **Object Info ▸ Random** → hue/value/roughness jitter; or **Attribute** node (Object/Instancer custom properties, or GN Store Named Attribute) [RfPro3hlOMg@14:00–16:45].
- Height-driven blending: `techniques/materials-height-blend-layers.md`.

---

## 8. Material recipes (starting points, metres, Cycles/EEVEE 5.x)
Each: **base** settings → **realism layers** → **failure signs**.

### Wood (varnished furniture)
- PBR wood scan, UVs with grain along the long axis (box projection only for non-directional chunks). Albedo dark wood 0.05–0.15, light 0.3–0.45.
- Varnish: Coat Weight 0.6–1, Coat Roughness 0.05–0.2 with smudge/scratch variation; base Roughness 0.4–0.6 from map. Satin/oiled: no coat, roughness 0.3–0.5.
- Layers: colour variation per plank (Object Info Random / Voronoi cell), edge wear revealing lighter wood (lower coat weight there), dirt in cavities, chips via painted mask + height dip [8HfKtaDx6tM@11:30–13:00].
- Fails: grain running across a chair leg; identical planks; plastic-even gloss.

### Painted metal
- Paint layer: Metallic 0, albedo per colour (desaturated), Roughness 0.3–0.6 (satin) or Coat for glossy enamel.
- Under-layer: bare steel Metallic 1, Base ~0.55, Roughness 0.3–0.5; maybe primer layer (grey/red-oxide, Metallic 0).
- Mask: edge wear (convex) × grunge → Mix Shader; rust in cavities/bottoms (Metallic 0, rough 0.7–0.9, orange-brown) [RfPro3hlOMg@09:45].
- Fails: whole surface Metallic 0.5; uniform outline wear.

### Brushed metal (aluminium/steel appliances)
- Metallic 1, Base 0.85–0.92 (Al) / 0.55 (steel), Roughness 0.25–0.4; **Specular ▸ Anisotropy 0.5–0.8**, Tangent node (UV map or radial for round brushing) — Cycles only.
- Fallback (EEVEE / no tangents): stretched noise (Mapping scale e.g. X 1, Y 200–500) into roughness ±0.05 and very subtle bump.
- Fails: anisotropy direction wrong; brushing scale visible as stripes too big.

### Chrome / polished metal
- Metallic 1, Base 0.55–0.6 (not white), Roughness 0.02–0.08 + smudge/fingerprint variation, tiny micro-scratch bump.
- Chrome lives or dies by its environment: needs an interesting HDRI/reflection cards; a plain grey world = dead chrome.
- Fails: looks like grey plastic (environment too flat); perfect mirror without smudges.

### Plastic
- Metallic 0, IOR 1.46–1.5, Roughness: glossy 0.1–0.25, matte 0.4–0.6; subtle micro-texture bump (injection-moulded grain) at small scale; slight colour desat.
- Thin/light-coloured plastic: small Subsurface (Weight 1, Scale a few mm) or Thin Wall for sheets. Avoid Transmission for opaque plastic (contrary to [RfPro3hlOMg@00:30]).
- Fails: the default Principled with one colour = the classic "AI/CG plastic"; fix with roughness variation + bevels + grain.

### Glass
- Transmission Weight 1, IOR 1.45–1.52, Roughness 0–0.05, base colour ~0.95–1.0 (slight green for thick soda-lime); model thickness (Solidify 3–6 mm) or Thin Wall for single sheets.
- Fingerprints/dust in roughness [8HfKtaDx6tM@14:15]; droplets in bump [LPCdpTcNXyM@00:30]; Light Path shadow-ray shortcut for non-hero windows [LPCdpTcNXyM@01:15].
- Render: Light Paths Transmission bounces ≥ 8–12; EEVEE: enable raytracing / refraction per material settings.
- Card: `techniques/materials-glass-realism.md`.

### Liquids
- Water: Transmission 1, IOR 1.33, Roughness 0–0.02; surface ripples via bump/displacement.
- Coloured drinks (coffee, juice, cola): Principled transmission with near-white Base Color **plus Volume Absorption** (colour = drink, density tuned to thickness: e.g. coffee density 20–100 in metres scale) — colour from depth, not from tinted surface. Milk/juice opaque-ish: Subsurface or Volume Scatter.
- Glass + liquid: liquid mesh overlaps glass inner wall slightly (≈0.1 mm) so the interface refracts correctly; meniscus curve up the wall.
- Fails: liquid looks like coloured glass (no depth-dependent colour); hard flat top without meniscus.

### Fabric
- Roughness 0.7–0.95, IOR Level 0.3–0.5 (low specular), **Sheen Weight 0.3–1, Sheen Roughness 0.3–0.5** (velvet/cotton fuzz), Diffuse Roughness 0.3–0.6 (Cycles).
- Weave normal/bump at real scale (0.5–2 mm threads); UVs follow the garment/cushion; colour variation & lint; wrinkles in geometry (cloth sim/sculpt), not textures.
- Fails: fabric shiny like plastic; weave visible at metre scale; perfectly smooth cushions.

### Concrete
- Albedo 0.15–0.35, Roughness 0.7–0.95, bump/height for pores; macro stains, formwork lines, water streaks under edges, darker damp bottom.
- Box projection OK; displacement only for close-ups/broken edges.

### Plaster / painted wall
- White paint albedo 0.65–0.8 (not 1.0), Roughness 0.8–0.9 (matte) / 0.4–0.6 (eggshell), subtle roller/orange-peel bump (very low strength), large-scale grime near floor/switches/corners, slightly wavy geometry [R4sOG6OPioc@01:15].
- Fails: perfectly flat, perfectly white, perfectly clean wall = 3D-viewport look.

### Skin (basics)
- Base Color albedo per skin tone (0.1–0.5 luminance), **Subsurface Weight 1, Method Random Walk (Skin)**, Radius ≈ (1.0, 0.35, 0.2) relative, **Scale ≈ 0.003–0.01 m** for a real-scale human (default scale assumes a different size — check), Subsurface IOR ~1.4.
- Roughness 0.35–0.55 with a roughness map (T-zone oilier: lower; cheeks rougher), specular map/cavity to kill specular in pores; micro-normal detail (pores) at real scale.
- Fails: wax/jelly look (SSS scale too large), plastic skin (uniform roughness), dead grey skin (SSS off).

---

## 9. Colour management effect on materials (AgX, Blender 5.x)
- **AgX** (default since 4.0) compresses highlights gracefully and desaturates very bright/saturated colours toward white — like film. Consequences:
  - Bright saturated albedo + strong light looks *less* saturated than the picker suggests. Don't compensate by cranking albedo saturation (makes shadows/midtones toy-like); use the Look (e.g. Punchy / higher contrast) or grade in post.
  - Brand colours shift. For packshots with brand-critical colour, test **Khronos PBR Neutral** (designed to keep base colours faithful) or Standard with careful exposure, or composite brand elements.
- **Standard** view clips highlights hard — emissive screens/lamps and white materials blow out fast; it's "the CG look" when used with bright lighting.
- Filmic Log + gamma tweak [SaZOuHQROIg@02:45] is outdated as a final look — it's a grading base.
- Blender 5.0 adds a per-file **working colour space** (Linear Rec.709 default, Linear Rec.2020, ACEScg) and ACES 1.3/2.0 and AgX HDR views; switching working space or view changes how the same material values look — pick once per project (`color-management.md`, `rendering.md`).
- Exposure in post on EXR (VSE/compositor) [J_mweAPcO4M@10:30] lets you judge materials at the final brightness; evaluate albedo *before* grading with a neutral, well-exposed lighting setup (grey-ball check: an 18% grey sphere should read mid-grey).
- Material look-dev environment: neutral HDRI (overcast/studio) + a chrome ball and a grey ball in frame during look-dev; remove for final.

---

## 10. Material QA checklist — "AI slop" signs and fixes
| # | Slop sign (what you see) | Root cause | Fix |
|---|---|---|---|
| 1 | Even, perfect highlights; surfaces look "plastic" | uniform roughness | roughness map + imperfection variation (§3) |
| 2 | Everything looks like the same plastic | default Principled values; only colour changed | material-specific recipe (§8), IOR, coat/sheen/SSS where appropriate |
| 3 | Objects look like toys/miniatures or giants | wrong texture scale / object scale | real dimensions, scan physical size, Mapping scale (§4) |
| 4 | Perfectly clean surfaces, no story | no imperfection layers | physics-based dirt/dust/wear masks, hand-painted story damage |
| 5 | Crunchy, embossed, "carved" surfaces | normal/bump strength too high | Normal strength 0.3–1, bump 0.05–0.3; compare to reference at same distance |
| 6 | Candy/toy colours | saturated albedo | desaturate; check linear albedo range; use AgX look not albedo saturation |
| 7 | Grid of repeating stains | tiling | macro variation, bombing, scale mixing (§6) |
| 8 | Black holes / blown whites | albedo 0 or 1 | clamp albedo 0.02–0.9 |
| 9 | Metal looks like grey plastic | Metallic 0.5 / dark metal base / boring environment | Metallic 1, bright F0 colour, richer reflections |
| 10 | Dents look like bumps; lighting inverted | DX normal map or sRGB normal | GL normal, Non-Color |
| 11 | Stretched/smeared texture | bad UVs / generated coords / unapplied scale | apply scale, UV or box projection |
| 12 | Imperfections everywhere equally, like a filter | random noise masks | geometry-driven masks × grunge, vary per object |
| 13 | Glass invisible/black, screens pasted-on | no thickness, no reflections | thickness/Thin Wall, coat reflection, bounces |
| 14 | Sharp edges with no highlights | no bevel | bevel modifier/shader (`assets-modeling.md`) |
| 15 | Neighbouring objects with different texture sharpness | inconsistent texel density | match resolution to screen size |
| 16 | Photo textures show contradicting shadows | baked lighting | de-lit scans, flat overcast photos |
QA procedure: (1) clay render (override material) to confirm form/light are good before blaming materials; (2) neutral HDRI look-dev with grey/chrome ball; (3) view at delivery resolution and at 200%; (4) squint/downscale test for tiling; (5) compare side-by-side with reference photo at same framing.

## Sources
- docs.blender.org Blender 5.2 manual — Principled BSDF (input names/panels, IOR Level semantics, Thin Wall, Thin Film).
- developer.blender.org — Blender 5.0 Cycles release notes (adaptive subdivision non-experimental; metallic thin film; SSS multiple bounces; Normal Map + displacement change).
- Blender 5.0 colour management (working spaces, ACES/AgX HDR) — blender.org release notes via press summaries (itsfoss, ubuntuhandbook).
- Videos: 8HfKtaDx6tM, aUnpMrAYzGs, RfPro3hlOMg, SaZOuHQROIg, LPCdpTcNXyM, R4sOG6OPioc, J_mweAPcO4M (see `sources/<id>.md`).
- Metal F0 and albedo tables: commonly published PBR reference values (e.g. physicallybased.info, Real-Time Rendering) — approximate, to be validated per scene.
