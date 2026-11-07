# Realistic Product Lighting In Blender
- url: https://youtu.be/WreZ_VKDn4M
- channel / duration / Blender version shown: Extra 3d / 8:05 / **Blender 4.3.2** (status bar, corrected from frames); Cycles
- domain(s): lighting | rendering | compositing
- evidence used: transcript + yt-dlp metadata + glass_6m05.jpg (earlier agent) + 2 contact sheets + 10 frames viewed in §6 (incl. linking_7m05.jpg).
- trust: medium–high for the structure (three-sided product lighting, glass gradients, light linking are industry-standard). Medium for specifics: no power values; contains a sponsor (Vagon) [00:45]–[01:45] and plugs for Patreon textures and a paid compositor.

## 1. Problem it solves
Products lit with default area lights show flat shapes, ugly white rectangles in reflections, washed-out glass, and floors blown out by the lights. The target is "commercial" product lighting: bright edge highlights, a shaped shadow side, soft main fill, and clean glass and floor reflections.

## 2. Techniques

### T1: Three-sided product setup: strong back, sharp side, soft opposite side  `[01:45]`, `[02:30]`–`[03:45]`
- What: (1) Set up the camera and product first [02:15]. (2) Highlight/back light: Area light behind the product, strong intensity ("don't increase it too much") [02:30]. Keep a small render-preview window open while dialling. (3) Sharp side light: snap the 3D cursor to the product (Shift+S > Cursor to Active, or Shift+right-click), Pivot = 3D Cursor, duplicate the back light, R R to orbit it to the side opposite where the product faces. Lower the intensity and reduce Spread so it gives hard shadows [02:45]–[03:30]. (4) Soft fill: duplicate it and rotate 180° (type 180) to the other side, then increase Spread [03:30]–[03:45].
- Why: the back light creates rim/edge highlights that define the silhouette and glossy edges. The low-spread light is directional (collimated), so its shadows are crisp and give texture and drama. The high-spread light wraps and lifts the shadow side. You get three distinct roles instead of three similar lights.
- Use when: matte or semi-gloss products (keyboard example). Don't use when: glass or chrome. The author says it "gets rough" on glossy objects [03:45] (see T3).
- Values (corrected from frames — not stated in narration but visible): back light Area Square **2.16 m, 100 W, Spread 180°** [02:55]; side light **110 W, Spread 50°**, 2.16 m [03:45]; fill duplicated at Spread 180°, power being lowered (digits illegible) [03:55]. Earlier assumed start, kept for small products about 30–40 cm: back 1.0×0.3 m rectangle 150–300 W at 0.6–1 m; side Spread 15–30°, 50–100 W; fill Spread 180°, 20–40 W. These numbers are ours, not the author's.
- Blender 5.2 notes: Area light > Spread exists in Cycles. EEVEE support is partial (verify). Spread narrows the emission cone, so it sharpens the beam edge and shadow penumbra like a honeycomb grid on a softbox.
- Status: Extracted

### T2: Softbox image texture on area lights to fix reflections  `[04:00]`–`[04:30]`
- What: "Area lights are sharp… reflections look terrible." Shader Editor with the light selected: Use Nodes, add Image Texture (softbox images from Patreon) into emission colour [04:00]–[04:15].
- Why: real softboxes have hotspots and falloff. A uniform rectangle in a reflection is an instant CG tell.
- Use when: glossy products in Cycles. Don't use when: EEVEE (light nodes ignored). Use emissive planes with gradients instead (T3).
- Status: Extracted

### T3: Glass: emissive gradient planes instead of area lights  `[04:30]`–`[06:15]`
- What: For glass, use planes with an Emission shader instead of area lights (same positions as T1). Back plane: delete Principled, Emission → Material Output, set the strength, then Object > Visibility uncheck Camera [05:00]–[05:15]. Scale to suit the product. Side planes: new material, Emission colour driven by Gradient Texture ← Mapping ← Texture Coordinate, then Color Ramp set to Spline interpolation, dragged soft. Rotate the gradient so the bright side faces the back of the product (rotate the plane 180° if needed) [05:45]–[06:00]. Duplicate it to the other side and rotate it a bit [06:15].
- Frame evidence (glass_6m05.jpg): a tall vertical plane with a horizontal gradient (white on one edge fading to black), Object Properties > Visibility > Ray Visibility panel open (Camera, Diffuse, Glossy, Transmission, Volume Scatter, Shadow).
- Why: on transparent and glossy surfaces you never see the light's illumination, only its reflection. A gradient strip reflected in curved glass gives the classic "smooth fade" studio look that defines the contour (bright edge rolling into dark), like strip softboxes with gradient diffusion in real bottle photography.
- Use when: glass, liquids, chrome, glossy plastic, cosmetics. Don't use when: matte objects (it makes little visible difference, and emissive meshes sample less efficiently than lights in Cycles).
- Values: "don't go too high" on strength; the author uses **Emission Strength 5.0** [07:05] (seen in frame). Typical emission strength 5–30 for planes about 0.3–1 m at 0.5–1 m, depending on exposure.
- Blender 5.2 notes: works in EEVEE and Cycles. In Cycles, emissive mesh light sampling is automatic (Material > Settings > Emission Sampling: Auto). In EEVEE, emissive meshes light the scene only through ray tracing / probes. Their reflection is what matters here, and that works. Ray Visibility path: Object Properties > Visibility > Ray Visibility > Camera.
- Status: Extracted

