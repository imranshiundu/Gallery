"""
Final Gallery Scene - Complete rebuild with proper positions
Usage: blender --background --python gallery_final.py
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for c in bpy.data.collections:
        bpy.data.collections.remove(c)
    for m in bpy.data.materials:
        bpy.data.materials.remove(m)

def mat(name, color, roughness=0.5, metallic=0.0):
    m = bpy.data.materials.new(name=name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return m

def add_img_texture(mat_obj, img_path, obj_name):
    if not os.path.exists(img_path):
        return
    img = bpy.data.images.load(img_path)
    nodes = mat_obj.node_tree.nodes
    links = mat_obj.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    tex = nodes.new('ShaderNodeTexImage')
    tex.image = img
    tex.location = (-600, 0)
    links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])

def make_cube(name, loc, scale, rot=(0,0,0), material=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    obj.rotation_euler = rot
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    if material:
        obj.data.materials.append(material)
    return obj

def make_cyl(name, loc, radius, depth, material=None, verts=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=loc, vertices=verts)
    obj = bpy.context.active_object
    obj.name = name
    bpy.ops.object.shade_smooth()
    if material:
        obj.data.materials.append(material)
    return obj

def make_plane(name, loc, scale, rot=(0,0,0), material=None):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    obj.rotation_euler = rot
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    if material:
        obj.data.materials.append(material)
    return obj

def build_room():
    coll = bpy.data.collections.new("Room")
    bpy.context.scene.collection.children.link(coll)

    floor_mat = mat("Floor", (0.18, 0.16, 0.14), roughness=0.25, metallic=0.05)
    make_plane("Floor", (0,0,0), (6,4,1), material=floor_mat)

    ceil_mat = mat("Ceiling", (0.96, 0.95, 0.93), roughness=0.9)
    make_plane("Ceiling", (0,0,3.5), (6,4,1), rot=(math.pi,0,0), material=ceil_mat)

    wall_mat = mat("Wall", (0.92, 0.90, 0.87), roughness=0.88)
    make_cube("Wall_N", (0,-4,1.75), (6,0.1,3.5), material=wall_mat)
    make_cube("Wall_S", (0,4,1.75), (6,0.1,3.5), material=wall_mat)
    make_cube("Wall_W", (-6,0,1.75), (0.1,8,3.5), material=wall_mat)
    make_cube("Wall_E", (6,0,1.75), (0.1,8,3.5), material=wall_mat)

    bb_mat = mat("Baseboard", (0.88, 0.86, 0.83), roughness=0.7)
    make_cube("BB_N", (0,-3.94,0.08), (5.9,0.03,0.16), material=bb_mat)
    make_cube("BB_S", (0,3.94,0.08), (5.9,0.03,0.16), material=bb_mat)
    make_cube("BB_W", (-5.94,0,0.08), (0.03,7.9,0.16), material=bb_mat)
    make_cube("BB_E", (5.94,0,0.08), (0.03,7.9,0.16), material=bb_mat)

    crown_mat = mat("Crown", (0.90, 0.88, 0.85), roughness=0.75)
    make_cube("Crown_N", (0,-3.92,3.42), (5.9,0.04,0.08), material=crown_mat)
    make_cube("Crown_S", (0,3.92,3.42), (5.9,0.04,0.08), material=crown_mat)
    make_cube("Crown_W", (-5.92,0,3.42), (0.04,7.9,0.08), material=crown_mat)
    make_cube("Crown_E", (5.92,0,3.42), (0.04,7.9,0.08), material=crown_mat)

    for obj in coll.objects:
        for c in obj.users_collection:
            c.objects.unlink(obj)
        bpy.context.scene.collection.objects.unlink(obj)
        coll.objects.link(obj)

def build_pillars():
    coll = bpy.data.collections.new("Pillars")
    bpy.context.scene.collection.children.link(coll)
    p_mat = mat("Pillar", (0.91, 0.89, 0.86), roughness=0.55, metallic=0.02)
    ring_mat = mat("Ring", (0.55, 0.42, 0.28), roughness=0.3, metallic=0.6)

    for x in [-3, 3]:
        make_cyl(f"P{x}_Shaft", (x,0,1.67), 0.12, 3.34, p_mat)
        make_cyl(f"P{x}_Cap", (x,0,3.38), 0.18, 0.08, p_mat)
        make_cyl(f"P{x}_Base", (x,0,0.03), 0.16, 0.06, p_mat)
        bpy.ops.mesh.primitive_torus_add(major_radius=0.14, minor_radius=0.015, location=(x,0,3.32))
        r = bpy.context.active_object
        r.name = f"P{x}_Ring"
        bpy.ops.object.shade_smooth()
        r.data.materials.append(ring_mat)
        coll.objects.link(r)

def build_sculptures():
    coll = bpy.data.collections.new("Sculptures")
    bpy.context.scene.collection.children.link(coll)

    bronze = mat("Bronze", (0.55, 0.42, 0.28), roughness=0.28, metallic=0.65)
    obsidian = mat("Obsidian", (0.08, 0.08, 0.09), roughness=0.15, metallic=0.8)
    marble = mat("Marble", (0.92, 0.90, 0.88), roughness=0.4, metallic=0.1)
    gold = mat("Gold", (0.72, 0.58, 0.32), roughness=0.25, metallic=0.7)
    pedestal = mat("Pedestal", (0.94, 0.93, 0.91), roughness=0.45, metallic=0.02)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.35, segments=48, ring_count=24, location=(-2,0,1.35))
    body = bpy.context.active_object
    body.name = "Abstract_Body"
    bm = bmesh.new()
    bm.from_mesh(body.data)
    bm.verts.ensure_lookup_table()
    for v in bm.verts:
        x, y, z = v.co
        angle = math.atan2(y, x)
        r = math.sqrt(x**2 + y**2)
        twist = math.sin(z*4 + angle*2) * 0.08
        stretch = 1.0 + math.sin(z*3) * 0.15
        wave = math.sin(angle*3 + z*2) * 0.04
        v.co.x = (r + wave) * math.cos(angle + twist) * 1.2
        v.co.y = (r + wave) * math.sin(angle + twist) * 1.2
        v.co.z = z * stretch
    bm.to_mesh(body.data)
    bm.free()
    body.data.update()
    bpy.ops.object.shade_smooth()
    body.data.materials.append(bronze)

    make_cyl("Abs_Stem", (-2,0,0.7), 0.04, 0.6, obsidian, 24)
    make_cube("Abs_Ped", (-2,0,0.45), (0.44,0.44,0.9), material=pedestal)
    make_cube("Abs_Cap", (-2,0,0.91), (0.48,0.48,0.02), material=pedestal)

    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.28, subdivisions=2, location=(2,1.5,1.4))
    geo_out = bpy.context.active_object
    geo_out.name = "Geo_Outer"
    bpy.ops.object.shade_smooth()
    geo_out.data.materials.append(obsidian)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, segments=32, ring_count=16, location=(2,1.5,1.4))
    geo_in = bpy.context.active_object
    geo_in.name = "Geo_Inner"
    bpy.ops.object.shade_smooth()
    geo_in.data.materials.append(marble)

    bpy.ops.mesh.primitive_torus_add(major_radius=0.35, minor_radius=0.008, location=(2,1.5,1.4), rotation=(0.3,0.5,0))
    orbit = bpy.context.active_object
    orbit.name = "Geo_Orbit"
    bpy.ops.object.shade_smooth()
    orbit.data.materials.append(gold)

    make_cyl("Geo_Stem", (2,1.5,0.55), 0.03, 0.85, obsidian, 24)
    make_cube("Geo_Ped", (2,1.5,0.55), (0.44,0.44,1.1), material=pedestal)
    make_cube("Geo_Cap", (2,1.5,1.11), (0.48,0.48,0.02), material=pedestal)

def build_benches():
    coll = bpy.data.collections.new("Furniture")
    bpy.context.scene.collection.children.link(coll)
    leather = mat("Leather", (0.12, 0.11, 0.10), roughness=0.65)
    metal = mat("Metal", (0.15, 0.14, 0.13), roughness=0.35, metallic=0.7)

    for bx, by, rot, name in [(0,0,0,"Center"), (-4.5,2,math.pi/8,"West"), (4.5,-2,-math.pi/6,"East")]:
        make_cube(f"Bench_{name}_Seat", (bx,by,0.46), (1.7,0.44,0.05), rot=(0,0,rot), material=leather)
        for lx, ly in [(-0.7,-0.15),(0.7,-0.15),(-0.7,0.15),(0.7,0.15)]:
            make_cyl(f"Bench_{name}_Leg", (bx+lx,by+ly,0.23), 0.012, 0.46, metal, 12)

def build_painting(loc, rot, w, h, name, img_file, frame_mat_obj):
    coll = bpy.data.collections.new("Paintings")
    bpy.context.scene.collection.children.link(coll)

    fw, fd = 0.04, 0.025

    for dx, dy, ds in [((w/2+fw/2),0,(fw,h,fd)), ((-w/2-fw/2),0,(fw,h,fd)), (0,(h/2+fw/2),(w+fw*2,fw,fd)), (0,(-h/2-fw/2),(w+fw*2,fw,fd))]:
        rx = dx * math.cos(rot[2]) - dy * math.sin(rot[2])
        ry = dx * math.sin(rot[2]) + dy * math.cos(rot[2])
        make_cube(f"{name}_Frame", (loc[0]+rx, loc[1]+ry, loc[2]+fd/2), ds, rot=rot, material=frame_mat_obj)

    make_plane(f"{name}_Mat", (loc[0], loc[1], loc[2]-0.001), (w/2+0.04, h/2+0.04, 1), rot=rot, material=mat(f"{name}_Mat_M", (0.94, 0.91, 0.85), roughness=0.95))

    canvas = make_plane(f"{name}_Canvas", (loc[0], loc[1], loc[2]+0.005), (w/2, h/2, 1), rot=rot)
    canvas_mat = mat(f"{name}_Canvas_M", (0.9, 0.88, 0.85), roughness=0.85)
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public", "textures", "paintings", img_file)
    add_img_texture(canvas_mat, img_path, name)
    canvas.data.materials.append(canvas_mat)

def build_paintings():
    frame_dark = mat("Frame_Dark", (0.20, 0.20, 0.20), roughness=0.5, metallic=0.15)
    frame_gilt = mat("Frame_Gilt", (0.72, 0.58, 0.32), roughness=0.5, metallic=0.6)
    frame_wood = mat("Frame_Wood", (0.18, 0.12, 0.08), roughness=0.6, metallic=0.15)

    specs = [
        ((-5.94,0,1.6), (0,math.pi/2,0), 1.6, 1.1, "Art_W1", "painting_01.jpg", frame_gilt),
        ((-5.94,-2.5,1.65), (0,math.pi/2,0), 1.2, 0.9, "Art_W2", "painting_02.jpg", frame_dark),
        ((-5.94,2.5,1.6), (0,math.pi/2,0), 1.8, 1.2, "Art_W3", "painting_03.jpg", frame_wood),
        ((-3,-3.94,1.65), (0,0,0), 1.4, 1.0, "Art_N1", "painting_04.jpg", frame_dark),
        ((0,-3.94,1.6), (0,0,0), 1.0, 1.4, "Art_N2", "painting_05.jpg", frame_gilt),
        ((3,-3.94,1.65), (0,0,0), 1.6, 1.1, "Art_N3", "painting_06.jpg", frame_wood),
        ((5.94,0,1.65), (0,-math.pi/2,0), 1.4, 1.0, "Art_E1", "painting_07.jpg", frame_wood),
        ((5.94,2.5,1.6), (0,-math.pi/2,0), 1.2, 1.6, "Art_E2", "painting_08.jpg", frame_gilt),
        ((-3,3.94,1.6), (0,math.pi,0), 1.6, 1.1, "Art_S1", "painting_09.jpg", frame_dark),
        ((0,3.94,1.65), (0,math.pi,0), 1.0, 1.4, "Art_S2", "painting_10.jpg", frame_wood),
        ((3,3.94,1.6), (0,math.pi,0), 1.8, 1.2, "Art_S3", "painting_11.jpg", frame_gilt),
    ]
    for loc, rot, w, h, name, img, fm in specs:
        build_painting(loc, rot, w, h, name, img, fm)

def build_windows():
    coll = bpy.data.collections.new("Windows")
    bpy.context.scene.collection.children.link(coll)
    frame = mat("Win_Frame", (0.1, 0.1, 0.1), roughness=0.2, metallic=0.8)
    glass = mat("Glass", (0.6, 0.8, 1.0), roughness=0.0)
    glass.node_tree.nodes.get("Principled BSDF").inputs["Alpha"].default_value = 0.3

    for wx, wy, rot, name in [(-2,3.94,math.pi,"Win_S1"), (2,3.94,math.pi,"Win_S2"), (-5.94,0,math.pi/2,"Win_W1")]:
        for dx, dy, ds in [(0,1.0,(5.0,0.08,0.08)), (0,-1.0,(5.0,0.08,0.08)), (-1.25,0,(0.08,0.08,2.0)), (1.25,0,(0.08,0.08,2.0)), (0,0,(0.06,0.06,2.0))]:
            rx = dx * math.cos(rot) - dy * math.sin(rot)
            ry = dx * math.sin(rot) + dy * math.cos(rot)
            make_cube(f"{name}_Frame", (wx+rx, wy+ry, 2.2), ds, rot=(0,0,rot), material=frame)
        make_plane(f"{name}_Glass", (wx, wy, 2.2), (1.2, 1.0, 1), rot=(0,0,rot), material=glass)

def setup_lighting():
    coll = bpy.data.collections.new("Lighting")
    bpy.context.scene.collection.children.link(coll)

    bpy.ops.object.light_add(type='AREA', location=(0,0,3.4))
    fill = bpy.context.active_object
    fill.name = "Area_Fill"
    fill.data.energy = 200
    fill.data.size = 5
    fill.data.color = (1.0, 0.97, 0.92)
    coll.objects.link(fill)

    spots = [
        ((-4,0,3.3), (-6,0,1.6), 120, "Spot_W1"),
        ((-4,-2.5,3.3), (-6,-2.5,1.65), 100, "Spot_W2"),
        ((-4,2.5,3.3), (-6,2.5,1.6), 100, "Spot_W3"),
        ((4,0,3.3), (6,0,1.65), 120, "Spot_E1"),
        ((4,2.5,3.3), (6,2.5,1.6), 100, "Spot_E2"),
        ((-2,-2.5,3.3), (-3,-3.94,1.65), 100, "Spot_N1"),
        ((0,-2.5,3.3), (0,-3.94,1.6), 100, "Spot_N2"),
        ((2,-2.5,3.3), (3,-3.94,1.65), 100, "Spot_N3"),
        ((-2,2.5,3.3), (-3,3.94,1.6), 100, "Spot_S1"),
        ((0,2.5,3.3), (0,3.94,1.65), 100, "Spot_S2"),
        ((2,2.5,3.3), (3,3.94,1.6), 100, "Spot_S3"),
        ((-2,0.5,3.3), (-2,0,1.35), 80, "Spot_Sculpt1"),
        ((3,2,3.3), (2,1.5,1.4), 80, "Spot_Sculpt2"),
    ]
    for pos, target, energy, name in spots:
        bpy.ops.object.light_add(type='SPOT', location=pos)
        s = bpy.context.active_object
        s.name = name
        s.data.energy = energy
        s.data.spot_size = math.radians(45)
        s.data.spot_blend = 0.65
        s.data.color = (1.0, 0.97, 0.92)
        direction = Vector(target) - Vector(pos)
        s.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
        coll.objects.link(s)

def main():
    print("\n" + "="*50)
    print("BUILDING FINAL GALLERY")
    print("="*50)

    clear_scene()
    build_room()
    build_pillars()
    build_sculptures()
    build_benches()
    build_paintings()
    build_windows()
    setup_lighting()

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
    os.makedirs(output_dir, exist_ok=True)
    export_path = os.path.join(output_dir, "gallery_final.glb")
    bpy.ops.export_scene.gltf(
        filepath=export_path,
        export_format='GLB',
        use_selection=False,
        export_apply=True,
        export_cameras=True,
        export_lights=True,
        export_materials='EXPORT'
    )
    print(f"Exported: {export_path}")

    blend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gallery_final.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Saved: {blend_path}")

if __name__ == "__main__":
    main()
