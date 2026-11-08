# ISDK Migration Plan for BP_VRPawn_HandTracking

**Date:** 2026-11-08
**Author:** Claude (AI Assistant)
**Blueprint:** `/Game/ColdStart/Blueprints/BP_VRPawn_HandTracking`

## Problem Statement

Hands appear "too far forward" when viewed in VR. Debug logging confirmed:
- MotionController positions are correct (tracking data is accurate)
- OculusXRHandComponent reports same position as parent MotionController
- But the rendered hand mesh appears offset from where it should be
- Quest native system icons (hand menu) appear at correct palm position

**Root cause:** Using raw `OculusXRHandComponent` instead of Meta's recommended Interaction SDK (ISDK) components.

---

## Source Documentation

### Source 1: Hand Tracking Overview
**URL:** https://developers.meta.com/vr/documentation/unreal/unreal-hand-tracking-overview
**Last Updated:** 2026-08-31

> "The recommended way to integrate hand tracking for Unreal developers is to use the Interaction SDK, which provides standardized interactions and gestures. Building custom interactions without the SDK can be a significant challenge and makes it difficult to get approved in the store."

### Source 2: Interaction SDK Overview
**URL:** https://developers.meta.com/vr/documentation/unreal/unreal-isdk-overview
**Last Updated:** 2026-08-31

> "The Meta XR Interaction SDK for Unreal Engine lets VR users immersively interact with their virtual environment. With Interaction SDK, you can grab and scale objects, push buttons, navigate user interfaces, and more while using controllers or your physical hands."

**Supported devices:** Meta Quest 2, Quest 3, Quest 3S, Quest Pro, Meta VR Glasses
**Supported UE versions:** Unreal Engine 5.4 and later

### Source 3: Getting Started with ISDK
**URL:** https://developers.meta.com/vr/documentation/unreal/unreal-isdk-getting-started
**Last Updated:** 2026-04-15

Defines the correct component hierarchy:

```
RootComponent (SceneComponent)
├── VRCamera (CameraComponent)
├── LeftMotionController (MotionControllerComponent, Motion Source = Left)
│   ├── IsdkHandRigComponentLeft
│   └── IsdkControllerRigComponentLeft (optional)
└── RightMotionController (MotionControllerComponent, Motion Source = Right)
    ├── IsdkHandRigComponentRight
    └── IsdkControllerRigComponentRight (optional)
```

### Source 4: VRC.Quest.Input.5
**URL:** https://developers.meta.com/vr/resources/vrc-quest-input-5
**Last Updated:** 2024-07-31

> "For apps that support hand tracking, hands should render in the correct position and orientation, and should animate properly."

**Status:** Recommended (not required) for Meta Horizon Store as of 2024-07-31.

---

## Prerequisites

### Required Plugins

1. **Meta XR Plugin** (MetaXR)
   - Already installed at: `C:\Program Files\Epic Games\UE_5.8\Engine\Plugins\Marketplace\MetaXR`
   - Status: ✅ Enabled in project

2. **Meta XR Interaction SDK Plugin** (MetaXRInteraction / OculusInteraction)
   - **Must be installed separately** from Meta VR Developer Hub
   - Download URL: https://developers.meta.com/horizon/downloads/package/meta-xr-interaction-sdk-unreal
   - Install location: `[UnrealDir]\Engine\Plugins\Marketplace\MetaXRInteraction`

### Verification Steps

Before proceeding, verify ISDK plugin is installed:
1. Open Unreal Editor
2. Go to Edit > Plugins
3. Search for "Meta XR Interaction"
4. If not found, download and install from Meta Developer Hub

---

## Migration Steps

### Phase 1: Verify Plugin Installation

**Action:** Check if Meta XR Interaction SDK plugin is installed and enabled.

```
Edit > Plugins > Search "Meta XR Interaction SDK"
```

If not installed (from unreal-isdk-overview, 2026-08-31):
1. Download from https://developers.meta.com/horizon/downloads/package/meta-xr-interaction-sdk-unreal
2. In `C:\Program Files\Epic Games\UE_5.8\Engine\Plugins\`, create `Marketplace` directory if it doesn't exist
3. Extract the `MetaXRInteraction` folder from the zip into the Marketplace directory
   Final path: `C:\Program Files\Epic Games\UE_5.8\Engine\Plugins\Marketplace\MetaXRInteraction`
4. Run Unreal Editor
5. Go to Edit > Plugins, search for "Meta" (not "Meta XR" - may not show all results)
6. Enable both "Meta XR" plugin (if present) AND "Meta XR Interaction SDK" plugin
7. Restart Unreal Editor for changes to take effect

### Phase 2: Modify BP_VRPawn_HandTracking

**Current hierarchy (WRONG):**
```
DefaultSceneRoot
├── VRCamera (CameraComponent)
├── MotionController_Left (MotionControllerComponent)
│   ├── OculusXRHand_Left (OculusXRHandComponent) ← REMOVE
│   └── LeftFingertip (SphereComponent) ← REMOVE
└── MotionController_Right (MotionControllerComponent)
    ├── OculusXRHand_Right (OculusXRHandComponent) ← REMOVE
    └── RightFingertip (SphereComponent) ← REMOVE
