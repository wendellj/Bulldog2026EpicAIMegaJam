# ColdStart Spaceship Aesthetic Implementation Plan

## Goal
Transform the current grey-box ColdStart level into a believable light freighter (MV *Hesperus*) interior using free Fab assets and Megascans materials.

---

## Current State
- 2.7m x 2.7m room with basic color materials (MI_Wall_*, MI_Floor, MI_Ceiling)
- Control components (buttons, switches, breakers) have glow materials
- No custom meshes or PBR textures

---

## Part 1: Assets to Claim/Import from Fab

### Priority 1: Megascans Materials (FREE - just went free Nov 5, 2026)
Access via Fab plugin in UE 5.8 or fab.com

**Surfaces needed:**
| Material Type | Megascans Search Terms | Use Case |
|---------------|------------------------|----------|
| Painted Metal | "painted metal", "industrial paint" | Wall panels, bulkheads |
| Bare Metal | "bare metal", "scratched metal", "aluminum" | Floor plates, trim |
| Grime/Dirt | "grime", "dirt overlay", "grease" | Decals for wear |
| Rust | "rust", "corroded", "oxidized" | Accent areas, pipes |
| Rubber/Gasket | "rubber mat", "industrial floor" | Floor matting |
| Riveted Metal | "riveted", "bolted metal" | Structural panels |

**Recommended specific assets:**
- `Metal Painted Worn` - scratched industrial paint
- `Metal Bare Scratched` - exposed metal areas
- `Metal Floor Plate` - diamond plate flooring
- `Grime Decals` pack - layer on top of base materials
- `Industrial Surface` collection

### Priority 2: Modular SciFi Station (may be in your library)
147 pieces by Martin Milz (Cloud Imperium Games artist)
- Was free until June 16, 2026
- If claimed: modular walls, flooring, structural pieces
- Search your Fab library for "Modular SciFi Station"

### Priority 3: Quaternius Modular Sci-Fi MegaKit (CC0, always free)
- Download from quaternius.com or CGTrader
- 40 modular sci-fi station tiles
- FBX/OBJ format - import directly to UE

### Priority 4: Additional Fab Free Claims (check your library)
Search your Fab library for these (may have been free previously):
- "Sci-Fi Creatures Research Lab" (free Aug-Sep 2026)
- "Modular Sci-Fi Treatment Station Environment" (free until Mar 2026)
- "Sci-Fi Interior Pack"

---

## Part 2: Visual Reference - Belter Aesthetic

The design doc mentions a "light freighter" and the CLAUDE.md notes "Belter aesthetic" - this is the worn, industrial, functional look from The Expanse:

**Key characteristics:**
- Industrial, not sleek
- Visible wear and use
- Practical labeling (stenciled, not holographic)
- Exposed conduits and piping
- Color palette: grey, dark blue, orange/yellow safety markings
- Grime accumulation in corners and seams

**Reference images to search:**
- "The Expanse Rocinante interior"
- "Industrial spaceship interior"
- "Submarine control room" (design doc mentions this)
- "Apollo spacecraft interior" (design doc: control panels)

---

## Part 3: Implementation Steps

### Step 1: Import Megascans Materials (30 min)
1. Open Fab plugin in UE (Window > Fab)
2. Search for and download these material sets:
   - Metal Painted Worn (2-3 variations)
   - Metal Bare Scratched
   - Metal Floor Plate
   - Grime/Dirt decals
3. Materials import to `/Game/Megascans/` by default

### Step 2: Create Master Materials (1 hour)
Create layered master materials that combine:
- Base metal (painted or bare)
- Grime overlay (blend based on vertex color or mask)
- Edge wear (curvature-based)

File: `/Game/ColdStart/Materials/M_BulkheadMaster`

Parameters:
- BaseColor tint
- Roughness multiplier
- Grime amount (0-1)
- Wear intensity

### Step 3: Apply to Walls (30 min)
Replace current MI_Wall_* materials with instances of M_BulkheadMaster:
- North wall: Engineering station - more wear/grime
- East wall: Systems Status - cleaner, control panels
- South wall: Life Support - moisture stains, grime
- West wall: Drone Bay - heavy wear

