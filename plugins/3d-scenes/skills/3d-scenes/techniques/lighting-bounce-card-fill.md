---
id: lighting-bounce-card-fill
domain: lighting
status: Extracted
sources: [ZYk3OOf-gBk@01:30, ZYk3OOf-gBk@04:15, KgqyWeF09wE@01:30, KgqyWeF09wE@06:00, a-IdD-RGb4Q@01:15]
blender: "5.2"
---
# Fill with an invisible bounce card instead of a second light
**Principle:** A white card reflects the key back into the shadow side. Fill brightness is tied to the key (ratio stays constant when you change the key), the fill colour matches the key, and there is no second cast shadow, so the shadow keeps its direction and depth cue [a-IdD-RGb4Q@01:15]. Same as a photographer's reflector.

**Steps / settings (starting points):**
1. Plane opposite the key, facing the subject. Size about 1–2× subject height, distance about 0.5–1× subject height [ZYk3OOf-gBk@01:30].
2. Material: Principled BSDF, Base Color white with about 0.8 albedo (sRGB ~0.9), Roughness 1.
3. Object Properties > Visibility > Ray Visibility: Camera OFF, Shadow OFF (so it doesn't block key/world) [ZYk3OOf-gBk@01:45]. Keep Glossy on if you want it in reflections (extra edge highlight), off otherwise.
4. A/B by toggling the render visibility: the shadow side should lift about 1–2 stops [ZYk3OOf-gBk@01:45].
5. If it creates a line/terminator on the floor, raise it or link it away [ZYk3OOf-gBk@02:00].
6. Not enough? Bigger or closer card first. Ducky's hack: Base Color Value 2 (up to 20) [KgqyWeF09wE@06:15] is non-physical (albedo > 1 creates energy). Use only as a last resort and check for fireflies. An alternative is a low emission strength (0.5–2) on the card.

**Use when:** key-dominant setups (products, portraits, interiors with one window). The scene looks contrasty but shadows are dead.
**Avoid when:** you want a fill with a different temperature (use a large dim area light, Temperature set, Cast Shadow off in Cycles, or a separate light with soft shadows). In EEVEE the bounce depends on ray tracing/probes. Enable Render > Raytracing (and screen-tracing fallback/probes) or the card does little (test).
**Failure signs:** shadow side still about 0 (card too small or missed the key). A visible white rectangle in glossy reflections. A pasted-on bright line on the floor. Noise/fireflies when using albedo > 1.
**Cost:** Cycles needs at least 2 diffuse bounces (default 4). Small extra noise.
**Conflicts with other sources:** none. All sources agree a bounce beats a second shadow-casting light. Ducky's albedo > 1 hack conflicts with physical plausibility. Resolve: increase size before albedo.
**Test to validate:** sphere + key 25 W. A: key only. B: + card. C: + card albedo 5. Shadow-side luminance and noise at 128 samples.
**Log:** 2026-11-05 — Extracted from ZYk3OOf-gBk, KgqyWeF09wE, a-IdD-RGb4Q.
