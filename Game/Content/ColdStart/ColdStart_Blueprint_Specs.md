# ColdStart MVP - Blueprint Implementation Specifications

This document provides exact specifications for creating all ColdStart Blueprints in Unreal Editor 5.8.

---

## 1. BP_ShipState (Actor)

**Location:** `Content/ColdStart/Blueprints/BP_ShipState.uasset`
**Parent Class:** Actor

### Variables

| Name | Type | Default | Replicated | Description |
|------|------|---------|------------|-------------|
| EmergencyBusLive | Boolean | false | No | Emergency bus power state |
| BreakerC7Reset | Boolean | false | No | Breaker C-7 reset state |
| DroneDeployed | Boolean | false | No | Drone deployment state |
| CurrentPhase | Integer | 0 | No | Current scenario phase (0-3) |
| Instance | BP_ShipState (Static) | None | No | Singleton reference |

### Event Dispatchers

| Name | Parameters | Description |
|------|------------|-------------|
| OnPhaseCompleted | Phase (Integer) | Fired when a phase is completed |
| OnBusStateChanged | IsLive (Boolean) | Fired when emergency bus state changes |
| OnBreakerC7StateChanged | IsReset (Boolean) | Fired when C-7 breaker state changes |
| OnDroneStateChanged | IsDeployed (Boolean) | Fired when drone is deployed/recalled |

### Functions

#### GetInstance (Static, Pure)
- **Return:** BP_ShipState reference
- **Logic:** Return Instance variable (set in BeginPlay)

#### SetEmergencyBusLive
- **Input:** NewState (Boolean)
- **Logic:**
  1. Set EmergencyBusLive = NewState
  2. Call OnBusStateChanged.Broadcast(NewState)
  3. If NewState == true AND CurrentPhase == 0, call AdvancePhase()

#### SetBreakerC7Reset
- **Input:** NewState (Boolean)
- **Logic:**
  1. Set BreakerC7Reset = NewState
  2. Call OnBreakerC7StateChanged.Broadcast(NewState)
  3. If NewState == true AND CurrentPhase == 2, call AdvancePhase()

#### SetDroneDeployed
- **Input:** NewState (Boolean)
- **Logic:**
  1. Set DroneDeployed = NewState
  2. Call OnDroneStateChanged.Broadcast(NewState)

#### AdvancePhase
- **Logic:**
  1. CurrentPhase = CurrentPhase + 1
  2. Call OnPhaseCompleted.Broadcast(CurrentPhase - 1)
  3. Print String: "Phase [X] Complete"

### Event Graph

#### BeginPlay
1. Set Instance = Self
2. Print String: "BP_ShipState initialized - Phase 0"

---

## 2. BPC_PushButton (Actor Component)

**Location:** `Content/ColdStart/Components/BPC_PushButton.uasset`
**Parent Class:** Actor Component (or Scene Component for transform support)

### Components Hierarchy (if using Actor instead)
```
DefaultSceneRoot (Scene)
├── ButtonBase (Static Mesh) - SM_Cube scaled to (0.08, 0.08, 0.02)
├── ButtonCap (Static Mesh) - SM_Cylinder scaled to (0.06, 0.06, 0.015)
├── HitVolume (Box Collision) - Extent (0.1, 0.1, 0.05) - larger than visual
├── EmissiveIndicator (Point Light) - Intensity 0, Color Red
└── AudioComponent (Audio) - For button press sound
```

### Variables

| Name | Type | Default | Description |
|------|------|---------|-------------|
| IsPressed | Boolean | false | Current press state |
| IsEnabled | Boolean | true | Can button be pressed |
| IndicatorColor | Linear Color | (1, 0, 0, 1) | Emissive color when blinking |
| IsBlinking | Boolean | false | Blink indicator state |
| BlinkRate | Float | 2.0 | Blinks per second |
| PressDepth | Float | 0.01 | How far button depresses (meters) |
| ButtonPressSound | Sound Cue | None | Sound to play on press |

### Event Dispatchers

| Name | Parameters | Description |
|------|------------|-------------|
| OnButtonPressed | None | Fired when button is pressed |
| OnButtonReleased | None | Fired when button is released |

### Functions

#### Press
- **Logic:**
  1. If NOT IsEnabled, return
  2. Set IsPressed = true
  3. Move ButtonCap down by PressDepth (relative Z)
  4. Play ButtonPressSound
  5. Call OnButtonPressed.Broadcast()

#### Release
- **Logic:**
  1. Set IsPressed = false
  2. Move ButtonCap back to original position
  3. Call OnButtonReleased.Broadcast()

