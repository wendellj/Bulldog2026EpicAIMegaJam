# VR Hand Tracking Debug Notes

**Date:** 2026-11-07/08
**Blueprint:** `/Game/ColdStart/Blueprints/BP_VRPawn_HandTracking`

## Original Problem

User reported "hands appear too far forward" when viewing through the Quest headset.

## Component Hierarchy (Verified Correct)

```
DefaultSceneRoot
├── VRCamera (CameraComponent, Lock to HMD enabled)
├── MotionController_Left (MotionControllerComponent)
│   ├── OculusXRHand_Left (OculusXRHandComponent)
│   └── LeftFingertip (SphereComponent)
└── MotionController_Right (MotionControllerComponent)
    ├── OculusXRHand_Right (OculusXRHandComponent)
    └── RightFingertip (SphereComponent)
```

## Debug Logging Added

Added Tick event debug logging with prefixes to identify each component:
- `Camera:` - VRCamera GetWorldLocation
- `LeftMC:` - MotionController_Left GetWorldLocation
- `RightMC:` - MotionController_Right GetWorldLocation
- `LeftHand:` - OculusXRHand_Left GetWorldLocation
- `RightHand:` - OculusXRHand_Right GetWorldLocation

### Debug Output (from VR Preview)

```
Camera:    X=0.000  Y=0.000  Z=0.000
LeftMC:    X=-33.3  Y=-4.6   Z=105.5
RightMC:   X=-33.0  Y=33.1   Z=121.7
LeftHand:  X=-33.3  Y=-4.6   Z=105.5
RightHand: X=-33.0  Y=33.1   Z=121.7
```

## Key Discovery: Camera (0,0,0) is NORMAL

**This is NOT a bug.** In Unreal VR:
- `CameraComponent->GetWorldLocation()` returns the component's scene position (where it's placed in the Blueprint)
- The rendered VIEW follows the HMD via "Lock to HMD" setting
- But transform queries (GetWorldLocation) do NOT reflect HMD tracking
- To get actual HMD position, must use `UHeadMountedDisplayFunctionLibrary::GetOrientationAndPosition()`

The MotionControllers ARE tracking correctly - they show real-world tracked positions.

## What We Checked

1. **Lock to HMD** - Already enabled on VRCamera (user confirmed)
2. **Use Pawn Control Rotation** - Already enabled (user confirmed)
3. **Tracking Origin** - Set to STAGE (queried via HeadMountedDisplayFunctionLibrary)
4. **Component collision** - Previous session disabled collision on MotionControllers (fix_hand_offset.py)
5. **Debug logging** - Added prefixed output to distinguish components

## What We Ruled Out

- Camera not tracking: This is expected UE behavior, not a bug
- MotionControllers not tracking: They ARE tracking (showing real positions)
- Wrong component hierarchy: Hierarchy is correct
- Missing Lock to HMD: Already enabled

## Positions Analysis

The tracked positions look reasonable:
- Z = 105-121 cm = waist to chest height (standing)
- Y separation of ~37 cm = normal distance between hands
- X = -33 cm = hands positioned forward of body (normal)

## Still To Investigate

1. **Visual verification needed** - Does the hand mesh VISUALLY appear offset when looking through the headset? The tracking data looks correct.

2. **OculusXRHand mesh offset** - The OculusXRHandComponent might have a render offset that doesn't match tracking position. Check:
   - `SkeletonType` property (should be HandLeft/HandRight)
   - Any transform offsets on the component
   - Mesh attachment point settings

3. **Tracking Origin** - Currently STAGE. Could try:
   - Floor level tracking origin
   - Eye level tracking origin

4. **Physical calibration** - Quest hand tracking calibration might be off

5. **Add actual HMD position to debug** - Add a node using `GetOrientationAndPosition` from HeadMountedDisplayFunctionLibrary to compare actual HMD position vs component position

## Files Modified

- `BP_VRPawn_HandTracking.uasset` - Added debug logging nodes with prefixes
- EventGraph now has 28 nodes for debug output

