# 3D Scenes — make banknote/paper bundles read as paper: warm tint + sheet lines on the sides.
# Assumes the stack axis is the object's local Y (check: thinnest local dimension). Units = object units.
import bpy, math

MATERIAL = "dollar"; STACK_AXIS = "Y"; SHEET_PITCH = 0.35   # object units per sheet line
TINT = (0.88, 0.92, 0.82, 1); VALUE = 0.75; ROUGH = 0.75

m = bpy.data.materials[MATERIAL]; N = m.node_tree.nodes; L = m.node_tree.links
b = next(n for n in N if n.type == "BSDF_PRINCIPLED")
for n in [n for n in N if n.name.startswith("PaperFX_")]: N.remove(n)
def nn(t, name):
    n = N.new(t); n.name = "PaperFX_" + name; n.label = name; return n
src = b.inputs["Base Color"].links[0].from_socket if b.inputs["Base Color"].is_linked else None
hv = nn("ShaderNodeHueSaturation", "Value"); hv.inputs["Value"].default_value = VALUE
if src: L.new(src, hv.inputs["Color"])
tint = nn("ShaderNodeMix", "Tint"); tint.data_type = "RGBA"; tint.blend_type = "MULTIPLY"; tint.inputs["Factor"].default_value = 1
tint.inputs["B"].default_value = TINT; L.new(hv.outputs[0], tint.inputs["A"])
tc = nn("ShaderNodeTexCoord", "Coord"); sp = nn("ShaderNodeSeparateXYZ", "Pos"); L.new(tc.outputs["Object"], sp.inputs[0])
no = nn("ShaderNodeTexNoise", "Wobble"); no.inputs["Scale"].default_value = 0.08; L.new(tc.outputs["Object"], no.inputs["Vector"])
wb = nn("ShaderNodeMath", "WobAmt"); wb.operation = "MULTIPLY"; wb.inputs[1].default_value = 0.6; L.new(no.outputs["Fac"], wb.inputs[0])
ad = nn("ShaderNodeMath", "Add"); ad.operation = "ADD"; L.new(sp.outputs[STACK_AXIS], ad.inputs[0]); L.new(wb.outputs[0], ad.inputs[1])
fq = nn("ShaderNodeMath", "Freq"); fq.operation = "MULTIPLY"; fq.inputs[1].default_value = 2 * math.pi / SHEET_PITCH; L.new(ad.outputs[0], fq.inputs[0])
sn = nn("ShaderNodeMath", "Sine"); sn.operation = "SINE"; L.new(fq.outputs[0], sn.inputs[0])
ln = nn("ShaderNodeMapRange", "Lines"); ln.inputs["From Min"].default_value = -1; L.new(sn.outputs[0], ln.inputs["Value"])
sn2 = nn("ShaderNodeSeparateXYZ", "Nrm"); L.new(tc.outputs["Normal"], sn2.inputs[0])
ab = nn("ShaderNodeMath", "Abs"); ab.operation = "ABSOLUTE"; L.new(sn2.outputs[STACK_AXIS], ab.inputs[0])
sd = nn("ShaderNodeMath", "SideMask"); sd.operation = "LESS_THAN"; sd.inputs[1].default_value = 0.5; L.new(ab.outputs[0], sd.inputs[0])
lm = nn("ShaderNodeMath", "LinesSides"); lm.operation = "MULTIPLY"; L.new(ln.outputs[0], lm.inputs[0]); L.new(sd.outputs[0], lm.inputs[1])
iv = nn("ShaderNodeMath", "Inv"); iv.operation = "SUBTRACT"; iv.inputs[0].default_value = 1; L.new(ln.outputs[0], iv.inputs[1])
gm = nn("ShaderNodeMath", "Groove"); gm.operation = "MULTIPLY"; L.new(iv.outputs[0], gm.inputs[0]); L.new(sd.outputs[0], gm.inputs[1])
ga = nn("ShaderNodeMath", "GrooveAmt"); ga.operation = "MULTIPLY"; ga.inputs[1].default_value = 0.5; L.new(gm.outputs[0], ga.inputs[0])
dk = nn("ShaderNodeMix", "Darken"); dk.data_type = "RGBA"; dk.blend_type = "MULTIPLY"; dk.inputs["B"].default_value = (0.72, 0.72, 0.70, 1)
L.new(ga.outputs[0], dk.inputs["Factor"]); L.new(tint.outputs["Result"], dk.inputs["A"]); L.new(dk.outputs["Result"], b.inputs["Base Color"])
bp = nn("ShaderNodeBump", "Bump"); bp.inputs["Strength"].default_value = 0.15; bp.inputs["Distance"].default_value = 0.0005
L.new(lm.outputs[0], bp.inputs["Height"]); L.new(bp.outputs["Normal"], b.inputs["Normal"])
b.inputs["Roughness"].default_value = ROUGH
print("paper material updated:", MATERIAL)
