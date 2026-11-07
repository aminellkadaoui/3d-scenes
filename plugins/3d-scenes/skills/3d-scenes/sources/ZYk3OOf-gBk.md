# 8 Lighting Tricks I Wish I Knew Earlier (Blender Product Lighting Tutorial)
- url: https://youtu.be/ZYk3OOf-gBk
- channel / duration / Blender version shown: Digitalist / 10:35 / not stated (uploaded 2025-07-12, so Blender 4.4–4.5; Cycles-style features used)
- domain(s): lighting | camera | materials (bevels) | composition
- evidence used: transcript + yt-dlp metadata + gobo_10m05.jpg (earlier agent) + 2 contact sheets + 10 frames viewed in §6 (incl. glassgrad_7m35.jpg).
- trust: medium–high. Clear demonstrations with A/B on/off comparisons [01:45], several distinct product scenarios, and one of the few sources that gives a number (key power 25 W, backlight 5 W, bevel values, 120 mm lens). Patreon plugs for gradients and gobos.

## 1. Problem it solves
Generic product renders: dark ugly shadows, rim lights spilling on floors, razor-sharp CG edges, white-rectangle reflections on glass and metal, boring matte products. It covers eight scenarios (sphere, cube bevels, real product 3-point, teaser, e-commerce, glass, metal, sun + gobo).

## 2. Techniques

### T1: Long lens + orbit pivot for product framing  `[00:15]`–`[00:45]`
- What: View > Cameras > Active Camera. 3D cursor at the centre, Pivot = 3D Cursor so the camera/lights orbit the centre. Camera Focal Length = 120 mm "so we don't get too much distortion… show the product exactly how it looks" [00:30].
- Why: a long lens compresses perspective and keeps product proportions true. Lighting needs a locked camera because highlights are view-dependent.
- Status: Extracted (camera domain, but a prerequisite for lighting)

### T2: Key light in front-side, tilted  `[01:00]`–`[01:15]`
- What: Area light, Pivot = 3D Cursor, placed "in front and then tilt it a little", then moved further away [01:15].
- Note: "in front" here means front-side and above, not on the camera axis. Moving it further away narrows the apparent size (harder shadows) and evens the falloff across the object.
- Status: Extracted

### T3: Fill with an invisible bounce plane instead of a light  `[01:30]`–`[02:00]`
- What: Add a Plane, scale it down, place it at the side of the sphere opposite the key. Object Properties > Visibility: disable Camera AND Shadow [01:45]. It reflects the key's light into the shadows. Hide/unhide A/B shows the shadow goes from "very dark" to "nice soft" [01:45]–[02:00]. Move it up if it makes a visible line/terminator artifact on the floor [02:00].
- Why: a bounce card is motivated fill. Its intensity automatically scales with the key (a fixed ratio), its colour is the key's colour × card albedo, and it never creates a second shadow. Disabling Shadow visibility prevents the card from blocking the key or ambient.
- Use when: any key-dominant setup. Don't use when: you need a fill with a different colour/temperature from the key (use a dim large area light) or there is no key to bounce.
- Status: Extracted

### T4: Backlight with light linking to exclude the floor  `[02:15]`–`[02:30]`, `[04:30]`–`[05:00]`
- What: Backlight behind the subject. Object Properties > Shading > Light Linking > New, drag in the Floor, and disable its check mark (exclude). Rim on the subject, no hotspot on the floor [02:15]–[02:30]. On the real product: rotate the backlight until the top surface shows a gradient instead of flat white [04:30]–[04:45]. Backlight power 5 W (key 25 W) [04:15], [05:00].
- Why: the rim's job is to separate the subject. Floor spill competes with the subject. Orbiting the rim until a surface reads as a gradient means the reflected light's falloff crosses the surface, which shows its curvature.
- Values: key 25 W, back 5 W, a 5:1 key:rim power ratio at roughly similar distances for a product of about 20–40 cm (scale not stated).
- Status: Extracted

### T5: Bevels so lights have edges to catch  `[03:00]`–`[04:00]`
- What: The default cube has edges "way too sharp" and surfaces "flat and boring". Option A: Bevel shader node → Normal, radius 0.02 [03:15]–[03:30] (shading only, the edge silhouette stays sharp when zoomed). Option B (preferred): Bevel modifier, 5 segments, Amount 0.03 [03:45].
- Why: real objects have rounded edges that catch specular highlights. That bright line is what makes lighting read on hard-surface objects. Units assume a default 2 m cube.
- Status: Extracted (materials/modeling, cross-ref)

### T6: Teaser lighting: backlights only  `[05:00]`–`[05:30]`
- What: "making a teaser and you don't want to show the entire product": only lights behind the product, linked to exclude the floor, duplicated and mirrored for rough symmetry [05:15]–[05:30].
- Why: silhouette + rim reveals shape while hiding detail. It builds mystery, ideal for reveals/hooks in marketing videos.
- Status: Extracted

### T7: E-commerce white-background setup  `[05:30]`–`[06:45]`
- What: Large strong area light overhead. Duplicate it into a very small, weaker light just for a specular highlight ("if you just have a larger light we won't get any reflections because it's too large") [05:45]–[06:00]. Cyclorama: the floor plane extruded up (E), with the joint edge bevelled (Ctrl+B, more segments), shaded smooth [06:00]–[06:30]. Add a smaller light behind to whiten the background, and raise it until the background reads white [06:30]–[06:45].
- Seen in frame [06:00]: the small specular light (Area.017) is **Square 0.45 m, 10 W** (Cycles).
- Why: big source = soft, shadowless product. The small source adds a defined specular "glint" that gives material/gloss cues. Separate background light controls background value independent of the product (pure white BG without overexposing the product).
- Status: Extracted

