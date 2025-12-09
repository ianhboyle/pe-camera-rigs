# VR360 Mono Rig - Developer Guide

**Location**: `src/pe_camera_rigs/rigs/vr360mono/`

## Overview

Creates a monoscopic 360° panoramic VR camera with a multi-step workflow for crash-safe production. Outputs equirectangular video suitable for YouTube VR.

## Module Structure

```
vr360mono/
├── __init__.py          # Registration
├── operators.py         # 4 workflow operators
├── panels.py            # VR360MONO_PT_panel (child of main panel)
└── properties.py        # PE_VR360MonoSceneSettings
```

**Note**: VR360 Mono does NOT use `rig.py` - camera creation is simpler and handled directly in operators.

## Architecture

### Workflow Rig Pattern

The VR360 Mono rig uses the **Workflow Rig** architecture:
- Multi-step production pipeline (4 steps)
- Each step is a separate operator
- Settings stored in property groups (Scene-level only)
- Crash-safe: can resume at any step
- Designed for production VR content

### Created Objects

- **Camera**: `VR360_Camera` (Camera, Panoramic)
  - Equirectangular panoramic camera
  - 360° × 180° full sphere capture
  - Positioned at world origin (or user-defined location)

## Implementation Details

### Property Groups

**PE_VR360MonoSceneSettings** (Scene-level only):
```python
bpy.types.Scene.pe_vr360_mono_settings = bpy.props.PointerProperty(type=PE_VR360MonoSceneSettings)
```

Properties:
- `resolution_preset`: '5K' (5120×2560), '8K' (7680×3840)
- `render_quality`: 'PREVIEW', 'PRODUCTION', 'FINAL' (sample counts)
- `output_path`: Base output directory
- `lighting_preset`: Scene lighting setup
- `include_cyclorama`: Add cyclorama stage
- `cyclorama_size`: 'SMALL', 'MEDIUM', 'LARGE' (10m/20m/30m)
- `cyclorama_color`: 'WHITE', 'GRAY', 'BLACK'
- `include_reference`: Add person-scale reference

**No Object Properties**: Unlike VR180, VR360 Mono does not store properties on the camera object.

### Camera Configuration

Single panoramic camera:

```python
cam_data = bpy.data.cameras.new("VR360_Camera_Data")
cam_data.type = 'PANO'
cam_data.cycles.panorama_type = 'EQUIRECTANGULAR'
```

**EQUIRECTANGULAR**: Full 360° × 180° spherical projection.

**Monoscopic**: Single camera, no stereo separation (simpler than VR180, smaller file sizes).

## Workflow Steps

### Step 1: Create Scene (VR360MONO_OT_CreateScene)

**bl_idname**: `vr360mono.create_scene`

**Actions:**
1. Create VR360 camera at world origin
2. Apply scene settings from property group
3. Set render resolution based on preset
4. Set render samples based on quality
5. Create output directory structure
6. Optionally add lighting preset
7. Optionally add cyclorama stage (with size/color options)
8. Optionally add person-scale reference

**Error Handling:**
- `RuntimeError`: Camera creation failures
- `(IOError, OSError, PermissionError)`: Output directory issues

### Step 2: Render Sequence (VR360MONO_OT_RenderSequence)

**bl_idname**: `vr360mono.render_sequence`

**Actions:**
1. Verify camera exists
2. Set output path for panoramic sequence
3. Render equirectangular frames
4. Save frames to output directory

**File Structure:**
```
output_path/
├── 0001.png
├── 0002.png
├── 0003.png
└── ...
```

**Error Handling:**
- `(KeyError, AttributeError)`: Missing camera
- `RuntimeError`: Render failures
- `(IOError, OSError, PermissionError)`: File write issues

### Step 3: Setup Compositor (VR360MONO_OT_SetupCompositor)

**bl_idname**: `vr360mono.setup_compositor`

**Actions:**
1. Enable compositor use nodes
2. Clear existing nodes
3. Create Image node for panoramic sequence
4. Create File Output node for final render
5. Connect nodes (optional color correction nodes)

**Node Layout:**
```
[Panoramic Sequence] → [Optional Color Correction] → [File Output]
```

**Simpler than VR180**: No side-by-side composition needed.

**Error Handling:**
- `(KeyError, AttributeError)`: Node access issues
- `RuntimeError`: Compositor setup failures

