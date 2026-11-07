---
id: rendering-eevee-reflection-probes
domain: rendering
status: Extracted
sources: [eevee_full_course@14:40, eevee_full_course@17:20, eevee_full_course@19:00, eevee_full_course@55:40, eevee_full_course@75:00]
blender: "5.2"
---
# EEVEE Plane and Sphere light probes (reflections that don't depend on the screen)
**Principle:** Screen-space reflections only contain what is on screen. A Plane probe re-renders the scene mirrored about a flat surface; a Sphere probe captures a cube map around a point. Both give off-screen reflections, at a render cost per probe.

**Steps / settings (starting points):**
1. **Plane probe** (Add › Light Probe › Plane) for floors, mirrors, glossy tabletops. Place it *exactly* on the surface, scale to cover it; toggle Viewport Display › **Capture** to check alignment [eevee_full_course@15:20]. Shown: Distance 0.1 m, Clipping Offset 0.001 m [eevee_full_course@17:20].
2. **Sphere probe** for chrome, glass, round mirrors: centre it on the object, Radius just enclosing it (0.43 m shown), Falloff 0.2, **Clipping Start larger than the object's own radius** (0.19 m shown) so it doesn't capture its own inside [eevee_full_course@55:40].
3. Probes can't reflect other probes (transcript). Scene › Light Probes › **Spheres Resolution** 1024 px (2048 for hero reflections) [eevee_full_course@75:00].
4. Delete plane probes the camera doesn't need; each one re-renders the scene (transcript, performance section).

**Use when:** glossy floors/desks seen at grazing angles; mirrors; chrome/glass hero props.
**Avoid when:** rough surfaces (Fast GI/volume probe is enough); many small glossy props (use one sphere probe for the area).
**Failure signs:** reflections that ghost/pop while panning; a chrome object reflecting itself as a blob (clip start too small); plane-probe reflection offset from the surface.
**Cost:** each plane probe ≈ one extra scene render; sphere probes are baked/updated, cheaper per frame.
**Conflicts with other sources:** none. Plane probes don't work on "Blended" render-method materials — see `materials-eevee-archviz-glass`.
**Test to validate:** glossy floor + object leaving frame; with/without plane probe; time per frame.
**Log:** 2026-11-06 — Extracted from eevee_full_course (Blender 4.4).
