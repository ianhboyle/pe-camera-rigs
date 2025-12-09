# Task 007: Split CLAUDE.md into Module-Specific Files

**Date**: 2025-12-08
**Status**: Planning
**Priority**: Medium - Improves maintainability

---

## Why Split CLAUDE.md?

**Current Issues**:
- Single 365-line file is hard to navigate
- Module-specific guidance mixed with general guidance
- Updates require scrolling through entire file
- No context-specific help when working in specific modules

**Benefits of Splitting**:
- ✅ Module-specific context for Claude when working in that area
- ✅ Easier to maintain (find relevant section quickly)
- ✅ Better documentation organization
- ✅ Can be more detailed per module without bloating main file
- ✅ Follows "proximity principle" - docs close to code they describe

---

## Recommended Structure

### Root Level: CLAUDE.md (High-Level Overview)

**Keep here** (~100 lines):
- Project overview and purpose
- Git commit guidelines (CRITICAL section)
- Target Blender version
- Packaging instructions
- High-level architecture overview
- Module structure diagram
- Links to module-specific CLAUDE.md files
- Code quality standards (imports, console output, etc.)
- Development notes
- Common pitfalls

**Purpose**: Quick orientation and critical guidelines

---

### Module Level: src/pe_camera_rigs/rigs/CLAUDE.md

**New file** (~80 lines):
- Rig module overview
- Two distinct architectures (Interactive vs Workflow)
- Rig module pattern (standard structure)
- Registration patterns specific to rigs
- Property storage patterns
- Common rig implementation patterns
- Links to individual rig CLAUDE.md files

**Purpose**: Understanding rig system architecture

---

### Individual Rig: src/pe_camera_rigs/rigs/orbit/CLAUDE.md

**New file** (~40-60 lines each):
- Rig-specific implementation details
- Geometry nodes approach
- Preset definitions
- Property update callbacks (if applicable)
- Testing checklist
- Known issues specific to this rig

**Create for**:
- `orbit/CLAUDE.md`
- `isometric/CLAUDE.md`
- `vr180/CLAUDE.md`
- `vr360mono/CLAUDE.md`

**Purpose**: Deep dive into specific rig implementation

---

### Utils Module: src/pe_camera_rigs/utils/CLAUDE.md

**New file** (~50 lines):
- Purpose of each utility module
- When to use each utility function
- Adding new utilities
- Blender-specific utilities vs pure Python
- Scene setup helpers
- Node creation patterns

**Purpose**: Guide for using and extending utilities

---

### UI Module: src/pe_camera_rigs/ui/CLAUDE.md

**New file** (~30 lines):
- Panel hierarchy system
- Parent panel pattern
- Adding new panels
- UI conventions (icons, labels, layout)

**Purpose**: UI development guidelines

---

### Docs: docs/CLAUDE.md

**Already exists** - Keep for:
- Git commit message standards (detailed examples)
- Documentation style guide
- Guide writing conventions

---

## Proposed File Structure

```
blender-camera-rigs-addon/
├── CLAUDE.md                           # Main overview + critical guidelines
├── docs/
│   └── CLAUDE.md                       # Documentation standards (already exists)
└── src/pe_camera_rigs/
    ├── rigs/
    │   ├── CLAUDE.md                   # Rig system overview
    │   ├── orbit/
    │   │   └── CLAUDE.md              # Orbit rig specifics
    │   ├── isometric/
    │   │   └── CLAUDE.md              # Isometric rig specifics
    │   ├── vr180/
    │   │   └── CLAUDE.md              # VR180 rig specifics
    │   └── vr360mono/
    │       └── CLAUDE.md              # VR360 rig specifics
    ├── ui/
    │   └── CLAUDE.md                   # UI development guide
    └── utils/
        └── CLAUDE.md                   # Utilities guide
```

**Total**: 10 CLAUDE.md files (vs current 2)

---

## Content Migration Plan

### 1. Root CLAUDE.md (Keep ~100 lines)

**Sections to Keep**:
```markdown
# CLAUDE.md

## Project Overview
[Brief description - 3-4 lines]

## ⚠️ IMPORTANT: Git Commit Guidelines
[CRITICAL section - keep in full]

## Quick Start for Claude
- Target Blender Version: 4.0.0+
- Main architecture: [link to detailed architecture]
- Module-specific guides: [links to module CLAUDE.md files]

## Packaging and Distribution
[Keep packaging commands]

## Architecture Overview
[High-level diagram and links to detailed docs]

## Code Quality Standards
- Import Organization
- Console Output (logging)
- Property Registration Pattern
- Error Handling Pattern

## Common Pitfalls
[Top 5 most important]

## Module Documentation
- [Rigs System](./src/pe_camera_rigs/rigs/CLAUDE.md)
- [UI Development](./src/pe_camera_rigs/ui/CLAUDE.md)
- [Utilities](./src/pe_camera_rigs/utils/CLAUDE.md)
- [Documentation](./docs/CLAUDE.md)

## Recent Changes
[Link to CHANGELOG.md for full history]
```

---

