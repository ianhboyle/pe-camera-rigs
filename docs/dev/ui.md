# UI Development Guide

**Location**: `src/pe_camera_rigs/ui/`

## Overview

The UI system provides a unified panel hierarchy in the Blender 3D Viewport sidebar under the "PE Cams" tab. All rig-specific panels are children of a single main panel.

## Module Structure

```
ui/
├── __init__.py          # Registration
└── main_panel.py        # PE_PT_main_panel (parent panel)
```

Individual rig panels are defined in their respective rig modules:
- `rigs/orbit/panels.py` - ORBIT_PT_add_panel
- `rigs/isometric/panels.py` - ISOMETRIC_PT_add_panel
- `rigs/vr180/panels.py` - VR180_PT_panel
- `rigs/vr360mono/panels.py` - VR360MONO_PT_panel

## Panel Hierarchy

All panels follow this hierarchy:

```
PE Cams (Sidebar Tab)
└── PE_PT_main_panel (Parent)
    ├── ORBIT_PT_add_panel (Child)
    ├── ISOMETRIC_PT_add_panel (Child)
    ├── VR180_PT_panel (Child)
    └── VR360MONO_PT_panel (Child)
```

**Benefits:**
- Unified, collapsible interface
- Clear organization by rig type
- Consistent user experience

## Main Panel

**Class**: `PE_PT_main_panel`

**Location**: `src/pe_camera_rigs/ui/main_panel.py`

**Properties:**
```python
bl_idname = "PE_PT_main_panel"
bl_label = "PE Camera Rigs"
bl_space_type = 'VIEW_3D'
bl_region_type = 'UI'
bl_category = "PE Cams"
```

**Purpose:**
- Parent panel for all rig panels
- Provides top-level "PE Camera Rigs" header
- Defines sidebar tab location ("PE Cams")

**Draw Method:**
```python
def draw(self, context):
    layout = self.layout
    # Main panel is mostly a container
    # Can add top-level info or links here
```

## Child Panel Pattern

All rig panels must declare the main panel as their parent:

```python
class RIGNAME_PT_panel(bpy.types.Panel):
    """Panel for RigName camera rig"""
    bl_idname = "RIGNAME_PT_panel"
    bl_label = "Rig Name"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PE Cams"
    bl_parent_id = "PE_PT_main_panel"  # CRITICAL: declares parent

    def draw(self, context):
        layout = self.layout
        # Panel UI elements here
```

**CRITICAL**: `bl_parent_id = "PE_PT_main_panel"` must exactly match the parent panel's `bl_idname`.

## Panel Types

### Interactive Rig Panels (Orbit, Isometric)

**Pattern**: Single button to create rig + preset selector

**Example** (Orbit):
```python
def draw(self, context):
    layout = self.layout

    # Preset selector
    layout.prop(context.scene.pe_orbit_add_props, "preset", text="Preset")

    # Add button
    layout.operator("cgt.add_orbit_controller", text="Add Orbit Camera", icon='CAMERA_DATA')

    # Optional: Show info if rig exists
    if "Orbit_Controller" in bpy.data.objects:
        box = layout.box()
        box.label(text="Orbit camera active", icon='INFO')
```

**Key Elements:**
- Preset dropdown (EnumProperty from scene properties)
- Single operator button
- Optional info box showing rig status

### Workflow Rig Panels (VR180, VR360 Mono)

**Pattern**: Settings + 4 numbered workflow buttons

**Example** (VR180):
```python
def draw(self, context):
    layout = self.layout
    settings = context.scene.pe_vr180_scene_settings

    # Settings section
    box = layout.box()
    box.label(text="Settings", icon='SETTINGS')
    box.prop(settings, "resolution_preset")
    box.prop(settings, "render_quality")
    box.prop(settings, "output_path")
    box.prop(settings, "lighting_preset")
    box.prop(settings, "include_cyclorama")

    # Workflow buttons
    layout.separator()
    layout.label(text="Workflow Steps:", icon='SEQUENCE')

    layout.operator("vr180.create_scene", text="1. Create Scene", icon='SCENE_DATA')
    layout.operator("vr180.render_sequences", text="2. Render Sequences", icon='RENDER_ANIMATION')
    layout.operator("vr180.setup_compositor", text="3. Setup Compositor", icon='NODE_COMPOSITING')
    layout.operator("vr180.render_youtube", text="4. Render YouTube VR", icon='FILE_MOVIE')
```

