# Task 002-03: UX Refinement - Orbit Camera

**Created:** 2025-12-08
**Status:** Planning
**Priority:** High
**Focus:** Orbit Camera Rig
**Parent Task:** task-002-01-vr180-ux.md

---

## Executive Summary

The **1-click preset workflow** is perfect for Orbit Camera. This camera type is all about **speed and convenience**:
- ✅ **Quick product shots** - One click, perfect orbit
- ✅ **Character turnarounds** - Instant character showcase
- ✅ **Preset-based** - No complex settings, just choose style
- ✅ **Immediate animation** - Camera already animated

**Refinement Goals:**
1. **One-click presets** - Instant perfect orbits
2. **Clear preset categories** - Know which to choose
3. **Smart defaults** - Works perfectly out of the box
4. **Optional tweaking** - Can adjust after creation

---

## The Refined Preset Workflow

### Why Preset-Based is Perfect for Orbit Camera

**Orbit cameras are predictable:**
- ✅ **Known use cases** - Product, character, architecture, etc.
- ✅ **Standard distances** - Each use case has typical radius
- ✅ **Consistent patterns** - Circular motion, specific duration
- ✅ **Repeatable setups** - Same settings work every time

**User just picks what they need:**
- ✅ **Product Photography** - 3m radius, 35mm lens, clean lighting
- ✅ **Character Showcase** - 4m radius, 50mm lens, soft lighting
- ✅ **Hero Shot** - 2.5m radius, 24mm wide, dramatic low angle
- ✅ **Detail Inspection** - 1.5m radius, 85mm telephoto, close-up
- ✅ **Architectural** - 15m radius, 35mm, building walkaround

---

## The ONE-CLICK Preset System

### Preset Categories

The panel is organized by **use case**, not by technical settings:

```
┌─────────────────────────────────────┐
│ Orbit Camera - Quick Create         │
├─────────────────────────────────────┤
│                                     │
│ 📦 Product Visualization             │
│   [Product Photography]             │
│   [Detail Close-Up]                 │
│                                     │
│ 👤 Character & Animation             │
│   [Character Showcase]              │
│   [Hero Shot]                       │
│                                     │
│ 🏗️  Architecture & Environment       │
│   [Architectural Walkaround]        │
│   [Environment Tour]                │
│                                     │
│ 🔧 Custom Setup                      │
│   [Advanced Settings...]            │
│                                     │
└─────────────────────────────────────┘
```

### What Each Preset Creates

**Every preset button does ALL of this in one click:**

1. **Creates camera rig**
   - Parent empty (pivot point)
   - Camera with constraint
   - Target empty at origin

2. **Sets perfect parameters**
   - Orbit radius (distance from subject)
   - Camera height (eye level vs low vs high)
   - Focal length (wide vs normal vs telephoto)

3. **Adds scene elements**
   - Reference capsule (1.8m person scale)
   - Lighting rig (preset-specific)
   - Floor plane (optional)

4. **Animates orbit**
   - Full 360° rotation
   - Duration based on preset
   - Linear or eased motion

5. **Activates camera**
   - Sets as scene camera
   - Switches to camera view
   - Ready to preview

---

## Preset Specifications

### 📦 Product Photography

**Perfect for:** Product renders, ecommerce, clean professional shots

```
What it creates:
├─ Orbit Radius: 3.0m (medium distance)
├─ Camera Height: 1.5m (table height, slight high angle)
├─ Focal Length: 35mm (normal perspective)
├─ Duration: 240 frames (10 seconds @ 24fps)
├─ Lighting: PRODUCT preset
│   ├─ Key light: Soft area, 1600W, front-high
│   ├─ Fill light: Large area, 800W, opposite side
│   └─ Rim light: Point, 1000W, back-high (edge highlight)
├─ Reference: 1.8m capsule at origin
└─ Floor: 10m × 10m plane (clean surface)
```

**Use cases:**
- Product photography
- Ecommerce turntables
- Clean professional renders
- Catalog shots

---

### 📦 Detail Close-Up

**Perfect for:** Jewelry, watches, small objects, macro shots

```
What it creates:
├─ Orbit Radius: 1.5m (close distance)
├─ Camera Height: 0.0m (level with object)
├─ Focal Length: 85mm (telephoto, shallow DOF)
├─ Duration: 240 frames (10 seconds)
├─ Lighting: PRODUCT preset
│   └─ Close, controlled lighting for detail
├─ Reference: 1.8m capsule (may be too large, user removes)
└─ Floor: Optional (often removed for close-ups)
```

**Use cases:**
- Jewelry renders
- Watch details
- Small product close-ups
- Macro photography style

