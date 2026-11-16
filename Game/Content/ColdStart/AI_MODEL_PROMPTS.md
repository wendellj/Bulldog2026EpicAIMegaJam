# AI 3D Model Generation Prompts
## ColdStart Control Components

Use these prompts with [Tripo AI](https://www.tripo3d.ai/) or [Meshy AI](https://www.meshy.ai/).

**Settings:**
- Style: Realistic / PBR
- Topology: Quad mesh
- Poly count: Low-medium (1K-5K)
- Export: FBX or GLB

---

## 1. Toggle Switch with Guard Cover (BPC_ToggleSwitch + BPC_GuardCover)

**Combined version:**
```
Industrial toggle switch with hinged metal guard cover, Apollo spacecraft style.
Worn olive drab painted metal, scratches and paint chips.
Two-position bat handle switch. Guard cover flips up on hinge.
Low poly game asset, separate meshes for guard and switch.
```

**Guard cover only:**
```
Hinged metal switch guard cover, military aircraft style.
Rectangular frame with flip-up lid, piano hinge on one side.
Worn red painted metal with scratches. Low poly game prop.
```

**Toggle switch only:**
```
Industrial toggle switch, SPDT two-position.
Metal bat handle, chrome or brushed steel.
Circular mounting base with hex nut. Submarine control room style.
Low poly game asset.
```

---

## 2. Push Button (BPC_PushButton)

**Large emergency button (50mm):**
```
Large industrial push button, 50mm diameter, emergency stop style.
Chunky mushroom head cap, bright red, backlit translucent plastic.
Heavy duty metal mounting ring, brushed aluminum.
Arcade button proportions. Low poly game prop.
```

**Standard panel button:**
```
Industrial panel mount push button, square bezel.
Illuminated button cap, translucent colored plastic.
Metal faceplate frame, worn brushed steel.
Spacecraft control panel style. Low poly game asset.
```

---

## 3. Circuit Breaker (BPC_PushBreaker)

```
Industrial circuit breaker, push-to-reset type.
Rectangular black plastic body with white toggle button.
Tripped position shows red indicator band.
Panel mount style, electrical cabinet. Low poly game prop.
```

**Alternative - thermal breaker:**
```
Thermal circuit breaker with manual reset button.
Black bakelite housing, round red reset button on top.
Two screw terminals visible on sides.
Vintage submarine electrical panel style. Low poly.
```

---

## 4. Rotary Selector Switch (BPC_RotarySelector)

```
Industrial rotary selector switch, 4-position detented.
Large black knob with white position indicator line.
Chrome metal collar and mounting plate.
Click-stop positions marked 0-1-2-3.
Military equipment style. Low poly game asset.
```

**Alternative - pointer knob:**
```
Rotary switch with pointer knob, aircraft instrument panel style.
Black phenolic knob with engraved white arrow.
Brushed aluminum faceplate with position markings.
6 positions in 60-degree increments. Low poly.
```

---

## 5. Valve Wheel (BPC_ValveWheel)

**Standard handwheel:**
```
Industrial valve handwheel, gate valve style.
Spoked wheel design, 5 spokes, cast iron look.
Worn red or orange painted metal, rust spots and paint chips.
Submarine or ship engine room style. Low poly game prop.
```

**Smaller valve:**
```
Small valve handwheel, brass or bronze material.
Three-spoke design, knurled rim for grip.
Threaded stem visible below wheel.
Steam pipe fitting style. Low poly game asset.
```

---

## 6. Lever (BPC_Lever)

**Throttle lever:**
```
Industrial control lever, single axis throw.
Ball grip handle, black phenolic or bakelite.
Chrome shaft with pivot mount and friction lock.
Ship engine telegraph style. Low poly game prop.
```

**Toggle lever:**
```
Heavy duty toggle lever, two-position with detent.
T-bar handle, cast aluminum, worn finish.
Panel mount base plate with position markings.
Industrial machinery control. Low poly.
```

---

## 7. Analog Gauge (BPC_AnalogGauge)

**Pressure gauge:**
```
Analog pressure gauge, Bourdon tube style.
Round face, 3 inch diameter, white dial with black markings.
Single needle, red zone marking at high end.
Chrome bezel, scratched glass lens.
Industrial steam gauge style. Low poly game asset.
```

**Voltmeter/ammeter:**
```
Analog panel meter, rectangular face.
Moving coil meter with needle indicator.
Scale markings 0-100, green-yellow-red zones.
Bakelite case, vintage electrical equipment style. Low poly.
```

**Neutron flux gauge (specific to reactor):**
```
Analog meter, logarithmic scale nuclear instrument style.
Round black face with white/green scale markings.
Red needle with damping. Chrome bezel ring.
Vintage nuclear control room gauge. Low poly game prop.
```

---

## 8. Indicator Lamp (BPC_IndicatorLamp)

```
Panel mount indicator lamp, industrial style.
Round lens cap, faceted or smooth, translucent colored plastic.
Chrome or brushed metal bezel ring.
Variety pack: red, green, amber, blue, white.
Low poly game asset, simple geometry.
```

**Rectangular indicator:**
```
Rectangular indicator light, annunciator panel style.
Backlit translucent panel with text area.
Metal frame surround, brushed aluminum.
Spacecraft warning light style. Low poly.
```

---

## 9. Additional Props

**Conduit and cable runs:**
```
Industrial electrical conduit, rigid metal.
90-degree elbow fittings, junction boxes.
Weathered gray painted steel, surface rust.
Modular pipe segments. Low poly game props.
```

**Panel mounting plate:**
```
Control panel mounting plate, blank.
Brushed aluminum or painted steel sheet.
Countersunk screw holes in grid pattern.
Slight edge bend for rigidity. Low poly.
```

**Placard/label holder:**
```
Industrial equipment label plate holder.
Small rectangular frame, brushed metal.
Slot for paper label insert.
Riveted mounting style. Low poly game prop.
```

---

## Generation Tips

1. **Generate each control separately** - easier to position in Unreal
2. **Request "separate meshes"** for moving parts (guard hinges, switch handles)
3. **Specify "worn" or "weathered"** - matches Belter aesthetic
4. **Ask for "low poly game asset"** - keeps Quest 3 friendly
5. **Colors:** olive drab, battleship gray, safety orange/red for accents

## Post-Generation

1. Import FBX to `Content/ColdStart/Meshes/Controls/`
2. Check scale (Tripo exports in meters, may need 100x scale in UE)
3. Set up simple collision
4. Apply Megascans metal materials or use generated textures
5. Replace primitives in existing BPC_* Blueprints

---

## Batch Generation Order

Priority for ColdStart MVP (Phases 0-2):

1. **Push Button (50mm emergency)** - Phase 0 interaction
2. **Toggle Switch + Guard** - Phase 1 battery isolation
3. **Circuit Breaker** - Phase 1 emergency bus
4. **Analog Gauge (pressure)** - Phase 2 diagnosis display

Lower priority (Phases 3-6):
5. Valve Wheel
6. Rotary Selector
7. Lever
8. Indicator Lamps (array)
