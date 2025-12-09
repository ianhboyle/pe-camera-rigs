# Rig System Architecture

This document describes the core rig system architecture and patterns used across all camera rigs in the PE Camera Rigs addon.

## Module Structure

All rigs are located in `src/pe_camera_rigs/rigs/` with the following standard structure:

```
rig_name/
├── __init__.py          # Registration and class list
├── operators.py         # Blender operators (actions/commands)
├── panels.py            # UI panels (child of main panel)
├── properties.py        # Property groups (settings)
└── rig.py              # Core rig creation logic (VR rigs only)
```

## Two Distinct Architectures

### Interactive Rigs (Orbit, Isometric)

**Characteristics:**
- Built with Geometry Nodes for real-time, procedural control
- All controls accessible in Modifier Properties after creation
- No multi-step workflow; single operator creates complete rig
- Animation driven by scene frame number, not keyframes
- Use presets to initialize modifier values

**Implementation Pattern:**
1. Create template camera object (hidden)
2. Create controller empty
3. Apply Geometry Nodes modifier to controller
4. Node group instances the template camera
5. User controls rig via modifier properties

**Benefits:**
- Non-destructive
- Real-time preview
- No keyframe management
- Fully procedural

**See Also:**
- [Orbit Rig](./orbit.md)
- [Isometric Rig](./isometric.md)

### Workflow Rigs (VR180, VR360 Mono)

**Characteristics:**
- Multi-step production pipeline (4 steps: Scene Setup → Render Sequences → Compositing → Export)
- Each step is a separate operator, presented as numbered buttons in the UI
- Designed for crash-safe VR content production
- Use custom property groups stored on Scene and Object
- Operators read settings from properties, execute workflow step

**Implementation Pattern:**
1. Step 1: Create scene with camera rig and settings
2. Step 2: Render sequences (left/right or panoramic)
3. Step 3: Set up compositor nodes
4. Step 4: Render final output and inject VR metadata

**Benefits:**
- Crash-safe (can resume at any step)
- Clear workflow progression
- Organized file outputs
- Production-ready

**See Also:**
- [VR180 Rig](./vr180.md)
- [VR360 Mono Rig](./vr360mono.md)

## Property Storage Patterns

### Scene Properties
For scene-wide settings:

```python
bpy.types.Scene.pe_rig_settings = bpy.props.PointerProperty(type=PE_RigSettings)
```

Access via: `context.scene.pe_rig_settings`

### Object Properties
For rig-specific settings:

```python
bpy.types.Object.pe_rig_specific_settings = bpy.props.PointerProperty(type=PE_RigSpecificSettings)
```

Access via: `rig_object.pe_rig_specific_settings`

## Property Registration Pattern

**Standard pattern** (used by all rigs):

Each rig's `properties.py` should define its PropertyGroups AND handle registration:

```python
# properties.py
class PE_RigSettings(bpy.types.PropertyGroup):
    # ... property definitions

def register():
    bpy.utils.register_class(PE_RigSettings)
    bpy.types.Scene.pe_rig_settings = bpy.props.PointerProperty(type=PE_RigSettings)

def unregister():
    del bpy.types.Scene.pe_rig_settings
    bpy.utils.unregister_class(PE_RigSettings)
```

Then call from `__init__.py`:

```python
# __init__.py
def register():
    properties.register()  # Must come before classes that use the properties
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    properties.unregister()  # Unregister properties last
```

## Object Naming Conventions

**VR180 Rig Objects:**
- Main rig: `VR180_Rig` (NOT `VR180_Controller`)
- Left camera: `VR180_Camera_Left`
- Right camera: `VR180_Camera_Right`

**VR360 Mono Objects:**
- Camera: `VR360_Camera`

**Interactive Rig Controllers:**
- Orbit: `Orbit_Controller`
- Isometric: `Isometric_Controller`

When checking for rig existence in panels, use the exact object names created in the rig creation code.

## Geometry Nodes Pattern (Interactive Rigs)

### Template Camera Pattern
Create a hidden camera object that Geometry Nodes can instance (GN cannot create Camera data directly).

### Modifier Inputs
Node group inputs become modifier properties in the UI.

### Socket Ordering
Input socket order in `create_*_node_group()` determines modifier property indices. This is critical for property update callbacks.

### Depsgraph Updates
After creating GN modifiers, call `context.view_layer.update()` and use `depsgraph.object_instances` to find generated instances.

**Example:**
```python
# Create modifier
modifier = controller.modifiers.new(name="CameraRig", type='NODES')
modifier.node_group = node_group

# Update depsgraph to generate instances
context.view_layer.update()
depsgraph = context.evaluated_depsgraph_get()

# Find generated camera instance
for instance in depsgraph.object_instances:
    if instance.parent == controller.original:
        camera_instance = instance.object
        break
```

## Error Handling Pattern

All interactive rig operators (Orbit, Isometric) follow this pattern:

```python
def execute(self, context):
    # 1. Validate inputs first
    if self.preset not in VALID_PRESETS:
        self.report({'ERROR'}, f"Invalid preset: {self.preset}")
        return {'CANCELLED'}

    # 2. Initialize cleanup variables
    template_cam_obj = None
    controller = None

    try:
        # 3. Create objects and modifiers
        # ...

        # 4. Validate created resources
        if not node_group:
            self.report({'ERROR'}, "Failed to create node group")
            return {'CANCELLED'}

        if len(node_group.inputs) < REQUIRED_COUNT:
            self.report({'ERROR'}, "Node group missing required inputs")
            return {'CANCELLED'}

        # 5. Continue with setup
        # ...

        return {'FINISHED'}

    except AttributeError as e:
        self.report({'ERROR'}, f"Node/Depsgraph error: {str(e)}")
        # Cleanup
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

**VR Workflow operators** use specific exception types:
- File operations: `(IOError, OSError, PermissionError)`
- Render operations: `RuntimeError`
- Data access: `(KeyError, AttributeError)`
- Generic fallback with traceback logging for unexpected errors

## Common Pitfalls

1. **Property registration order**: Properties must be registered before being used in PointerProperty
2. **Template objects**: For GN camera rigs, the template camera must be linked to a collection to persist in the .blend file
3. **Depsgraph timing**: Generated GN instances only appear after `context.view_layer.update()`
4. **Panel parent IDs**: Must exactly match the parent panel's `bl_idname`
5. **Input socket indices**: In GN node groups, socket order matters for modifier access

## See Also

- [Geometry Nodes Utilities](../utils.md#geometry-nodes-utilities)
- [UI Panel System](../ui.md)
