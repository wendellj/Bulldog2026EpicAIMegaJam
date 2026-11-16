# L_CanyonBridge Level Design Document

## Overview

**Level Name:** L_CanyonBridge
**Duration:** 15-30 seconds crossing time
**Theme:** Rickety wooden plank bridge spanning a deep canyon
**Inspiration:** Indiana Jones, Temple of Doom, classic adventure film tension scenes
**Play Space:** Room-scale (2.5m bridge fits within Quest 3 guardian)

---

## Narrative Integration

**Decision: Standalone Level**

This is a separate VR experience with no narrative connection to ColdStart. It exists as its own self-contained tension/atmosphere piece.

**Player Goal:** Simply cross the bridge to reach the other side. No story justification needed - the experience IS the content.

**Menu Integration:** Appears as a separate level in the main menu alongside ColdStart.

---

## Environment Design

### Canyon Geography

```
[Start Platform]  <- solid rock ledge
     |
     |  <- Bridge (2.5m long, room-scale)
     |
[End Platform]    <- solid rock ledge

        v 200+ meters to river below (virtual depth)
```

**Canyon Walls:**
- Dark granite/basalt rock faces
- Sparse vegetation (dead trees, scrub)
- Visible river/stream at bottom (adds depth perception)
- Distant mountains for skybox depth

**Lighting:**
- Overcast sky (diffuse lighting, no harsh shadows)
- Subtle god rays through cloud breaks
- No fog/mist (full visibility to canyon floor)

### Bridge Construction

Based on reference image (no handrails):

```
Top View:
    [slat]  gap  [slat]  gap  [slat]  gap  [slat]
    ===============================================
    ^                                              ^
  Support rail (underneath)            Support rail (underneath)

Side View:
    +====+     +====+     +====+     +====+
    |    |     |    |     |    |     |    |
----+----+-----+----+-----+----+-----+----+----  <- support rails
         v           v           v
      (gaps show canyon 200m below)

Player View:
    Nothing at eye level - just slats and void
```

**Bridge Specifications:**
- **Width:** 0.6m (narrow, nothing to hold onto)
- **Length:** 2.5m (fits within room-scale guardian, ~8 feet)
- **Slat dimensions:**
  - Length (across bridge): 0.6m (spans the bridge width)
  - Width (along walking direction): 15cm / 0.15m
  - Thickness: 2cm / 0.02m
- **Gap between slats:** 0.1m to 1.0m (variable, some very large gaps)
- **Side rails:** NONE (maximum tension, nothing to grab)
- **Support:** Two parallel log rails underneath slats (structural only, not handrails)
- **Rope lashings:** Visible at slat-to-rail joints
- **Slat count:** Variable based on gap distribution

**Bridge Behaviors:**
- Static (no sway, no movement)
- Silent (no creaking, no audio feedback)
- Solid slats (no give when stepped on)
- Some slats visibly cracked/damaged (visual detail only)

---

## VR Comfort Implementation

### Room-Scale Advantage

Pure room-scale walking eliminates most VR comfort concerns:
- **No artificial locomotion** = no motion sickness
- **1:1 movement** = vestibular system matches visual input
- **Physical turning** = natural, no snap-turn needed

### Comfort Through Environment

| Technique | Implementation |
|-----------|----------------|
| **Stable horizon** | Distant mountains/sky stay fixed, no world shake |

No fog, no audio cues. Raw exposure to the void.

### Intentional Discomfort (The Point)

1. **No rails** - Nothing to grab, maximum exposure
2. **Visible gaps** - Canyon depth visible between every slat
3. **Looking down encouraged** - The fear IS the experience
4. **No safety cues** - Player must trust their own balance
5. **Safe return option** - Player can physically turn around and walk back

### Locomotion Method

**Decision: Pure Room-Scale Physical Walking**

The entire bridge fits within the Quest 3 guardian space (~2.7m x 2.7m). Player physically walks the full 2.5m bridge with no artificial locomotion or teleportation.

