"""
Gallery Scene Builder - canonical layout matching public/models/gallery.glb
Usage: blender --background --python gallery_final.py
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
TEXTURE_DIR = os.path.join(PROJECT_ROOT, "public", "textures", "paintings")
EXPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")

HALF_W = 6.0
HALF_D = 4.0
HEIGHT = 3.5


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
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return m


def add_img_texture(mat_obj, img_path):
    if not os.path.exists(img_path):
        print(f"  WARNING: missing texture {img_path}")
        return
    img = bpy.data.images.load(img_path)
    nodes = mat_obj.node_tree.nodes
    links = mat_obj.node_tree.links
    tex = nodes.new('ShaderNodeTexImage')
    tex.image = img
    tex.location = (-600, 0)
    links.new(tex.outputs["Color"], nodes.get("Principled BSDF").inputs["Base Color"])


def link(obj, coll):
    for c in obj.users_collection:
        c.objects.unlink(obj)
    bpy.context.scene.collection.objects.unlink(obj)
    coll.objects.link(obj)


def make_cube(name, loc, scale, rot=(0, 0, 0), material=None, coll=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    obj.rotation_euler = rot
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    if material:
        obj.data.materials.append(material)
    if coll:
        link(obj, coll)
    return obj


def make_cyl(name, loc, radius, depth, material=None, verts=32, coll=None):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=loc, vertices=verts)
    obj = bpy.context.active_object
    obj.name = name
    bpy.ops.object.shade_smooth()
    if material:
        obj.data.materials.append(material)
    if coll:
        link(obj, coll)
    return obj


def make_plane(name, loc, scale, rot=(0, 0, 0), material=None, coll=None):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    obj.rotation_euler = rot
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    if material:
        obj.data.materials.append(material)
    if coll:
        link(obj, coll)
    return obj


def build_room():
    coll = bpy.data.collections.new("Room")
    bpy.context.scene.collection.children.link(coll)

    floor_mat = mat("Floor", (0.20, 0.18, 0.16), roughness=0.2, metallic=0.05)
    make_plane("Floor", (0, 0, 0), (HALF_W, HALF_D, 1), material=floor_mat, coll=coll)

    ceil_mat = mat("Ceiling", (0.96, 0.95, 0.93), roughness=0.9)
    make_plane("Ceiling", (0, 0, HEIGHT), (HALF_W, HALF_D, 1), rot=(math.pi, 0, 0), material=ceil_mat, coll=coll)

    wall_mat = mat("Wall", (0.93, 0.91, 0.88), roughness=0.85)
    make_cube("Wall_N", (0, -HALF_D, HEIGHT / 2), (HALF_W, 0.05, HEIGHT / 2), material=wall_mat, coll=coll)
    make_cube("Wall_S", (0, HALF_D, HEIGHT / 2), (HALF_W, 0.05, HEIGHT / 2), material=wall_mat, coll=coll)
    make_cube("Wall_W", (-HALF_W, 0, HEIGHT / 2), (0.05, HALF_D, HEIGHT / 2), material=wall_mat, coll=coll)
    make_cube("Wall_E", (HALF_W, 0, HEIGHT / 2), (0.05, HALF_D, HEIGHT / 2), material=wall_mat, coll=coll)

    bb_mat = mat("Baseboard", (0.87, 0.85, 0.82), roughness=0.7)
    make_cube("BB_N", (0, -3.94, 0.08), (5.9, 0.02, 0.08), material=bb_mat, coll=coll)
    make_cube("BB_S", (0, 3.94, 0.08), (5.9, 0.02, 0.08), material=bb_mat, coll=coll)
    make_cube("BB_W", (-5.94, 0, 0.08), (0.02, 7.8, 0.08), material=bb_mat, coll=coll)
    make_cube("BB_E", (5.94, 0, 0.08), (0.02, 7.8, 0.08), material=bb_mat, coll=coll)

    crown_mat = mat("Crown", (0.90, 0.88, 0.85), roughness=0.75)
    make_cube("Crown_N", (0, -3.92, 3.42), (5.9, 0.04, 0.04), material=crown_mat, coll=coll)
    make_cube("Crown_S", (0, 3.92, 3.42), (5.9, 0.04, 0.04), material=crown_mat, coll=coll)
    make_cube("Crown_W", (-5.92, 0, 3.42), (0.04, 7.8, 0.04), material=crown_mat, coll=coll)
    make_cube("Crown_E", (5.92, 0, 3.42), (0.04, 7.8, 0.04), material=crown_mat, coll=coll)

    print("  Room built")


def build_pillars():
    coll = bpy.data.collections.new("Pillars")
    bpy.context.scene.collection.children.link(coll)
    p_mat = mat("Pillar", (0.91, 0.89, 0.86), roughness=0.55, metallic=0.02)
    ring_mat = mat("Ring", (0.55, 0.42, 0.28), roughness=0.3, metallic=0.6)

    for x in [-3, 3]:
        make_cyl(f"P{x}_Shaft", (x, 0, 1.67), 0.12, 3.34, p_mat, coll=coll)
        make_cyl(f"P{x}_Cap", (x, 0, 3.38), 0.18, 0.08, p_mat, coll=coll)
        make_cyl(f"P{x}_Base", (x, 0, 0.03), 0.16, 0.06, p_mat, coll=coll)
        bpy.ops.mesh.primitive_torus_add(major_radius=0.14, minor_radius=0.015, location=(x, 0, 3.32))
        ring = bpy.context.active_object
        ring.name = f"P{x}_Ring"
        bpy.ops.object.shade_smooth()
        ring.data.materials.append(ring_mat)
        link(ring, coll)

    print("  Pillars built")


def build_sculptures():
    coll = bpy.data.collections.new("Sculptures")
    bpy.context.scene.collection.children.link(coll)

    bronze = mat("Bronze", (0.58, 0.44, 0.30), roughness=0.25, metallic=0.7)
    obsidian = mat("Obsidian", (0.08, 0.08, 0.09), roughness=0.15, metallic=0.8)
    marble = mat("Marble", (0.92, 0.90, 0.88), roughness=0.35)
    gold = mat("Gold", (0.72, 0.58, 0.32), roughness=0.22, metallic=0.75)
    ped_mat = mat("Pedestal", (0.94, 0.93, 0.91), roughness=0.45)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.35, segments=48, ring_count=24, location=(-2, 0, 1.35))
    body = bpy.context.active_object
    body.name = "Abstract_Body"
    bm = bmesh.new()
    bm.from_mesh(body.data)
    bm.verts.ensure_lookup_table()
    for v in bm.verts:
        x, y, z = v.co
        angle = math.atan2(y, x)
        r = math.sqrt(x ** 2 + y ** 2)
        twist = math.sin(z * 4 + angle * 2) * 0.08
        stretch = 1.0 + math.sin(z * 3) * 0.15
        wave = math.sin(angle * 3 + z * 2) * 0.04
        v.co.x = (r + wave) * math.cos(angle + twist) * 1.2
        v.co.y = (r + wave) * math.sin(angle + twist) * 1.2
        v.co.z = z * stretch
    bm.to_mesh(body.data)
    bm.free()
    body.data.update()
    bpy.ops.object.shade_smooth()
    body.data.materials.append(bronze)
    link(body, coll)

    make_cyl("Abs_Stem", (-2, 0, 0.7), 0.04, 0.6, obsidian, 24, coll=coll)
    make_cube("Abs_Ped", (-2, 0, 0.45), (0.44, 0.44, 0.9), material=ped_mat, coll=coll)
    make_cube("Abs_Cap", (-2, 0, 0.91), (0.48, 0.48, 0.02), material=ped_mat, coll=coll)

    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.28, subdivisions=2, location=(2, 1.5, 1.4))
    geo_out = bpy.context.active_object
    geo_out.name = "Geo_Outer"
    bpy.ops.object.shade_smooth()
    geo_out.data.materials.append(obsidian)
    link(geo_out, coll)

    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, segments=32, ring_count=16, location=(2, 1.5, 1.4))
    geo_in = bpy.context.active_object
    geo_in.name = "Geo_Inner"
    bpy.ops.object.shade_smooth()
    geo_in.data.materials.append(marble)
    link(geo_in, coll)

    bpy.ops.mesh.primitive_torus_add(major_radius=0.35, minor_radius=0.008, location=(2, 1.5, 1.4), rotation=(0.3, 0.5, 0))
    orbit = bpy.context.active_object
    orbit.name = "Geo_Orbit"
    bpy.ops.object.shade_smooth()
    orbit.data.materials.append(gold)
    link(orbit, coll)

    make_cyl("Geo_Stem", (2, 1.5, 0.55), 0.03, 0.85, obsidian, 24, coll=coll)
    make_cube("Geo_Ped", (2, 1.5, 0.55), (0.44, 0.44, 1.1), material=ped_mat, coll=coll)
    make_cube("Geo_Cap", (2, 1.5, 1.11), (0.48, 0.48, 0.02), material=ped_mat, coll=coll)

    print("  Custom sculptures built")


def build_benches():
    coll = bpy.data.collections.new("Furniture")
    bpy.context.scene.collection.children.link(coll)
    leather = mat("Leather", (0.13, 0.11, 0.10), roughness=0.65)
    metal = mat("Metal", (0.15, 0.14, 0.13), roughness=0.35, metallic=0.7)

    for bx, by, rot, name in [(0, 0, 0, "C"), (-4.5, 2, math.pi / 8, "W"), (4.5, -2, -math.pi / 6, "E")]:
        make_cube(f"Bench_{name}_Seat", (bx, by, 0.46), (1.7, 0.44, 0.06), rot=(0, 0, rot), material=leather, coll=coll)
        for lx, ly in [(-0.7, -0.15), (0.7, -0.15), (-0.7, 0.15), (0.7, 0.15)]:
            rlx = lx * math.cos(rot) - ly * math.sin(rot)
            rly = lx * math.sin(rot) + ly * math.cos(rot)
            make_cyl(f"Bench_{name}_Leg", (bx + rlx, by + rly, 0.23), 0.012, 0.46, metal, 12, coll=coll)

    print("  Benches built")


WALLS = {
    # wall: (tangent, inward normal, canvas rotation)
    'N': ((1, 0, 0), (0, 1, 0), (-math.pi / 2, 0, 0)),
    'S': ((1, 0, 0), (0, -1, 0), (math.pi / 2, 0, 0)),
    'W': ((0, 1, 0), (1, 0, 0), (0, math.pi / 2, 0)),
    'E': ((0, 1, 0), (-1, 0, 0), (0, -math.pi / 2, 0)),
}


def _offset(loc, direction, distance):
    return tuple(l + d * distance for l, d in zip(loc, direction))


def build_painting(wall, loc, w, h, name, img_file, frame_m):
    coll = bpy.data.collections.get("Paintings")
    T, Nn, plane_rot = WALLS[wall]
    fw, fd = 0.06, 0.055
    vertical = (fw, fd, h) if wall in ('N', 'S') else (fd, fw, h)
    horizontal = (w + fw * 2, fd, fw) if wall in ('N', 'S') else (fd, w + fw * 2, fw)

    for sign in (-1, 1):
        off = tuple(t * sign * (w / 2 + fw / 2) for t in T)
        make_cube(f"{name}_Side", _offset(loc, off, 1), vertical,
                  material=frame_m, coll=coll)
    for sign in (-1, 1):
        off = (0, 0, sign * (h / 2 + fw / 2))
        make_cube(f"{name}_Cap", _offset(loc, off, 1), horizontal,
                  material=frame_m, coll=coll)

    mb = mat(f"{name}_Mat_M", (0.95, 0.92, 0.86), roughness=0.95)
    mat_loc = _offset(loc, Nn, -0.004)
    make_plane(f"{name}_Mat", mat_loc, ((w + 0.07) / 2, (h + 0.07) / 2, 1),
               rot=plane_rot, material=mb, coll=coll)

    canvas = make_plane(f"{name}_Canvas", _offset(loc, Nn, 0.004),
                        (w / 2, h / 2, 1), rot=plane_rot, coll=coll)
    canvas_mat = mat(f"{name}_Canvas_M", (0.9, 0.88, 0.85), roughness=0.65)
    add_img_texture(canvas_mat, os.path.join(TEXTURE_DIR, img_file))
    canvas.data.materials.append(canvas_mat)


def build_paintings():
    bpy.data.collections.new("Paintings")
    coll = bpy.data.collections.get("Paintings")
    bpy.context.scene.collection.children.link(coll)

    frame_gilt = mat("F_Gilt", (0.72, 0.58, 0.32), roughness=0.32, metallic=0.85)
    frame_wood = mat("F_Wood", (0.17, 0.11, 0.07), roughness=0.55, metallic=0.15)
    frame_modern = mat("F_Modern", (0.20, 0.20, 0.24), roughness=0.38, metallic=0.45)

    specs = [
        ('W', (-5.94, 0, 1.6), 1.6, 1.1, "Art_W1", "painting_01.jpg", frame_gilt),
        ('W', (-5.94, 2.5, 1.62), 1.2, 0.9, "Art_W2", "painting_02.jpg", frame_modern),
        ('W', (-5.94, -2.5, 1.58), 1.8, 1.2, "Art_W3", "painting_03.jpg", frame_wood),
        ('N', (-3, -3.94, 1.6), 1.4, 1.0, "Art_N1", "painting_04.jpg", frame_modern),
        ('N', (0, -3.94, 1.56), 1.0, 1.4, "Art_N2", "painting_05.jpg", frame_gilt),
        ('N', (3, -3.94, 1.6), 1.6, 1.1, "Art_N3", "painting_06.jpg", frame_wood),
        ('E', (5.94, 0, 1.6), 1.4, 1.0, "Art_E1", "painting_07.jpg", frame_wood),
        ('E', (5.94, -2.5, 1.56), 1.2, 1.6, "Art_E2", "painting_08.jpg", frame_gilt),
        ('S', (-3, 3.94, 1.56), 1.6, 1.1, "Art_S1", "painting_09.jpg", frame_modern),
        ('S', (0, 3.94, 1.6), 1.0, 1.4, "Art_S2", "painting_10.jpg", frame_wood),
        ('S', (3, 3.94, 1.56), 1.8, 1.2, "Art_S3", "painting_11.jpg", frame_gilt),
    ]

    for wall, loc, w, h, name, img_file, fm in specs:
        build_painting(wall, loc, w, h, name, img_file, fm)

    print("  11 paintings built vertically with frames, mats, textures")


def build_windows():
    bpy.data.collections.new("Windows")
    coll = bpy.data.collections.get("Windows")
    bpy.context.scene.collection.children.link(coll)

    frame = mat("WFrame", (0.10, 0.10, 0.10), roughness=0.35, metallic=0.7)
    glass = mat("Glass", (0.74, 0.84, 0.90), roughness=0.05, metallic=0.1)
    glass.node_tree.nodes.get("Principled BSDF").inputs["Alpha"].default_value = 0.18

    W, H, ft, fd = 2.2, 1.8, 0.07, 0.12

    specs = [
        ('S', (-2, 3.94, 2.25), "WS1"),
        ('S', (2, 3.94, 2.25), "WS2"),
        ('W', (-5.94, 0, 2.25), "WW1"),
    ]
    for wall, loc, name in specs:
        T, Nn, plane_rot = WALLS[wall]
        vertical = (ft, fd, H) if wall in ('N', 'S') else (fd, ft, H)
        horizontal = (W + ft * 2, fd, ft) if wall in ('N', 'S') else (fd, W + ft * 2, ft)

        for sign in (-1, 1):
            off = tuple(t * sign * (W / 2 + ft / 2) for t in T)
            make_cube(f"{name}_Side", _offset(loc, off, 1), vertical, material=frame, coll=coll)
        for sign in (-1, 1):
            off = (0, 0, sign * (H / 2 + ft / 2))
            make_cube(f"{name}_Cap", _offset(loc, off, 1), horizontal, material=frame, coll=coll)
        mid_v = (0.05, fd * 0.6, H) if wall in ('N', 'S') else (fd * 0.6, 0.05, H)
        mid_h = (W, fd * 0.6, 0.05) if wall in ('N', 'S') else (fd * 0.6, W, 0.05)
        make_cube(f"{name}_MullV", loc, mid_v, material=frame, coll=coll)
        make_cube(f"{name}_MullH", loc, mid_h, material=frame, coll=coll)

        make_plane(f"{name}_Glass", _offset(loc, Nn, fd - 0.02), (W / 2, H / 2, 1),
                   rot=plane_rot, material=glass, coll=coll)

    print("  Windows rebuilt vertically")


def setup_lighting():
    coll = bpy.data.collections.new("Lighting")
    bpy.context.scene.collection.children.link(coll)

    bpy.ops.object.light_add(type='AREA', location=(0, 0, 3.4))
    fill = bpy.context.active_object
    fill.name = "Fill"
    fill.data.energy = 200
    fill.data.size = 5
    fill.data.color = (1.0, 0.97, 0.92)
    coll.objects.link(fill)

    spots = [
        ((-4, 0, 3.3), (-6, 0, 1.6), 120, "Spot"),
        ((-4, -2.5, 3.3), (-6, -2.5, 1.65), 100, "Spot"),
        ((-4, 2.5, 3.3), (-6, 2.5, 1.6), 100, "Spot"),
        ((4, 0, 3.3), (6, 0, 1.65), 120, "Spot"),
        ((4, 2.5, 3.3), (6, 2.5, 1.6), 100, "Spot"),
        ((-2, -2.5, 3.3), (-3, -3.94, 1.65), 100, "Spot"),
        ((0, -2.5, 3.3), (0, -3.94, 1.6), 100, "Spot"),
        ((2, -2.5, 3.3), (3, -3.94, 1.65), 100, "Spot"),
        ((-2, 2.5, 3.3), (-3, 3.94, 1.6), 100, "Spot"),
        ((0, 2.5, 3.3), (0, 3.94, 1.65), 100, "Spot"),
        ((2, 2.5, 3.3), (3, 3.94, 1.6), 100, "Spot"),
    ]
    for pos, target, energy, base_name in spots:
        bpy.ops.object.light_add(type='SPOT', location=pos)
        s = bpy.context.active_object
        s.name = f"{base_name}.{len([o for o in bpy.data.objects if o.name.startswith(base_name)]):03d}"
        s.data.energy = energy
        s.data.spot_size = math.radians(45)
        s.data.spot_blend = 0.65
        s.data.color = (1.0, 0.97, 0.92)
        direction = Vector(target) - Vector(pos)
        s.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
        coll.objects.link(s)

    print("  Lighting rigged")


def setup_camera():
    bpy.ops.object.camera_add(location=(3.6, -2.9, 2.4))
    cam = bpy.context.active_object
    cam.name = "Gallery_Camera"
    cam.data.angle = math.radians(55)
    direction = Vector((-1, 1.2, 1.3)) - Vector((3.6, -2.9, 2.4))
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()


def main():
    print("\n" + "=" * 50)
    print("BUILDING GALLERY SCENE")
    print("=" * 50)

    clear_scene()
    build_room()
    build_pillars()
    build_sculptures()
    build_benches()
    build_paintings()
    build_windows()
    setup_lighting()
    setup_camera()

    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    bpy.context.scene.eevee.use_ssr = True

    os.makedirs(EXPORT_DIR, exist_ok=True)
    export_path = os.path.join(EXPORT_DIR, "gallery.glb")
    bpy.ops.export_scene.gltf(
        filepath=export_path,
        export_format='GLB',
        use_selection=False,
        export_apply=True,
        export_cameras=True,
        export_lights=True,
        export_materials='EXPORT'
    )
    print(f"\nExported: {export_path}")

    blend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gallery_final.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Saved: {blend_path}\n" + "=" * 50)


if __name__ == "__main__":
    main()
