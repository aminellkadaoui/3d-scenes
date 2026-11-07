# 3D Scenes — keep HDRI lighting but hide it from camera AND reflections (dark designed backdrop).
import bpy
COLOR = (0.006, 0.007, 0.010, 1)
w = bpy.context.scene.world; nt = w.node_tree; N = nt.nodes; L = nt.links
out = next(n for n in N if n.type == "OUTPUT_WORLD"); bg = next(n for n in N if n.type == "BACKGROUND" and n.name != "Camera_Backdrop")
if "CamRay_Backdrop_Mix" not in N:
    lp = N.new("ShaderNodeLightPath"); bd = N.new("ShaderNodeBackground"); bd.name = "Camera_Backdrop"
    mx = N.new("ShaderNodeMixShader"); mx.name = "CamRay_Backdrop_Mix"
    m = N.new("ShaderNodeMath"); m.operation = "MAXIMUM"
    for l in list(out.inputs["Surface"].links): L.remove(l)
    L.new(lp.outputs["Is Camera Ray"], m.inputs[0]); L.new(lp.outputs["Is Glossy Ray"], m.inputs[1])
    L.new(m.outputs[0], mx.inputs["Fac"]); L.new(bg.outputs[0], mx.inputs[1]); L.new(bd.outputs[0], mx.inputs[2])
    L.new(mx.outputs[0], out.inputs["Surface"])
N["Camera_Backdrop"].inputs["Color"].default_value = COLOR
print("world: HDRI lights the scene; camera + glossy rays see", COLOR[:3])
