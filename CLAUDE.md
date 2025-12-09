# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Blender addon providing professional camera rigs for production workflows. The addon creates four distinct camera rig types: Orbit, Isometric, VR180, and VR360 Mono. All rigs are accessible through a unified panel in the Blender 3D Viewport sidebar under the "PE Cams" tab.

**Target Blender Version:** 4.0.0+

---

## ⚠️ IMPORTANT: Git Commit Guidelines

**CRITICAL:** NO "Co-Authored-By: Claude" lines, NO emojis, NO "Generated with Claude Code" footers, NO AI references.

Keep commit messages focused on technical changes only. See **[/docs/CLAUDE.md - Git Commit Message Standards](./docs/CLAUDE.md#git-commit-message-standards)** for examples and details.

---

## Developer Documentation

**Complete technical documentation is in `docs/dev/`**:

### Quick Start
- **[Developer Documentation Index](./docs/dev/README.md)** - Start here for overview

### Module Guides
- **[Rig System Architecture](./docs/dev/rigs/README.md)** - Core patterns and conventions
- **[Orbit Rig](./docs/dev/rigs/orbit.md)** - Procedural turntable camera
- **[Isometric Rig](./docs/dev/rigs/isometric.md)** - Orthographic projections
- **[VR180 Rig](./docs/dev/rigs/vr180.md)** - Stereoscopic VR workflow
- **[VR360 Mono Rig](./docs/dev/rigs/vr360mono.md)** - 360° panoramic VR
- **[UI Development](./docs/dev/ui.md)** - Panel system and conventions
- **[Utilities Reference](./docs/dev/utils.md)** - Shared helper functions

---

## Quick Reference

### Packaging and Distribution

Create distributable zip file:

```bash
cd src
zip -r ../pe_camera_rigs.zip pe_camera_rigs
```

The zip must contain the `pe_camera_rigs` folder at its root (not `src/pe_camera_rigs`).

### Module Structure

```
src/pe_camera_rigs/
├── __init__.py          # Main registration, bl_info
├── preferences.py       # Addon preferences
├── ui/                  # UI panels
│   └── main_panel.py    # Main parent panel
├── rigs/                # Camera rig implementations
│   ├── orbit/           # Procedural orbit camera
│   ├── isometric/       # Isometric projection camera
│   ├── vr180/           # Stereoscopic VR180 workflow
│   └── vr360mono/       # Monoscopic VR360 workflow
└── utils/               # Shared utilities
    ├── blender.py       # Blender API utilities
    ├── nodes.py         # Geometry node creation
    └── scene_setup.py   # Scene setup helpers
```

### Two Rig Architectures

**Interactive Rigs (Orbit, Isometric):**
- Built with Geometry Nodes for real-time, procedural control
- Single operator creates complete rig
- All controls via Modifier Properties
- See: [Rig System Architecture](./docs/dev/rigs/README.md#interactive-rigs-orbit-isometric)

**Workflow Rigs (VR180, VR360 Mono):**
- Multi-step production pipeline (4 steps)
- Each step is a separate operator
- Designed for crash-safe VR content production
- See: [Rig System Architecture](./docs/dev/rigs/README.md#workflow-rigs-vr180-vr360-mono)

### Naming Conventions

- **Operators**: `RIGNAME_OT_action_name` (e.g., `VR180_OT_CreateScene`)
- **Panels**: `RIGNAME_PT_panel_name` (e.g., `ORBIT_PT_add_panel`)
- **Properties**: `PE_RigNameSettings` (e.g., `PE_VR180SceneSettings`)

### Registration Pattern

1. **Top-level** (`__init__.py`): Registers addon preferences, delegates to submodules
2. **Submodule level**: `ui` and `rigs` modules have their own `register()`/`unregister()`
3. **Rig level**: Each rig module registers its own classes

**Important**: Always register/unregister in proper order. Classes must be registered before being assigned as `PointerProperty` types.

---

## Blender API Conventions

- **bl_idname**: Use lowercase with dots (e.g., `"vr180.create_scene"`)
- **Class names**: Use uppercase with underscores (e.g., `VR180_OT_CreateScene`)
- **bl_options**: Common combinations:
  - `{'REGISTER', 'UNDO'}` for most operators
  - `{'REGISTER'}` for operators that shouldn't support undo
- **EnumProperty items**: Tuples of `(identifier, name, description)`
- **Report types**: `{'INFO'}`, `{'WARNING'}`, `{'ERROR'}`

---

## Code Quality Standards

### Import Organization
All module-level imports should be at the top of files. Avoid late imports inside functions.

**Good:**
```python
import bpy
import os
from pathlib import Path

def execute(self, context):
    path = Path(context.scene.output_path)
```

**Bad:**
```python
def execute(self, context):
    from pathlib import Path  # Don't do this
    path = Path(context.scene.output_path)
```

### Console Output
**Do NOT use print() statements** in production code. The addon should load and operate silently. If debugging output is needed, use Python's logging module:

```python
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

### Error Handling
All operators should implement comprehensive error handling with specific exception types and cleanup logic.

**See**: [Error Handling Pattern](./docs/dev/rigs/README.md#error-handling-pattern)

---

## Common Pitfalls

1. **Property registration order**: Properties must be registered before being used in PointerProperty
2. **Template objects**: For GN camera rigs, the template camera must be linked to a collection
3. **Depsgraph timing**: Generated GN instances only appear after `context.view_layer.update()`
4. **Panel parent IDs**: Must exactly match the parent panel's `bl_idname`
5. **Input socket indices**: In GN node groups, socket order matters for modifier access

**See**: [Common Pitfalls](./docs/dev/rigs/README.md#common-pitfalls)

---

## Development Workflow

1. Make code changes in `src/pe_camera_rigs/`
2. Test in Blender (reload addon)
3. Verify all error handling works
4. Check no print() statements in production code
5. Package: `cd src && zip -r ../pe_camera_rigs.zip pe_camera_rigs`
6. Verify zip structure (pe_camera_rigs/ at root)

---

## Documentation Structure

**Root**: `/CLAUDE.md` (this file) - Quick reference and links
**Dev Docs**: `/docs/dev/` - Complete technical documentation
**User Docs**: `/docs/guides/` - User-facing guides
**Research**: `/docs/research/` - Research and validation documents

**Why this structure?**
- Keeps developer docs separate from distribution (`src/` only contains code)
- No risk of shipping CLAUDE.md files to end users
- Centralized documentation that's easy to maintain

---

## For More Information

See the complete developer documentation in `docs/dev/`:
- **[Developer Documentation Index](./docs/dev/README.md)** - Complete technical docs
- **[Rig System Architecture](./docs/dev/rigs/README.md)** - In-depth rig patterns
- **[UI Development Guide](./docs/dev/ui.md)** - Panel system details
- **[Utilities Reference](./docs/dev/utils.md)** - Shared function documentation
