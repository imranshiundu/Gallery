"""
Gallery Scene Creator for Blender
Run this script in Blender to generate the gallery room, custom models, and lighting.
Usage: blender --background --python create_gallery.py
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)

def create_collection(name):
    collection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(collection)
    return collection

def set_collection(collection, obj):
    for obj_in_scene in list(bpy.context.scene.collection.objects):
        bpy.context.scene.collection.objects.unlink(obj_in_scene)
    collection.objects.link(obj)

def create_material(name, color, roughness=0.5, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return mat

def create_floor():
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "Floor"
    floor.scale = (6, 4, 1)
    bpy.ops.object.transform_apply(scale=True)
    
    mat = create_material("Floor_Material", (0.15, 0.15, 0.15), roughness=0.3, metallic=0.1)
    floor.data.materials.append(mat)
    
    bpy.ops.object.shade_smooth()
    return floor

def create_ceiling():
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 3.5))
    ceiling = bpy.context.active_object
    ceiling.name = "Ceiling"
    ceiling.scale = (6, 4, 1)
    ceiling.rotation_euler = (math.pi, 0, 0)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    
    mat = create_material("Ceiling_Material", (0.95, 0.95, 0.95), roughness=0.9)
    ceiling.data.materials.append(mat)
    
    bpy.ops.object.shade_smooth()
    return ceiling

def create_walls():
    walls_collection = create_collection("Walls")
    
    wall_data = [
        {"name": "Wall_Back", "location": (0, -4, 1.75), "rotation": (0, 0, 0), "scale": (6, 0.1, 3.5), "color": (0.95, 0.95, 0.95)},
        {"name": "Wall_Front", "location": (0, 4, 1.75), "rotation": (0, 0, 0), "scale": (6, 0.1, 3.5), "color": (0.95, 0.95, 0.95)},
        {"name": "Wall_Left", "location": (-6, 0, 1.75), "rotation": (0, 0, math.pi/2), "scale": (4, 0.1, 3.5), "color": (0.92, 0.92, 0.92)},
        {"name": "Wall_Right", "location": (6, 0, 1.75), "rotation": (0, 0, math.pi/2), "scale": (4, 0.1, 3.5), "color": (0.92, 0.92, 0.92)},
    ]
    
    walls = []
    for wall_info in wall_data:
        bpy.ops.mesh.primitive_cube_add(size=1, location=wall_info["location"])
        wall = bpy.context.active_object
        wall.name = wall_info["name"]
        wall.scale = wall_info["scale"]
        wall.rotation_euler = wall_info["rotation"]
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        
        mat = create_material(f"{wall_info['name']}_Mat", wall_info["color"], roughness=0.85)
        wall.data.materials.append(mat)
        
        walls.append(wall)
        set_collection(walls_collection, wall)
    
    return walls

def create_baseboard():
    baseboard_collection = create_collection("Baseboards")
    
    baseboard_data = [
        {"name": "Baseboard_Back", "location": (0, -3.95, 0.06), "rotation": (0, 0, 0), "scale": (6, 0.03, 0.12)},
        {"name": "Baseboard_Front", "location": (0, 3.95, 0.06), "rotation": (0, 0, 0), "scale": (6, 0.03, 0.12)},
        {"name": "Baseboard_Left", "location": (-5.95, 0, 0.06), "rotation": (0, 0, math.pi/2), "scale": (4, 0.03, 0.12)},
        {"name": "Baseboard_Right", "location": (5.95, 0, 0.06), "rotation": (0, 0, math.pi/2), "scale": (4, 0.03, 0.12)},
    ]
    
    for bb_info in baseboard_data:
        bpy.ops.mesh.primitive_cube_add(size=1, location=bb_info["location"])
        baseboard = bpy.context.active_object
        baseboard.name = bb_info["name"]
        baseboard.scale = bb_info["scale"]
        baseboard.rotation_euler = bb_info["rotation"]
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        
        mat = create_material(f"{bb_info['name']}_Mat", (0.88, 0.88, 0.88), roughness=0.7)
        baseboard.data.materials.append(mat)
        
        set_collection(baseboard_collection, baseboard)

def create_pillar(location, name):
    pillar_collection = create_collection("Pillars")
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=3.5, location=(location[0], location[1], 1.75))
    pillar = bpy.context.active_object
    pillar.name = name
    bpy.ops.object.shade_smooth()
    
    mat = create_material(f"{name}_Mat", (0.92, 0.92, 0.92), roughness=0.6, metallic=0.05)
    pillar.data.materials.append(mat)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=0.1, location=(location[0], location[1], 3.5))
    capital = bpy.context.active_object
    capital.name = f"{name}_Capital"
    bpy.ops.object.shade_smooth()
    capital.data.materials.append(mat)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.1, location=(location[0], location[1], 0.05))
    base = bpy.context.active_object
    base.name = f"{name}_Base"
    bpy.ops.object.shade_smooth()
    base.data.materials.append(mat)
    
    set_collection(pillar_collection, pillar)
    set_collection(pillar_collection, capital)
    set_collection(pillar_collection, base)
    
    return pillar

def create_custom_sculpture():
    sculpture_collection = create_collection("Custom_Sculpture")
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=(-2, 0, 1.2))
    sphere = bpy.context.active_object
    sphere.name = "Sculpture_Body"
    bpy.ops.object.shade_smooth()
    
    bm = bmesh.new()
    bm.from_mesh(sphere.data)
    bm.verts.ensure_lookup_table()
    
    for vert in bm.verts:
        noise = math.sin(vert.co.x * 5) * math.cos(vert.co.y * 5) * 0.05
        vert.co.z += noise
        vert.co.x *= 1.3
        vert.co.y *= 1.3
    
    bm.to_mesh(sphere.data)
    bm.free()
    sphere.data.update()
    
    mat = create_material("Sculpture_Mat", (0.82, 0.66, 0.48), roughness=0.3, metallic=0.4)
    sphere.data.materials.append(mat)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.8, location=(-2, 0, 0.4))
    stem = bpy.context.active_object
    stem.name = "Sculpture_Stem"
    bpy.ops.object.shade_smooth()
    
    stem_mat = create_material("Stem_Mat", (0.2, 0.2, 0.2), roughness=0.4, metallic=0.3)
    stem.data.materials.append(stem_mat)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.9, location=(-2, 0, 0.45))
    pedestal = bpy.context.active_object
    pedestal.name = "Sculpture_Pedestal"
    bpy.ops.object.shade_smooth()
    
    ped_mat = create_material("Pedestal_Mat", (0.95, 0.95, 0.95), roughness=0.5, metallic=0.05)
    pedestal.data.materials.append(ped_mat)
    
    set_collection(sculpture_collection, sphere)
    set_collection(sculpture_collection, stem)
    set_collection(sculpture_collection, pedestal)
    
    return sphere

def create_second_sculpture():
    sculpture_collection = create_collection("Second_Sculpture")
    
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.25, subdivisions=2, location=(2, 1.5, 1.3))
    outer = bpy.context.active_object
    outer.name = "Geometric_Outer"
    bpy.ops.object.shade_smooth()
    
    outer_mat = create_material("Geometric_Outer_Mat", (0.55, 0.55, 0.55), roughness=0.4, metallic=0.3)
    outer.data.materials.append(outer_mat)
    
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.2, subdivisions=1, location=(2, 1.5, 1.3))
    inner = bpy.context.active_object
    inner.name = "Geometric_Inner"
    bpy.ops.object.shade_smooth()
    
    inner_mat = create_material("Geometric_Inner_Mat", (0.85, 0.85, 0.85), roughness=0.5, metallic=0.2)
    inner.data.materials.append(inner_mat)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=1.0, location=(2, 1.5, 0.5))
    stem = bpy.context.active_object
    stem.name = "Geometric_Stem"
    bpy.ops.object.shade_smooth()
    
    stem_mat = create_material("Geo_Stem_Mat", (0.25, 0.25, 0.25), roughness=0.4, metallic=0.3)
    stem.data.materials.append(stem_mat)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=1.1, location=(2, 1.5, 0.55))
    pedestal = bpy.context.active_object
    pedestal.name = "Geometric_Pedestal"
    bpy.ops.object.shade_smooth()
    
    ped_mat = create_material("Geo_Pedestal_Mat", (0.92, 0.92, 0.92), roughness=0.5, metallic=0.05)
    pedestal.data.materials.append(ped_mat)
    
    set_collection(sculpture_collection, outer)
    set_collection(sculpture_collection, inner)
    set_collection(sculpture_collection, stem)
    set_collection(sculpture_collection, pedestal)
    
    return outer

def create_bench(location, rotation=0, name="Bench"):
    bench_collection = create_collection("Furniture")
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(location[0], location[1], 0.45))
    seat = bpy.context.active_object
    seat.name = f"{name}_Seat"
    seat.scale = (0.9, 0.25, 0.03)
    seat.rotation_euler = (0, 0, rotation)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    
    mat = create_material(f"{name}_Seat_Mat", (0.1, 0.1, 0.1), roughness=0.4, metallic=0.2)
    seat.data.materials.append(mat)
    
    leg_positions = [(-0.75, -0.15), (0.75, -0.15), (-0.75, 0.15), (0.75, 0.15)]
    for i, (lx, ly) in enumerate(leg_positions):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(location[0] + lx, location[1] + ly, 0.22))
        leg = bpy.context.active_object
        leg.name = f"{name}_Leg_{i}"
        leg.scale = (0.025, 0.025, 0.22)
        leg.rotation_euler = (0, 0, rotation)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        leg.data.materials.append(mat)
        set_collection(bench_collection, leg)
    
    set_collection(bench_collection, seat)
    return seat

def create_painting_frame(location, rotation, width, height, name):
    painting_collection = create_collection("Paintings")
    
    bpy.ops.mesh.primitive_plane_add(size=1, location=location)
    frame = bpy.context.active_object
    frame.name = f"{name}_Frame"
    frame.scale = (width/2 + 0.06, height/2 + 0.06, 1)
    frame.rotation_euler = rotation
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    
    frame_mat = create_material(f"{name}_Frame_Mat", (0.15, 0.15, 0.15), roughness=0.6, metallic=0.2)
    frame.data.materials.append(frame_mat)
    
    canvas_offset = 0.01
    canvas_location = (
        location[0] + math.sin(rotation[2]) * canvas_offset,
        location[1] + math.cos(rotation[2]) * canvas_offset,
        location[2]
    )
    
    bpy.ops.mesh.primitive_plane_add(size=1, location=canvas_location)
    canvas = bpy.context.active_object
    canvas.name = f"{name}_Canvas"
    canvas.scale = (width/2, height/2, 1)
    canvas.rotation_euler = rotation
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    
    colors = [
        (0.29, 0.44, 0.65), (0.18, 0.29, 0.24), (0.55, 0.29, 0.29),
        (0.24, 0.24, 0.36), (0.36, 0.29, 0.24), (0.16, 0.29, 0.36),
        (0.29, 0.24, 0.36), (0.36, 0.36, 0.24), (0.24, 0.36, 0.29),
        (0.36, 0.24, 0.24), (0.29, 0.29, 0.36), (0.36, 0.29, 0.29)
    ]
    
    canvas_mat = create_material(f"{name}_Canvas_Mat", colors[hash(name) % len(colors)], roughness=0.85)
    canvas.data.materials.append(canvas_mat)
    
    set_collection(painting_collection, frame)
    set_collection(painting_collection, canvas)
    
    return frame

def create_pedestal(location, height=0.9, name="Pedestal"):
    pedestal_collection = create_collection("Pedestals")
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(location[0], location[1], height/2))
    pedestal = bpy.context.active_object
    pedestal.name = name
    pedestal.scale = (0.25, 0.25, height/2)
    bpy.ops.object.transform_apply(scale=True)
    
    mat = create_material(f"{name}_Mat", (0.95, 0.95, 0.95), roughness=0.5, metallic=0.05)
    pedestal.data.materials.append(mat)
    
    bpy.ops.object.shade_smooth()
    set_collection(pedestal_collection, pedestal)
    
    return pedestal

def setup_lighting():
    lighting_collection = create_collection("Lighting")
    
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 3.4))
    main_light = bpy.context.active_object
    main_light.name = "Main_Light"
    main_light.data.energy = 200
    main_light.data.size = 4
    main_light.data.color = (1.0, 0.97, 0.92)
    set_collection(lighting_collection, main_light)
    
    spot_positions = [
        ((-4, 0, 3.4), "Spot_Left"),
        ((4, 0, 3.4), "Spot_Right"),
        ((0, -3, 3.4), "Spot_Back"),
        ((0, 3, 3.4), "Spot_Front"),
    ]
    
    for pos, name in spot_positions:
        bpy.ops.object.light_add(type='SPOT', location=pos)
        spot = bpy.context.active_object
        spot.name = name
        spot.data.energy = 100
        spot.data.spot_size = math.radians(60)
        spot.data.spot_blend = 0.6
        spot.data.color = (1.0, 0.98, 0.95)
        
        direction = Vector((0, 0, 0)) - Vector(pos)
        rot_quat = direction.to_track_quat('-Z', 'Y')
        spot.rotation_euler = rot_quat.to_euler()
        
        set_collection(lighting_collection, spot)

def setup_camera():
    bpy.ops.object.camera_add(location=(0, 6, 1.6))
    camera = bpy.context.active_object
    camera.name = "Gallery_Camera"
    
    direction = Vector((0, 0, 1.6)) - camera.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()
    
    camera.data.lens = 35
    camera.data.clip_end = 100
    
    bpy.context.scene.camera = camera
    
    return camera

def setup_render():
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 128
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.resolution_percentage = 100
    
    bpy.context.scene.world = bpy.data.worlds.new("Gallery_World")
    bpy.context.scene.world.use_nodes = True
    bg_node = bpy.context.scene.world.node_tree.nodes.get("Background")
    bg_node.inputs["Color"].default_value = (0.05, 0.05, 0.05, 1.0)
    bg_node.inputs["Strength"].default_value = 0.1

def export_glb(filepath):
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        use_selection=False,
        export_apply=True,
        export_cameras=True,
        export_lights=True,
        export_materials='EXPORT'
    )
    print(f"Exported to {filepath}")

def main():
    clear_scene()
    
    create_floor()
    create_ceiling()
    create_walls()
    create_baseboard()
    
    create_pillar((-3, 0), "Pillar_1")
    create_pillar((3, 0), "Pillar_2")
    
    create_custom_sculpture()
    create_second_sculpture()
    
    create_bench((0, 0), 0, "Bench_Center")
    create_bench((-4, 2), math.pi/6, "Bench_Left")
    create_bench((4, -2), -math.pi/4, "Bench_Right")
    
    painting_specs = [
        ((-6, 0, 1.6), (0, math.pi/2, 0), 1.8, 1.2, "Painting_1"),
        ((-3, -4, 1.6), (0, 0, 0), 2.0, 1.4, "Painting_2"),
        ((0, -4, 1.6), (0, 0, 0), 1.2, 1.6, "Painting_3"),
        ((3, -4, 1.6), (0, 0, 0), 1.6, 1.2, "Painting_4"),
        ((6, 0, 1.6), (0, -math.pi/2, 0), 1.4, 1.8, "Painting_5"),
        ((6, 2.5, 1.6), (0, -math.pi/2, 0), 1.6, 1.2, "Painting_6"),
        ((-6, 2.5, 1.6), (0, math.pi/2, 0), 1.8, 1.2, "Painting_7"),
        ((-3, 4, 1.6), (0, math.pi, 0), 2.0, 1.4, "Painting_8"),
        ((0, 4, 1.6), (0, math.pi, 0), 1.4, 1.8, "Painting_9"),
        ((3, 4, 1.6), (0, math.pi, 0), 1.8, 1.2, "Painting_10"),
    ]
    
    for loc, rot, w, h, name in painting_specs:
        create_painting_frame(loc, rot, w, h, name)
    
    setup_lighting()
    setup_camera()
    setup_render()
    
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
    os.makedirs(output_dir, exist_ok=True)
    
    export_path = os.path.join(output_dir, "gallery.glb")
    export_glb(export_path)
    
    blend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gallery.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    
    print(f"\nGallery scene created successfully!")
    print(f"Blender file: {blend_path}")
    print(f"GLB export: {export_path}")

if __name__ == "__main__":
    main()
