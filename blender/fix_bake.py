"""
Fix baking by removing empty bake textures and rebaking
Usage: blender --background gallery_pro.blend --python fix_bake.py
"""

import bpy
import os

def clean_empty_bakes():
    print("Removing empty bake textures...")
    removed = 0

    baked_image_names = set()
    for img in bpy.data.images:
        if '_Baked' in img.name:
            baked_image_names.add(img.name)

    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        for mat in obj.data.materials:
            if not mat or not mat.use_nodes:
                continue
            nodes_to_remove = []
            for node in mat.node_tree.nodes:
                if node.type == 'TEX_IMAGE' and node.image and '_Baked' in node.image.name:
                    nodes_to_remove.append(node)
            for node in nodes_to_remove:
                mat.node_tree.nodes.remove(node)
                removed += 1

    for img_name in baked_image_names:
        img = bpy.data.images.get(img_name)
        if img:
            bpy.data.images.remove(img)

    print(f"Removed {removed} bake nodes")
    return removed

def bake_all():
    print("\nBaking...")

    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 32
    bpy.context.scene.cycles.use_denoising = True
    bpy.context.scene.render.bake.use_pass_direct = False
    bpy.context.scene.render.bake.use_pass_indirect = True
    bpy.context.scene.render.bake.use_pass_color = True

    baked = 0
    skipped = 0

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
            skipped += 1
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

            img = bpy.data.images.new(f"{obj.name}_Baked", width=512, height=512)
            img.colorspace_settings.name = 'sRGB'

            tex = nodes.new('ShaderNodeTexImage')
            tex.image = img
            tex.location = (-600, 300)
            tex.select = True
            nodes.active = tex

            emission = nodes.new('ShaderNodeEmission')
            emission.location = (-400, 300)
            links.new(bsdf.inputs[base_color_key], emission.inputs["Color"])

            output = nodes.get("Material Output")
            links.new(emission.outputs["Emission"], output.inputs["Surface"])

            try:
                bpy.ops.object.bake(type='EMIT')
                baked += 1
                print(f"  Baked: {obj.name}")
            except Exception as e:
                print(f"  Failed: {obj.name}: {e}")

            for link in list(links):
                links.remove(link)
            links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

            tex2 = nodes.new('ShaderNodeTexImage')
            tex2.image = img
            tex2.location = (-600, 100)
            links.new(tex2.outputs["Color"], bsdf.inputs[base_color_key])

        obj.select_set(False)

    print(f"\nBaked: {baked}, Skipped: {skipped}")

def main():
    print("\n" + "="*50)
    print("FIX BAKE")
    print("="*50)

    clean_empty_bakes()
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
