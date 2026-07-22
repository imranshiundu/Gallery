"""
Clean failed bake textures and rebake properly
Usage: blender --background gallery_pro.blend --python clean_and_bake.py
"""

import bpy
import os

def clean_materials():
    print("Cleaning failed bake textures...")
    cleaned = 0
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        for mat in obj.data.materials:
            if not mat or not mat.use_nodes:
                continue
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            bsdf = nodes.get("Principled BSDF")
            if not bsdf:
                continue

            baked_nodes = [n for n in nodes if n.type == 'TEX_IMAGE' and '_Baked' in n.name]
            for node in baked_nodes:
                nodes.remove(node)
                cleaned += 1

            if not links:
                output = nodes.get("Material Output")
                if output:
                    links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    print(f"Cleaned {cleaned} bake texture nodes")

def bake_all():
    print("\nBaking lighting...")

    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 32
    bpy.context.scene.cycles.use_denoising = True
    bpy.context.scene.render.bake.use_pass_direct = False
    bpy.context.scene.render.bake.use_pass_indirect = True
    bpy.context.scene.render.bake.use_pass_color = True

    baked_count = 0
    skipped_count = 0

    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        if not obj.data.materials:
            continue

        has_image = False
        for mat in obj.data.materials:
            if not mat or not mat.use_nodes:
                continue
            for node in mat.node_tree.nodes:
                if node.type == 'TEX_IMAGE':
                    has_image = True
                    break
            if has_image:
                break

        if has_image:
            skipped_count += 1
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

            base_color_key = None
            for key in ["Base Color", "Color", "Base_color"]:
                if key in bsdf.inputs:
                    base_color_key = key
                    break
            if not base_color_key:
                continue

            img_name = f"{obj.name}_Baked"
            img = bpy.data.images.new(img_name, width=512, height=512)
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
                baked_count += 1
                print(f"  Baked: {obj.name}")
            except Exception as e:
                print(f"  Failed: {obj.name} - {e}")

            for link in list(links):
                links.remove(link)
            links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

            tex_baked = nodes.new('ShaderNodeTexImage')
            tex_baked.image = img
            tex_baked.location = (-600, 100)
            links.new(tex_baked.outputs["Color"], bsdf.inputs[base_color_key])

        obj.select_set(False)

    print(f"\nBaked: {baked_count}, Skipped: {skipped_count}")

def main():
    print("\n" + "="*50)
    print("CLEAN AND BAKE")
    print("="*50)

    clean_materials()
    bake_all()

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
    print(f"\nExported: {export_path}")

    blend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gallery_pro.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Saved: {blend_path}")

if __name__ == "__main__":
    main()
