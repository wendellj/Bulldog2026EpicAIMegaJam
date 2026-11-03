# VR Test Checklist - ColdStart MVP

Use this checklist before each build/deploy to catch issues early.

---

## Pre-Build Checks (Editor VR Preview)

Run these tests in **VR Preview** (⋮ next to Play → VR Preview) before building for Quest:

### Visual Checks
- [ ] **All controls visible** - CO2 button, guard cover, switch, breaker all render
- [ ] **Controls glowing properly** - Red, green, orange, cyan emissive materials working
- [ ] **Text displays readable** - FaultDisplay and SystemStatusDisplay visible
- [ ] **No black screen** - Level loads, camera positioned correctly at (0,0,100)
- [ ] **Proper darkness** - Ambient lighting dim (SkyLight 0.0125, PointLights 0.15-0.25)
- [ ] **No washed-out bloom** - Post-process not making everything white

### Performance Checks
- [ ] **No performance warnings** in editor console
- [ ] **Frame rate stable** - Should feel smooth (no hitches)
- [ ] **No shader compilation lag** - Wait for shaders to finish before testing

### Interaction Checks (VR Preview)
- [ ] **Hand tracking toggles** - Set controllers down, hands appear after 2-3 sec
- [ ] **Controllers work** - Can pick up controllers and they re-appear
- [ ] **Teleport/movement disabled** - Should be stationary room-scale only
- [ ] **Head tracking smooth** - No judder or stuttering

### Audio Checks (if implemented)
- [ ] **Button sounds play** on press
- [ ] **Switch sounds play** on toggle
- [ ] **Breaker sounds play** on reset
- [ ] **No audio clipping** or distortion

---

## Build Checklist

Before running `cook_android.bat`:

### Project Settings
- [ ] **Default map set** - DefaultEngine.ini has L_ColdStart as GameDefaultMap
- [ ] **Hand tracking enabled** - OculusXRHMDRuntimeSettings has HandTrackingSupport=ControllersAndHands
- [ ] **Package name correct** - Currently `com.YourCompany.BulldogMegaJam` (update for submission)
- [ ] **Android SDK configured** - ANDROID_HOME, NDKROOT, JAVA_HOME env vars set

### Content Validation
- [ ] **All assets saved** - No asterisks (*) in Content Browser
- [ ] **No temp actors** - Run `cleanup_level.py` to remove test actors
- [ ] **Lightmaps built** (if using static lighting) - Build → Build Lighting
- [ ] **No console errors** - Check Output Log for red errors

---

## Post-Build Checks (Quest Device)

After running `deploy_quest.bat`:

### Installation Verification
- [ ] **APK installed** - Check `adb shell pm list packages | grep Bulldog`
- [ ] **OBB pushed** - Check `/sdcard/Android/obb/com.YourCompany.BulldogMegaJam/`
- [ ] **App appears** in Quest Library under "Unknown Sources"

### Launch Testing
- [ ] **App launches** without crash
- [ ] **No black screen** - Level visible within 5 seconds
- [ ] **Guardian appears** - Quest boundary system active
- [ ] **Hand tracking works** - Set controllers down, hands appear

### Visual Quality (Quest)
- [ ] **Controls visible** - All 4 interactive elements render
- [ ] **Glows working** - Emissive materials display correctly
- [ ] **Text readable** - System status and fault displays clear
- [ ] **No graphical glitches** - No z-fighting, missing textures, etc.
- [ ] **Proper brightness** - Scene dark but controls visible

### Performance (Quest)
- [ ] **Frame rate stable** - 72fps (check with Performance Overlay if enabled)
- [ ] **No thermal throttling** - Test for 5+ minutes
- [ ] **Tracking smooth** - Hand/head tracking with no jitter
- [ ] **No loading stutters** - Asset streaming smooth

### Interaction Testing
- [ ] **CO2 button pressable** (if event graph wired)
- [ ] **Guard cover opens** (if event graph wired)
- [ ] **Switch toggles** (if event graph wired)
- [ ] **Breaker resets** (if event graph wired)
- [ ] **Hand collisions work** - Hands interact with controls

---

## Debug Tools

If issues occur, use these diagnostic tools:

### Logs
```bash
# View live logs
logcat_ue.bat

# Full logs
logcat_full.bat
```

### Screenshots
```bash
# Capture Quest screen
screenshot_quest.bat
```

### File Inspection
```bash
# Check OBB exists
adb shell ls /sdcard/Android/obb/com.YourCompany.BulldogMegaJam/

# Check pak files
adb shell ls /sdcard/Android/data/com.YourCompany.BulldogMegaJam/files/UnrealGame/BulldogMegaJam/BulldogMegaJam/Content/Paks/
```

### Content Updates
If content changes but APK didn't rebuild:
```bash
# Push just the updated paks (faster than full rebuild)
push_paks.bat
```

---

## Common Issues & Fixes

### Black Screen on Launch
- **Cause:** Default map not set
- **Fix:** Check DefaultEngine.ini has `GameDefaultMap=/Game/ColdStart/Levels/L_ColdStart`

### Controls Not Glowing
- **Cause:** Material parameters not saved
- **Fix:** Manually verify MI_Ctrl_* instances have Color set to HDR values (10.0+)

### Hand Tracking Not Working
- **Cause:** VR Pawn missing OculusXRHandComponent
- **Fix:** Use Meta XR Building Blocks VR Pawn, not DefaultPawn

### Content Not Loading
- **Cause:** Stale pak files in data directory
- **Fix:** Run `push_paks.bat` to update pak files directly

### Gradle Build Fails
- **Cause:** Configuration cache error
- **Fix:** Edit `gradle.properties`, add `org.gradle.configuration-cache=false`

### NDK Error During Build
- **Cause:** NDK_VERSION=NDK (invalid)
- **Fix:** Edit `gradle.properties`, set `NDK_VERSION=27.0.12077973`

---

## Regression Testing

Before major milestones (daily builds, submission), test ALL functionality:

### Phase 0 (Cold Open)
- [ ] Scene starts dark
- [ ] CO2 button visible and glowing red
- [ ] Pressing button advances to Phase 1

### Phase 1 (Emergency Power)
- [ ] Guard cover visible and glowing orange
- [ ] Opening cover reveals toggle switch
- [ ] Switch toggles on/off
- [ ] Flipping switch advances to Phase 2

### Phase 2 (Diagnosis)
- [ ] Breaker visible and glowing
- [ ] FaultDisplay shows fault tree
- [ ] Resetting breaker completes sequence

---

## Performance Targets (Quest 3)

- **Frame Rate:** 72fps minimum (never drop below 60fps)
- **Draw Calls:** < 200
- **Triangles:** < 1M visible
- **Real-time Lights:** Max 2 per area (we have 5 PointLights at low intensity)
- **GPU Frame Time:** < 11ms

---

## Pre-Submission Final Check

Before submitting to Epic AI MegaJam:

- [ ] **All phases playable** end-to-end
- [ ] **No crashes** in 10-minute playthrough
- [ ] **Hand tracking works** (critical for Quest experience)
- [ ] **Build runs standalone** (no PC tethering required)
- [ ] **Package name updated** from `com.YourCompany.BulldogMegaJam`
- [ ] **Credits screen** (if applicable)
- [ ] **Dev log complete** (DEVLOG.md filled out)
- [ ] **Git history clean** (no sensitive data, reasonable commits)
- [ ] **Screenshot/video captured** for submission thumbnail

---

**Last Updated:** 2026-11-03
**Version:** ColdStart MVP