## How to Read Debug Logs

1. Run VR Preview in editor
2. Check `C:\Bulldog\Game\Saved\Logs\BulldogMegaJam_2.log` (or BulldogMegaJam.log)
3. Search for "Camera:", "LeftMC:", etc.

PowerShell command:
```powershell
Get-Content 'C:\Bulldog\Game\Saved\Logs\BulldogMegaJam_2.log' | Select-String -Pattern 'Camera:|LeftMC:' | Select-Object -Last 20
```

## Previous Fix Attempt (fix_hand_offset.py)

Script at `C:\Bulldog\Game\fix_hand_offset.py` attempted to disable collision on MotionController components to prevent camera push. This was based on Meta XR docs noting that MotionControllerComponents with collision can push the camera if bounds overlap camera origin.

## Session Update (2026-11-08)

### Offset Watchdog Implemented

Added a watchdog to the EventGraph that runs on every tick:
1. Gets pawn's actor location
2. Calculates vector length (distance from origin)
3. If distance > 0.1, logs "OFFSET RESET: Pawn was at [position]" and resets to (0,0,0)
4. Connected to Tick event execution flow

Nodes added:
- K2Node_CallFunction_3: GetActorLocation
- K2Node_CallFunction_1: VectorLength (VSize)
- K2Node_CallFunction_2: Greater_DoubleDouble (threshold 0.1)
- K2Node_IfThenElse_0: Branch
- K2Node_CallFunction_7: Append (prefix "OFFSET RESET: Pawn was at ")
- K2Node_CallFunction_6: Conv_VectorToString
- K2Node_CallFunction_0: PrintString (for logging)
- K2Node_CallFunction_4: SetActorLocation
- K2Node_CallFunction_5: MakeVector (0,0,0)

### Watchdog Test Results

- No "OFFSET RESET" messages in logs = pawn is staying at origin (correct)
- Camera now reports (0,0,0) as expected
- Hand positions show real tracked values

### CRITICAL DISCOVERY: Quest Native vs Blueprint Hand Tracking

**User observation:** "The virtual hands did not match my hand position, however the menu icons that the headset replaced in the virtual scene were displayed where my palms were relative to the headset."

**What this means:**
- Quest's NATIVE hand tracking (system menu icons) works correctly
- The Blueprint's OculusXRHandComponent meshes do NOT track correctly
- The tracking DATA is correct (MotionControllers show real positions)
- The problem is in how OculusXRHandComponent RENDERS the hand mesh

### Root Cause Hypothesis

The OculusXRHandComponent might have:
1. **Incorrect attachment** - hands attached to MotionControllers which track controllers, not hands
2. **Wrong tracking source** - OculusXRHandComponent needs direct hand tracking, not controller tracking
3. **Render offset** - mesh rendering offset from component position

### SOLUTION: Use Interaction SDK (ISDK) Hand Rigs

**Root cause identified:** We're using raw `OculusXRHandComponent` instead of Meta's recommended **Interaction SDK** prebuilt hand rig components.

**From Meta documentation:**
> "The recommended way to integrate hand tracking for Unreal developers is to use the Interaction SDK, which provides standardized interactions and gestures."

**Current (WRONG) hierarchy:**
```
DefaultSceneRoot
├── VRCamera
├── MotionController_Left
│   └── OculusXRHand_Left (OculusXRHandComponent) ← RAW COMPONENT
└── MotionController_Right
    └── OculusXRHand_Right (OculusXRHandComponent) ← RAW COMPONENT
```

**Recommended (CORRECT) hierarchy:**
```
DefaultSceneRoot
├── VRCamera (CameraComponent)
├── LeftMotionController (MotionControllerComponent, Motion Source = Left)
│   ├── IsdkHandRigComponentLeft (ISDK prebuilt)
│   └── IsdkControllerRigComponentLeft (optional, for controller support)
└── RightMotionController (MotionControllerComponent, Motion Source = Right)
    ├── IsdkHandRigComponentRight (ISDK prebuilt)
    └── IsdkControllerRigComponentRight (optional, for controller support)
```

