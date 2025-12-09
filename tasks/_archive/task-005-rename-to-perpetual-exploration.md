# Task 005: Rename to Perpetual Exploration (PE Camera Rigs)

**Status**: ✅ COMPLETE
**Priority**: Medium
**Created**: 2025-12-08
**Estimated Scope**: Medium (2-3 hours)

## Overview

Rename the addon from `cgt_camera_rigs` to `pe_camera_rigs` to align with the Perpetual Exploration project branding.

**Impact**: This is a breaking change. Existing users will need to:
1. Uninstall the old `cgt_camera_rigs` addon
2. Install the new `pe_camera_rigs` addon
3. Any saved .blend files referencing CGT properties will need updating

**Recommendation**: Bump version to 2.0.0 to indicate major breaking change.

---

## Scope Analysis

### Python Code Changes (~38 occurrences across 16 files)

**Class Name Prefixes**: `CGT_` → `PE_`
- `CGT_PT_main_panel` → `PE_PT_main_panel`
- `CGT_AddonPreferences` → `PE_AddonPreferences`
- `CGT_VR180SceneSettings` → `PE_VR180SceneSettings`
- `CGT_VR180RigSettings` → `PE_VR180RigSettings`
- `CGT_VR360MonoSceneSettings` → `PE_VR360MonoSceneSettings`
- `CGT_OrbitCameraSettings` → `PE_OrbitCameraSettings`
- `CGT_IsometricCameraAddProps` → `PE_IsometricCameraAddProps`
- `CGT_IsometricCameraSettings` → `PE_IsometricCameraSettings`

**Property Names**: `cgt_` → `pe_`
- `bpy.types.Scene.cgt_vr180_settings` → `pe_vr180_settings`
- `bpy.types.Scene.cgt_vr360_mono_settings` → `pe_vr360_mono_settings`
- `bpy.types.Scene.cgt_orbit_cam_settings` → `pe_orbit_cam_settings`
- `bpy.types.Scene.cgt_iso_cam_add_props` → `pe_iso_cam_add_props`
- `bpy.types.Object.cgt_iso_cam` → `pe_iso_cam`
- `bpy.types.Object.cgt_orbit_cam` → `pe_orbit_cam`
- `bpy.types.Object.cgt_vr180_rig` → `pe_vr180_rig`

**Files to Update** (16 Python files):
- `src/cgt_camera_rigs/__init__.py`
- `src/cgt_camera_rigs/preferences.py`
- `src/cgt_camera_rigs/ui/__init__.py`
- `src/cgt_camera_rigs/ui/main_panel.py`
- `src/cgt_camera_rigs/rigs/orbit/__init__.py`
- `src/cgt_camera_rigs/rigs/orbit/properties.py`
- `src/cgt_camera_rigs/rigs/orbit/panels.py`
- `src/cgt_camera_rigs/rigs/isometric/properties.py`
- `src/cgt_camera_rigs/rigs/isometric/panels.py`
- `src/cgt_camera_rigs/rigs/vr180/__init__.py`
- `src/cgt_camera_rigs/rigs/vr180/properties.py`
- `src/cgt_camera_rigs/rigs/vr180/panels.py`
- `src/cgt_camera_rigs/rigs/vr180/rig.py`
- `src/cgt_camera_rigs/rigs/vr360mono/properties.py`
- `src/cgt_camera_rigs/rigs/vr360mono/panels.py`
- `src/cgt_camera_rigs/rigs/vr360mono/operators.py`

### Folder/Package Renaming

**Directory Structure**:
```
src/cgt_camera_rigs/  →  src/pe_camera_rigs/
```

### bl_info Updates

**Current**:
```python
bl_info = {
    "name": "CGT Camera Rigs",
    "author": "Ian Worthington",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > CGT Cams",
    "description": "Advanced camera rig creation for Isometric, Orbit, VR180, and VR360 workflows.",
    "warning": "",
    "doc_url": "https://github.com/ianworthington/blender-camera-rigs-addon",
    "category": "Camera",
}
```

**New**:
```python
bl_info = {
    "name": "PE Camera Rigs",
    "author": "Ian Worthington",
    "version": (2, 0, 0),  # Major version bump for breaking change
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > PE Cams",
    "description": "Advanced camera rig creation for Isometric, Orbit, VR180, and VR360 workflows. Part of Perpetual Exploration.",
    "warning": "",
    "doc_url": "https://github.com/ianworthington/blender-camera-rigs-addon",
    "category": "Camera",
}
```

**Alternative UI Tab Names** (choose one):
- "PE Cams" (short, matches CGT pattern)
- "PE Camera Rigs" (descriptive)
- "Perpetual Exploration" (full branding)

### Documentation Updates (10+ files)

