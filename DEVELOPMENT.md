# ColdStart MVP - Development Guide

**Project:** Bulldog MegaJam 2026 (Epic AI MegaJam)
**Engine:** Unreal Engine 5.8
**Platform:** Meta Quest 3 Standalone VR
**Team Collaboration:** This guide helps new team members get up to speed quickly.

---

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/wendellj/Bulldog2026EpicAIMegaJam.git
cd Bulldog2026EpicAIMegaJam/Game
```

### 2. Setup Development Environment
Follow detailed steps in: **`SETUP_GENORCA_INSTRUCTIONS.md`**

**TL;DR:**
- Install Unreal Engine 5.8
- Install Python 3.11
- Install UnrealMCPython plugin
- Configure Claude Code with `.mcp.json`
- Launch via `LaunchEditor.bat` (sets Android SDK paths)

### 3. Open Project
```bash
# Launch with MCP server auto-start
LaunchEditor.bat

# Or open manually
"C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe" BulldogMegaJam.uproject
```

### 4. Test VR Preview
- Click **⋮** next to Play button
- Select **"VR Preview"**
- Put on Quest 3 with Link Cable or Air Link active
- Verify controls are visible and glowing

---

## Development Workflow

### Daily Routine

**Start of session:**
1. Pull latest from Git: `git pull`
2. Run cleanup script: `python Game/cleanup_level.py`
3. Open editor via `LaunchEditor.bat`
4. Check VR Preview works

**During development:**
1. Make changes (use GenOrca for procedural edits)
2. Test in VR Preview frequently
3. Take screenshots of progress (save to `devlog_media/screenshots/`)
4. Commit often with descriptive messages

**End of session:**
1. Run through `VR_TEST_CHECKLIST.md`
2. Commit and push: `git add . && git commit -m "Description" && git push`
3. Update `DEVLOG.md` with daily entry
4. Post standup to Discord #standup channel

### Build & Deploy to Quest

**Full rebuild workflow:**
```bash
# 1. Cook content
cook_android.bat

# 2. Build APK
build_apk_nocache.bat

# 3. Create OBB
powershell -ExecutionPolicy Bypass -File create_obb.ps1

# 4. Deploy to Quest
deploy_quest.bat
```

**Quick iteration (content-only changes):**
```bash
# Skip APK rebuild, just push updated paks
push_paks.bat
```

**Debug tools:**
```bash
# Live logs
logcat_ue.bat

# Screenshot from Quest
screenshot_quest.bat
```

---

## Project Structure

```
Bulldog2026EpicAIMegaJam/
├── Game/
│   ├── Content/
│   │   └── ColdStart/
│   │       ├── Levels/
│   │       │   └── L_ColdStart.umap        # Main level
│   │       ├── Blueprints/
│   │       │   ├── BP_ShipState.uasset     # Game state manager
│   │       │   └── Components/
│   │       │       ├── BPC_PushButton
│   │       │       ├── BPC_GuardCover
│   │       │       ├── BPC_ToggleSwitch
│   │       │       └── BPC_PushBreaker
│   │       ├── Materials/
│   │       │   ├── M_ControlGlow           # Emissive parent
│   │       │   ├── MI_Ctrl_Red
│   │       │   ├── MI_Ctrl_Green
│   │       │   ├── MI_Ctrl_Orange
│   │       │   └── MI_Ctrl_Cyan
│   │       └── UI/
│   │           ├── WBP_FaultDisplay
│   │           └── WBP_FaultTree
│   ├── Config/
│   │   └── DefaultEngine.ini               # Project settings
│   ├── Plugins/
│   │   └── UnrealMCPython/                 # GenOrca plugin
│   └── .mcp.json                           # MCP server config
├── devlog_media/                           # Dev log assets
│   ├── screenshots/
│   ├── videos/
│   └── discord/
├── DEVLOG.md                               # Glass Box prize submission
├── VR_TEST_CHECKLIST.md                    # QA checklist
├── DEVELOPMENT.md                          # This file
├── SETUP_GENORCA_INSTRUCTIONS.md           # Team onboarding
└── .gitignore                              # Git ignore rules
```

---

## AI-Assisted Development

### GenOrca (UnrealMCPython)

**What it is:** Python API for procedural Unreal editing via Claude Code

**When to use:**
- Batch operations (spawn 10 actors, delete all temp objects)
- Automated setup (configure materials, set properties)
- Level cleanup and organization

**Example usage:**
```python
from unreal_helper import actor

# Spawn actor
actor('spawn_from_class',
      class_path='/Script/Engine.TextRenderActor',
      location=[0, 130, 150],
      rotation=[0, 180, 0])

# Set component property
actor('set_component_property',
      actor_label='MyActor',
      component_name='NewTextRenderComponent',
      property_name='Text',
      value='Hello World')

# List all actors
result = actor('list_all_with_locations')
for a in result.get('actors', []):
    print(f"{a['name']} at {a['location']}")