**Why ISDK is better:**
1. Handles tracking pose and late-update automatically
2. Provides standardized poke/grab/ray interactions
3. Properly routes hand tracking through the Enhanced Input system
4. Quest store approval requires ISDK for hand interactions

**Action items:**
1. Delete OculusXRHand_Left and OculusXRHand_Right components
2. Add IsdkHandRigComponentLeft under MotionController_Left
3. Add IsdkHandRigComponentRight under MotionController_Right
4. Ensure Motion Source is set correctly on each MotionController
5. Set Tracking Origin to "Local Floor" in BeginPlay
6. Add ISDK Input Mapping Contexts (IMC_IsdkHand)

### HMD Position Logging (Partially Added)

Started adding nodes to log actual HMD position (incomplete):
- K2Node_CallFunction_8: GetOrientationAndPosition
- K2Node_CallFunction_9: Conv_VectorToString
- K2Node_CallFunction_10: Concat_StrStr (Append)
- K2Node_CallFunction_11: PrintString

**Status:** Nodes added but NOT yet wired together or connected to execution flow.

## Session Update (2026-11-08, continued)

### Native Hand Tracking Comparison Added

Added nodes to query Quest's **native hand tracking** positions via `UOculusXRInputFunctionLibrary::GetPointerPose()` and compare them to where Blueprint renders the hands.

**Why this approach:**
- User observed: Quest system menu icons appear at correct palm positions
- User observed: Blueprint OculusXRHandComponent meshes appear offset (too far forward)
- This means native tracking DATA is correct, but Blueprint RENDERING is offset
- GetPointerPose returns the native tracking position, bypassing Blueprint component hierarchy

**Nodes added for native tracking comparison:**

LEFT hand chain:
- K2Node_CallFunction_37: GetPointerPose (DeviceHand=HandLeft)
- K2Node_CallFunction_14: BreakTransform
- K2Node_CallFunction_26: Conv_VectorToString
- K2Node_CallFunction_39: Append (prefix="NativeLeft: ")
- K2Node_CallFunction_30: PrintString

RIGHT hand chain:
- K2Node_CallFunction_38: GetPointerPose (DeviceHand=HandRight)
- K2Node_CallFunction_15: BreakTransform
- K2Node_CallFunction_27: Conv_VectorToString
- K2Node_CallFunction_40: Append (prefix="NativeRight: ")
- K2Node_CallFunction_36: PrintString

**Execution flow:** Connected after existing debug chain (_35.then → _30 → _36)

**Expected debug output:**
```
LeftMC:      X=-33.3  Y=-4.6   Z=105.5    <- MotionController position
NativeLeft:  X=???    Y=???    Z=???      <- Native GetPointerPose position
RightMC:     X=-33.0  Y=33.1   Z=121.7
NativeRight: X=???    Y=???    Z=???
```

**What to look for:**
- If NativeLeft/NativeRight positions MATCH LeftMC/RightMC positions → problem is in OculusXRHandComponent rendering
- If NativeLeft/NativeRight positions DIFFER from LeftMC/RightMC → MotionControllers are tracking controllers, not hands

### How to Test

1. Save the blueprint (Ctrl+S in editor)
2. Run VR Preview
3. Check logs for "NativeLeft:" and "NativeRight:" entries
4. Compare native positions to LeftMC/RightMC positions

PowerShell command:
```powershell
Get-Content 'C:\Bulldog\Game\Saved\Logs\BulldogMegaJam_2.log' | Select-String -Pattern 'NativeLeft:|NativeRight:|LeftMC:|RightMC:' | Select-Object -Last 20
```

## Next Steps

1. **Run VR Preview** and collect native vs MotionController position logs
2. **Analyze the offset** between native tracking and Blueprint component positions
3. If offset exists: Calculate the correction vector and apply to OculusXRHandComponent transform
4. If no offset: Problem is in OculusXRHandComponent mesh attachment/rendering
