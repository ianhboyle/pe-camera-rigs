# Isometric Camera Rig - Developer Guide

**Location**: `src/pe_camera_rigs/rigs/isometric/`

## Overview

Creates true isometric and axonometric projection views using Geometry Nodes. The rig provides real-time control over orthographic camera angles with mathematically correct presets.

## Module Structure

```
isometric/
├── __init__.py          # Registration
├── operators.py         # ISOMETRIC_OT_add_controller
├── panels.py            # ISOMETRIC_PT_add_panel
└── properties.py        # Property groups and update callbacks
```

## Architecture

### Interactive Rig Pattern

The Isometric rig uses the **Interactive Rig** architecture:
- Single operator creates complete rig
- Geometry Nodes for procedural positioning
- Controls via both Modifier Properties AND custom property UI
- Property update callbacks sync UI to modifier

### Created Objects

- **Template Camera**: `Isometric_Template_Cam` (hidden)
  - Hidden camera object that GN instances
  - Must be linked to collection to persist
  - Set to Orthographic projection

- **Controller**: `Isometric_Controller` (Empty, Plain Axes display)
  - Geometry Nodes modifier applied here
  - Custom properties for UI control
  - User-facing object in viewport

## Implementation Details

### Property Groups

**PE_IsometricCameraAddProps** (Scene-level):
- Stores initial preset selection for add panel
- Property: `bpy.types.Scene.pe_iso_cam_add_props`

**PE_IsometricCameraSettings** (Object-level):
- Stores runtime controller settings
- Property: `bpy.types.Object.pe_iso_cam`
- Includes update callbacks that modify GN modifier

### Projection Type Presets

**7 Presets Available** (defined in `properties.py:PROJECTION_TYPES`):

| Preset | Tilt Angle | Description |
|--------|-----------|-------------|
| GAME_2_1 | 26.565° | 2:1 pixel art ratio |
| GAME_4_3 | 30° | 4:3 pixel art ratio |
| TRUE_ISOMETRIC | 35.264° | Mathematically correct isometric |
| DIMETRIC | 30° | Common artistic variation |
| MILITARY | 90° | Top-down view |
| CAVALIER | 0° tilt, 45° roll | Front-facing with depth |
| CUSTOM | User-defined | Custom rotation/tilt/roll values |

### Node Group Inputs

Defined in `src/pe_camera_rigs/utils/nodes.py:create_isometric_camera_node_group()`

**Input Socket Order** (critical for modifier access):
- Socket_0: Camera Template (Object)
- Socket_1: Projection Type (Int, 0-6)
- Socket_2: Ortho Scale (Float)
- Socket_3: Custom Rotation Z (Float, radians)
- Socket_4: Custom Tilt X (Float, radians)
- Socket_5: Custom Roll Y (Float, radians)

**Note**: Socket names use Socket_N format (not named), accessed by index in update callbacks.

## Property Update Callbacks

**Critical Feature**: The Isometric rig implements update callbacks that sync UI properties to modifier inputs.

### Update Callback Pattern

```python
def update_projection_type(self, context):
    """Update modifier when projection type changes"""
    # Only update if this is a controller object (Empty with modifier)
    if self.id_data.type != 'EMPTY':
        return

    modifier = self.id_data.modifiers.get('Isometric Camera')
    if modifier and modifier.node_group:
        # Convert projection type string to index
        projection_index = PROJECTION_TYPE_TO_INDEX.get(self.projection_type, 2)
        modifier["Socket_1"] = projection_index

        # Force viewport update
        context.view_layer.update()
```

**Key Points:**
- `self.id_data` references the object (controller) that owns the property
- Must check object type to avoid errors on other objects
- Modifier accessed by name: `'Isometric Camera'`
- Modifier inputs accessed by socket index: `modifier["Socket_N"]`
- Must call `context.view_layer.update()` to refresh viewport

### All Update Callbacks

1. **update_projection_type**: Sets Socket_1 (projection type index)
2. **update_ortho_scale**: Sets Socket_2 (ortho scale)
3. **update_custom_rotation_z**: Sets Socket_3 (converts degrees → radians)
4. **update_custom_tilt_x**: Sets Socket_4 (converts degrees → radians)
5. **update_custom_roll_y**: Sets Socket_5 (converts degrees → radians)

**Angle Conversion**: UI properties use degrees (user-friendly), but GN modifier requires radians:
```python
modifier["Socket_3"] = math.radians(self.custom_rotation_z)
```

## Operator Execution Flow

```python
def execute(self, context):
    # 1. Validate preset
    # 2. Create template camera (hidden, orthographic)
    # 3. Create node group
    # 4. Create controller empty
    # 5. Add GN modifier to controller
    # 6. Set initial modifier values from preset
    # 7. Initialize custom properties on controller
    # 8. Update depsgraph to generate camera instance
    # 9. Set active camera
```

