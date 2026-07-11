"""
Gallery Scene Creator - Professional Grade
Run this script in Blender to generate a museum-quality gallery.
Usage: blender --background --python create_gallery_pro.py
"""

import bpy
import bmesh
import math
import os
from mathutils import Vector, Euler

# =============================================================================
# COLOR PALETTE - Professional Gallery
# =============================================================================

PALETTE = {
    # Walls - Warm gallery white (not pure white, which looks sterile)
    "wall_primary": (0.92, 0.90, 0.87),      # Warm ivory
    "wall_secondary": (0.89, 0.87, 0.84),     # Slightly darker accent wall
    
    # Floor - Polished concrete or hardwood
    "floor_main": (0.18, 0.16, 0.14),         # Dark espresso
    "floor_highlight": (0.22, 0.19, 0.16),    # Warm undertone
    
    # Ceiling
    "ceiling": (0.96, 0.95, 0.93),            # Off-white
    
    # Architectural details
    "baseboard": (0.88, 0.86, 0.83),          # Warm gray
    "crown_molding": (0.90, 0.88, 0.85),      # Matching baseboard
    "pillar": (0.91, 0.89, 0.86),             # Subtle warmth
    
    # Furniture
    "bench_leather": (0.12, 0.11, 0.10),      # Dark leather
    "bench_frame": (0.15, 0.14, 0.13),        # Matte black metal
    "pedestal": (0.94, 0.93, 0.91),           # Clean white
    
    # Sculptures
    "sculpture_bronze": (0.55, 0.42, 0.28),   # Rich bronze
    "sculpture_marble": (0.92, 0.90, 0.88),   # Warm marble
    "sculpture_obsidian": (0.08, 0.08, 0.09), # Deep black
    
    # Painting frames
    "frame_dark_wood": (0.18, 0.12, 0.08),    # Walnut
    "frame_gilt": (0.72, 0.58, 0.32),         # Antiqued gold
    "frame_modern": (0.20, 0.20, 0.20),       # Matte black
    
    # Canvas backgrounds (neutral for abstract art)
    "canvas_white": (0.95, 0.93, 0.90),
    "canvas_cream": (0.94, 0.91, 0.85),
    "canvas_warm_gray": (0.82, 0.79, 0.76),
}

# Professional art colors for paintings
ART_COLORS = [
    # Deep blues and teals
    {"primary": (0.15, 0.28, 0.45), "secondary": (0.22, 0.42, 0.58), "accent": (0.68, 0.78, 0.85)},
    # Earth tones
    {"primary": (0.45, 0.32, 0.22), "secondary": (0.58, 0.45, 0.32), "accent": (0.82, 0.72, 0.58)},
    # Muted reds
    {"primary": (0.52, 0.22, 0.18), "secondary": (0.65, 0.32, 0.28), "accent": (0.85, 0.62, 0.55)},
    # Sage greens
    {"primary": (0.35, 0.42, 0.32), "secondary": (0.48, 0.55, 0.42), "accent": (0.72, 0.78, 0.68)},
    # Warm grays
    {"primary": (0.42, 0.40, 0.38), "secondary": (0.55, 0.52, 0.50), "accent": (0.78, 0.75, 0.72)},
    # Deep purples
    {"primary": (0.32, 0.22, 0.38), "secondary": (0.45, 0.32, 0.52), "accent": (0.68, 0.55, 0.75)},
    # Burnt orange
    {"primary": (0.58, 0.35, 0.18), "secondary": (0.72, 0.48, 0.28), "accent": (0.88, 0.72, 0.52)},
    # Navy and gold
    {"primary": (0.12, 0.18, 0.32), "secondary": (0.22, 0.28, 0.42), "accent": (0.72, 0.58, 0.28)},
]


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)

def create_collection(name):
    collection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(collection)
    return collection

def move_to_collection(collection, obj):
    for c in obj.users_collection:
        c.objects.unlink(obj)
    collection.objects.link(obj)

def create_material(name, color, roughness=0.5, metallic=0.0, specular=0.5):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if "Specular IOR Level" in bsdf.inputs:
        bsdf.inputs["Specular IOR Level"].default_value = specular
    return mat

