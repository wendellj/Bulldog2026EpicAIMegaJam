# Hand Tracking Bug Report: Invisible Hands and Position Offset

**Project:** BulldogMegaJam
**Engine:** Unreal Engine 5.8
**Target Device:** Meta Quest 3
**Date:** 2026-11-05
**Reporter:** [Your Name]

---

## Executive Summary

Hand tracking is non-functional in this project. Hands are completely invisible at runtime, and prior to becoming invisible, hands were rendering approximately 12-18 inches (30-45 cm) to the LEFT of actual hand positions. This report documents all current configuration settings and compares them against Meta's documented best practices.

---

## Symptoms

### Current Issue: Invisible Hands
- Hands do not render at all during VR preview or device deployment
- No hand mesh is visible regardless of tracking confidence
- Issue persists whether hands are in or out of camera view

### Previous Issue: Position Offset (12-18" to the left)
- Before hands became invisible, they rendered consistently offset to the LEFT
- Offset was approximately 12-18 inches (30-45 cm) from actual hand position
- Both hands exhibited the same leftward offset
- Offset was consistent regardless of hand position in space

---

## Environment

| Component | Version/Value |
|-----------|---------------|
| Unreal Engine | 5.8 |
| Meta XR Plugin | Marketplace version (OculusXR) |
| MetaXR Plugin | Enabled |
| OpenXR Plugin | Enabled |
| OpenXRHandTracking Plugin | Enabled |
| Target Device | Meta Quest 3 |
| Hand Tracking Mode | Hands Only |
| Development OS | Windows 11 |

---

## Current Configuration (Extracted via GenOrca/UnrealMCPython)

### Project Settings (DefaultEngine.ini)

```ini
[/Script/OculusXRHMD.OculusXRHMDRuntimeSettings]
HandTrackingSupport=HandsOnly
HandTrackingFrequency=HIGH
HandTrackingVersion=V2
bInsightPassthroughEnabled=True
SystemSplashBackground=Contextual
```

### Enabled Plugins (BulldogMegaJam.uproject)

```json
{
  "Plugins": [
    { "Name": "OpenXR", "Enabled": true },
    { "Name": "OpenXREyeTracker", "Enabled": true },
    { "Name": "OpenXRHandTracking", "Enabled": true },
    { "Name": "MetaXR", "Enabled": true, "Optional": true },
    { "Name": "OculusXR", "Enabled": true }
  ]
}
```

### VR Pawn Component Hierarchy (BP_VRPawn_HandTracking)

```
DefaultSceneRoot (SceneComponent)
├── VRCamera (CameraComponent)
│   └── lock_to_hmd: True
│   └── relative_location: [0, 0, 0]
├── MotionController_Left (MotionControllerComponent)
│   ├── motion_source: "LeftHand"
│   ├── player_index: 0
│   ├── disable_low_latency_update: False
│   ├── current_tracking_status: NOT_TRACKED
│   └── OculusXRHand_Left (OculusXRHandComponent)
│       ├── skeleton_type: HAND_LEFT
│       ├── mesh_type: HAND_LEFT
│       ├── confidence_behavior: HIDE_ACTOR
│       ├── system_gesture_material: None
│       ├── material_override: None
│       ├── hidden_in_game: False
│       ├── update_hand_scale: True
│       ├── initialize_physics: False
│       └── skeletal_mesh: None  ← CRITICAL ISSUE
├── MotionController_Right (MotionControllerComponent)
│   ├── motion_source: "RightHand"
│   ├── player_index: 0
│   ├── disable_low_latency_update: False
│   ├── current_tracking_status: NOT_TRACKED
│   └── OculusXRHand_Right (OculusXRHandComponent)
│       ├── skeleton_type: HAND_RIGHT
│       ├── mesh_type: HAND_RIGHT
│       ├── confidence_behavior: HIDE_ACTOR
│       ├── system_gesture_material: None
│       ├── material_override: None
│       ├── hidden_in_game: False
│       ├── update_hand_scale: True
│       ├── initialize_physics: False
│       └── skeletal_mesh: None  ← CRITICAL ISSUE
```

---

## Comparison Against Meta Documentation

### 1. Plugin Configuration

