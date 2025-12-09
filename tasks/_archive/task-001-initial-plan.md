# Task 001: Initial Project Planning

**Created:** 2025-12-07
**Status:** Planning
**Priority:** High

---

## Project Overview

Creating two powerful Blender tools from existing VR camera toolkit code:
1. **Unified VR Camera Add-on/Plugin** - Professional Blender add-on
2. **Blender Startup File Generator** - Python CLI tool for generating custom .blend files

---

## Current State Analysis

### Existing Assets in `_archive/`

#### VR180 Blender 5 Package
Located: `_archive/vr180_blender5_package/`

- **vr180_blender5_4090.py** (242 lines)
  - Complete VR180 scene generator
  - RTX 4090 GPU optimization (OptiX)
  - Creates cameras (VR180 L/R, Standard, Isometric, 360°)
  - Lighting setup (3-point lighting: Key, Fill, Rim)
  - Cyclorama scene (floor, wall, curved transition)
  - Capsule person-scale reference
  - Compositor setup for side-by-side stereo output
  - Auto-saves to `vr180_ready.blend`
  - Renders: 3840×2160 per eye, 7680×2160 SBS, H.265/HEVC output

- **vr180_addon.py** (80 lines)
  - Simple UI panel in 3D View sidebar
  - Operators: Create Rig, Render SBS, Save Blend
  - Minimal implementation (mostly UI wrapper)

- **vr180_guide.mdx**
  - User documentation
  - Quick start guide
  - Command-line render examples

- **README.md**
  - Quick reference guide

#### VR Camera Toolkit
Located: `_archive/vr_camera_toolkit/`

- **__init__.py** (314 lines)
  - Property group for VR camera settings
  - Operators for creating rigs and rendering
  - Professional UI panel with organized sections
  - Settings for IPD, resolution, FOV, file formats
  - Support for both 180° fisheye and 360° equirect

- **camera_rigs.py** (341 lines)
  - `create_180_fisheye_rig()` - Canon Dual Fisheye style
  - `create_360_equirect_mono()` - Single 360° camera
  - `create_360_equirect_stereo()` - Dual 360° (top/bottom or left/right)
  - Collection management for organization
  - Full camera configuration (panoramic types, FOV, lens settings)

- **render_utils.py** (264 lines)
  - `render_all_vr_cameras()` - Batch render all cameras
  - `render_camera_pair()` - Render stereo pairs
  - `render_single_camera()` - Individual camera rendering
  - Animation support
  - Automatic file naming and output management

- **README.md**
  - Comprehensive documentation
  - Installation instructions
  - Usage examples
  - Technical specifications
  - Python API reference

---

## Strengths of Each Package

### VR180 Blender 5 Package Strengths
- Complete scene setup (lighting, cyclorama, reference objects)
- GPU optimization for RTX 4090
- Compositor setup for final output
- Auto-save functionality
- Production-ready render settings
- Standalone script approach (can run without installation)

### VR Camera Toolkit Strengths
- Modular architecture (separate concerns)
- Professional UI with organized sections
- Property groups for settings persistence
- Multiple camera rig types
- Batch rendering utilities
- Collection-based organization
- Better code structure for maintenance

---

## Proposed Projects

### Project 1: Unified VR Production Toolkit Add-on

**Vision:** Professional Blender add-on combining best features from both packages

**Core Features to Include:**
- [ ] TBD by user
- [ ] TBD by user
- [ ] TBD by user

**User Stories:**
- [ ] TBD by user

---

### Project 2: Blender Startup File Generator

**Vision:** Python CLI tool for generating custom .blend startup files

**Core Features to Include:**
- [ ] TBD by user
- [ ] TBD by user
- [ ] TBD by user

**User Stories:**
- [ ] TBD by user

---

## Proposed Directory Structure

```
blender-ultimate-startup-and-addon/
├── README.md
├── tasks/
│   └── task-001-initial-plan.md (this file)
├── docs/
│   ├── quick-start.mdx
│   ├── vr180-guide.mdx
│   ├── vr360-guide.mdx
│   ├── startup-generator-guide.mdx
│   └── api-reference.mdx
├── addons/
│   └── vr_production_toolkit/
│       ├── __init__.py
│       ├── bl_info.py
│       ├── camera_rigs.py
│       ├── scene_setup.py
│       ├── lighting_rigs.py
│       ├── render_utils.py
│       ├── gpu_optimization.py
│       ├── ui/
│       │   ├── __init__.py
│       │   ├── panels.py
│       │   ├── operators.py
│       │   └── properties.py
│       └── presets/
│           ├── camera_presets.json
│           ├── lighting_presets.json
│           └── render_presets.json
├── startup_generator/
│   ├── generator.py
│   ├── config_loader.py
│   ├── scene_builder.py
│   ├── templates/
│   │   ├── vr180_template.py
│   │   ├── vr360_template.py
│   │   └── standard_production_template.py
│   └── presets/
│       ├── vr180_4k.yaml
│       ├── vr180_8k.yaml
│       └── vr360_standard.yaml
├── scripts/
│   ├── quick_setups/
│   │   ├── quick_vr180.py
│   │   ├── quick_vr360.py
│   │   └── quick_standard_scene.py
│   └── utilities/
│       ├── gpu_detect.py
│       └── batch_render.py
└── _archive/
    ├── vr180_blender5_package/
    └── vr_camera_toolkit/
```

---

## Next Steps

### Immediate Actions
1. [ ] User to outline desired features for VR Camera Add-on
2. [ ] User to outline desired features for Startup Generator
3. [ ] Finalize project structure
4. [ ] Create implementation plan

---

## User Input Needed

### For the VR Camera Plugin/Add-on:

**What features do you want?**
-
-
-

**What camera rigs should it support?**
-
-
-

**What scene setup features?**
-
-
-

**What rendering capabilities?**
-
-
-

**UI/UX preferences?**
-
-
-

---

### For the Python Startup Generator:

**What templates should it generate?**
-
-
-

**How should it be configured?** (CLI args, config files, interactive?)
-
-
-

**What should be customizable?**
-
-
-

**Output options?**
-
-
-

**Additional features?**
-
-
-

---

## Technical Considerations

### Blender Version Compatibility
- Target Blender version(s): _____
- Backward compatibility needed? _____

### Dependencies
- External Python libraries: _____
- Blender add-on dependencies: _____

### Platform Support
- Windows: ___
- macOS: ___
- Linux: ___

### GPU Optimization
- NVIDIA OptiX: ___
- AMD HIP: ___
- Intel: ___
- CPU fallback: ___

---

## Questions to Resolve

1. Should the add-on and generator share code, or be completely separate?
2. What's the priority: add-on first or generator first?
3. Do you want preset management (save/load custom presets)?
4. Should the generator be able to run inside Blender, or strictly CLI?
5. Do you need version control for .blend files or templates?

---

## Resources & References

- Blender API Documentation: https://docs.blender.org/api/current/
- VR180 Spec: https://github.com/google/spatial-media/blob/master/docs/vr180.md
- Cycles Panoramic Cameras: https://docs.blender.org/manual/en/latest/render/cycles/camera.html

---

## Notes

- Consider backward compatibility with Blender 3.x vs 5.x API changes
- GPU detection and optimization could be a shared utility
- Documentation should include installation, usage, and API reference
- Consider automated testing for scene generation
