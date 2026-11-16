# L_CarHop - Head-Tracked Low-Gravity Car Hopping

## Concept
Roomscale VR level where players physically jump to traverse a parking lot full of cars. Low gravity (1/5th Earth) and minimal mass (1kg) means body movements control trajectory.

**Movie Inspiration:** Action chase scenes, parkour over traffic

## Core Mechanics

### Head-Tracked Jump Detection
```
Every frame while grounded:
  1. Sample HMD world position (Y axis)
  2. Calculate Y velocity = (current_Y - previous_Y) / deltaTime
  3. If velocity > JUMP_THRESHOLD (0.4 m/s):
     - Launch player with impulse proportional to velocity
     - Enter airborne state
```

### Snowboard-Style Hand Control (Air Control)
```
While airborne:
  1. Get both hand positions relative to HMD
  2. Calculate hand centroid (midpoint between hands)
  3. Offset from HMD = thrust direction
     - Hands forward of head = forward thrust
     - Hands to left = drift left
     - Hands above head = slight upward (extend hang time)
  4. Calculate hand spread distance
     - Arms wide = air brake (dampen velocity)
     - Arms tucked = streamline (less drag)
  5. Apply forces based on 1kg mass

Example poses:
  - "Superman" (arms forward): Max forward thrust
  - "T-pose" (arms wide): Air brake, stabilize
  - "Tuck" (arms close to chest): Minimize drag, coast
  - "Point left" (left arm extended): Steer left
```

### Landing & Play Space Recentering
```
On collision with car surface:
  1. Set player grounded
  2. Recenter virtual world so current car is under player's physical position
  3. Brief cooldown before next jump allowed (0.3s)
```

### Fall Recovery
```
If player falls below car level:
  1. Fade to black (0.5s)
  2. Teleport back to last successfully landed car
  3. Fade in
  4. No penalty - encourages experimentation
```

## Physics Settings

| Parameter | Value | Reasoning |
|-----------|-------|-----------|
| Gravity Scale | 0.2 | 1/5th Earth gravity - floaty moon jumps |
| Player Mass | 1.0 kg | Tiny mass = responsive air control |
| Jump Threshold | 0.4 m/s | Filters out head sway, triggers on real jumps |
| Max Jump Impulse | 600 | Caps huge physical jumps |
| Air Control Force | 200 | Lean influence while airborne |
| Landing Cooldown | 0.3s | Prevents bunny hopping |

## Car Placement Design

### Parking Lot Layout (Top-Down)
```
START                                               GOAL
  [P]                                                [G]
   |
   v
  [===]  [===]      [===]
         [===]  [===]      [===]
  [===]         [===]  [===]
      [===]  [===]      [===]  [===]
   [===]      [===]  [===]      [===]

Legend:
  [P] = Player start platform (easy first jump)
  [===] = Car (roof = landing surface)
  [G] = Goal platform (glowing, distinct)
```

### Difficulty Progression
1. **Near start:** Cars close together (1-2m gaps), similar heights
2. **Mid section:** Larger gaps (2-3m), varied heights (sedan vs SUV vs truck)
3. **Near goal:** Requires longer jumps, strategic routing

### Car Types (Height Variety)
| Type | Roof Height | Notes |
|------|-------------|-------|
| Sedan | 1.4m | Standard, most common |
| SUV | 1.7m | Taller, good landing target |
| Pickup Truck | 1.5m | Bed at 1.0m, cab at 1.5m |
| Sports Car | 1.2m | Low, harder to land on |
| Van | 1.9m | Tallest, landmark |

## Asset Requirements

### From Hyper3D Rodin
Generate via https://hyper3d.ai/workspace/rodin:
- "realistic sedan car low poly game asset"
- "realistic SUV low poly game asset"
- "realistic pickup truck low poly game asset"
- "realistic sports car low poly game asset"
- "realistic van low poly game asset"

**Request settings:**
- Format: GLB or FBX
- Target: Low poly (~5k tris max for Quest 3)
- Style: Realistic but optimized

### Environment
- Ground plane: Asphalt texture (realistic parking lot)
- Cars at ground level (realistic placement, not floating)
- Parking lines: White stripes
- Light posts: For scale reference
- Sky: Daytime, outdoor
- Start platform: Raised platform with "START" text
- Goal platform: Glowing/distinct "FINISH" marker

### Audio
- **Jump whoosh**: Plays on launch, pitch varies with jump strength
- **Wind rush**: Looping while airborne, volume scales with velocity
- **Landing thud**: Plays on car roof contact, heavier for harder landings
- **Victory fanfare**: Plays when reaching goal
- **Ambient**: Outdoor parking lot ambience (birds, distant traffic)

## Blueprint Architecture

### BP_VRPawn_HeadJump
```
Components:
├── DefaultSceneRoot
├── VRCamera (CameraComponent, bLockToHmd=true)
├── MotionController_Left
│   └── LeftHandRig (IsdkHandRigComponentLeft)
├── MotionController_Right
│   └── RightHandRig (IsdkHandRigComponentRight)
├── CapsuleCollision (for physics)
└── FloatingPawnMovement (GravityScale=0.2)

Variables:
- bIsGrounded (bool)
- LastGroundedLocation (Vector)
- PreviousHeadY (float)
- JumpCooldownRemaining (float)
- CurrentLandedCar (Actor reference)
- HandCentroid (Vector) - midpoint between hands
- HandSpread (float) - distance between hands

Functions:
- DetectJump() - samples head Y velocity, triggers launch
- ApplyHandControl() - snowboard-style thrust from hand positions
- HandleLanding() - recenter play space on car
- HandleFall() - fade + teleport recovery
```

### BP_CarPlatform
```
Components:
├── CarMesh (StaticMeshComponent)
├── RoofCollider (BoxComponent) - landing detection
└── Audio (landing sound)

Variables:
- CarType (enum: Sedan, SUV, Truck, Sports, Van)
```

### BP_GoalPlatform
```
Components:
├── PlatformMesh
├── GoalTrigger (BoxComponent)
├── GlowEffect (particle/material)
└── Audio (victory sound)
```

## Level Flow

1. **Spawn:** Player starts on raised platform, sees parking lot ahead
2. **Tutorial:** First car is close, easy jump to learn mechanic
3. **Traversal:** Player hops across cars toward goal
4. **Falls:** Teleport back to last car, no penalty
5. **Victory:** Reach goal platform, celebration effect, level complete

## Quest 3 Performance Targets

- 72 FPS minimum (90 FPS target)
- Max 20 cars visible at once
- LOD system for distant cars
- Baked lighting where possible
- Total triangle budget: ~500k for scene

## File Locations

```
Content/DirectorsCut/CarHop/
├── Levels/
│   └── L_CarHop.umap
├── Blueprints/
│   ├── BP_VRPawn_HeadJump.uasset
│   ├── BP_CarPlatform.uasset
│   └── BP_GoalPlatform.uasset
├── Meshes/
│   ├── SM_Car_Sedan.uasset
│   ├── SM_Car_SUV.uasset
│   ├── SM_Car_Truck.uasset
│   ├── SM_Car_Sports.uasset
│   └── SM_Car_Van.uasset
├── Materials/
│   ├── M_Asphalt.uasset
│   └── M_ParkingLines.uasset
└── Audio/
    ├── SFX_Land.uasset
    └── SFX_Victory.uasset
```
