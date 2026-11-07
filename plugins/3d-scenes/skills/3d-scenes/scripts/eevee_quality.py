# 3D Scenes — final EEVEE quality profile + OIDN compositor denoise. Prints before -> after.
import bpy

PROFILE = dict(samples=256, ray_res="1", fastgi_res="1", fastgi_rays=8, fastgi_precision=1.0,
               fastgi_steps=16, shadow_rays=3, shadow_steps=16, mblur_steps=3, shutter=0.5,
               overscan=0.2, dof=False, temporal_denoise=False, add_denoise=True)
P = PROFILE; sc = bpy.context.scene; e = sc.eevee; log = []

def setp(obj, attr, val):
    old = getattr(obj, attr)
    try: setattr(obj, attr, val); log.append(f"{attr}: {old} -> {getattr(obj, attr)}")
    except Exception as ex: log.append(f"! {attr}: {ex}")

try: sc.render.engine = "BLENDER_EEVEE"
except TypeError as ex: log.append(str(ex))
setp(e, "taa_render_samples", P["samples"]); setp(e, "use_raytracing", True)
setp(e, "ray_tracing_method", "SCREEN"); ro = e.ray_tracing_options
setp(ro, "resolution_scale", P["ray_res"]); setp(ro, "use_denoise", True); setp(ro, "denoise_temporal", P["temporal_denoise"])
setp(e, "use_fast_gi", True); setp(e, "fast_gi_resolution", P["fastgi_res"]); setp(e, "fast_gi_ray_count", P["fastgi_rays"])
setp(e, "fast_gi_quality", P["fastgi_precision"]); setp(e, "fast_gi_step_count", P["fastgi_steps"])
setp(e, "shadow_ray_count", P["shadow_rays"]); setp(e, "shadow_step_count", P["shadow_steps"])
setp(e, "motion_blur_steps", P["mblur_steps"]); setp(sc.render, "use_motion_blur", True); setp(sc.render, "motion_blur_shutter", P["shutter"])
setp(e, "use_overscan", True); setp(e, "overscan_size", P["overscan"])
if sc.camera: setp(sc.camera.data.dof, "use_dof", P["dof"])

if P["add_denoise"]:
    vl = bpy.context.view_layer; vl.use_pass_normal = True; vl.use_pass_diffuse_color = True
    ng = bpy.data.node_groups.get("CMP_Denoise_Clean") or bpy.data.node_groups.new("CMP_Denoise_Clean", "CompositorNodeTree")
    ng.nodes.clear()
    if not any(getattr(s, "in_out", "") == "OUTPUT" for s in ng.interface.items_tree):
        ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    rl = ng.nodes.new("CompositorNodeRLayers"); rl.scene = sc; rl.location = (-400, 0)
    dn = ng.nodes.new("CompositorNodeDenoise"); out = ng.nodes.new("NodeGroupOutput"); out.location = (300, 0)
    ng.links.new(rl.outputs["Image"], dn.inputs["Image"])
    for o in rl.outputs:
        if o.name == "Normal": ng.links.new(o, dn.inputs["Normal"])
        if o.name in ("Diffuse Color", "DiffCol"): ng.links.new(o, dn.inputs["Albedo"])
    ng.links.new(dn.outputs[0], out.inputs[0])
    if sc.compositing_node_group and sc.compositing_node_group != ng:
        log.append(f"previous compositor kept as node group: {sc.compositing_node_group.name}")
    sc.compositing_node_group = ng; sc.render.use_compositing = True
    log.append("compositor -> CMP_Denoise_Clean (OIDN, Normal+Albedo)")
print("\n".join(log))