```

**Target hierarchy (CORRECT per Meta docs - unreal-isdk-getting-started, 2026-04-15):**
```
DefaultSceneRoot
├── VRCamera (CameraComponent)
├── LeftMotionController (MotionControllerComponent, Motion Source = Left)
│   ├── LeftHandInteractors (IsdkHandRigComponentLeft - "Isdk Hand Rig (L)")
│   └── LeftControllerInteractors (IsdkControllerRigComponentLeft) [OPTIONAL]
└── RightMotionController (MotionControllerComponent, Motion Source = Right)
    ├── RightHandInteractors (IsdkHandRigComponentRight - "Isdk Hand Rig (R)")
    └── RightControllerInteractors (IsdkControllerRigComponentRight) [OPTIONAL]
```

**Note:** Controller rig components are optional. Since we're using hand tracking only, we only need the IsdkHandRigComponent on each side.

**Steps:**

1. Open BP_VRPawn_HandTracking in Blueprint Editor
2. Delete components:
   - OculusXRHand_Left
   - OculusXRHand_Right
   - LeftFingertip
   - RightFingertip
3. Add under MotionController_Left:
   - `Isdk Hand Rig (L)` component
4. Add under MotionController_Right:
   - `Isdk Hand Rig (R)` component
5. Verify MotionController_Left has Motion Source = "Left"
6. Verify MotionController_Right has Motion Source = "Right"
7. Compile and Save

### Phase 3: Set Tracking Origin in BeginPlay

**Source:** unreal-isdk-getting-started (2026-04-15)

Add to EventGraph BeginPlay:

```
BeginPlay
    ↓
Is Head Mounted Display Enabled (from HeadMountedDisplay library)
    ↓ (Branch on True)
Set Tracking Origin (Origin = Local Floor)
    ↓
[Continue to Input Mapping Contexts]
```

**Blueprint node sequence:**
1. Right-click next to BeginPlay event → Add "Is Head Mounted Display Enabled"
2. Drag off Return value → Add "Branch" node
3. Connect BeginPlay exec → Branch input
4. Drag off True exec pin → Add "Set Tracking Origin"
5. Set Origin pin value to "Local Floor"

### Phase 4: Add Input Mapping Contexts

**Source:** unreal-isdk-getting-started (2026-04-15)

> "Interaction SDK uses Unreal's Enhanced Input system to connect input events (such as pinch, or button press) to Unreal Input Actions."

Required Input Mapping Contexts:
- `IMC_IsdkHand` (for hand tracking input)
- `IMC_IsdkControllerAnimation` (optional, for controller support)

**Location:** `Plugins/OculusInteraction/Inputs/`

**Note:** To see these assets, enable "Show plugin content" and "Show engine content" from the gear icon in the Content Browser.

Add to BeginPlay after Set Tracking Origin:

```
Set Tracking Origin
    ↓
Get Player Controller
    ↓
Get EnhancedInputLocalPlayerSubsystem
    ↓
Add Mapping Context (IMC_IsdkHand, Priority = 1)
    ↓
Add Mapping Context (IMC_IsdkControllerAnimation, Priority = 1)
```

**Blueprint node sequence:**
1. Right-click after Set Tracking Origin → Add "Get Player Controller"
2. Drag off output pin → Add "Get EnhancedInputLocalPlayerSubsystem"
3. Drag off subsystem → Add "Add Mapping Context"
4. Set Mapping Context to "IMC_IsdkHand", Priority = 1
5. Connect Set Tracking Origin exec → Add Mapping Context input
6. Duplicate the Add Mapping Context node (Ctrl+D)
7. Set second node's Mapping Context to "IMC_IsdkControllerAnimation", Priority = 1
8. Connect first Add Mapping Context exec → second Add Mapping Context input

**Default input mappings (from docs):**
| Source | Interaction | Input |
|--------|-------------|-------|
| Hand | Poke | Extend index finger |
| Hand | Ray Select | Pinch Index + Thumb |
| Controller | Poke | Poke with tip of controller |
| Controller | Ray Select | Press and hold Trigger |

### Phase 5: Clean Up Debug Nodes (Optional)

The existing debug logging nodes can be removed or kept for verification:
- Camera position logging
- MotionController position logging
- Native tracking comparison nodes

### Phase 6: Test

1. Compile Blueprint
2. Save Blueprint
3. Run VR Preview
4. Verify:
   - Hands appear at correct position (matching Quest system icons)
   - Fingers track correctly
   - Hand mesh animates properly

---

## Rollback Plan

If ISDK causes issues, revert to previous setup:
1. Delete IsdkHandRigComponent components
2. Re-add OculusXRHandComponent under each MotionController
3. Set SkeletonType to HandLeft/HandRight respectively

---

## References

| Document | URL | Last Updated |
|----------|-----|--------------|
| Hand Tracking Overview | https://developers.meta.com/vr/documentation/unreal/unreal-hand-tracking-overview | 2026-08-31 |
| ISDK Overview | https://developers.meta.com/vr/documentation/unreal/unreal-isdk-overview | 2026-08-31 |
| ISDK Getting Started | https://developers.meta.com/vr/documentation/unreal/unreal-isdk-getting-started | 2026-04-15 |
| Custom Hand Meshes | https://developers.meta.com/vr/documentation/unreal/unreal-isdk-custom-hand-controller-mesh | 2026-04-15 |
| VRC.Quest.Input.5 | https://developers.meta.com/vr/resources/vrc-quest-input-5 | 2024-07-31 |
| ISDK Download | https://developers.meta.com/horizon/downloads/package/meta-xr-interaction-sdk-unreal | - |

---

## Notes

- ISDK is a **separate plugin** from MetaXR - must be downloaded and installed independently
- ISDK requires UE 5.4+ (we have UE 5.8, so compatible)
- Controller support is optional - we only need hand tracking for this project
- The `IsdkHandRigComponent` components handle mesh positioning, tracking, and late-update automatically
