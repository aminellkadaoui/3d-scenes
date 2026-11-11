"""Endless floor in a black void: fade a floor material into the camera backdrop colour
so no horizon edge is ever visible (low or high camera). Run inside Blender.
See techniques/environment-endless-floor-void.md.

Usage:
  import endless_floor as ef
  ef.apply("Floor_Material", backdrop=(0.006, 0.007, 0.01), centre_fade=(1.5, 8.0), angle_fade=(0.30, 0.02))

The fade factor = MAX(angle fade, radial fade):
  angle  : Geometry.Incoming.Z, Map Range smoothstep (near the horizon Z -> 0)
  radial : length(Geometry.Position - centre), Map Range smoothstep, metres
backdrop must equal the colour the world shows to camera rays (read it from the world nodes).
Never deletes nodes; re-running updates the values.
"""
import bpy


def apply(material, backdrop=(0.006, 0.007, 0.01), centre=(0.0, 0.0, 0.0),
          centre_fade=(1.5, 8.0), angle_fade=(0.30, 0.02)):
    nt = bpy.data.materials[material].node_tree
    N, L = nt.nodes, nt.links
    out = [n for n in N if n.type == "OUTPUT_MATERIAL" and n.is_active_output][0]

    def get(name, kind):
        n = N.get(name)
        if n is None:
            n = N.new(kind)
            n.name = n.label = name
        return n

    mix = N.get("Horizon_Mix")
    if mix is None:
        src = out.inputs["Surface"].links[0].from_socket
        mix = get("Horizon_Mix", "ShaderNodeMixShader")
        L.new(src, mix.inputs[1])
        L.new(mix.outputs[0], out.inputs["Surface"])
    em = get("Horizon_Backdrop", "ShaderNodeEmission")
    em.inputs["Color"].default_value = (*backdrop, 1.0)
    em.inputs["Strength"].default_value = 1.0
    L.new(em.outputs[0], mix.inputs[2])

    geo = get("Horizon_Geo", "ShaderNodeNewGeometry")
    sep = get("Horizon_IncZ", "ShaderNodeSeparateXYZ")
    af = get("Horizon_Fade", "ShaderNodeMapRange")
    af.interpolation_type = "SMOOTHSTEP"
    af.inputs["From Min"].default_value, af.inputs["From Max"].default_value = angle_fade
    L.new(geo.outputs["Incoming"], sep.inputs[0])
    L.new(sep.outputs["Z"], af.inputs["Value"])

    sub = get("Radial_Offset", "ShaderNodeVectorMath")
    sub.operation = "SUBTRACT"
    sub.inputs[1].default_value = centre
    ln = get("Radial_Dist", "ShaderNodeVectorMath")
    ln.operation = "LENGTH"
    rf = get("Radial_Fade", "ShaderNodeMapRange")
    rf.interpolation_type = "SMOOTHSTEP"
    rf.inputs["From Min"].default_value, rf.inputs["From Max"].default_value = centre_fade
    L.new(geo.outputs["Position"], sub.inputs[0])
    L.new(sub.outputs[0], ln.inputs[0])
    L.new(ln.outputs["Value"], rf.inputs["Value"])

    mx = get("Fade_Max", "ShaderNodeMath")
    mx.operation = "MAXIMUM"
    L.new(af.outputs["Result"], mx.inputs[0])
    L.new(rf.outputs["Result"], mx.inputs[1])
    L.new(mx.outputs[0], mix.inputs["Fac"])
    return mix
