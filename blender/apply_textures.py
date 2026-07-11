"""
Apply downloaded images to gallery paintings
Usage: blender --background gallery_pro.blend --python apply_textures.py
"""

import bpy
import os

TEXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public", "textures", "paintings")

PAINTING_MAPPING = {
    "Art_W1_Canvas": "painting_01.jpg",
    "Art_W2_Canvas": "painting_02.jpg",
    "Art_W3_Canvas": "painting_03.jpg",
    "Art_N1_Canvas": "painting_04.jpg",
    "Art_N2_Canvas": "painting_05.jpg",
    "Art_N3_Canvas": "painting_06.jpg",
    "Art_E1_Canvas": "painting_07.jpg",
    "Art_E2_Canvas": "painting_08.jpg",
    "Art_S1_Canvas": "painting_09.jpg",
    "Art_S2_Canvas": "painting_10.jpg",
    "Art_S3_Canvas": "painting_11.jpg",
}

def apply_image_texture(obj_name, image_path):
    if not os.path.exists(image_path):
        print(f"  Warning: Image not found: {image_path}")
        return False
    
    obj = bpy.data.objects.get(obj_name)
    if not obj:
        print(f"  Warning: Object not found: {obj_name}")
        return False
    
    img = bpy.data.images.load(image_path)
    
    mat = bpy.data.materials.new(name=f"{obj_name}_ImageMat")
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    bsdf = nodes.get("Principled BSDF")
    
    tex_node = nodes.new('ShaderNodeTexImage')
    tex_node.image = img
    tex_node.location = (-400, 0)
    
    links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
    
    bsdf.inputs["Roughness"].default_value = 0.85
    bsdf.inputs["Metallic"].default_value = 0.0
    
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    
    print(f"  Applied {os.path.basename(image_path)} to {obj_name}")
    return True

def main():
    print("\n" + "="*50)
    print("APPLYING IMAGE TEXTURES TO PAINTINGS")
    print("="*50 + "\n")
    
    applied = 0
    for obj_name, img_file in PAINTING_MAPPING.items():
        img_path = os.path.join(TEXTURES_DIR, img_file)
        if apply_image_texture(obj_name, img_path):
            applied += 1
    
    print(f"\nApplied {applied}/{len(PAINTING_MAPPING)} textures")
    
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
    export_path = os.path.join(output_dir, "gallery_pro.glb")
    bpy.ops.export_scene.gltf(
        filepath=export_path,
        export_format='GLB',
        use_selection=False,
        export_apply=True,
        export_cameras=True,
        export_lights=True,
        export_materials='EXPORT'
    )
    print(f"Exported to {export_path}")
    
    blend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gallery_pro.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Saved blend file: {blend_path}")

if __name__ == "__main__":
    main()