---

### 👤 Character Showcase

**Perfect for:** Character turnarounds, character sheets, model portfolios

```
What it creates:
├─ Orbit Radius: 4.0m (medium-far, full body visible)
├─ Camera Height: 1.6m (eye level with character)
├─ Focal Length: 50mm (natural portrait perspective)
├─ Duration: 360 frames (15 seconds @ 24fps)
├─ Lighting: SOFT preset
│   ├─ Key light: Large soft area, 1400W
│   ├─ Fill light: Very soft, 600W
│   └─ Rim light: Subtle, 700W (gentle separation)
├─ Reference: 1.8m capsule (character height guide)
└─ Floor: 10m × 10m (character stands on surface)
```

**Use cases:**
- Character turnarounds
- Model portfolio showcases
- Character design presentations
- Animation character sheets

---

### 👤 Hero Shot

**Perfect for:** Dramatic reveals, heroic poses, low-angle power shots

```
What it creates:
├─ Orbit Radius: 2.5m (closer, more dramatic)
├─ Camera Height: 0.5m (low angle, looking up)
├─ Focal Length: 24mm (wide angle, dramatic perspective)
├─ Duration: 120 frames (5 seconds @ 24fps - quick reveal)
├─ Lighting: DRAMATIC preset
│   ├─ Key light: Hard point, 2000W, low side (dramatic shadows)
│   ├─ Rim light: Strong, 1500W, back (glowing edge)
│   └─ No fill (high contrast, moody)
├─ Reference: 1.8m capsule
└─ Floor: 10m × 10m (dark material)
```

**Use cases:**
- Hero character reveals
- Dramatic product shots
- Low-angle power poses
- Cinematic character intros

---

### 🏗️ Architectural Walkaround

**Perfect for:** Buildings, vehicles, large structures

```
What it creates:
├─ Orbit Radius: 15.0m (far distance, see whole structure)
├─ Camera Height: 2.0m (human eye level)
├─ Focal Length: 35mm (architectural standard)
├─ Duration: 480 frames (20 seconds @ 24fps - slow tour)
├─ Lighting: SOFT preset (even, architectural)
│   ├─ Sun lamp (outdoor simulation)
│   ├─ Sky shader (ambient fill)
│   └─ Bounce fill (subtle)
├─ Reference: 1.8m capsule (scale reference)
└─ Floor: 30m × 30m (large ground plane)
```

**Use cases:**
- Building exteriors
- Vehicle turnarounds (cars, planes)
- Large product displays
- Architectural visualization

---

### 🏗️ Environment Tour

**Perfect for:** Environment art, level design, large scenes

```
What it creates:
├─ Orbit Radius: 20.0m (very far, see full environment)
├─ Camera Height: 3.0m (elevated view)
├─ Focal Length: 28mm (wide, see more environment)
├─ Duration: 600 frames (25 seconds - slow cinematic)
├─ Lighting: SOFT preset
│   └─ Natural outdoor lighting
├─ Reference: 1.8m capsule
└─ Floor: 50m × 50m (large environment ground)
```

**Use cases:**
- Environment art showcases
- Level design tours
- Large scene overviews
- Cinematic environment reveals

---

## UI Panel Design

### Quick Create Panel (Main)

```
┌───────────────────────────────────────────────────┐
│ Orbit Camera - Quick Create                       │
├───────────────────────────────────────────────────┤
│                                                   │
│ 📋 One-Click Perfect Orbits                       │
│                                                   │
│ Choose your use case below. Each button creates: │
│   • Camera rig with perfect settings             │
│   • Animated 360° orbit                          │
│   • Preset lighting                              │
│   • Reference objects                            │
│   • Ready to preview immediately!                │
│                                                   │
├───────────────────────────────────────────────────┤
│                                                   │
│ 📦 Product Visualization                          │
│                                                   │
│ [🎬 Product Photography]                          │
│   3m radius • 10s orbit • Clean lighting         │
│   Perfect for: Products, ecommerce, catalog      │
│                                                   │
│ [🔍 Detail Close-Up]                              │
│   1.5m radius • 85mm lens • Macro style          │
│   Perfect for: Jewelry, watches, small objects   │
│                                                   │
├───────────────────────────────────────────────────┤
│                                                   │
│ 👤 Character & Animation                          │
│                                                   │
│ [👤 Character Showcase]                           │
│   4m radius • 15s orbit • Soft lighting          │
│   Perfect for: Turnarounds, model sheets         │
│                                                   │
│ [⚡ Hero Shot]                                     │
│   2.5m low angle • 5s orbit • Dramatic           │
│   Perfect for: Hero reveals, power poses         │
│                                                   │
├───────────────────────────────────────────────────┤
│                                                   │
│ 🏗️  Architecture & Environment                    │
│                                                   │
│ [🏢 Architectural Walkaround]                     │
│   15m radius • 20s orbit • Even lighting         │
│   Perfect for: Buildings, vehicles, structures   │
│                                                   │
│ [🌍 Environment Tour]                             │
│   20m radius • 25s orbit • Cinematic             │
│   Perfect for: Environment art, level design     │
│                                                   │
├───────────────────────────────────────────────────┤
│                                                   │
│ 🔧 Advanced                                       │
│                                                   │
│ Need custom settings?                            │
│ [⚙️  Custom Setup...]                             │
│   ↳ Opens advanced panel with full controls     │
│                                                   │
└───────────────────────────────────────────────────┘
```

