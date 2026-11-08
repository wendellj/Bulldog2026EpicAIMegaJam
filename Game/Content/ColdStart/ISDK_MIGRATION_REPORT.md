# VR Hand Tracking Fix: ISDK Migration Report

**Date:** 2026-11-08
**Project:** Bulldog MegaJam (ColdStart Level)
**Engine:** Unreal Engine 5.8
**Target Device:** Meta Quest 3
**Author:** Claude (AI Assistant) with Wendell Johnson

---

## Executive Summary

VR hand tracking was displaying hands "too far forward" relative to the user's actual hand positions. After extensive debugging and documentation research, the issue was resolved by migrating from raw `OculusXRHandComponent` to Meta's recommended **Interaction SDK (ISDK)** prebuilt hand rig components.

**Resolution:** Created new `BP_VRPawn_ISDK` blueprint using `IsdkHandRigComponentLeft` and `IsdkHandRigComponentRight`. Hands now track correctly.

---

## Problem Statement

### Symptoms
- Virtual hands appeared offset ("too far forward") when viewed through Quest 3 headset
- Quest's native system icons (hand menu pinned to palm) appeared at correct position
- Blueprint-rendered hand meshes did not align with native tracking

### Initial Hypothesis
The tracking data itself might be incorrect, or the camera/pawn setup was misconfigured.

---

## Debugging Timeline

### Phase 1: Debug Logging (Nov 7-8)

**What we tried:**
1. Added debug logging nodes to `BP_VRPawn_HandTracking` EventGraph
2. Logged positions of:
   - VRCamera (`GetWorldLocation`)
   - MotionController_Left/Right (`GetWorldLocation`)
   - OculusXRHand_Left/Right (`GetWorldLocation`)

**Findings:**
- Camera reported (0,0,0) - this is NORMAL (component position, not HMD position)
- MotionController positions showed real-world tracked values
- **OculusXRHandComponent reported SAME position as parent MotionController**

**Conclusion:** Tracking DATA was correct. Problem was in mesh RENDERING.

### Phase 2: Native Tracking Comparison (Nov 8)

**What we tried:**
Added `GetPointerPose` calls from `UOculusXRInputFunctionLibrary` to compare native Quest hand tracking positions with Blueprint component positions.

**Findings:**
- Native tracking positions matched MotionController positions
- Confirmed: the OculusXRHandComponent mesh has internal render offset (wrist at origin, hand extends forward)

### Phase 3: Documentation Research (Nov 8)

**What we tried:**
Queried Meta's official documentation via `vr_docs_search` and `vr_docs_get_page` MCP tools.

