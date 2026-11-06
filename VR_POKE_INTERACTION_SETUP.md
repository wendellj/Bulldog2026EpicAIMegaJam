# VR Poke Interaction Setup Guide
**ColdStart MVP - Hand Tracking Button Presses**

## Current Status

### ✅ What's Already Done:
1. **Hand collision enabled** - Both OculusXRHand components set to "OverlapAllDynamic" profile
2. **Button hitboxes configured** - CO2 button has HitVolume (BoxComponent) with OverlapAllDynamic
3. **SystemStatusDisplay visible** - Bright green text on east wall
4. **VR pawn spawned** - BP_VRPawn_HandTracking at (0, 0, 0) with hands tracking

### ⚠️ What Needs Blueprint Wiring:

## Step 1: Test Hand Collision (VR Preview)

1. **Launch VR Preview**
   - Click ⋮ next to Play button → "Play in VR"
   - Put on Quest 3 headset (ensure Link is active)

2. **Test hand visibility**
   - Hold hands in front of face
   - Hands should be visible and tracking

3. **Test CO2 button collision**
   - Reach toward west wall (-130, 0, 120)
   - Try to poke the CO2 button with index finger
   - **Watch Output Log** for any overlap events

## Step 2: Add Fingertip Collision (If Needed)

If hand mesh collision doesn't trigger overlaps, manually add fingertip spheres:

### In BP_VRPawn_HandTracking Blueprint:

1. **Open** `Content/ColdStart/Blueprints/BP_VRPawn_HandTracking`

2. **Add Components:**
   - Add Sphere Collision component → name: `LeftFingertip`
   - Add Sphere Collision component → name: `RightFingertip`

3. **Configure LeftFingertip:**
   - **Parent:** MotionController_Left
   - **Sphere Radius:** 1.5 (1.5cm)
   - **Relative Location:** (10, 0, 0) ← 10cm forward
   - **Collision Preset:** OverlapAllDynamic
   - **Generate Overlap Events:** ✓ Enabled
   - **Component Tags:** Add tag `Fingertip`

4. **Configure RightFingertip:**
   - **Parent:** MotionController_Right
   - **Sphere Radius:** 1.5
   - **Relative Location:** (10, 0, 0)
   - **Collision Preset:** OverlapAllDynamic
   - **Generate Overlap Events:** ✓ Enabled
   - **Component Tags:** Add tag `Fingertip`

5. **Compile and Save**

## Step 3: Wire CO2 Button to Game Logic

### In Ctrl_CO2_Button Blueprint:

1. **Open** `Content/ColdStart/Components/BPC_PushButton` (or the CO2 button actor)

2. **Event Graph:**

```
Event BeginPlay
  └─ Get Actor Reference → BP_ShipState (cast to BP_ShipState)
      └─ Save to variable: ShipStateRef

Event OnComponentBeginOverlap (HitVolume)
  ├─ Other Actor → Get Component by Class → OculusXRHandComponent
  │   └─ Is Valid?
  │       └─ YES → Print String: "Hand touching CO2 button!"
  │                └─ Call Press()
  │
  └─ OR check Component Tags contains "Fingertip"
      └─ YES → Print String: "Fingertip touching CO2 button!"
               └─ Call Press()

Function: Press
  ├─ Print String: "CO2 BUTTON PRESSED"
  ├─ Get ShipStateRef
  └─ Call ShipStateRef.SetEmergencyBusLive(true)
```

## Step 4: Create BP_ShipState Functions

### In BP_ShipState Blueprint:

1. **Open** `Content/ColdStart/Blueprints/BP_ShipState`

2. **Create Function: SetEmergencyBusLive**
   - **Input:** NewState (Boolean)
   - **Logic:**
     ```
     Set EmergencyBusLive = NewState
     ├─ Call OnBusStateChanged (Event Dispatcher)
     └─ Branch: NewState == true AND CurrentPhase == 0
         └─ TRUE → Call AdvancePhase()
                   Print String: "Emergency bus online! Phase 0 complete"
     ```

3. **Create Function: AdvancePhase**
   - **Logic:**
     ```
     CurrentPhase = CurrentPhase + 1
     ├─ Print String: "Advanced to Phase [CurrentPhase]"
     └─ Call OnPhaseCompleted (Event Dispatcher with old phase number)
     ```

4. **Event BeginPlay:**
   ```
   Set Instance = Self
   └─ Print String: "BP_ShipState initialized - Phase 0"
   ```

## Step 5: Test Phase 0

1. **Launch VR Preview**
2. **Look for west wall** (CO2 button)
3. **Reach out and poke** the button with index finger
4. **Expected behavior:**
   - Output Log shows: "Hand touching CO2 button!"
   - Output Log shows: "CO2 BUTTON PRESSED"
   - Output Log shows: "Emergency bus online! Phase 0 complete"
   - Output Log shows: "Advanced to Phase 1"

## Troubleshooting

### Hands not visible:
- Check Quest settings → Movement Tracking → Hand Tracking enabled
- Make sure no controllers are nearby (they override hand tracking)

### No overlap events firing:
- Add fingertip collision spheres (see Step 2)
- Check Output Log for any error messages
- Verify HitVolume has Generate Overlap Events enabled

### Button pressed but no phase change:
- Check BP_ShipState is spawned in level at (0, 0, 0)
- Verify SetEmergencyBusLive function exists and is wired correctly
- Check CurrentPhase variable starts at 0

## Next Steps After Phase 0 Works:

1. **Phase 1:** Guard cover + toggle switch + breaker
2. **Phase 2:** Fault tree display
3. **Audio:** Button click sounds
4. **Visual feedback:** Button depression animation, indicator lights

---

**Files Modified:**
- BP_VRPawn_HandTracking: Collision enabled on hands
- Ctrl_CO2_Button: Has HitVolume ready for overlap detection
- SystemStatusDisplay: Visible, bright green text

**Ready for Blueprint wiring!**
