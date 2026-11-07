# 3D Scenes — "mountain" speed graph (جراف الجبل) = After Effects Speed graph In 75% / Out 75%.
# THE DEFAULT for every move: camera, objects, zooms, UI/cursor. Speed 0 → smooth single peak in the middle → 0.
# Usage: set CONFIG (object + data_path [+ index]) and run, or import apply_mountain(fcurve).
# Exceptions: hold keys stay flat, constant drift / frame tracking stay LINEAR.
import bpy

CONFIG = dict(obj="CAM_Shot", data_path="location", index=None, influence=0.75)


def apply_mountain(fc, influence=0.75):
    """Every consecutive key pair becomes one mountain segment (flat tangents, FREE handles at influence × segment)."""
    kps = fc.keyframe_points
    for k in kps:
        k.interpolation = "BEZIER"
        k.handle_left_type = k.handle_right_type = "FREE"
    for a, b in zip(kps[:-1], kps[1:]):
        h = (b.co[0] - a.co[0]) * influence
        a.handle_right = (a.co[0] + h, a.co[1])
        b.handle_left = (b.co[0] - h, b.co[1])
    kps[0].handle_left = (kps[0].co[0] - 1, kps[0].co[1])
    kps[-1].handle_right = (kps[-1].co[0] + 1, kps[-1].co[1])
    fc.update()


def fcurves_of(obj):
    ad = obj.animation_data
    if not ad or not ad.action:
        return []
    a = ad.action
    if hasattr(a, "layers") and a.layers:  # Blender 5.x slotted actions
        return [fc for l in a.layers for s in l.strips for cb in s.channelbags for fc in cb.fcurves]
    return list(a.fcurves)


if __name__ == "__main__":
    C = CONFIG
    o = bpy.data.objects[C["obj"]]
    n = 0
    for fc in fcurves_of(o):
        if fc.data_path == C["data_path"] and (C["index"] is None or fc.array_index == C["index"]):
            apply_mountain(fc, C["influence"]); n += 1
    print("mountain applied to", n, "fcurves")
    # verify: print speed per frame — must rise from ~0, peak once mid-segment, fall to ~0