| Setting | Current Value | Meta Best Practice | Status | Source |
|---------|---------------|-------------------|--------|--------|
| MetaXR Plugin | Enabled | Required | ✓ | [Meta XR Plugin Setup](https://developers.meta.com/vr/documentation/unreal/unreal-setting-up-metaxr-plugin) |
| OculusXR Plugin | Enabled | Should NOT coexist with MetaXR | ⚠️ CONFLICT | See note below |
| OpenXR Plugin | Enabled | Required for OpenXR backend | ✓ | [Choosing OpenXR Backend](https://developers.meta.com/vr/documentation/unreal/unreal-openxr) |
| OpenXRHandTracking | Enabled | Required for OpenXR hand tracking | ✓ | [Choosing OpenXR Backend](https://developers.meta.com/vr/documentation/unreal/unreal-openxr) |

**Note on Plugin Conflict:** The project has BOTH `OculusXR` (Marketplace plugin) AND `MetaXR` enabled. These are separate plugins that may have overlapping functionality. Meta documentation states to enable "Meta XR" and explicitly warns: "If the Oculus VR plugin is displayed, do not enable it when using Unreal 5.x because it is deprecated."

### 2. Hand Tracking Project Settings

| Setting | Current Value | Meta Best Practice | Status | Source |
|---------|---------------|-------------------|--------|--------|
| HandTrackingSupport | HandsOnly | Controllers, ControllersAndHands, or HandsOnly | ✓ | [Setup Hand Tracking](https://developers.meta.com/vr/documentation/unreal/unreal-hand-tracking) |
| HandTrackingFrequency | HIGH | HIGH recommended for accuracy | ✓ | [Setup Hand Tracking](https://developers.meta.com/vr/documentation/unreal/unreal-hand-tracking) |
| HandTrackingVersion | V2 | V2 is current | ✓ | Meta XR Plugin Settings |

### 3. OculusXRHandComponent Configuration

| Property | Current Value | Meta Best Practice | Status | Source |
|----------|---------------|-------------------|--------|--------|
| Parent Component | MotionControllerComponent | Must be child of UMotionControllerComponent | ✓ | [UOculusXRHandComponent](https://developers.meta.com/vr/reference/unreal/v207/class_u_oculus_x_r_hand_component) |
| SkeletonType | HAND_LEFT / HAND_RIGHT | Must match hand | ✓ | [UOculusXRHandComponent](https://developers.meta.com/vr/reference/unreal/v207/class_u_oculus_x_r_hand_component) |
| MeshType | HAND_LEFT / HAND_RIGHT | Must match hand | ✓ | [UOculusXRHandComponent](https://developers.meta.com/vr/reference/unreal/v207/class_u_oculus_x_r_hand_component) |
| ConfidenceBehavior | HIDE_ACTOR | HIDE_MESH or None recommended | ⚠️ | See analysis below |
| SystemGestureMaterial | None | Should be assigned | ⚠️ | [UOculusXRHandComponent](https://developers.meta.com/vr/reference/unreal/v207/class_u_oculus_x_r_hand_component) |
| skeletal_mesh | None | Auto-loaded at BeginPlay | ❌ FAIL | [GetHandSkeletalMesh](https://developers.meta.com/vr/documentation/unreal/unreal-blueprints-get-hand-skeletal-mesh) |
| bUpdateHandScale | True | True recommended | ✓ | [UOculusXRHandComponent](https://developers.meta.com/vr/reference/unreal/v207/class_u_oculus_x_r_hand_component) |

### 4. MotionControllerComponent Configuration

| Property | Current Value | Meta Best Practice (OpenXR) | Status | Source |
|----------|---------------|----------------------------|--------|--------|
| MotionSource (Left) | LeftHand | "Left" (wrist) for OpenXR | ⚠️ | [Choosing OpenXR Backend](https://developers.meta.com/vr/documentation/unreal/unreal-openxr) |
| MotionSource (Right) | RightHand | "Right" (wrist) for OpenXR | ⚠️ | [Choosing OpenXR Backend](https://developers.meta.com/vr/documentation/unreal/unreal-openxr) |

**Note:** Meta documentation states: "Motion source for hand tracking using default models should be set to wrist" when using OpenXR backend. The current configuration uses "LeftHand"/"RightHand" which may be OVRPlugin-specific motion sources.

---

## Identified Issues

### CRITICAL: skeletal_mesh is None

**Observation:** Both OculusXRHandComponent instances report `skeletal_mesh: None`

**Expected Behavior:** Per Meta documentation: "In most cases, UOculusXRHandComponent handles mesh creation automatically during BeginPlay. Use GetHandSkeletalMesh directly when you need custom hand mesh generation without relying on the component."

**Possible Causes:**
1. Plugin content not loading (hand mesh assets not found)
2. Plugin conflict between OculusXR and MetaXR preventing proper initialization
3. BeginPlay not being called or failing silently
4. Hand tracking data not available causing mesh generation to fail

### HIGH: Plugin Conflict (OculusXR + MetaXR)

**Observation:** Both `OculusXR` (Marketplace) and `MetaXR` plugins are enabled simultaneously

**Risk:** These plugins may have overlapping hand tracking implementations that conflict with each other. The OculusXR marketplace plugin is separate from the MetaXR plugin installed with the engine.

**Meta Guidance:** "If the Oculus VR plugin is displayed, do not enable it when using Unreal 5.x because it is deprecated."

### MEDIUM: ConfidenceBehavior set to HIDE_ACTOR

**Observation:** `ConfidenceBehavior: HIDE_ACTOR`

**Risk:** When tracking confidence drops (which happens frequently during normal use), the ENTIRE actor is hidden, not just the mesh. This can cause hands to disappear unexpectedly.

**Recommendation:** Use `HIDE_MESH` or `None` for more graceful degradation.

### MEDIUM: Motion Source Mismatch for OpenXR

**Observation:** MotionSource is "LeftHand"/"RightHand"

**OpenXR Requirement:** Per Meta documentation for OpenXR backend: "Motion source for hand tracking using default models should be set to wrist" (i.e., "Left"/"Right", not "LeftHand"/"RightHand")

**Impact:** May cause tracking origin or coordinate system mismatch, potentially explaining the 12-18" offset.

---

## VRC Compliance Status

| VRC Requirement | Status | Notes |
|-----------------|--------|-------|
| [VRC.Quest.Input.3](https://developers.meta.com/vr/resources/vrc-quest-input-3): Hands should line up with real-world position | ❌ FAIL | 12-18" offset observed |
| [VRC.Quest.Input.5](https://developers.meta.com/vr/resources/vrc-quest-input-5): Hands should render correctly | ❌ FAIL | Hands invisible |

---

## Steps to Reproduce

1. Create new Unreal Engine 5.8 project
2. Enable plugins: OpenXR, OpenXRHandTracking, MetaXR, OculusXR (Marketplace)
3. Configure DefaultEngine.ini with HandTrackingSupport=HandsOnly
4. Create VR Pawn with:
   - CameraComponent (lock_to_hmd=True)
   - Two MotionControllerComponents (LeftHand, RightHand)
   - OculusXRHandComponent as child of each MotionController
5. Deploy to Quest 3 or use VR Preview with Quest Link
6. Observe: Hands do not render

---

## Questions for Meta/Epic

1. **Plugin Coexistence:** Is it supported to have both `OculusXR` (Marketplace) and `MetaXR` enabled simultaneously? If not, which should be disabled?

2. **Skeletal Mesh Auto-Loading:** Under what conditions does `UOculusXRHandComponent::BeginPlay()` fail to auto-load the hand skeletal mesh? Are there prerequisites that must be met?

3. **Motion Source for OpenXR:** When using the OpenXR backend with OculusXRHandComponent, should the MotionControllerComponent use:
   - "Left"/"Right" (generic OpenXR wrist poses)
   - "LeftHand"/"RightHand" (OVRPlugin-specific)
   - Something else?

4. **Hand Mesh Asset Location:** Where should the hand mesh assets be located? We searched `/OculusXR/`, `/MetaXR/`, `/OculusInteraction/`, `/OculusXRInput/` and found no hand mesh assets.

5. **ConfidenceBehavior:** What is the recommended `EOculusXRConfidenceBehavior` setting for production apps?

---

## Requested Resolution

1. Clarification on correct plugin configuration for UE 5.8 + Quest 3 + hand tracking
2. Documentation on why skeletal_mesh auto-loading may fail
3. Guidance on correct MotionSource values for OpenXR backend
4. Fix for hand position offset (if this is a known issue)

---

## Attachments

- `DefaultEngine.ini` (hand tracking settings section)
- `BulldogMegaJam.uproject` (plugin list)
- Component hierarchy dump (above)

---

## References

- [Hand Tracking in Unreal Engine](https://developers.meta.com/vr/documentation/unreal/unreal-hand-tracking-overview/)
- [Setup Hand Tracking in Unreal Engine](https://developers.meta.com/vr/documentation/unreal/unreal-hand-tracking/)
- [UOculusXRHandComponent Class Reference](https://developers.meta.com/vr/reference/unreal/v207/class_u_oculus_x_r_hand_component)
- [GetHandSkeletalMesh Blueprint](https://developers.meta.com/vr/documentation/unreal/unreal-blueprints-get-hand-skeletal-mesh)
- [Choosing an OpenXR Backend](https://developers.meta.com/vr/documentation/unreal/unreal-openxr)
- [Setting up the Meta XR Plugin](https://developers.meta.com/vr/documentation/unreal/unreal-setting-up-metaxr-plugin)
- [VRC.Quest.Input.3](https://developers.meta.com/vr/resources/vrc-quest-input-3)
- [VRC.Quest.Input.5](https://developers.meta.com/vr/resources/vrc-quest-input-5)
- [Custom Hand and Controller Meshes](https://developers.meta.com/vr/documentation/unreal/unreal-isdk-custom-hand-controller-mesh/)