**Documentation Files**:
- `README.md`
- `CLAUDE.md`
- `docs/guides/01-installation.mdx`
- `docs/guides/00-packaging_up.mdx`
- `docs/specs/cameras/orbit-02-code.mdx`
- `docs/specs/cameras/isometric-02-code.mdx`
- `docs/specs/cameras/vr180-02-code.mdx`
- `docs/specs/cameras/vr360mono-02-code.mdx`
- `docs/research/blender-addon-best-practices.mdx`
- `tasks/task-004-comprehensive-fixes.md`

**Search/Replace Patterns**:
- `cgt_camera_rigs` → `pe_camera_rigs`
- `CGT Camera Rigs` → `PE Camera Rigs`
- `CGT Cams` → `PE Cams` (or chosen alternative)
- GitHub URLs (if repo name changes)

### Packaging

**Zip Filename**:
- Old: `cgt_camera_rigs.zip`
- New: `pe_camera_rigs.zip` or `pe-camera-rigs-v2.0.0.zip`

**Zip Contents**:
```
pe_camera_rigs.zip
└── pe_camera_rigs/
    ├── __init__.py
    ├── preferences.py
    ├── ui/
    ├── rigs/
    └── utils/
```

---

## Implementation Steps

### Phase 1: Python Code Updates

- [ ] **Update bl_info** in `src/cgt_camera_rigs/__init__.py`:
  - [ ] Change name: "CGT Camera Rigs" → "PE Camera Rigs"
  - [ ] Bump version: (1, 0, 0) → (2, 0, 0)
  - [ ] Update location: "CGT Cams" → "PE Cams"
  - [ ] Update description to mention Perpetual Exploration

- [ ] **Replace all class name prefixes** (search/replace `CGT_` → `PE_`):
  - [ ] `preferences.py`: CGT_AddonPreferences → PE_AddonPreferences
  - [ ] `ui/main_panel.py`: CGT_PT_main_panel → PE_PT_main_panel
  - [ ] `rigs/orbit/properties.py`: CGT_OrbitCameraSettings → PE_OrbitCameraSettings
  - [ ] `rigs/orbit/panels.py`: ORBIT panels with parent_id update
  - [ ] `rigs/isometric/properties.py`: CGT_IsometricCamera* → PE_IsometricCamera*
  - [ ] `rigs/isometric/panels.py`: ISOMETRIC panels with parent_id update
  - [ ] `rigs/vr180/properties.py`: CGT_VR180* → PE_VR180*
  - [ ] `rigs/vr180/panels.py`: VR180 panels
  - [ ] `rigs/vr360mono/properties.py`: CGT_VR360MonoSceneSettings → PE_VR360MonoSceneSettings
  - [ ] `rigs/vr360mono/panels.py`: VR360 panels

- [ ] **Replace all property names** (search/replace `cgt_` → `pe_` in property assignments):
  - [ ] `bpy.types.Scene.cgt_vr180_settings` → `pe_vr180_settings`
  - [ ] `bpy.types.Scene.cgt_vr360_mono_settings` → `pe_vr360_mono_settings`
  - [ ] `bpy.types.Scene.cgt_orbit_cam_settings` → `pe_orbit_cam_settings`
  - [ ] `bpy.types.Scene.cgt_iso_cam_add_props` → `pe_iso_cam_add_props`
  - [ ] `bpy.types.Object.cgt_iso_cam` → `pe_iso_cam`
  - [ ] `bpy.types.Object.cgt_orbit_cam` → `pe_orbit_cam`
  - [ ] `bpy.types.Object.cgt_vr180_rig` → `pe_vr180_rig`

- [ ] **Update property access in operators/panels**:
  - [ ] Search for `context.scene.cgt_` and replace with `pe_`
  - [ ] Search for `.cgt_` (object properties) and replace with `.pe_`

- [ ] **Update bl_parent_id references**:
  - [ ] All child panels: `bl_parent_id = "CGT_PT_main_panel"` → `"PE_PT_main_panel"`

- [ ] **Verify all imports still work** (no changes needed, just verification)

### Phase 2: Folder Renaming

- [ ] **Rename the main package directory**:
  ```bash
  cd src
  mv cgt_camera_rigs pe_camera_rigs
  ```

- [ ] **Verify folder structure**:
  ```
  src/pe_camera_rigs/
  ├── __init__.py
  ├── preferences.py
  ├── ui/
  ├── rigs/
  └── utils/
  ```

### Phase 3: Documentation Updates

- [ ] **Update CLAUDE.md**:
  - [ ] Project title and descriptions
  - [ ] All code examples with class names
  - [ ] Module structure paths
  - [ ] Recent fixes log

- [ ] **Update README.md**:
  - [ ] Addon name
  - [ ] Installation instructions
  - [ ] Usage examples
  - [ ] Screenshots (if any mention CGT)

