# Perpetual Exploration Camera Rigs Addon for Blender

**A workflow automation addon** built to streamline camera rig setup for [perpetualexploration.com](https://perpetualexploration.com) blog content production.

[![Blender](https://img.shields.io/badge/Blender-4.0+-orange.svg)](https://www.blender.org)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/ianhboyle/pe-camera-rigs/releases)
[![License](https://img.shields.io/badge/license-GPL%20v3-blue.svg)](./LICENSE)

This addon automates the most frequently-used camera configurations in my Blender workflow, with primary focus on the VR180 pipeline. It eliminates manual setup overhead and enforces YouTube VR specification compliance for consistent output.

---

## ✨ What It Does

Four camera rigs I use constantly, divided into two categories:

### 🎮 Interactive Rigs (Real-Time, Modifier-Driven)

**Orbit Camera**

- Procedural turntable animations
- Customizable easing and speed
- Perfect for product showcases

**Isometric Camera** _(inspired by [Polygon Runway](https://polygonrunway.com))_

- True isometric, dimetric, and custom projections
- 7 built-in presets for game art and technical illustrations
- Orthographic views with real-time control

### 🥽 Workflow Rigs (4-Step Production Pipeline)

**VR180 Stereoscopic** _(The main reason this addon exists)_

- Automates the entire YouTube VR180 workflow
- Ensures correct stereoscopic settings every time
- Crash-safe EXR rendering for production reliability
- Built specifically for Perpetual Exploration blog content

**VR360 Monoscopic**

- Full 360° panoramic content
- Equirectangular projection
- Perfect for virtual tours

---

## 📖 Documentation

### Getting Started

1. **[Installation Guide](./docs/guides/01-installation.mdx)** - Install and configure the addon
2. **[Getting Started](./docs/guides/02-getting-started.mdx)** - Quick overview of all rigs

### Feature Guides

3. **[Orbit Camera](./docs/guides/03-orbit-camera.mdx)** - Turntable animations
4. **[Isometric Camera](./docs/guides/04-isometric-camera.mdx)** - Isometric/axonometric views
5. **[VR180 Workflow](./docs/guides/05-vr180-workflow.mdx)** - Stereoscopic VR content
6. **[VR360 Workflow](./docs/guides/06-vr360-workflow.mdx)** - Panoramic VR content

### Reference

7. **[Troubleshooting](./docs/guides/07-troubleshooting.mdx)** - Common issues and solutions
8. **[Packaging Guide](./docs/guides/08-packaging.mdx)** - For developers

---

## 🚀 Quick Start

### Installation

1. Download the latest `pe_camera_rigs.zip` from [Releases](https://github.com/ianhboyle/pe-camera-rigs/releases)
2. In Blender: `Edit` → `Preferences` → `Add-ons`
3. Click `Install...` and select the zip file
4. Enable "PE Camera Rigs"
5. Press `N` in the 3D Viewport to find the **"PE Cams"** tab

### 30-Second Turntable

1. Open **PE Cams** sidebar
2. Click **"Add Orbit Rig"**
3. Press `Numpad 0` to look through camera
4. Press `Spacebar` to preview animation
5. Done! 🎉

---

## 🎯 My Use Cases

| Rig           | What I Use It For                                          |
| ------------- | ---------------------------------------------------------- |
| **Orbit**     | Quick product showcases and 3D model turnarounds           |
| **Isometric** | Technical illustrations and game-style renders             |
| **VR180**     | **Primary:** YouTube VR content for Perpetual Exploration blog posts |
| **VR360**     | Occasional 360° environment captures                       |

---

## 📦 What's New in v1.0.0

### Features

- **Orbit Camera** - Procedural turntable animations with geometry nodes
- **Isometric Camera** - True isometric and axonometric projections
- **VR180 Stereoscopic** - Automated YouTube VR180 workflow with crash-safe rendering
- **VR360 Monoscopic** - 360° panoramic content pipeline
- Complete documentation with focused guides
- Comprehensive error handling across all operators
- Production-tested VR workflows

---

## 🛠️ Requirements

- **Blender:** 4.0.0 or newer
- **OS:** Windows, macOS, or Linux
- **GPU:** Recommended for faster rendering (Cycles)
- **VR Workflows:** Sufficient disk space for EXR sequences

---

## 📚 Technical Details

### Architecture

The addon uses a hierarchical registration pattern:

```
src/pe_camera_rigs/
├── __init__.py          # Main registration, bl_info
├── preferences.py       # Addon preferences
├── ui/                  # UI panels
│   └── main_panel.py
├── rigs/                # Camera rig implementations
│   ├── orbit/           # Procedural orbit camera
│   ├── isometric/       # Isometric projection camera
│   ├── vr180/           # Stereoscopic VR180 workflow
│   └── vr360mono/       # Monoscopic VR360 workflow
└── utils/               # Shared utilities
    ├── blender.py
    ├── nodes.py
    └── scene_setup.py
```

**Key Technologies:**

- **Interactive Rigs:** Geometry Nodes for real-time procedural control
- **VR Workflows:** Python operators with automatic compositor setup
- **Registration:** Modular system with proper dependency handling

For development details, see [CLAUDE.md](./CLAUDE.md).

---

## 🤝 Contributing

Contributions welcome!

**Before contributing:**

1. Read [CLAUDE.md](./CLAUDE.md) for code conventions
2. Check existing [Issues](https://github.com/ianhboyle/pe-camera-rigs/issues)
3. Test thoroughly in Blender 4.0+

**Reporting bugs:**

- Include Blender version and OS
- Provide steps to reproduce
- Share System Console errors
- Screenshots if UI-related

---

## 📝 Development

### Building from Source

```bash
cd src
zip -r ../pe_camera_rigs.zip pe_camera_rigs
```

See [Packaging Guide](./docs/guides/08-packaging.mdx) for detailed instructions.

### Code Quality

This project follows Blender 4.0+ best practices:

- Modular architecture with clear separation
- Comprehensive error handling
- Property validation before execution
- Clean registration/unregistration
- No debug output in production

---

## 🔗 Links

- **Documentation:** [docs/guides/](./docs/guides/)
- **Issues:** [GitHub Issues](https://github.com/ianhboyle/pe-camera-rigs/issues)
- **Releases:** [GitHub Releases](https://github.com/ianhboyle/pe-camera-rigs/releases)
- **Perpetual Exploration:** [perpetualexploration.com](https://perpetualexploration.com)

---

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](./LICENSE) file for details.

**In short:** You're free to use, modify, and distribute this addon. Any derivatives must also be open source under GPL v3.

---

## 🙏 Acknowledgments

- **Isometric Camera:** Inspired by [Polygon Runway's](https://polygonrunway.com) isometric camera tutorial
- **VR Workflows:** Based on production pipelines for YouTube VR content
- **Blender Community:** For continuous inspiration and feedback

---

**Made with ❤️ for the Blender community**

_PE Camera Rigs - Perpetual Exploration Project_
