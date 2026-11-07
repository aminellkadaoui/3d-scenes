---
id: composition-lead-room-overlay-space
domain: composition
status: Extracted
sources: [HBWYieo5RmU@01:15, HBWYieo5RmU@01:30, HBWYieo5RmU@00:30, HBWYieo5RmU@05:45]
blender: "5.2"
---
# Lead room + negative space reserved for VSL text and captions

**Principle:** Leave space in the direction the subject faces or moves (rule of space) [HBWYieo5RmU@01:30]; negative space creates scale/isolation [HBWYieo5RmU@01:15]. In VSL/marketing work that negative space is also the planned home of headlines, numbers, captions and lower thirds, so composition must be designed *with* the overlay, not fixed in the edit.

**Steps / settings (starting points):**
1. Ask the editor's overlay plan per shot: title side, caption band (usually lower third; for 9:16 the bottom ~20–25 % and right edge are covered by platform UI).
2. Camera Properties ▸ Viewport Display ▸ Composition Guides: Thirds; and the Safe Areas sub-panel (Title Safe / Action Safe margins are editable there and stored per scene in `scene.safe_areas`). Set Title Safe to match the editor's caption margins.
3. 16:9 with title: subject on one third (e.g. right third, facing left/into frame), title in the opposite 40 %. Lead room in front of a moving/facing subject ≈ ⅔ of frame width ahead of it.
4. 9:16: subject in the upper-middle (between 25 % and 65 % height), keep bottom 20 % and right 15 % clear of essential detail.
5. Keep the negative space quiet: low detail, low contrast, consistent value (text needs a stable backdrop — test white and dark text on it).
6. During camera moves, the empty space must stay empty through the whole move (check first/mid/last frame).

**Use when:** any VSL/ad shot that will receive text; any directional subject.
**Avoid when:** deliberate tension (subject pushed against frame edge it faces — "violated rule of space" [HBWYieo5RmU@05:45]) for unease beats.

**Failure signs:** subject centered with text forced on top of it; subject facing/moving out of frame with space behind it (unless intentional); busy/high-contrast texture behind titles; caption band covering product; 9:16 crop of a 16:9 render loses the subject.
**Cost:** none; may require separate 9:16 camera instead of cropping.
**Conflicts with other sources:** none.
**Test to validate:** composite a dummy title + caption plate over render (compositor Alpha Over or in the editor); check legibility and that subject is unobstructed in all frames.
**Log:** 2026-11-05 — Extracted from HBWYieo5RmU + VSL production practice.
