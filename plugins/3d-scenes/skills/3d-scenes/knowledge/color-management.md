# Color Management — scene-linear, view transforms, textures, and delivery to editors (Blender 5.x)

> Status: Knowledge (research + expert synthesis + video extraction). Target Blender 5.2 LTS. Checked against the Blender 5.0 color-management release notes and the 5.2 manual (Displays & Views).
> Related: `rendering.md`, `compositing.md`, `ai-slop-diagnosis.md`, techniques `color-view-transform-exposure`, `color-linear-acescg-resolve-handoff`.

---

## 0. The mental model (read this once and everything else follows)

```
 textures (sRGB → linear)  ─┐
 light powers (W, physical) ├─► RENDER in scene-linear (working space) ─► [compositor works here, linear]
 material colours (linear) ─┘                                            │
                                                     Exposure (stops) ──►│
                                                     Look / Curves  ───►│ ► VIEW TRANSFORM (AgX/ACES/…) ► DISPLAY (sRGB/Rec.1886/P3) ► pixels on screen / PNG / ProRes
                                                                         │
                                                                         └─► EXR saves HERE (linear, no view transform)
```

1. **Scene-linear:** the renderer computes light quantities proportional to physical energy. 2× the light = 2× the value. Values have no upper limit (a lamp can be 50.0). All maths (blur, glow, add, multiply, denoise) is physically correct only in linear [vtdczoXVyvQ@19:15].
2. **View transform (tone mapping):** compresses unbounded scene values into the display's 0–1 range. This is where "film-like" or "digital/clipped" character comes from. It is *not* a filter. It is how the camera/film responds.
3. **Display:** the encoding for the monitor or deliverable (sRGB piecewise ~2.2 gamma for computer screens/web; Rec.1886 2.4 gamma for broadcast/TV grading; Display P3; Rec.2100 PQ/HLG for HDR).
4. **Working space (new in 5.0):** the gamut that "linear" means in this file: **Linear Rec.709** (default), **Linear Rec.2020**, or **ACEScg**. Change it under Color Management › Working Space (with an option to convert existing colours).

---

## 1. View transforms in Blender 5.x (Render Properties › Color Management › View)

| View | What it does | Use for | Avoid for |
|---|---|---|---|
| **Standard** | Only the display transform. Values > 1.0 clip; colours stay saturated until they clip with hue skew | UI, flat graphics, logos in 3D where exact sRGB colour matters and nothing exceeds 1.0; NPR/toon; editing footage in the VSE | any scene with bright lights, emissives, sun, specular highlights. It creates **blown, flat highlights**, the #1 render slop sign |
| **AgX** (default since 4.0) | ~16.5 stops of range; highlights roll off; saturated bright colours desaturate toward white (like film/sensors) | the default for cinematic/mixed scenes, emissive/neon scenes, interiors, exteriors [lE308jCAT2o@00:30] | colour-critical brand/product colours (AgX slightly desaturates and shifts saturated hues) |
| **Khronos PBR Neutral** | minimal hue/saturation change for well-exposed base colours; compresses only near the top | **product shots, e-commerce, brand colours**, packaging, "what you set is what you get" | very high dynamic range scenes (sun + shadows), where highlights compress harshly |
| **ACES 1.3** (5.0+) | the classic ACES RRT/ODT; contrasty, film-standard look | photoreal shots that must match an ACES pipeline or footage | when you want AgX's softer highlight desaturation |
| **ACES 2.0** (5.0+) | more neutral than 1.3: less mid-tone contrast, gentler highlight rolloff | photoreal, matching live action in an ACES 2 pipeline | — |
| **AgX HDR / ACES HDR variants** | the same for HDR displays | HDR deliverables only | SDR VSL (the default case) |
| **Filmic** | deprecated, superseded by AgX | opening old files | new work [gmGMsKJ6xd8@08:15 still mentions it] |
| **Filmic Log / AgX Log** | log encodings | grading inspection/export to a colourist | final viewing |
| **False Color** | heat map of exposure | **exposure checking** [lE308jCAT2o@00:45] | final |
| **Raw** | no conversion | inspection of data | final |

