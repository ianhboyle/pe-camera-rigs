# Utilities Reference

**Location**: `src/pe_camera_rigs/utils/`

## Overview

Shared utility functions used across all camera rigs. Provides helpers for Blender API operations, Geometry Nodes creation, and scene setup.

## Module Structure

```
utils/
├── blender.py           # Blender API utilities
├── nodes.py             # Geometry Nodes creation
└── scene_setup.py       # Scene setup helpers (lighting, cyclorama)
```

---

## blender.py - Blender API Utilities

General-purpose Blender API helper functions.

### detect_and_enable_gpu()

**Purpose**: Detect and enable GPU rendering if available.

**Signature**:
```python
def detect_and_enable_gpu() -> str | None
```

**Returns**: Name of enabled GPU device, or None if no GPU found.

**Supported GPU Types**:
- CUDA (NVIDIA)
- OptiX (NVIDIA)
- HIP (AMD)
- Metal (Apple Silicon)
- OneAPI (Intel)

**Example**:
```python
from ...utils.blender import detect_and_enable_gpu

gpu_name = detect_and_enable_gpu()
if gpu_name:
    self.report({'INFO'}, f"GPU rendering enabled: {gpu_name}")
else:
    self.report({'WARNING'}, "No GPU available, using CPU")
```

**Error Handling**: Safe to call even if no GPU is available or Cycles addon is not loaded.

---

### validate_output_path(filepath, scene=None)

**Purpose**: Validates that a render output path is writable and has sufficient disk space.

**Signature**:
```python
def validate_output_path(filepath: str, scene: bpy.types.Scene | None = None) -> tuple[bool, str]
```

**Parameters**:
- `filepath`: Render output path (supports Blender path tokens like `//`)
- `scene`: Scene to use for path expansion (defaults to current scene)

**Returns**: Tuple of `(is_valid: bool, error_message: str)`

**Checks Performed**:
1. Expands Blender path tokens (`//`, `///`)
2. Verifies parent directory exists
3. Verifies directory is writable
4. Warns if less than 1GB disk space available

**Example**:
```python
from ...utils.blender import validate_output_path

valid, error = validate_output_path(settings.output_path)
if not valid:
    self.report({'ERROR'}, f"Invalid output path: {error}")
    return {'CANCELLED'}
```

**Platform Notes**: Disk space check skipped on Windows (statvfs not available).

---

### get_active_camera_or_create(context)

**Purpose**: Get the active scene camera, or create one if none exists.

**Signature**:
```python
def get_active_camera_or_create(context: bpy.types.Context) -> bpy.types.Object
```

**Returns**: The active camera object.

**Behavior**:
- If `context.scene.camera` exists, returns it
- Otherwise, creates default camera named "Camera"

**Example**:
```python
from ...utils.blender import get_active_camera_or_create

camera = get_active_camera_or_create(context)
context.scene.camera = camera
```

---

### safe_object_delete(obj, do_unlink=True)

**Purpose**: Safely delete an object with existence checking.

**Signature**:
```python
def safe_object_delete(obj: bpy.types.Object | None, do_unlink: bool = True) -> bool
```

**Parameters**:
- `obj`: Object to delete (can be None)
- `do_unlink`: Whether to unlink from all collections

**Returns**: True if deleted, False if object was None or already deleted.

**Example**:
```python
from ...utils.blender import safe_object_delete

# Cleanup in error handler
if safe_object_delete(template_cam_obj):
    self.report({'INFO'}, "Cleaned up template camera")
```

---

### set_modifier_input(modifier, socket_name, value)

**Purpose**: Safely set a Geometry Nodes modifier input by socket name.

**Signature**:
```python
def set_modifier_input(modifier: bpy.types.Modifier, socket_name: str, value: Any) -> bool
```

**Parameters**:
- `modifier`: The Geometry Nodes modifier
- `socket_name`: Name of the input socket
- `value`: Value to set (type depends on socket)

**Returns**: True if successful, False otherwise.

**Why Name-Based?**: More robust than index-based access when node groups change.

**Example**:
```python
from ...utils.blender import set_modifier_input

modifier = controller.modifiers.get('Orbit Camera')
if not set_modifier_input(modifier, "Orbit Radius", 3.0):
    self.report({'ERROR'}, "Failed to set orbit radius")
    return {'CANCELLED'}
```