### 2. src/pe_camera_rigs/rigs/CLAUDE.md (New ~80 lines)

**Content**:
```markdown
# Rig System Architecture

## Overview
[Rig system purpose and design]

## Two Distinct Architectures

### Interactive Rigs (Orbit, Isometric)
[Detailed explanation with examples]

### Workflow Rigs (VR180, VR360 Mono)
[Detailed explanation with examples]

## Rig Module Pattern
[Standard structure with explanations]

## Registration Patterns
[How rig registration works]

## Property Storage Patterns
[Scene vs Object properties]

## Geometry Nodes for Interactive Rigs
[Template camera pattern, depsgraph usage]

## Property Update Callbacks
[How to implement interactive properties - NEW in v1.1]

## Individual Rig Documentation
- [Orbit Rig](./orbit/CLAUDE.md)
- [Isometric Rig](./isometric/CLAUDE.md)
- [VR180 Rig](./vr180/CLAUDE.md)
- [VR360 Mono Rig](./vr360mono/CLAUDE.md)
```

---

### 3. src/pe_camera_rigs/rigs/isometric/CLAUDE.md (New ~50 lines)

**Content**:
```markdown
# Isometric Camera Rig

## Overview
Creates true isometric and axonometric projection views using Geometry Nodes.

## Architecture
- **Type**: Interactive Rig
- **Setup**: Single operator creates complete rig
- **Properties**: Object Properties panel (v1.1+)
- **Updates**: Real-time via property callbacks

## Key Components

### Operators (`operators.py`)
- `ISOMETRIC_OT_add_controller` - Creates rig

### Properties (`properties.py`)
- `PE_IsometricCameraAddProps` - Scene-level (add panel presets)
- `PE_IsometricCameraSettings` - Object-level (controller settings)

### Property Update Callbacks (v1.1+)
[Implementation details with examples]

## Projection Types
[7 presets with mathematical angles]

## Node Group Structure
[Socket mapping: 0-5]

## Testing Checklist
- [ ] Create rig with each preset
- [ ] Verify real-time property updates
- [ ] Test custom angle inputs
- [ ] Verify viewport updates immediately

## Known Issues
- Viewport update limitation: [Issue #87006]
- Workaround: [Details]

## Recent Changes
- v1.1.0: Added property update callbacks for real-time editing
```

---

### 4. src/pe_camera_rigs/utils/CLAUDE.md (New ~50 lines)

**Content**:
```markdown
# Utilities Module

## Purpose
Shared helper functions for Blender operations, geometry nodes, and scene setup.

## Module Overview

### blender.py - Blender API Helpers
**Functions**:
- `detect_and_enable_gpu()` - Auto-enable GPU rendering
- `validate_output_path()` - Check path is writable
- `get_active_camera_or_create()` - Ensure camera exists
- `safe_object_delete()` - Delete with existence check
- `set_modifier_input()` - Update geometry node inputs (v1.1+)

**When to Use**:
- GPU detection in VR workflows
- Path validation before rendering
- Safe resource cleanup

### nodes.py - Geometry Node Creation
**Functions**:
- `create_orbit_camera_node_group()` - Orbit rig nodes
- `create_isometric_camera_node_group()` - Isometric rig nodes

**Pattern**: Template camera + instance on points + rotation nodes

### scene_setup.py - Scene Helpers
**Functions**:
- `create_lighting_preset()` - Add studio lighting
- `create_cyclorama()` - Add background cyclorama
- `add_reference_sphere()` - Add scale reference

**Used By**: VR workflow scene creation operators

## Adding New Utilities
[Guidelines for new functions]

## Testing Utilities
[How to test utility functions]
```

---

### 5. src/pe_camera_rigs/ui/CLAUDE.md (New ~30 lines)

**Content**:
```markdown
# UI Module

## Overview
Unified panel system in 3D Viewport sidebar under "PE Cams" tab.

## Panel Hierarchy

### Main Panel (`main_panel.py`)
- `PE_PT_main_panel` - Parent panel for all rigs
- `bl_category = 'PE Cams'`
- All rig panels are children of this panel

### Child Panels
Each rig has its own panel that sets:
```python
bl_parent_id = 'PE_PT_main_panel'
bl_order = [number]  # Display order
```

## UI Conventions
- No emojis in labels (use icons instead)
- Use appropriate Blender icons
- Real-time feedback for interactive rigs
- Step numbers for workflow rigs

## Adding New Panels
[Instructions]

## Registration Order
Parent must register before children!
```

---

## Implementation Plan

### Phase 1: Create Module CLAUDE.md Files
1. [ ] Create `src/pe_camera_rigs/rigs/CLAUDE.md`
2. [ ] Create `src/pe_camera_rigs/utils/CLAUDE.md`
3. [ ] Create `src/pe_camera_rigs/ui/CLAUDE.md`

