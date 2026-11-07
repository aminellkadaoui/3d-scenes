# 3D Scenes — "track matte" lighting with Light Linking (Blender 5.x).
# 1) isolate(): exclude objects from EVERY other light (incl. lights that already use a collection)
# 2) only(): make a light affect only a list of objects
# 3) report(): print who lights what
import bpy

def _coll(name):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    return c

def _set_state(coll, names, state):
    for o, item in zip(coll.objects, coll.collection_objects):
        if o.name in names: item.light_linking.link_state = state

def only(light_name, object_names, coll_name):
    """Light affects only these objects (Include)."""
    c = _coll(coll_name)
    for n in object_names:
        if n not in c.objects: c.objects.link(bpy.data.objects[n])
    _set_state(c, set(object_names), "INCLUDE")
    bpy.data.objects[light_name].light_linking.receiver_collection = c

def isolate(object_names, keep_lights=(), exclude_coll="LL_Exclude_Hero"):
    """Remove these objects from all lights except keep_lights."""
    ex = _coll(exclude_coll); names = set(object_names)
    for L in [o for o in bpy.context.scene.objects if o.type == "LIGHT" and o.name not in keep_lights]:
        c = L.light_linking.receiver_collection
        if c is None:
            L.light_linking.receiver_collection = ex; c = ex
        # if c is an INCLUDE list, just drop the hero from it
        for n in names:
            if n not in c.objects: c.objects.link(bpy.data.objects[n])
        has_include = any(i.light_linking.link_state == "INCLUDE" and o.name not in names
                          for o, i in zip(c.objects, c.collection_objects))
        if has_include:
            for n in names:
                if n in c.objects: c.objects.unlink(bpy.data.objects[n])
        else:
            _set_state(c, names, "EXCLUDE")

def report():
    for L in [o for o in bpy.context.scene.objects if o.type == "LIGHT"]:
        c = L.light_linking.receiver_collection
        if not c: print(L.name, "-> ALL"); continue
        st = {}
        for o, i in zip(c.objects, c.collection_objects): st.setdefault(i.light_linking.link_state, []).append(o.name)
        print(L.name, "->", c.name, {k: (len(v), v[:3]) for k, v in st.items()},
              "| %.0f W exp %.1f" % (L.data.energy, L.data.exposure))

# Example (edit names):
# money = [o.name for o in bpy.data.objects if o.name.startswith("Money_Bundle_")]
# isolate(money, keep_lights=("Money_Fill", "Money_Sweep_L", "Money_Sweep_R", "Rim_Blue_Back"))
# only("Money_Fill", money, "LL_Money_Only")
report()
