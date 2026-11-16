# Bug: `pin_defaults` doesn't work for object reference pins

## Summary

The `pin_defaults` feature in `add_blueprint_node` fails to properly set default values for object reference pins (Sound, Material, Texture, etc.). It sets a string path to `Pin->DefaultValue`, but object pins require `Pin->DefaultObject` with a loaded UObject.

## Steps to Reproduce

```python
blueprint('add_blueprint_node', asset_path='/Game/MyBlueprint', graph_name='EventGraph',
    node_json={
        'type': 'CallFunction',
        'function_name': 'PlaySound2D',
        'target': 'GameplayStatics',
        'pos_x': 400,
        'pos_y': 576,
        'pin_defaults': {
            'Sound': '/Game/Audio/MySound.MySound'  # This fails
        }
    })
```

## Expected Behavior

The `Sound` pin should have `MySound` asset assigned as its default object.

## Actual Behavior

The pin gets an invalid string value. Compilation fails with:
```
The current value (/Game/Audio/MySound.MySound) of the 'Sound' pin is invalid:
String NewDefaultValue '/Game/Audio/MySound.MySound' specified on object pin 'Sound'
```

## Root Cause

`MCPythonHelper.cpp` line 670 unconditionally sets `Pin->DefaultValue` for all pin types:

```cpp
// Set pin defaults if specified
if (NewNode && NodeJson->HasField(TEXT("pin_defaults")))
{
    const TSharedPtr<FJsonObject>& PinDefaults = NodeJson->GetObjectField(TEXT("pin_defaults"));
    for (auto& Pair : PinDefaults->Values)
    {
        UEdGraphPin* Pin = FindPinByName(NewNode, FString(*Pair.Key), EGPD_Input);
        if (Pin)
        {
            FString Value;
            if (Pair.Value->TryGetString(Value))
            {
                Pin->DefaultValue = Value;  // BUG: Wrong for object pins
            }
        }
    }
}
```

## Proposed Fix

Check pin category and use `DefaultObject` for object reference types:

```cpp
// Set pin defaults if specified
if (NewNode && NodeJson->HasField(TEXT("pin_defaults")))
{
    const TSharedPtr<FJsonObject>& PinDefaults = NodeJson->GetObjectField(TEXT("pin_defaults"));
    for (auto& Pair : PinDefaults->Values)
    {
        UEdGraphPin* Pin = FindPinByName(NewNode, FString(*Pair.Key), EGPD_Input);
        if (Pin)
        {
            FString Value;
            if (Pair.Value->TryGetString(Value))
            {
                // Check if this is an object reference pin
                if (Pin->PinType.PinCategory == UEdGraphSchema_K2::PC_Object ||
                    Pin->PinType.PinCategory == UEdGraphSchema_K2::PC_Class ||
                    Pin->PinType.PinCategory == UEdGraphSchema_K2::PC_SoftObject ||
                    Pin->PinType.PinCategory == UEdGraphSchema_K2::PC_SoftClass ||
                    Pin->PinType.PinCategory == UEdGraphSchema_K2::PC_Interface)
                {
                    // Load the asset and set DefaultObject
                    UObject* Asset = StaticLoadObject(UObject::StaticClass(), nullptr, *Value);
                    if (Asset)
                    {
                        Pin->DefaultObject = Asset;
                    }
                    else
                    {
                        UE_LOG(LogTemp, Warning, TEXT("pin_defaults: Failed to load asset '%s' for pin '%s'"), *Value, *Pin->GetName());
                    }
                }
                else
                {
                    // For non-object pins, use string value as before
                    Pin->DefaultValue = Value;
                }
            }
        }
    }
}
```

## Affected Pin Types

| Pin Category | Example Pins | Status |
|--------------|--------------|--------|
| `PC_Object` | Sound, Material, Texture, StaticMesh | **Broken** |
| `PC_Class` | Class reference pins | **Broken** |
| `PC_SoftObject` | Soft object references | **Broken** |
| `PC_SoftClass` | Soft class references | **Broken** |
| `PC_Interface` | Interface references | **Broken** |
| `PC_Int`, `PC_Float`, `PC_Boolean`, `PC_String`, `PC_Byte`, `PC_Enum` | Primitive pins | Working |

## Workaround

Set object reference pins manually in the Blueprint editor using the dropdown or drag-drop from Content Browser.

## Environment

- Unreal Engine: 5.8.4
- UnrealMCPython: 2.2.0
- Platform: Windows
