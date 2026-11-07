# 3D Scenes — list mesh islands and split one off (e.g. a tabletop to spin, a shelf to remove).
import bpy, bmesh, math

OBJ = "Table_Base"; MODE = "list"          # "list" | "split_z_above" | "split_z_between"
Z_MIN, Z_MAX = 0.735, 99.0; NEW_NAME = "Table_Top"; HIDE_INTO = None   # e.g. "_HIDDEN_removed"

o = bpy.data.objects[OBJ]; me = o.data; bm = bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
if MODE == "list":
    seen = set()
    for f in bm.faces:
        if f.index in seen: continue
        st, isl = [f], []; seen.add(f.index)
        while st:
            x = st.pop(); isl.append(x)
            for e in x.edges:
                for g in e.link_faces:
                    if g.index not in seen: seen.add(g.index); st.append(g)
        vs = {v for ff in isl for v in ff.verts}
        print("island faces %4d  z %.3f..%.3f  r %.3f" % (len(isl), min(v.co.z for v in vs), max(v.co.z for v in vs), max(math.hypot(v.co.x, v.co.y) for v in vs)))
    bm.free()
else:
    sel = [f for f in bm.faces if all(Z_MIN < v.co.z < Z_MAX for v in f.verts)]
    nm = bpy.data.meshes.new(NEW_NAME); b2 = bmesh.new(); vmap = {}
    us = bm.loops.layers.uv.active; ud = b2.loops.layers.uv.new("UVMap") if us else None
    for f in sel:
        for v in f.verts:
            if v not in vmap: vmap[v] = b2.verts.new(v.co)
    for f in sel:
        nf = b2.faces.new([vmap[v] for v in f.verts]); nf.smooth = f.smooth; nf.material_index = f.material_index
        if us:
            for a, c in zip(f.loops, nf.loops): c[ud].uv = a[us].uv
    b2.to_mesh(nm); b2.free(); bmesh.ops.delete(bm, geom=sel, context="FACES"); bm.to_mesh(me); bm.free()
    for m in me.materials: nm.materials.append(m)
    n = bpy.data.objects.new(NEW_NAME, nm); n.matrix_world = o.matrix_world.copy()
    (bpy.data.collections[HIDE_INTO] if HIDE_INTO else o.users_collection[0]).objects.link(n)
    print("split", len(sel), "faces ->", NEW_NAME)
