# Blender Scene Files

This directory contains the Blender project files for the gallery.

## Files to Create

- `gallery.blend` - Main Blender project file
- `exports/` - Exported GLB/GLTF files for web use
- `models/` - External downloaded models
- `textures/` - Baked texture maps

## Export Process

1. Open `gallery.blend` in Blender
2. Model the gallery room and furniture
3. Apply textures and lighting
4. Bake lighting to textures (Cycles render)
5. Export as GLB: File > Export > glTF 2.0 (.glb)
6. Place exports in `exports/` directory
7. Copy to `public/models/` for web use

## Recommended Settings

- Room dimensions: 12m x 8m x 3.5m
- Export format: GLB (binary)
- Texture resolution: 2048px max
- Target polycount: Under 100k per model