### Advanced Settings Panel (Optional)

**Only shown if user clicks "Custom Setup..."**

```
┌───────────────────────────────────────────────────┐
│ Orbit Camera - Advanced Settings                  │
├───────────────────────────────────────────────────┤
│                                                   │
│ 📷 Camera Settings                                │
│                                                   │
│ Orbit Radius: [3.0   ] m                         │
│ Camera Height: [1.5   ] m                        │
│ Focal Length: [35.0  ] mm                        │
│                                                   │
│ 🎬 Animation Settings                             │
│                                                   │
│ Duration: [Custom ▼] frames                      │
│   • 120 frames (5s)                              │
│   • 240 frames (10s) ⭐                           │
│   • 360 frames (15s)                             │
│   • Custom: [240   ] frames                      │
│                                                   │
│ Start Angle: [0    ]°                            │
│ End Angle: [360  ]°                              │
│                                                   │
│ Direction: [Clockwise ▼]                         │
│   • Clockwise                                    │
│   • Counter-Clockwise                            │
│                                                   │
│ Easing: [Linear ▼]                               │
│   • Linear (constant speed)                      │
│   • Ease In-Out (smooth start/stop)             │
│   • Ease In (slow start)                         │
│   • Ease Out (slow stop)                         │
│                                                   │
│ 💡 Lighting                                       │
│                                                   │
│ Preset: [Product ▼]                              │
│   • None                                         │
│   • Product (clean) ⭐                            │
│   • Soft (character)                             │
│   • Dramatic (hero)                              │
│                                                   │
│ 📦 Scene Elements                                 │
│                                                   │
│ ☑ Reference Capsule (1.8m)                       │
│ ☑ Floor Plane                                    │
│   Floor Size: [10  ] m                           │
│                                                   │
│ [Create Orbit Camera]                            │
│                                                   │
└───────────────────────────────────────────────────┘
```

---

## Success Messages

### After Preset Creation

```
✅ ORBIT CAMERA CREATED!

Preset: Product Photography
Camera: OrbitCamera_Product at 3.0m radius
Animation: 240 frames (10 seconds)
Lighting: Product preset (3-point clean)
Scene elements: Reference capsule, floor plane

🎥 Camera is ACTIVE and READY!
   ├─ Already in camera view
   ├─ Animation already set up
   └─ Press SPACEBAR to preview orbit

👉 NEXT STEPS:
  1. Add your product/object at origin (0, 0, 0)
  2. Press Spacebar to preview the orbit
  3. Adjust lighting/materials if needed
  4. Render animation when ready

💡 TIP: Select OrbitCamera_Pivot to:
  • Move entire rig (G key)
  • Rotate orbit starting angle (R Z)
```

---

## Error Handling

### Preset Creation Errors

**Error: Scene already has orbit camera**
```
⚠️  Orbit camera already exists in scene!

Existing camera: OrbitCamera_Product

Options:
  [Add Another]   Create new orbit camera (multi-camera)
  [Replace]       Delete existing, create new one
  [Cancel]        Keep existing, do nothing
```

**Warning: No object at origin**
```
ℹ️  Camera created, but no object at origin!

The orbit camera will circle around (0, 0, 0).

👉 Add your subject:
  1. Place object at origin (0, 0, 0), OR
  2. Move OrbitCamera_Target to your subject

[OK, Got It]
```

---

## Animation Tweaking

### After Creation, User Can:

**Adjust orbit duration:**
```
Select: OrbitCamera_Pivot
Panel: Orbit Camera - Settings
Change: Duration preset
Click: [Update Animation]
```

**Change orbit radius:**
```
Select: OrbitCamera_Pivot
Press: S (scale mode)
Scale larger/smaller
Note: Camera constraint maintains orbit
```