### Step 4: Floor Treatment (30 min)
- Diamond plate metal in high-traffic center
- Rubber matting near stations (anti-fatigue)
- Grime accumulation at wall edges
- Safety stripe decals at station boundaries

### Step 5: Ceiling (20 min)
- Painted metal panels
- Conduit runs (use modular kit pieces if available)
- Emergency light housings (placeholder geometry)

### Step 6: Trim and Detail (1 hour)
Add modular kit pieces for:
- Wall panel frames/borders
- Floor edge trim
- Corner covers
- Conduit brackets
- Cable runs

### Step 7: Decals and Labels (45 min)
Create/apply:
- Safety warnings (DANGER HIGH VOLTAGE, etc.)
- Station labels (ENGINEERING, SYSTEMS, etc.)
- Equipment placards
- Wear/damage decals at high-touch areas

---

## Part 4: Material Settings for VR/Quest 3

**Performance requirements (from design doc):**
- Forward shading, MSAA 4x
- No Lumen (baked lighting only)
- Texture budget: 1024x1024 tiled for large surfaces

**Material settings:**
```
Shading Model: Default Lit
Blend Mode: Opaque (except decals)
Mobile Material Quality: Check "Fully Rough" where appropriate
Texture Compression: ASTC (Android)
```

**Decals:**
- Use DBuffer decals for grime overlays
- Keep decal count low (< 20 total)
- Bake grime into base textures where possible

---

## Part 5: Lighting Considerations

The design doc specifies 3 lighting scenarios:
1. **Dark (Phase 0):** Only glow stick and starlight
2. **Emergency (Phase 1):** Red strips, low intensity
3. **Main Bus (Phase 5):** Full white overhead

**Material emissive setup:**
- Emergency light strips: Emissive red, driven by parameter
- Indicator panels: Emissive per-station color
- Gauge backlighting: Warm white emissive

All emissive intensities should be parameter-driven for lighting state transitions.

---

## Part 6: File Organization

```
Content/ColdStart/
  Materials/
    M_BulkheadMaster.uasset      (master material)
    MI_Bulkhead_North.uasset     (instances per wall)
    MI_Bulkhead_East.uasset
    MI_Bulkhead_South.uasset
    MI_Bulkhead_West.uasset
    MI_Floor_DiamondPlate.uasset
    MI_Floor_Rubber.uasset
    MI_Ceiling.uasset
    Decals/
      D_Grime_*.uasset
      D_Warning_*.uasset
      D_Label_*.uasset
  Meshes/
    Structural/
      SM_WallPanel_*.uasset
      SM_FloorTrim_*.uasset
      SM_ConduitRun_*.uasset
    Props/
      SM_CableBundle_*.uasset
      SM_EmergencyLight_*.uasset
  Textures/
    (Megascans auto-imports here or /Game/Megascans/)
```

---

## Part 7: Checklist

### Before Starting
- [ ] Open Fab plugin, sign in with Epic account
- [ ] Claim Megascans materials (search "metal", "grime", etc.)
- [ ] Check library for previously claimed modular kits
- [ ] Download Quaternius kit if modular kit not available

### Implementation
- [ ] Import 5-8 Megascans material sets
- [ ] Create M_BulkheadMaster with grime blend
- [ ] Create material instances for each wall
- [ ] Apply floor materials
- [ ] Apply ceiling material
- [ ] Add structural trim meshes (if available)
- [ ] Create and apply decals
- [ ] Set up emissive parameters for lighting states

### Validation
- [ ] Check in VR Preview - materials readable at arm's length
- [ ] Verify texture memory budget (stat memory)
- [ ] Test lighting scenario transitions
- [ ] Confirm no mobile shader errors

---

## Resources

- [Fab - Megascans Free Library](https://fab.com) (free as of Nov 5, 2026)
- [Quaternius Sci-Fi MegaKit](https://quaternius.com) (CC0)
- [Download 140+ free modular sci-fi assets](https://www.cgchannel.com/2026/06/download-140-free-modular-assets-for-building-a-sci-fi-base/)
- [Megascans now free on Fab](https://quixel.com/news/update-megascans-are-going-free-again)

---

## Notes

Another Claude session is currently working on the level. Coordinate before making changes:
- This plan is for reference/planning only
- Actual implementation should wait until the level work is complete
- Material work can be done in parallel without affecting level geometry
