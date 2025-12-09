# Task 002-04: UX Refinement - Isometric Camera

**Created:** 2025-12-08
**Status:** Planning
**Priority:** High
**Focus:** Isometric Camera
**Parent Task:** task-002-01-vr180-ux.md

---

## Executive Summary

The **1-click preset workflow** is perfect for Isometric Camera. Inspired by the popular **IsoCam add-on** pattern:
- ✅ **Instant isometric view** - One click, perfect angles
- ✅ **Preset projections** - Game isometric, true iso, dimetric, etc.
- ✅ **Auto-activated** - Camera view ready immediately
- ✅ **Orthographic** - Perfect parallel projection

**Refinement Goals:**
1. **One-click presets** - Instant isometric cameras
2. **Clear projection types** - Know which style to choose
3. **IsoCam-style UX** - Familiar to existing users
4. **Immediate feedback** - See isometric view instantly

---

## The Refined Preset Workflow

### Why Preset-Based is Perfect for Isometric

**Isometric cameras have standard angles:**
- ✅ **Game Isometric** - 26.565° (2:1 pixel ratio stairs)
- ✅ **True Isometric** - 35.264° (mathematically correct)
- ✅ **Dimetric** - 30° (common variation)
- ✅ **Military** - 90° (top-down plan view)

**Users pick by visual style, not angles:**
- ✅ **Game Isometric** → Pixel art, strategy games
- ✅ **True Isometric** → CAD, technical drawings
- ✅ **Dimetric** → Games, illustrations
- ✅ **Military** → Floor plans, strategy maps

---

## The ONE-CLICK Preset System

### Preset Categories

The panel shows **visual examples**, not technical jargon:

```
┌─────────────────────────────────────┐
│ Isometric Camera - Quick Create     │
├─────────────────────────────────────┤
│                                     │
│ 🎮 Game & Pixel Art                 │
│   [Game Isometric (2:1)]           │
│   [Game 4:3 Ratio]                 │
│                                     │
│ 📐 Technical & CAD                  │
│   [True Isometric]                 │
│   [Dimetric (30°)]                 │
│   [Trimetric]                      │
│                                     │
│ 🗺️  Plans & Maps                    │
│   [Military (Top-Down)]            │
│   [Cavalier]                       │
│                                     │
│ 🔧 Custom                           │
│   [Advanced Settings...]           │
│                                     │
└─────────────────────────────────────┘
```

### What Each Preset Creates

**Every preset button does ALL of this in one click:**

1. **Creates camera rig**
   - Parent empty (for easy positioning)
   - Orthographic camera
   - Perfect isometric angles set

2. **Sets projection angles**
   - Rotation Z (45°, 60°, 90°, etc.)
   - Tilt X (26.565°, 35.264°, 30°, etc.)
   - Roll Y (0° - typically locked)

3. **Configures orthographic scale**
   - Default: 14.0 units (IsoCam standard)
   - Fits typical scenes perfectly
   - User can scale later

4. **Activates camera view**
   - Sets as scene camera
   - Switches viewport to camera view
   - See isometric view immediately

5. **Optional scene elements**
   - Reference grid (optional)
   - Axis indicators (optional)
   - Scale reference (optional)

---

## Preset Specifications

### 🎮 Game Isometric (2:1)

**Perfect for:** Pixel art, strategy games, 2:1 ratio stairs

```
What it creates:
├─ Projection Type: Game Isometric
├─ Rotation Z: 45° (diagonal view)
├─ Tilt X: 30° (2:1 pixel ratio for stairs)
├─ Roll Y: 0° (no roll)
├─ Ortho Scale: 14.0 units
├─ Camera Type: ORTHO
└─ Visual Result: Classic strategy game look

Mathematical note:
  tan(30°) = 0.577 ≈ 1:2 ratio
  Perfect for: Stairs that are 2 pixels horizontal : 1 pixel vertical
```

**Use cases:**
- Pixel art games
- Strategy games (Civilization, SimCity style)
- 2D isometric tile maps
- Retro game art

**Visual:**
```
      ╱╲
     ╱  ╲      ← 2 units wide
    ╱____╲
    |    |     ← 1 unit tall
    |____|

2:1 ratio stairs look perfect
```

---

### 🎮 Game 4:3 Ratio

**Perfect for:** Pixel art with 4:3 tiles, isometric RPGs

```
What it creates:
├─ Projection Type: Game 4:3
├─ Rotation Z: 45° (diagonal view)
├─ Tilt X: 26.565° (exact 4:3 ratio)
├─ Roll Y: 0°
├─ Ortho Scale: 14.0 units
└─ Visual Result: Square tiles in 4:3 aspect

Mathematical note:
  tan(26.565°) = 0.5 = 2:4 = 1:2
  Perfect for: Diamond tiles that are 4:3 pixels
```