### Key Implementation Patterns

**Template Camera Setup:**
```python
template_cam_data = bpy.data.cameras.new(name="Isometric_Template_CamData")
template_cam_data.type = 'ORTHO'  # Critical for isometric projection
template_cam_data.ortho_scale = 10.0
template_cam_obj = bpy.data.objects.new(name=ISOMETRIC_TEMPLATE_CAM_NAME,
                                         object_data=template_cam_data)
template_cam_obj.hide_set(True)
template_cam_obj.hide_render = True
context.collection.objects.link(template_cam_obj)
```

**Custom Property Initialization:**
```python
# Initialize custom properties on controller
# This makes them appear in UI and triggers update callbacks
controller.pe_iso_cam.projection_type = self.preset
controller.pe_iso_cam.ortho_scale = 10.0

# For CUSTOM preset, set custom angles
if self.preset == 'CUSTOM':
    controller.pe_iso_cam.custom_rotation_z = 45.0
    controller.pe_iso_cam.custom_tilt_x = 35.264
    controller.pe_iso_cam.custom_roll_y = 0.0
```

## Error Handling

Similar to Orbit rig, with specific exception handling:

```python
try:
    # Validate preset
    if self.preset not in valid_presets:
        self.report({'ERROR'}, f"Invalid preset: {self.preset}")
        return {'CANCELLED'}

    # Create rig...

except AttributeError as e:
    self.report({'ERROR'}, f"Node/Depsgraph error: {str(e)}")
    # Cleanup
    return {'CANCELLED'}
except RuntimeError as e:
    self.report({'ERROR'}, f"Blender API error: {str(e)}")
    # Cleanup
    return {'CANCELLED'}
```

## User Workflow

1. User selects preset in UI panel
2. Clicks "Add Isometric Camera"
3. Controller created at world origin
4. Camera generated as child instance
5. User adjusts settings in Modifier Properties OR custom property panel
6. Update callbacks sync property changes to modifier in real-time

**User Control Points:**
- Projection Type: Dropdown selector (7 presets)
- Orthographic Scale: Zoom level
- Custom Rotation Z: Horizontal rotation (custom preset only)
- Custom Tilt X: Vertical tilt (custom preset only)
- Custom Roll Y: Camera roll (custom preset only)

## Testing Checklist

- [ ] Each preset creates rig successfully
- [ ] Template camera is hidden and orthographic
- [ ] Controller visible and selectable
- [ ] Projection type dropdown works in UI
- [ ] Changing projection type updates camera angle immediately
- [ ] Ortho scale adjustment works
- [ ] Custom preset shows custom angle inputs
- [ ] Custom angle inputs update camera in real-time
- [ ] Active camera set correctly
- [ ] Rig survives .blend save/reload
- [ ] Update callbacks work after reload

## Known Limitations

### Blender Issue #87006

**Problem**: Object properties (`bpy.types.Object.pe_iso_cam`) do NOT trigger update callbacks reliably when:
- The property owner object is not selected
- Changes made via Python API (not UI interaction)

**Impact**: Update callbacks may not fire when:
- Modifying properties via scripts
- Properties changed while object is not active

**Workaround**: User must select the Isometric_Controller object to ensure callbacks work.

**Reference**: https://projects.blender.org/blender/blender/issues/87006

### Socket Naming Limitation

Modifier inputs use generic `Socket_N` names instead of descriptive names. This is because:
- Socket names with spaces/special characters are sanitized
- Index-based access is more reliable for callbacks

**Example**:
```python
# This works reliably:
modifier["Socket_1"] = projection_index

# This may break if socket name changes:
modifier["Projection Type"] = projection_index
```

## Node Group Implementation

The geometry node group uses a switch-chain pattern:

```
Compare nodes → Switch nodes → Rotation values
```

Each preset has predefined XYZ rotation values (Tilt X, Roll Y, Rotation Z). Custom preset reads from separate input sockets.

**See**: `src/pe_camera_rigs/utils/nodes.py:create_isometric_camera_node_group()` for full implementation.

## Related Files

- `src/pe_camera_rigs/utils/nodes.py` - `create_isometric_camera_node_group()`
- `src/pe_camera_rigs/utils/blender.py` - `set_modifier_input()`
- `src/pe_camera_rigs/constants.py` - Object name constants

## Recent Changes (v1.1+)

- **2025-12-08**: Added property update callbacks for real-time UI control
- **2025-12-08**: Implemented 7 projection type presets with correct angles
- **2025-12-08**: Added comprehensive error handling with cleanup

## See Also

- [Rig System Architecture](./README.md)
- [Orbit Rig](./orbit.md) - Similar GN-based architecture without callbacks
- [Geometry Nodes Utilities](../utils.md#geometry-nodes-utilities)
