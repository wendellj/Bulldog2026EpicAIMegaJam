# Feature Request: Support BreakStruct nodes in add_blueprint_node

## Summary

`add_blueprint_node` doesn't support `BreakStruct` (UK2Node_BreakStruct) nodes, which are essential for accessing struct members in Blueprint graphs.

## Use Case

When binding to ISDK's `interactable_state_changed` delegate, the event outputs an `IsdkInteractableStateEvent` struct. To check if `NewState == Select` (to filter actual pokes from other state changes), we need to break the struct to access the `NewState` member.

Currently this requires manual Blueprint editing.

## Steps to Reproduce

```python
blueprint('add_blueprint_node', asset_path='/Game/MyBlueprint', graph_name='EventGraph',
    node_json={
        'type': 'BreakStruct',
        'struct_type': 'IsdkInteractableStateEvent',
        'pos_x': 0,
        'pos_y': 0
    })
```

## Expected Behavior

A UK2Node_BreakStruct node is created that can receive a struct input and output individual member pins.

## Actual Behavior

```
Unknown node type 'BreakStruct'. Supported: CallFunction, Event, CustomEvent,
CastTo, Branch, Sequence, VariableGet, VariableSet, MacroInstance, InputKey, SpawnActor.
```

## Proposed Implementation

Add BreakStruct handling in `CreateBPNodeFromJson()` in MCPythonHelper.cpp:

```cpp
else if (NodeType == TEXT("BreakStruct"))
{
    FString StructTypeName;
    if (!NodeJson->TryGetStringField(TEXT("struct_type"), StructTypeName))
    {
        OutError = TEXT("BreakStruct node missing 'struct_type'.");
        return nullptr;
    }

    // Find the struct type
    UScriptStruct* StructType = FindObject<UScriptStruct>(nullptr, *StructTypeName);
    if (!StructType)
    {
        // Try with /Script/... prefix
        StructType = FindFirstObject<UScriptStruct>(*StructTypeName, EFindFirstObjectOptions::NativeFirst);
    }

    if (!StructType)
    {
        OutError = FString::Printf(TEXT("Struct type '%s' not found."), *StructTypeName);
        return nullptr;
    }

    FGraphNodeCreator<UK2Node_BreakStruct> Creator(*Graph);
    UK2Node_BreakStruct* BreakNode = Creator.CreateNode(false);
    BreakNode->StructType = StructType;
    BreakNode->NodePosX = PosX;
    BreakNode->NodePosY = PosY;
    BreakNode->AllocateDefaultPins();
    Creator.Finalize();
    NewNode = BreakNode;
}
```

Required include:
```cpp
#include "K2Node_BreakStruct.h"
```

## Also Consider

- `MakeStruct` (UK2Node_MakeStruct) - for creating struct instances
- `SetStructMember` / `GetStructMember` nodes

## Environment

- Unreal Engine: 5.8.4
- UnrealMCPython: 2.2.0
