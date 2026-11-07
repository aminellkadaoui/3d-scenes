# 03 — Assets (Proven)

## Sources, in order
1. The user's own files (`.blend`, `.glb` they send). Copy into `<project>/blend/models/` before importing.
2. Poly Haven via MCP (`search_assets` → `import_asset`). Enable first if off: `scene.blendermcp_use_polyhaven = True`. CC0. Great for furniture, floors, stone; **its metal textures are mostly rusty** (not for clean polished metal).
3. Sketchfab via MCP needs the user's API key in the addon. If missing, say so and ask the user for a file instead.
4. Never build hero/support props from primitives. Simple emissive cards / LED strips are lights, not props — allowed.

## Import discipline
- Size from the bounding box to real dimensions (banknote bundle 15.6 × 6.6 × ~1.75 cm; MacBook 16" ≈ 35.5 × 24.8 cm; side table top ≈ 33–37 cm Ø). Imported GLB from Sketchfab can arrive ×100.
- Snap to the support surface by **vertex min-Z**, not bbox (a laptop sat 7.7 mm inside the table; bbox said it was fine).
- Containment: for objects on a round top, check the max horizontal distance of every bbox corner from the centre < radius.
- Multi-part models: parent to a `<Hero>_Group` empty at the base centre and scale the empty (shrink 20% = 0.8) instead of scaling parts.

## Splitting a model
To spin only a tabletop, or remove a shelf: find mesh **islands** (bmesh flood fill over linked faces), list each island's z-range and radius, separate by island or by `all verts z > threshold`. If there are zero boundary edges between the selection and the rest, it's a clean separate part. Copy UVs and material indices when rebuilding the mesh. Put the origin at the part's centre-bottom.

## Duplicates that don't look duplicated
- **Linked duplicates** (`bpy.data.objects.new(name, src.data)`) — light on memory.
- Jitter each copy: rotation 1–5°, position a few mm; at least one leaning/crossed piece. Mirror a leaning piece for the other side, then add +4° and 8 mm offset so it isn't a mirror image.
- Keep the source hidden (`hide_render`, `hide_viewport`).
- Stack heights by real thickness (bundle H = 1.75 cm) + 0.2–0.3 mm gap.
