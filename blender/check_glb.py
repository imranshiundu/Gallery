import bpy
import json

 bpy.ops.export_scene.gltf(
    filepath="/tmp/check_gallery.gltf",
    export_format='GLTF_SEPARATE',
    use_selection=False,
    export_apply=True,
    export_cameras=True,
    export_lights=True,
    export_materials='EXPORT'
)

with open("/tmp/check_gallery.gltf") as f:
    gltf = json.load(f)

for mesh in gltf.get("meshes", []):
    name = mesh.get("name", "unknown")
    if "Canvas" in name or "Wall" in name:
        prim = mesh["primitives"][0]
        accessor_idx = prim["attributes"]["POSITION"]
        accessor = gltf["accessors"][accessor_idx]
        buffer_view = gltf["bufferViews"][accessor["bufferView"]]
        print(f"{name}: min={accessor.get('min')}, max={accessor.get('max')}")
