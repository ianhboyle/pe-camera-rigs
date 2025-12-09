# Task 002-02: UX Refinement - VR360 Mono Camera

**Created:** 2025-12-08
**Status:** Planning
**Priority:** High
**Focus:** VR360 Mono Camera Rig
**Parent Task:** task-002-01-vr180-ux.md
**Updated:** 2025-12-08 (Revised to 4-step workflow with sequences)

---

## Executive Summary

The **4-step professional workflow** is the right approach for VR360 Mono. This follows the same crash-safe pattern as VR180:
- ✅ **Only ONE camera** (no stereo, no IPD)
- ✅ **Crash-safe sequences** (same as VR180, but only 1 folder)
- ✅ **Compositor for tweaks** (color correction, denoising, effects)
- ✅ **Simpler metadata** (mono vs stereo)

**Refinement Goals:**
1. **Automate the boring parts** of each step
2. **Make each step crystal clear** (no guessing what to do next)
3. **Smart defaults** (works perfectly out of the box)
4. **Professional flexibility** (can override when needed)
5. **Crash recovery** (don't lose hours of rendering)

---

## The Refined 4-Step Workflow

### Why 4 Steps is GOOD for VR360 Mono

**Same Professional Benefits as VR180:**
- ✅ **Crash recovery** - Don't lose hours of rendering if Blender crashes
- ✅ **Manual control** - Tweak compositor before final export
- ✅ **Industry standard** - Matches professional VFX workflows (separate render/comp)
- ✅ **Checkpoints** - Verify each stage before moving forward
- ✅ **Flexibility** - Re-composite without re-rendering (saves hours!)
- ✅ **Archival** - Keep high-quality EXR sequences for later

**Simpler than VR180:**
- ✅ **One camera** - Only one sequence folder (not two)
- ✅ **Simpler compositor** - Process single sequence (not combine two)
- ✅ **No IPD settings** - No left/right eye alignment
- ✅ **Mono metadata** - Simpler spatial-media injection

---

## STEP 1: Create VR360 Scene

### Button Label
```
[1️⃣ Create VR360 Scene]
```

### What It Does (Fully Automated)

**One button press creates EVERYTHING:**

```
Output after clicking:
├─ 📷 VR360 Camera
│   ├─ VR360_Camera (at 1.6m eye level)
│   ├─ Type: PANO + EQUIRECTANGULAR
│   ├─ Resolution: 5120×2560 (default)
│   ├─ 360° field of view
│   └─ Already LEVEL (X=0°, Y=0°)
│
├─ 💡 Lighting Setup (VR_Lighting collection)
│   └─ Based on selected preset (default: 3-Point Studio)
│
├─ 🎬 Cyclorama Stage (VR_Background collection)
│   ├─ Cyclorama_Floor (size based on selection)
│   ├─ Cyclorama_Wall (curved transition, scaled to size)
│   ├─ Material color (white, gray, or black)
│   ├─ Default size: 20m × 20m (user can choose 10m or 30m)
│   └─ Default color: Neutral gray (user can choose white or black)
│
├─ 👤 Reference Sphere (VR_Reference collection)
│   └─ Sphere_Reference (0.5m radius at 1.0m height)
│
└─ ⚙️ Auto-Configuration
    ├─ Scene.render.engine = 'CYCLES'
    ├─ Scene.render.resolution_x = 5120
    ├─ Scene.render.resolution_y = 2560
    ├─ Aspect ratio = 2:1 (equirectangular)
    ├─ GPU rendering enabled (OptiX/HIP detected)
    ├─ Collections organized
    ├─ Camera view activated
    └─ Camera auto-leveled
```

### Success Message

```
✅ VR360 Scene Created!

Camera: VR360_Camera at (0, 0, 1.6m)
Resolution: 5120×2560 (YouTube 5K)
Type: Equirectangular 360°
Collections: VR_Cameras, VR_Lighting, VR_Background, VR_Reference

👉 NEXT: Add your content, then click Step 2 to render sequences
```

### User Actions After Step 1

User now:
1. Adds their content (characters, objects, animations)
2. Positions/animates VR360_Camera if needed
3. Adjusts lighting/materials if desired
4. Sets animation frame range
5. When ready → Click Step 2

### Lighting Type Selection (Same 8 Options as VR180)

**Dropdown menu visible BEFORE clicking Step 1:**

```
Lighting: [3-Point (Studio) ▼]  ← User chooses BEFORE clicking button

Dropdown options:
  1. None
  2. 3-Point (Studio) ⭐ (default)
  3. 3-Point (Outdoor)
  4. Studio Multi-Light
  5. Outdoor Natural
  6. Outdoor Overcast
  7. Stage/Performance
  8. Custom Preset...
```

### Cyclorama Size & Color Selection (Same as VR180)

**Size options:**
- 10m × 10m (Small/Intimate)
- 20m × 20m (Medium) ⭐ (default)
- 30m × 30m (Large/Spacious)

**Color options:**
- White (High-key, Bright)
- Neutral Gray (Balanced) ⭐ (default)
- Black (Low-key, Dramatic)

### UI Panel State After Step 1

```
┌──────────────────────────────────────┐
│ VR360 Mono Professional Workflow     │
├──────────────────────────────────────┤
│ ✅ Step 1: Scene Created             │
│    Camera: VR360_Camera              │
│    Resolution: 5120×2560 (2:1)       │
│    Lighting: 3-Point (Studio)        │
│                                      │
│ 👉 Next: Render Sequence             │
│                                      │
│ [2️⃣ Render EXR Sequence]             │
│   ↳ Renders crash-safe sequence     │
│     Format: OpenEXR (32-bit float)  │
│     Output: //output/vr360/frames/  │
│                                      │
│ Frame Range: [1] to [250]           │
│ Quality: [Production ▼] (512 samp)  │
│                                      │
└──────────────────────────────────────┘
```

---

## STEP 2: Render EXR Sequence

### Button Label
```
[2️⃣ Render EXR Sequence]
```

### What It Does (Fully Automated)

**Renders crash-safe EXR sequence:**

```
Process:
1. Detect VR360 camera in scene

2. Create output folder:
   //output/vr360/frames/

3. Configure render settings:
   ├─ Resolution: 5120×2560 (equirectangular)
   ├─ Format: OpenEXR (.exr)
   ├─ Codec: DWAA (compressed, lossless)
   ├─ Color depth: 32-bit float
   └─ Denoising: OptiX enabled

4. Render sequence:
   ├─ Render frame 1 → //output/vr360/frames/vr360_0001.exr
   │                    //output/vr360/frames/vr360_0002.exr
   │                    ...
   │                    //output/vr360/frames/vr360_0250.exr

5. Crash recovery (automatic):
   ├─ Checks for existing frames before starting
   ├─ If found: "Found frames 1-150, resuming from 151..."
   └─ Resumes where it left off (no re-render)
```

### File Naming Convention

**EXACTLY correct for Step 3 compositor:**

```
//output/vr360/
└─ frames/
   ├─ vr360_0001.exr
   ├─ vr360_0002.exr
   ├─ vr360_0003.exr
   └─ ...
```

### Progress Reporting

```
Rendering VR360 Sequence...

  Frame 125/250 | 3.5 fps | ETA: 36 min
  [████████████░░░░░░░░░░░░] 50%
```

### Success Message

```
✅ VR360 Sequence Rendered!

Frames: 250 frames → //output/vr360/frames/
Format: OpenEXR 32-bit (DWAA compressed)
File size: ~10.5 GB total
Resolution: 5120×2560 per frame

👉 NEXT: Click Step 3 to load compositor
```

### UI Panel State After Step 2

```
┌──────────────────────────────────────┐
│ VR360 Mono Professional Workflow     │
├──────────────────────────────────────┤
│ ✅ Step 1: Scene Created             │
│ ✅ Step 2: Sequence Rendered         │
│    Frames: 250 frames (10.5 GB)     │
│                                      │
│ 👉 Next: Load Compositor             │
│                                      │
│ [3️⃣ Setup Compositor]                │
│   ↳ Auto-loads sequence into nodes  │
│     Denoising: ☑ OptiX              │
│     Format: H.265 MP4               │
│                                      │
│   [Preview Frame: 125 ]             │
│                                      │
└──────────────────────────────────────┘
```

---

## STEP 3: Setup Compositor

### Button Label
```
[3️⃣ Setup Compositor]
```

### What It Does (Fully Automated)

**Creates compositor setup for processing single sequence:**

```
Process:
1. Create "VR360_Compositor" scene (or update existing)

2. Auto-detect sequence path:
   └─ //output/vr360/frames/vr360_####.exr

3. Build compositor node tree:

   SINGLE SEQUENCE PROCESSING:
   [Image Sequence]
   └─ vr360_####.exr
   │
   └─> [Denoise: OptiX]
       │
       └─> [Color Correction] (identity - user can tweak)
           │
           └─> [Composite Output]
               │
               └─> [Viewer]

4. Configure scene settings:
   ├─ Resolution: 5120×2560 (2:1 equirectangular)
   ├─ Frame range: Match original scene
   ├─ Output format: H.265 (temporary, for preview)
   └─ Compositor enabled

5. Switch to Compositing workspace

6. Load preview frame (mid-point of animation)

7. Success message with instructions
```

### Node Layout (Visual)

```
Compositor Node Editor (auto-generated):

┌─────────────────┐
│  Image Sequence │
│  vr360_####.exr │
└────────┬────────┘
         │
         v
    ┌──────────┐
    │ Denoise  │
    │  OptiX   │
    └─────┬────┘
          │
          v
  ┌───────────────┐
  │     Color     │
  │  Correction   │ ← User can add nodes here
  └───────┬───────┘
          │
          v
  ┌───────────────┐     ┌──────────┐
  │   Composite   │────>│  Viewer  │
  │    Output     │     │ (Preview)│
  └───────────────┘     └──────────┘
```

### Success Message

```
✅ Compositor Ready!

Scene: VR360_Compositor
Resolution: 5120×2560 (2:1 equirectangular)
Nodes created: 4 nodes, all connected
Sequence loaded:
  └─ //output/vr360/frames/vr360_####.exr
Denoising: OptiX enabled

Preview loaded: Frame 125

🔧 MANUAL TWEAKS (optional):
  ├─ Adjust denoising strength (if needed)
  ├─ Add color correction nodes
  ├─ Add vignette/effects
  └─ Tweak any parameters you want

👉 NEXT: When happy with preview, click Step 4 to render final YouTube video
```

### UI Panel State After Step 3

```
┌──────────────────────────────────────┐
│ VR360 Mono Professional Workflow     │
├──────────────────────────────────────┤
│ ✅ Step 1: Scene Created             │
│ ✅ Step 2: Sequence Rendered         │
│ ✅ Step 3: Compositor Ready          │
│    Scene: VR360_Compositor           │
│    Preview: Frame 125                │
│                                      │
│ 🔧 Make any manual tweaks now        │
│    (optional - compositor is ready)  │
│                                      │
│ 👉 Next: Render Final Video          │
│                                      │
│ [4️⃣ Render YouTube Video]            │
│   ↳ Composites to H.265 MP4         │
│     Format: H.265 (100 Mbps)        │
│     Metadata: VR360 auto-injected   │
│                                      │
│   Output: vr360_youtube.mp4         │
│                                      │
│   ☑ Auto-inject VR360 metadata      │
│   ☑ Verify metadata after render    │
│   ☐ Cleanup sequence (delete EXRs)  │
│                                      │
└──────────────────────────────────────┘
```

---

## STEP 4: Render YouTube Video

### Button Label
```
[4️⃣ Render YouTube Video]
```

### What It Does (Fully Automated)

**Renders final YouTube-ready MP4 with metadata:**

```
Process:
1. Switch to VR360_Compositor scene

2. Configure final output:
   ├─ Format: FFMPEG / MP4
   ├─ Video codec: H.265 (HEVC)
   ├─ Bitrate: 100 Mbps (YouTube high quality)
   ├─ GOP size: 15 (every 15 frames)
   ├─ Audio codec: AAC 384 kbps
   └─ Output: //output/vr360/vr360_temp.mp4

3. Render animation:
   ├─ Compositor processes sequence
   ├─ Applies denoising, color correction, effects
   ├─ Encodes to H.265
   └─ Progress: [████████████████] 100%

4. Inject VR360 metadata:
   ├─ Use spatial-media tool (bundled)
   ├─ Add spherical metadata (360° mono)
   ├─ Add VR360 mode (no stereo)
   └─ Output: //output/vr360/vr360_youtube.mp4

5. Verify metadata:
   ├─ Check spatial metadata exists
   ├─ Verify 360° mono mode correct
   └─ Confirm YouTube compatibility

6. Optional cleanup:
   └─ If checked: Delete EXR sequences (saves space)

7. Success message with file info
```

### Progress Reporting

```
Rendering Final YouTube Video...

Compositing equirectangular frames...
  Frame 125/250 | 8.5 fps | ETA: 15 min
  [████████████░░░░░░░░░░░░] 50%

Encoding H.265 video...
  [████████████████████████] 100%

Injecting VR360 metadata...
  ✓ Spatial metadata injected
  ✓ Mode: 360° mono
  ✓ YouTube VR compatible

Verifying metadata...
  ✓ Metadata verified successfully!
```

### Success Message

```
╔══════════════════════════════════════╗
║  ✅ VR360 YOUTUBE VIDEO READY!       ║
╚══════════════════════════════════════╝

File: //output/vr360/vr360_youtube.mp4
Size: 6.5 GB
Duration: 10 seconds (250 frames @ 25 fps)
Resolution: 5120×2560 (2:1 equirectangular)
Format: H.265 (HEVC) @ 100 Mbps
Audio: AAC 384 kbps
Metadata: ✅ VR360 spatial metadata injected
Status: ✅ YouTube VR compatible

📤 READY TO UPLOAD!
   ├─ Upload to YouTube
   ├─ YouTube will auto-detect VR360
   └─ Video will show VR button in player

🎥 Viewing Options:
   ├─ VR headset (full 360° immersion)
   ├─ YouTube mobile (swipe to look around)
   └─ Desktop browser (drag to look around)

🗑️  Optional: Cleanup sequences?
   ├─ Delete 250 EXR files (10.5 GB)
   └─ Keep final MP4 only (6.5 GB)

   [Delete Sequences] [Keep Everything]
```

---

## UI Panel Design (All Steps Combined)

### Complete Panel Layout

```
┌───────────────────────────────────────────────────┐
│ VR360 Mono Professional Workflow                  │
├───────────────────────────────────────────────────┤
│                                                   │
│ 📋 Quick Start Guide:                             │
│   1️⃣ Create scene with camera & lighting          │
│   2️⃣ Render crash-safe EXR sequences              │
│   3️⃣ Load compositor (make manual tweaks)         │
│   4️⃣ Render final YouTube MP4 with metadata       │
│                                                   │
├───────────────────────────────────────────────────┤
│                                                   │
│ ⚙️  Settings                                       │
│                                                   │
│ Preset: [YouTube 5K (Recommended) ▼]             │
│   ℹ️ 5120×2560 @ 60fps                            │
│      Best quality/speed balance                   │
│                                                   │
│ Camera:                                           │
│   Height: [1.6] m (eye level)                    │
│   Type: Equirectangular (360°)                   │
│                                                   │
│ Quality: [Production ▼]                           │
│   • Preview (256 samples) - Fast                 │
│   • Production (512 samples) - Balanced ⭐        │
│   • Final (1024 samples) - Best quality          │
│                                                   │
│ Output Path: [//output/vr360/              📁]   │
│                                                   │
├───────────────────────────────────────────────────┤
│                                                   │
│ 🎬 STEP 1: Create Scene                           │
│                                                   │
│ Lighting: [3-Point (Studio) ▼]                   │
│   • None (no lights)                             │
│   • 3-Point (Studio) ⭐ DEFAULT                   │
│   • 3-Point (Outdoor)                            │
│   • Studio Multi-Light                           │
│   • Outdoor Natural                              │
│   • Outdoor Overcast                             │
│   • Stage/Performance                            │
│   • Custom Preset...                             │
│                                                   │
│ Include:                                          │
│   ☑ Cyclorama Stage                              │
│      Size: [20m × 20m ▼]                         │
│        • 10m × 10m (small/intimate)              │
│        • 20m × 20m (medium) ⭐ DEFAULT            │
│        • 30m × 30m (large/spacious)              │
│      Color: [Neutral Gray ▼]                     │
│        • White (high-key, bright)                │
│        • Neutral Gray (balanced) ⭐ DEFAULT       │
│        • Black (low-key, dramatic)               │
│   ☑ Reference Sphere (0.5m radius)               │
│                                                   │
│ [1️⃣ Create VR360 Scene]                           │
│   ↳ Creates: camera + chosen lighting + stage    │
│                                                   │
│ Status: ⏸️ Not created                             │
│                                                   │
├───────────────────────────────────────────────────┤
│                                                   │
│ 📹 STEP 2: Render Sequence                        │
│                                                   │
│ Frame Range: [1] to [250] (250 frames)           │
│                                                   │
│ Format: OpenEXR (crash-safe, 32-bit float)       │
│ Denoising: ☑ OptiX                               │
│                                                   │
│ [2️⃣ Render EXR Sequence]                          │
│   ↳ Renders vr360_####.exr frames                │
│                                                   │
│ Status: ⏸️ Not rendered                            │
│                                                   │
├───────────────────────────────────────────────────┤
│                                                   │
│ 🎨 STEP 3: Setup Compositor                       │
│                                                   │
│ Processing: Single equirectangular sequence      │
│ Denoising: ☑ OptiX                               │
│                                                   │
│ [3️⃣ Setup Compositor]                             │
│   ↳ Auto-loads sequence, creates nodes           │
│                                                   │
│ Preview Frame: [125   ]  [Update Preview]        │
│                                                   │
│ Status: ⏸️ Not setup                               │
│                                                   │
│ 💡 After clicking: Make manual tweaks in         │
│    Compositing workspace (optional)              │
│                                                   │
├───────────────────────────────────────────────────┤
│                                                   │
│ 🎥 STEP 4: Render YouTube Video                   │
│                                                   │
│ Output: vr360_youtube.mp4                         │
│                                                   │
│ Video Settings:                                   │
│   Format: H.265 (HEVC) @ 100 Mbps               │
│   Audio: AAC @ 384 kbps                          │
│   Aspect: 2:1 (equirectangular)                 │
│                                                   │
│ ☑ Auto-inject VR360 metadata                     │
│ ☑ Verify metadata after render                   │
│ ☐ Delete sequences after render (save 10 GB)    │
│                                                   │
│ [4️⃣ Render YouTube Video]                         │
│   ↳ Composites + injects metadata                │
│                                                   │
│ Status: ⏸️ Not rendered                            │
│                                                   │
├───────────────────────────────────────────────────┤
│                                                   │
│ 🛠️  Camera Tools                                   │
│                                                   │
│ [Level Camera] [Check Setup] [Frame Selection]   │
│                                                   │
└───────────────────────────────────────────────────┘
```

---

## VR180 vs VR360 Mono Comparison

### Workflow Similarities ✅

**Both follow same professional pattern:**

| Step | VR180 Fisheye | VR360 Mono |
|------|---------------|------------|
| **1** | Create scene | Create scene |
| **2** | Render sequences (L+R) | Render sequence (single) |
| **3** | Compositor (combine) | Compositor (process) |
| **4** | Export + metadata | Export + metadata |

### Key Differences

| Feature | VR180 Fisheye | VR360 Mono |
|---------|---------------|------------|
| **Cameras** | 2 cameras (L/R) | 1 camera |
| **Sequences** | 2 folders (left/right) | 1 folder (frames) |
| **Compositor** | Combine two views | Process one view |
| **IPD** | 64mm (adjustable) | N/A (mono) |
| **FOV** | 180° fisheye | 360° equirect |
| **Depth** | Stereoscopic 3D | None (2D) |
| **Metadata** | Stereo left-right | Mono 360° |

### When to Use Each

**VR360 Mono:**
- ✅ 360° tours (real estate, tourism)
- ✅ Events/concerts (see full environment)
- ✅ 2D content is fine (no depth needed)
- ✅ Slightly simpler than VR180 (1 sequence vs 2)

**VR180 Fisheye:**
- ✅ Immersive storytelling (need depth)
- ✅ Close-up experiences (personal, intimate)
- ✅ Professional VR production
- ✅ Stereoscopic 3D required

---

## Error Handling

### Step 2 Errors

**Error: No VR360 camera found**
```
❌ No VR360 camera found in scene!

👉 Solution: Click Step 1 to create scene first
   Then come back to Step 2

[Go to Step 1] [Cancel]
```

**Warning: Large file size**
```
⚠️  This will create LARGE files!

Frame range: 1-1000 (1000 frames)
Estimated size: ~42 GB
Available disk space: 30 GB

❌ NOT ENOUGH DISK SPACE!

Options:
  1. Reduce frame range (render in batches)
  2. Free up disk space
  3. Change output path to larger drive

[Change Settings] [Cancel]
```

### Step 3 Errors

**Error: Sequence not found**
```
❌ EXR sequence not found!

Expected:
  //output/vr360/frames/vr360_####.exr

👉 Solution: Run Step 2 to render sequence first

[Go to Step 2] [Browse...] [Cancel]
```

**Warning: Partial sequence**
```
⚠️  Incomplete sequence detected!

Found: 150/250 frames ❌ (100 frames missing!)

Options:
  [Resume Render]  Render missing frames (Step 2)
  [Use Partial]    Load compositor anyway (will error on frame 151+)
  [Cancel]

Recommended: Resume render to complete sequence
```

### Step 4 Errors

**Error: Metadata injection failed**
```
❌ VR360 metadata injection FAILED!

Video created: vr360_temp.mp4
But: NO VR360 metadata (will play as flat video on YouTube)

Solutions:
  [Try Again]           Retry metadata injection
  [Manual Injection]    Open guide for manual metadata
  [Skip Metadata]       Keep video without VR metadata

⚠️  Without metadata, YouTube won't recognize as VR360!
```

---

## Implementation Checklist

### Phase 1: Core Operators

- [ ] **VR360_OT_CreateScene** (Step 1)
  - [ ] Create equirectangular camera function
  - [ ] **Create lighting function (8 types)**
  - [ ] **Create cyclorama function (3 sizes, 3 colors)**
  - [ ] Create reference sphere function
  - [ ] Auto-configuration (GPU, resolution, etc.)
  - [ ] Collection organization
  - [ ] Camera auto-level
  - [ ] Success message with next steps

- [ ] **VR360_OT_RenderSequence** (Step 2)
  - [ ] Detect VR360 camera
  - [ ] Create output folder: //output/vr360/frames/
  - [ ] Configure OpenEXR format
  - [ ] Crash recovery (detect existing frames)
  - [ ] Render sequence
  - [ ] Progress reporting with ETA
  - [ ] Success message with stats

- [ ] **VR360_OT_SetupCompositor** (Step 3)
  - [ ] Create/update compositor scene
  - [ ] Auto-detect sequence path
  - [ ] Create Image Sequence node
  - [ ] Create Denoise node
  - [ ] Create Color Correction node (identity)
  - [ ] Create Composite Output node
  - [ ] Create Viewer node
  - [ ] Link all nodes correctly
  - [ ] Switch to Compositing workspace
  - [ ] Load preview frame
  - [ ] Success message with manual tweak instructions

- [ ] **VR360_OT_RenderYouTube** (Step 4)
  - [ ] Check compositor ready
  - [ ] Configure H.265 output
  - [ ] Render compositor animation
  - [ ] Create temp MP4 file
  - [ ] Inject VR360 metadata (spatial-media)
  - [ ] Verify metadata
  - [ ] Rename to final file
  - [ ] Optional: cleanup sequences
  - [ ] Success message with upload instructions
  - [ ] Optional: open output folder

### Phase 2: UI Panel

- [ ] Main panel layout (4 steps visible)
- [ ] Settings section (presets, height, quality)
- [ ] Step 1 section (lighting, cyclorama options)
- [ ] Step 2 section (frame range, format options)
- [ ] Step 3 section (preview frame control)
- [ ] Step 4 section (metadata options, cleanup)
- [ ] Progressive status updates (checkmarks, stats)
- [ ] "Next step" hints (dynamic based on current state)
- [ ] Camera tools section

### Phase 3: Error Handling

- [ ] Friendly error messages (not cryptic)
- [ ] Solutions provided (tell user what to do)
- [ ] Warnings for large files/long renders
- [ ] Disk space checks
- [ ] Sequence validation (complete vs partial)
- [ ] Metadata injection fallbacks

### Phase 4: Automation & Smart Defaults

- [ ] Preset system (YouTube 5K, 8K, Quest)
- [ ] Quality presets (Preview, Production, Final)
- [ ] Auto-detect GPU (OptiX, HIP, CUDA, CPU)
- [ ] Auto-level camera function
- [ ] Crash recovery (automatic resume)
- [ ] File naming conventions
- [ ] Path detection (sequence from Step 2)
- [ ] Preview frame auto-selection (mid-point)
- [ ] 2:1 aspect ratio enforcement

### Phase 5: Helper Functions

- [ ] `create_vr360_mono_camera()` - Camera creation
- [ ] `create_cyclorama()` - Stage setup (shared with VR180)
- [ ] `create_lighting_preset()` - Lighting rigs (shared with VR180)
- [ ] `inject_vr360_metadata()` - Metadata injection
- [ ] `verify_vr360_metadata()` - Check metadata exists
- [ ] `check_camera_level()` - Detect camera tilt
- [ ] `format_time()` - Human-readable time (ETA display)
- [ ] `format_file_size()` - Human-readable file sizes

---

## Summary: Key Improvements

### 1. Crash Recovery ✅

**Same as VR180:**
- ✅ Render to EXR sequences (crash-safe)
- ✅ Auto-resume from last frame
- ✅ Don't lose hours of work if Blender crashes

**Simpler than VR180:**
- ✅ Only one sequence folder (not two)
- ✅ Easier to manage files

### 2. Professional Checkpoints ✅

**After Step 2 (Render Sequence):**
- ✅ Verify render quality
- ✅ Check if animation looks good
- ✅ Re-render if needed (before compositor)

**After Step 3 (Compositor):**
- ✅ Preview with denoising/color correction
- ✅ Make manual tweaks if desired
- ✅ Re-composite without re-rendering

### 3. Flexibility ✅

**Can re-composite later:**
- ✅ Keep EXR sequences for archival
- ✅ Re-export with different color grading
- ✅ Add effects years later
- ✅ No need to re-render (saves hours!)

### 4. Consistent Pattern ✅

**Both VR workflows follow same philosophy:**
1. Scene setup
2. Crash-safe rendering
3. Compositor processing
4. Final export with metadata

**Result:** Users familiar with VR180 will understand VR360 immediately.

---

**Created:** 2025-12-08
**Last Updated:** 2025-12-08 (Revised to 4-step workflow)
**Status:** Planning - Ready for Implementation
