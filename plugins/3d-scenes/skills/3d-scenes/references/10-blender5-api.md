# 10 — Blender 5.x Python traps (verified in 5.2)

| Topic | Old / wrong | 5.x correct |
|---|---|---|
| F-curves | `action.fcurves` | Slotted actions: `for l in action.layers: for s in l.strips: for cb in s.channelbags: cb.fcurves` |
| Engine id | `BLENDER_EEVEE_NEXT` | `BLENDER_EEVEE` (set inside try/except, read back) |
| Compositor | `scene.node_tree`, Composite node, `use_nodes` | `scene.compositing_node_group` = a `CompositorNodeTree` node group with a **Group Output**; create sockets via `ng.interface.new_socket('Image', in_out='OUTPUT', socket_type='NodeSocketColor')`; `scene.render.use_compositing = True` |
| Denoise node options | `node.prefilter`, `node.use_hdr` | Input sockets: `HDR`, `Prefilter`, `Quality` |
| Light linking state | `coll.collection_objects['name']` | Not supported → `zip(coll.objects, coll.collection_objects)` then `item.light_linking.link_state = 'EXCLUDE'` |
| Light linking target | — | `obj.light_linking.receiver_collection = coll` (also `blocker_collection` for shadows) |
| EEVEE settings | legacy names | `taa_render_samples`, `use_raytracing`, `ray_tracing_method` ('SCREEN'/'PROBE'), `ray_tracing_options.resolution_scale` ('1','2'…), `.denoise_temporal`, `.trace_max_roughness`, `use_fast_gi`, `fast_gi_resolution` ('1'), `fast_gi_ray_count`, `fast_gi_quality` (precision), `fast_gi_step_count`, `shadow_ray_count`, `shadow_step_count`, `motion_blur_steps`, `use_overscan`, `overscan_size` |
| Motion blur | — | `scene.render.use_motion_blur`, `scene.render.motion_blur_shutter` |
| Light probes | — | `bpy.data.lightprobes.new(name, 'PLANE')`; props `clip_start`, `influence_distance` |
| Principled sockets | `Specular` | `Specular IOR Level`, `Coat Weight`, `Coat Roughness`, `Coat IOR`, `Emission Color/Strength` |
| Shader node lookup | by name | by `type` (`'BSDF_PRINCIPLED'`, `'NORMAL_MAP'`, `'TEX_IMAGE'`) — names are localised/renamed |
| Some socket types | `sock.default_value` everywhere | Shader sockets have none — guard with `hasattr` |
| Enum values | hard-coded | read `bl_rna.properties[prop].enum_items` when unsure |
| Hide keys | `hide` | key `hide_render` **and** `hide_viewport`, CONSTANT |

## MCP specifics
- `look` with `shading='rendered'` works only for EEVEE/Workbench; through the camera use `mode='camera'`.
- `look` may not show screen-space reflections the user sees — don't conclude "no reflection" from it.
- Poly Haven / Sketchfab toggles are scene properties (`scene.blendermcp_use_polyhaven`); Sketchfab needs an API key.
- `import_asset(apply_to=...)` creates a material named `<id>_material_<object>` and may keep your renamed copy unused — assign the material you edited explicitly.
- Select for the user: deselect all → `obj.select_set(True)` → `view_layer.objects.active = obj` → set Properties area `context='DATA'` → `outliner.show_active` via `temp_override`.
