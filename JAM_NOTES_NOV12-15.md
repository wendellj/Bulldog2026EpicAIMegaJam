# Bulldogs Directors Cut - Jam Notes (Nov 12-15, 2026)

## Epic AI MegaJam 2026

**Team:** Bellevue College Bulldogs
**Theme:** "Directors Cut" - VR experiences inspired by iconic movie scenes
**Platform:** Meta Quest 3 (hand tracking only, no controllers)
**Engine:** Unreal Engine 5.8 + Meta XR SDK + ISDK

---

## Day 1 (Nov 12) - ISDK Wiring & Hand Tracking

### What We Did
- Fixed VR hand tracking using Meta Interaction SDK (ISDK)
- Discovered that `XR_ERROR_ACTIONSET_NOT_ATTACHED` warnings do NOT block poke interactions
- Poke uses hand tracking position data, not Enhanced Input actions
- Wired ISDK components for button interactions

### Key Technical Discovery
ISDK poke interaction chain:
```
IsdkPokeInteractor (on finger tip)
    ↓ detects intersection with
IsdkPokeInteractable.surface_patch
    → IsdkClippedPlaneSurface.pointable_plane
        → IsdkPointablePlane (defines pokeable area)
```

### Files Created
- `POKE_EVENT_WIRING_INSTRUCTIONS.md` - Manual Blueprint wiring steps
- `POKE_WIRING_STATUS.md` - Component wiring checklist
- `POINTABLE_PLANE_WIRING.md` - Surface patch configuration

---

## Day 2 (Nov 13) - Level Integration & Bridge

### What We Did
- Imported ln37's bridge assets (beam.fbx, slat.fbx)
- Created canyon bridge level with cliff walls
- Set up wood texture materials (duckboard from Megascans)
- Worked on Guardian play area orientation Blueprint

### Bridge Setup
- Beam dimensions: 12.9 x 450 x 17.2 cm
- Slat dimensions: 100 x 15.3 x 3.7 cm
- 80cm gap between beams (player walks on slats)
- Canyon walls using desert cliff textures

### GenOrca Limitations Discovered
- Cannot delete Blueprint nodes
- Cannot set pin default values
- Cannot create typed Get nodes (creates generic wildcard)
- Object reference pins require manual wiring

---

## Day 3 (Nov 14) - Asset Consolidation & Levels

### What We Did
- Consolidated project structure under `Content/DirectorsCut/`
- Imported Rob's CliffPath level (rock dodge on mountain ledge)
- Created materials for cliff rocks, hiker body parts, dust effects
- Set up audio (wind loop, rock impacts, helicopter rescue)

### Levels Structure
```
Content/DirectorsCut/
├── MainMenu/Levels/L_MainMenu.umap
├── TheFall/Levels/L_TheFall.umap      (Nakatomi fall)
├── CliffPath/Levels/L_CliffPath.umap  (Rob's level)
├── Levels/L_CanyonBridge.umap         (Indiana Jones bridge)
├── Highway/Levels/L_Highway.umap      (Brian's Frogger)
└── CarHop/Levels/L_CarHop.umap        (Low-G car hopping)
```

### Rob's CliffPath Assets
- BP_FallingRock, BP_RockfallDirector (boulder spawning)
- BP_HikerBody (player body representation)
- BP_PlayerBounds (keep player on path)
- SM_Boulder_A/B/C, SM_CliffWall, SM_Mountain_A/B/C
- Audio: SW_WindLoop, SW_RockImpact, SW_RockRumble, SW_RescueHelicopter

---

## Day 4 (Nov 15) - Build & Submission

### Build Pipeline Issues & Fixes