**Key discovery from Meta docs:**
> "The recommended way to integrate hand tracking for Unreal developers is to use the Interaction SDK, which provides standardized interactions and gestures."
> — [Hand Tracking Overview](https://developers.meta.com/vr/documentation/unreal/unreal-hand-tracking-overview)

### Phase 4: ISDK Migration (Nov 8)

**What we tried:**
1. Downloaded Meta XR Interaction SDK plugin (v207.0.0)
2. Installed to `UE_5.8/Engine/Plugins/Marketplace/MetaXRInteraction`
3. Attempted to modify existing `BP_VRPawn_HandTracking`:
   - Removed OculusXRHandComponent instances
   - Added IsdkHandRigComponent instances
   - Encountered hierarchy issues (components parented incorrectly)
   - EventGraph had orphaned nodes causing compile errors

4. Created fresh `BP_VRPawn_ISDK` blueprint:
   - Clean component hierarchy
   - Proper parent-child relationships
   - No legacy debug nodes

**Result:** Hands track correctly in VR Preview.

---

## What Worked vs. What Didn't

### What Worked

| Approach | Outcome |
|----------|---------|
| Debug logging to verify tracking data | Confirmed data was correct |
| Querying Meta docs via MCP tools | Found official recommendation for ISDK |
| Creating fresh blueprint instead of modifying old one | Clean hierarchy, no orphaned nodes |
| Using GenOrca/UnrealMCPython for blueprint manipulation | Successfully added/removed components programmatically |
| Setting Auto Possess Player = Player 0 on placed pawn | Player correctly possesses VR pawn |

### What Didn't Work

| Approach | Issue |
|----------|-------|
| Manually adding ISDK components in Blueprint Editor | Components ended up at wrong hierarchy level (duplicates, wrong parents) |
| Modifying existing BP_VRPawn_HandTracking | Old EventGraph nodes referenced deleted components, causing compile errors |
| Using `add_blueprint_node` for EventGraph wiring | Node JSON format required `type` field we didn't have documented |

---

## Resources Used

### Official Meta Documentation (ACCURATE)

| Document | URL | Status | Notes |
|----------|-----|--------|-------|
| Hand Tracking Overview | https://developers.meta.com/vr/documentation/unreal/unreal-hand-tracking-overview | **CURRENT** (2026-08-31) | Explicitly recommends ISDK |
| ISDK Overview | https://developers.meta.com/vr/documentation/unreal/unreal-isdk-overview | **CURRENT** (2026-08-31) | Plugin installation instructions |
| ISDK Getting Started | https://developers.meta.com/vr/documentation/unreal/unreal-isdk-getting-started | **CURRENT** (2026-04-15) | Component hierarchy, BeginPlay setup |
| Custom Hand Meshes | https://developers.meta.com/vr/documentation/unreal/unreal-isdk-custom-hand-controller-mesh | **CURRENT** (2026-04-15) | Hand mesh replacement guide |
| Setup Hand Tracking | https://developers.meta.com/vr/documentation/unreal/unreal-hand-tracking | **CURRENT** (2026-04-14) | Low-level OculusXRHandComponent API |
| VRC.Quest.Input.5 | https://developers.meta.com/vr/resources/vrc-quest-input-5 | **CURRENT** (2024-07-31) | Store requirement: RECOMMENDED (not required) |

### Plugin Download

| Resource | URL | Notes |
|----------|-----|-------|
| Meta XR Interaction SDK | https://developers.meta.com/horizon/downloads/package/meta-xr-interaction-sdk-unreal | v207.0.0, 3GB download |

### Documentation That Was Initially Misleading

| Claim | Reality |
|-------|---------|
| "ISDK required for store approval" | **INCORRECT** - VRC.Quest.Input.5 changed to RECOMMENDED (not required) on 2024-07-31 |
| "OculusXRHandComponent should work correctly when parented to MotionController" | **PARTIALLY TRUE** - Tracking works, but mesh has internal render offset that ISDK handles automatically |

---

## Final Solution

### New Blueprint: `BP_VRPawn_ISDK`

**Location:** `/Game/ColdStart/Blueprints/BP_VRPawn_ISDK`

**Component Hierarchy:**
```
DefaultSceneRoot
├── VRCamera (CameraComponent)
│   └── bLockToHmd = true
├── MotionController_Left (MotionControllerComponent)
│   └── MotionSource = Left
│   └── LeftHandRig (IsdkHandRigComponentLeft)
└── MotionController_Right (MotionControllerComponent)
    └── MotionSource = Right
    └── RightHandRig (IsdkHandRigComponentRight)
```

**Level Setup:**
- Placed `BP_VRPawn_ISDK` in `L_ColdStart` at (0, 0, 0)
- Set `Auto Possess Player = Player 0`
- Removed old `PlayerStart` actor

### What ISDK Provides

1. **Automatic mesh positioning** - handles wrist/palm offset internally
2. **Late update** - reduces tracking latency
3. **Standardized interactions** - poke, grab, ray (not used yet but available)
4. **Input mapping contexts** - `IMC_IsdkHand` for Enhanced Input integration

---

## Git History

| Commit | Description |
|--------|-------------|
| `87c8d07` | Pre-ISDK migration milestone - debug notes + migration plan |
| `12beda8` | feat: Fix VR hand tracking with Meta Interaction SDK (ISDK) |

---

## Recommendations for Team

1. **Use ISDK for new VR projects** - it's Meta's recommended approach and handles edge cases automatically

2. **Don't use raw OculusXRHandComponent** for hand visualization - the mesh has internal offsets that are difficult to compensate for

3. **Keep old blueprints for reference** - `BP_VRPawn_HandTracking` preserved for comparison

4. **BeginPlay setup is optional but recommended:**
   ```
   BeginPlay → IsHMDEnabled → Branch (True) → SetTrackingOrigin(LocalFloor)
   → GetPlayerController → GetEnhancedInputLocalPlayerSubsystem
   → AddMappingContext(IMC_IsdkHand, Priority=1)
   ```

5. **For poke/grab interactions** - ISDK provides `IsdkPokeInteractable`, `IsdkGrabbable` components (future work)

---

## Files Changed

| File | Change |
|------|--------|
| `BP_VRPawn_ISDK.uasset` | NEW - ISDK-based VR pawn |
| `BP_VRPawn_HandTracking.uasset` | MODIFIED - cleaned up orphaned components |
| `L_ColdStart.umap` | MODIFIED - uses new ISDK pawn |
| `ISDK_MIGRATION_PLAN.md` | MODIFIED - added adversarial review findings |

---

## Appendix: Plugin Installation

### Meta XR Interaction SDK Installation Steps

1. Download from: https://developers.meta.com/horizon/downloads/package/meta-xr-interaction-sdk-unreal
2. Extract `MetaXRInteraction` folder to:
   ```
   C:\Program Files\Epic Games\UE_5.8\Engine\Plugins\Marketplace\MetaXRInteraction
   ```
3. Restart Unreal Editor
4. Enable "Meta XR Interaction SDK" in Edit → Plugins
5. Restart Unreal Editor again

### Verification

In Plugins window, search "Meta Interaction" - should show:
- **Meta Interaction SDK** (Experimental) - enabled
- **Meta XR** - enabled

---

*Report generated 2026-11-08*
