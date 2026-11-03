#!/usr/bin/env python3
"""
Cleanup Level - Remove Temporary Test Actors
Run this at the start of each session to clean up duplicate/temp actors.
"""
from unreal_helper import actor
import json

print("="*60)
print("LEVEL CLEANUP - REMOVING TEMPORARY ACTORS")
print("="*60)

# Get all actors
all_actors_result = actor('list_all_with_locations')
if not all_actors_result.get('success'):
    print("\n[ERROR] Failed to get actor list")
    print(json.dumps(all_actors_result, indent=2))
    exit(1)

all_actors = all_actors_result.get('actors', [])
print(f"\nTotal actors in level: {len(all_actors)}\n")

# Categories of temp actors to remove
temp_patterns = [
    # Numbered duplicates (Actor_0, Actor_1, etc.)
    '_0', '_1', '_2', '_3', '_4', '_5', '_6', '_7', '_8', '_9',

    # Temp/test prefixes
    'Temp', 'Test', 'Debug', 'Old',

    # Multiple PostProcessVolumes (keep only one)
    'PostProcessVolume2', 'PostProcessVolume3', 'PostProcessVolume4',

    # VR pawn duplicates (keep VRPawn_HandTracking that's type Pawn, not DefaultPawn)
    # Will handle this separately
]

# Keep track of what we delete
deleted = []
kept = []

# Special handling for VRPawn_HandTracking duplicates
vr_pawns = [a for a in all_actors if 'VRPawn' in a['name']]
if len(vr_pawns) > 1:
    print("Multiple VR Pawns found:")
    for vp in vr_pawns:
        print(f"  - {vp['name']} at {vp['location']}")

    # Delete all but the first one (assuming it's the correct one)
    for i, vp in enumerate(vr_pawns):
        if i > 0:  # Keep first, delete rest
            print(f"\n  Deleting duplicate: {vp['name']}")
            result = actor('delete_by_label', actor_label=vp['name'])
            if result.get('success'):
                deleted.append(vp['name'])
                print(f"    OK")
            else:
                print(f"    Failed: {result.get('message')}")

# Delete actors matching temp patterns
print("\nScanning for temporary actors...")
for a in all_actors:
    name = a['name']

    # Skip if already deleted
    if name in deleted:
        continue

    # Check if matches any temp pattern
    should_delete = False
    for pattern in temp_patterns:
        if pattern in name:
            should_delete = True
            break

    if should_delete:
        print(f"  Deleting: {name}")
        result = actor('delete_by_label', actor_label=name)
        if result.get('success'):
            deleted.append(name)
            print(f"    OK")
        else:
            print(f"    Failed: {result.get('message')}")
    else:
        kept.append(name)

# Summary
print("\n" + "="*60)
print("CLEANUP SUMMARY")
print("="*60)
print(f"\nActors deleted: {len(deleted)}")
if deleted:
    for name in deleted:
        print(f"  - {name}")

print(f"\nActors kept: {len(kept)}")
print("\nLevel is now clean!")
print("="*60)

# Verification - list remaining actors
print("\nREMAINING ACTORS:")
remaining_result = actor('list_all_with_locations')
if remaining_result.get('success'):
    remaining = remaining_result.get('actors', [])
    for a in remaining:
        print(f"  - {a['name']} at {a['location']}")
    print(f"\nTotal: {len(remaining)} actors")
else:
    print("[ERROR] Could not verify remaining actors")

print("\n" + "="*60)
print("CLEANUP COMPLETE")
print("="*60)
