# 3D Scenes — object match cut: A disappears, B appears on CUT (CONSTANT keys).
# Includes all mesh descendants. Re-run safely: it clears previous hide keys.
import bpy

CONFIG = dict(
    cut=180,
    a_roots=["Laptop_Group"],        # visible before the cut
    b_roots=["Money_SLOT"],          # visible from the cut (children included)
    shift_existing_from=None,        # e.g. 150 -> move old cut keys (149/150) to the new cut
)
C = CONFIG

def tree(name):
    o = bpy.data.objects[name]
    return [o] + list(o.children_recursive)

def clear_hide_keys(o):
    ad = o.animation_data
    if not (ad and ad.action): return
    for l in ad.action.layers:
        for s in l.strips:
            for cb in s.channelbags:
                for fc in [fc for fc in cb.fcurves if fc.data_path.startswith("hide_")]:
                    cb.fcurves.remove(fc)

def key(o, hidden_before, cut):
    for f, h in ((cut - 1, hidden_before), (cut, not hidden_before)):
        o.hide_render = h; o.hide_viewport = h
        o.keyframe_insert("hide_render", frame=f); o.keyframe_insert("hide_viewport", frame=f)
    for l in o.animation_data.action.layers:
        for s in l.strips:
            for cb in s.channelbags:
                for fc in cb.fcurves:
                    if fc.data_path.startswith("hide_"):
                        for k in fc.keyframe_points: k.interpolation = "CONSTANT"

n = 0
for roots, hidden_before in ((C["a_roots"], False), (C["b_roots"], True)):
    for r in roots:
        for o in tree(r):
            if o.type not in {"MESH", "CURVE", "FONT"}: continue
            clear_hide_keys(o); key(o, hidden_before, C["cut"]); n += 1
sc = bpy.context.scene
m = sc.timeline_markers.get("CUT") or sc.timeline_markers.new("CUT", frame=C["cut"]); m.frame = C["cut"]
print("keyed objects:", n, "| cut at", C["cut"])