def create_emission_material(name, color, strength=1.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Emission Color"].default_value = (*color, 1.0)
    bsdf.inputs["Emission Strength"].default_value = strength
    return mat

def add_smooth(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.shade_smooth()
    obj.select_set(False)


# =============================================================================
# ARCHITECTURAL ELEMENTS
# =============================================================================

def create_floor():
    coll = create_collection("Floor")
    
    # Main floor - dark polished wood
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "Floor_Main"
    floor.scale = (6, 4, 1)
    bpy.ops.object.transform_apply(scale=True)
    floor.data.materials.append(create_material(
        "Floor_Wood", PALETTE["floor_main"], 
        roughness=0.25, metallic=0.05, specular=0.6
    ))
    move_to_collection(coll, floor)
    
    # Floor border/inlay
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0.001))
    border = bpy.context.active_object
    border.name = "Floor_Border"
    border.scale = (5.8, 3.8, 1)
    bpy.ops.object.transform_apply(scale=True)
    border.data.materials.append(create_material(
        "Floor_Border_Mat", PALETTE["floor_highlight"],
        roughness=0.3, metallic=0.05
    ))
    move_to_collection(coll, border)

def create_ceiling():
    coll = create_collection("Ceiling")
    
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 3.5))
    ceiling = bpy.context.active_object
    ceiling.name = "Ceiling_Main"
    ceiling.scale = (6, 4, 1)
    ceiling.rotation_euler = (math.pi, 0, 0)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    ceiling.data.materials.append(create_material(
        "Ceiling_Mat", PALETTE["ceiling"], roughness=0.92
    ))
    move_to_collection(coll, ceiling)
    
    # Ceiling beam accents
    for x_pos in [-3, 3]:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x_pos, 0, 3.45))
        beam = bpy.context.active_object
        beam.name = f"Ceiling_Beam_{x_pos}"
        beam.scale = (0.15, 4, 0.05)
        bpy.ops.object.transform_apply(scale=True)
        beam.data.materials.append(create_material(
            "Beam_Mat", PALETTE["crown_molding"], roughness=0.8
        ))
        move_to_collection(coll, beam)

def create_walls():
    coll = create_collection("Walls")
    
    wall_configs = [
        {"name": "Wall_North", "pos": (0, -4, 1.75), "rot": (0, 0, 0), 
         "scale": (6, 0.1, 3.5), "color": PALETTE["wall_primary"]},
        {"name": "Wall_South", "pos": (0, 4, 1.75), "rot": (0, 0, 0),
         "scale": (6, 0.1, 3.5), "color": PALETTE["wall_primary"]},
        {"name": "Wall_West", "pos": (-6, 0, 1.75), "rot": (0, 0, math.pi/2),
         "scale": (4, 0.1, 3.5), "color": PALETTE["wall_secondary"]},
        {"name": "Wall_East", "pos": (6, 0, 1.75), "rot": (0, 0, math.pi/2),
         "scale": (4, 0.1, 3.5), "color": PALETTE["wall_secondary"]},
    ]
    
    for cfg in wall_configs:
        bpy.ops.mesh.primitive_cube_add(size=1, location=cfg["pos"])
        wall = bpy.context.active_object
        wall.name = cfg["name"]
        wall.scale = cfg["scale"]
        wall.rotation_euler = cfg["rot"]
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        wall.data.materials.append(create_material(
            f"{cfg['name']}_Mat", cfg["color"], roughness=0.88
        ))
        move_to_collection(coll, wall)