#### SetBlinking
- **Input:** ShouldBlink (Boolean)
- **Logic:**
  1. Set IsBlinking = ShouldBlink
  2. If ShouldBlink, start blink timer
  3. If NOT ShouldBlink, stop timer, set indicator intensity to 0

### Event Graph

#### OnComponentBeginOverlap (HitVolume)
- **Condition:** Other Actor has tag "PlayerHand" or is XRPawn hand component
- **Logic:** Call Press()

#### OnComponentEndOverlap (HitVolume)
- **Logic:** Call Release()

#### Tick (when IsBlinking)
- **Logic:**
  1. Sin wave on EmissiveIndicator intensity
  2. Intensity = (Sin(Time * BlinkRate * 2PI) + 1) / 2 * MaxIntensity

---

## 3. BPC_GuardCover (Actor Component)

**Location:** `Content/ColdStart/Components/BPC_GuardCover.uasset`
**Parent Class:** Actor (needs physics)

### Components Hierarchy
```
DefaultSceneRoot (Scene)
├── HingePoint (Scene) - Pivot location at top edge
│   └── CoverMesh (Static Mesh) - SM_Cube scaled to (0.1, 0.06, 0.002)
├── GrabVolume (Box Collision) - Extent matches CoverMesh + padding
└── ChildSlot (Scene) - Where guarded control attaches
```

### Variables

| Name | Type | Default | Description |
|------|------|---------|-------------|
| IsOpen | Boolean | false | Cover state |
| OpenAngle | Float | -110.0 | Rotation when fully open (degrees) |
| ClosedAngle | Float | 0.0 | Rotation when closed |
| CurrentAngle | Float | 0.0 | Current hinge rotation |
| IsGrabbed | Boolean | false | Currently being manipulated |
| ChildControl | Actor | None | Reference to switch underneath |

### Event Dispatchers

| Name | Parameters | Description |
|------|------------|-------------|
| OnCoverOpened | None | Fired when cover reaches open position |
| OnCoverClosed | None | Fired when cover reaches closed position |

### Functions

#### SetOpen
- **Input:** ShouldOpen (Boolean)
- **Logic:**
  1. Timeline: Interp CurrentAngle to OpenAngle or ClosedAngle
  2. Apply rotation to HingePoint (local Y axis)
  3. Set IsOpen = ShouldOpen
  4. Broadcast appropriate event

#### OnGrabbed
- **Logic:**
  1. Set IsGrabbed = true
  2. Disable physics sim if using physics

#### OnReleased
- **Logic:**
  1. Set IsGrabbed = false
  2. If CurrentAngle < -55, snap to open; else snap to closed

### Notes
- Cover must be opened BEFORE the switch underneath can be interacted with
- ChildControl should check parent cover IsOpen state before allowing interaction

---

## 4. BPC_ToggleSwitch (Actor Component)

**Location:** `Content/ColdStart/Components/BPC_ToggleSwitch.uasset`
**Parent Class:** Actor

### Components Hierarchy
```
DefaultSceneRoot (Scene)
├── SwitchBase (Static Mesh) - SM_Cube scaled (0.04, 0.02, 0.01)
├── SwitchHandle (Static Mesh) - SM_Cylinder scaled (0.008, 0.008, 0.03)
├── GrabVolume (Sphere Collision) - Radius 0.05 (larger for hand tracking)
├── AudioComponent (Audio)
└── ParentCoverRef (Scene) - Optional reference to guard cover
```

### Variables

| Name | Type | Default | Description |
|------|------|---------|-------------|
| IsOn | Boolean | false | Switch state |
| IsEnabled | Boolean | true | Can be toggled |
| OnAngle | Float | 45.0 | Handle angle when ON |
| OffAngle | Float | -45.0 | Handle angle when OFF |
| RequiresGuardOpen | Boolean | true | Must parent guard be open |
| ParentGuard | BPC_GuardCover | None | Reference to covering guard |
| SwitchClickSound | Sound Cue | None | Sound on toggle |

### Event Dispatchers

| Name | Parameters | Description |
|------|------------|-------------|
| OnSwitchToggled | NewState (Boolean) | Fired when switch changes state |

### Functions

#### Toggle
- **Logic:**
  1. If NOT IsEnabled, return
  2. If RequiresGuardOpen AND ParentGuard.IsOpen == false, return
  3. Set IsOn = NOT IsOn
  4. Timeline: Rotate SwitchHandle to OnAngle or OffAngle
  5. Play SwitchClickSound
  6. Call OnSwitchToggled.Broadcast(IsOn)

#### SetState
- **Input:** NewState (Boolean)
- **Logic:**
  1. If NewState == IsOn, return
  2. Call Toggle()

