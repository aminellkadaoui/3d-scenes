---
id: compositing-view-layers-holdout-indirect
domain: compositing
status: Extracted
sources: [vtdczoXVyvQ@09:15, vtdczoXVyvQ@10:45, vtdczoXVyvQ@12:45, vtdczoXVyvQ@16:30, vtdczoXVyvQ@17:30, vtdczoXVyvQ@17:45]
blender: "5.2"
---
# Element view layers with Indirect Only + Holdout, recombined by Alpha Over

**Principle:** separate elements (background, subject, fog, dust, text-safe overlays) into view layers. Each must still *receive* shadows and bounce from the others (**Indirect Only**) and be *occluded* by them (**Holdout**). Recombined back to front, the result matches a single render but each layer can be re-rendered or graded on its own.

**Steps / settings:**
1. Sort objects into collections per element.
2. View layer "everything" (work layer): Use for Rendering ✗ [10:45].
3. New view layer per element (copy settings from the previous one). Exclude the other collections.
4. Outliner › Filter › Restriction toggles: show **Indirect Only** and **Holdout** [12:45], [16:30].
   - Collections that affect lighting (cast shadows/bounce) but belong to another layer → Indirect Only (Cycles only).
   - Collections that are in front of parts of this element → Holdout. Rule: elements that are both in front of and behind others need holdouts [17:30].
5. Compositor: Render Layers node per view layer → **Alpha Over** back to front (5.0: inputs Background/Foreground) [14:45].
6. Fix one element: View Layer › "Render Single Layer" → F12 [17:45].
7. For editors: output each layer as its own EXR/PNG-RGBA sequence (File Output), so Premiere/AE can stack them.

**Use when:** a separate fog/dust/glow layer, product + background for VSL compositing (swappable backgrounds, text behind product), heavy scenes that crash.
**Avoid when:** EEVEE (no Indirect Only; holdout yes); simple single-element shots; motion-blurred or DOF edges (alpha-over of premultiplied DOF edges gives halos; prefer holdout-based layers and render DOF in 3D consistently).

**Failure signs:** dark fringes/halos at edges (premultiplied vs straight alpha mismatch); missing contact shadows on the ground layer (forgot Indirect Only); objects visible through others (forgot Holdout); black ground-intersection areas visible [15:30]–[16:30].

**Cost:** total render time ≈ sum of layers (often more than a single pass); big gain when iterating one element.

**Conflicts with other sources:** none.

**Test to validate:** a vehicle + dust + mountain scene. Single render vs 3-layer recombination difference. Expect < 1% except at semi-transparent edges.

**Log:** 2026-11-05 — Extracted from vtdczoXVyvQ.