def create_moldings():
    coll = create_collection("Moldings")
    
    # Baseboards
    bb_configs = [
        ("BB_North", (0, -3.94, 0.08), (0, 0, 0), (5.9, 0.02, 0.16)),
        ("BB_South", (0, 3.94, 0.08), (0, 0, 0), (5.9, 0.02, 0.16)),
        ("BB_West", (-5.94, 0, 0.08), (0, 0, math.pi/2), (3.9, 0.02, 0.16)),
        ("BB_East", (5.94, 0, 0.08), (0, 0, math.pi/2), (3.9, 0.02, 0.16)),
    ]
    
    for name, pos, rot, scale in bb_configs:
        bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
        bb = bpy.context.active_object
        bb.name = name
        bb.scale = scale
        bb.rotation_euler = rot
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        bb.data.materials.append(create_material(
            f"{name}_Mat", PALETTE["baseboard"], roughness=0.7
        ))
        move_to_collection(coll, bb)
    
    # Crown molding (decorative strip at ceiling)
    crown_configs = [
        ("Crown_North", (0, -3.92, 3.42), (0, 0, 0), (5.9, 0.04, 0.08)),
        ("Crown_South", (0, 3.92, 3.42), (0, 0, 0), (5.9, 0.04, 0.08)),
        ("Crown_West", (-5.92, 0, 3.42), (0, 0, math.pi/2), (3.9, 0.04, 0.08)),
        ("Crown_East", (5.92, 0, 3.42), (0, 0, math.pi/2), (3.9, 0.04, 0.08)),
    ]
    
    for name, pos, rot, scale in crown_configs:
        bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
        crown = bpy.context.active_object
        crown.name = name
        crown.scale = scale
        crown.rotation_euler = rot
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        crown.data.materials.append(create_material(
            f"{name}_Mat", PALETTE["crown_molding"], roughness=0.75
        ))
        move_to_collection(coll, crown)

def create_pillars():
    coll = create_collection("Pillars")
    
    pillar_positions = [(-3, 0), (3, 0)]
    
    for i, pos in enumerate(pillar_positions, 1):
        # Main shaft
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.12, depth=3.34, 
            location=(pos[0], pos[1], 1.67),
            vertices=32
        )
        shaft = bpy.context.active_object
        shaft.name = f"Pillar_{i}_Shaft"
        add_smooth(shaft)
        shaft.data.materials.append(create_material(
            f"Pillar_{i}_Mat", PALETTE["pillar"], 
            roughness=0.55, metallic=0.02, specular=0.7
        ))
        move_to_collection(coll, shaft)
        
        # Capital (top)
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.18, depth=0.08,
            location=(pos[0], pos[1], 3.38),
            vertices=32
        )
        capital = bpy.context.active_object
        capital.name = f"Pillar_{i}_Capital"
        add_smooth(capital)
        capital.data.materials.append(shaft.data.materials[0])
        move_to_collection(coll, capital)
        
        # Base
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.16, depth=0.06,
            location=(pos[0], pos[1], 0.03),
            vertices=32
        )
        base = bpy.context.active_object
        base.name = f"Pillar_{i}_Base"
        add_smooth(base)
        base.data.materials.append(shaft.data.materials[0])
        move_to_collection(coll, base)
        
        # Decorative ring
        bpy.ops.mesh.primitive_torus_add(
            major_radius=0.14, minor_radius=0.015,
            location=(pos[0], pos[1], 3.32)
        )
        ring = bpy.context.active_object
        ring.name = f"Pillar_{i}_Ring"
        add_smooth(ring)
        ring.data.materials.append(create_material(
            f"Ring_{i}_Mat", PALETTE["sculpture_bronze"],
            roughness=0.3, metallic=0.6
        ))
        move_to_collection(coll, ring)


# =============================================================================
# SCULPTURES (Custom Models)
# =============================================================================

def create_abstract_sculpture():
    """Organic flowing form - the hero piece"""
    coll = create_collection("Sculpture_Abstract")
    
    # Main organic form
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.35, segments=48, ring_count=24,
        location=(-2, 0, 1.35)
    )
    body = bpy.context.active_object
    body.name = "Abstract_Body"
    
    # Sculpt organic deformation
    bm = bmesh.new()
    bm.from_mesh(body.data)
    bm.verts.ensure_lookup_table()
    
    for vert in bm.verts:
        # Create flowing, organic distortion
        x, y, z = vert.co
        angle = math.atan2(y, x)
        r = math.sqrt(x**2 + y**2)
        
        # Twist and stretch
        twist = math.sin(z * 4 + angle * 2) * 0.08
        stretch = 1.0 + math.sin(z * 3) * 0.15
        wave = math.sin(angle * 3 + z * 2) * 0.04
        
        vert.co.x = (r + wave) * math.cos(angle + twist) * 1.2
        vert.co.y = (r + wave) * math.sin(angle + twist) * 1.2
        vert.co.z = z * stretch
    
    bm.to_mesh(body.data)
    bm.free()
    body.data.update()
    add_smooth(body)
    
    body.data.materials.append(create_material(
        "Abstract_Bronze", PALETTE["sculpture_bronze"],
        roughness=0.28, metallic=0.65, specular=0.8
    ))
    move_to_collection(coll, body)
    
    # Stem
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.04, depth=0.6, vertices=24,
        location=(-2, 0, 0.7)
    )
    stem = bpy.context.active_object
    stem.name = "Abstract_Stem"
    add_smooth(stem)
    stem.data.materials.append(create_material(
        "Stem_Black", PALETTE["sculpture_obsidian"],
        roughness=0.15, metallic=0.8
    ))
    move_to_collection(coll, stem)
    
    # Pedestal
    create_pedestal((-2, 0), 0.9, "Pedestal_Abstract")
    
    return body