### Event Graph

#### OnGrab (GrabVolume overlap + hand grasp)
- **Logic:** Track hand position relative to switch center

#### OnRelease
- **Logic:**
  1. If hand moved > threshold distance up/down from grab point
  2. Call Toggle()

---

## 5. BPC_PushBreaker (Actor Component)

**Location:** `Content/ColdStart/Components/BPC_PushBreaker.uasset`
**Parent Class:** Actor

### Components Hierarchy
```
DefaultSceneRoot (Scene)
├── BreakerBody (Static Mesh) - SM_Cube scaled (0.03, 0.05, 0.02)
├── BreakerButton (Static Mesh) - SM_Cylinder scaled (0.015, 0.015, 0.01)
├── StatusIndicator (Point Light) - Shows tripped (red) or reset (green)
├── HitVolume (Box Collision) - Larger than visual for hand tracking
├── AudioComponent (Audio)
└── Label (Text Render) - "C-7" or similar
```

### Variables

| Name | Type | Default | Description |
|------|------|---------|-------------|
| IsTripped | Boolean | true | Breaker state (true = tripped/off) |
| BreakerID | String | "C-7" | Identifier for this breaker |
| CanBeReset | Boolean | true | Reset allowed |
| PressDepth | Float | 0.005 | Button depression distance |
| ResetSound | Sound Cue | None | Sound on successful reset |
| TripSound | Sound Cue | None | Sound when tripped |

### Event Dispatchers

| Name | Parameters | Description |
|------|------------|-------------|
| OnBreakerReset | BreakerID (String) | Fired when breaker is reset |
| OnBreakerTripped | BreakerID (String) | Fired when breaker trips |

### Functions

#### Reset
- **Logic:**
  1. If NOT CanBeReset OR NOT IsTripped, return
  2. Set IsTripped = false
  3. Depress BreakerButton, then return
  4. Set StatusIndicator color to Green, intensity up
  5. Play ResetSound
  6. Call OnBreakerReset.Broadcast(BreakerID)

#### Trip
- **Logic:**
  1. If IsTripped, return
  2. Set IsTripped = true
  3. Set StatusIndicator color to Red
  4. Play TripSound
  5. Call OnBreakerTripped.Broadcast(BreakerID)

### Event Graph

#### OnComponentBeginOverlap (HitVolume)
- **Condition:** Overlapping actor is player hand or drone manipulator
- **Logic:** Call Reset()

---

## 6. BP_MaintenanceDrone (Actor)

**Location:** `Content/ColdStart/Blueprints/BP_MaintenanceDrone.uasset`
**Parent Class:** Pawn

### Components Hierarchy
```
DefaultSceneRoot (Scene)
├── DroneBody (Static Mesh) - Simple box/sphere shape
├── Spotlight (Spot Light) - Range 3m, Angle 30, Warm white
├── DroneCamera (Scene Capture Component 2D) - 320x240
├── CollisionVolume (Sphere Collision) - For physics
├── ManipulatorArm (Scene)
│   └── ManipulatorTip (Sphere Collision) - Radius 0.02
├── ThrusterAudio (Audio) - Looping motor sound
└── FloatingPawnMovement (Movement Component)
```

### Variables

| Name | Type | Default | Description |
|------|------|---------|-------------|
| IsDeployed | Boolean | false | Drone active state |
| MoveSpeed | Float | 0.4 | Movement speed m/s |
| TurnSpeed | Float | 45.0 | Rotation speed deg/s |
| RenderTarget | Texture Render Target 2D | None | Camera output |
| HomeLocation | Vector | (0,0,0) | Deployment origin |
| ControllerRef | BP_DroneController | None | Physical controller reference |

### Event Dispatchers

| Name | Parameters | Description |
|------|------------|-------------|
| OnDroneDeployed | None | Drone activated |
| OnDroneRecalled | None | Drone deactivated |
| OnManipulatorActivated | None | Manipulator arm extended |

### Functions

#### Deploy
- **Input:** StartLocation (Vector)
- **Logic:**
  1. Set HomeLocation = StartLocation
  2. Teleport to StartLocation
  3. Set IsDeployed = true
  4. Enable SceneCaptureComponent2D
  5. Start ThrusterAudio
  6. Call OnDroneDeployed.Broadcast()

#### Recall
- **Logic:**
  1. Stop ThrusterAudio
  2. Disable SceneCaptureComponent2D
  3. Set IsDeployed = false
  4. Call OnDroneRecalled.Broadcast()