**Problem 1: GameFeatureData Asset Manager errors**
- Error: "Asset manager settings do not include a rule for assets of type GameFeatureData"
- Tried multiple fixes in DefaultEngine.ini - all failed
- **Fix:** Moved `PrimaryAssetTypesToScan` to `DefaultGame.ini` (matches Engine's BaseGame.ini location)
```ini
[/Script/Engine.AssetManagerSettings]
+PrimaryAssetTypesToScan=(PrimaryAssetType="GameFeatureData",AssetBaseClass=/Script/GameFeatures.GameFeatureData,bHasBlueprintClasses=False,bIsEditorOnly=True,Directories=((Path="/Game")),SpecificAssets=,Rules=(Priority=-1,ChunkId=-1,bApplyRecursively=True,CookRule=Unknown))
```

**Problem 2: Gradle configuration cache error**
- Error: "cannot serialize object of type StripDebugSymbolsTask"
- **Fix:** Added `org.gradle.configuration-cache=false` to gradle.properties

**Problem 3: Invalid NDK_VERSION**
- Error: "Requested NDK version 'NDK' could not be parsed"
- Unreal sets `NDK_VERSION=NDK` (invalid string) on each cook
- **Fix:** Change to `NDK_VERSION=27.0.12077973` in gradle.properties after each cook

### Final Build
- APK: 293 MB (all data bundled inside with `bPackageDataInsideApk=True`)
- Location: `C:\Bulldog\Game\Binaries\Android\BulldogMegaJam-arm64.apk`
- Installed on Quest 3 via `metavr_app` MCP tool

### Submission Package
Created `C:\Bulldog\Bulldog_BulldogsDirectorsCut.zip` (268 MB):
- BulldogMegaJam-arm64.apk (293 MB compressed)
- README.txt (sideloading instructions)
- DEVLOG.html (Glass Box prize documentation)
- cover_630x500.png (itch.io cover image)
- thefall.mp4 (gameplay video)

### GitHub Push Issue
- GitHub blocked push due to Discord token in `Game/.mcp.json`
- **Fix:** Replaced token with placeholder `YOUR_DISCORD_TOKEN_HERE`
- Amended commit and pushed successfully

### Team Info Gathered
| Name | Discord | itch.io | Epic Email |
|------|---------|---------|------------|
| Wendell | wendell1036 | wendellj | wendell@bellevuecollege.edu |
| Rob | powerful_tiger_82951 | robsvin | robs83838@gmail.com |
| ln37 | ln37 | syenbu | Blackoutfox2@gmail.com |
| Jacob | kernkob | kernkob | jpboudrx@gmail.com |
| Brian | djprofk | [pending] | [pending] |

---

## Tools Used

### AI Tools (for Partner Prize)
- **Claude Code (Anthropic)** - Coding assistant, Blueprint wiring, build debugging
- **Hyper3D Rodin** - 3D model generation (cars for CarHop)

### MCP Servers
- **UnrealMCPython (GenOrca)** - Editor automation, actor spawning, material setup
- **metavr (Meta VR CLI)** - Device management, APK install, screenshots, logcat
- **Discord MCP** - Team communication, reading standup messages

### Build Tools
- **Unity's Android SDK** - Used because Unreal's SDK (r27c) wasn't configured
- **Gradle 8.13** - APK packaging (with configuration cache disabled)
- **ADB** - Device communication, APK sideloading

---

## Key Scripts Created During Jam

| Script | Purpose |
|--------|---------|
| `build_full_apk.bat` | Full cook + package pipeline |
| `update_zip.ps1` | Update submission zip with new APK |

---

## Lessons Learned

1. **AssetManagerSettings location matters** - Must be in DefaultGame.ini, not DefaultEngine.ini
2. **Gradle config cache breaks UE5.8** - Always disable it for Android builds
3. **NDK_VERSION gets reset** - Unreal overwrites gradle.properties on each cook
4. **ISDK poke != Enhanced Input** - Poke uses geometric detection, not input actions
5. **GenOrca has limits** - Object references, BreakStruct nodes, component events need manual wiring
6. **GitHub secret scanning** - Remove tokens before pushing, or use env vars

---

## Final Deliverables

- **Game:** Bulldogs Directors Cut
- **Package:** com.bulldog.directorscut
- **Levels:** 6 (MainMenu, TheFall, CliffPath, CanyonBridge, Highway, CarHop)
- **APK Size:** 293 MB
- **Submission Zip:** 268 MB
- **GitHub:** https://github.com/wendellj/Bulldog2026EpicAIMegaJam
- **Devlog:** https://github.com/wendellj/Bulldog2026EpicAIMegaJam/blob/master/Game/BulldogDevlog.html
- **Gameplay Video:** https://github.com/wendellj/Bulldog2026EpicAIMegaJam/blob/master/Game/BulldogGameplay.mp4