def create_geometric_sculpture():
    """Interlocking geometric forms"""
    coll = create_collection("Sculpture_Geometric")
    
    # Outer wireframe icosahedron
    bpy.ops.mesh.primitive_ico_sphere_add(
        radius=0.28, subdivisions=2,
        location=(2, 1.5, 1.4)
    )
    outer = bpy.context.active_object
    outer.name = "Geo_Outer"
    add_smooth(outer)
    outer.data.materials.append(create_material(
        "Geo_Outer_Mat", PALETTE["sculpture_obsidian"],
        roughness=0.12, metallic=0.85
    ))
    move_to_collection(coll, outer)
    
    # Inner solid sphere
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.18, segments=32, ring_count=16,
        location=(2, 1.5, 1.4)
    )
    inner = bpy.context.active_object
    inner.name = "Geo_Inner"
    add_smooth(inner)
    inner.data.materials.append(create_material(
        "Geo_Inner_Mat", PALETTE["sculpture_marble"],
        roughness=0.4, metallic=0.1, specular=0.9
    ))
    move_to_collection(coll, inner)
    
    # Orbital ring
    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.35, minor_radius=0.008,
        location=(2, 1.5, 1.4),
        rotation=(0.3, 0.5, 0)
    )
    orbit = bpy.context.active_object
    orbit.name = "Geo_Orbit"
    add_smooth(orbit)
    orbit.data.materials.append(create_material(
        "Orbit_Gold", PALETTE["frame_gilt"],
        roughness=0.25, metallic=0.7
    ))
    move_to_collection(coll, orbit)
    
    # Stem
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.03, depth=0.85, vertices=24,
        location=(2, 1.5, 0.55)
    )
    stem = bpy.context.active_object
    stem.name = "Geo_Stem"
    add_smooth(stem)
    stem.data.materials.append(create_material(
        "Geo_Stem_Mat", PALETTE["sculpture_obsidian"],
        roughness=0.15, metallic=0.8
    ))
    move_to_collection(coll, stem)
    
    # Pedestal
    create_pedestal((2, 1.5), 1.1, "Pedestal_Geometric")
    
    return outer


# =============================================================================
# FURNITURE
# =============================================================================

def create_gallery_bench(location, rotation=0, name="Bench"):
    """Modern gallery bench with leather seat"""
    coll = create_collection("Furniture")
    
    # Seat cushion
    bpy.ops.mesh.primitive_cube_add(size=1, location=(location[0], location[1], 0.46))
    seat = bpy.context.active_object
    seat.name = f"{name}_Seat"
    seat.scale = (0.85, 0.22, 0.025)
    seat.rotation_euler = (0, 0, rotation)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    seat.data.materials.append(create_material(
        f"{name}_Leather", PALETTE["bench_leather"],
        roughness=0.65, metallic=0.0
    ))
    move_to_collection(coll, seat)
    
    # Metal frame
    frame_mat = create_material(
        f"{name}_Frame", PALETTE["bench_frame"],
        roughness=0.35, metallic=0.7
    )
    
    # Legs - angled metal
    leg_offsets = [(-0.7, -0.12), (0.7, -0.12), (-0.7, 0.12), (0.7, 0.12)]
    for i, (lx, ly) in enumerate(leg_offsets):
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.012, depth=0.46, vertices=12,
            location=(location[0] + lx, location[1] + ly, 0.23)
        )
        leg = bpy.context.active_object
        leg.name = f"{name}_Leg_{i}"
        leg.rotation_euler = (0, 0, rotation)
        bpy.ops.object.transform_apply(rotation=True)
        add_smooth(leg)
        leg.data.materials.append(frame_mat)
        move_to_collection(coll, leg)
    
    return seat