```

**Available action modules:**
- `actor()` - spawn, delete, list, properties, components
- `material()` - material parameters
- `asset()` - asset operations
- `level()` - level operations

**Documentation:** See `Game/Plugins/UnrealMCPython/Content/Python/UnrealMCPython/*_actions.py`

### Claude Code Integration

**Setup:** Already configured in `.mcp.json`

**Usage:**
1. Ask Claude to perform editor tasks
2. Claude calls GenOrca actions automatically
3. Results shown in chat

**Examples:**
- "Delete all actors with '_0' in the name"
- "Set all control materials to glow brighter"
- "List all components on the VR pawn"

---

## Common Tasks

### Add a New Interactive Control

1. **Create Blueprint Component:**
   - Duplicate `BPC_PushButton` in Content Browser
   - Rename (e.g., `BPC_MyControl`)
   - Open and modify components/variables

2. **Configure Material:**
   - Duplicate `MI_Ctrl_Red`
   - Set Color parameter to desired HDR value (10.0+ for brightness)
   - Assign to mesh in component

3. **Place in Level:**
   - Drag from Content Browser into viewport
   - Position inside room walls (X or Y = ±130cm max)
   - Set rotation to face player

4. **Wire Event Graph:**
   - Add interaction logic (OnPressed, OnGrab, etc.)
   - Communicate with BP_ShipState for game state

5. **Test in VR Preview**

### Adjust Lighting

**Make it darker:**
```python
from unreal_helper import actor

# Reduce SkyLight
actor('set_component_property',
      actor_label='SkyLight',
      component_name='LightComponent',
      property_name='Intensity',
      value=0.01)  # Very dim
```

**Make controls glow brighter:**
- Open material instance (MI_Ctrl_*)
- Set Color parameter R/G/B to higher values (20.0+)

### Add Text Display

Use `setup_status_display_genorca.py` as template:
1. Spawn TextRenderActor
2. Set text content, size, color via GenOrca
3. Position on wall facing player

---

## Testing

### Before Every Commit

Run: **`VR_TEST_CHECKLIST.md`** (Pre-Build section)

Key checks:
- [ ] VR Preview works
- [ ] All controls visible and glowing
- [ ] No black screen
- [ ] Frame rate smooth

### Before Quest Deploy

Run: **`VR_TEST_CHECKLIST.md`** (Build section)

Key checks:
- [ ] All assets saved
- [ ] No console errors
- [ ] Default map set correctly

### After Quest Deploy

Run: **`VR_TEST_CHECKLIST.md`** (Post-Build section)

Key checks:
- [ ] App launches
- [ ] Hand tracking works
- [ ] Performance acceptable (72fps)

---

## Troubleshooting

### Editor Won't Start
- **Check:** MCP server running on port 12029?
- **Fix:** Kill python processes, restart `LaunchEditor.bat`

### Black Screen in VR Preview
- **Check:** Default map set in DefaultEngine.ini?
- **Fix:** Edit → Project Settings → Maps & Modes → Default Maps

### Controls Not Glowing
- **Check:** Material Color parameter set to HDR values?
- **Fix:** Open MI_Ctrl_* instances, set Color to 10.0+ per channel

### Hand Tracking Not Working
- **Check:** VR Pawn has OculusXRHandComponent?
- **Fix:** Delete pawn, use Tools → Meta XR → Building Blocks → VR Pawn

### Gradle Build Fails
- **Check:** gradle.properties has configuration-cache disabled?
- **Fix:** Add `org.gradle.configuration-cache=false` to Game/Intermediate/Android/arm64/gradle/gradle.properties

### Content Not Loading on Quest
- **Check:** Pak files up to date?
- **Fix:** Run `push_paks.bat` to update paks directly

---

## Git Workflow

### Branching Strategy

**Main branch:** Production-ready code only
**Feature branches:** `feature/your-name/feature-name`

```bash
# Create feature branch
git checkout -b feature/wendell/new-puzzle

# Work on feature, commit often
git add .
git commit -m "Add puzzle mechanism"

# Push to remote
git push -u origin feature/wendell/new-puzzle

# When ready, create PR to main
```

### Commit Message Format

```
Type: Brief description

Detailed explanation if needed

- Bullet points for changes
- Reference issue numbers if applicable
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code restructuring
- `docs:` Documentation
- `test:` Testing
- `chore:` Maintenance

**Example:**
```
feat: Add emergency breaker interaction

Implemented BPC_PushBreaker component with:
- Reset animation
- State management (tripped/reset)
- Integration with BP_ShipState
- Emissive material feedback
```

---

## Performance Guidelines

### Quest 3 Targets

- **Frame Rate:** 72fps minimum
- **Draw Calls:** < 200
- **Triangles:** < 1M visible
- **Real-time Lights:** Max 5 (we're at limit)

### Optimization Tips

1. **Disable shadows on lights** (already done)
2. **Use emissive materials** instead of real-time lights
3. **Keep post-process effects minimal** (bloom threshold high)
4. **Avoid transparent materials** (use masked if needed)
5. **Static lighting** where possible (bake lightmaps)

---

## Resources

### Documentation
- Unreal Engine: https://docs.unrealengine.com/5.0/
- Meta XR SDK: https://developers.meta.com/horizon/documentation/unreal/
- GenOrca: `Game/Plugins/UnrealMCPython/README.md`

### Team Communication
- **Discord:** #standup channel for daily updates
- **GitHub Issues:** Bug tracking and feature requests
- **Dev Log:** `DEVLOG.md` for Glass Box submission

### Equipment
- **Quest 3 Loan:** See `bc_game_jam_equipment_guide.txt`
- **Lab Hours:** See `bc_game_jam_hours_and_checklist.txt`

---

## Support

**Issues?**
1. Check `VR_TEST_CHECKLIST.md` common issues
2. Search Discord #standup for similar problems
3. Ask Claude Code (AI assistant)
4. Post in team Discord channel

**Need help with GenOrca?**
- See `SETUP_GENORCA_INSTRUCTIONS.md`
- Ask Claude Code for examples
- Check `*_actions.py` files for available functions

---

**Last Updated:** 2026-11-03
**Maintained By:** [Your name]