**Key Elements:**
- Settings box (scene properties)
- Separator between settings and workflow
- Numbered workflow buttons (1, 2, 3, 4)
- Descriptive icons

## Blender API Conventions

### Panel Class Attributes

```python
bl_idname = "UNIQUE_PT_panel_name"      # Must be globally unique
bl_label = "Display Name"                # User-visible name
bl_space_type = 'VIEW_3D'                # 3D Viewport
bl_region_type = 'UI'                    # Sidebar
bl_category = "PE Cams"                  # Sidebar tab name
bl_parent_id = "PE_PT_main_panel"        # Parent panel (for children)
```

### Common Icons

- `'CAMERA_DATA'` - Camera/rig creation
- `'SCENE_DATA'` - Scene setup
- `'RENDER_ANIMATION'` - Rendering
- `'NODE_COMPOSITING'` - Compositor
- `'FILE_MOVIE'` - Video output
- `'SETTINGS'` - Settings sections
- `'SEQUENCE'` - Workflow steps
- `'INFO'` - Information boxes

### Layout Methods

```python
layout.prop(data, "property_name", text="Label")  # Property field
layout.operator("operator.idname", text="Button", icon='ICON')  # Button
layout.label(text="Text", icon='ICON')  # Static label
layout.separator()  # Spacer
box = layout.box()  # Grouped box
box.label(text="Header")
```

## Rig Existence Checks

Panels can show different UI based on whether a rig exists:

```python
def draw(self, context):
    layout = self.layout

    # Check if rig exists
    if "Orbit_Controller" in bpy.data.objects:
        layout.label(text="Orbit camera active", icon='INFO')
        layout.operator("some.edit_operator", text="Edit Settings")
    else:
        layout.label(text="No orbit camera in scene")
        layout.operator("cgt.add_orbit_controller", text="Add Orbit Camera")
```

**Object Name Constants**: Use constants from `src/pe_camera_rigs/constants.py`:
- `ORBIT_CONTROLLER_NAME = "Orbit_Controller"`
- `ISOMETRIC_CONTROLLER_NAME = "Isometric_Controller"`
- `VR180_RIG_NAME = "VR180_Rig"`
- `VR360_CAMERA_NAME = "VR360_Camera"`

**Important**: Must match exact object names created by operators.

## Property Access Patterns

### Scene Properties
```python
settings = context.scene.pe_vr180_scene_settings
layout.prop(settings, "resolution_preset")
```

### Object Properties
```python
controller = bpy.data.objects.get("Isometric_Controller")
if controller:
    layout.prop(controller.pe_iso_cam, "projection_type")
```

### Addon Preferences
```python
prefs = context.preferences.addons['pe_camera_rigs'].preferences
layout.prop(prefs, "spatial_media_tool_path")
```

## Panel Registration

Panels are registered via their module's `__init__.py`:

```python
# In rigs/orbit/__init__.py
from . import panels

classes = [
    panels.ORBIT_PT_add_panel,
    # ... other classes
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
```

**Order**: Main panel must be registered before child panels.

## Testing Checklist

- [ ] Panel appears in correct sidebar tab ("PE Cams")
- [ ] Panel is child of main panel (indented)
- [ ] Panel label displays correctly
- [ ] All properties are accessible
- [ ] All operators trigger correctly
- [ ] Icons display correctly
- [ ] Panel survives .blend save/reload
- [ ] Panel works in different Blender window layouts

## Common Pitfalls

1. **Parent ID mismatch**: `bl_parent_id` must exactly match parent's `bl_idname`
2. **Category mismatch**: All panels should use same `bl_category` ("PE Cams")
3. **Property access**: Ensure properties are registered before panel tries to access them
4. **Object name checks**: Use exact names from constants, case-sensitive
5. **Icon names**: Must use valid Blender icon identifiers (single quotes)

## UI Design Guidelines

1. **Consistency**: All rig panels should follow similar layout patterns
2. **Clarity**: Use descriptive labels and helpful icons
3. **Grouping**: Use boxes to group related settings
4. **Workflow**: For multi-step rigs, clearly number and label steps
5. **Feedback**: Show rig status (exists/doesn't exist) when relevant

## Related Files

- `src/pe_camera_rigs/ui/main_panel.py` - Main parent panel
- `src/pe_camera_rigs/constants.py` - Object name constants
- Individual rig `panels.py` files - Rig-specific panels

## See Also

- [Rig System Architecture](./rigs/README.md)
- [Property Groups Documentation](./rigs/README.md#property-storage-patterns)