# =============================================================================
# PAINTINGS
# =============================================================================

def create_painting_frame(location, rotation, width, height, name, frame_type="modern"):
    """Professional painting with proper framing"""
    coll = create_collection("Paintings")
    
    # Frame selection
    frame_configs = {
        "modern": {"color": PALETTE["frame_modern"], "width": 0.035, "depth": 0.025},
        "wood": {"color": PALETTE["frame_dark_wood"], "width": 0.05, "depth": 0.03},
        "gilt": {"color": PALETTE["frame_gilt"], "width": 0.06, "depth": 0.035},
    }
    cfg = frame_configs.get(frame_type, frame_configs["modern"])
    
    # Frame - 4 pieces
    frame_mat = create_material(
        f"{name}_Frame_Mat", cfg["color"],
        roughness=0.5 if frame_type == "gilt" else 0.6,
        metallic=0.6 if frame_type == "gilt" else 0.15
    )
    
    fw = cfg["width"]
    fd = cfg["depth"]
    
    # Frame pieces (positioned in local space, then rotated)
    frame_pieces = [
        # Top
        (0, height/2 + fw/2, fd/2, (width + fw*2, fw, fd)),
        # Bottom
        (0, -height/2 - fw/2, fd/2, (width + fw*2, fw, fd)),
        # Left
        (-width/2 - fw/2, 0, fd/2, (fw, height, fd)),
        # Right
        (width/2 + fw/2, 0, fd/2, (fw, height, fd)),
    ]
    
    frame_collection = create_collection(f"{name}_Frame")
    
    for i, (fx, fy, fz, fscale) in enumerate(frame_pieces):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(
            location[0] + fx * math.cos(rotation[2]) - fy * math.sin(rotation[2]),
            location[1] + fx * math.sin(rotation[2]) + fy * math.cos(rotation[2]),
            location[2] + fz
        ))
        piece = bpy.context.active_object
        piece.name = f"{name}_Frame_{i}"
        piece.scale = fscale
        piece.rotation_euler = rotation
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        piece.data.materials.append(frame_mat)
        move_to_collection(frame_collection, piece)
    
    # Canvas (slightly recessed)
    canvas_offset = -0.005
    bpy.ops.mesh.primitive_plane_add(size=1, location=(
        location[0] + canvas_offset * math.sin(rotation[2]),
        location[1] + canvas_offset * math.cos(rotation[2]),
        location[2]
    ))
    canvas = bpy.context.active_object
    canvas.name = f"{name}_Canvas"
    canvas.scale = (width/2, height/2, 1)
    canvas.rotation_euler = rotation
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    
    # Apply art color palette
    art_idx = hash(name) % len(ART_COLORS)
    art = ART_COLORS[art_idx]
    
    canvas.data.materials.append(create_material(
        f"{name}_Canvas_Mat", art["primary"], roughness=0.9
    ))
    move_to_collection(coll, canvas)
    
    # Mat board (border around canvas)
    mat_offset = 0.008
    bpy.ops.mesh.primitive_plane_add(size=1, location=(
        location[0] + mat_offset * math.sin(rotation[2]),
        location[1] + mat_offset * math.cos(rotation[2]),
        location[2] - 0.001
    ))
    mat_board = bpy.context.active_object
    mat_board.name = f"{name}_MatBoard"
    mat_board.scale = (width/2 + 0.04, height/2 + 0.04, 1)
    mat_board.rotation_euler = rotation
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    mat_board.data.materials.append(create_material(
        f"{name}_MatBoard_Mat", PALETTE["canvas_cream"], roughness=0.95
    ))
    move_to_collection(coll, mat_board)
    
    return canvas