**Implementation**: Searches node group inputs by name, then sets via `identifier`.

---

## nodes.py - Geometry Nodes Creation

Functions that create complete Geometry Node groups for camera rigs.

### create_orbit_camera_node_group()

**Purpose**: Creates the Geometry Node group for the Orbit camera rig.

**Signature**:
```python
def create_orbit_camera_node_group() -> bpy.types.GeometryNodeTree
```

**Returns**: The created node group.

**Node Group Inputs** (in order):
1. **Socket_0**: Camera Template Object (Object)
2. **Socket_1**: Orbit Radius (Float, default 3.0)
3. **Socket_2**: Camera Height (Float, default 1.5)
4. **Socket_3**: Focal Length (Float, default 35.0)
5. **Socket_4**: Duration (Frames) (Int, default 240)
6. **Socket_5**: Speed Multiplier (Float, default 1.0)
7. **Socket_6**: Reverse Direction (Bool, default False)
8. **Socket_7**: Easing (Int, 0-3)

**Implementation**:
- Uses current frame number to drive rotation
- Instances template camera at calculated position
- Applies easing curves (Linear, Ease In/Out, Ease In, Ease Out)

**Example**:
```python
from ...utils.nodes import create_orbit_camera_node_group

node_group = create_orbit_camera_node_group()
modifier = controller.modifiers.new(name="Orbit Camera", type='NODES')
modifier.node_group = node_group
```

---

### create_isometric_camera_node_group()

**Purpose**: Creates the Geometry Node group for the Isometric camera rig.

**Signature**:
```python
def create_isometric_camera_node_group() -> bpy.types.GeometryNodeTree
```

**Returns**: The created node group.

**Node Group Inputs** (in order):
1. **Socket_0**: Camera Template (Object)
2. **Socket_1**: Projection Type (Int, 0-6)
3. **Socket_2**: Ortho Scale (Float, default 10.0)
4. **Socket_3**: Custom Rotation Z (Float, radians)
5. **Socket_4**: Custom Tilt X (Float, radians)
6. **Socket_5**: Custom Roll Y (Float, radians)

**Projection Types**:
- 0: GAME_2_1 (26.565°)
- 1: GAME_4_3 (30°)
- 2: TRUE_ISOMETRIC (35.264°)
- 3: DIMETRIC (30°)
- 4: MILITARY (90°)
- 5: CAVALIER (0° tilt, 45° roll)
- 6: CUSTOM (use Socket_3, 4, 5)

**Implementation**:
- Switch chain for preset selection
- Compare nodes + Switch nodes → rotation values
- Custom angles read from separate sockets (Socket_3, 4, 5)
- Set Camera node configures orthographic scale

**Example**:
```python
from ...utils.nodes import create_isometric_camera_node_group

node_group = create_isometric_camera_node_group()
modifier = controller.modifiers.new(name="Isometric Camera", type='NODES')
modifier.node_group = node_group
```

---

## scene_setup.py - Scene Setup Helpers

Functions for creating lighting setups, cycloramas, and reference objects.

### create_cyclorama(context, size, color)

**Purpose**: Creates a mesh-based cyclorama stage.

**Signature**:
```python
def create_cyclorama(context: bpy.types.Context, size: str, color: str) -> bpy.types.Object
```

**Parameters**:
- `size`: 'SMALL' (10m), 'MEDIUM' (20m), 'LARGE' (30m)
- `color`: 'WHITE', 'GRAY', 'BLACK'

**Returns**: The cyclorama object.

**Implementation**:
1. Creates plane at origin
2. Extrudes back edge upward to create wall
3. Adds Bevel modifier (curved corner)
4. Adds Subdivision Surface modifier (smooth)
5. Applies material with specified color

**Color Values**:
- WHITE: (0.8, 0.8, 0.8) - High-key lighting
- GRAY: (0.18, 0.18, 0.18) - Neutral gray (18% reflectance)
- BLACK: (0.01, 0.01, 0.01) - Low-key/dramatic

