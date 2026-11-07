---
id: lighting-product-three-role-setup
domain: lighting
status: Extracted
sources: [WreZ_VKDn4M@01:45, WreZ_VKDn4M@02:30, WreZ_VKDn4M@03:15, WreZ_VKDn4M@03:30, ZYk3OOf-gBk@04:15, ZYk3OOf-gBk@05:30, ZYk3OOf-gBk@05:45, ZYk3OOf-gBk@08:45]
blender: "5.2"
---
# Product lighting with three distinct roles (rim/back, hard shaping side, soft fill)
**Principle:** Three lights that all do the same thing make flat slop. Give each one a distinct job and a distinct quality: (1) strong backlight for edge highlights, (2) a sharp (low-Spread) side light for crisp shadows and texture, (3) a broad (high-Spread) light on the opposite side to lift the main faces [WreZ_VKDn4M@01:45].

**Steps / settings (starting points)** (product about 30 cm, scene in metres, AgX, Exposure 0; source gave no watts except ZYk3):
1. Camera first. Long lens 85–120 mm for true proportions [ZYk3OOf-gBk@00:30].
2. Back/highlight: Area 1.0 × 0.3 m behind the product, about 150° from the camera axis, 0.6–1 m away, 80–200 W. "Don't increase it too much" [WreZ_VKDn4M@02:30]. Author's actual values (seen in frames, Blender 4.3.2, full-size keyboard): back light **Area Square 2.16 m, 100 W, Spread 180°** [WreZ_VKDn4M@02:55]; hard side **110 W, Spread 50°**, same 2.16 m size [WreZ_VKDn4M@03:45]; glass emissive planes Emission Strength **5.0** [WreZ_VKDn4M@07:05]. The 2.16 m size is much larger than our 1.0×0.3 m start — sharpness comes from Spread, not size.
3. Hard side: duplicate, orbit around the 3D cursor to the side opposite the product's facing [WreZ_VKDn4M@02:45]. Size 0.3 m, Spread 15–30° [WreZ_VKDn4M@03:15], 30–80 W.
4. Soft fill: duplicate, rotate 180° [WreZ_VKDn4M@03:30]. Size 0.8–1.2 m, Spread 180°, 10–30 W (fill:key about 1:3–1:4).
5. Link back/rim lights off the floor (see lighting-light-linking-spill-control).
6. Variants: teaser = backlights only, mirrored [ZYk3OOf-gBk@05:15]. E-commerce = big overhead softbox + tiny weak specular light + separate background light to white out a cyclorama [ZYk3OOf-gBk@05:45]–[06:45]. Flat-colour matte products = Sun (Angle 0.5–3°) + gobo [ZYk3OOf-gBk@08:45].
7. Glossy, glass or metal: swap plain lights for gradient strips (lighting-gradient-reflection-cards) [WreZ_VKDn4M@03:45].

**Use when:** hero product shots, packshots, VSL product reveals.
**Avoid when:** product placed in a realistic environment (then motivate from that environment's sources, e.g. window + bounce).
**Failure signs:** no bright edge separating the product from the background. Shadow side pure black or same value as the lit side. Multiple shadows of equal strength on the floor. Text/label blown out.
**Cost:** low. Spread < 180° in EEVEE: verify support/appearance.
**Conflicts with other sources:** WreZ's "sharp side light" vs ZYk3's "soft key + bounce card". Both valid. Choose hard side light for texture (fabric, keyboards, embossing), bounce-card fill for smooth premium cosmetics.
**Test to validate:** keyboard or embossed box. A: three identical lights. B: three-role setup. Compare edge separation and texture visibility in a clay override.
**Log:** 2026-11-05 — Extracted from WreZ_VKDn4M, ZYk3OOf-gBk.
