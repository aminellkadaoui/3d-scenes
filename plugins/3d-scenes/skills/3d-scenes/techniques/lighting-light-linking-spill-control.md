---
id: lighting-light-linking-spill-control
domain: lighting
status: Extracted
sources: [WreZ_VKDn4M@06:45, ZYk3OOf-gBk@02:15, ZYk3OOf-gBk@04:45, ZYk3OOf-gBk@05:15]
blender: "5.2"
---
# Light linking to stop rim/back lights spilling onto floors
**Principle:** Each light should do one job. Rim and back lights placed behind the subject also hit the floor and reflect off glossy floors, creating hotspots that compete with the subject [WreZ_VKDn4M@06:45]. Light linking is a digital flag. It restricts which objects receive a light.

**Steps / settings (starting points):**
1. Select the light > Object Properties > Shading > Light Linking > Receiver Collection > New [ZYk3OOf-gBk@02:15].
2. Either drag in the subject only (include list) [WreZ_VKDn4M@06:45], or drag in the Floor and untick its check mark to exclude it [ZYk3OOf-gBk@02:30].
3. Shadow Linking (Blocker Collection) controls which objects cast shadows from this light (useful for removing an ugly shadow from a single prop).
4. Repeat per light. Keep the KEY light (and world) affecting the floor so contact shadows and bounce remain.
5. Rim power start: about 1/5 of key at similar distance (key 25 W, rim 5 W) [ZYk3OOf-gBk@04:15][ZYk3OOf-gBk@05:00].

**Use when:** product shots on glossy floors or cycloramas, teaser backlight setups [ZYk3OOf-gBk@05:15], character rims spilling onto sets.
**Avoid when:** realism depends on consistent illumination (an exterior sun must light everything). Linking the key off the floor makes the object float.
**Failure signs:** the product looks pasted on (bright product, floor unlit, no contact shadow). Reflection of the product on the floor shows a rim that isn't lighting the floor (usually fine). Rim visible on the subject but its expected bounce absent.
**Cost:** none (Cycles). EEVEE supports light linking. Emissive meshes support linking in Cycles only (manual 5.2). Verify shadow linking in EEVEE before relying on it.
**Conflicts with other sources:** WreZ links all lights to the product only [07:00]. ZYk3 excludes only the floor from rim lights. Resolution: exclude the floor from rims and backlights only, never from the key.
**Test to validate:** product on a glossy floor. A: rim unlinked. B: rim excludes floor. Measure floor hotspot luminance and confirm the contact shadow is unchanged.
**Log:** 2026-11-05 — Extracted from WreZ_VKDn4M, ZYk3OOf-gBk.