**Use cases:**
- Isometric RPGs (Diablo, Ultima style)
- 4:3 pixel art tiles
- Diamond-shaped tile maps
- Classic isometric games

---

### 📐 True Isometric

**Perfect for:** CAD drawings, technical illustrations, mathematically correct

```
What it creates:
├─ Projection Type: True Isometric
├─ Rotation Z: 45° (diagonal view)
├─ Tilt X: 35.264° (arctan(1/√2))
├─ Roll Y: 0°
├─ Ortho Scale: 14.0 units
└─ Visual Result: All three axes equally foreshortened

Mathematical note:
  arctan(1/√2) = 35.264°
  Perfect for: All 3 axes appear at 120° angles
  X, Y, Z axes all equally shortened
```

**Use cases:**
- Technical drawings
- CAD visualizations
- Engineering diagrams
- Mathematically accurate isometric

**Visual:**
```
        Z
        |
        |
        •---- Y
       /
      /
     X

All three axes at 120° angles
```

---

### 📐 Dimetric (30°)

**Perfect for:** Game art, illustrations, slight variation from isometric

```
What it creates:
├─ Projection Type: Dimetric
├─ Rotation Z: 45° (diagonal view)
├─ Tilt X: 30° (two axes equal, one different)
├─ Roll Y: 0°
├─ Ortho Scale: 14.0 units
└─ Visual Result: Two axes equal, Z axis different foreshortening

Note: Dimetric means "two measures"
  Two axes scaled equally, third axis different
```

**Use cases:**
- Game illustrations
- Stylized isometric art
- Blend between game and true isometric
- Common in Japanese games

---

### 📐 Trimetric

**Perfect for:** Unique perspectives, all axes different

```
What it creates:
├─ Projection Type: Trimetric
├─ Rotation Z: 60° (custom angle)
├─ Tilt X: 30° (custom tilt)
├─ Roll Y: 0°
├─ Ortho Scale: 14.0 units
└─ Visual Result: All three axes foreshortened differently

Note: Trimetric means "three measures"
  All three axes scaled differently
```

**Use cases:**
- Unique artistic perspectives
- Custom isometric styles
- Architectural visualizations
- When standard isometric is too symmetrical

---

### 🗺️ Military (Top-Down)

**Perfect for:** Floor plans, strategy maps, RTS games

```
What it creates:
├─ Projection Type: Military
├─ Rotation Z: 0° or 45° (user choice)
├─ Tilt X: 90° (looking straight down)
├─ Roll Y: 0°
├─ Ortho Scale: 14.0 units
└─ Visual Result: Perfect top-down orthographic view

Also called: "Plan view" or "Orthographic top"
```

**Use cases:**
- Floor plans
- Real-time strategy games (Age of Empires)
- Map design
- Architectural plans

**Visual:**
```
    ┌─────────┐
    │         │
    │    •    │  ← Looking straight down
    │         │
    └─────────┘
```

---

### 🗺️ Cavalier

**Perfect for:** Side views with depth, cabinet projection

```
What it creates:
├─ Projection Type: Cavalier
├─ Rotation Z: 0° (straight front)
├─ Tilt X: 0° (no tilt)
├─ Roll Y: 45° (depth at 45°)
├─ Ortho Scale: 14.0 units
└─ Visual Result: Front face true size, depth at 45°

Note: One face shown at true size and shape
  Depth recedes at 45° angle
```

**Use cases:**
- Cabinet drawings
- Furniture design
- Side view with depth
- Quick 3D sketches

---

## UI Panel Design

### Quick Create Panel (Main)

