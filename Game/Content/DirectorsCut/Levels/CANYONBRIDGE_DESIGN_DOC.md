# L_CanyonBridge - Design Document & Implementation Plan

**Project:** Directors Cut VR (BulldogMegaJam)
**Engine:** Unreal Engine 5.8
**Platform:** Meta Quest 3
**Author:** Claude Code (handoff to Aura)
**Date:** 2026-11-14

---

## 1. Level Concept

### Theme
A vertigo-inducing rope bridge crossing over a deep canyon. The player must carefully walk across a rickety wooden bridge with missing slats, creating tension and fear of heights.

### Gameplay
- Player spawns at one end of a 3-meter rope bridge
- Bridge spans a deep canyon with visible drop
- Some slats are missing, requiring careful foot placement
- Wind audio and subtle bridge sway enhance immersion
- Success: reach the other side

### Inspiration
- Indiana Jones rope bridge scenes
- "Directors Cut" theme: iconic movie vertigo moments

---

## 2. Asset Inventory

### Bridge Meshes (ln37 contribution - Nov 13-14)

| Asset | Path | Dimensions | Notes |
|-------|------|------------|-------|
| beam.uasset | `/Game/DirectorsCut/Meshes/beam` | 12.9 x 450 x 17.2 cm | Side rails |
| slat.uasset | `/Game/DirectorsCut/Meshes/slat` | 100 x 15.3 x 3.7 cm | Walkway planks |
| lambert3.uasset | `/Game/DirectorsCut/Meshes/lambert3` | - | Beam material |
| phong1.uasset | `/Game/DirectorsCut/Meshes/phong1` | - | Slat material |
| Wood textures | `/Game/DirectorsCut/Meshes/` | - | AO, diffuse maps |

### Canyon Environment (to be added)

| Asset | Source | Path |
|-------|--------|------|
| Canyon rocks | GrandCanyonRocks (Fab) | `/Game/ThirdParty/GrandCanyonRocks/` |
| Cliff meshes | Kenney Space Station | `/Game/ThirdParty/Kenney_SpaceStation/` |
| Skybox | Built-in or custom | TBD |

### Audio (to be added)

| Sound | Source | Purpose |
|-------|--------|---------|
| Wind ambient | Kenney UI Audio or custom | Canyon atmosphere |
| Wood creak | Custom/Freesound | Bridge stress sounds |
| Footstep wood | Kenney or custom | Player feedback |

---

## 3. Current Implementation Status

### Completed
- [x] Level created: `L_CanyonBridge.umap`
- [x] FBX assets imported manually (beam.fbx, slat.fbx)
- [x] 2 BridgeBeam actors placed (X=-50, X=50)
- [x] 10 BridgeSlat actors placed (Y=-200 to Y=205, step ~45cm)
- [x] Meshes assigned to StaticMeshComponents
- [x] Level saved

### Current Actor Layout
```
BridgeBeam_Left:   Location=(-50, 0, 0)    Mesh=beam
BridgeBeam_Right:  Location=(50, 0, 0)     Mesh=beam
BridgeSlat_0:      Location=(0, -200, 0)   Mesh=slat
BridgeSlat_1:      Location=(0, -155, 0)   Mesh=slat
BridgeSlat_2:      Location=(0, -110, 0)   Mesh=slat
BridgeSlat_3:      Location=(0, -65, 0)    Mesh=slat
BridgeSlat_4:      Location=(0, -20, 0)    Mesh=slat
BridgeSlat_5:      Location=(0, 25, 0)     Mesh=slat
BridgeSlat_6:      Location=(0, 70, 0)     Mesh=slat
BridgeSlat_7:      Location=(0, 115, 0)    Mesh=slat
BridgeSlat_8:      Location=(0, 160, 0)    Mesh=slat
BridgeSlat_9:      Location=(0, 205, 0)    Mesh=slat
```

### Not Yet Implemented
- [ ] Canyon walls/environment
- [ ] Skybox
- [ ] Lighting setup
- [ ] PlayerStart positioning
- [ ] BP_VRPawn_ISDK placement
- [ ] Missing slat gaps (for gameplay tension)
- [ ] Bridge rope/cable meshes
- [ ] Audio ambience
- [ ] Win condition (reach other side)

---

## 4. Implementation Steps

### Phase 1: Environment Setup

1. **Add Canyon Walls**
   ```python
   from unreal_helper import actor

   # Spawn canyon wall actors on each side
   actor('spawn_from_class',
         class_path='/Script/Engine.StaticMeshActor',
         location=[-300, 0, -500])
   # Then set mesh via exec_python
   ```

2. **Configure Skybox**
   - Add SkyAtmosphere or use BP_Sky_Sphere
   - Set to outdoor desert/canyon look

3. **Add Lighting**
   ```python
   actor('spawn_from_class',
         class_path='/Script/Engine.DirectionalLight',
         location=[0, 0, 500],
         rotation=[0, -45, 0])

   actor('spawn_from_class',
         class_path='/Script/Engine.SkyLight',
         location=[0, 0, 200])
   ```

### Phase 2: Bridge Refinement

1. **Remove Some Slats** (for gameplay)
   - Delete slats 2, 5, 8 to create gaps
   - Player must step carefully
   ```python
   actor('delete_by_label', actor_label='BridgeSlat_2')
   actor('delete_by_label', actor_label='BridgeSlat_5')
   actor('delete_by_label', actor_label='BridgeSlat_8')
   ```

2. **Add Rope/Cable Meshes** (optional)
   - Spline mesh for handrails
   - Or use cylinder primitives

