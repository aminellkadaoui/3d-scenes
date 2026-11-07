# 3D Scenes — "this light doesn't work": aim error, effective power, receivers, duplicates.
import bpy, math
from mathutils import Vector

LIGHT = "Money_Blue"; TARGET = Vector((0, 0, 0.89)); SOLO = False   # SOLO=True hides other lights in viewport

o = bpy.data.objects[LIGHT]; d = o.data; p = o.matrix_world.translation
fwd = o.matrix_world.to_3x3() @ Vector((0, 0, -1))
print("aim error deg: %.1f (>15 = re-aim)" % math.degrees(fwd.angle((TARGET - p).normalized())))
print("effective power: %.0f W (power %.0f x 2^exposure %.2f)" % (d.energy * 2 ** d.exposure, d.energy, d.exposure))
c = o.light_linking.receiver_collection
print("receivers:", c.name if c else "ALL", [(x.name, i.light_linking.link_state) for x, i in zip(c.objects, c.collection_objects)][:6] if c else "")
sc = bpy.context.scene; cam = sc.camera.matrix_world.translation; caz = math.atan2(cam.y, cam.x)
print("angle from camera: %.0f deg, height %.2f m" % ((math.degrees(math.atan2(p.y, p.x) - caz) + 540) % 360 - 180, p.z))
same = [x.name for x in sc.objects if x.type == "LIGHT" and x != o and tuple(x.data.color) == tuple(d.color)]
print("lights with the same colour (check them too):", same)
if SOLO:
    for x in sc.objects:
        if x.type == "LIGHT" and x != o: x.hide_viewport = True
    print("SOLO on — remember to unhide")
# re-aim: o.rotation_euler = (TARGET - p).to_track_quat('-Z','Y').to_euler()
