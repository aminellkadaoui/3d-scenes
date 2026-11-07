---
id: rendering-eevee-shadow-jitter-area-center
domain: rendering
status: Reproduced
sources: [own test 2026-11-07, VSL chair scene frame 129, EEVEE vs Cycles]
blender: "5.2"
---
# EEVEE large area lights: shadow is taken from the light CENTRE → enable Shadow Jitter
**Finding (measured):** without Shadow Jitter, EEVEE shadows an area light from its centre point. A 5.6 m ceiling fill whose centre sat inside the fan down-rod contributed **exactly 0** light; the window area light whose centre sat behind the blind slats gave ~42 % of its Cycles contribution. Light › Shadow › **Jitter ✔** (Overblur 10) fixed both (overall EEVEE/Cycles brightness 0.63 → 0.87, region error halved).

**Side effects and fixes:**
- Jitter adds grain at 64 samples (wall noise 1.81 Cycles → 2.41 EEVEE). Compositor **Denoise** node (OIDN, Image + Normal + Diffuse Color passes, HDR, Accurate) brings it to 1.85 at no visible cost; 128 samples alone only gave 2.14 and +70 % time.
- Jitter on a light whose **specular** hits a glossy floor sparkles (floor noise 4.9 vs 0.69), and the denoiser doesn't remove it. Fix: jittered copy with Specular 0 for the diffuse light + a non-jittered copy placed in front of the occluder with Diffuse 0, Specular 1, energy fitted (here 0.16×).
- EEVEE ignores area-light **Spread** (verified: 60° vs 180° identical).
- Emissive meshes don't light directly in EEVEE; EEVEE volume with density ≈0.012 is practically invisible.

**Method that worked:** solo renders per light group in both engines (linear EXR), then least-squares strengths + a few fitted compensation lights. Strength scaling alone can't fix distribution problems; fix the cause first (jitter), then fit.
**Result:** frame 129: Cycles 223 s → EEVEE 34 s, brightness 0.88, noise ≈ Cycles. Still differs: window frame/blind warm glow, ceiling round the fan, floor reflection size.
