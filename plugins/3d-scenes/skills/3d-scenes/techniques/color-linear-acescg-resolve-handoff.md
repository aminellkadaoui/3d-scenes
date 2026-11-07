---
id: color-linear-acescg-resolve-handoff
domain: color
status: Extracted
sources: [vtdczoXVyvQ@19:00, vtdczoXVyvQ@20:00, vtdczoXVyvQ@22:45, vtdczoXVyvQ@29:15, vtdczoXVyvQ@30:45]
blender: "5.2"
---
# Linear (ACEScg) EXR → OCIO transform in DaVinci Resolve

**Principle:** compositing math is only correct on linear light. If you export linear and apply the *same* OCIO view transform (e.g. AgX) at the end in Resolve, you get the Blender look back while keeping full latitude for comp and grade.

**Steps / settings:**
1. Blender: Output Properties › Output › Color Management: **Override**. For EXR choose the linear space (Linear Rec.709 = the default working space, or **ACEScg**) [vtdczoXVyvQ@19:30]. Since 5.0 you can also set the scene **Working Space** to ACEScg so everything is ACEScg end to end.
2. Expect the EXR to look dark and flat in a non-colour-managed viewer. That is correct [vtdczoXVyvQ@19:45].
3. Resolve › Fusion: MediaIn → (comp) → **OCIO ColorSpace** node. Config = Blender's `config.ocio` (macOS: `/Applications/Blender.app/Contents/Resources/5.2/datafiles/colormanagement/config.ocio`). Source = ACEScg (or Linear Rec.709), Output = the AgX display/view space you used in Blender (e.g. "AgX Base sRGB"; check names in 5.2's config) [vtdczoXVyvQ@20:00], [29:30].
4. Colour page: CST → DaVinci Wide Gamut/Intermediate, grade, CST → Rec.709 Gamma 2.4 for delivery [vtdczoXVyvQ@30:45]–[31:30].
5. Alternative without Fusion: Resolve Color Management (RCM/ACES) with the input transform set to ACEScg. Note: this gives the ACES look, not AgX.

**Use when:** the shot will be comped or graded with other footage, or you deliver to a colourist.
**Avoid when:** a single VSL editor in Premiere needs plug-and-play clips. Render baked AgX ProRes/PNG instead (see rendering-exr-handoff-formats).

**Failure signs:** image "looks absolutely horrible" after OCIO = double transform (a view LUT plus the OCIO node) [vtdczoXVyvQ@30:00]; colour mismatch between the Blender render window and Resolve = wrong source space or wrong config version; neon or clipped highlights = treated as Rec.709 display-referred instead of linear.

**Cost:** extra disk space, a heavier Resolve timeline, and you need to know the config.

**Conflicts with other sources:** none. Note: Blender 5.0 added ACES 1.3/2.0 view transforms built in, so an ACES pipeline no longer needs a custom config.

**Test to validate:** render a Macbeth/colour-checker scene. Compare the Blender AgX PNG with the Resolve OCIO-transformed EXR via a difference blend (expect ≈0).

**Log:** 2026-11-05 — Extracted from vtdczoXVyvQ + Blender 5.0 color management release notes.
