# ColdStart Manual Blueprint Steps

These steps cannot be automated due to GenOrca/UnrealMCPython limitations.

---

## 1. Apply Yellow Material to VR Hands

**Blueprint:** `BP_VRPawn_HandTracking` at `/Game/ColdStart/Blueprints/`

1. Open `BP_VRPawn_HandTracking` in Blueprint Editor (double-click in Content Browser)
2. In **Components** panel, expand **LeftHandRig**
3. Look for **Hand Visuals Component** (may be collapsed under IsdkHandRigComponent)
4. Under that, find **Tracked Hand Visual** and/or **Synthetic Hand Visual**
5. In Details panel, find **Material Override** property
6. Set it to `MI_Hand_Yellow` (located at `/Game/ColdStart/Materials/`)
7. Repeat steps 2-6 for **RightHandRig**
8. Click **Compile** and **Save**

**Material created:** `MI_Hand_Yellow` - Light yellow color (R=1.0, G=0.95, B=0.6)

---

## 2. Filter Button Pokes for SELECT State Only

**Problem:** `InteractableStateChanged` fires on ALL state changes (DISABLED→NORMAL at startup, HOVER, SELECT). We only want to trigger on actual pokes (SELECT).

**Blueprint:** `BPC_PushButton_New` at `/Game/ColdStart/Components/`

### Add State Check Logic:

1. Open `BPC_PushButton_New` EventGraph
2. Find the **On Interactable State Changed** event node
3. From the **Args** output pin, drag and select **Break IsdkInteractableStateChangeArgs**
4. From **New State** pin of the Break node, drag and search for **Equal (Enum)**
5. For the comparison value, select **Select** (value 2)
6. Add a **Branch** node
7. Connect the **Equal** result to the Branch **Condition**
8. Wire execution: Event → Break → Branch
9. Connect Branch **True** to your PlaySound2D and SetMaterial nodes
10. **Compile** and **Save**

### Visual Flow:
```
[On Interactable State Changed]
         |
         v
[Break IsdkInteractableStateChangeArgs]
         |
    [New State] ──► [Equal (Select)]
                           |
                           v
                      [Branch]
                           |
                      True ▼
                    [DoOnce]
                           |
                           v
                  [Play Sound 2D]
                           |
                           v
                   [Set Material]
```

**State enum values:**
- NORMAL (0) - Ready, not touched
- HOVER (1) - Finger approaching
- SELECT (2) - Finger has poked (TRIGGER ON THIS)
- DISABLED (3) - Component not active

---

## 3. Set Object Reference Pins Manually

**Problem:** GenOrca's `pin_defaults` only works for primitive types (int, float, bool, string). Object reference pins (Sound, Material, Texture, etc.) must be set manually.

**Bug filed:** `Plugins/UnrealMCPython/ISSUE_pin_defaults_object_refs.md`

### For PlaySound2D Sound Pin:

1. In `BPC_PushButton_New` EventGraph, find **Play Sound 2D** node
2. Click the **Sound** pin dropdown
3. Search for and select `click4` (or your preferred sound from `/Game/ColdStart/Audio/`)

### For SetMaterial Material Pin:

1. Find the **Set Material** node
2. Click the **Material** pin dropdown
3. Select `MI_Ctrl_Green` for the "on" state (or `MI_Ctrl_Red` for toggle)

---

## 4. Wire ISDK Component References (if not already done)

**Problem:** Interface references (`TScriptInterface`) don't persist when saved. Must wire at runtime.

See: `POKE_EVENT_WIRING_INSTRUCTIONS.md` for full details.

### Quick Summary:

In **Construction Script** of `BPC_PushButton_New`:

1. Get **PokeInteractable** → call **Set Surface Patch** → input **PokeSurface**
2. Get **PokeSurface** → call **Set Pointable Plane** → input **PokeablePlane**

Both should already be wired if the Blueprint was built correctly.

---

## 5. Wire Input Mapping Contexts in VR Pawn (CRITICAL for ISDK Poke)

**Problem:** ISDK poke interactions require Input Mapping Contexts to be added in BeginPlay. GenOrca cannot create `K2Node_GetSubsystemFromPC` nodes.

**Blueprint:** `BP_VRPawn_HandTracking` at `/Game/Blackbox/Blueprints/`

**Status:** Partial automation completed. The following nodes were added by GenOrca:
- Is Head Mounted Display Enabled
- Branch
- Set Tracking Origin (Local Floor)
- Get Player Controller
- Add Mapping Context (IMC_IsdkHand)
- Add Mapping Context (IMC_IsdkControllerAnimation)
- Get Local Player Subsystem (incomplete)

### Manual Completion Steps:

1. Open `BP_VRPawn_HandTracking` in Blueprint Editor
2. Go to **Event Graph**
3. Find the two **Add Mapping Context** nodes (they should show "Target is Enhanced Input Subsystem Interface")
4. **Delete** the existing `Get Local Player Subsystem` node (K2Node_CallFunction_6) - it's the wrong type
5. Right-click and search for **Get Enhanced Input Local Player Subsystem**
   - This creates a `K2Node_GetSubsystemFromPC` node
6. Connect **Get Player Controller** output to **Get Enhanced Input Local Player Subsystem** PlayerController input
7. Connect **Get Enhanced Input Local Player Subsystem** output to BOTH **Add Mapping Context** Target pins
8. Verify the IMC pins are set (enable "Show Plugin Content" via gear icon in asset picker):
   - First Add Mapping Context: `/OculusInteraction/Inputs/IMC_IsdkHand`
   - Second Add Mapping Context: `/OculusInteraction/Inputs/IMC_IsdkControllerAnimation`
   - Priority: 1 for both
9. **Compile** and **Save**

### Visual Flow:
```
[Event BeginPlay]
        |
        v
[Is Head Mounted Display Enabled] ──► [Branch]
                                          |
                                     True ▼
                              [Set Tracking Origin]
                              (Origin = Local Floor)
                                          |
                                          v
[Get Player Controller] ──► [Get Enhanced Input Local Player Subsystem]
                                          |
                                          v
                              [Add Mapping Context]
                              (IMC_IsdkHand, Priority 1)
                                          |
                                          v
                              [Add Mapping Context]
                              (IMC_IsdkControllerAnimation, Priority 1)
```

### Why This Matters:
Without Input Mapping Contexts, ISDK cannot receive hand input events (pinch, poke gestures). The poke button will not respond to finger touches.

---

## GenOrca Limitations Reference

| Feature | Status | Workaround |
|---------|--------|------------|
| `pin_defaults` for object pins | Bug filed (#73) | Set manually via dropdown |
| `BreakStruct` nodes | Feature request (#74) | Create manually in Blueprint |
| `K2Node_ComponentBoundEvent` | Not supported | Add event via Details panel + button |
| `K2Node_GetSubsystemFromPC` | Not supported | Create manually via right-click |
| Interface property persistence | Engine limitation | Wire in Construction Script |

---

*Last updated: 2026-11-12*
