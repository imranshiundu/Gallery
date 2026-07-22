"""
Simple bake - just render and save baked textures
Usage: blender --background gallery_pro.blend --python bake_simple.py
"""

import bpy
import os

def clean_old_bakes():
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

    for img in list(bpy.data.images):
        if '_Baked' in img.name:
            bpy.data.images.remove(img)

def bake():
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 32
    bpy.context.scene.render.bake.use_pass_direct = False
    bpy.context.scene.render.bake.use_pass_indirect = True

    baked = 0
    for obj in bpy.data.objects:
        if obj.type != 'MESH' or not obj.data.materials:
            continue

        has_image = False
        for mat in obj.data.materials:
            if mat and mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE':
                        has_image = True
                        break
            if has_image:
                break
        if has_image:
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

            color_key = None
            for k in ["Base Color", "Color"]:
                if k in bsdf.inputs:
                    color_key = k
                    break
            if not color_key:
                continue

            img = bpy.data.images.new(f"{obj.name}_Baked", width=512, height=512)
            img.colorspace_settings.name = 'sRGB'

            tex = nodes.new('ShaderNodeTexImage')
            tex.image = img
            tex.location = (-600, 0)
            tex.select = True
            nodes.active = tex

            emission = nodes.new('ShaderNodeEmission')
            emission.location = (-400, 0)

            color_val = bsdf.inputs[color_key].default_value
            emission.inputs["Color"].default_value = color_val

            output = nodes.get("Material Output")
            links.new(emission.outputs["Emission"], output.inputs["Surface"])

            try:
                bpy.ops.object.bake(type='EMIT')
                baked += 1
                print(f"Baked: {obj.name}")
            except Exception as e:
                print(f"Failed: {obj.name}: {e}")

            for link in list(links):
                links.remove(link)
            links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

            tex2 = nodes.new('ShaderNodeTexImage')
            tex2.image = img
            tex2.location = (-600, 200)
            links.new(tex2.outputs["Color"], bsdf.inputs[color_key])

        obj.select_set(False)

    print(f"Total baked: {baked}")

def main():
    print("Clean and bake...")
    clean_old_bakes()
    bake()

    export_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports", "gallery_pro.glb")
    bpy.ops.export_scene.gltf(
        filepath=export_path,
        export_format='GLB',
        use_selection=False,
        export_apply=True,
        export_cameras=True,
        export_lights=False,
        export_materials='EXPORT'
    )
    print(f"Exported: {export_path}")

    blend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gallery_pro.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Saved: {blend_path}")

if __name__ == "__main__":
    main()
