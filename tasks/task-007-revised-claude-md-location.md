# Task 007 REVISED: CLAUDE.md File Locations (Avoiding Distribution)

**Date**: 2025-12-08
**Status**: Planning - Revised
**Issue**: Original plan would include CLAUDE.md files in distributable zip

---

## Problem with Original Plan

**Original Recommendation**: Place CLAUDE.md files in source directories
```
src/pe_camera_rigs/
├── rigs/CLAUDE.md
├── utils/CLAUDE.md
└── ui/CLAUDE.md
```

**Issue**: Current packaging command includes everything:
```bash
cd src
zip -r ../pe_camera_rigs.zip pe_camera_rigs  # Includes ALL files!
```

**Result**: CLAUDE.md files would be distributed to end users ❌

---

## Revised Recommendation: Keep CLAUDE.md in docs/

**Better Approach**: Mirror source structure in `docs/` directory

### Proposed Structure

```
blender-camera-rigs-addon/
├── CLAUDE.md                           # Main overview + critical guidelines
├── CHANGELOG.md
├── README.md
├── docs/
│   ├── CLAUDE.md                       # Documentation standards (exists)
│   └── dev/                            # NEW: Developer documentation
│       ├── README.md                   # Index of all dev docs
│       ├── rigs/
│       │   ├── README.md              # Rig system overview
│       │   ├── orbit.md               # Orbit rig specifics
│       │   ├── isometric.md           # Isometric rig specifics
│       │   ├── vr180.md               # VR180 rig specifics
│       │   └── vr360mono.md           # VR360 rig specifics
│       ├── ui.md                       # UI development guide
│       └── utils.md                    # Utilities guide
└── src/
    └── pe_camera_rigs/                # Clean - no CLAUDE.md files
        ├── rigs/
        ├── ui/
        └── utils/
```

**Benefits**:
- ✅ No CLAUDE.md files in distributable code
- ✅ Documentation organized near code conceptually
- ✅ Can still use descriptive names (README.md, not CLAUDE.md)
- ✅ No need to modify zip command
- ✅ Clean separation of dev docs from user docs

---

## Alternative: Exclude CLAUDE.md from Zip

**If you really want CLAUDE.md in source directories:**

### Option A: Use .zipignore Pattern

Update packaging command to exclude CLAUDE.md:
```bash
cd src
zip -r ../pe_camera_rigs.zip pe_camera_rigs -x "*/CLAUDE.md" -x "CLAUDE.md"
```

**Pros**:
- Documentation lives with code
- Claude Code has better context

**Cons**:
- Need to remember exclusion pattern
- Easy to forget and ship CLAUDE.md files
- More complex packaging command

### Option B: Create Packaging Script

Create `scripts/package.sh`:
```bash
#!/bin/bash
# Package PE Camera Rigs addon for distribution

cd "$(dirname "$0")/.."
VERSION=${1:-dev}

echo "Packaging PE Camera Rigs v${VERSION}..."

cd src
zip -r "../pe_camera_rigs_v${VERSION}.zip" pe_camera_rigs \
  -x "*/CLAUDE.md" \
  -x "CLAUDE.md" \
  -x "*/__pycache__/*" \
  -x "*.pyc" \
  -x ".DS_Store"

echo "Created: pe_camera_rigs_v${VERSION}.zip"
echo "Verifying structure..."
unzip -l "../pe_camera_rigs_v${VERSION}.zip" | head -20
```

Usage:
```bash
./scripts/package.sh 1.1.0
```

**Pros**:
- Consistent packaging
- Never forget exclusions
- Can add version numbers

**Cons**:
- Need to maintain script
- Still risk of forgetting to use it

---

## Recommended Solution: docs/dev/ Structure