3. **Adjust Bridge Height**
   - Move entire bridge up so canyon drop is visible below
   ```python
   # Move all bridge actors up by 200 units
   for i in range(10):
       actor('set_actor_property',
             actor_label=f'BridgeSlat_{i}',
             property_path='RelativeLocation',
             value={'X': 0, 'Y': ..., 'Z': 200})
   ```

### Phase 3: VR Player Setup

1. **Copy BP_VRPawn_ISDK**
   - Source: `/Game/ColdStart/Blueprints/BP_VRPawn_ISDK`
   - Destination: `/Game/DirectorsCut/Blueprints/BP_VRPawn_ISDK`
   - This pawn has working ISDK hand tracking

2. **BP_VRPawn_ISDK Component Hierarchy**
   ```
   DefaultSceneRoot
   ├── VRCamera (CameraComponent, bLockToHmd=true)
   ├── MotionController_Left (MotionSource=Left)
   │   └── LeftHandRig (IsdkHandRigComponentLeft)
   └── MotionController_Right (MotionSource=Right)
       └── RightHandRig (IsdkHandRigComponentRight)
   ```

3. **Add PlayerStart**
   ```python
   actor('spawn_from_class',
         class_path='/Script/Engine.PlayerStart',
         location=[0, -250, 200],  # Behind bridge start
         rotation=[0, 90, 0])      # Face toward bridge
   ```

4. **Create GameMode**
   - Set default pawn to BP_VRPawn_ISDK
   - Or set in World Settings for this level only

### Phase 4: Audio & Polish

1. **Add Ambient Sound**
   ```python
   actor('spawn_from_class',
         class_path='/Script/Engine.AmbientSound',
         location=[0, 0, 100])
   # Set sound asset manually or via exec_python
   ```

2. **Add Trigger Volume at End**
   - TriggerBox at far end of bridge
   - On overlap: Play success sound, fade to black, return to menu

---

## 5. GenOrca/MCP Usage Guide

### Connection Test
```bash
cd C:\Bulldog\Game
python unreal_helper.py
# Should print current level name
```

### Common Actions
```python
from unreal_helper import actor, material, asset, level, exec_python

# Spawn actor
actor('spawn_from_class', class_path='/Script/Engine.StaticMeshActor', location=[0,0,0])

# List actors
actor('list_all_with_locations')

# Delete actor
actor('delete_by_label', actor_label='ActorName')

# Set property
actor('set_actor_property', actor_label='MyActor', property_path='RelativeLocation', value={'X':0,'Y':0,'Z':100})

# For object references (meshes, materials), use exec_python:
exec_python("""
import unreal
subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = subsystem.get_all_level_actors()
for a in actors:
    if 'BridgeSlat' in a.get_actor_label():
        comp = a.get_component_by_class(unreal.StaticMeshComponent)
        mesh = unreal.EditorAssetLibrary.load_asset('/Game/DirectorsCut/Meshes/slat')
        comp.set_static_mesh(mesh)
""")
```

### CRITICAL: Deprecated API Warning
**NEVER use `unreal.EditorLevelLibrary`** - it's deprecated in UE5.8.

```python
# BAD - Deprecated
unreal.EditorLevelLibrary.get_editor_world()
unreal.EditorLevelLibrary.load_level()

# GOOD - Use subsystems
subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
subsystem.get_current_level()
subsystem.new_level('/Game/Path/To/Level')
```

---

## 6. Known Issues & Limitations

### FBX Import Crashes Editor
- **Issue:** Importing FBX via Python (`AssetImportTask`) causes TaskGraph assertion failure
- **Error:** `Assertion failed: ++Queue(QueueIndex).RecursionGuard == 1 [TaskGraph.cpp:705]`
- **Workaround:** Import FBX manually via Content Browser
- **Bug Report:** `C:\Bulldog\BUG_REPORT_FBX_IMPORT_TASKGRAPH.md`

### Viewport Camera Control Not Working
- **Issue:** Cannot programmatically frame camera on actors via MCP
- **Workaround:** Manual camera positioning in editor
- **Status:** Logged to Discord devlog for investigation

### GenOrca Object References
- **Issue:** `set_component_property` cannot set object references (meshes, materials, textures)
- **Workaround:** Use `exec_python()` with proper Python API calls

---

## 7. Reference Documents

| Document | Path |
|----------|------|
| Project Plan | `C:\Users\wendell\.claude\plans\staged-launching-lemon.md` |
| Consolidation Status | `C:\Bulldog\CONSOLIDATION_STATUS.md` |
| Sourced Assets | `C:\Bulldog\Game\Content\ThirdParty\SOURCED_ASSETS.md` |
| ISDK Migration Report | `C:\Bulldog\Archive\PreJam_ColdStart\ISDK_MIGRATION_REPORT.md` |
| Blueprint Specs | `C:\Bulldog\Game\Content\ColdStart\ColdStart_Blueprint_Specs.md` |

---

## 8. Success Criteria

- [ ] Player can spawn at bridge start with working hand tracking
- [ ] Bridge is visually complete with beams, slats, and gaps
- [ ] Canyon environment creates sense of height/vertigo
- [ ] Player can walk across bridge
- [ ] Reaching the end triggers completion
- [ ] Level runs on Quest 3 without performance issues

---

## 9. Timeline

**Deadline:** Nov 15, 2026 8:59 PM ET

| Task | Priority | Est. Time |
|------|----------|-----------|
| Canyon environment | HIGH | 30 min |
| VR pawn setup | HIGH | 15 min |
| Lighting | MEDIUM | 15 min |
| Audio | MEDIUM | 15 min |
| Polish & test | HIGH | 30 min |

---

*Document created for handoff to Aura - 2026-11-14*
