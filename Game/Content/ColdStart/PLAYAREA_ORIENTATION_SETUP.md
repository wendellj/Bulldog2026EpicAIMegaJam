# PlayArea Orientation Manager Setup

## Overview
The `APlayAreaOrientationManager` analyzes your Quest Guardian play area to find the longest traversable axis (diagonal for rectangles). Use this to orient your virtual world so corridors align with maximum physical walking distance.

## Why This Matters

For an 8'×8' (2.4m×2.4m) square play area:
- Edge length: 2.4m
- Diagonal length: 3.4m (41% more walking distance!)

Aligning virtual hallways with the diagonal maximizes how far the player can walk before needing redirection.

## Files Created
- `Source/BulldogMegaJam/PlayAreaOrientationManager.h`
- `Source/BulldogMegaJam/PlayAreaOrientationManager.cpp`

## Step 1: Compile the Project

Same as GuardianVisualizer - rebuild after adding new source files.

## Step 2: Place in Level

1. Open your level
2. In Place Actors panel, search for `PlayAreaOrientationManager`
3. Drag into level (position doesn't matter, it's just a data holder)
4. In Details panel:
   - **Use Fallback Bounds:** True for testing without VR
   - **Fallback Bounds Size:** (240, 240, 0) for 2.4m square
   - **Draw Debug Visualization:** True to see the analysis

## Step 3: Use the Orientation Data

### Option A: Blueprint - Rotate VR Pawn at Spawn

In your VR Pawn's BeginPlay:

```
Event BeginPlay
    |
    v
Get PlayAreaOrientationManager (static function)
    |
    v
Get Optimal Rotation
    |
    v
Set Actor Rotation (self)
```

### Option B: Blueprint - Rotate Level Geometry

If your level has a root actor containing all geometry:

```
Event BeginPlay
    |
    v
Get PlayAreaOrientationManager
    |
    v
Get Optimal Yaw Offset (negate it: multiply by -1)
    |
    v
Make Rotator (0, NegatedYaw, 0)
    |
    v
Set Actor Rotation (LevelRoot)
```

### Option C: C++ - Apply to Pawn

```cpp
#include "PlayAreaOrientationManager.h"

void AMyVRPawn::BeginPlay()
{
    Super::BeginPlay();

    if (APlayAreaOrientationManager* OrientationMgr = APlayAreaOrientationManager::Get(this))
    {
        // Rotate pawn to face along longest axis
        SetActorRotation(OrientationMgr->GetOptimalRotation());

        // Or get full spawn transform (position + rotation)
        // SetActorTransform(OrientationMgr->GetOptimalSpawnTransform());
    }
}
```

## API Reference

### Static Access
```cpp
// Get singleton instance from anywhere
APlayAreaOrientationManager* Mgr = APlayAreaOrientationManager::Get(WorldContextObject);
```

### Properties (BlueprintReadOnly)

| Property | Type | Description |
|----------|------|-------------|
| OptimalYawOffset | float | Degrees to rotate pawn to face diagonal |
| PlayAreaCenter | FVector | World position of play area center |
| LongestAxisStart | FVector | First endpoint of diagonal |
| LongestAxisEnd | FVector | Second endpoint of diagonal |
| LongestAxisLength | float | Diagonal length in cm |
| BoundaryPoints | TArray<FVector> | All 4 corner positions |

### Functions

| Function | Returns | Description |
|----------|---------|-------------|
| GetOptimalYawOffset() | float | Yaw in degrees |
| GetOptimalRotation() | FRotator | Rotator with just yaw set |
| GetOptimalSpawnTransform() | FTransform | Center position + optimal rotation |
| GetLongestAxis(...) | void | Out params for start, end, length |
| IsPlayAreaSufficient(MinLength) | bool | True if diagonal >= MinLength cm |
| RecalculateOrientation() | void | Force recalculation |

## Debug Visualization

When `bDrawDebugVisualization = true`:

- **Green lines:** Boundary edges
- **Cyan line:** Longest axis (diagonal)
- **Yellow arrow:** Optimal forward direction from center
- **Yellow sphere:** Play area center
- **White labels:** Corner point indices (P0, P1, P2, P3)

## Integration with GuardianVisualizer

Both actors can coexist in the same level:
- `GuardianVisualizer` - renders the neon tube boundary
- `PlayAreaOrientationManager` - calculates optimal orientation

They query the same Guardian data independently.

## Example: Full VR Pawn Setup

```cpp
void AMyVRPawn::BeginPlay()
{
    Super::BeginPlay();

    APlayAreaOrientationManager* Orientation = APlayAreaOrientationManager::Get(this);
    if (Orientation)
    {
        // Check if play area is large enough
        if (!Orientation->IsPlayAreaSufficient(150.0f))
        {
            UE_LOG(LogTemp, Warning, TEXT("Play area too small for comfortable RDW!"));
            // Show warning UI to player
        }

        // Position at center, facing diagonal
        SetActorTransform(Orientation->GetOptimalSpawnTransform());

        // Log the setup
        UE_LOG(LogTemp, Log, TEXT("VR Pawn spawned at center, facing %.1f degrees, diagonal = %.1fm"),
            Orientation->GetOptimalYawOffset(),
            Orientation->LongestAxisLength / 100.0f);
    }
}
```

## Troubleshooting

**OptimalYawOffset is 0:**
- Check if Guardian returned valid points (see Output Log)
- Enable fallback bounds for testing

**Pawn facing wrong direction:**
- You may need to negate the yaw depending on your setup
- Check if pawn's forward is +X (Unreal convention)

**Diagonal seems wrong:**
- Enable debug visualization to see the analysis
- For non-square rectangles, longest axis should be corner-to-corner