#### Move
- **Input:** ForwardInput (Float), YawInput (Float)
- **Logic:**
  1. If NOT IsDeployed, return
  2. Add movement: Forward * MoveSpeed * DeltaTime
  3. Add rotation: Yaw * TurnSpeed * DeltaTime

#### ActivateManipulator
- **Logic:**
  1. Extend ManipulatorArm forward (timeline)
  2. Call OnManipulatorActivated.Broadcast()
  3. Retract after 0.5s

### Tick
- **Logic:**
  1. Get input from ControllerRef
  2. Call Move(ForwardInput, YawInput)

---

## 7. BP_DroneController (Actor)

**Location:** `Content/ColdStart/Blueprints/BP_DroneController.uasset`
**Parent Class:** Actor

### Components Hierarchy
```
DefaultSceneRoot (Scene)
├── ControllerBase (Static Mesh) - Console-mounted joystick base
├── JoystickHandle (Static Mesh) - Grabbable stick
├── GrabVolume (Sphere Collision) - For hand interaction
├── DeployButton (Child Actor: BPC_PushButton)
├── ManipulatorButton (Child Actor: BPC_PushButton)
└── FeedDisplay (Static Mesh with Material Instance)
```

### Variables

| Name | Type | Default | Description |
|------|------|---------|-------------|
| DroneRef | BP_MaintenanceDrone | None | Controlled drone |
| ForwardInput | Float | 0.0 | Current forward/back input |
| YawInput | Float | 0.0 | Current turn input |
| IsGrabbed | Boolean | false | Joystick held |
| NeutralPosition | Vector | (0,0,0) | Joystick rest position |
| MaxTilt | Float | 30.0 | Max joystick angle |

### Functions

#### UpdateInputFromHand
- **Input:** HandPosition (Vector)
- **Logic:**
  1. Calculate offset from NeutralPosition
  2. Convert X offset to YawInput (-1 to 1)
  3. Convert Y offset to ForwardInput (-1 to 1)
  4. Rotate JoystickHandle to match

#### GetForwardInput (Pure)
- **Return:** ForwardInput (Float)

#### GetYawInput (Pure)
- **Return:** YawInput (Float)

### Event Graph

#### BeginPlay
1. Get DeployButton.OnButtonPressed, bind to DroneRef.Deploy()
2. Get ManipulatorButton.OnButtonPressed, bind to DroneRef.ActivateManipulator()

#### OnGrab
- **Logic:** Set IsGrabbed = true

#### OnRelease
- **Logic:**
  1. Set IsGrabbed = false
  2. Timeline: Return JoystickHandle to neutral
  3. Set ForwardInput = 0, YawInput = 0

#### Tick (when IsGrabbed)
- **Logic:** Call UpdateInputFromHand with grabbed hand position

---

## 8. UI Widgets

### WBP_FaultDisplay

**Location:** `Content/ColdStart/UI/WBP_FaultDisplay.uasset`
**Parent Class:** User Widget

#### Hierarchy
```
Canvas Panel
└── Vertical Box
    ├── Text Block (Line1) - "CO2 SCRUBBER"
    ├── Text Block (Line2) - "FAULT: MAIN BUS OFFLINE"
    └── Text Block (Line3) - "PRESS TO ACKNOWLEDGE"
```

#### Variables
| Name | Type | Default |
|------|------|---------|
| Line1Text | Text | "CO2 SCRUBBER" |
| Line2Text | Text | "FAULT" |
| Line3Text | Text | "" |
| TextColor | Slate Color | Green (0.2, 1.0, 0.2) |
| FontSize | Integer | 18 |

#### Functions
- SetLine1(Text)
- SetLine2(Text)
- SetLine3(Text)
- SetAllLines(Text, Text, Text)

---

### WBP_FaultTree

**Location:** `Content/ColdStart/UI/WBP_FaultTree.uasset`
**Parent Class:** User Widget

#### Hierarchy
```
Canvas Panel
└── Vertical Box
    ├── Text Block (Header) - "SYSTEM STATUS"
    ├── Horizontal Box (Row1)
    │   ├── Text Block - "MAIN BUS"
    │   └── Text Block - "OFFLINE" (red) / "ONLINE" (green)
    ├── Horizontal Box (Row2)
    │   ├── Text Block - "BREAKER C-7"
    │   └── Text Block - "TRIPPED" (red) / "RESET" (green)
    └── ... additional rows
```

#### Variables
| Name | Type |
|------|------|
| StatusItems | Array of Structs (Name: String, Status: Boolean) |

#### Functions
- UpdateStatus(Name: String, IsOK: Boolean)
- AddStatusItem(Name: String)

---

## 9. Level Setup: L_ColdStart

**Location:** `Content/XRFramework/Levels/L_ColdStart.umap`

