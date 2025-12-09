# Orbit Camera Rig - Developer Guide

**Location**: `src/pe_camera_rigs/rigs/orbit/`

## Overview

Creates procedural turntable animations using Geometry Nodes. The rig provides real-time control over orbital camera movement without keyframes.

## Module Structure

```
orbit/
├── __init__.py          # Registration
├── operators.py         # ORBIT_OT_add_controller
└── panels.py            # ORBIT_PT_add_panel
```

**Note**: The Orbit rig does NOT use a `properties.py` file. Settings are controlled directly through modifier properties, not custom property groups.

## Architecture

### Interactive Rig Pattern

The Orbit rig uses the **Interactive Rig** architecture:
- Single operator creates complete rig
- Geometry Nodes for procedural animation
- All controls via Modifier Properties
- Animation driven by scene frame number

### Created Objects

- **Template Camera**: `Orbit_Template_Cam` (hidden)
  - Hidden camera object that GN instances
  - Must be linked to collection to persist

- **Controller**: `Orbit_Controller` (Empty, Sphere display)
  - Geometry Nodes modifier applied here
  - User-facing object in viewport

## Implementation Details

### Operator: ORBIT_OT_add_controller

**bl_idname**: `cgt.add_orbit_controller`

**Presets** (6 available):
- `PRODUCT`: Standard product photography (radius 3.0, height 1.5, 35mm)
- `DETAIL`: Close-up jewelry shots (radius 1.5, height 0, 85mm)
- `CHARACTER`: Character turnarounds (radius 4.0, height 1.6, 50mm)
- `HERO`: Dramatic reveals (radius 2.5, height 0.5, 24mm)
- `ARCHITECTURAL`: Building walkarounds (radius 15.0, height 2.0, 35mm)
- `ENVIRONMENT`: Large scene tours (radius 20.0, height 3.0, 28mm)

### Node Group Inputs

Defined in `src/pe_camera_rigs/utils/nodes.py:create_orbit_camera_node_group()`

**Input Socket Order** (critical for modifier access):
1. Socket_0: Camera Template Object (Object)
2. Socket_1: Orbit Radius (Float)
3. Socket_2: Camera Height (Float)
4. Socket_3: Focal Length (Float)
5. Socket_4: Duration (Frames) (Int)
6. Socket_5: Speed Multiplier (Float)
7. Socket_6: Reverse Direction (Bool)
8. Socket_7: Easing (Int: 0=Linear, 1=Ease In/Out, 2=Ease In, 3=Ease Out)

### Operator Execution Flow

```python
def execute(self, context):
    # 1. Validate preset
    # 2. Create template camera (hidden)
    # 3. Create node group
    # 4. Create controller empty
    # 5. Add GN modifier to controller
    # 6. Set initial values from preset
    # 7. Update depsgraph to generate camera instance
    # 8. Set active camera
```

### Key Implementation Patterns

**Template Camera Pattern:**
```python
# Camera data must exist for GN to instance
template_cam_data = bpy.data.cameras.new(name="Orbit_Template_CamData")
template_cam_obj = bpy.data.objects.new(name=ORBIT_TEMPLATE_CAM_NAME,
                                         object_data=template_cam_data)
template_cam_obj.hide_set(True)
template_cam_obj.hide_render = True
context.collection.objects.link(template_cam_obj)  # Critical: must link to save
```

**Modifier Input Setting:**
```python
# Use name-based access (robust)
from ...utils.blender import set_modifier_input

set_modifier_input(mod, "Orbit Radius", initial_values['radius'])
set_modifier_input(mod, "Camera Height", initial_values['height'])

# Easing requires int mapping
easing_map = {"LINEAR": 0, "EASE_IN_OUT": 1, "EASE_IN": 2, "EASE_OUT": 3}
set_modifier_input(mod, "Easing", easing_map.get(initial_values['easing'], 0))
```

**Depsgraph Update:**
```python
# After modifier creation, update depsgraph to generate instances
context.view_layer.update()
depsgraph = context.evaluated_depsgraph_get()

# Find the generated camera instance
camera_instance = None
for instance in depsgraph.object_instances:
    if instance.parent == controller.original:
        if instance.object.data and isinstance(instance.object.data, bpy.types.Camera):
            camera_instance = instance.object
            break
```

## Error Handling

The operator implements comprehensive error handling:

```python
try:
    # Create objects and modifiers
    # ...
except AttributeError as e:
    self.report({'ERROR'}, f"Node/Depsgraph error: {str(e)}")
    # Cleanup partial objects
    if template_cam_obj and template_cam_obj.name in bpy.data.objects:
        bpy.data.objects.remove(template_cam_obj, do_unlink=True)
    if controller and controller.name in bpy.data.objects:
        bpy.data.objects.remove(controller, do_unlink=True)
    return {'CANCELLED'}
except RuntimeError as e:
    self.report({'ERROR'}, f"Blender API error: {str(e)}")
    # Cleanup (same as above)
    return {'CANCELLED'}
```

**Validations performed:**
- Preset exists in ORBIT_PRESETS
- Node group created successfully
- Node group has required input count (8 minimum)
- Camera template set successfully

## User Workflow

1. User selects preset in UI panel
2. Clicks "Add Orbit Camera"
3. Controller created at world origin
4. Camera generated as child instance
5. User adjusts settings in Modifier Properties panel
6. Animation plays based on scene frame number

**User Control Points:**
- Orbit Radius: Distance from center
- Camera Height: Vertical offset
- Focal Length: Camera lens setting
- Duration: Animation length in frames
- Speed Multiplier: Animation speed adjustment
- Reverse Direction: Clockwise/counter-clockwise
- Easing: Animation curve type

## Testing Checklist

- [ ] Each preset creates rig successfully
- [ ] Template camera is hidden in viewport and render
- [ ] Controller visible and selectable
- [ ] Modifier properties accessible
- [ ] Camera animates on playback
- [ ] All easing modes work
- [ ] Reverse direction functions
- [ ] Active camera set correctly
- [ ] Rig survives .blend save/reload

## Known Limitations

1. **Template camera must stay linked**: Deleting it breaks the rig
2. **Modifier property editing**: Users must know to check Modifier Properties panel
3. **No update callbacks**: Unlike Isometric rig, Orbit has no property update callbacks for UI properties

## Related Files

- `src/pe_camera_rigs/utils/nodes.py` - `create_orbit_camera_node_group()`
- `src/pe_camera_rigs/utils/blender.py` - `set_modifier_input()`
- `src/pe_camera_rigs/constants.py` - Object name constants

## See Also

- [Rig System Architecture](./README.md)
- [Isometric Rig](./isometric.md) - Similar GN-based architecture
- [Geometry Nodes Utilities](../utils.md#geometry-nodes-utilities)