**Why this works:**
- Zero artificial locomotion = zero motion sickness
- Physical walking maximizes presence/tension
- Player actually feels the narrow width
- 1:1 movement is most comfortable for heights
- Simple implementation, no teleport logic needed

**Physical Space Layout:**
```
Guardian: 2.7m x 2.7m
Bridge:   2.5m long x 0.6m wide (centered in guardian)
Buffer:   0.1m on each end for platforms
```

**Player Movement:**
- Starts on solid platform (physical back of guardian)
- Walks forward across bridge (physical center)
- Arrives at end platform (physical front of guardian)
- Can turn around and walk back if desired

---

## Gameplay Elements

### Phase 0: Approach (10 seconds)
- Player spawns on start platform (solid rock ledge)
- Bridge visible ahead, canyon depth visible below
- Player can look around, see the drop, mentally prepare
- Physical step onto first slat triggers Phase 1

### Phase 1: Crossing (15-20 seconds)
- Player physically walks the 2.5m bridge
- Bridge is static (no sway)
- Silent (no audio)
- Looking down through gaps reveals 200m drop
- Tension peaks at midpoint (center of bridge)

### Phase 2: Arrival (10 seconds)
- Player steps onto end platform (solid rock)
- Solid ground, relief moment
- Panoramic vista reward (mountains, valley)
- Level complete / return to menu

### Optional Hazards (if gameplay > pure atmosphere)

| Hazard | Description | Comfort Rating |
|--------|-------------|----------------|
| Large gaps | 1m gaps require careful step-over | Safe |
| Bird visual | Crow flies up from below (no sound) | Safe |

**Avoid:**
- Any slat breaking (falling sensation = nausea)
- Any camera shake or movement
- Audio of any kind

---

## Technical Implementation

### Asset Requirements

**Meshes:**
| Asset | Source | Notes |
|-------|--------|-------|
| Bridge slats | Procedural or Megascans | Weathered wood planks |
| Log rails | Megascans/Quixel | Rough bark texture |
| Rope | Spline mesh | Hemp/fiber material |
| Rock cliff faces | Megascans | Modular cliff pieces |
| Dead trees | Megascans | Canyon wall decoration |
| River | Plane + scrolling normal | Far below, low detail OK |

**Materials:**
| Material | Type |
|----------|------|
| M_WeatheredWood | PBR, worn grain |
| M_Rope | Subsurface, fiber look |
| M_CanyonRock | PBR, granite/basalt |
| M_DistantWater | Unlit, animated UVs |

**Audio:**
None. Silent experience.

### Blueprint Architecture

```
BP_CanyonBridgeState (singleton, like BP_ShipState)
+-- CurrentPhase (int)
+-- PlayerOnBridge (bool)
+-- OnPhaseChanged (dispatcher)
+-- OnBridgeEvent (dispatcher)

BP_BridgeSlat (instanced per slat)
+-- SlatMesh (StaticMeshComponent)
+-- StepTrigger (BoxCollision)
+-- OnStepped (dispatcher)

BP_BridgeSupport (2 instances, left/right - UNDERNEATH slats, not handrails)
+-- SupportLogMesh (StaticMeshComponent)
+-- RopeLashings[] (StaticMeshComponent at slat joints)

BP_BridgeTriggerZone (start/end platform detection)
+-- StartTrigger (BoxCollision at bridge entrance)
+-- EndTrigger (BoxCollision at bridge exit)
+-- OnBridgeEntered (dispatcher)
+-- OnBridgeExited (dispatcher)
```

### Level Layout

```
World Origin (0, 0, 0) = Center of bridge
Units: centimeters (Unreal default)

Start Platform: (-175, 0, 0) to (-125, 0, 0)  <- 50cm deep
Bridge Start:   (-125, 0, 0)
Bridge End:     (125, 0, 0)                   <- 250cm bridge
End Platform:   (125, 0, 0) to (175, 0, 0)    <- 50cm deep

Canyon floor:   Z = -20000 (200 meters down)
Canyon walls:   Y = +/-300 (3 meters from bridge edges)

PlayerStart:    (-150, 0, 0)  <- On start platform, facing +X
```