### Required Actors

| Actor | Location | Notes |
|-------|----------|-------|
| Player Start | (0, 0, 0) | Center of room |
| BP_ShipState | (0, 0, 0) | Singleton state manager |
| BP_XRPawn | Spawned by GameMode | Player character |

### Wall Positions (2.7m x 2.7m room)

| Wall | Center Position | Forward | Controls |
|------|-----------------|---------|----------|
| North | (0, 1.35, 0) | -Y | Fault Tree Display |
| East | (1.35, 0, 0) | -X | Emergency Bus Breaker, Drone Controller |
| South | (0, -1.35, 0) | +Y | Schematic Display |
| West | (-1.35, 0, 0) | +X | CO2 Button, Battery Switch, Conduit Hatch |

### Control Placements (heights from floor)

| Control | Wall | Height | Position |
|---------|------|--------|----------|
| CO2 Fault Button | West | 1.2m | (-1.3, 0, 1.2) |
| Battery Guard Cover | West | 1.4m | (-1.3, -0.3, 1.4) |
| Battery Toggle Switch | West | 1.4m | Under guard cover |
| Emergency Bus Breaker | East | 1.3m | (1.3, 0.2, 1.3) |
| Fault Tree Display | North | 1.5m | (0, 1.3, 1.5) |
| Drone Controller | East | 1.0m | (1.3, -0.3, 1.0) |
| Conduit Hatch | West | 0.5m | (-1.3, 0.3, 0.5) |

### Lighting Setup

#### Light Group: Dark
- All lights disabled except:
  - CO2 Button indicator (blinking red, low intensity)

#### Light Group: Emergency
- Red strip lights along ceiling edges
- Low-intensity red point lights at each station
- Emergency bus breaker indicator (green)

---

## 10. Phase Logic Implementation

### Phase 0: Cold Open (BP_ShipState + Level Blueprint)

**Trigger:** Game Start
**State:** All power off, darkness

**Sequence:**
1. Player spawns at center
2. CO2 button starts blinking (SetBlinking(true))
3. Wait for player to press CO2 button
4. Fault display shows "NO MAIN BUS - CHECK BATTERY ISOLATION"
5. Phase 0 ends (no advancement yet, just tutorial)

### Phase 1: Emergency Power

**Trigger:** CO2 button pressed
**Goal:** Restore emergency bus power

**Sequence:**
1. Hint: Battery isolation switch (West wall)
2. Player opens guard cover
3. Player toggles battery switch to ON
4. Emergency bus breaker becomes available
5. Player presses emergency bus breaker
6. OnBusStateChanged fires
7. Emergency lighting activates
8. Phase advances to 1

### Phase 2: Diagnosis

**Trigger:** Emergency bus online
**Goal:** Identify C-7 breaker as fault source

**Sequence:**
1. Fault tree display updates
2. Shows "BREAKER C-7 - TRIPPED"
3. Conduit hatch becomes accessible
4. Phase advances to 2

### Phase 3: Drone

**Trigger:** Fault identified
**Goal:** Reset C-7 with drone

**Sequence:**
1. Player opens conduit hatch
2. Player deploys drone from controller
3. Player pilots drone through conduit (~15m with 2 turns)
4. Player locates C-7 breaker
5. Player uses manipulator to reset C-7
6. OnBreakerC7StateChanged fires
7. Fault tree updates "BREAKER C-7 - RESET"
8. Screen fades: "Scenario continues..."

---

## Implementation Checklist

### Week 1
- [ ] Create L_ColdStart level (duplicate L_XRTemplate)
- [ ] Build 2.7m x 2.7m greybox room
- [ ] Place Player Start
- [ ] Create BP_ShipState actor
- [ ] Test hand tracking reach to all wall positions

### Week 2
- [ ] Create BPC_PushButton
- [ ] Create BPC_GuardCover
- [ ] Create BPC_ToggleSwitch
- [ ] Create BPC_PushBreaker
- [ ] Wire controls to BP_ShipState

### Week 3
- [ ] Create WBP_FaultDisplay
- [ ] Create WBP_FaultTree
- [ ] Implement Phase 0 sequence
- [ ] Implement Phase 1 sequence
- [ ] Add emergency lighting

### Week 4
- [ ] Create BP_MaintenanceDrone
- [ ] Create drone render target + material
- [ ] Create BP_DroneController
- [ ] Build conduit geometry
- [ ] Implement Phase 3 sequence

### Week 5
- [ ] Audio pass (button, switch, breaker, drone sounds)
- [ ] Hand tracking tuning
- [ ] Quest 3 performance validation
- [ ] End-of-demo fade
