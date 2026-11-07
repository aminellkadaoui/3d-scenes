# 3D Scenes — turntable rig with constant drift + "mountain" speed graph.
# Paste into Blender MCP execute_blender_code. Edit CONFIG. Prints a deg/frame table.
import bpy, math

CONFIG = dict(
    spin_object="Table_Top",        # the part that spins (already separated)
    heroes=["Laptop_Group"],         # objects that ride on it (parents are enough)
    surface_z=None,                  # None = top of spin_object bbox
    drift_deg_per_frame=0.5,         # constant slow spin, never stops
    turn_deg=360,                    # extra turn inside the speed graph
    f_start=130, f_end=230,          # speed-graph segment; peak is in the middle
    handle_pct=0.75,                 # AE Speed In/Out 75%
)

C = CONFIG; sc = bpy.context.scene

def fcurves(obj):
    a = obj.animation_data.action
    return [fc for l in a.layers for s in l.strips for cb in s.channelbags for fc in cb.fcurves]

top = bpy.data.objects[C["spin_object"]]
if C["surface_z"] is None:
    from mathutils import Vector
    C["surface_z"] = max((top.matrix_world @ Vector(c)).z for c in top.bound_box)
col = top.users_collection[0]

drift = bpy.data.objects.get("Turntable_Drift") or bpy.data.objects.new("Turntable_Drift", None)
piv = bpy.data.objects.get("Turntable_Pivot") or bpy.data.objects.new("Turntable_Pivot", None)
for o in (drift, piv):
    if not o.users_collection: col.objects.link(o)
    o.empty_display_type = "CIRCLE"; o.empty_display_size = 0.25
drift.parent = None; drift.location = (0, 0, C["surface_z"]); drift.rotation_euler = (0, 0, 0)
bpy.context.view_layer.update()
piv.parent = drift; piv.matrix_parent_inverse.identity(); piv.location = (0, 0, 0); piv.rotation_euler = (0, 0, 0)
bpy.context.view_layer.update()
for name in [C["spin_object"]] + C["heroes"]:
    o = bpy.data.objects[name]; mw = o.matrix_world.copy()
    o.parent = piv; o.matrix_parent_inverse = piv.matrix_world.inverted(); o.matrix_world = mw

# layer 1: drift (linear + linear extrapolation)
drift.animation_data_clear()
for f in (0, 100):
    drift.rotation_euler[2] = math.radians(C["drift_deg_per_frame"] * f)
    drift.keyframe_insert("rotation_euler", index=2, frame=f)
dfc = fcurves(drift)[0]
for k in dfc.keyframe_points: k.interpolation = "LINEAR"
dfc.extrapolation = "LINEAR"; drift.rotation_euler[2] = 0

# layer 2: mountain speed graph
piv.animation_data_clear()
F0, F1 = C["f_start"], C["f_end"]
for f, d in ((F0, 0), (F1, C["turn_deg"])):
    piv.rotation_euler[2] = math.radians(d); piv.keyframe_insert("rotation_euler", index=2, frame=f)
pfc = fcurves(piv)[0]; k0, k1 = pfc.keyframe_points; L = C["handle_pct"] * (F1 - F0)
for k in (k0, k1): k.interpolation = "BEZIER"; k.handle_left_type = k.handle_right_type = "FREE"
k0.handle_right = (F0 + L, k0.co[1]); k0.handle_left = (F0 - 10, k0.co[1])
k1.handle_left = (F1 - L, k1.co[1]); k1.handle_right = (F1 + 10, k1.co[1]); pfc.update()

def total(f): return math.degrees(dfc.evaluate(f) + pfc.evaluate(f))
speeds = [(f, total(f) - total(f - 1)) for f in range(F0 + 1, F1 + 1)]
peak = max(speeds, key=lambda s: s[1])
print("peak frame (use as CUT):", peak[0], "deg/f %.2f" % peak[1])
print([(f, round(v, 2)) for f, v in speeds if f % 10 == 0])