### Looks (Color Management › Look)
With AgX: **Punchy** [0M0-TESgB7E@00:00], Greyscale, Very High / High / **Medium High** [1MyARLB8KzY@10:00] / Base / Medium Low / Low / Very Low Contrast. Looks act *before* the display conversion and are tied to the selected view (switching the view resets or changes the available looks).
- Base Contrast / None: neutral starting point.
- Medium High / High: for flat, low-contrast scenes (overcast, fog-heavy).
- Punchy: more saturation and contrast. Risky with already saturated colour schemes (neon), where it produces garish slop.

### Exposure, Gamma, Curves, White Balance
- **Exposure** (stops, before the view transform): output = value × 2^exposure. The correct global brightness control. Prefer fixing light powers. Use Exposure for global shifts (±0.5 typ.) [1MyARLB8KzY@10:15], [lE308jCAT2o@01:15].
- **Gamma** (after the view transform): an artistic tweak only. Leave at 1.0. The display transform already handles encoding.
- **Curves** (Use Curves): RGB curves before the conversion. Fine for gentle global contrast, but prefer the compositor for reversible grading.
- **White Balance** (5.x): Temperature/Tint relative to D65. Neutralise a warm/cool cast globally, or deliberately warm a scene (e.g. 5000 K → warmer). Easier than retinting every light.

### Exposure workflow with False Color (objective, no guessing)
1. View → False Color. 2. Adjust exposure or key light power until the subject (face, product label) sits in the **grey/green middle bands**. Only speculars and light sources reach yellow/orange; large red/white areas mean overexposed [lE308jCAT2o@00:45–01:15]. Large blue/purple areas mean crushed. 3. Back to AgX.

---

## 2. Texture colour spaces (Image Texture node › Color Space)

