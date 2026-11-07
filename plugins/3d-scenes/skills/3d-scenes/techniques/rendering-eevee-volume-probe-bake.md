---
id: rendering-eevee-volume-probe-bake
domain: rendering
status: Extracted
sources: [eevee_full_course@29:20, eevee_full_course@36:00, eevee_full_course@40:20, eevee_full_course@42:40, eevee_full_course@43:40, eevee_full_course@51:00]
blender: "5.2"
---
# EEVEE Volume probe bake (interior bounce, world-light leak, sun threshold)
**Principle:** A Volume light probe stores baked irradiance on a 3D grid. It gives off-screen bounce light and, importantly, **blocks world/HDRI light inside closed rooms** — without it EEVEE world lighting ignores walls and floods interiors [eevee_full_course@36:00].

**Steps / settings (starting points):**
1. Add › Light Probe › **Volume**; scale to the room so the outer grid points sit **just inside** the walls (check in ortho views) [eevee_full_course@32:00].
2. Bake › Resolution X/Y/Z ≈ **cubic cells** (room 3×7×2 → 8×19×5 shown) [eevee_full_course@42:40]. Bake Samples 2048. **Surfel Resolution 20 → ~100** (sharper, less leaking bounce) [eevee_full_course@42:40].
3. Capture: Distance 20 m; World ☐ / Indirect Light ✔ / Emission ✔ (as shown) [eevee_full_course@40:20]. Offset: **Surface Offset** 0.05 (raise toward ~0.3 if banding/stripes), **Search Distance** small (0.1) [eevee_full_course@40:20].
4. Probe bias: Normal Bias 0.3, View Bias 0, Facing Bias 0.5, Validity 0.4, Dilation 0.5 (shown) [eevee_full_course@43:40]; adjust Normal/View bias if light bleeds under objects (transcript).
5. **Hide fog volumes and fake/opaque window glass before baking** (collection "hide before baking") [eevee_full_course@65:20], then Bake Light Cache. Re-bake after moving lights or walls.
6. World sun: World › Settings › Sun › **Threshold** extracts the HDRI sun as a shadow-casting light (Angle 0.526° shown) [eevee_full_course@51:00]. Author prefers **Threshold 0 + a real Sun lamp** (direction/softness/colour under control) [eevee_full_course@52:00].

**Use when:** every EEVEE interior; any room with a world/HDRI outside.
**Avoid when:** objects/lights animate strongly through the room (bake is static — bounce won't follow; rely on Fast GI then).
**Failure signs:** blue/HDRI tint in closed rooms; dark/light stripes on walls (raise Surface Offset); light leaking under furniture (bias); bounce from a now-moved lamp (stale bake).
**Cost:** bake seconds–minutes; render cost tiny (0.93 s/frame simple room shown [eevee_full_course@43:40]).
**Conflicts with other sources:** `knowledge/lighting.md` §5 #7 suggests "Use EEVEE Sun Threshold extraction instead of a mismatched Sun". This source prefers Threshold 0 + Sun lamp. Resolution: Sun lamp when you need control/animation or light linking; Threshold when the HDRI sun direction must match the background exactly.
**Test to validate:** closed room with HDRI outside: no probe vs probe (world tint inside); Surfel 20 vs 100 (corner leak, bake time).
**Log:** 2026-11-06 — Extracted from eevee_full_course (Blender 4.4).
