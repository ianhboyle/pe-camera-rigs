# Task 006: Guide Updates Needed

**Date**: 2025-12-08
**Status**: Documentation Updates Required
**Parent Task**: task-006-implementation-summary.md

---

## Overview

The Isometric Camera property update callbacks implementation requires updates to user documentation. The guide currently instructs users to edit properties in **Modifier Properties**, but with the new interactive system, users should edit properties in **Object Properties** where they'll update in real-time.

---

## Files Requiring Updates

### 1. docs/guides/04-isometric-camera.mdx

**Priority**: HIGH - Core feature documentation

**Sections Needing Updates**:

#### Section: "Step 2: Adjust Settings" (Lines 49-54)

**Current**:
```markdown
### Step 2: Adjust Settings

1. **Select** the `Isometric_Controller`
2. Go to **Modifier Properties** tab (wrench icon)
3. Find the **"Isometric Camera"** modifier
4. Adjust **Ortho Scale** to zoom in/out
```

**Should Be**:
```markdown
### Step 2: Adjust Settings

1. **Select** the `Isometric_Controller`
2. Go to **Object Properties** tab (orange square icon)
3. Scroll down to **"Isometric Camera Settings"** panel
4. Adjust settings in real-time:
   - **Projection Type** - Switch between presets instantly
   - **Ortho Scale** - Zoom in/out
   - **Custom angles** - Available when Projection Type = Custom
```

---

#### Section: "Understanding the Settings" (Lines 172-228)

**Current Issues**:
- Says "All controls in **Modifier Properties**" (Line 174)
- Describes modifier inputs by socket index (0-6)
- Shows radians for custom angles without mentioning degrees
- No mention that properties update in real-time

**Should Add**:
```markdown
## Understanding the Settings

**Where to find:** Select `Isometric_Controller` → **Object Properties** tab → **"Isometric Camera Settings"** panel

**New in v1.1:** Settings now update in real-time! Change any property and the viewport updates immediately.

### 📐 Projection Type

Dropdown menu with 7 presets:
- **Game 2:1** - 26.565° tilt for 2:1 pixel art
- **Game 4:3** - 30° tilt for 4:3 pixel art
- **True Isometric** - 35.264° tilt, mathematically correct
- **Dimetric** - 30° variant
- **Military** - Top-down 90° view
- **Cavalier** - 45° oblique projection
- **Custom** - Define your own angles (shows custom angle inputs)

**Tip:** Switch between presets instantly to compare views!

---

### 🔍 Ortho Scale

Controls zoom level:
- **Smaller values** = zoomed in (tight framing)
- **Larger values** = zoomed out (wide view)
- **Default:** 10.0

**Examples:**
- **5.0** = Close-up (small object fills frame)
- **10.0** = Medium (character or furniture)
- **30.0** = Wide (building or large scene)

**Important:** With orthographic cameras, you zoom by changing scale, not by moving closer!

---

### Custom Angles (Only when Projection Type = Custom)

When **Custom** projection is selected, three additional angle inputs appear:

**Custom Rotation Z** (Degrees)
- Horizontal spin around Z-axis
- **0°** = Front
- **45°** = Diagonal
- **90°** = Side
- **180°** = Back

**Custom Tilt X** (Degrees)
- Vertical tilt (camera pitch)
- **0°** = Looking at horizon
- **35.264°** = Isometric-like
- **90°** = Top-down

**Custom Roll Y** (Degrees)
- Camera roll/banking (rarely used)
- **0°** = Level
- Usually keep at 0°

**Note:** Values are in degrees (Blender's UI preference). The addon handles radian conversion internally.
```

---

#### Section: "Degree to Radian Conversion" (Lines 231-251)

**Update Needed**: This section can be simplified or removed since properties now accept degrees.

**Suggested Update**:
```markdown
## Working with Angles

**Good News:** Custom angle properties use **degrees** in the UI for easier adjustment!

The addon handles radian conversion internally - you don't need to calculate radians yourself.

**Quick Reference:**
| Degrees | Description |
|---------|-------------|
| 0° | Front/Level |
| 30° | Shallow angle |
| 45° | Diagonal |
| 60° | Steep angle |
| 90° | Side/Top-down |
| 180° | Back/Upside-down |

**Tip:** Use whole number degrees for easy experimentation (15°, 30°, 45°, 60°, etc.)
```

---

#### Section: "Tutorial 4: Custom Angle Experimentation" (Lines 347-363)

**Current**:
```markdown
2. **Experiment with angles:**
   - Try **Rotation Z:** 0.52 (30°)
   - Try **Tilt X:** 0.87 (50°)
   - Keep **Roll Y:** 0.0
```

**Should Be**:
```markdown
2. **Experiment with angles:**
   - Select `Isometric_Controller`
   - Go to **Object Properties** → **Isometric Camera Settings**
   - Set **Projection Type** to **Custom**
   - Try **Custom Rotation Z:** 30°
   - Try **Custom Tilt X:** 50°
   - Keep **Custom Roll Y:** 0°
   - **Watch the viewport update in real-time!**
```

---

### 2. docs/guides/07-troubleshooting.mdx

**Priority**: MEDIUM - Add new troubleshooting entries

**New Section to Add** (After line 220):

