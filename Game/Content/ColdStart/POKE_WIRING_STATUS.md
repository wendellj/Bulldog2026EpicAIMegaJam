# BPC_PushButton ISDK Poke Wiring Status

**Date:** 2026-11-08
**Blueprint:** `/Game/ColdStart/Components/BPC_PushButton`

## Automated via GenOrca ✅

### 1. Construction Script - SurfacePatch Wiring
```
Construction Script Entry
        ↓
Set SurfacePatch (on PokeInteractable)
  ├── Target: PokeInteractable
  └── SurfacePatch: PokeSurface
```
**Status:** COMPLETE - Compiles successfully

### 2. EventGraph - OnPokeSelect Event
- Added `OnPokeSelect` custom event
- Wired to existing DoOnce → Play Sound → Toggle Material

**Status:** COMPLETE

---

## Manual Step Required ❌

### Bind interactable_state_changed Event

GenOrca cannot create `K2Node_ComponentBoundEvent` nodes. You must manually bind the event.

**Steps:**

1. Open `BPC_PushButton` in Blueprint Editor (double-click in Content Browser)

2. In the **Components** panel (left side), click on `PokeInteractable`

3. In the **Details** panel (right side), scroll to find **Events** section

4. Find `Interactable State Changed` delegate

5. Click the **+** button next to it to create an event node in EventGraph

6. The event node has these outputs:
   - `Interactable` (reference)
   - `Args` (struct with `PreviousState` and `NewState`)

7. Wire the event to check for SELECT state:
   ```
   [On Interactable State Changed]
            ↓
   [Break IsdkInteractableStateChangeArgs] ← drag off Args
            ↓
   [Get New State] → [== Select?] → [Branch]
            ↓ (True)
   [Call OnPokeSelect]
   ```

   Or simpler (if you trust all state changes):
   ```
   [On Interactable State Changed]
            ↓
   [Call OnPokeSelect]
   ```

8. **Compile** and **Save** the blueprint

---

## Testing

1. Start VR Preview (Play dropdown → VR Preview)
2. Walk to the button on the West wall
3. Poke the button with your index finger
4. Expected: Click sound plays, button cap changes color

---

## Technical Reference

**IsdkInteractableState enum values:**
| Value | State | Description |
|-------|-------|-------------|
| 0 | NORMAL | Ready, not touched |
| 1 | HOVER | Finger approaching |
| 2 | SELECT | Finger poked through surface |
| 3 | DISABLED | Component not active |

**Key Components:**
- `PokeablePlane` (IsdkPointablePlane) - Defines pokeable surface bounds
- `PokeSurface` (IsdkClippedPlaneSurface) - Clips plane to button area
- `PokeInteractable` (IsdkPokeInteractable) - Detects poke intersection

**ISDK automatically provides:**
- `IsdkPokeInteractor` on index fingertips via `IsdkHandRigComponent`
- Touch limiting (hand stops when poking)
- Visual feedback (finger doesn't penetrate geometry)
