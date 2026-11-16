# Guardian Visualizer Setup

## Overview
The `AGuardianVisualizer` C++ class reads your Quest Guardian play area at runtime and renders it as glowing green neon tubing (2cm diameter).

## Files Created
- `Source/BulldogMegaJam/GuardianVisualizer.h`
- `Source/BulldogMegaJam/GuardianVisualizer.cpp`
- `BulldogMegaJam.Build.cs` (updated with modules)
- `BulldogMegaJam.uproject` (ProceduralMeshComponent plugin enabled)

## Step 1: Compile the Project
1. Close Unreal Editor
2. Delete `Intermediate` and `Binaries` folders (clean rebuild)
3. Right-click `BulldogMegaJam.uproject` > Generate Visual Studio project files
4. Open in Visual Studio and Build (Development Editor | Win64)
5. Launch editor

## Step 2: Create M_NeonTube Material

1. In Content Browser: `Content/ColdStart/Materials/`
2. Right-click > Material > name it `M_NeonTube`
3. Open the material and configure:

### Material Settings (Details panel)
- **Shading Model:** Unlit
- **Blend Mode:** Opaque
- **Two Sided:** True

### Node Graph

```
[Constant3Vector]          [ScalarParameter]
 (0, 1, 0.25)      -->     "EmissiveIntensity"
 Name: "NeonColor"          Default: 50.0
       |                         |
       v                         v
   [Multiply] ------------------->
       |
       v
   [Emissive Color]
```

**Steps:**
1. Add **VectorParameter** node, name it `NeonColor`, set default to (0, 1, 0.25, 1)
2. Add **ScalarParameter** node, name it `EmissiveIntensity`, default: 50.0
3. Add **Multiply** node
4. Connect NeonColor RGB to Multiply A
5. Connect EmissiveIntensity to Multiply B
6. Connect Multiply output to **Emissive Color** input
7. Apply and Save

## Step 3: Place Guardian Visualizer in Level

1. Open your level (e.g., L_ColdStart)
2. In Place Actors panel, search for `GuardianVisualizer`
3. Drag into level at (0, 0, 0)
4. In Details panel:
   - **Tube Material:** Select `M_NeonTube`
   - **Tube Diameter:** 2.0 (cm)
   - **Height Offset:** 1.0 (cm above floor)
   - **Neon Color:** (0, 1, 0.25) green
   - **Emissive Intensity:** 50.0

## Step 4: Test

### In Editor (no Guardian available)
- Set **Use Fallback Bounds:** True
- Set **Fallback Bounds Size:** (200, 200, 0) for 2m x 2m test area
- Play in Editor to see green rectangle

### In VR Preview / On Quest
- Set **Use Fallback Bounds:** False
- Ensure Guardian is configured on Quest
- Play in VR Preview or deploy to Quest
- You should see green neon tube tracing your Guardian boundary

## Exposed Properties

| Property | Default | Description |
|----------|---------|-------------|
| TubeDiameter | 2.0 | Tube thickness in cm |
| TubeSegments | 8 | Vertices around circumference |
| HeightOffset | 1.0 | Height above floor in cm |
| NeonColor | (0, 1, 0.25) | Phosphor green |
| EmissiveIntensity | 50.0 | Glow brightness multiplier |
| TubeMaterial | null | Assign M_NeonTube here |
| bShowDebugPoints | false | Draw debug spheres at corners |
| bUseFallbackBounds | false | Use rectangle instead of Guardian |
| FallbackBoundsSize | (200, 200, 0) | Test bounds size in cm |

## Troubleshooting

**No mesh visible:**
- Check Output Log for "GuardianVisualizer:" messages
- Enable `bUseFallbackBounds` to test without Guardian
- Verify material is assigned

**Mesh visible but not glowing:**
- Ensure M_NeonTube uses Unlit shading model
- Check EmissiveIntensity is > 0
- Verify Post Process Volume has Bloom enabled

**Guardian returns 0 points:**
- Normal on PC without VR headset
- Use fallback bounds for testing
- On Quest: ensure Guardian is set up in system settings

## API Notes

Quest 3 (OpenXR) only supports `Boundary_PlayArea`, returning 4 corner points (rectangle).
`Boundary_Outer` (exact drawn boundary) returns empty array on OpenXR backend.
