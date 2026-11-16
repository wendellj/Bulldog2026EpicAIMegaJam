# BPC_PushButton Material Toggle Wiring

## Current State (as of session)
The EventGraph has the toggle logic wired:
- Branch node checking `IsGreen` variable
- Two `Set IsGreen` nodes (one for each branch)
- Missing: SetMaterial calls to actually change the ButtonCap color

## Manual Steps to Complete

### 1. Open BPC_PushButton in Blueprint Editor
- Content Browser: `/Game/ColdStart/Components/BPC_PushButton`
- Double-click to open

### 2. Find the Branch Node
- Look for `K2Node_IfThenElse_0` (Branch)
- `IsGreen` connected to Condition pin
- `Then` pin goes to `K2Node_VariableSet_2` (Set IsGreen = false)
- `Else` pin goes to `K2Node_VariableSet_3` (Set IsGreen = true)

### 3. Add SetMaterial for TRUE path (green to red)
1. Find `K2Node_VariableSet_2` (True branch)
2. Drag off its **output exec pin** (white arrow on right)
3. Type "SetMaterial" and select it
4. On the SetMaterial node:
   - **Target**: Drag from Components panel -> `ButtonCap`
   - **Element Index**: 0
   - **Material**: `/Game/ColdStart/Materials/MI_NeonRed`

### 4. Add SetMaterial for FALSE path (red to green)
1. Find `K2Node_VariableSet_3` (Else branch)
2. Drag off its **output exec pin** (white arrow on right)
3. Type "SetMaterial" and select it
4. On the SetMaterial node:
   - **Target**: Drag from Components panel -> `ButtonCap`
   - **Element Index**: 0
   - **Material**: `/Game/ColdStart/Materials/MI_NeonGreen`

### 5. Compile and Save

## Final Flow
```
OnPokeSelect -> DoOnce -> Set IsPressed -> Branch (IsGreen?)
    |-- True  -> Set IsGreen=false -> SetMaterial(ButtonCap, MI_NeonRed)
    |-- Else  -> Set IsGreen=true  -> SetMaterial(ButtonCap, MI_NeonGreen)
```

## Material Paths
- Red: `/Game/ColdStart/Materials/MI_NeonRed.MI_NeonRed`
- Green: `/Game/ColdStart/Materials/MI_NeonGreen.MI_NeonGreen`
