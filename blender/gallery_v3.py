"""
Gallery v3 - Direct mesh creation without transform_apply
Usage: blender --background --python gallery_v3.py
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

def make_mesh(name, verts, faces, location=(0,0,0), material=None):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    bpy.context.scene.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.shade_smooth()
    obj.select_set(False)
    if material:
        obj.data.materials.append(material)
    return obj

def cube_verts(sx, sy, sz):
    hx, hy, hz = sx/2, sy/2, sz/2
    return [(-hx,-hy,-hz),(hx,-hy,-hz),(hx,hy,-hz),(-hx,hy,-hz),
            (-hx,-hy,hz),(hx,-hy,hz),(hx,hy,hz),(-hx,hy,hz)]

cube_faces = [(0,1,2,3),(4,5,6,7),(0,1,5,4),(2,3,7,6),(0,3,7,4),(1,2,6,5)]

def plane_verts(sx, sy):
    hx, hy = sx/2, sy/2
    return [(-hx,-hy,0),(hx,-hy,0),(hx,hy,0),(-hx,hy,0)]

plane_faces = [(0,1,2,3)]

def build_room():
    floor_m = mat("Floor", (0.18, 0.16, 0.14), 0.25, 0.05)
    make_mesh("Floor", plane_verts(12, 8), plane_faces, (0,0,0), floor_m)

    ceil_m = mat("Ceiling", (0.96, 0.95, 0.93), 0.9)
    c = make_mesh("Ceiling", plane_verts(12, 8), plane_faces, (0,0,3.5), ceil_m)
    c.rotation_euler = (math.pi, 0, 0)

    wall_m = mat("Wall", (0.92, 0.90, 0.87), 0.88)
    make_mesh("Wall_N", cube_verts(12, 0.1, 3.5), cube_faces, (0, -4, 1.75), wall_m)
    make_mesh("Wall_S", cube_verts(12, 0.1, 3.5), cube_faces, (0, 4, 1.75), wall_m)
    make_mesh("Wall_W", cube_verts(0.1, 8, 3.5), cube_faces, (-6, 0, 1.75), wall_m)
    make_mesh("Wall_E", cube_verts(0.1, 8, 3.5), cube_faces, (6, 0, 1.75), wall_m)

    bb_m = mat("Baseboard", (0.88, 0.86, 0.83), 0.7)
    make_mesh("BB_N", cube_verts(11.8, 0.03, 0.16), cube_faces, (0, -3.94, 0.08), bb_m)
    make_mesh("BB_S", cube_verts(11.8, 0.03, 0.16), cube_faces, (0, 3.94, 0.08), bb_m)
    make_mesh("BB_W", cube_verts(0.03, 7.8, 0.16), cube_faces, (-5.94, 0, 0.08), bb_m)
    make_mesh("BB_E", cube_verts(0.03, 7.8, 0.16), cube_faces, (5.94, 0, 0.08), bb_m)

    crown_m = mat("Crown", (0.90, 0.88, 0.85), 0.75)
    make_mesh("Crown_N", cube_verts(11.8, 0.04, 0.08), cube_faces, (0, -3.92, 3.42), crown_m)
    make_mesh("Crown_S", cube_verts(11.8, 0.04, 0.08), cube_faces, (0, 3.92, 3.42), crown_m)
    make_mesh("Crown_W", cube_verts(0.04, 7.8, 0.08), cube_faces, (-5.92, 0, 3.42), crown_m)
    make_mesh("Crown_E", cube_verts(0.04, 7.8, 0.08), cube_faces, (5.92, 0, 3.42), crown_m)

def build_pillars():
    p_m = mat("Pillar", (0.91, 0.89, 0.86), 0.55, 0.02)
    r_m = mat("Ring", (0.55, 0.42, 0.28), 0.3, 0.6)
    for x in [-3, 3]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=3.34, location=(x, 0, 1.67))
        s = bpy.context.active_object
        s.name = f"P{x}_Shaft"
        bpy.ops.object.shade_smooth()
        s.data.materials.append(p_m)

        bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=0.08, location=(x, 0, 3.38))
        cap = bpy.context.active_object
        cap.name = f"P{x}_Cap"
        bpy.ops.object.shade_smooth()
        cap.data.materials.append(p_m)

        bpy.ops.mesh.primitive_cylinder_add(radius=0.16, depth=0.06, location=(x, 0, 0.03))
        base = bpy.context.active_object
        base.name = f"P{x}_Base"
        bpy.ops.object.shade_smooth()
        base.data.materials.append(p_m)

        bpy.ops.mesh.primitive_torus_add(major_radius=0.14, minor_radius=0.015, location=(x, 0, 3.32))
        ring = bpy.context.active_object
        ring.name = f"P{x}_Ring"
        bpy.ops.object.shade_smooth()
        ring.data.materials.append(r_m)

def build_sculptures():
    bronze = mat("Bronze", (0.55, 0.42, 0.28), 0.28, 0.65)
    obsidian = mat("Obsidian", (0.08, 0.08, 0.09), 0.15, 0.8)
    marble_m = mat("Marble", (0.92, 0.90, 0.88), 0.4, 0.1)
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

    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.6, location=(-2, 0, 0.7))
    stem = bpy.context.active_object
    stem.name = "Abs_Stem"
    bpy.ops.object.shade_smooth()
    stem.data.materials.append(obsidian)

    make_mesh("Abs_Ped", cube_verts(0.44, 0.44, 0.9), cube_faces, (-2, 0, 0.45), ped_m)
    make_mesh("Abs_Cap", cube_verts(0.48, 0.48, 0.02), cube_faces, (-2, 0, 0.91), ped_m)

    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.28, subdivisions=2, location=(2, 1.5, 1.4))
    geo_out = bpy.context.active_object
    geo_out.name = "Geo_Outer"
    bpy.ops.object.shade_smooth()
    geo_out.data.materials.append(obsidian)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=(2, 1.5, 1.4))
    geo_in = bpy.context.active_object
    geo_in.name = "Geo_Inner"
    bpy.ops.object.shade_smooth()
    geo_in.data.materials.append(marble_m)

    bpy.ops.mesh.primitive_torus_add(major_radius=0.35, minor_radius=0.008, location=(2, 1.5, 1.4), rotation=(0.3, 0.5, 0))
    orbit = bpy.context.active_object
    orbit.name = "Geo_Orbit"
    bpy.ops.object.shade_smooth()
    orbit.data.materials.append(gold_m)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.85, location=(2, 1.5, 0.55))
    g_stem = bpy.context.active_object
    g_stem.name = "Geo_Stem"
    bpy.ops.object.shade_smooth()
    g_stem.data.materials.append(obsidian)

    make_mesh("Geo_Ped", cube_verts(0.44, 0.44, 1.1), cube_faces, (2, 1.5, 0.55), ped_m)
    make_mesh("Geo_Cap", cube_verts(0.48, 0.48, 0.02), cube_faces, (2, 1.5, 1.11), ped_m)

def build_benches():
    leather = mat("Leather", (0.12, 0.11, 0.10), 0.65)
    metal = mat("Metal", (0.15, 0.14, 0.13), 0.35, 0.7)
    for bx, by, n in [(0, 0, "C"), (-4.5, 2, "W"), (4.5, -2, "E")]:
        make_mesh(f"Bench_{n}_Seat", cube_verts(1.7, 0.44, 0.05), cube_faces, (bx, by, 0.46), leather)
        for lx, ly in [(-0.7,-0.15),(0.7,-0.15),(-0.7,0.15),(0.7,0.15)]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.012, depth=0.46, location=(bx+lx, by+ly, 0.23))
            leg = bpy.context.active_object
            leg.name = f"Bench_{n}_Leg"
            bpy.ops.object.shade_smooth()
            leg.data.materials.append(metal)

def build_painting(px, py, pz, ry, w, h, name, img_file, frame_m):
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
        make_mesh(f"{name}_F_{dx}_{dy}", cube_verts(dsx, dsy, dsz), cube_faces, (px+rx, py+ry_off, pz+fd/2), frame_m)

    make_mesh(f"{name}_Mat", cube_verts(w+0.08, h+0.08, 0.005), cube_faces, (px, py, pz-0.001), mat(f"{name}_Mat_M", (0.94, 0.91, 0.85), 0.95))

    canvas_m = mat(f"{name}_Canvas_M", (0.9, 0.88, 0.85), 0.85)
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public", "textures", "paintings", img_file)
    add_img(canvas_m, img_path)

    cv = plane_verts(w, h)
    rotated_cv = []
    for v in cv:
        rx = v[0] * math.cos(ry) - v[1] * math.sin(ry)
        ry_off = v[0] * math.sin(ry) + v[1] * math.cos(ry)
        rotated_cv.append((px+rx, py+ry_off, pz+0.005))
    canvas = make_mesh(f"{name}_Canvas", rotated_cv, plane_faces, (0,0,0), canvas_m)
    canvas.location = (0, 0, 0)

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
            make_mesh(f"{n}_F_{dx}_{dy}", cube_verts(dsx, dsy, dsz), cube_faces, (wx+rx, wy+ry_off, 2.2), frame_m)

        gv = plane_verts(2.4, 2.0)
        rotated_gv = []
        for v in gv:
            grx = v[0] * math.cos(ry) - v[1] * math.sin(ry)
            gry = v[0] * math.sin(ry) + v[1] * math.cos(ry)
            rotated_gv.append((wx+grx, wy+gry, 2.2))
        make_mesh(f"{n}_Glass", rotated_gv, plane_faces, (0,0,0), glass_m)

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
    print("BUILDING GALLERY v3")
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
        filepath=os.path.join(out, "gallery_v3.glb"),
        export_format='GLB', use_selection=False, export_apply=True,
        export_cameras=True, export_lights=True, export_materials='EXPORT'
    )
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), "gallery_v3.blend"))
    print("DONE")

if __name__ == "__main__":
    main()