### T8: Gradient textures on area lights for glass and metal  `[06:45]`–`[08:30]`
- What: Glass: area light behind the glass looks "completely white and this edge is completely sharp". Light > Use Nodes > image "elliptical sharper" gradient → emission colour. Move it behind the glass, tilt it down, bring it closer [07:00]–[07:30]. "Not physically accurate, but it works" [07:30]. Optional light colour. Metal: the same gradient light, scaled tall in Z (strip), wider and stronger. Two lights behind on each side + two in front "cuz we don't want too much black areas on our metal bottle" [07:45]–[08:30].
- Why: metal has no diffuse. It is only its reflections, so you must give it things to reflect: strip lights produce the long vertical highlights of commercial bottle shots. Black areas are reflections of the black void. Some are good (contrast), too many = dead metal.
- On HDRIs: "use HDRIs sparingly because you don't have full control over the lighting" [08:30]–[08:45].
- Status: Extracted

### T9: Sun light for flat-colour matte products + gobo spotlight  `[08:45]`–`[10:00]`
- What: For matte, strong flat-colour products (you "can't play with reflections"), add a Sun for hard shadows (summer / sunscreen commercial look) [08:45]–[09:15]. Soften by increasing the Sun Angle [09:15] (frame shows Sun Strength **1.0**, Angle **0.526°** before softening — a near-pinpoint sun). Gobo: add a Spot, increase spot size to cover the scene, Use Nodes on the light and image gobo (window, leaves…) → Color [09:30]–[09:45]. Increase the light Radius slightly to soften the gobo shadow edges [10:00].
- Why: hard light = high contrast, saturated "sunny" mood. A gobo adds a motivated off-screen world (window, foliage) and breaks uniform light into shapes, which gives visual interest on otherwise flat surfaces.
- Frame evidence (gobo_10m05.jpg): Spot light, Spot Size 80°, Blend 0.150, Radius 0 m at that moment, Max Bounces 1024, Cast Shadow + Multiple Importance on. Nodes: Emission Color = Gobo1.png. A Sun is also in the scene. Result: palm-leaf shadow pattern over yellow/white bottles on a cyan backdrop with a hard sun shadow, i.e. the "summer commercial" look.
- Blender 5.2: image gobos via light nodes are Cycles-only. Use the light's Normal coordinates (Texture Coordinate > Normal → Mapping) for spot projections. EEVEE alternative: a real cutout card (alpha-masked plane) between light and subject. Larger Radius = softer projected edges (physically right).
- Status: Extracted

## 3. Claims I doubt or must test
- "Use HDRIs sparingly" is good for studio product work but wrong for integration/realism (exteriors, CG-in-live-action), where an HDRI is the basis.
- The bevel shader at 0.02 vs modifier 0.03: units are scene-scale dependent (default cube = 2 m). On a 10 cm product these are huge. Scale by object size (about 0.5–2% of the object dimension).
- Gradient textures on lights: "not physically accurate" but acceptable. Fine for stylised product work, but don't mix with physically matched HDRI scenes.

## 4. Anti-AI-slop lessons
- Shadows must not be pure black. Fill via bounce, not a second shadow-casting light.
- Sharp CG edges kill lighting. Bevel everything that should catch light.
- Match the setup to the material: matte → shadows/gobos; glossy/metal/glass → reflection design.
- Rims should not spill onto the floor.

## 5. Candidate isolated test
Sphere + bevelled cube on a floor. A: key only (25 W). B: + invisible bounce card. C: + 5 W rim linked off the floor. Measure the shadow-side luminance (A→B should lift about 1–2 stops), check for floor hotspots (C), and that no double shadows appear.

## 6. Visual verification (frames viewed)
(gobo_10m05.jpg described earlier; not redone.)
- [00:35] Camera Lens panel at default **50 mm** being edited (transcript says set to 120 mm; the final value isn't in this frame).
- [03:45] Close-up of the cube corner with a sharp edge before the bevel (render preview); Area.015 selected — confirms the "too sharp" baseline of T5.
- [04:15] Product scene at the Add menu (empty black preview); outliner shows the archived per-scenario collections (Basic, Teaser, Ecommerce, Glass, Reflective, Sun) — tidy scene organisation.
- [04:25] Plane.002 placed horizontally through the bottle mid-height and rotated (−44° Z) — a card being positioned; preview shows key-lit bottle with soft floor falloff.
- [05:00] Basic product result: blue/white bottle, rim on the left edge, soft floor gradient; Light Linking panel for Area.017 with Floor4 being dragged in (T4 exclude-floor step seen).
- [06:00] E-commerce: peach bottle on a light-grey cyc, very soft wrap; specular light **Area.017 = 0.45 m, 10 W**.
- [07:35] (glassgrad_7m35.jpg) Glass dropper bottle: gradient area light Area.019 **10 W, Square 1 m**, rotated −14° behind the bottle; Emission node fed by an image; render shows smooth vertical highlight strips on the glass instead of a white rectangle.
- [08:20] Metal bottle: Area.020 **10 W, 1 m**, being scaled tall (Z 1.12+) into a strip; preview shows a thin vertical highlight on black metal.
- [09:15] Sun scenario: Sun **Strength 1.0, Angle 0.526°**, hard shadow of two yellow/white bottles on a cyan backdrop.
- [10:20] Presenter only (outro).
- Values not legible in my frames: key 25 W / back 5 W (transcript only, unchanged).
- Quality judgement: **clean, competent teaching renders** — correct light behaviour and good A/Bs, but untextured primitive bottles and flat backdrops; not portfolio-grade advertising. Good source for setups, not for final look.
