"""
Gallery v2 - Fixed position issue
Usage: blender --background --python gallery_v2.py
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

def add_img(mat_obj, img_path):
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

def cube(name, x, y, z, sx, sy, sz, material=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
    o = bpy.context.active_object
    o.name = name
    o.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    if material:
        o.data.materials.append(material)
    return o

def cyl(name, x, y, z, r, d, material=None, v=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=(x, y, z), vertices=v)
    o = bpy.context.active_object
    o.name = name
    bpy.ops.object.shade_smooth()
    if material:
        o.data.materials.append(material)
    return o

def plane(name, x, y, z, sx, sy, material=None, rx=0, ry=0, rz=0):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y, z), rotation=(rx, ry, rz))
    o = bpy.context.active_object
    o.name = name
    o.scale = (sx, sy, 1)
    bpy.ops.object.transform_apply(scale=True)
    if material:
        o.data.materials.append(material)
    return o

def build_room():
    floor_m = mat("Floor", (0.18, 0.16, 0.14), 0.25, 0.05)
    plane("Floor", 0, 0, 0, 6, 4, floor_m)

    ceil_m = mat("Ceiling", (0.96, 0.95, 0.93), 0.9)
    plane("Ceiling", 0, 0, 3.5, 6, 4, ceil_m, rx=math.pi)

    wall_m = mat("Wall", (0.92, 0.90, 0.87), 0.88)
    cube("Wall_N", 0, -4, 1.75, 6, 0.1, 3.5, wall_m)
    cube("Wall_S", 0, 4, 1.75, 6, 0.1, 3.5, wall_m)
    cube("Wall_W", -6, 0, 1.75, 0.1, 8, 3.5, wall_m)
    cube("Wall_E", 6, 0, 1.75, 0.1, 8, 3.5, wall_m)

    bb_m = mat("Baseboard", (0.88, 0.86, 0.83), 0.7)
    cube("BB_N", 0, -3.94, 0.08, 5.9, 0.03, 0.16, bb_m)
    cube("BB_S", 0, 3.94, 0.08, 5.9, 0.03, 0.16, bb_m)
    cube("BB_W", -5.94, 0, 0.08, 0.03, 7.9, 0.16, bb_m)
    cube("BB_E", 5.94, 0, 0.08, 0.03, 7.9, 0.16, bb_m)

    crown_m = mat("Crown", (0.90, 0.88, 0.85), 0.75)
    cube("Crown_N", 0, -3.92, 3.42, 5.9, 0.04, 0.08, crown_m)
    cube("Crown_S", 0, 3.92, 3.42, 5.9, 0.04, 0.08, crown_m)
    cube("Crown_W", -5.92, 0, 3.42, 0.04, 7.9, 0.08, crown_m)
    cube("Crown_E", 5.92, 0, 3.42, 0.04, 7.9, 0.08, crown_m)

def build_pillars():
    p_m = mat("Pillar", (0.91, 0.89, 0.86), 0.55, 0.02)
    r_m = mat("Ring", (0.55, 0.42, 0.28), 0.3, 0.6)
    for x in [-3, 3]:
        cyl(f"P{x}_Shaft", x, 0, 1.67, 0.12, 3.34, p_m)
        cyl(f"P{x}_Cap", x, 0, 3.38, 0.18, 0.08, p_m)
        cyl(f"P{x}_Base", x, 0, 0.03, 0.16, 0.06, p_m)
        bpy.ops.mesh.primitive_torus_add(major_radius=0.14, minor_radius=0.015, location=(x, 0, 3.32))
        r = bpy.context.active_object
        r.name = f"P{x}_Ring"
        bpy.ops.object.shade_smooth()
        r.data.materials.append(r_m)

def build_sculptures():
    bronze = mat("Bronze", (0.55, 0.42, 0.28), 0.28, 0.65)
    obsidian = mat("Obsidian", (0.08, 0.08, 0.09), 0.15, 0.8)
    marble = mat("Marble", (0.92, 0.90, 0.88), 0.4, 0.1)
    gold_m = mat("Gold", (0.72, 0.58, 0.32), 0.25, 0.7)
    ped_m = mat("Pedestal", (0.94, 0.93, 0.91), 0.45, 0.02)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.35, segments=48, ring_count=24, location=(-2, 0, 1.35))
    body = bpy.context.active_object
    body.name = "Abstract_Body"
    bm = bmesh.new()
    bm.from_mesh(body.data)
    bm.verts.ensure_lookup_table()
    for v in bm.verts:
        x, y, z = v.co
        a = math.atan2(y, x)
        r = math.sqrt(x**2 + y**2)
        twist = math.sin(z*4 + a*2) * 0.08
        stretch = 1.0 + math.sin(z*3) * 0.15
        wave = math.sin(a*3 + z*2) * 0.04
        v.co.x = (r + wave) * math.cos(a + twist) * 1.2
        v.co.y = (r + wave) * math.sin(a + twist) * 1.2
        v.co.z = z * stretch
    bm.to_mesh(body.data)
    bm.free()
    body.data.update()
    bpy.ops.object.shade_smooth()
    body.data.materials.append(bronze)

    cyl("Abs_Stem", -2, 0, 0.7, 0.04, 0.6, obsidian, 24)
    cube("Abs_Ped", -2, 0, 0.45, 0.44, 0.44, 0.9, ped_m)
    cube("Abs_Cap", -2, 0, 0.91, 0.48, 0.48, 0.02, ped_m)

    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.28, subdivisions=2, location=(2, 1.5, 1.4))
    geo_out = bpy.context.active_object
    geo_out.name = "Geo_Outer"
    bpy.ops.object.shade_smooth()
    geo_out.data.materials.append(obsidian)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, segments=32, ring_count=16, location=(2, 1.5, 1.4))
    geo_in = bpy.context.active_object
    geo_in.name = "Geo_Inner"
    bpy.ops.object.shade_smooth()
    geo_in.data.materials.append(marble)

    bpy.ops.mesh.primitive_torus_add(major_radius=0.35, minor_radius=0.008, location=(2, 1.5, 1.4), rotation=(0.3, 0.5, 0))
    orbit = bpy.context.active_object
    orbit.name = "Geo_Orbit"
    bpy.ops.object.shade_smooth()
    orbit.data.materials.append(gold_m)

    cyl("Geo_Stem", 2, 1.5, 0.55, 0.03, 0.85, obsidian, 24)
    cube("Geo_Ped", 2, 1.5, 0.55, 0.44, 0.44, 1.1, ped_m)
    cube("Geo_Cap", 2, 1.5, 1.11, 0.48, 0.48, 0.02, ped_m)

def build_benches():
    leather = mat("Leather", (0.12, 0.11, 0.10), 0.65)
    metal = mat("Metal", (0.15, 0.14, 0.13), 0.35, 0.7)
    for bx, by, r, n in [(0,0,0,"C"), (-4.5,2,math.pi/8,"W"), (4.5,-2,-math.pi/6,"E")]:
        cube(f"Bench_{n}_Seat", bx, by, 0.46, 1.7, 0.44, 0.05, leather)
        for lx, ly in [(-0.7,-0.15),(0.7,-0.15),(-0.7,0.15),(0.7,0.15)]:
            cyl(f"Bench_{n}_Leg_{lx}_{ly}", bx+lx, by+ly, 0.23, 0.012, 0.46, metal, 12)

def build_painting(px, py, pz, ry, w, h, name, img_file, frame_mat):
    fw = 0.04
    fd = 0.025

    for dx, dy, dsx, dsy, dsz in [
        (w/2+fw/2, 0, fw, h, fd),
        (-w/2-fw/2, 0, fw, h, fd),
        (0, h/2+fw/2, w+fw*2, fw, fd),
        (0, -h/2-fw/2, w+fw*2, fw, fd)
    ]:
        rx = dx * math.cos(ry) - dy * math.sin(ry)
        ry_off = dx * math.sin(ry) + dy * math.cos(ry)
        cube(f"{name}_Frame_{dx}_{dy}", px+rx, py+ry_off, pz+fd/2, dsx, dsy, dsz, frame_mat)

    cube(f"{name}_Mat", px, py, pz-0.001, w+0.08, h+0.08, 0.005, mat(f"{name}_Mat_M", (0.94, 0.91, 0.85), 0.95))

    canvas_m = mat(f"{name}_Canvas_M", (0.9, 0.88, 0.85), 0.85)
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public", "textures", "paintings", img_file)
    add_img(canvas_m, img_path)
    plane(f"{name}_Canvas", px, py, pz+0.005, w/2, h/2, canvas_m, ry=ry)

def build_paintings():
    f_dark = mat("F_Dark", (0.20, 0.20, 0.20), 0.5, 0.15)
    f_gilt = mat("F_Gilt", (0.72, 0.58, 0.32), 0.5, 0.6)
    f_wood = mat("F_Wood", (0.18, 0.12, 0.08), 0.6, 0.15)

    specs = [
        (-5.94, 0, 1.6, math.pi/2, 1.6, 1.1, "Art_W1", "painting_01.jpg", f_gilt),
        (-5.94, -2.5, 1.65, math.pi/2, 1.2, 0.9, "Art_W2", "painting_02.jpg", f_dark),
        (-5.94, 2.5, 1.6, math.pi/2, 1.8, 1.2, "Art_W3", "painting_03.jpg", f_wood),
        (-3, -3.94, 1.65, 0, 1.4, 1.0, "Art_N1", "painting_04.jpg", f_dark),
        (0, -3.94, 1.6, 0, 1.0, 1.4, "Art_N2", "painting_05.jpg", f_gilt),
        (3, -3.94, 1.65, 0, 1.6, 1.1, "Art_N3", "painting_06.jpg", f_wood),
        (5.94, 0, 1.65, -math.pi/2, 1.4, 1.0, "Art_E1", "painting_07.jpg", f_wood),
        (5.94, 2.5, 1.6, -math.pi/2, 1.2, 1.6, "Art_E2", "painting_08.jpg", f_gilt),
        (-3, 3.94, 1.6, math.pi, 1.6, 1.1, "Art_S1", "painting_09.jpg", f_dark),
        (0, 3.94, 1.65, math.pi, 1.0, 1.4, "Art_S2", "painting_10.jpg", f_wood),
        (3, 3.94, 1.6, math.pi, 1.8, 1.2, "Art_S3", "painting_11.jpg", f_gilt),
    ]
    for px, py, pz, ry, w, h, name, img, fm in specs:
        build_painting(px, py, pz, ry, w, h, name, img, fm)

def build_windows():
    frame_m = mat("WFrame", (0.1, 0.1, 0.1), 0.2, 0.8)
    glass_m = mat("Glass", (0.6, 0.8, 1.0), 0.0)
    glass_m.node_tree.nodes.get("Principled BSDF").inputs["Alpha"].default_value = 0.3

    for wx, wy, ry, n in [(-2, 3.94, math.pi, "WS1"), (2, 3.94, math.pi, "WS2"), (-5.94, 0, math.pi/2, "WW1")]:
        for dx, dy, dsx, dsy, dsz in [(0, 1.0, 5.0, 0.08, 0.08), (0, -1.0, 5.0, 0.08, 0.08),
                                       (-1.25, 0, 0.08, 0.08, 2.0), (1.25, 0, 0.08, 0.08, 2.0),
                                       (0, 0, 0.06, 0.06, 2.0)]:
            rx = dx * math.cos(ry) - dy * math.sin(ry)
            ry_off = dx * math.sin(ry) + dy * math.cos(ry)
            cube(f"{n}_F_{dx}_{dy}", wx+rx, wy+ry_off, 2.2, dsx, dsy, dsz, frame_m)
        plane(f"{n}_Glass", wx, wy, 2.2, 1.2, 1.0, glass_m, ry=ry)

def setup_lighting():
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 3.4))
    fill = bpy.context.active_object
    fill.name = "Fill"
    fill.data.energy = 200
    fill.data.size = 5
    fill.data.color = (1.0, 0.97, 0.92)

    spots = [
        (-4, 0, 3.3, -6, 0, 1.6, 120),
        (-4, -2.5, 3.3, -6, -2.5, 1.65, 100),
        (-4, 2.5, 3.3, -6, 2.5, 1.6, 100),
        (4, 0, 3.3, 6, 0, 1.65, 120),
        (4, 2.5, 3.3, 6, 2.5, 1.6, 100),
        (-2, -2.5, 3.3, -3, -3.94, 1.65, 100),
        (0, -2.5, 3.3, 0, -3.94, 1.6, 100),
        (2, -2.5, 3.3, 3, -3.94, 1.65, 100),
        (-2, 2.5, 3.3, -3, 3.94, 1.6, 100),
        (0, 2.5, 3.3, 0, 3.94, 1.65, 100),
        (2, 2.5, 3.3, 3, 3.94, 1.6, 100),
    ]
    for sx, sy, sz, tx, ty, tz, e in spots:
        bpy.ops.object.light_add(type='SPOT', location=(sx, sy, sz))
        s = bpy.context.active_object
        s.data.energy = e
        s.data.spot_size = math.radians(45)
        s.data.spot_blend = 0.65
        s.data.color = (1.0, 0.97, 0.92)
        d = Vector((tx, ty, tz)) - Vector((sx, sy, sz))
        s.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

def main():
    print("\nBUILDING GALLERY v2")
    clear_scene()
    build_room()
    build_pillars()
    build_sculptures()
    build_benches()
    build_paintings()
    build_windows()
    setup_lighting()

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
    os.makedirs(out, exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=os.path.join(out, "gallery_v2.glb"),
        export_format='GLB', use_selection=False, export_apply=True,
        export_cameras=True, export_lights=True, export_materials='EXPORT'
    )
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), "gallery_v2.blend"))
    print("DONE")

if __name__ == "__main__":
    main()
