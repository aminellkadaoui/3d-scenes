---
id: lighting-key-off-axis-rembrandt
domain: lighting
status: Extracted   # Extracted | Reproduced | Validated | Production-ready
sources: [hQKJx1wXkfM@00:00, hQKJx1wXkfM@00:15, WreZ_VKDn4M@02:45, ZYk3OOf-gBk@01:00, KgqyWeF09wE@00:45, a-IdD-RGb4Q@01:15, skool-rr-cinematic-composition@10:53, skool-rr-cinematic-composition@11:56]
blender: "5.2"
---
# Off-axis key light, orbited around the subject (Rembrandt start)
**Principle:** Form is revealed by the gradient from lit to shadow side. Light on the camera axis removes that gradient (flat). One dominant key at about 30–60° horizontally off the camera axis and 20–45° above the subject gives a clear terminator, a cast shadow that anchors the object, and a single readable direction [hQKJx1wXkfM@00:15][KgqyWeF09wE@00:45].

**Steps / settings (starting points):**
1. Lock the camera first (highlights are view-dependent) [WreZ_VKDn4M@02:15].
2. World strength 0 while building the key, so you only see your light [hQKJx1wXkfM@00:15][a-IdD-RGb4Q@14:30].
3. 3D cursor to the subject (Shift+S > Cursor to Selected/Active), Pivot Point = 3D Cursor. Select the light, R R to orbit it [hQKJx1wXkfM@00:00][WreZ_VKDn4M@03:00]. Alternative: Track To constraint → Empty at the subject.
4. Area light, Rectangle. Size about 0.5–1× subject height for soft-but-shaped light (character 1.8 m: 1–1.5 m area at 2–3 m, 300–800 W). Product 30 cm: 0.4–0.6 m area at 0.6–1 m, 30–100 W. Example from source: product key 25 W [ZYk3OOf-gBk@04:15] (scale not stated).
5. Rotate until (faces) a small triangle of light appears on the shadow-side cheek (Rembrandt) [hQKJx1wXkfM@00:15]. (Products) the top/side planes show different values.
6. Temperature: neutral 5000–5600 K for studio, or the motivated source's temperature.

**Use when:** almost every subject. It is the first light placed.
**Avoid when:** a beauty/clamshell look (cosmetics) or flat graphic styles are intended. Even then, add a subtle under-fill rather than a camera-axis key.
**Failure signs (how QA detects it went wrong):** both sides of the subject within about 0.5 stop of each other (flat). Cast shadow hidden directly behind the object (key on axis). Two or more shadow directions of similar strength. Specular hotspot centred on the object facing the camera.
**Cost:** zero render cost.
**Conflicts with other sources:** ZYk3OOf-gBk puts the key "in front then tilted" [01:15], which still means front-side, not on axis. Ducky prefers a big HDRI window as key [KgqyWeF09wE@01:15]. Same principle, different emitter.
**Test to validate:** Suzanne, grey 0.5 albedo, camera 85 mm. Key at 0°, 45°, 90°. Measure lit/shadow cheek ratio and judge shape readability in a clay render (View Layer > Material Override).
**Log:** 2026-11-05 — Extracted from hQKJx1wXkfM, WreZ_VKDn4M, ZYk3OOf-gBk, KgqyWeF09wE, a-IdD-RGb4Q.
**Log:** 2026-11-07 — skool-rr-cinematic-composition: key at an angle, never straight above/below [10:53]; "cheat code" for realistic rooms = replace flat white overhead light with an angled motivated source (corner lamp, sunset, window) [11:56–12:56].
