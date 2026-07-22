import bpy
import math

print("\n=== ROOM BOUNDS ===")
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        if 'Wall' in obj.name or 'Floor' in obj.name or 'Ceiling' in obj.name:
            print(f"{obj.name}: loc=({obj.location.x:.2f}, {obj.location.y:.2f}, {obj.location.z:.2f}) rot=({math.degrees(obj.rotation_euler.x):.1f}, {math.degrees(obj.rotation_euler.y):.1f}, {math.degrees(obj.rotation_euler.z):.1f})")

print("\n=== PAINTINGS ===")
for obj in bpy.data.objects:
    if obj.type == 'MESH' and 'Canvas' in obj.name:
        print(f"{obj.name}: loc=({obj.location.x:.2f}, {obj.location.y:.2f}, {obj.location.z:.2f}) rot=({math.degrees(obj.rotation_euler.x):.1f}, {math.degrees(obj.rotation_euler.y):.1f}, {math.degrees(obj.rotation_euler.z):.1f})")

print("\n=== SCULPTURES ===")
for obj in bpy.data.objects:
    if obj.type == 'MESH' and ('Abstract' in obj.name or 'Geo_' in obj.name):
        print(f"{obj.name}: loc=({obj.location.x:.2f}, {obj.location.y:.2f}, {obj.location.z:.2f})")
