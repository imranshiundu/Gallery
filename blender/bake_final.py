"""
Bake lighting into textures for gallery scene
Usage: blender --background gallery_pro.blend --python bake_final.py
"""

import bpy
import os

def get_base_color_input(bsdf):
    for key in ["Base Color", "Color", "Base_color"]:
        if key in bsdf.inputs:
            return key
    return None

def bake_scene():
    print("\nPreparing bake...")

    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 64
    bpy.context.scene.cycles.use_denoising = True
    bpy.context.scene.render.bake.use_pass_direct = False
    bpy.context.scene.render.bake.use_pass_indirect = True
    bpy.context.scene.render.bake.use_pass_color = True

    objects_to_bake = []
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        if not obj.data.materials:
            continue
        objects_to_bake.append(obj)

    print(f"Found {len(objects_to_bake)} mesh objects to bake")

    for obj in objects_to_bake:
        has_image_texture = False
        for mat in obj.data.materials:
            if not mat or not mat.use_nodes:
                continue
            for node in mat.node_tree.nodes:
                if node.type == 'TEX_IMAGE':
                    has_image_texture = True
                    break
            if has_image_texture:
                break

        if has_image_texture:
            print(f"  Skipping {obj.name} (has image texture)")
            continue

        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        for mat in obj.data.materials:
            if not mat or not mat.use_nodes:
                continue

            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            bsdf = nodes.get("Principled BSDF")
            if not bsdf:
                continue

            base_color_key = get_base_color_input(bsdf)
            if not base_color_key:
                continue

            img_name = f"{obj.name}_Baked"
            img = bpy.data.images.new(img_name, width=1024, height=1024)
            img.colorspace_settings.name = 'sRGB'

            tex_node = nodes.new('ShaderNodeTexImage')
            tex_node.image = img
            tex_node.location = (-600, 300)
            tex_node.select = True
            nodes.active = tex_node

            emission = nodes.new('ShaderNodeEmission')
            emission.location = (-400, 300)
            links.new(bsdf.inputs[base_color_key], emission.inputs["Color"])

            output = nodes.get("Material Output")
            links.new(emission.outputs["Emission"], output.inputs["Surface"])

            try:
                bpy.ops.object.bake(type='EMIT')
                print(f"  Baked: {obj.name}")
            except Exception as e:
                print(f"  Bake failed for {obj.name}: {e}")

            for link in links:
                links.remove(link)

            links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

            tex_node_baked = nodes.new('ShaderNodeTexImage')
            tex_node_baked.image = img
            tex_node_baked.location = (-600, 100)
            links.new(tex_node_baked.outputs["Color"], bsdf.inputs[base_color_key])

        obj.select_set(False)

def main():
    print("\n" + "="*50)
    print("BAKING LIGHTING INTO TEXTURES")
    print("="*50)

    bake_scene()

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
    export_path = os.path.join(output_dir, "gallery_pro.glb")
    bpy.ops.export_scene.gltf(
        filepath=export_path,
        export_format='GLB',
        use_selection=False,
        export_apply=True,
        export_cameras=True,
        export_lights=False,
        export_materials='EXPORT'
    )
    print(f"\nExported to {export_path}")

    blend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gallery_pro.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Saved: {blend_path}")

if __name__ == "__main__":
    main()
