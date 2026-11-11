---
id: environment-endless-floor-void
domain: environment
status: Proven
sources: [laptop-to-money v2 session 2026-11-11]
blender: "5.2"
---
# Endless floor in a black void (no visible horizon edge)

**Problem:** A product on a floor in a black space. When the camera drops low, the top of the frame sees past the floor's edge: in Material Preview a band of Blender's built-in HDRI (green trees), in the render a faint line where the floor's sheen stops. Making the plane bigger never fully fixes it.

**Decisions the user approved:**
1. **Bigger plane is not enough** — scale it (40 m → 200 m) but the real fix is a fade. Texture mapped on world/object position is unaffected by the scale; UV-mapped textures need the UVs scaled too.
2. **Fade the floor into the camera backdrop** inside the floor material: Mix Shader (floor ↔ Emission with the exact backdrop colour the world shows camera rays). Fac = MAX of two fades:
   - **angle fade:** Geometry ▸ Incoming ▸ Z → Map Range smoothstep 0.30 → 0.02 (fades near the horizon smoothly in screen space; distance alone compresses into a few pixels → line),
   - **radial fade:** Geometry ▸ Position ▸ Length → Map Range smoothstep 1.5 m → 8 m around the hero (no edge even when the camera is high and looks down).
3. **Check pixel values**, not the eye: across the horizon the floor must not dip below the backdrop (a 2/255 darker band still reads as a line after grading).
4. **Light on the floor = very diffused, soft, fades fast into black.** Wide spot (cone 140°, blend 1) + a large area light; about 25 % less than first tried. "Strong light" was rejected. The user wants a lot of fade, no visible pool edge.
5. **Glossy floor must not reflect big area lights as hard rectangles** — set Specular 0 on floor fill lights (diffuse only).
6. **Surface feel = like the hero's lacquered table top, not a mirror.** A mirror (roughness 0.005–0.04) in a black void reflects black and looks dead. Roughness ≈ the hero top's (≈0.36–0.48, coat 0.30–0.40) spreads the light into a soft sheen. Keep the original texture — the user asked for "feel", not a new material.

**Viewport note:** Material Preview shows Blender's own HDRI unless "Scene World" is on — judge the void in Rendered view.

**Avoid:** swapping the texture (e.g. marble) when the user asks for a reflective "feel"; adding strong or new-looking lights; area-light rectangles in glossy floors.
**Log:** 2026-11-11 — laptop-to-money v2. Marble swap and a strong round spot were tried and rejected; final = original texture, higher roughness, soft fills, double fade.
