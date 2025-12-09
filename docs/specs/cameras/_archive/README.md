# Camera Rig Specifications

Detailed specifications for all camera rigs in the VR Production Toolkit.

Each camera rig has **two specification files**:
- **`.mdx`** - Documentation/Blueprint (conceptual, use cases, user-facing)
- **`.tech.mdx`** - Technical Spec (implementation-ready, code-focused)

## Camera Rigs

### VR Camera Rigs

#### VR180 Fisheye
- **[vr180-fisheye.mdx](./vr180-fisheye.mdx)** - Documentation & Overview
- **[vr180-tech-01-overview.mdx](./vr180-tech-01-overview.mdx)** - Technical Spec Part 1: Data Model
- **[vr180-tech-02-implementation.mdx](./vr180-tech-02-implementation.mdx)** - Technical Spec Part 2: Implementation
- **[vr180-tech-03-operators.mdx](./vr180-tech-03-operators.mdx)** - Technical Spec Part 3: Operators & UI
- **[vr180-tech-04-reference.mdx](./vr180-tech-04-reference.mdx)** - Technical Spec Part 4: Reference & Testing

Canon RF 5.2mm F2.8 L Dual Fisheye style, side-by-side stereo output

#### VR360 Mono
- **[vr360-mono.mdx](./vr360-mono.mdx)** - Documentation & Overview
- **[vr360mono-tech-01-overview.mdx](./vr360mono-tech-01-overview.mdx)** - Technical Spec Part 1: Data Model
- **[vr360mono-tech-02-implementation.mdx](./vr360mono-tech-02-implementation.mdx)** - Technical Spec Part 2: Implementation
- **[vr360mono-tech-03-operators.mdx](./vr360mono-tech-03-operators.mdx)** - Technical Spec Part 3: Operators & UI
- **[vr360mono-tech-04-reference.mdx](./vr360mono-tech-04-reference.mdx)** - Technical Spec Part 4: Reference & Testing

Single 360° camera, full spherical coverage, non-stereoscopic

#### VR360 Stereo
- **[vr360-stereo.mdx](./vr360-stereo.mdx)** - Documentation & Overview
- **[vr360-stereo.tech.mdx](./vr360-stereo.tech.mdx)** - Technical Implementation Spec

Dual cameras for 3D VR, Top/Bottom or Left/Right layouts

### Production Camera Rigs

#### Orbit Camera
- **[orbit-camera.mdx](./orbit-camera.mdx)** - Documentation & Overview
- **[orbit-camera-tech-01-overview.mdx](./orbit-camera-tech-01-overview.mdx)** - Technical Spec Part 1: Data Model
- **[orbit-camera-tech-02-implementation.mdx](./orbit-camera-tech-02-implementation.mdx)** - Technical Spec Part 2: Implementation
- **[orbit-camera-tech-03-operators.mdx](./orbit-camera-tech-03-operators.mdx)** - Technical Spec Part 3: Operators & UI
- **[orbit-camera-tech-04-reference.mdx](./orbit-camera-tech-04-reference.mdx)** - Technical Spec Part 4: Reference & Testing

Automated circular orbit camera for product visualization, character showcases, 360° presentations

#### Standard Camera
- **[standard.mdx](./standard.mdx)** - Documentation & Overview
- **[standard.tech.mdx](./standard.tech.mdx)** - Technical Implementation Spec

Traditional film/video camera, configurable lens and sensor

#### Isometric Camera
- **[isometric.mdx](./isometric.mdx)** - Documentation & Overview
- **[isometric-tech-01-overview.mdx](./isometric-tech-01-overview.mdx)** - Technical Spec Part 1: Data Model
- **[isometric-tech-02-implementation.mdx](./isometric-tech-02-implementation.mdx)** - Technical Spec Part 2: Implementation
- **[isometric-tech-03-operators.mdx](./isometric-tech-03-operators.mdx)** - Technical Spec Part 3: Operators & UI
- **[isometric-tech-04-reference.mdx](./isometric-tech-04-reference.mdx)** - Technical Spec Part 4: Reference & Testing

Technical/architectural visualization, true isometric projection

## Common Features

All camera rigs include:
- **Parent empty** for easy rig positioning
- **Collection organization** for scene management
- **Preset system** for quick setup
- **Property panel** for live adjustment
- **Render settings** optimized per camera type

## Specification Format

### Documentation File (`.mdx`)
User-facing documentation and conceptual overview:

1. **Overview** - What it does and why
2. **Use Cases** - Who uses it and when
3. **Features** - User-facing capabilities
4. **Concepts** - Understanding stereoscopic, FOV, IPD, etc.
5. **Workflow** - How to use it in production
6. **Presets** - Pre-configured setups explained
7. **Tips & Best Practices** - Common pitfalls, recommendations
8. **Examples** - Real-world usage scenarios
9. **Troubleshooting** - Common issues and solutions

### Technical Spec File (`.tech.mdx`)
Implementation-ready technical specification:

1. **Data Model** - Property definitions (copy-paste ready)
2. **Function Signatures** - Exact API with type hints
3. **Implementation Steps** - Step-by-step checklist
4. **Blender API Calls** - Specific bpy commands needed
5. **File Organization** - Which module/file for each function
6. **UI Implementation** - Panel layout code
7. **Validation & Errors** - Input validation, error handling
8. **Dependencies** - Required imports and modules
9. **Test Cases** - Expected inputs/outputs
10. **Performance Notes** - Optimization considerations

## Development Priority

1. 🔴 VR180 Fisheye (highest priority)
2. 🔴 VR360 Mono
3. 🔴 VR360 Stereo
4. 🟡 Standard
5. 🟡 Isometric