- [ ] **Update docs/guides/01-installation.mdx**:
  - [ ] Zip filename references
  - [ ] Folder name in installation steps
  - [ ] UI location (sidebar tab name)

- [ ] **Update docs/guides/00-packaging_up.mdx**:
  - [ ] Zip creation commands
  - [ ] Folder name references

- [ ] **Update spec files** (4 files):
  - [ ] `docs/specs/cameras/orbit-02-code.mdx`
  - [ ] `docs/specs/cameras/isometric-02-code.mdx`
  - [ ] `docs/specs/cameras/vr180-02-code.mdx`
  - [ ] `docs/specs/cameras/vr360mono-02-code.mdx`
  - [ ] Replace class names, property names, import paths

- [ ] **Update docs/research/blender-addon-best-practices.mdx**:
  - [ ] Code examples

- [ ] **Update tasks/task-004-comprehensive-fixes.md**:
  - [ ] File paths in task descriptions
  - [ ] Code examples

### Phase 4: Testing & Validation

- [ ] **Test addon installation**:
  - [ ] Create zip: `cd src && zip -r ../pe_camera_rigs.zip pe_camera_rigs`
  - [ ] Install in Blender
  - [ ] Verify appears as "PE Camera Rigs" in preferences
  - [ ] Verify sidebar shows "PE Cams" tab

- [ ] **Test all rigs**:
  - [ ] Orbit rig creates and animates
  - [ ] Isometric rig creates with all presets
  - [ ] VR180 4-step workflow completes
  - [ ] VR360 4-step workflow completes

- [ ] **Verify no CGT references remain**:
  ```bash
  grep -r "CGT" src/pe_camera_rigs/
  grep -r "cgt_camera_rigs" src/pe_camera_rigs/
  ```

- [ ] **Check Python console for errors**:
  - [ ] Enable/disable addon
  - [ ] Create each rig type
  - [ ] No AttributeError or NameError

### Phase 5: Git & Distribution

- [ ] **Git operations**:
  ```bash
  git mv src/cgt_camera_rigs src/pe_camera_rigs
  git add -A
  git commit -m "Rename addon to PE Camera Rigs (Perpetual Exploration)

  - Renamed package: cgt_camera_rigs → pe_camera_rigs
  - Renamed all class prefixes: CGT_ → PE_
  - Renamed all property prefixes: cgt_ → pe_
  - Updated UI tab: CGT Cams → PE Cams
  - Bumped version to 2.0.0 (breaking change)
  - Updated all documentation"
  ```

- [ ] **Create release package**:
  - [ ] `cd src && zip -r ../pe-camera-rigs-v2.0.0.zip pe_camera_rigs`
  - [ ] Test installation from zip

- [ ] **Update GitHub** (if applicable):
  - [ ] Consider renaming repo (or leave as-is for backward compat)
  - [ ] Update README
  - [ ] Create v2.0.0 release tag
  - [ ] Add migration notes for users upgrading from v1.x

---

## Migration Notes for Users

**If users have .blend files with v1.x (CGT) addon:**

The properties won't automatically transfer because the internal names changed. Users would need to:

1. **Before updating**: Note down their settings
2. **Uninstall** CGT Camera Rigs v1.x
3. **Install** PE Camera Rigs v2.0
4. **Recreate rigs** with noted settings

**Alternative**: Could provide a migration script, but that's probably overkill for an addon at this stage.

---

## Post-Rename Checklist

After completing the rename:

- [ ] All Python files use PE_ prefix
- [ ] All property names use pe_ prefix
- [ ] Folder is named pe_camera_rigs
- [ ] bl_info shows "PE Camera Rigs" v2.0.0
- [ ] Sidebar tab shows "PE Cams"
- [ ] Documentation updated (no CGT references except in history)
- [ ] Zip file is pe_camera_rigs.zip or pe-camera-rigs-v2.0.0.zip
- [ ] Addon installs and works in Blender 4.0+
- [ ] All four rigs functional
- [ ] No console errors

---

## Notes

- **Breaking Change**: This is a major version bump because existing .blend files with CGT properties won't work
- **Clean Break**: Better to do this now before wide distribution
- **Branding**: "PE" is shorter and cleaner than "CGT", matches "Perpetual Exploration" project
- **Tab Name**: "PE Cams" is recommended (short, clear, consistent with old pattern)
- **Backward Compatibility**: Not maintained - users must uninstall old version

---

## Estimated Time

- Phase 1 (Python): 1 hour
- Phase 2 (Folder): 5 minutes
- Phase 3 (Docs): 45 minutes
- Phase 4 (Testing): 30 minutes
- Phase 5 (Git/Release): 15 minutes

**Total**: ~2.5 hours