def create_pedestal(location, height=0.9, name="Pedestal"):
    """Clean white pedestal"""
    coll = create_collection("Pedestals")
    
    # Main body
    bpy.ops.mesh.primitive_cube_add(size=1, location=(location[0], location[1], height/2))
    pedestal = bpy.context.active_object
    pedestal.name = name
    pedestal.scale = (0.22, 0.22, height/2)
    bpy.ops.object.transform_apply(scale=True)
    pedestal.data.materials.append(create_material(
        f"{name}_Mat", PALETTE["pedestal"],
        roughness=0.45, metallic=0.02, specular=0.8
    ))
    move_to_collection(coll, pedestal)
    
    # Top cap (slightly larger)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(location[0], location[1], height + 0.01))
    cap = bpy.context.active_object
    cap.name = f"{name}_Cap"
    cap.scale = (0.24, 0.24, 0.01)
    bpy.ops.object.transform_apply(scale=True)
    cap.data.materials.append(pedestal.data.materials[0])
    move_to_collection(coll, cap)


# =============================================================================
# LIGHTING
# =============================================================================

def setup_lighting():
    coll = create_collection("Lighting")
    
    # Ambient fill
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 3.4))
    fill = bpy.context.active_object
    fill.name = "Light_Fill"
    fill.data.energy = 150
    fill.data.size = 5
    fill.data.color = (1.0, 0.98, 0.95)
    move_to_collection(coll, fill)
    
    # Track lighting - spots aimed at artworks
    spot_configs = [
        # Left wall paintings
        {"pos": (-4.5, 0, 3.3), "target": (-6, 0, 1.6), "energy": 120, "name": "Spot_West_1"},
        {"pos": (-4.5, -2.5, 3.3), "target": (-6, -2.5, 1.6), "energy": 100, "name": "Spot_West_2"},
        {"pos": (-4.5, 2.5, 3.3), "target": (-6, 2.5, 1.6), "energy": 100, "name": "Spot_West_3"},
        
        # Right wall paintings
        {"pos": (4.5, 0, 3.3), "target": (6, 0, 1.6), "energy": 120, "name": "Spot_East_1"},
        {"pos": (4.5, 2.5, 3.3), "target": (6, 2.5, 1.6), "energy": 100, "name": "Spot_East_2"},
        
        # North wall paintings
        {"pos": (-2, -2.5, 3.3), "target": (-3, -4, 1.6), "energy": 100, "name": "Spot_North_1"},
        {"pos": (0, -2.5, 3.3), "target": (0, -4, 1.6), "energy": 100, "name": "Spot_North_2"},
        {"pos": (2, -2.5, 3.3), "target": (3, -4, 1.6), "energy": 100, "name": "Spot_North_3"},
        
        # South wall paintings
        {"pos": (-2, 2.5, 3.3), "target": (-3, 4, 1.6), "energy": 100, "name": "Spot_South_1"},
        {"pos": (0, 2.5, 3.3), "target": (0, 4, 1.6), "energy": 100, "name": "Spot_South_2"},
        {"pos": (2, 2.5, 3.3), "target": (3, 4, 1.6), "energy": 100, "name": "Spot_South_3"},
        
        # Sculpture lighting
        {"pos": (-2, 0.5, 3.3), "target": (-2, 0, 1.35), "energy": 80, "name": "Spot_Sculpture_1"},
        {"pos": (2, 2, 3.3), "target": (2, 1.5, 1.4), "energy": 80, "name": "Spot_Sculpture_2"},
    ]
    
    for cfg in spot_configs:
        bpy.ops.object.light_add(type='SPOT', location=cfg["pos"])
        spot = bpy.context.active_object
        spot.name = cfg["name"]
        spot.data.energy = cfg["energy"]
        spot.data.spot_size = math.radians(45)
        spot.data.spot_blend = 0.65
        spot.data.color = (1.0, 0.97, 0.92)
        spot.data.shadow_soft_size = 0.5
        
        target = Vector(cfg["target"])
        direction = target - Vector(cfg["pos"])
        rot_quat = direction.to_track_quat('-Z', 'Y')
        spot.rotation_euler = rot_quat.to_euler()
        
        move_to_collection(coll, spot)


# =============================================================================
# CAMERA & RENDER
# =============================================================================