```
┌───────────────────────────────────────────────────┐
│ Isometric Camera - Quick Create                   │
├───────────────────────────────────────────────────┤
│                                                   │
│ 📋 One-Click Isometric Views                      │
│                                                   │
│ Choose your projection style. Each button:       │
│   • Creates orthographic camera                  │
│   • Sets perfect isometric angles               │
│   • Activates camera view instantly             │
│   • Ready to use immediately!                   │
│                                                   │
├───────────────────────────────────────────────────┤
│                                                   │
│ 🎮 Game & Pixel Art                               │
│                                                   │
│ [🎮 Game Isometric (2:1)]                         │
│   26.565° tilt • Perfect for strategy games      │
│   Stairs: 2 horizontal : 1 vertical pixels       │
│                                                   │
│ [🎮 Game 4:3 Ratio]                               │
│   30° tilt • Perfect for RPG tiles               │
│   Diamond tiles in 4:3 aspect ratio             │
│                                                   │
├───────────────────────────────────────────────────┤
│                                                   │
│ 📐 Technical & CAD                                │
│                                                   │
│ [📐 True Isometric]                               │
│   35.264° tilt • Mathematically correct          │
│   All axes equally foreshortened                │
│                                                   │
│ [📐 Dimetric (30°)]                               │
│   30° tilt • Two axes equal                      │
│   Common in Japanese games                       │
│                                                   │
│ [📐 Trimetric]                                    │
│   60° + 30° • All axes different                 │
│   Unique custom perspectives                     │
│                                                   │
├───────────────────────────────────────────────────┤
│                                                   │
│ 🗺️  Plans & Maps                                  │
│                                                   │
│ [🗺️ Military (Top-Down)]                          │
│   90° tilt • Perfect top-down view               │
│   Floor plans, RTS games, maps                   │
│                                                   │
│ [🗺️ Cavalier]                                     │
│   0° + 45° roll • Front face true size           │
│   Cabinet drawings, furniture                    │
│                                                   │
├───────────────────────────────────────────────────┤
│                                                   │
│ 🔧 Advanced                                       │
│                                                   │
│ Need custom angles?                              │
│ [⚙️  Custom Angles...]                            │
│   ↳ Opens advanced panel with full controls     │
│                                                   │
├───────────────────────────────────────────────────┤
│                                                   │
│ ℹ️  Quick Guide                                   │
│                                                   │
│ • Game Isometric: Strategy games, pixel art      │
│ • True Isometric: CAD, technical drawings        │
│ • Military: Floor plans, top-down maps          │
│                                                   │
└───────────────────────────────────────────────────┘
```

### Advanced Settings Panel (Optional)

**Only shown if user clicks "Custom Angles..."**

```
┌───────────────────────────────────────────────────┐
│ Isometric Camera - Advanced Settings              │
├───────────────────────────────────────────────────┤
│                                                   │
│ 📷 Camera Settings                                │
│                                                   │
│ Projection Type: [Custom ▼]                      │
│   • Game Isometric (2:1)                         │
│   • Game 4:3 Ratio                               │
│   • True Isometric ⭐                             │
│   • Dimetric (30°)                               │
│   • Trimetric                                    │
│   • Military (Top-Down)                          │
│   • Cavalier                                     │
│   • Custom                                       │
│                                                   │
│ 🔄 Custom Angles (when Custom selected)          │
│                                                   │
│ Rotation Z: [45.0  ]° (horizontal rotation)      │
│   ℹ️ 0° = front, 45° = diagonal, 90° = side      │
│                                                   │
│ Tilt X: [35.264]° (vertical tilt)                │
│   ℹ️ 0° = level, 90° = top-down                  │
│                                                   │
│ Roll Y: [0.0   ]° (camera roll)                  │
│   ℹ️ Usually 0° for isometric                    │
│                                                   │
│ 📏 Orthographic Scale                             │
│                                                   │
│ Ortho Scale: [14.0  ] units                      │
│   ℹ️ Smaller = zoomed in, Larger = zoomed out    │
│                                                   │
│ 📦 Optional Scene Elements                        │
│                                                   │
│ ☐ Reference Grid                                 │
│   Grid Size: [10  ] m                            │
│   Subdivisions: [10] lines                       │
│                                                   │
│ ☐ Axis Indicators (XYZ arrows)                   │
│   Arrow Length: [5.0] units                      │
│                                                   │
│ ☐ Scale Reference                                │
│   Floor: [10] m × [10] m                         │
│   Cube: [5] m × [5] m × [5] m                    │
│                                                   │
│ 💡 Lighting                                       │
│                                                   │
│ Add Lighting: [Flat ▼]                           │
│   • None                                         │
│   • Flat (even, no shadows) ⭐                    │
│   • Soft (subtle shadows)                        │
│   • 3-Point (standard)                           │
│                                                   │
│ [Create Isometric Camera]                        │
│                                                   │
└───────────────────────────────────────────────────┘
```

### Settings Panel (After Creation)

**Shown when isometric camera is selected:**