**I recommend keeping CLAUDE.md files OUT of src/** for these reasons:

### 1. Cleaner Distribution
- No need for exclusion patterns
- Impossible to accidentally ship dev docs
- Simpler packaging process

### 2. Clear Separation
- `src/` = production code only
- `docs/` = all documentation (user + dev)
- Clear mental model

### 3. Better Organization
- Can use better filenames (README.md instead of CLAUDE.md)
- Can include diagrams, examples without distribution concerns
- Natural place for developer guides

### 4. Claude Code Still Works
Claude Code can find documentation via:
- Root CLAUDE.md points to all dev docs
- Cross-references in each doc
- Consistent naming makes it predictable

---

## Proposed Content Structure

### Root CLAUDE.md (~100 lines)

```markdown
# CLAUDE.md

## Project Overview
[Brief overview]

## ⚠️ IMPORTANT: Git Commit Guidelines
[CRITICAL section - keep in full]

## Architecture Overview
[High-level with links]

## Developer Documentation

**Module-Specific Guides** (in `docs/dev/`):
- [Rig System](./docs/dev/rigs/README.md)
  - [Orbit Rig](./docs/dev/rigs/orbit.md)
  - [Isometric Rig](./docs/dev/rigs/isometric.md)
  - [VR180 Rig](./docs/dev/rigs/vr180.md)
  - [VR360 Mono Rig](./docs/dev/rigs/vr360mono.md)
- [UI Development](./docs/dev/ui.md)
- [Utilities](./docs/dev/utils.md)

## Quick Reference
[Common patterns and pitfalls]
```

### docs/dev/README.md (Index)

```markdown
# Developer Documentation

Complete technical documentation for PE Camera Rigs addon development.

## Module Guides

### Rig System
- [Rig Architecture Overview](./rigs/README.md)
- Individual Rigs:
  - [Orbit Camera](./rigs/orbit.md) - Procedural turntable animations
  - [Isometric Camera](./rigs/isometric.md) - Orthographic projections
  - [VR180](./rigs/vr180.md) - Stereoscopic VR workflow
  - [VR360 Mono](./rigs/vr360mono.md) - 360° panoramic VR

### Supporting Systems
- [UI Development](./ui.md) - Panel system and conventions
- [Utilities](./utils.md) - Shared helper functions

## Getting Started
[Links to setup, architecture, etc.]

## Code Quality Standards
[Links to standards]
```

### docs/dev/rigs/isometric.md

```markdown
# Isometric Camera Rig - Developer Guide

**Location**: `src/pe_camera_rigs/rigs/isometric/`

## Overview
Creates true isometric and axonometric projection views using Geometry Nodes.

## Module Structure
- `__init__.py` - Registration
- `operators.py` - `ISOMETRIC_OT_add_controller`
- `panels.py` - `ISOMETRIC_PT_add_panel`
- `properties.py` - Property groups and update callbacks

## Property Update Callbacks (v1.1+)

### Implementation
[Detailed explanation with code examples]

### Socket Mapping
- Socket_1: Projection Type (Int 0-6)
- Socket_2: Ortho Scale (Float)
- Socket_3: Custom Rotation Z (Radians)
- Socket_4: Custom Tilt X (Radians)
- Socket_5: Custom Roll Y (Radians)

### Testing
[Testing checklist]

## Known Limitations
[Issue #87006 details]

## Recent Changes
[Version history]
```

---

## Implementation Plan (Revised)

### Phase 1: Create docs/dev/ Structure
1. [ ] Create `docs/dev/` directory
2. [ ] Create `docs/dev/README.md` (index)
3. [ ] Create `docs/dev/rigs/` directory
4. [ ] Create `docs/dev/rigs/README.md` (rig system overview)

### Phase 2: Create Module Guides
5. [ ] Create `docs/dev/rigs/orbit.md`
6. [ ] Create `docs/dev/rigs/isometric.md`
7. [ ] Create `docs/dev/rigs/vr180.md`
8. [ ] Create `docs/dev/rigs/vr360mono.md`
9. [ ] Create `docs/dev/ui.md`
10. [ ] Create `docs/dev/utils.md`

### Phase 3: Update Root CLAUDE.md
11. [ ] Condense root CLAUDE.md
12. [ ] Add links to docs/dev/ guides
13. [ ] Ensure critical guidelines remain

### Phase 4: Verification
14. [ ] Package zip and verify no CLAUDE.md files
15. [ ] Test Claude Code finds docs
16. [ ] Validate all cross-references

---

## Comparison: Three Approaches

| Aspect | Original (CLAUDE.md in src/) | Exclude Pattern | docs/dev/ (Recommended) |
|--------|------------------------------|-----------------|-------------------------|
| **Packaging** | Include CLAUDE.md in zip ❌ | Need exclusion pattern | No exclusions needed ✅ |
| **Maintenance** | Simple | Complex | Simple |
| **Risk** | High (ship dev docs) | Medium (forget exclusion) | Low (separate dirs) |
| **Clarity** | Docs with code | Docs with code | Clear separation |
| **Claude Context** | Best (most local) | Best (most local) | Good (via links) |

---

## Updated Packaging Guide

No changes needed to packaging guide since docs/ is already excluded from src/.

Current packaging remains simple:
```bash
cd src
zip -r ../pe_camera_rigs.zip pe_camera_rigs
```

✅ No CLAUDE.md files
✅ No docs/ directory
✅ Clean addon code only

---

## Benefits of docs/dev/ Approach

### For Distribution
- **Zero risk** of shipping dev docs
- **Simple packaging** - no exclusion patterns needed
- **Clean user experience** - only addon code

### For Development
- **Centralized docs** - all in docs/ directory
- **Better filenames** - can use README.md, specific names
- **Richer content** - can include diagrams, examples
- **Clear ownership** - docs team owns docs/, dev team owns src/

### For Claude Code
- **Still discoverable** - root CLAUDE.md links to all docs
- **Predictable structure** - follows common pattern
- **Rich context** - docs can be more detailed without bloat

---

## Recommended File Names

Instead of CLAUDE.md everywhere, use descriptive names:

```
docs/dev/
├── README.md                # Developer docs index
├── architecture.md          # System architecture
├── code-quality.md          # Standards and conventions
├── rigs/
│   ├── README.md           # Rig system overview
│   ├── orbit.md            # Orbit rig guide
│   ├── isometric.md        # Isometric rig guide
│   ├── vr180.md           # VR180 rig guide
│   └── vr360mono.md       # VR360 rig guide
├── ui.md                   # UI development
└── utils.md               # Utilities reference
```

**Why better**:
- More descriptive than CLAUDE.md
- Standard convention (README.md for directories)
- Easier for human developers too
- Still easy for Claude Code to find

---

## Migration Path

### Quick Start (30 minutes)
1. Create `docs/dev/` with basic structure
2. Move isometric-specific content from root CLAUDE.md
3. Update root CLAUDE.md with link
4. Test packaging to verify exclusion

### Full Implementation (3 hours)
1. Create all docs/dev/ guides
2. Migrate content from root CLAUDE.md
3. Add cross-references
4. Update root CLAUDE.md to be index
5. Test and validate

---

## Conclusion

**Recommendation**: Use `docs/dev/` structure, NOT CLAUDE.md in `src/`

**Reasoning**:
1. Zero risk of shipping dev docs to users
2. Simpler packaging (no exclusions needed)
3. Better organization (clear separation)
4. Richer documentation possible
5. Standard practice (many projects do this)

**Trade-off**: Slightly less local context for Claude Code, but mitigated by:
- Clear links from root CLAUDE.md
- Predictable structure
- Can still be very detailed

---

**Status**: Revised plan complete
**Recommendation**: Implement docs/dev/ structure
**Priority**: Medium (after testing current implementation)
**Estimated Time**: 3 hours for full implementation
