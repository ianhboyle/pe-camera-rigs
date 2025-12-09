# Blender Addon Best Practices - 2025 Research

**Research Date**: December 8, 2025
**Purpose**: Validate code review findings against official Blender documentation and community standards
**Scope**: Python addon development for Blender 4.0+

---

## Table of Contents

1. [Logging and Console Output](#logging-and-console-output)
2. [Property Update Callbacks with Geometry Nodes](#property-update-callbacks-with-geometry-nodes)
3. [Import Organization](#import-organization)
4. [Panel Hierarchy with bl_parent_id](#panel-hierarchy-with-bl_parent_id)
5. [Naming Conventions](#naming-conventions)
6. [Error Handling and Reporting](#error-handling-and-reporting)
7. [Depsgraph and Modifier Updates](#depsgraph-and-modifier-updates)
8. [Development Best Practices](#development-best-practices)

---

## 1. Logging and Console Output

### Official Recommendation

**Source**: [Blender Developers Blog - Logging from Python code in Blender](https://code.blender.org/2016/05/logging-from-python-code-in-blender/)

### Key Findings

1. **Use Python's standard logging module** rather than `print()` statements
2. **Do NOT configure the logging module** in your addon - users have different logging preferences
3. Users can configure logging via `$HOME/.config/blender/{version}/scripts/startup/setup_logging.py`
4. This allows developers to not have to remove all those print() statements before publishing addons

### Implementation

```python
import logging

logger = logging.getLogger(__name__)

# For informational messages
logger.info("Addon initialized")

# For warnings
logger.warning("Template camera not found, creating new one")

# For errors with full traceback
logger.exception("Unexpected error during render")  # Automatically logs traceback

# For errors without traceback
logger.error(f"Invalid preset: {preset_name}")
```

### Why This Matters

- **Addon distribution**: Print statements and `traceback.print_exc()` create console spam for users
- **User control**: Users can configure logging levels per their needs
- **Professional**: Standard Python logging is expected in production code

### Application to PE Camera Rigs

**Current Issue**: 11 instances of `traceback.print_exc()` in VR operators

**Impact**: Console spam when errors occur, violates professional addon standards

**Fix Priority**: CRITICAL - Must fix before distribution

---

## 2. Property Update Callbacks with Geometry Nodes

### Official Documentation

**Source**: [Blender Python API - Property Definitions (bpy.props)](https://docs.blender.org/api/current/bpy.props.html)

### Known Limitations

**Source**: [Issue #87006 - Geometry Node: Changing modifier input values with python no cause update](https://developer.blender.org/T87006)

### Key Findings

1. **Property update callbacks are supported** via the `update` parameter:
   ```python
   bpy.props.FloatProperty(update=update_func)
   ```

2. **Threading considerations**: Property access might happen in threaded context on a per-data-block level

3. **Critical Limitation with Geometry Nodes**:
   - When changing geometry node modifier input values via Python, the modifier UI may change but **the viewport does not update**
   - ID-properties edited via Python skip update functions since RNA properties aren't used
   - Using `update_tag()` doesn't fully work - updates once but not dynamically

4. **Developer workarounds**:
   - Some developers moved to using **drivers** as inputs for more reliable updates
   - Manual depsgraph updates may help but aren't guaranteed

### Implications for Interactive Rigs

**Current Issue**: Isometric rig properties don't update modifier inputs after creation

**Recommended Approach**:
1. **Short-term**: Implement property update callbacks with `context.view_layer.update()`
2. **Long-term**: Consider driver-based approach for more reliable updates
3. **Test thoroughly**: Viewport update behavior may be inconsistent

### Example Implementation

```python
def update_ortho_scale(self, context):
    """Update modifier when ortho_scale changes"""
    if self.id_data.type == 'EMPTY':  # This is the controller
        mod = self.id_data.modifiers.get('Isometric Camera')
        if mod and 'Ortho Scale' in mod:
            mod['Ortho Scale'] = self.ortho_scale
            # Force depsgraph update
            context.view_layer.update()
            # May also need:
            # self.id_data.update_tag()

ortho_scale: bpy.props.FloatProperty(
    name="Orthographic Scale",
    default=10.0,
    min=0.1,
    update=update_ortho_scale
)
```

### Alternative: Driver-Based Approach

```python
# Create driver from property to modifier input
def create_property_driver(controller, modifier, input_name, property_path):
    """Create driver linking property to modifier input"""
    driver = modifier[input_name].driver_add("default_value")
    var = driver.driver.variables.new()
    var.name = "prop"
    var.targets[0].id_type = 'OBJECT'
    var.targets[0].id = controller
    var.targets[0].data_path = property_path
    driver.driver.expression = "prop"
```

### Application to PE Camera Rigs

**Priority**: HIGH - Feature incomplete

**Risk**: Known Blender limitation may require alternative solution

---

## 3. Import Organization

### Official Documentation

**Source**: [Python 3 Tutorial - Modules](https://docs.python.org/3/tutorial/modules.html)

### Key Findings

1. **Standard convention**: Place all import statements at the beginning of a module
2. **Not strictly required** but highly recommended
3. **Module-level imports** add names to module's global namespace
4. **Function-level imports** can offer minor performance benefits when:
   - Function might not be called (exception handlers)
   - Accessing local variables is faster than dictionary lookups
   - But: Blurs dependencies, reduces code clarity

### Best Practice

```python
# ✅ GOOD - Module level
import bpy
import os
import traceback
import logging
from pathlib import Path

def my_function():
    logger.info("Function called")

# ❌ BAD - Function level (except rare cases)
def my_function():
    import traceback  # Don't do this
    traceback.print_exc()
```

### Exceptions

Function-level imports acceptable for:
- Avoiding circular imports (rare, indicates design issue)
- Optional dependencies (e.g., `try: import numpy`)
- Performance-critical code where function is rarely called

### Application to PE Camera Rigs

**Current Issue**: 3 instances of late imports (traceback in exception handlers, bpy.utils in register functions)

**Priority**: LOW - Style consistency, not functional issue

**Fix**: Move all imports to module level for maintainability

---

## 4. Panel Hierarchy with bl_parent_id

### Official Documentation

**Source**: [Blender Python API - Panel (bpy.types.Panel)](https://docs.blender.org/api/current/bpy.types.Panel.html)

### Community Examples

**Source**: [GitHub Gist - Example of creating sub panels in blender](https://gist.github.com/sambler/2cdafb820dfdd5044b33421d8df706e2)

### Key Findings

1. **bl_parent_id creates nested panels**: Set to parent panel's `bl_idname` string
2. **Registration order matters**: Parent panel MUST be registered before child panels
3. **Common error**: `RuntimeError: Error: Registering panel class: parent 'VIEW3D_PT_mainPanel' for 'VIEW3D_PT_subPanel' not found`

### Implementation

```python
# Parent panel
class ADDON_PT_main_panel(bpy.types.Panel):
    bl_idname = "ADDON_PT_main_panel"
    bl_label = "My Addon"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'My Tab'

# Child panel (nested under main panel)
class ADDON_PT_sub_panel(bpy.types.Panel):
    bl_parent_id = "ADDON_PT_main_panel"  # References parent
    bl_label = "Sub Section"
    bl_space_type = 'VIEW_3D'  # Must match parent
    bl_region_type = 'UI'      # Must match parent
    bl_category = 'My Tab'     # Must match parent

# Registration order
def register():
    bpy.utils.register_class(ADDON_PT_main_panel)  # Parent first
    bpy.utils.register_class(ADDON_PT_sub_panel)   # Then child
```

### Panel Ordering

Use `bl_order` to control panel display order within parent:

```python
class ADDON_PT_tools(bpy.types.Panel):
    bl_parent_id = "ADDON_PT_main_panel"
    bl_order = 1  # Appears first

class ADDON_PT_settings(bpy.types.Panel):
    bl_parent_id = "ADDON_PT_main_panel"
    bl_order = 2  # Appears second
```

### Application to PE Camera Rigs

**Current Issue**: VR180 and VR360 panels create separate top-level panels instead of nesting under main panel

**Priority**: MEDIUM - UI consistency, not functional issue

**Benefit**: Creates unified, collapsible interface

---

## 5. Naming Conventions

### Official Guidelines

**Sources**:
- [Blender Class Naming Convention](https://markbtomlinson.com/post/2022/blender-class-naming-convention/)
- [Class naming conventions in Blender 2.8 Python API](https://b3d.interplanety.org/en/class-naming-conventions-in-blender-2-8-python-api/)
- [Blender Developer Documentation - Addons](https://developer.blender.org/docs/release_notes/2.80/python_api/addons/)

### Key Conventions

#### Class Names

Format: `UPPER_CASE_{SEPARATOR}_mixed_case`

**Separators by class type**:
- **HT** - Header
- **MT** - Menu
- **OT** - Operator
- **PT** - Panel
- **UL** - UI List

**Examples**:
```python
class VIEW3D_PT_tools_active(bpy.types.Panel):  # Panel
    bl_idname = "VIEW3D_PT_tools_active"  # Matches class name

class MESH_OT_duplicate(bpy.types.Operator):    # Operator
    bl_idname = "mesh.duplicate"                 # Lowercase with dot

class VIEW3D_MT_edit_mesh(bpy.types.Menu):      # Menu
    bl_idname = "VIEW3D_MT_edit_mesh"           # Matches class name
```

#### Operator bl_idname

**Format**: `lowercase.with_dots`

**Rules**:
1. Must use lowercase
2. Separator is dot (.)
3. Convention: `category.action_name`
4. Case sensitivity matters: `ops.export_button` works, `ops.ExportButton` fails

**Examples**:
```python
# Class name uses _OT_ separator and underscores
class EXPORT_OT_custom_format(bpy.types.Operator):
    # bl_idname uses dots and lowercase
    bl_idname = "export.custom_format"
```

#### Panel bl_idname

**Format**: Matches class name (automatic if not specified)

```python
class TOOLS_PT_my_panel(bpy.types.Panel):
    bl_idname = "TOOLS_PT_my_panel"  # Same as class name
```

### Enforcement

**Not strictly enforced** - Blender won't crash if you don't follow conventions, but will raise warnings

### Application to PE Camera Rigs

**Current Naming**:
- Orbit/Isometric: `cgt.add_orbit_controller`, `cgt.add_isometric_controller`
- VR180/VR360: `vr180.create_scene`, `vr360mono.create_scene`

**Observation**: Mixed naming convention (`cgt.*` vs `vr180.*`) is functional but inconsistent

**Recommendation**: Standardize to rig-specific prefixes for clarity

**Priority**: LOW - Functional but worth standardizing

---

## 6. Error Handling and Reporting

### Community Best Practices

**Sources**:
- [Easy user error reporting for Blender Addons](https://theduckcow.com/2020/blender-addon-user-error-reporting/)
- [Developer Discussion: Handling Errors](https://devtalk.blender.org/t/developer-discussion-handling-errors/33054)

### Using self.report()

**Severity Levels**:
- `{'INFO'}` - Shows popup that automatically goes away in info area header
- `{'WARNING'}` - Shows warning message
- `{'ERROR'}` - Shows popup under cursor that doesn't go away automatically

**Example**:
```python
class MY_OT_operator(bpy.types.Operator):
    def execute(self, context):
        try:
            # Do work
            self.report({'INFO'}, "Operation completed successfully")
            return {'FINISHED'}
        except ValueError as e:
            self.report({'ERROR'}, f"Invalid value: {str(e)}")
            return {'CANCELLED'}
        except RuntimeError as e:
            self.report({'ERROR'}, f"Runtime error: {str(e)}")
            return {'CANCELLED'}
```

### Error Wrapper Pattern

**Advanced**: Wrap all operators with error-handling decorator

```python
def error_wrapper(operator_func):
    """Decorator to catch unhandled exceptions"""
    def wrapper(self, context):
        try:
            return operator_func(self, context)
        except Exception as e:
            logger.exception("Unhandled exception in operator")
            self.report({'ERROR'}, f"Unexpected error: {str(e)}")
            # Optionally: Trigger user feedback operator
            return {'CANCELLED'}
    return wrapper

class MY_OT_operator(bpy.types.Operator):
    @error_wrapper
    def execute(self, context):
        # Operator code
        pass
```

### Best Practices Summary

1. **Use appropriate severity levels** - INFO for success, WARNING for caution, ERROR for failures
2. **Return correct operator status** - `{'FINISHED'}` or `{'CANCELLED'}`
3. **Catch specific exceptions** first, then generic
4. **Clean up resources** on error
5. **Consider user error reporting** for production addons

### Application to PE Camera Rigs

**Current State**: Good error handling with specific exceptions in Orbit/Isometric operators

**Missing**: Could enhance with error wrapper pattern for comprehensive coverage

**Priority**: LOW - Current approach is solid

---

## 7. Depsgraph and Modifier Updates

### Official Documentation

**Sources**:
- [Blender Python API - Depsgraph (bpy.types.Depsgraph)](https://docs.blender.org/api/current/bpy.types.Depsgraph.html)
- [Blender Python API - NodesModifier](https://docs.blender.org/api/current/bpy.types.NodesModifier.html)

### Key Concepts

#### Getting Evaluated Depsgraph

```python
depsgraph = context.evaluated_depsgraph_get()
```

#### Getting Evaluated Object

```python
# Get object with all modifiers applied
object_eval = obj.evaluated_get(depsgraph)
mesh_eval = object_eval.data
```

#### Depsgraph Updates

```python
# Update view layer before getting depsgraph
context.view_layer.update()

# Get fresh depsgraph
depsgraph = context.evaluated_depsgraph_get()

# Iterate over object instances (geometry nodes)
for obj_instance in depsgraph.object_instances:
    if obj_instance.is_instance:
        instance_obj = obj_instance.object.original
```

### Known Issues with Geometry Nodes

**Source**: [Issue #87006](https://developer.blender.org/T87006)

1. **Problem**: Changing modifier input values via Python may not trigger viewport updates
2. **Symptom**: Modifier UI changes but viewport doesn't update
3. **Cause**: ID-properties edited via Python skip RNA update functions
4. **Workaround**: Some developers use drivers instead of direct property assignment

### Best Practices

1. **Always call `context.view_layer.update()`** before getting depsgraph
2. **Check `obj_instance.is_instance`** when iterating instances
3. **Use `obj.original`** to get the original object from evaluated instance
4. **Force updates with `obj.update_tag()`** if needed (may not work reliably with GN)

### Application to PE Camera Rigs

**Current State**: Excellent depsgraph usage in Orbit and Isometric operators

**Pattern Used**:
```python
context.view_layer.update()
depsgraph = context.evaluated_depsgraph_get()
for obj_instance in depsgraph.object_instances:
    if obj_instance.is_instance:
        instance_obj = obj_instance.object.original
        if instance_obj.type == 'CAMERA':
            # Found generated camera
```

**Priority**: Already correct - no changes needed

---

## 8. Development Best Practices

### Code Organization

**Source**: [Blender Addon Development Needs More DevOps](https://dev.to/unclepomedev/blender-addon-development-needs-more-devops-5c1e)

#### Separation of Concerns

**Best Practice**: Keep `operators.py` (interface with Blender) thin

```python
# operators.py - Thin Blender interface
class MY_OT_process(bpy.types.Operator):
    def execute(self, context):
        try:
            result = core.process_data(context.scene.data)
            self.report({'INFO'}, "Processing complete")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

# core.py - Pure Python logic (no bpy dependency)
def process_data(data):
    """Process data without Blender dependency"""
    # Can be tested without launching Blender
    return processed_result
```

**Benefits**:
- Can unit test core logic without Blender
- Easier to maintain
- Faster development iteration

#### Policy: bpy.data vs bpy.ops

**Recommendation**: "First consider operations with `bpy.data`, and only consider `bpy.ops` if absolutely necessary"

**Reason**: `bpy.ops` is a "simulation of user operations" and requires appropriate context

**Example**:
```python
# ✅ PREFERRED - Direct data manipulation
camera_data = bpy.data.cameras.new("MyCamera")
camera_obj = bpy.data.objects.new("MyCamera", camera_data)
context.collection.objects.link(camera_obj)

# ❌ AVOID - Operator simulation (context-dependent)
bpy.ops.object.camera_add(location=(0, 0, 0))
```

### Testing Recommendations

**Types of tests**:
1. **Unit tests** - For logic without Blender (core.py functions)
2. **End-to-end tests** - Run in actual Blender to verify API compatibility

### Application to PE Camera Rigs

**Current State**:
- Good separation - rig creation logic in dedicated modules
- Uses `bpy.data` appropriately, minimal `bpy.ops` usage

**Opportunity**: Could extract more node creation logic for testability

**Priority**: LOW - Current architecture is solid

---

## Summary of Key Findings

### Confirmed Best Practices

1. ✅ **Use Python logging module** instead of print/traceback.print_exc()
2. ✅ **Module-level imports** are standard convention
3. ✅ **bl_parent_id** creates proper panel hierarchies
4. ✅ **Operator naming** uses lowercase.dot_notation
5. ✅ **self.report()** with severity levels for user feedback
6. ✅ **Depsgraph updates** before evaluating geometry nodes
7. ✅ **bpy.data over bpy.ops** for direct data manipulation

### Important Limitations Discovered

1. ⚠️ **Geometry Nodes + Python property updates** have known viewport update issues
   - May require driver-based approach for reliable interactive controls
   - Testing needed to validate property update callback approach

2. ⚠️ **Panel registration order** matters for parent-child relationships
   - Parent must be registered before children

### Application to PE Camera Rigs Addon

**Validation Result**: Code review recommendations are **consistent with official Blender standards and community best practices**

**Critical Issues Confirmed**:
1. Console output via traceback.print_exc() violates logging standards
2. Property update callbacks may have limitations with GN modifiers

**All Other Recommendations Validated**:
- Import organization
- Panel hierarchy
- Naming conventions
- Error handling

---

## References

### Official Blender Documentation

1. [Blender Developers Blog - Logging from Python code](https://code.blender.org/2016/05/logging-from-python-code-in-blender/)
2. [Blender Python API - Property Definitions](https://docs.blender.org/api/current/bpy.props.html)
3. [Blender Python API - Panel](https://docs.blender.org/api/current/bpy.types.Panel.html)
4. [Blender Python API - Depsgraph](https://docs.blender.org/api/current/bpy.types.Depsgraph.html)
5. [Blender Developer Documentation - Addons](https://developer.blender.org/docs/release_notes/2.80/python_api/addons/)

### Official Python Documentation

6. [Python 3 Tutorial - Modules](https://docs.python.org/3/tutorial/modules.html)
7. [Python 3 - The import system](https://docs.python.org/3/reference/import.html)

### Blender Bug Reports & Issues

8. [Issue #87006 - Geometry Node: Changing modifier input values with python no cause update](https://developer.blender.org/T87006)

### Community Resources

9. [Blender Class Naming Convention - Mark B Tomlinson](https://markbtomlinson.com/post/2022/blender-class-naming-convention/)
10. [Class naming conventions in Blender 2.8 Python API - Interplanety](https://b3d.interplanety.org/en/class-naming-conventions-in-blender-2-8-python-api/)
11. [GitHub Gist - Example of creating sub panels](https://gist.github.com/sambler/2cdafb820dfdd5044b33421d8df706e2)
12. [Easy user error reporting for Blender Addons - The Duck Cow](https://theduckcow.com/2020/blender-addon-user-error-reporting/)
13. [Developer Discussion: Handling Errors](https://devtalk.blender.org/t/developer-discussion-handling-errors/33054)
14. [Blender Addon Development Needs More DevOps](https://dev.to/unclepomedev/blender-addon-development-needs-more-devops-5c1e)

---

**Document Version**: 1.0
**Last Updated**: December 8, 2025
**Next Review**: When upgrading to new Blender major version