```
┌───────────────────────────────────────────────────┐
│ Isometric Camera - Settings                       │
├───────────────────────────────────────────────────┤
│                                                   │
│ 📷 Active Camera: IsometricCamera                 │
│                                                   │
│ Current Angles:                                   │
│   Rotation Z: 45.0°                              │
│   Tilt X: 35.264° (True Isometric)               │
│   Roll Y: 0.0°                                   │
│                                                   │
│ Ortho Scale: [14.0  ] units                      │
│   [Zoom In -] [Zoom Out +]                       │
│                                                   │
│ 🔄 Change Projection                              │
│                                                   │
│ [Set to Game Isometric]                          │
│ [Set to Dimetric]                                │
│ [Set to Military Top-Down]                       │
│                                                   │
│ 🛠️  Tools                                          │
│                                                   │
│ [Frame Selection]                                │
│   ↳ Auto-fit camera to selected objects         │
│                                                   │
│ [Reset to True Isometric]                        │
│   ↳ Reset angles to 45° / 35.264° / 0°          │
│                                                   │
│ [Level Camera]                                   │
│   ↳ Ensure camera is perfectly level            │
│                                                   │
└───────────────────────────────────────────────────┘
```

---

## Success Messages

### After Preset Creation

```
✅ ISOMETRIC CAMERA CREATED!

Preset: True Isometric
Angles: 45° / 35.264° / 0° (Rotation/Tilt/Roll)
Ortho Scale: 14.0 units
Type: Orthographic (perfect parallel projection)

🎥 Camera is ACTIVE and READY!
   ├─ Already in camera view
   ├─ Isometric perspective set
   └─ Ready to add/view your content

👉 NEXT STEPS:
  1. Add or position your objects in scene
  2. Objects automatically shown in isometric
  3. Use G/R/S to move/rotate/scale (grid snap helpful)
  4. Render or export when ready

💡 TIPS:
  • Select camera parent to move entire view
  • Scroll wheel to zoom (changes ortho scale)
  • Grid snapping (Shift+Tab) helps with alignment
```

---

## IsoCam-Style UX Features

### Instant Camera Activation

**Like IsoCam, camera is immediately active:**

1. User clicks preset button
2. Camera is created
3. Camera is set as scene.camera
4. Viewport switches to camera view
5. User sees isometric view instantly

**No extra steps needed!**

### Scroll Wheel Zoom

**Viewport scroll wheel adjusts orthographic scale:**

```python
# When in camera view with isometric camera:
Scroll Up = Zoom In (decrease ortho scale)
Scroll Down = Zoom Out (increase ortho scale)

This is familiar to IsoCam users!
```

### Quick Preset Switching

**User can change projection type after creation:**

```
Select camera → Settings panel → [Set to Dimetric]

Camera angles update instantly
No need to recreate camera
```

---

## Frame Selection Tool

### Auto-Fit Camera to Objects

**IsoCam-style frame selection:**

```
ISOMETRIC_OT_FrameSelection:
  1. User selects objects to frame
  2. User clicks [Frame Selection] button
  3. Operator calculates bounding box
  4. Adjusts ortho_scale to fit objects perfectly
  5. Optional: padding around objects (1.2x default)
```

**Example:**

```
Before:
  ortho_scale = 14.0
  Objects too small in view

After [Frame Selection]:
  ortho_scale = 6.8 (auto-calculated)
  Objects fill frame perfectly
```

---

## Error Handling

### Preset Creation Errors

**Error: Already in orthographic view**
```
ℹ️  Camera already exists!

Existing camera: IsometricCamera

Options:
  [Replace]      Delete old, create new
  [Add Another]  Create second isometric camera
  [Cancel]       Keep existing
```

**Warning: Active object is not at origin**
```
ℹ️  Isometric camera created at (0, 0, 0)

Your selected object is at (5.2, -3.4, 1.8)

👉 To center view on object:
  1. Select IsometricCamera_Parent empty
  2. Press G (move mode)
  3. Move to your object's location

[OK, Got It]
```

---

## Implementation Checklist

### Phase 1: Preset Operators

- [ ] **ISOMETRIC_OT_QuickCreate_GameIsometric**
  - [ ] Create Game Isometric (2:1) camera
  - [ ] Angles: 45° / 26.565° / 0°
  - [ ] Ortho scale: 14.0
  - [ ] Auto-activate camera view

- [ ] **ISOMETRIC_OT_QuickCreate_Game43**
  - [ ] Create Game 4:3 camera
  - [ ] Angles: 45° / 30° / 0°
  - [ ] Auto-activate

- [ ] **ISOMETRIC_OT_QuickCreate_TrueIsometric**
  - [ ] Create True Isometric camera
  - [ ] Angles: 45° / 35.264° / 0°
  - [ ] Auto-activate

- [ ] **ISOMETRIC_OT_QuickCreate_Dimetric**
  - [ ] Create Dimetric camera
  - [ ] Angles: 45° / 30° / 0°
  - [ ] Auto-activate