def setup_camera():
    bpy.ops.object.camera_add(location=(0, 6, 1.6))
    camera = bpy.context.active_object
    camera.name = "Gallery_Camera"
    
    direction = Vector((0, 0, 1.6)) - camera.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()
    
    camera.data.lens = 35
    camera.data.clip_start = 0.1
    camera.data.clip_end = 100
    camera.data.dof.use_dof = True
    camera.data.dof.aperture_fstop = 8.0
    
    bpy.context.scene.camera = camera
    return camera

def setup_render():
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 256
    bpy.context.scene.cycles.use_denoising = True
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.resolution_percentage = 100
    
    # World
    world = bpy.data.worlds.new("Gallery_World")
    bpy.context.scene.world = world
    world.use_nodes = True
    
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs["Color"].default_value = (0.02, 0.02, 0.025, 1.0)
        bg_node.inputs["Strength"].default_value = 0.05


# =============================================================================
# EXPORT
# =============================================================================

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
    print(f"Exported GLB: {filepath}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("\n" + "="*60)
    print("GALLERY SCENE CREATOR - Professional Grade")
    print("="*60 + "\n")
    
    clear_scene()
    
    # Architecture
    print("[1/8] Creating floor...")
    create_floor()
    
    print("[2/8] Creating ceiling...")
    create_ceiling()
    
    print("[3/8] Creating walls...")
    create_walls()
    
    print("[4/8] Creating moldings...")
    create_moldings()
    
    print("[5/8] Creating pillars...")
    create_pillars()
    
    # Sculptures
    print("[6/8] Creating sculptures...")
    create_abstract_sculpture()
    create_geometric_sculpture()
    
    # Furniture
    print("       Adding furniture...")
    create_gallery_bench((0, 0), 0, "Bench_Center")
    create_gallery_bench((-4.5, 2), math.pi/8, "Bench_West")
    create_gallery_bench((4.5, -2), -math.pi/6, "Bench_East")
    
    # Paintings
    print("[7/8] Creating paintings...")
    painting_specs = [
        # West wall (left)
        ((-5.94, 0, 1.6), (0, math.pi/2, 0), 1.6, 1.1, "Art_W1", "gilt"),
        ((-5.94, -2.5, 1.65), (0, math.pi/2, 0), 1.2, 0.9, "Art_W2", "modern"),
        ((-5.94, 2.5, 1.6), (0, math.pi/2, 0), 1.8, 1.2, "Art_W3", "wood"),
        
        # North wall (back)
        ((-3, -3.94, 1.65), (0, 0, 0), 1.4, 1.0, "Art_N1", "modern"),
        ((0, -3.94, 1.6), (0, 0, 0), 1.0, 1.4, "Art_N2", "gilt"),
        ((3, -3.94, 1.65), (0, 0, 0), 1.6, 1.1, "Art_N3", "wood"),
        
        # East wall (right)
        ((5.94, 0, 1.65), (0, -math.pi/2, 0), 1.4, 1.0, "Art_E1", "wood"),
        ((5.94, 2.5, 1.6), (0, -math.pi/2, 0), 1.2, 1.6, "Art_E2", "gilt"),
        
        # South wall (front)
        ((-3, 3.94, 1.6), (0, math.pi, 0), 1.6, 1.1, "Art_S1", "modern"),
        ((0, 3.94, 1.65), (0, math.pi, 0), 1.0, 1.4, "Art_S2", "wood"),
        ((3, 3.94, 1.6), (0, math.pi, 0), 1.8, 1.2, "Art_S3", "gilt"),
    ]
    
    for loc, rot, w, h, name, ftype in painting_specs:
        create_painting_frame(loc, rot, w, h, name, ftype)
    
    # Lighting
    print("[8/8] Setting up lighting...")
    setup_lighting()
    
    # Camera and render
    setup_camera()
    setup_render()
    
    # Export
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
    os.makedirs(output_dir, exist_ok=True)
    
    export_path = os.path.join(output_dir, "gallery_pro.glb")
    export_glb(export_path)
    
    blend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gallery_pro.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    
    print("\n" + "="*60)
    print("SCENE COMPLETE")
    print(f"  Blend file: {blend_path}")
    print(f"  GLB export: {export_path}")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
