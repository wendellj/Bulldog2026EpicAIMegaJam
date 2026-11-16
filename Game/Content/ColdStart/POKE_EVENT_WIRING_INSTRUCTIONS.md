# Manual Blueprint Wiring: ISDK Poke Event

**Verified for:** Unreal Engine 5.8.4, Meta XR Interaction SDK v207

## Automation Status

| Property | Status | Method |
|----------|--------|--------|
| `PokeSurface.PointablePlane` | ✅ AUTOMATED | Set via GenOrca `ue_set_component_property` |
| `PokeInteractable.SurfacePatch` | ❌ MANUAL | Interface reference - must use Blueprint nodes |
| `interactable_state_changed` event | ❌ MANUAL | GenOrca can't create K2Node_ComponentBoundEvent |

## Why Some Steps Are Manual

1. **Interface references** (`TScriptInterface<IIsdkISurfacePatch>`) cannot be set via Unreal's text import system
2. GenOrca/UnrealMCPython cannot create `K2Node_ComponentBoundEvent` nodes
3. Blueprint SCS (SimpleConstructionScript) isn't exposed to Python API in UE 5.8

## Verified API Names (from live query)

| Property | Actual Name | Type |
|----------|-------------|------|
| State change delegate | `interactable_state_changed` | `IsdkInteractableStateChanged` (multicast) |
| Surface reference | `SurfacePatch` | Interface property (`TScriptInterface`) |
| Plane reference | `PointablePlane` | Object reference (works with GenOrca) |
| Interactable state | `current_state` | `IsdkInteractableState` enum |
| Auto-enable | `auto_activate` | Boolean |

**State enum values** (from `IsdkInteractableState`):
- `NORMAL` (0) - Ready, not touched
- `HOVER` (1) - Finger approaching
- `SELECT` (2) - Finger has poked (TRIGGER ON THIS)
- `DISABLED` (3) - Component not active

**Note:** State shows DISABLED in editor; becomes NORMAL at runtime when interaction system initializes.

---

## Step 1: Wire PokeInteractable.SurfacePatch (MANUAL)

**Note:** `PokeSurface.PointablePlane → PokeablePlane` was already set via automation.

Open `BPC_PushButton` in Blueprint Editor (double-click in Content Browser).

### Why This Must Be Manual (Verified Findings)

**Technical findings from verification:**
1. `SurfacePatch` is `TScriptInterface<IIsdkISurfacePatch>` (interface reference)
2. GenOrca cannot set interface properties (text serialization limitation)
3. ISDK exposes **zero** Blueprint setter functions (verified: 0 matches)
4. Python `set_editor_property()` CAN set the value at runtime
5. **CRITICAL:** Interface references **do NOT persist** when level is saved - they reset to None

**Conclusion:** Wiring MUST happen at **runtime** via Construction Script or BeginPlay.

### Option A: Via Construction Script (RECOMMENDED)

1. Open `BPC_PushButton` in Blueprint Editor
2. Open **Construction Script** graph (next to Event Graph tab)
3. Drag `PokeInteractable` from Components panel into the graph
4. Drag off the blue pin → search **"Set Surface Patch"**
   - If found, drag `PokeSurface` to the Surface Patch input
   - If NOT found, search for **"Set"** and look for Surface Patch in property list
5. Connect execution wire from Construction Script entry node

### Option B: Via Event Graph BeginPlay

If Construction Script doesn't work:

1. Open **Event Graph**
2. Find or create **Event BeginPlay** node
3. Drag `PokeInteractable` from Components panel
4. Drag off blue pin → search "Surface Patch" or property setter
5. Connect `PokeSurface` to the input
6. Wire execution from BeginPlay

### Option C: Use UIsdkInteractableWidgetComponent

Meta's PokeExamples sample uses `UIsdkInteractableWidgetComponent` which auto-wires everything:

```
UIsdkInteractableWidgetComponent:
  bCreatePokeInteractable = true  // auto-creates and wires poke geometry
```

This is simpler but requires a Widget-based UI instead of mesh buttons.

Sample: https://github.com/oculus-samples/Unreal-InteractionSDK-Sample

### Verify auto_activate

1. In Components panel, select `PokeInteractable`
2. In Details panel, ensure `Auto Activate` is checked

**Compile and Save the Blueprint.**

---

## Step 2: Add State Changed Event to EventGraph

1. In **Components** panel, select `PokeInteractable`
2. In **Details** panel, scroll to **Events** section
3. Find `Interactable State Changed` (the delegate we verified: `interactable_state_changed`)
4. Click the **+** button to create an event node in EventGraph

If no Events section is visible:
- Right-click in EventGraph
- Search for "Interactable State Changed"
- Or search for "Bind Event to Interactable State Changed"

---

## Step 3: Wire Event to Button Logic

The event node outputs:
- **Interactable** - Reference to the IsdkPokeInteractable
- **Args** - Struct containing state change info

### Wire the logic:

```
[On Interactable State Changed]
         |
         v
[Break IsdkInteractableStateChangeArgs]  (drag off Args pin, select "Break")
         |
         v
[Get New State] ──────────────────────┐
                                      |
[Make Literal IsdkInteractableState]  |  (set to "Select")
         |                            |
         v                            v
      [Equal] ◄───────────────────────┘
         |
         v (True)
    [Branch]
         |
         v (True)
    [DoOnce]  ◄── (use existing DoOnce if present)
         |
         v
[Play Sound 2D]  ◄── (existing audio: click_004)
         |
         v
[Set Material]  ◄── (existing: green → red)
```

**Key:** Compare `NewState` to `Select` (value 2). When finger pokes the surface, state becomes `Select`.

---

## Step 4: Compile, Save, Test

1. Click **Compile** in Blueprint toolbar
2. Click **Save**
3. Save the level (Ctrl+S)
4. Enter VR Preview (Play dropdown → VR Preview)
5. Poke button with index finger
6. Should hear click sound and see color change

---

## Troubleshooting

**Button doesn't respond in VR:**
- Verify `PokeSurface.pointable_plane` is wired to `PokeablePlane`
- Verify `PokeInteractable.surface_patch` is wired to `PokeSurface`
- Verify `PokeInteractable.auto_activate` is true
- Check that ISDK hand rigs have `IsdkPokeInteractor` on index fingertips (they should by default)

**State shows DISABLED in editor:**
- This is normal. State becomes NORMAL at runtime when BeginPlay fires.

**Event fires multiple times:**
- Use DoOnce node
- Only trigger on `NewState == Select`, not on Hover

**Finger goes through button:**
- Check `PokeablePlane.Size` is appropriate (5x5 cm default)
- Ensure button mesh aligns with the plane

---

## Component Hierarchy Reference

```
BPC_PushButton
├── DefaultSceneRoot
├── ButtonBase (StaticMesh - cube)
├── ButtonCap (StaticMesh - cylinder)
├── PokeablePlane (IsdkPointablePlane)
│   └── Size: (5, 5)
├── PokeSurface (IsdkClippedPlaneSurface)
│   └── pointable_plane → PokeablePlane
├── PokeInteractable (IsdkPokeInteractable)
│   └── surface_patch → PokeSurface
│   └── auto_activate: true
├── HitVolume (BoxComponent) - legacy overlap detection
├── EmissiveIndicator (PointLight)
├── AudioComponent
└── ButtonClickSound (AudioComponent)
```

---

*Verified 2026-11-08 via MCP queries against live Unreal Editor*
