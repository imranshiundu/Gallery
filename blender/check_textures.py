import bpy

for obj in bpy.data.objects:
    if obj.type != 'MESH':
        continue
    for mat in obj.data.materials:
        if not mat or not mat.use_nodes:
            continue
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                img_name = node.image.name if node.image else "none"
                print(f"{obj.name}: {node.name} -> img={img_name}")
                break
