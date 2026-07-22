import bpy
bpy.ops.export_scene.gltf(
    filepath='/home/imran/Code/Kood Corner/Gallery/public/models/gallery.glb',
    export_format='GLB',
    use_selection=False,
    export_apply=False,
    export_cameras=True,
    export_lights=True,
    export_materials='EXPORT'
)
print('Exported without apply')
