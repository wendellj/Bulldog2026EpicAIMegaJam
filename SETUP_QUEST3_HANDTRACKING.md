# Quest 3 Hand Tracking VR Setup Guide
## Epic AI MegaJam 2026 - Roomscale 10'x10' Configuration

**Target**: Meta Quest 3 with hand tracking (no controllers)
**Play Space**: 10'x10' (3m x 3m) roomscale
**Engine**: Unreal Engine 5.8

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [PC Software Setup](#pc-software-setup)
3. [Unreal Project Configuration](#unreal-project-configuration)
4. [VR Pawn Blueprint Setup](#vr-pawn-blueprint-setup)
5. [Quest 3 Device Settings](#quest-3-device-settings)
6. [Testing & Verification](#testing--verification)
7. [Common Issues & Fixes](#common-issues--fixes)

---

## Prerequisites

### Required Software
- ✓ Unreal Engine 5.8 installed
- ✓ Meta Horizon Link app installed on PC
- ✓ Quest 3 headset with hand tracking enabled
- ✓ USB-C cable for Quest Link (or Air Link configured)

### Required Files (in this repo)
- `setup_vr_handtracking.py` - Automated blueprint creation script
- `verify_vr_setup.py` - Verification diagnostic script
- `fix_motion_source.py` - Motion source repair script

---

## PC Software Setup

### 1. Meta Horizon Link Configuration

**CRITICAL: These settings must be correct or hand tracking won't work!**

1. Open **Meta Horizon Link** app on your PC
2. Click **Settings** (gear icon)
3. **General tab**:
   - OpenXR Runtime: **"Meta Horizon Link"** ✓
4. **Developer tab**:
   - Developer Runtime Features: **ON** ✓

**Why this matters**: Without Developer Runtime Features enabled, hand skeleton data doesn't flow over the Link cable to Unreal. Your hands will appear but won't move.

### 2. Connect Quest 3 via Link

1. Connect Quest 3 to PC via USB-C cable
2. Put on headset
3. Allow USB debugging (if prompted)
4. Launch Quest Link from the headset
5. Verify "Connected" status in Meta Horizon Link app

---

## Unreal Project Configuration

### 1. Create New Project (if needed)

```
Project Type: Blank
Target Platform: Mobile / Tablet
Quality Preset: Scalable
Starter Content: No
Raytracing: Disabled
```

### 2. Enable Meta XR Plugin

**Method A: Marketplace Install (Recommended)**

1. Epic Games Launcher > Marketplace
2. Search "Meta XR"
3. Install "Meta XR All-in-One SDK" to engine
4. In Unreal: Edit > Plugins
5. Search "Meta XR"
6. Enable **"Meta XR"** plugin
7. Restart editor

**Method B: Manual Install**

If not in Marketplace:
1. Copy MetaXR plugin to: `[UE_Install]\Engine\Plugins\Marketplace\MetaXR\`
2. Edit > Plugins > Enable "Meta XR"
3. Restart editor

### 3. Project Settings - Critical Configuration

**Edit > Project Settings**, then configure:

#### **Platforms > Android**

```
Minimum SDK: 29
Target SDK: 32
Package for Meta Quest: Quest 3 ✓
```

#### **Platforms > Android > Oculus (or Meta XR)**

```
Hand Tracking Support: Controllers And Hands
Hand Tracking Frequency: High
```

**CRITICAL**: If you don't see these settings, the Meta XR plugin isn't installed correctly.

#### **Maps & Modes > Default Modes**

We'll set this per-level via WorldSettings instead (more flexible).

#### **Engine > Rendering**

```
Mobile HDR: Enabled ✓
Forward Shading: Enabled ✓
Mobile Multi-View: Enabled ✓
```

#### **Project > Description**

```
Settings > Start in VR: True ✓
```

### 4. Save Settings

File > Save All

---

## VR Pawn Blueprint Setup

### Option A: Automated Setup (Recommended)

**Use the provided Python script:**

```bash
cd [ProjectRoot]
python setup_vr_handtracking.py
```

This creates:
- `BP_VRPawn_HandTracking` blueprint at `/Game/Blueprints/`
- Camera component (eye level)
- Left & Right MotionControllers with OculusXRHand components
- Proper Motion Source settings (Left/Right)
- Proper Skeleton Type settings (HAND_LEFT/HAND_RIGHT)

**After script runs:**
1. Verify blueprint was created in Content Browser
2. Run verification: `python verify_vr_setup.py`

### Option B: Manual Blueprint Creation

If automation fails, create manually:

#### 1. Create Blueprint

1. Content Browser > Right-click > Blueprint Class
2. Parent Class: **Pawn**
3. Name: `BP_VRPawn_HandTracking`
4. Save to `/Game/Blueprints/`

#### 2. Add Components (Viewport tab)

**Component Hierarchy:**
```
DefaultSceneRoot
├─ VRCamera (CameraComponent)
├─ MotionController_Left (MotionControllerComponent)
│  └─ OculusXRHand_Left (OculusXRHandComponent)
├─ MotionController_Right (MotionControllerComponent)
   └─ OculusXRHand_Right (OculusXRHandComponent)
```

#### 3. Configure Components (Details panel)

**VRCamera**:
- Location: (0, 0, 0)
- No special settings needed

**MotionController_Left**:
- Motion Source: **Left** (NOT LeftGrip or LeftAim!)
- Location: (0, 0, 0)

**MotionController_Right**:
- Motion Source: **Right** (NOT RightGrip or RightAim!)
- Location: (0, 0, 0)

**OculusXRHand_Left**:
- Skeleton Type: **Hand Left**
- Mesh Type: **Hand Left**
- Visible: ✓ True
- Location: (0, 0, 0) relative to parent

**OculusXRHand_Right**:
- Skeleton Type: **Hand Right**
- Mesh Type: **Hand Right**
- Visible: ✓ True
- Location: (0, 0, 0) relative to parent

#### 4. Compile & Save

---

## Level Setup

### 1. Create VR Level

1. File > New Level > Empty Level
2. Save as: `L_VRTest` (or your game level name)

### 2. Add Basic Geometry (10'x10' space)

**For testing/reference:**

1. Add Floor:
   - Cube (300 x 300 x 10 cm)
   - Location: (0, 0, -5)

2. Add Walls (optional for debugging):
   - Cube (10 x 300 x 200 cm) at (-150, 0, 100)
   - Cube (10 x 300 x 200 cm) at (150, 0, 100)
   - Cube (300 x 10 x 200 cm) at (0, -150, 100)
   - Cube (300 x 10 x 200 cm) at (0, 150, 100)

3. Add **PlayerStart**:
   - Location: (0, 0, 0)
   - Center of your play space

4. Add Lighting:
   - SkyLight (Intensity: 2.0)
   - DirectionalLight (Intensity: 10.0)
   - **IMPORTANT**: Disable shadows on all lights (CastShadows = False) for performance

### 3. Set Default Pawn Class

**Option A: Via WorldSettings (Recommended for per-level control)**

1. Window > World Settings (or World Outliner > WorldSettings)
2. Game Mode section:
   - GameMode Override: None (leave default) OR create custom GameMode
   - Default Pawn Class: **BP_VRPawn_HandTracking**
3. Save level

**Option B: Via Script**

```bash
python set_default_pawn.py
```

**CRITICAL CHECK**: Make sure NO instance of `BP_VRPawn_HandTracking` is placed in the level manually. It should spawn automatically at PlayerStart.

If you see a pawn instance in World Outliner, delete it:

```bash
python -c "import sys; sys.path.insert(0, '.'); from unreal_helper import actor; print(actor('delete_by_label', actor_label='BP_VRPawn_HandTracking'))"
```

---

## Quest 3 Device Settings

### 1. Enable Hand Tracking

**On the Quest 3 headset:**

1. Go to **Settings** (gear icon)
2. **Movement Tracking**:
   - Hand Tracking: **ON** ✓
   - Auto Enable Hands or Controllers: **ON** ✓

### 2. Set Guardian for 10'x10' Space

1. Settings > Guardian
2. **Clear existing boundary** (if needed)
3. Draw new boundary:
   - **Stationary** mode OR **Roomscale** mode
   - Draw a 10'x10' (3m x 3m) boundary around your physical space
4. Confirm setup

**Why this matters**: Guardian drift can cause hand tracking spatial misalignment. Fresh boundary = accurate tracking.

### 3. Developer Mode (Optional but Recommended)

For faster iteration during jam:

1. Install Meta Quest Developer Hub (MQDH) on PC
2. Enable Developer Mode on Quest 3 via Meta account
3. Restart headset

---

## Testing & Verification

### 1. Run Verification Script

```bash
cd [ProjectRoot]
python verify_vr_setup.py
```

This checks:
- ✓ Blueprint exists
- ✓ Motion Source settings (Left/Right)
- ✓ Skeleton Type settings (HAND_LEFT/HAND_RIGHT)
- ✓ Component hierarchy
- ✓ Default Pawn Class assignment

### 2. VR Preview Test

1. In Unreal Editor: Click **▼** next to Play button
2. Select **"Play in VR"** (or **Alt+V**)
3. **Put on Quest 3 headset**
4. **Put down Touch controllers completely** (hand tracking ONLY works without controllers!)
5. Hold hands in front of headset

**Expected Results:**
- ✓ You're at floor level in the VR space
- ✓ Hands appear when you hold them in front
- ✓ **Hands MOVE when you move your real hands**
- ✓ Fingers track individual movements

### 3. Common Test Failures

| Symptom | Cause | Fix |
|---------|-------|-----|
| Hands appear but don't move | VR pawn not set as Default Pawn Class | Run `set_default_pawn.py` or check WorldSettings |
| Hands overlap / both in same position | Motion Source set to LeftGrip/RightGrip instead of Left/Right | Run `fix_motion_source.py` |
| Hands invisible | Controllers in your hands (turn off hand tracking) | Put controllers down, hands only |
| Hands jittery/laggy | Developer Runtime Features OFF in Meta Horizon Link | Enable in Meta Horizon Link > Settings > Developer |
| Black screen in headset | PlayerStart not in level, or lighting missing | Add PlayerStart at (0,0,0), add SkyLight |
| Hands too dim | Insufficient lighting | Increase SkyLight intensity to 2.0+ |

---

## Common Issues & Fixes

### Issue 1: "Hands appear but don't move"

**Root Cause**: Static pawn instance in level, not using Default Pawn Class

**Fix**:
```bash
# Delete static instance
python -c "import sys; sys.path.insert(0, '.'); from unreal_helper import actor; print(actor('delete_by_label', actor_label='BP_VRPawn_HandTracking'))"

# Set default pawn
python set_default_pawn.py

# Verify
python verify_vr_setup.py
```

### Issue 2: "Both hands in the same location"

**Root Cause**: Motion Source set to wrong values (LeftGrip/LeftAim instead of Left)

**Fix**:
```bash
python fix_motion_source.py
```

Should output:
```
MotionController_Left.MotionSource: Left [OK]
MotionController_Right.MotionSource: Right [OK]
```

### Issue 3: "Hand tracking data not flowing to Unreal"

**Root Cause**: Meta Horizon Link Developer Runtime Features disabled

**Fix**:
1. Open Meta Horizon Link on PC
2. Settings > Developer
3. Developer Runtime Features: **ON**
4. Reconnect Quest Link (unplug/replug cable)

### Issue 4: "Hands drift when I turn my head"

**Root Cause**: Guardian boundary drift / tracking space misalignment

**Fix**:
1. Reset Guardian on Quest 3 (Settings > Guardian > Clear & Redraw)
2. Reconnect Link
3. Add tracking origin reset to VR pawn BeginPlay:
   - Open BP_VRPawn_HandTracking Event Graph
   - BeginPlay → **Set Tracking Origin** node
   - Origin: **Floor Level**

### Issue 5: "Can't find Meta XR plugin settings"

**Root Cause**: Plugin not installed or not enabled

**Fix**:
1. Verify plugin exists: `[UE_Install]\Engine\Plugins\Marketplace\MetaXR\`
2. Edit > Plugins > Search "Meta" → Enable "Meta XR"
3. Restart editor
4. Edit > Project Settings > Search "Hand Tracking"

---

## Quick Setup Checklist (for Jam Day)

Use this checklist when setting up a new project during the jam:

### Pre-Flight (5 min)
- [ ] Meta Horizon Link installed on PC
- [ ] Developer Runtime Features: ON
- [ ] Quest 3 connected via Link cable
- [ ] Hand Tracking enabled on Quest 3 device
- [ ] Guardian boundary set (10'x10')

### Unreal Project (10 min)
- [ ] Meta XR plugin installed & enabled
- [ ] Project Settings > Android > Hand Tracking Support: "Controllers And Hands"
- [ ] BP_VRPawn_HandTracking blueprint created (run `setup_vr_handtracking.py`)
- [ ] Level created with PlayerStart at (0,0,0)
- [ ] WorldSettings > Default Pawn Class: BP_VRPawn_HandTracking
- [ ] NO static pawn instance in level (delete if present)

### Verification (5 min)
- [ ] Run `verify_vr_setup.py` → all checks pass
- [ ] VR Preview (Alt+V) → hands appear
- [ ] Put down controllers → hands move with real hands
- [ ] Fingers track individually

**Total Setup Time: ~20 minutes**

---

## Automated Scripts Reference

All scripts assume you're in the project root directory and have `unreal_helper.py` available.

### `setup_vr_handtracking.py`
Creates BP_VRPawn_HandTracking blueprint with all components configured.

**Usage**:
```bash
python setup_vr_handtracking.py
```

### `verify_vr_setup.py`
Runs diagnostic checks on VR pawn configuration.

**Usage**:
```bash
python verify_vr_setup.py
```

**Expected output**:
```
[OK] Motion Source: Left/Right
[OK] Skeleton Type: HAND_LEFT/HAND_RIGHT
[OK] Default Pawn Class set
```

### `fix_motion_source.py`
Repairs Motion Source settings if hands overlap.

**Usage**:
```bash
python fix_motion_source.py
```

### `set_default_pawn.py`
Sets BP_VRPawn_HandTracking as Default Pawn Class.

**Usage**:
```bash
python set_default_pawn.py
```

---

## Advanced: Adding Interactivity (Post-Setup)

Once basic hand tracking works, add interactions:

### 1. Hand Collision (for grabbing)

Add SphereComponents to fingertips:

```python
# Add to each OculusXRHand component in blueprint
- LeftIndexTip (SphereComponent, radius 1.5cm, attached to index finger bone)
- RightIndexTip (SphereComponent, radius 1.5cm, attached to index finger bone)
```

### 2. Pinch Detection

Use OculusXR hand tracking API:

```cpp
// Blueprint callable
bool IsPinching = OculusXRHandComponent->GetFingerIsPinching(EOculusXRHandFinger::Index);
```

### 3. Grabbable Objects

Create BP_Grabbable actor blueprint:
- StaticMesh component
- Box/Sphere collision
- Event: OnComponentBeginOverlap (fingertip sphere)
- Check: IsPinching → Attach to hand

---

## Troubleshooting During Jam

### Quick Diagnostic Command

If something breaks mid-jam:

```bash
python verify_vr_setup.py > diagnostic.txt
```

Share `diagnostic.txt` with team for debugging.

### Emergency Reset

If VR is completely broken:

1. Delete `Saved/` and `Intermediate/` folders
2. Restart Unreal Editor
3. Re-run `setup_vr_handtracking.py`
4. Re-run `set_default_pawn.py`

### Performance Issues on Quest 3

If framerate drops below 72fps:

1. Disable shadows on ALL lights (CastShadows = False)
2. Reduce draw calls (combine meshes)
3. Lower texture resolution (max 1024x1024 for mobile)
4. Profile using: `stat fps` in VR Preview console

---

## Support & Resources

### Documentation
- Meta XR Docs: https://developers.meta.com/horizon/documentation/unreal/
- Hand Tracking Guide: https://developers.meta.com/horizon/documentation/unreal/unreal-hand-tracking/

### During Jam
- Keep this guide open in browser/editor
- Bookmark: Meta XR Troubleshooting page
- Have `verify_vr_setup.py` ready to run

---

## Credits & Lessons Learned

**Key Insights from Bulldog MegaJam Prep (Nov 2026)**:

1. **Motion Source is critical**: Must be `Left`/`Right`, not `LeftGrip`/`LeftAim`
2. **Default Pawn Class matters**: Static pawn in level won't receive tracking data
3. **Developer Runtime Features**: Required for hand tracking over Link
4. **Guardian reset**: Fixes spatial drift issues
5. **Controllers OFF**: Hand tracking only works when controllers are put down

**Setup validated on**:
- Unreal Engine 5.8
- Meta Quest 3
- Meta XR All-in-One SDK (latest)
- Windows 11 PC with Meta Horizon Link

---

**Last Updated**: November 5, 2026
**Prepared for**: Epic AI MegaJam 2026 (Nov 11-15)
**Team**: Bulldog (Project: ColdStart MVP)