**Change starting angle:**
```
Select: OrbitCamera_Pivot
Press: R Z (rotate Z-axis)
Rotate to new starting position
Animation will start from new angle
```

**Adjust camera height:**
```
Select: OrbitCamera (camera object)
Press: G Z (move Z-axis)
Move up or down
```

---

## Implementation Checklist

### Phase 1: Preset Operators

- [ ] **ORBIT_OT_QuickCreate_Product**
  - [ ] Create product photography orbit
  - [ ] 3m radius, 1.5m height, 35mm
  - [ ] Product lighting preset
  - [ ] 240 frames animation
  - [ ] Reference capsule + floor

- [ ] **ORBIT_OT_QuickCreate_Detail**
  - [ ] Create detail close-up orbit
  - [ ] 1.5m radius, 0m height, 85mm
  - [ ] Product lighting preset
  - [ ] 240 frames animation

- [ ] **ORBIT_OT_QuickCreate_Character**
  - [ ] Create character showcase orbit
  - [ ] 4m radius, 1.6m height, 50mm
  - [ ] Soft lighting preset
  - [ ] 360 frames animation

- [ ] **ORBIT_OT_QuickCreate_Hero**
  - [ ] Create hero shot orbit
  - [ ] 2.5m radius, 0.5m height, 24mm
  - [ ] Dramatic lighting preset
  - [ ] 120 frames animation

- [ ] **ORBIT_OT_QuickCreate_Architectural**
  - [ ] Create architectural walkaround
  - [ ] 15m radius, 2m height, 35mm
  - [ ] Soft lighting preset
  - [ ] 480 frames animation

- [ ] **ORBIT_OT_QuickCreate_Environment**
  - [ ] Create environment tour
  - [ ] 20m radius, 3m height, 28mm
  - [ ] Soft lighting preset
  - [ ] 600 frames animation

### Phase 2: Advanced Setup

- [ ] **ORBIT_OT_CreateCustom**
  - [ ] Custom orbit with all parameters
  - [ ] Use settings from advanced panel
  - [ ] Apply selected lighting preset
  - [ ] Add optional scene elements

- [ ] **ORBIT_OT_UpdateAnimation**
  - [ ] Update keyframes on existing orbit
  - [ ] Change duration/easing/direction
  - [ ] Preserve other settings

### Phase 3: UI Panels

- [ ] Quick Create panel (6 preset buttons)
- [ ] Advanced Settings panel (custom setup)
- [ ] Settings panel (adjust existing orbits)
- [ ] Category organization (product/character/architecture)

### Phase 4: Lighting Presets

- [ ] PRODUCT lighting preset
  - [ ] Clean 3-point lighting
  - [ ] Soft key, large fill, rim highlight

- [ ] SOFT lighting preset
  - [ ] Character-friendly soft lighting
  - [ ] Large soft key, gentle fill

- [ ] DRAMATIC lighting preset
  - [ ] High-contrast moody lighting
  - [ ] Hard key, strong rim, minimal fill

### Phase 5: Helper Functions

- [ ] `create_orbit_camera_rig()` - Complete rig creation
- [ ] `animate_orbit()` - Keyframe circular motion
- [ ] `apply_lighting_preset()` - Create preset lights
- [ ] `add_reference_capsule()` - 1.8m person reference
- [ ] `add_floor_plane()` - Ground plane helper

---

## Key UX Principles

### 1. Instant Gratification ✅

**User clicks button → Immediately working:**
- ✅ Camera created and active
- ✅ Already in camera view
- ✅ Animation already set up
- ✅ Just add object and preview

### 2. Clear Categories ✅

**Organized by use case, not settings:**
- ✅ Product Visualization
- ✅ Character & Animation
- ✅ Architecture & Environment
- ✅ Each button clearly labeled

### 3. Perfect Defaults ✅

**Every preset is production-ready:**
- ✅ Proper orbit radius for subject
- ✅ Correct focal length for framing
- ✅ Appropriate lighting for style
- ✅ Sensible animation duration

### 4. Easy Tweaking ✅

**If defaults aren't perfect:**
- ✅ Select pivot → move entire rig
- ✅ Scale pivot → change radius
- ✅ Rotate pivot → change start angle
- ✅ Advanced panel for full control

---

## Summary

The **1-click preset workflow** is perfect for Orbit Camera because:

1. **Instant results** - One click, working camera
2. **Clear choices** - Know which preset to pick
3. **Perfect defaults** - Each preset is production-ready
4. **Easy to tweak** - Can adjust after creation
5. **Fast workflow** - No complex setup needed

**Result:** Users spend 5 seconds creating the camera, not 5 minutes configuring settings. They can focus on their content, not technical setup.