**Example**:
```python
from ...utils.scene_setup import create_cyclorama

if settings.include_cyclorama:
    cyc_obj = create_cyclorama(context, settings.cyclorama_size, settings.cyclorama_color)
```

---

### create_lighting_preset(context, preset)

**Purpose**: Creates a set of lights based on a preset name.

**Signature**:
```python
def create_lighting_preset(context: bpy.types.Context, preset: str) -> None
```

**Parameters**:
- `preset`: Lighting preset name

**Presets Available**:

#### 3POINT_STUDIO
Classic 3-point studio lighting:
- **Key Light**: Area light at (3, -3, 3), 1600W energy
- **Fill Light**: Area light at (-3, -3, 2), 500W energy, 5m size
- **Rim Light**: Point light at (-2, 4, 2), 900W energy

#### 3POINT_OUTDOOR
Outdoor 3-point with sun:
- Similar to studio but with sun light instead of area lights
- Higher energy values for outdoor brightness

**Example**:
```python
from ...utils.scene_setup import create_lighting_preset

if settings.lighting_preset != 'NONE':
    create_lighting_preset(context, settings.lighting_preset)
```

---

### create_person_reference(context)

**Purpose**: Creates a 1.7m tall reference mesh for scale.

**Signature**:
```python
def create_person_reference(context: bpy.types.Context) -> bpy.types.Object
```

**Returns**: The reference object.

**Implementation**: Creates a simple mesh approximately human-sized (1.7m tall).

**Example**:
```python
from ...utils.scene_setup import create_person_reference

if settings.include_reference:
    ref_obj = create_person_reference(context)
```

---

## Common Usage Patterns

### Error-Safe Rig Creation

```python
from ...utils.blender import safe_object_delete

template_cam = None
controller = None

try:
    # Create rig...
    template_cam = bpy.data.objects.new(...)
    controller = bpy.data.objects.new(...)
    # ...
except RuntimeError as e:
    # Cleanup on failure
    safe_object_delete(template_cam)
    safe_object_delete(controller)
    self.report({'ERROR'}, f"Failed to create rig: {str(e)}")
    return {'CANCELLED'}
```

### Modifier Input Setting

```python
from ...utils.blender import set_modifier_input

# Prefer name-based access
if not set_modifier_input(modifier, "Radius", 3.0):
    self.report({'ERROR'}, "Node group missing 'Radius' input")
    return {'CANCELLED'}
```

### Scene Setup

```python
from ...utils.scene_setup import create_lighting_preset, create_cyclorama

# Add lighting
if settings.lighting_preset != 'NONE':
    create_lighting_preset(context, settings.lighting_preset)

# Add cyclorama
if settings.include_cyclorama:
    create_cyclorama(context, settings.cyclorama_size, settings.cyclorama_color)
```

---

## Testing Checklist

### blender.py
- [ ] GPU detection works on CUDA/OptiX/HIP/Metal/OneAPI
- [ ] GPU detection safe when no GPU available
- [ ] Path validation detects non-existent directories
- [ ] Path validation detects unwritable directories
- [ ] Path validation warns on low disk space
- [ ] Camera creation works when no camera exists
- [ ] Safe object delete handles None objects
- [ ] Modifier input setting works by name

### nodes.py
- [ ] Orbit node group creates successfully
- [ ] Orbit inputs in correct order
- [ ] Isometric node group creates successfully
- [ ] Isometric inputs in correct order
- [ ] All projection presets have correct angles
- [ ] Custom preset reads from Socket_3, 4, 5

### scene_setup.py
- [ ] Cyclorama sizes create correct dimensions
- [ ] Cyclorama colors apply correctly
- [ ] Lighting presets create all lights
- [ ] Person reference is correct height (1.7m)

---

## Related Files

- `src/pe_camera_rigs/constants.py` - Object name constants
- Individual rig `operators.py` - Consumers of these utilities

---

## See Also

- [Rig System Architecture](./rigs/README.md)
- [Orbit Rig](./rigs/orbit.md) - Uses `create_orbit_camera_node_group()`
- [Isometric Rig](./rigs/isometric.md) - Uses `create_isometric_camera_node_group()`
- [VR Rigs](./rigs/vr180.md) - Use scene_setup utilities
