# 3D Scenes — camera crane: starts low in front, rises slowly to the user's approved angle.
# Step 1: user frames the END angle in the camera. Step 2: run this; it reads that pose and builds the rig.
import bpy, math
from mathutils import Vector

CONFIG = dict(camera="CAM_Shot", hero_axis_xy=(0.0, 0.0), start_elev_deg=10.0,
              f_start=100, f_end=259)
C = CONFIG; sc = bpy.context.scene; cam = bpy.data.objects[C["camera"]]
cam.animation_data_clear(); cam.parent = None
p = cam.matrix_world.translation.copy(); fwd = cam.matrix_world.to_3x3() @ Vector((0, 0, -1))
ax = Vector((*C["hero_axis_xy"], 0))
t = min((i * 0.005 for i in range(1, 2000)), key=lambda t: ((p + fwd * t) - ax).xy.length)
aim = p + fwd * t; D = (p - aim).length
az = math.degrees(math.atan2(p.y - aim.y, p.x - aim.x)) - 90
end_el = math.degrees(math.asin((p.z - aim.z) / D))
print("aim", tuple(round(x, 3) for x in aim), "dist %.3f az %.1f end elevation %.1f" % (D, az, end_el))

rig = bpy.data.objects.get("CAM_Rig") or bpy.data.objects.new("CAM_Rig", None)
if not rig.users_collection: sc.collection.objects.link(rig)
rig.empty_display_type = "SPHERE"; rig.empty_display_size = 0.05
rig.animation_data_clear(); rig.location = aim; rig.rotation_euler = (math.radians(-end_el), 0, math.radians(az))
bpy.context.view_layer.update()
cam.parent = rig; cam.matrix_parent_inverse.identity(); cam.location = (0, -D, 0); cam.rotation_euler = (math.radians(90), 0, 0)
for f, el in ((C["f_start"], C["start_elev_deg"]), (C["f_end"], end_el)):
    rig.rotation_euler[0] = math.radians(-el); rig.keyframe_insert("rotation_euler", index=0, frame=f)
a = rig.animation_data.action
fc = [fc for l in a.layers for s in l.strips for cb in s.channelbags for fc in cb.fcurves][0]
k0, k1 = fc.keyframe_points; seg = k1.co[0] - k0.co[0]; avg = (k1.co[1] - k0.co[1]) / seg; h = seg / 3; s = avg * 0.5
for k in (k0, k1): k.interpolation = "BEZIER"; k.handle_left_type = k.handle_right_type = "FREE"
k0.handle_right = (k0.co[0] + h, k0.co[1] + s * h); k0.handle_left = (k0.co[0] - h, k0.co[1] - s * h)
k1.handle_left = (k1.co[0] - h, k1.co[1] - s * h); k1.handle_right = (k1.co[0] + h, k1.co[1] + s * h)
fc.extrapolation = "LINEAR"; fc.update()
sc.frame_set(C["f_end"]); print("end camera", tuple(round(x, 3) for x in cam.matrix_world.translation), "(should equal the approved pose)")