- [ ] **ISOMETRIC_OT_QuickCreate_Trimetric**
  - [ ] Create Trimetric camera
  - [ ] Angles: 60° / 30° / 0°
  - [ ] Auto-activate

- [ ] **ISOMETRIC_OT_QuickCreate_Military**
  - [ ] Create Military (top-down) camera
  - [ ] Angles: 0° / 90° / 0°
  - [ ] Auto-activate

- [ ] **ISOMETRIC_OT_QuickCreate_Cavalier**
  - [ ] Create Cavalier camera
  - [ ] Angles: 0° / 0° / 45°
  - [ ] Auto-activate

### Phase 2: Advanced Setup

- [ ] **ISOMETRIC_OT_CreateCustom**
  - [ ] Custom isometric with all parameters
  - [ ] Use settings from advanced panel
  - [ ] Optional scene elements (grid, axes, scale)

- [ ] **ISOMETRIC_OT_SetAngles**
  - [ ] Change angles on existing camera
  - [ ] Apply preset angles
  - [ ] Update camera rotation

- [ ] **ISOMETRIC_OT_ResetAngles**
  - [ ] Reset to True Isometric angles
  - [ ] 45° / 35.264° / 0°

### Phase 3: Tools

- [ ] **ISOMETRIC_OT_FrameSelection**
  - [ ] Calculate bounding box of selected objects
  - [ ] Auto-fit ortho_scale
  - [ ] Optional padding parameter

- [ ] **ISOMETRIC_OT_LevelCamera**
  - [ ] Ensure camera is perfectly level
  - [ ] Check X/Y/Z rotations
  - [ ] Warn if tilted

### Phase 4: UI Panels

- [ ] Quick Create panel (7 preset buttons)
- [ ] Advanced Settings panel (custom setup)
- [ ] Settings panel (adjust existing cameras)
- [ ] Category organization (game/technical/plans)

### Phase 5: Optional Scene Elements

- [ ] Reference grid creation
  - [ ] Configurable size and subdivisions
  - [ ] Aligned to world axes

- [ ] Axis indicators
  - [ ] XYZ arrows in world space
  - [ ] Color-coded (R/G/B)

- [ ] Scale reference
  - [ ] Floor plane + cube
  - [ ] Known dimensions for scale

### Phase 6: Helper Functions

- [ ] `create_isometric_camera()` - Complete rig creation
- [ ] `set_isometric_angles()` - Apply preset angles
- [ ] `update_orthographic_scale()` - Zoom helper
- [ ] `frame_selection()` - Auto-fit to objects
- [ ] `reset_to_isometric()` - Reset to standard angles

---

## Key UX Principles

### 1. IsoCam-Style Instant Activation ✅

**Camera is active immediately:**
- ✅ Created and set as scene.camera
- ✅ Viewport switches to camera view
- ✅ See isometric view instantly
- ✅ No extra clicks needed

### 2. Clear Visual Categories ✅

**Organized by visual style, not angles:**
- ✅ Game & Pixel Art
- ✅ Technical & CAD
- ✅ Plans & Maps
- ✅ Easy to know which to pick

### 3. Perfect Angles Out of the Box ✅

**Every preset is mathematically correct:**
- ✅ Game Isometric: 26.565° (2:1 ratio)
- ✅ True Isometric: 35.264° (arctan(1/√2))
- ✅ Dimetric: 30° (standard variation)
- ✅ Military: 90° (perfect top-down)

### 4. Easy to Switch Presets ✅

**Can change projection after creation:**
- ✅ Select camera
- ✅ Click different preset button
- ✅ Angles update instantly
- ✅ No need to recreate

---

## Comparison to IsoCam Add-on

### Similarities (Familiar UX)

**What we keep from IsoCam:**
- ✅ One-click preset creation
- ✅ Instant camera activation
- ✅ Multiple projection types
- ✅ Frame selection tool
- ✅ Orthographic scale adjustment

### Improvements

**What we do better:**
- ✅ More presets (7 vs 3)
- ✅ Clearer category organization
- ✅ Visual descriptions of each type
- ✅ Optional scene elements (grid, axes)
- ✅ Advanced panel for full control
- ✅ Integrated with VR toolkit

---

## Summary

The **1-click preset workflow** for Isometric Camera is perfect because:

1. **Instant results** - One click, isometric view active
2. **Clear choices** - Know which projection style to pick
3. **IsoCam-familiar** - Existing users feel at home
4. **Perfect angles** - Mathematically correct presets
5. **Easy switching** - Change projection anytime

**Result:** Users get perfect isometric views in 1 second, not 1 minute of angle tweaking. The preset system makes technical projection theory accessible to everyone.
