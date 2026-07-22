import bpy
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        print(f"{obj.name}: ({obj.location.x:.2f}, {obj.location.y:.2f}, {obj.location.z:.2f})")