### Step 4: Render YouTube VR (VR360MONO_OT_RenderYouTube)

**bl_idname**: `vr360mono.render_youtube`

**Actions:**
1. Verify compositor setup
2. Render final equirectangular video
3. (Optional) Inject VR metadata using spatial-media tool
4. Output final YouTube-ready file

**Output Format:**
- Equirectangular projection
- 2:1 aspect ratio (width = 2× height)
- YouTube VR metadata (if spatial-media tool configured)

**Error Handling:**
- `RuntimeError`: Render failures
- `(IOError, OSError, PermissionError)`: File write/metadata injection issues

## User Workflow

1. **Configure settings** in VR360 Mono panel
2. **Step 1**: Click "1. Create Scene" → camera created
3. **Adjust camera** (position, rotation if needed)
4. **Step 2**: Click "2. Render Sequence" → panoramic frames rendered
5. **Step 3**: Click "3. Setup Compositor" → compositor configured
6. **Step 4**: Click "4. Render YouTube VR" → final video output

**Crash Recovery**: If Blender crashes at any step, user can restart Blender and continue from next step (previous outputs preserved).

## Comparison: VR360 Mono vs VR180

| Feature | VR360 Mono | VR180 |
|---------|-----------|--------|
| **Field of View** | 360° × 180° (full sphere) | 190° (hemisphere) |
| **Stereo** | No (monoscopic) | Yes (stereoscopic) |
| **Cameras** | 1 | 2 (left/right) |
| **File Size** | Smaller | Larger (2× views) |
| **Complexity** | Simpler | More complex |
| **Depth Perception** | None | Yes |
| **Use Cases** | Tours, landscapes, presentations | Immersive VR, depth-critical content |

## Testing Checklist

- [ ] Step 1 creates panoramic camera
- [ ] Resolution presets set correct dimensions (2:1 aspect)
- [ ] Render quality presets set correct samples
- [ ] Cyclorama size options work (SMALL/MEDIUM/LARGE)
- [ ] Cyclorama color options work (WHITE/GRAY/BLACK)
- [ ] Step 2 renders equirectangular sequence
- [ ] Output directory created correctly
- [ ] Step 3 creates compositor node setup
- [ ] Compositor processes panoramic frames
- [ ] Step 4 renders final video
- [ ] Spatial-media metadata injection (if tool configured)
- [ ] Crash recovery works (resume from any step)

## Known Limitations

1. **Cycles only**: Panoramic cameras require Cycles renderer
2. **Spatial-media tool**: Optional, must be configured in addon preferences
3. **Monoscopic only**: No depth perception (use VR180 for stereo)
4. **Large file sizes**: High-resolution equirectangular (especially 8K)
5. **Sequential workflow**: Steps must be done in order (1→2→3→4)

## Camera Technical Details

**Equirectangular Projection:**
- Maps 360° × 180° sphere to 2:1 rectangle
- Horizontal: 0° to 360° (full circle)
- Vertical: -90° to +90° (full hemisphere)
- Distortion increases near poles

**Resolution Presets:**
- 5K: 5120×2560 (YouTube standard)
- 8K: 7680×3840 (High quality)

**Recommended Aspect Ratio**: Always 2:1 (width = 2× height) for equirectangular.

## Scene Setup Options

**Cyclorama Sizes:**
- SMALL: 10m × 10m (product shots)
- MEDIUM: 20m × 20m (character showcases)
- LARGE: 30m × 30m (environmental scenes)

**Cyclorama Colors:**
- WHITE: High-key lighting
- GRAY: Neutral lighting (most versatile)
- BLACK: Low-key/dramatic lighting

**Person-Scale Reference:**
- 1.7m tall mesh for scale reference
- Helps visualize camera height and scene scale

## Related Files

- `src/pe_camera_rigs/constants.py` - Camera name constants
- `src/pe_camera_rigs/preferences.py` - `spatial_media_tool_path` preference
- `src/pe_camera_rigs/utils/scene_setup.py` - Lighting and cyclorama helpers

## Recent Changes

- **2025-12-08**: Removed non-existent `scene` module import from `__init__.py`

## See Also

- [Rig System Architecture](./README.md)
- [VR180 Rig](./vr180.md) - Stereoscopic VR workflow
- [Scene Setup Utilities](../utils.md#scene-setup-utilities)