### T4: Light linking to keep lights off the floor  `[06:30]`–`[07:00]`
- What: once a ground is added, "the lights will destroy the reflections on the ground." Select the light > Object Properties > Shading > Light Linking > New, then drag the product (objects to be lit) into the receiver collection. Repeat for every light [06:45]–[07:00].
- Why: floor hotspots and reflections of rim lights pull attention and wash out the contact area. Linking lights to the product only gives studio-style "selective lighting" (like flags) with zero geometry.
- Use when: product shots on glossy floors; rim lights that spill. Don't use when: realism depends on the floor receiving the same light (contact shadow/bounce becomes inconsistent: a lit product sitting on an unlit floor looks pasted on). Keep at least one light (usually the key) linked to the floor too.
- Blender 5.2: Object Properties > Shading > Light Linking (Receiver Collection) and Shadow Linking (Blocker Collection). Light linking works in Cycles and EEVEE. Emissive meshes support linking only in Cycles (manual). Shadow linking: verify in EEVEE.
- Status: Extracted

### T5: "Cinematic compositor"  `[07:00]`–`[07:15]`
- Paid product. Claim: turns "sharp renders into soft good-looking renders". Reproduce with your own compositor: Glare (Bloom/Fog Glow), slight lens distortion/dispersion, a vignette, a tone curve.

## 3. Claims I doubt or must test
- "Area lights are sharp and reflections look terrible" [04:00]: they look uniform, not sharp. The fix (texture) is right, the diagnosis wording is loose.
- Light linking every light off the floor [07:00] risks a floating product. Check contact shadows.
- ~~No numeric powers were given~~ — powers are visible on screen (see §6): 100 W / 110 W at 2.16 m; glass planes strength 5.

## 4. Anti-AI-slop lessons
- Assign each light ONE job (rim, shape, fill). Three identical soft lights = flat slop.
- On glossy and glass subjects, lighting = designing reflections. Use gradient strips, not white squares.
- Control spill (light linking or flags), but keep the product grounded.

## 5. Candidate isolated test
Glass bottle (BlenderKit-type) on a dark glossy floor, Cycles. A: three plain area lights at the same positions. B: emissive gradient planes (T3) + linking. Metrics: edge definition (visible bright contour along both sides), no rectangular reflections, floor hotspot luminance reduced, contact shadow still present.

## 6. Visual verification (frames viewed)
(glass_6m05.jpg was described by an earlier agent; not redone.)
- [02:40] Back light being set: new Area.004, defaults (Square 1 m, 10 W, Spread 180°); small render-preview window bottom right shows only a thin rim on the keyboard edge. Status bar **4.3.2**.
- [02:55] crop: back light **100 W, Square 2.16 m, Spread 180°**, Max Bounces 1024.
- [03:20] annotation circle marks where the side light goes; preview shows the back light's crisp edge highlight only.
- [03:30] crop: light N panel with **Nodes › Use Nodes** button (same 2.16 m light).
- [03:45] Side light Area.006 duplicated around the 3D cursor (rotation 126° about global Z): **110 W, 2.16 m, Spread 50°**; preview shows strong hard texture across the keys.
- [03:55] crop: fill duplicate, Spread 180°, power being dragged (illegible).
- [04:15] Softbox section: Image editors show "Softbox.exr" (rectangular, hot centre, darker edges) and "Circular Light.exr" (octabox) — the textures plugged into the light; Area 1 m 10 W in a test scene.
- [05:10] Glass section: bottle on a grey backdrop, output **1000×1600 at 200%, 24 fps**, adding an Emission shader to a plane.
- [07:05] (linking_7m05.jpg) Black-and-white perfume bottle (a real brand's bottle model, "Sauvage") with gradient-plane reflections; plane material **Emission Strength 5.000**; Light Linking popup assigning the receiver collection "Perfume Sauvage".
- [07:30] Keyboard scene top view: three area lights around the keyboard.
- Quality judgement: **good, commercial-looking** — the keyboard render has a clean rim and textured key shadows; the perfume shot has crisp gradient edges. It's simple (one product, black void) but not slop. Caveat: the perfume demo uses a branded product model — fine for learning, not for our deliverables.