**Physical Guardian Mapping:**
- Player's physical "back" = Start platform (X = -175)
- Player's physical "forward" = End platform (X = +175)
- Total physical walk distance: 3.5m (fits 2.7m guardian with margin)

### Performance Budget (Quest 3)

| Metric | Target |
|--------|--------|
| Draw calls | < 150 |
| Triangles | < 500K visible |
| Texture memory | < 512MB |
| Real-time lights | 1 (directional sun) |
| Frame time | < 11ms |

**Optimization strategies:**
- LODs on canyon walls (distance culling)
- Instanced slats (single draw call for all)
- Baked lighting on static geometry
- Unlit/emissive materials for distant details
- Fog hides distant detail pop-in

---

## File Structure

```
Content/CanyonBridge/
+-- Levels/
|   +-- L_CanyonBridge.umap
+-- Blueprints/
|   +-- BP_CanyonBridgeState.uasset
|   +-- BP_BridgeSlat.uasset
|   +-- BP_BridgeSupport.uasset
|   +-- BP_BridgeTriggerZone.uasset
+-- Materials/
|   +-- M_WeatheredWood.uasset
|   +-- M_Rope.uasset
|   +-- M_CanyonRock.uasset
|   +-- M_DistantWater.uasset
+-- Meshes/
|   +-- SM_BridgeSlat.uasset
|   +-- SM_SupportLog.uasset
|   +-- SM_RopeLashing.uasset
|   +-- SM_CliffSection_01-04.uasset
+-- Textures/
    +-- (imported with Megascans materials)
```

---

## Testing Checklist

### Comfort Testing
- [ ] Cross bridge at walking speed - no nausea
- [ ] Look down through gaps - tolerable vertigo (intentional)
- [ ] Physical turn 180 mid-bridge - no disorientation
- [ ] Test with VR-sensitive user - gather feedback

### Functionality Testing
- [ ] Start/end platform triggers fire correctly
- [ ] Phase transitions fire correctly
- [ ] Level complete returns to menu

### Performance Testing
- [ ] Maintains 72fps throughout crossing
- [ ] No frame drops when looking at canyon depth
- [ ] Memory usage stable (no leaks)
- [ ] Load time < 5 seconds

---

## Implementation Priority

### MVP (Day 1)
1. Basic level with static bridge mesh
2. Start/end platforms
3. Simple canyon walls (BSP or basic mesh)
4. Skybox
5. Player can walk across

### Polish (Day 2)
1. Individual slat collision
2. Canyon wall detail (rock textures, dead trees)
3. River at bottom (visual only)
4. Skybox refinement
5. Lighting pass

### Final (Day 3)
1. Material polish (Megascans)
2. Phase logic + level complete screen
3. Main menu integration
4. VR comfort testing
5. QA testing

---

## Decisions Made

| Question | Decision |
|----------|----------|
| Narrative | Standalone level (no ColdStart connection) |
| Locomotion | Pure room-scale physical walking (no teleport) |
| Bridge length | 2.5m (fits guardian, one continuous walk) |
| Handrails | None (maximum tension) |
| Bridge sway | None (static) |
| Audio | None (silent) |
| Fog/mist | None (full visibility to canyon floor) |
| Slat gaps | Variable 10cm to 1m (some require stepping over) |

## Remaining Questions

1. **Hazards** - Pure atmosphere or include scripted dangers (breaking slat, wind gust)?
2. **End goal** - What's on the other side? (Vista view, collectible, door, just completion?)
3. **Replayability** - One-time experience or repeatable from menu?

---

## References

- Reference image: Rickety plank bridge over Black Canyon (user provided)
- Meta VR Comfort Guidelines (vr_docs_search results)
- ColdStart level patterns (existing project architecture)
- Indiana Jones and the Temple of Doom (rope bridge scene)
- Uncharted series (bridge/cliff traversal)
