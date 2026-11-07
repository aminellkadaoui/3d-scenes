# BLENDER DAY/NIGHT CYCLE IN UNDER 2 MIN (Physical Addons)
- url: https://youtu.be/CPZtbXTVdWs
- channel / duration / Blender version shown: Mārtiņš Upītis & The Physical Addons Crew / 1:34 / not stated (uploaded 2025-07-13, so Blender 4.4–4.5; "Get Extensions" UI)
- domain(s): lighting | environment | animation
- evidence used: transcript + yt-dlp metadata + contact sheet 01 + 5 extracted frames from the 480p mp4 (see §6).
- trust: medium-low for general lighting knowledge. It is an addon promo (Physical Starlight & Atmosphere, a paid addon) whose core is "keyframe the time". Technically correct for what it shows. The author (Mārtiņš Upītis) is a respected atmosphere/shader developer.

## 1. Problem it solves
Animating a believable sun path and sky over 24 h without hand-animating the sun rotation, sky colour and night sky.

## 2. Techniques

### T1: Physically driven sun via Sun Position extension  `[00:00]`–`[00:45]`
- What: In the Physical Starlight & Atmosphere (PSA) N-panel > Atmosphere > Add [00:00]. Edit > Preferences > Get Extensions, install "Sun Position" [00:15]. World Properties > Sun Position panel: Sun Object = your Sun light. Set Latitude/Longitude to a real place (the captions say "RAM, the city we are based out of", Riga — confirmed from frames [00:50]: Lat 56.968, Lon 24.106; note UTC Zone left at 0) [00:30].
- Why: real sun elevation and azimuth for a location, date and time give believable shadow length and direction. A motivated, consistent sun is the backbone of an exterior lighting look.
- Use when: exteriors, architecture, timelapses, anything that must match a real time of day. Don't use when: stylised studio work.
- Blender 5.2: Sun Position is an extension (extensions.blender.org), not a bundled addon. It can also sync the Sky Texture's sun direction. Blender 5.0's new Multiple Scattering sky "can generate a sunset by animating a single parameter" (sun elevation), a free native alternative to PSA for most needs.
- Status: Extracted

### T2: Keyframe time 0 → 24 and set LINEAR interpolation  `[00:45]`–`[01:15]`
- What: Frame 1: Time = 0, press I to key it. Last frame: Time = 24 and key it [00:45]. Graph Editor: A (select all) > right-click > Interpolation > Linear, so the sun moves at constant speed. The default Bezier easing "speeds up and slows down, which is not really realistic" [01:00]–[01:15].
- Why: real celestial motion is uniform. Ease-in/out on a time channel makes dawn and dusk linger or rush, so viewers sense something wrong in timelapses.
- Status: Extracted

### T3: PSA's own sun properties as an alternative  `[01:15]`
- The same can be done inside PSA, "more realistic" per the author (a promotional claim).

## 3. Claims I doubt or must test
- "More realistic result" with PSA [01:15]: unverified marketing claim. Compare against Blender 5.x's native Multiple Scattering Sky + Sun Position.
- No mention of exposure. A 24 h cycle spans about 20 stops (noon sun vs moonlight). Without animated exposure, night will be pure black or day will clip. That is the real hard part of a day/night cycle.

## 4. Anti-AI-slop lessons
- Exterior light must be motivated by a real sun position. Shadow direction and length should match the time of day you claim (long and warm at golden hour, short and white at noon).
- Animated lighting needs exposure adaptation (like a camera's auto-exposure) or night reads as "broken render".

## 5. Candidate isolated test
Native 5.2: Sky Texture (Multiple Scattering) + Sun light synced with Sun Position, animate 6:00 → 20:00 over 300 frames, linear. Also animate Film/Color Management Exposure. Check that shadow direction is continuous, sky colour transitions are smooth, there is no pure-black frame, and the noon sun doesn't clip.

## 6. Visual verification (frames viewed)
Frames viewed: contact sheet 01, plus extracted frames below. Status-bar version digits are barely legible at 480p (appears to be 4.x, possibly 4.3.0 — low confidence).
- [00:05] PSA sky with volumetric-looking clouds over a flat brown ground plane; PSA ▸ Sun panel: **Angular Diameter 0.526°, Temperature 5700 K, Intensity ≈200000 (PSA units)**, Sun Disk + Sun Lamp on.
- [00:35] Sun Position panel: Usage Mode **Sun Object** = "Starlight Sun", Use Refraction on, Distance 50 m, Time 12.0 default; PSA panel lists presets and sections (Sun, Atmosphere, Stars, Clouds, Object Fog, Ground, Artistic Controls).
- [00:50] **Confirms T1/T2:** Latitude **56.968**, Longitude **24.106** → **Riga** (inference confirmed), Date 1 May 2025, Time keyed (green field) at 0.0 on the last-frame side of the animation; **UTC Zone 0.0, Daylight Savings off** → the panel shows Sunrise 02:35 / Sunset 18:07, i.e. times in UTC, not Riga local time (UTC+3 in May). (added from frames) For a real location, set the UTC zone, otherwise "time of day" labels are off by hours (sun geometry itself stays correct for the UTC time).
- [01:10] Night end of the cycle: viewport near-black with the grid — consistent with my doubt that no exposure adaptation is shown.
- [01:25] Graph Editor: the Time F-curve from frame 0 to 250 is shown with straight (linear) segments; Time 13.69 at frame 144 — confirms T2 linear interpolation.
- Final quality judgement: sky/cloud rendering from PSA looks physically pleasant; there is no scene, so no production result to judge. A tool demo, not a lighting lesson. Trust unchanged.
