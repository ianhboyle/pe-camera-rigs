# Developer Documentation

Complete technical documentation for PE Camera Rigs addon development.

## Module Guides

### Rig System
- [Rig Architecture Overview](./rigs/README.md) - Core rig system patterns and conventions
- Individual Rigs:
  - [Orbit Camera](./rigs/orbit.md) - Procedural turntable animations with Geometry Nodes
  - [Isometric Camera](./rigs/isometric.md) - Orthographic projections and axonometric views
  - [VR180](./rigs/vr180.md) - Stereoscopic VR180 workflow pipeline
  - [VR360 Mono](./rigs/vr360mono.md) - 360° panoramic monoscopic VR

### Supporting Systems
- [UI Development](./ui.md) - Panel system, hierarchies, and UI conventions
- [Utilities](./utils.md) - Shared helper functions and Geometry Nodes utilities

## Quick Reference

### Architecture Overview

The addon uses a hierarchical registration pattern:

1. **Top-level** (`src/pe_camera_rigs/__init__.py`): Registers addon preferences and delegates to submodules
2. **Submodule level**: `ui` and `rigs` modules each have their own `register()`/`unregister()` functions
3. **Rig level**: Each rig module registers its own classes

**Important**: Always register/unregister in proper order. Classes must be registered before being assigned as `PointerProperty` types.

### Two Distinct Rig Architectures

**Interactive Rigs (Orbit, Isometric):**
- Built with Geometry Nodes for real-time, procedural control
- All controls accessible in Modifier Properties after creation
- Single operator creates complete rig
- Animation driven by scene frame number

**Workflow Rigs (VR180, VR360 Mono):**
- Multi-step production pipeline (4 steps)
- Each step is a separate operator
- Designed for crash-safe VR content production
- Use custom property groups stored on Scene and Object

### Naming Conventions

- **Operators**: `RIGNAME_OT_action_name` (e.g., `VR180_OT_CreateScene`)
- **Panels**: `RIGNAME_PT_panel_name` (e.g., `ORBIT_PT_add_panel`)
- **Properties**: `PE_RigNameSettings` (e.g., `PE_VR180SceneSettings`)

### Common Pitfalls

1. **Property registration order**: Properties must be registered before being used in PointerProperty
2. **Template objects**: For GN camera rigs, the template camera must be linked to a collection
3. **Depsgraph timing**: Generated GN instances only appear after `context.view_layer.update()`
4. **Panel parent IDs**: Must exactly match the parent panel's `bl_idname`
5. **Input socket indices**: In GN node groups, socket order matters for modifier access

## Code Quality Standards

### Import Organization
All module-level imports should be at the top of files. Avoid late imports inside functions.

### Console Output
Do NOT use `print()` statements in production code. Use Python's logging module instead.

### Error Handling
All operators should implement comprehensive error handling with specific exception types and cleanup logic.

See individual module guides for detailed information.