### Phase 2: Create Individual Rig Files
4. [ ] Create `src/pe_camera_rigs/rigs/orbit/CLAUDE.md`
5. [ ] Create `src/pe_camera_rigs/rigs/isometric/CLAUDE.md`
6. [ ] Create `src/pe_camera_rigs/rigs/vr180/CLAUDE.md`
7. [ ] Create `src/pe_camera_rigs/rigs/vr360mono/CLAUDE.md`

### Phase 3: Refactor Root CLAUDE.md
8. [ ] Condense root `CLAUDE.md` to ~100 lines
9. [ ] Add links to module-specific files
10. [ ] Verify all content has a home

### Phase 4: Validation
11. [ ] Ensure no duplicate information
12. [ ] Verify all cross-references work
13. [ ] Test with Claude Code (does it find the right context?)

---

## Benefits After Split

### For Claude Code
- **Better context**: Gets relevant docs when working in specific modules
- **Less noise**: Doesn't load irrelevant rig details when working on UI
- **Faster parsing**: Smaller files load faster

### For Developers
- **Easier navigation**: Find relevant docs quickly
- **Modular updates**: Update one rig's docs without touching others
- **Clear ownership**: Each module owns its documentation

### For Maintenance
- **Focused changes**: Update docs close to code
- **Better git diffs**: Changes isolated to relevant files
- **Scalability**: Easy to add new rigs without bloating main file

---

## Example: Claude Working on Isometric Rig

**Before** (single CLAUDE.md):
- Loads 365 lines
- Searches for Isometric section
- Mixed with Orbit, VR180, VR360 details

**After** (split files):
- Loads root CLAUDE.md (~100 lines) for overview
- Loads rigs/CLAUDE.md (~80 lines) for architecture
- Loads rigs/isometric/CLAUDE.md (~50 lines) for specifics
- **Total context**: ~230 lines, all highly relevant

---

## Content Distribution

| File | Lines | Content Type |
|------|-------|--------------|
| Root CLAUDE.md | ~100 | Critical guidelines + overview |
| docs/CLAUDE.md | ~50 | Documentation standards (exists) |
| rigs/CLAUDE.md | ~80 | Rig system architecture |
| orbit/CLAUDE.md | ~50 | Orbit specifics |
| isometric/CLAUDE.md | ~50 | Isometric specifics |
| vr180/CLAUDE.md | ~60 | VR180 specifics |
| vr360mono/CLAUDE.md | ~60 | VR360 specifics |
| utils/CLAUDE.md | ~50 | Utilities guide |
| ui/CLAUDE.md | ~30 | UI development |

**Total**: ~530 lines across 10 files (vs 365 in 1 file)

**Why more lines?**
- Can be more detailed per module
- Less cross-referencing needed
- Clearer examples in context

---

## Maintenance Guidelines

### When to Update

**Root CLAUDE.md**:
- Project-wide changes
- New critical guidelines
- Architecture changes affecting multiple modules

**Module CLAUDE.md**:
- New patterns in that module
- Module-specific conventions
- Changes to module structure

**Individual Rig CLAUDE.md**:
- Rig implementation changes
- New features for that rig
- Rig-specific issues

### Keeping Them Synced

**Avoid**:
- Duplicating information across files
- Repeating root guidelines in module files

**Instead**:
- Reference root CLAUDE.md: "See [Root CLAUDE.md](../../../CLAUDE.md#section)"
- Keep module files focused on module specifics
- Use root for project-wide standards

---

## Testing the Split

After implementation, test:

1. **Ask Claude Code**: "How do I add a new Isometric preset?"
   - Should find `rigs/isometric/CLAUDE.md`

2. **Ask Claude Code**: "What are the git commit guidelines?"
   - Should find root `CLAUDE.md`

3. **Ask Claude Code**: "How do I add a new utility function?"
   - Should find `utils/CLAUDE.md`

4. **Ask Claude Code**: "How do I create a new panel?"
   - Should find `ui/CLAUDE.md`

---

## Estimated Effort

- **Phase 1**: 1 hour (create 3 module files)
- **Phase 2**: 1.5 hours (create 4 rig files)
- **Phase 3**: 1 hour (refactor root CLAUDE.md)
- **Phase 4**: 30 minutes (validation)

**Total**: ~4 hours

---

## Priority

**Recommendation**: MEDIUM priority

**Do this**:
- Before adding new rigs (sets pattern)
- When CLAUDE.md exceeds 400 lines
- When frequent updates cause merge conflicts

**Can wait**:
- If actively developing and don't want disruption
- If only one developer (less benefit)

---

## Conclusion

**Recommendation: YES, split CLAUDE.md**

The project has grown to a point where modular documentation makes sense. The split will:
- Improve Claude Code's contextual understanding
- Make docs easier to maintain
- Scale better as project grows
- Follow "documentation near code" principle

**Suggested Approach**:
1. Start with Phase 1 (module-level files)
2. Test with Claude Code to verify benefit
3. If beneficial, continue with Phases 2-3
4. Keep root CLAUDE.md as authoritative index

---

**Status**: Planning complete - Ready for implementation
**Estimated Time**: 4 hours
**Files to Create**: 8 new CLAUDE.md files
**Files to Update**: 1 (root CLAUDE.md)
