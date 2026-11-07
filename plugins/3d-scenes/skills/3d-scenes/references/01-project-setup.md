# 01 — Project setup (Proven)

## Start from an approved scene, not an empty file
The fastest premium result came from **copying the user's existing project that already had a good model + lighting** and only changing what the new idea needed. Building lights from zero costs hours; tuning a good rig costs minutes.

1. Ask/locate: "Is there a project with the hero model and lighting you like?" Search: `mdfind -name .blend | grep -i <keyword>`.
2. Copy the **Collected** version (with `textures/` and `footage/` beside the .blend) into `<projects>/<shot>/blend/<shot>_v001.blend`. Never edit the original.
3. If Blender is open on another file, check `bpy.data.is_dirty`. Unsaved → ask the user to save; never close it yourself.
4. On macOS `open file.blend` can fail with error −600 while Blender starts: launch the binary instead (`/Applications/Blender.app/Contents/MacOS/Blender file.blend`, in the background).
5. `get_addon_status` + `get_scene_info` (fields: settings, materials, details). Note engine, view transform, frame range, camera, HDRI, every light's power/colour/existing light-linking collection.

## Keep, hide, never delete
- Unneeded things (old props, walls) → collection `_HIDDEN_<what>`, layer collection `exclude=True`.
- Mesh parts to remove (e.g. a table's lower shelf): split by **connected islands** with bmesh (`scripts/mesh_split.py`), move the island to `<name>_REMOVED` in the hidden collection.
- Keep the user's camera; add `CAM_<shot>` and set it as scene camera.

## Organisation that paid off
| Object / collection | Purpose |
|---|---|
| `Turntable_Drift` → `Turntable_Pivot` → heroes | Spin rig (06) |
| `<Hero>_Group` empty | Scale/move a multi-part model as one |
| `<Swap>_SLOT` empty under the pivot | Where the match-cut object lives |
| `CAM_Rig` → `CAM_<shot>` | Camera crane |
| `LL_*` collections | Light-linking receiver sets, one per light job |
| `_HIDDEN_*` (excluded) | Everything removed |

## Versioning
`<shot>_v001.blend`; save only when the user says so. For render jobs save a **copy** (`save_as_mainfile(filepath=..., copy=True)`) so the open file is untouched.
