"""
Add windows to gallery and bake lighting
Usage: blender --background gallery_pro.blend --python add_windows_bake.py
"""

import bpy
import math
import os

def add_window(location, rotation, width, height, name):
    coll = None
    for c in bpy.data.collections:
        if c.name == "Windows":
            coll = c
            break
    if not coll:
        coll = bpy.data.collections.new("Windows")
        bpy.context.scene.collection.children.link(coll)
    
    # Window frame
    frame_mat = bpy.data.materials.new(name=f"{name}_Frame_Mat")
    frame_mat.use_nodes = True
    bsdf = frame_mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (0.1, 0.1, 0.1, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.8
    bsdf.inputs["Roughness"].default_value = 0.2
    
    # Frame pieces
    frame_depth = 0.05
    frame_width = 0.04
    
    # Top frame
    bpy.ops.mesh.primitive_cube_add(size=1, location=(
        location[0], location[1], location[2] + height/2
    ))
    top = bpy.context.active_object
    top.name = f"{name}_Top"
    top.scale = (width + frame_width*2, frame_depth, frame_width)
    top.rotation_euler = rotation
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    top.data.materials.append(frame_mat)
    for c in top.users_collection:
        c.objects.unlink(top)
    coll.objects.link(top)
    
    # Bottom frame
    bpy.ops.mesh.primitive_cube_add(size=1, location=(
        location[0], location[1], location[2] - height/2
    ))
    bottom = bpy.context.active_object
    bottom.name = f"{name}_Bottom"
    bottom.scale = (width + frame_width*2, frame_depth, frame_width)
    bottom.rotation_euler = rotation
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    bottom.data.materials.append(frame_mat)
    for c in bottom.users_collection:
        c.objects.unlink(bottom)
    coll.objects.link(bottom)
    
    # Left frame
    bpy.ops.mesh.primitive_cube_add(size=1, location=(
        location[0] - width/2, location[1], location[2]
    ))
    left = bpy.context.active_object
    left.name = f"{name}_Left"
    left.scale = (frame_width, frame_depth, height)
    left.rotation_euler = rotation
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    left.data.materials.append(frame_mat)
    for c in left.users_collection:
        c.objects.unlink(left)
    coll.objects.link(left)
    
    # Right frame
    bpy.ops.mesh.primitive_cube_add(size=1, location=(
        location[0] + width/2, location[1], location[2]
    ))
    right = bpy.context.active_object
    right.name = f"{name}_Right"
    right.scale = (frame_width, frame_depth, height)
    right.rotation_euler = rotation
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    right.data.materials.append(frame_mat)
    for c in right.users_collection:
        c.objects.unlink(right)
    coll.objects.link(right)
    
    # Glass pane
    glass_mat = bpy.data.materials.new(name=f"{name}_Glass_Mat")
    glass_mat.use_nodes = True
    glass_bsdf = glass_mat.node_tree.nodes.get("Principled BSDF")
    glass_bsdf.inputs["Base Color"].default_value = (0.6, 0.8, 1.0, 1.0)
    glass_bsdf.inputs["Alpha"].default_value = 0.3
    glass_bsdf.inputs["Roughness"].default_value = 0.0
    glass_bsdf.inputs["Metallic"].default_value = 0.0
    glass_mat.blend_method = 'BLEND' if hasattr(glass_mat, 'blend_method') else None
    
    bpy.ops.mesh.primitive_plane_add(size=1, location=location)
    glass = bpy.context.active_object
    glass.name = f"{name}_Glass"
    glass.scale = (width/2, height/2, 1)
    glass.rotation_euler = rotation
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    glass.data.materials.append(glass_mat)
    for c in glass.users_collection:
        c.objects.unlink(glass)
    coll.objects.link(glass)
    
    # Sky light behind window
    bpy.ops.object.light_add(type='SUN', location=(
        location[0] + math.sin(rotation[2]) * 2,
        location[1] + math.cos(rotation[2]) * 2,
        location[2] + 1
    ))
    sun = bpy.context.active_object
    sun.name = f"{name}_Sun"
    sun.data.energy = 3
    sun.data.color = (1.0, 0.95, 0.85)
    sun.rotation_euler = rotation
    for c in sun.users_collection:
        c.objects.unlink(sun)
    coll.objects.link(sun)
    
    print(f"  Added window: {name}")
    return glass

def bake_lighting():
    print("\nBaking lighting...")
    
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 128
    bpy.context.scene.cycles.use_denoising = True
    
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            if not obj.data.materials:
                continue
            
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            
            for mat in obj.data.materials:
                if not mat.use_nodes:
                    continue
                
                nodes = mat.node_tree.nodes
                links = mat.node_tree.links
                
                bsdf = nodes.get("Principled BSDF")
                if not bsdf:
                    continue
                
                # Check if already has image texture
                has_image = False
                for node in nodes:
                    if node.type == 'TEX_IMAGE':
                        has_image = True
                        break
                
                if has_image:
                    continue
                
                # Create bake target image
                img_name = f"{obj.name}_Baked"
                img = bpy.data.images.new(img_name, width=1024, height=1024)
                
                tex_node = nodes.new('ShaderNodeTexImage')
                tex_node.image = img
                tex_node.location = (-600, 0)
                
                # Link to emission for baking
                emission = nodes.new('ShaderNodeEmission')
                emission.location = (-400, 0)
                
                # Find the correct output socket name
                base_color_key = None
                for key in ["Base Color", "Color", "Base_color"]:
                    if key in bsdf.outputs:
                        base_color_key = key
                        break
                
                if base_color_key:
                    links.new(bsdf.outputs[base_color_key], emission.inputs["Color"])
                
                output = nodes.get("Material Output")
                links.new(emission.outputs["Emission"], output.inputs["Surface"])
                
                # Bake
                bpy.context.scene.render.bake.use_pass_direct = False
                bpy.context.scene.render.bake.use_pass_indirect = True
                
                try:
                    bpy.ops.object.bake(type='EMIT')
                    print(f"  Baked: {obj.name}")
                except Exception as e:
                    print(f"  Bake failed for {obj.name}: {e}")
                
                # Restore original connections
                links.clear()
                links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
                
                # Add image texture to material
                if base_color_key:
                    tex_node_baked = nodes.new('ShaderNodeTexImage')
                    tex_node_baked.image = img
                    tex_node_baked.location = (-600, 200)
                    links.new(tex_node_baked.outputs["Color"], bsdf.inputs[base_color_key])
                
                obj.select_set(False)

def main():
    print("\n" + "="*50)
    print("ADDING WINDOWS AND BAKING LIGHTING")
    print("="*50 + "\n")
    
    # Add windows on the south wall (front, y=4)
    print("[1/2] Adding windows...")
    add_window(
        location=(-2, 3.94, 2.2),
        rotation=(0, 0, math.pi),
        width=2.5,
        height=2.0,
        name="Window_South_1"
    )
    add_window(
        location=(2, 3.94, 2.2),
        rotation=(0, 0, math.pi),
        width=2.5,
        height=2.0,
        name="Window_South_2"
    )
    
    # Add windows on the west wall (left, x=-6)
    add_window(
        location=(-5.94, 0, 2.2),
        rotation=(0, math.pi/2, 0),
        width=3.0,
        height=2.0,
        name="Window_West_1"
    )
    
    # Bake lighting
    print("\n[2/2] Baking lighting...")
    bake_lighting()
    
    # Export
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
    print(f"\nExported to {export_path}")
    
    blend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gallery_pro.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Saved blend file: {blend_path}")

if __name__ == "__main__":
    main()
