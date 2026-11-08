"""Screen pixel effect (approved look): the screen video is multiplied by a tiny repeating
pixel mask so real-looking pixels show on close-ups. Run inside Blender (MCP execute or -b).

Shapes (ask the user which one):
  "stripes"  RGB subpixel bars, red|green|blue  (the approved default, like a real LCD)
  "dots"     RGB subpixel circles, red|green|blue
  "circles"  one full-colour round cell per pixel (LED-wall look, cheap shader version)
  "squares"  one full-colour rounded-square cell per pixel

Usage:
  import screen_fx as fx
  fx.apply(["Win11_Screen", "Win11_Screen_Revisions"], shape="stripes", cells=(640, 383))
  # later: change look everywhere at once
  bpy.data.node_groups["RGB_Screen_FX"].nodes["Strength"]... or edit group input default

What apply() does per material (never deletes nodes):
  - inserts group RGB_Screen_FX before every Emission node's Color input
  - multiplies that Emission's Strength by 1/(1 - s*(1 - mask_mean)) so overall brightness stays
  - adds a soft, faint glass layer before the Material Output (Glossy rough 0.25, colour 0.022)
cells = pixel count across/down the screen; keep cells square: cells_y = cells_x * screen_h / screen_w.
"""
import bpy
import numpy as np

GROUP = "RGB_Screen_FX"
SIZE = 128


def _rounded_rect(xx, yy, x0, x1, y0, y1, r):
    cx = np.clip(xx, x0 + r, x1 - r)
    cy = np.clip(yy, y0 + r, y1 - r)
    return ((xx - cx) ** 2 + (yy - cy) ** 2) <= r * r


def make_mask(shape="stripes", size=SIZE):
    """Build the mask as a packed image (no file needed). Returns (image, mean brightness)."""
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32) / size + 0.5 / size
    rgb = np.zeros((size, size, 3), np.float32)
    if shape in ("stripes", "dots"):
        w = 1 / 3
        for c in range(3):
            x0, x1 = c * w + 0.025, (c + 1) * w - 0.025
            if shape == "stripes":
                m = _rounded_rect(xx, yy, x0, x1, 0.03, 0.97, 0.06)
            else:
                m = ((xx - (x0 + x1) / 2) ** 2 + (yy - 0.5) ** 2) <= (0.155 ** 2)
            rgb[..., c][m] = 1.0
    elif shape == "circles":
        m = ((xx - 0.5) ** 2 + (yy - 0.5) ** 2) <= 0.42 ** 2
        rgb[m] = 1.0
    elif shape == "squares":
        m = _rounded_rect(xx, yy, 0.06, 0.94, 0.06, 0.94, 0.08)
        rgb[m] = 1.0
    else:
        raise ValueError("shape must be stripes / dots / circles / squares")
    name = f"PixelMask_{shape}"
    img = bpy.data.images.get(name) or bpy.data.images.new(name, size, size, alpha=False, float_buffer=False)
    if tuple(img.size) != (size, size):
        img.scale(size, size)
    rgba = np.concatenate([rgb, np.ones((size, size, 1), np.float32)], axis=2)
    img.colorspace_settings.name = "Non-Color"
    img.pixels.foreach_set(rgba.ravel())
    img.update()
    img.pack()  # keeps the generated pixels inside the .blend
    return img, float(rgb.mean())


def build_group(shape="stripes", cells=(640, 383), strength=1.0):
    img, mean = make_mask(shape)
    g = bpy.data.node_groups.get(GROUP) or bpy.data.node_groups.new(GROUP, "ShaderNodeTree")
    g.nodes.clear()
    for it in list(g.interface.items_tree):
        g.interface.remove(it)
    g.interface.new_socket("Color", in_out="INPUT", socket_type="NodeSocketColor")
    s = g.interface.new_socket("RGB Effect Strength", in_out="INPUT", socket_type="NodeSocketFloat")
    s.default_value, s.min_value, s.max_value = strength, 0.0, 1.0
    g.interface.new_socket("Color", in_out="OUTPUT", socket_type="NodeSocketColor")
    N, L = g.nodes, g.links
    gi, go = N.new("NodeGroupInput"), N.new("NodeGroupOutput")
    tc, mp = N.new("ShaderNodeTexCoord"), N.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (cells[0], cells[1], 1)
    mk = N.new("ShaderNodeTexImage"); mk.image = img; mk.interpolation = "Linear"; mk.name = "Pixel_Mask"
    mix = N.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "MIX"
    mul = N.new("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"
    mul.inputs[0].default_value = 1.0
    col = lambda n, nm: [i for i in n.inputs if i.name == nm and i.type == "RGBA"][0]
    out = lambda n: [o for o in n.outputs if o.type == "RGBA"][0]
    col(mix, "A").default_value = (1, 1, 1, 1)
    L.new(tc.outputs["UV"], mp.inputs["Vector"]); L.new(mp.outputs["Vector"], mk.inputs["Vector"])
    L.new(mk.outputs["Color"], col(mix, "B")); L.new(gi.outputs[1], mix.inputs[0])
    L.new(gi.outputs[0], col(mul, "A")); L.new(out(mix), col(mul, "B")); L.new(out(mul), go.inputs[0])
    for i, n in enumerate((gi, tc, mp, mk, mix, mul, go)):
        n.location = (i * 220, 0)
    g["mask_mean"] = mean
    g["shape"] = shape
    return g


def apply(material_names, shape="stripes", cells=(640, 383), strength=1.0,
          glass_rough=0.25, glass_color=0.022):
    g = build_group(shape, cells, strength)
    comp = 1.0 / (1.0 - strength * (1.0 - g["mask_mean"]))
    report = []
    for mn in material_names:
        m = bpy.data.materials[mn]; nt = m.node_tree; N, L = nt.nodes, nt.links
        if any(n.type == "GROUP" and n.node_tree == g for n in N):
            report.append((mn, "already has the effect")); continue
        for e in [n for n in N if n.type == "EMISSION" and n.inputs["Color"].is_linked]:
            src = e.inputs["Color"].links[0].from_socket
            gn = N.new("ShaderNodeGroup"); gn.node_tree = g
            gn.name = gn.label = f"{GROUP}_{e.name}"; gn.location = (e.location.x - 220, e.location.y)
            L.new(src, gn.inputs[0]); L.new(gn.outputs[0], e.inputs["Color"])
            old = e.inputs["Strength"].default_value
            e.inputs["Strength"].default_value = old * comp
            report.append((mn, e.name, round(old, 3), round(old * comp, 3)))
        outn = [n for n in N if n.type == "OUTPUT_MATERIAL" and n.is_active_output][0]
        if outn.inputs["Surface"].is_linked:
            fs = outn.inputs["Surface"].links[0].from_socket
            gl = N.new("ShaderNodeBsdfGlossy"); gl.name = "Screen_Glass"
            gl.inputs["Roughness"].default_value = glass_rough
            gl.inputs["Color"].default_value = (glass_color, glass_color, glass_color, 1)
            ad = N.new("ShaderNodeAddShader"); ad.name = "Screen_Add_Glass"
            gl.location = (outn.location.x - 200, outn.location.y - 200)
            ad.location = (outn.location.x - 100, outn.location.y - 60)
            L.new(fs, ad.inputs[0]); L.new(gl.outputs[0], ad.inputs[1]); L.new(ad.outputs[0], outn.inputs["Surface"])
    return report