| Map | Color Space | Why |
|---|---|---|
| Base Color / Albedo, emission colour maps, HDRIs (.hdr/.exr) | **sRGB** for 8-bit PNG/JPG colour; **Linear Rec.709** (or the file's tagged space) for EXR/HDR | colour images are display-encoded and must be linearised; HDR files are already linear |
| Roughness, Metallic, Normal, Bump/Height, Displacement, AO, Opacity/Alpha masks, Specular, ID masks | **Non-Color** | these are *data*; an sRGB decode would bend the values (roughness wrong, normals skewed) |
| ACEScg textures from studios | **ACEScg** | match the file |

Slop signs from wrong texture spaces: normal maps set to sRGB (lighting looks bent/embossed wrong); roughness as sRGB (surfaces too glossy or too matte, "plastic"); albedo as Non-Color (washed-out, pale colours).
A quick bpy audit: list all Image Texture nodes whose image name contains normal/rough/metal/disp/ao/height and whose `colorspace_settings.name != 'Non-Color'`.

**Material colours:** colour pickers show linear values with Linear and Perceptual sliders (5.0). A hex code in the picker is display-encoded. Type brand hex codes as hex, not as RGB floats. Keep albedo within plausible ranges (≈ 0.03–0.85 linear; pure 1.0 white or 0.0 black albedo looks fake).

---

## 3. ACES / OCIO — what the video claims vs what is built in

**Video claim (vtdczoXVyvQ):** export EXR with Output › Color Management **Override** to a linear space or **ACEScg** ("most other software knows how to handle ACES") [19:30]. The image "should look awful" in a non-managed viewer [19:45]. In Resolve, use an **OCIO ColorSpace** node pointing at Blender's `config.ocio`, source = ACEScg, output = "AgX Base sRGB" [20:00–20:30], [29:15–30:15]. Then a CST into DaVinci Wide Gamut/Intermediate, grade, CST to Gamma 2.4 [30:45–31:30].

**What Blender 5.x actually has built in:**
- Bundled OCIO config (OCIO 2.5 since 5.1) at macOS `/Applications/Blender.app/Contents/Resources/5.2/datafiles/colormanagement/config.ocio`.
- **Working Space** per file: Linear Rec.709 (default) / Linear Rec.2020 / **ACEScg** (5.0). Linked/appended assets auto-convert.
- **ACES 1.3 and ACES 2.0 view transforms** (SDR + HDR) built in, plus AgX HDR (5.0). No custom ACES config is needed for the ACES look.
- Displays: sRGB, Display P3, Rec.1886, Rec.2020; HDR Rec.2100 PQ / HLG.
- Compositor: **Convert Colorspace** node (now with a "Working Space" option), **Convert to Display** node (5.0).
- EXR files carry an `interop_id` colour-space identity (5.1), which helps other apps auto-detect.
- `BLENDER_OCIO` environment variable to use a custom config for Blender only (e.g. a studio ACES config).

**Verdict:** the video's linear-EXR + OCIO-in-Resolve workflow is correct and still valid. In 5.x it's simpler: ACEScg can be the working space, and ACES views exist natively. For a solo VSL editor, it's only worth it when a colourist or heavy comp is involved [vtdczoXVyvQ@32:30: "if you don't know why you need this, you don't need it"].

---

## 4. Working with editors (Premiere Pro / DaVinci Resolve)

### Option B — "Data for grading" (colourist / Resolve heavy)
- EXR (half, DWAA) scene-linear. Resolve: either Fusion OCIO ColorSpace with Blender's config (exact AgX match) [vtdczoXVyvQ@29:30], or Resolve Color Management with the input = ACEScg/Linear (the ACES look, not AgX).
- Alternative middle ground: render **AgX Log / Filmic Log** baked into ProRes 4444 / 16-bit PNG, and the colourist applies the LUT or transform. (Lighter than EXR. Verify the log space availability in the 5.2 view list.)

### Option C — "Transparent elements over live footage"
- Film › Transparent, PNG 16-bit RGBA or EXR. View transform: same as the rest. Make sure the editor interprets the alpha as **premultiplied** (Blender's PNG output is straight alpha; EXR is premultiplied). Mismatch → dark or bright fringes.

---

## 5. Slop signs in colour (detection → fix)

| Sign | How to detect | Fix |
|---|---|---|
| **Clipped highlights, hue-skewed lights** (orange lamp turns yellow, blue screen turns cyan, flat white blobs) | view = Standard; histogram spike at 1.0; False Color red areas | AgX/ACES; lower exposure/lights; Clamp |
| **Oversaturated "neon" image** | mean saturation high; many pixels at max chroma; Punchy + saturated materials | lower material saturation (albedo chroma ≤ ~0.8), Look Base, accent colour only on the hero |
| **Crushed blacks** | > 5% of pixels at near 0; no shadow detail | a fill/bounce light, World strength > 0, a slight black lift in the curve (0.01–0.03) |
| **Grey, washed-out image** | AgX + underexposure lifted in comp; low-contrast look on a flat scene | expose correctly (False Color), stronger key:fill ratio, Base → Medium High Contrast look |
| **Wrong texture spaces** | normal/roughness as sRGB | Non-Color (§2) |
| **Teal-orange everywhere** | split toning affects product/brand colours | mask the grade or reduce it; keep brand ΔE < 3 |
| **Mismatch between Blender and the editor** | the editor shows darker/lighter/shifted footage | check display (sRGB vs Rec.1886), PNG vs EXR interpretation, alpha mode; test with a grey ramp |
| **Banding** | stepped gradients after the grade/export | 16-bit/EXR, Dither, grain |
| **Logo colour wrong** | brand hex vs rendered pixel ΔE > 3 | PBR Neutral or Standard for that shot, emissive logo at ≤ 1.0, or composite a flat logo in the edit |

---

## 6. Default policy for this OS (what Claude should set unless the brief says otherwise)

1. Working Space: Linear Rec.709 (default). ACEScg only for a colourist pipeline.
2. View: **AgX**, Look **None/Base Contrast**. Product/brand hero: **Khronos PBR Neutral**. Photoreal matched to footage: ACES 2.0.
3. Display: sRGB (web VSL). Exposure set with False Color. Gamma 1.0.
4. Textures: colour = sRGB, data = Non-Color (audit with bpy).
5. Output: EXR half for anything going to comp; PNG16 → ProRes for the editor.

## Sources
- Videos: vtdczoXVyvQ, lE308jCAT2o, 0M0-TESgB7E, 1MyARLB8KzY, gmGMsKJ6xd8 (see `sources/`).
- Blender 5.0 color management release notes (working space, ACES 1.3/2.0 views, HDR displays, Convert to Display): https://developer.blender.org/docs/release_notes/5.0/color_management/
- Blender 5.1 rendering notes (OCIO 2.5, interop_id): https://developer.blender.org/docs/release_notes/5.1/rendering/
- Blender 5.2 manual — Displays and Views: https://docs.blender.org/manual/en/latest/render/color_management/displays_views.html