```markdown
### Can't find Isometric settings / Where are the controls?

**Location Changed in v1.1:**

Settings are now in **Object Properties** (not Modifier Properties):

1. Select `Isometric_Controller`
2. Look for **Object Properties** tab (orange square icon)
3. Scroll down to **"Isometric Camera Settings"** panel
4. Edit properties here - updates happen in real-time!

**Note:** You can still see the modifier in Modifier Properties, but editing there is not recommended.

---

### Isometric properties don't update viewport

**Symptoms:**
- Changed Projection Type but view doesn't change
- Adjusted Ortho Scale but zoom stays same
- Custom angles don't affect camera

**Causes:**
1. **Wrong object selected** - Must select `Isometric_Controller`, not the camera
2. **Editing modifier directly** - Use Object Properties instead
3. **Viewport not refreshing** (rare, known Blender limitation)

**Solutions:**
1. Verify you're editing properties in **Object Properties** panel
2. Select `Isometric_Controller` object (not camera)
3. If still not updating, try:
   - Press `Numpad 0` to refresh camera view
   - Switch to another viewport and back
   - Save and reload file (forces update)

**Known Limitation:**
There's a rare Blender issue ([#87006](https://developer.blender.org/T87006)) where geometry node modifier updates may not trigger viewport refresh. If you experience persistent issues, please report with your Blender version.

---
```

---

### 3. docs/guides/02-getting-started.mdx

**Priority**: LOW - Minor clarification

**Check**: Verify Getting Started guide mentions interactive property updates for Isometric rig.

**Suggested Addition** (if not present):
```markdown
**Interactive Rigs:**
- **Orbit Camera** - Adjust animation in Modifier Properties
- **Isometric Camera** - Adjust projection in Object Properties (real-time updates!)
```

---

## Summary of Changes

### Key Message to Communicate

**"Isometric Camera is now fully interactive!"**
- Properties update in real-time
- Edit in Object Properties (not Modifier Properties)
- Custom angles use degrees (not radians)
- Switch presets instantly to compare views

### Documentation Philosophy

**Before (v1.0)**:
- Settings were static after creation
- Users edited modifier inputs directly (technical, error-prone)
- Custom angles required radian calculations
- No real-time feedback

**After (v1.1)**:
- Settings update in real-time as you adjust them
- User-friendly Object Properties panel
- Custom angles use familiar degrees
- Instant visual feedback in viewport

---

## Implementation Checklist

- [ ] Update 04-isometric-camera.mdx - Section "Step 2: Adjust Settings"
- [ ] Update 04-isometric-camera.mdx - Section "Understanding the Settings"
- [ ] Update 04-isometric-camera.mdx - Section "Degree to Radian Conversion"
- [ ] Update 04-isometric-camera.mdx - Section "Tutorial 4: Custom Angle Experimentation"
- [ ] Update 07-troubleshooting.mdx - Add new troubleshooting entries
- [ ] Update 02-getting-started.mdx - Verify interactive rig description
- [ ] Update CHANGELOG.md - Add entry for v1.1 Isometric improvements
- [ ] Consider adding screenshot showing Object Properties panel location

---

## Additional Improvements to Consider

### 1. Add Screenshots

**High Value:**
- Screenshot showing Object Properties location
- Screenshot showing Isometric Camera Settings panel
- Before/after comparison of different projections

**Location**: Create `docs/images/isometric/` directory

### 2. Video Tutorial

**Consider**:
- 2-minute video showing real-time property updates
- Demonstrate switching between presets
- Show custom angle experimentation

### 3. Property Update Behavior Note

**Add to Technical Notes**:
```markdown
## Technical Note: Property Updates

The Isometric rig uses property update callbacks to synchronize UI properties with geometry node modifier inputs. This enables real-time viewport updates.

**For Developers:**
- Update callbacks in `properties.py`
- Socket mapping in `PROJECTION_TYPE_TO_INDEX`
- Degree-to-radian conversion handled automatically
- `context.view_layer.update()` called after each change

See [Blender API - bpy.props](https://docs.blender.org/api/current/bpy.props.html) for property update callback documentation.
```

---

## Testing Documentation Updates

**Before Publishing:**

1. **Follow the guide** - Create Isometric rig using updated instructions
2. **Verify accuracy** - Check all property locations match
3. **Test scenarios** - Try each tutorial step-by-step
4. **Check links** - Verify all internal links work
5. **Proofread** - Grammar, spelling, formatting

---

## Priority Assessment

| Update | Priority | Reason | Estimated Time |
|--------|----------|--------|----------------|
| 04-isometric-camera.mdx | HIGH | Core feature docs | 30-45 min |
| 07-troubleshooting.mdx | MEDIUM | User support | 15 min |
| 02-getting-started.mdx | LOW | Overview only | 5 min |
| Screenshots | MEDIUM | Visual clarity | 20 min |
| CHANGELOG.md | HIGH | Version tracking | 5 min |

**Total Time**: ~1.5 hours

---

## Version Note for CHANGELOG.md

**Suggested Entry**:

```markdown
## [1.1.0] - 2025-12-08

### Added - Isometric Camera
- **Real-time property updates** - Isometric rig properties now update viewport in real-time
- **User-friendly angle inputs** - Custom angles now use degrees instead of radians
- **Object Properties panel** - Settings moved from Modifier Properties for easier access
- Property update callbacks for all Isometric settings (projection type, ortho scale, custom angles)

### Changed - Code Quality
- Replaced `traceback.print_exc()` with Python logging module (11 instances)
- Removed emojis from VR workflow panel labels (13 instances)
- Organized imports to module level (3 files)
- Extracted `set_modifier_input()` to shared utility function

### Technical
- All changes follow official Blender Python API best practices
- Validated against Blender Developers Blog logging standards
- Property update callbacks validated against bpy.props documentation

### Known Limitations
- Geometry node property updates may have rare viewport refresh issues in some Blender versions ([Issue #87006](https://developer.blender.org/T87006))
```

---

## Rollback Documentation

If property update callbacks have issues:

1. Document workaround in troubleshooting guide
2. Add note about editing modifier directly as fallback
3. Keep both methods documented until confirmed stable

---

**Status**: Documentation updates pending code testing
**Next Step**: Test Isometric property updates in Blender, then update documentation accordingly
