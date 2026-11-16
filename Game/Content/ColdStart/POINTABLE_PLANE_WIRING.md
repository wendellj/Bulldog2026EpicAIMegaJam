# BPC_PushButton: PointablePlane Wiring Instructions

## Problem
The ISDK PokeInteractable shows "Interactable not registered" error because `PokeSurface.PointablePlane` is not set to reference the `PokeablePlane` component.

## Solution: Set Default Value (Easiest)

1. Open **BPC_PushButton** Blueprint
   - Path: `Content/ColdStart/Components/BPC_PushButton`

2. In the **Components** panel (left side), select **PokeSurface**

3. In the **Details** panel (right side), search for **Pointable Plane**

4. Click the dropdown and select **PokeablePlane**

5. Click **Compile** and **Save**

---

## Alternative: Wire in Construction Script

If you prefer runtime wiring:

1. Open **BPC_PushButton** Blueprint

2. Go to the **Construction Script** tab (not EventGraph)

3. Find the existing **Set SurfacePatch** node

4. From the **then** exec pin of "Set SurfacePatch", drag and release to add a new node

5. Search for **Set Pointable Plane** and add it

6. Connect the pins:
   - **Target**: Drag from the existing "Get PokeSurface" node (at position 112, 480)
   - **Pointable Plane**: Drag from the existing "Get PokeablePlane" node (at position 112, 600)

7. **Compile** and **Save**

---

## Verification

After wiring, the Construction Script should flow:
```
Construction Script Entry
    |
    v
Set SurfacePatch (PokeInteractable.SurfacePatch = PokeSurface)
    |
    v
Set PointablePlane (PokeSurface.PointablePlane = PokeablePlane)  <-- NEW
```

## Test
Run VR Preview and poke the button. The material should toggle between green and red.
