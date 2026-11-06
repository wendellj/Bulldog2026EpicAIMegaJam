# COLD START
## Design & Implementation Document
### Room-Scale VR — Unreal Engine 5.8.3

**Working title:** COLD START
**Vessel:** MV *Hesperus*, light freighter
**Platform:** Meta Quest 3 — native standalone build (Android)
**Input:** Hand tracking only. No controllers. See Part 5.6.
**Engine:** Unreal Engine 5.8.3, Blueprint-first
**Play space:** 10ft × 10ft (3.05m × 3.05m) room scale
**Scope:** Scenario 1 of a planned series. 25–40 minutes.

---

## HOW TO USE THIS DOCUMENT

Paste this entire document into a new Claude conversation. It contains the design, system specs, asset sources, and a sequenced prompt list for building the first playable scenario. Work the prompts in order — later systems depend on earlier ones.

This is an original hard-science-fiction setting. All vessel names, systems terminology, and designs here are original. Keep them that way — the genre conventions are free to use, specific expression from existing franchises is not.

---

## PART 1 — PREMISE

### The scenario

You wake on the bridge of a freighter that has been dark for an unknown period. The reactor is cold. The lights are out. Your emergency mask has roughly twenty-five minutes of air, and the cabin is losing heat.

Nothing is attacking you. The antagonist is thermodynamics and a dependency chain you have to solve in the right order.

You restore the ship, system by system, from battery power up to main bus. Each system you bring online unlocks the diagnostics you need for the next. One critical breaker sits in an unpressurized conduit you cannot reach — so you learn to pilot a drone, which becomes the core mechanic of every scenario that follows.

### Why this scenario first

It teaches everything without teaching anything explicitly:

- Physical controls, by making you find them in the dark
- The dependency logic the whole ship runs on
- Drone piloting, as the only solution to an unreachable problem
- Reading instruments instead of reading UI
- Working under time pressure without combat

### Design pillars

1. **Competence pressure, not threat pressure.** The tension comes from a clock and a problem, never from something hunting you. This is the hardest sci-fi tone to get right and the most underserved in VR.
2. **Physical controls beat screens.** Toggles under covers, rotary selectors, valve wheels, breakers. If a player can grab it, grab it.
3. **The ship explains itself.** No tutorial text. Placards, labels, schematics on the bulkhead, and a procedures binder you can physically pick up and read.
4. **Darkness is the first antagonist.** You carry your own light for the first ten minutes. It shapes everything about how the room reads.
5. **Failure is setback, not death.** Running out of air means you black out and wake with less margin, not a game over screen.

---

## PART 2 — THE PLAY SPACE

### Physical versus virtual dimensions

```
Physical guardian:   3.05m × 3.05m  (10ft × 10ft)
Virtual compartment: 2.70m × 2.70m
Safety margin:       ~17cm on each side
```

The virtual bridge is **deliberately smaller than the physical room.** The player should be able to touch every bulkhead without approaching their guardian. Never design an interaction that requires reaching past a virtual wall.

**Ceiling:** 2.3m virtual. Low enough to feel like a working vessel, high enough that tall players don't clip.

### Station layout

Four stations, one per bulkhead. Player stands center, turns and takes one or two steps to reach any of them.

```
                    NORTH
        ┌─────────────────────────────┐
        │   ENGINEERING / REACTOR     │
        │   rod controls, scram,      │
        │   flux gauges, temp         │
        │                             │
   W    │                             │    E
   E    │                             │    A
   S    │          [PLAYER]           │    S
   T    │                             │    T
        │                             │
  DRONE │                             │ SYSTEMS
  BAY   │                             │ STATUS
  hatch │                             │ main console
  conduit access                      │ fault tree
        │                             │
        │   LIFE SUPPORT / FLUIDS     │
        │   valve wheels, pumps,      │
        │   pressure gauges, scrubber │
        └─────────────────────────────┘
                    SOUTH
```

**North — Engineering.** Reactor control. Rod position selectors, neutron flux gauge, coolant temperature, the scram handle under a guarded cover.

**East — Systems Status.** The main console. Fault tree display, bus status board, breaker panel, the drone feed screen.

**South — Life Support and Fluids.** Coolant loop valve wheels, pump switches, pressure gauges, atmospheric scrubber controls.

**West — Drone Bay and Conduit Access.** A hatch at knee height leading to the conduit run. Drone docking cradle, charge indicator, deployment lever.

### Interaction height rules

```
Primary controls:        0.9m – 1.4m  (comfortable standing reach)
Secondary / infrequent:  0.6m – 1.7m
Never place below:       0.4m  (requires deep crouch)
Never place above:       1.9m  (excludes shorter players)
```

Add a **height calibration** at session start. Capture standing eye height, scale console placement by a factor derived from it. A 1.6m player and a 1.9m player must both reach everything comfortably.

---

## PART 3 — THE DEPENDENCY CHAIN

This is the game. Six phases, each gated by the previous one.

### Phase 0 — The cold open

**Starting state:** total darkness. Silence except your own breathing inside the mask. No glow stick yet — it's clipped to your harness and you haven't found it.

**Beat 1 — the call.** After four to six seconds of nothing, a single red backlit button illuminates on the far bulkhead, directly across the compartment. It bleeps once, then begins a slow blink with a matching tone. The small monitor above it lights with the fault:

```
ENV-04   CO2 SCRUBBER — FAULT
         PRESS RESET
```

It is the only light and the only sound in the ship.

**Beat 2 — the crossing.** The player walks to it. This is their first physical traverse of the room, roughly two and a half meters, and it teaches room-scale locomotion without a word of instruction. The blinking light is the only thing they can see, so there is nothing else to do.

**Beat 3 — the press.** The button is a 50mm square industrial pushbutton — chunky, backlit, findable by touch alone. It depresses with real travel and a heavy mechanical clunk. Strong haptic.

**Beat 4 — the failure.** The light goes solid amber for half a second. The tone stops. In that silence, the monitor updates:

```
ENV-04   CO2 SCRUBBER — FAULT
         RESET FAILED — NO MAIN BUS
         SEE SYSTEMS STATUS
```

Then the button returns to blinking red, and the tone resumes.

**What this accomplishes:**

- The player acts within thirty seconds, with no tutorial and no prompt
- They learn that controls are physical, satisfying, and responsive
- They learn the ship answers them
- They learn there is a dependency they don't yet understand
- They are pointed at the Systems Status console, which is Phase 2
- **They now want something specific.** Not abstract survival — they want to press that button and have it work.

**Why the button has power at all:** the environmental alarm circuit runs off a small dedicated backup cell, separate from the main battery bank. Real vessels isolate life-support alarms this way. It's why one thing in a dead ship is awake, and the procedures binder says so if anyone checks.

**Audio note:** the bleep is the only sound in the game until Phase 1. When the failed press silences it for half a second, that silence is the loudest moment in the scenario. Do not undercut it with anything else.

**The structural payoff:** the first thing the player sees is the last thing they do. Phase 6 is returning to this exact button and pressing it again. The entire scenario is the distance between those two presses.

**Expected duration:** 30–60 seconds.

---

### Phase 1 — Emergency power

**Starting state:** total darkness except a chemical glow stick clipped to your harness and faint starlight through the viewport.

**Required actions:**
1. Locate the battery isolation switch, West bulkhead, under a hinged red cover
2. Lift cover, throw switch
3. Locate emergency bus breaker on the East panel, push to reset

**Result:** red emergency lighting at roughly 10% intensity. The Systems Status console boots.

**Teaching:** covers must be lifted before switches throw. Breakers push rather than flip. The ship has physical controls, not screens.

**Expected duration:** 3–6 minutes, most of it spent searching in the dark.

---

### Phase 2 — Diagnosis

**Required actions:**
1. Read the fault tree on the Systems Status console
2. Identify three faults: reactor offline, coolant loop depressurized, breaker C-7 tripped
3. Find the schematic placard on the West bulkhead showing C-7's location inside the conduit run

**Result:** the player knows what to do and knows one part of it is physically unreachable.

**Teaching:** the console reports, it doesn't act. Information lives in the world — on placards, in the binder, on gauges.

**Expected duration:** 2–4 minutes.

---

### Phase 3 — The drone

**Required actions:**
1. Open the conduit hatch, West bulkhead, knee height — requires a crouch
2. Release the drone from its cradle
3. Place the drone in the conduit mouth
4. Return to Systems Status, switch the screen to drone feed
5. Pilot the drone through the conduit using the console's two-axis controller
6. Locate and reset breaker C-7 with the drone's manipulator

**Result:** coolant pump circuit energized.

**Teaching:** this is the core loop of the entire game. Deploy physically, pilot remotely, act at distance, retrieve.

**Design notes:**
- The conduit run should be short for this first use — roughly 15 virtual meters with two turns
- Drone feed is monochrome, low resolution, with visible noise
- Drone has a small forward light with a narrow cone
- No fail state — the drone can bump walls and get stuck, but reversing always works
- Drone battery is generous here, tight in later scenarios

**Expected duration:** 5–8 minutes.

---

### Phase 4 — Prime the coolant loop

**Required actions:**
1. Open the main coolant isolation valve — a wheel requiring several physical rotations
2. Open the return valve
3. Start the circulation pump
4. Watch the pressure gauge rise to nominal band
5. If the pump was started before both valves opened, it cavitates — bleed the line and retry

**Result:** coolant loop at pressure, reactor startup permitted.

**Teaching:** order matters. Gauges tell you the truth. The game will let you do it wrong and show you why it was wrong.

**Design note:** the valve wheel should take genuine physical effort — three to four full hand rotations with haptic detents. This is the most tactile interaction in the scenario and it should feel like work.

**Expected duration:** 4–7 minutes.

---

### Phase 5 — Reactor start

**Required actions:**
1. Confirm coolant pressure and flow on the North panel
2. Withdraw control rods in sequence using the position selectors — three banks, withdrawn in a specified order found in the procedures binder
3. Monitor neutron flux as it climbs
4. If flux rises too fast, the automatic scram trips and you restart from rods fully inserted
5. Hold at criticality, then advance to power

**Result:** main bus live. White lighting comes up. The ship hums.

**Teaching:** the most demanding instrument-reading task in the scenario. Rewards patience, punishes rushing. This is the moment the player feels like an engineer.

**Design notes:**
- Flux gauge is analog, with a redline
- Rod withdrawal is three selectors, each with detented positions
- The correct sequence is in the binder, not on screen
- A scram costs roughly 90 seconds of redo — frustrating but not punishing

**Expected duration:** 6–10 minutes including at least one scram.

---

### Phase 6 — Life support

**Required actions:**
1. Energize the environmental bus from the East breaker panel
2. Start the CO₂ scrubber from the South station
3. Bring cabin heaters online
4. Watch cabin pressure and temperature climb to nominal
5. **Return to the button on the West bulkhead and press it again**
6. Remove the emergency mask

**Result:** scenario complete. The air timer ends. Full white lighting. The ship hums.

**The closing beat.** The button has been blinking red for the entire scenario — in the player's peripheral vision at every station, through every scram and every cavitation retry. It is the one constant.

This time the press lands differently:

```
ENV-04   CO2 SCRUBBER — ONLINE
```

Solid green. The tone stops and does not resume. Somewhere behind the bulkhead a fan spins up — the sound builds over about four seconds and settles into a steady hum.

Hold there. Let the player stand in the silence-that-isn't-silence for a moment before anything else happens. Then the mask comes off.

**Teaching:** resolution. The payoff for everything prior, delivered at the exact object that started it.

**Design note:** do not gate mask removal behind a prompt. Once cabin O₂ crosses the threshold, the mask becomes grabbable and the player works it out. Someone who keeps it on for another minute has lost nothing.

**Expected duration:** 2–4 minutes.

---

## PART 4 — PRESSURE SYSTEMS

### The air timer

```
Starting supply:    25 minutes
Displayed on:       wrist gauge (diegetic, analog needle)
Audio:              breathing in the mask, audible throughout
                    rate increases below 8 minutes
Visual:             mask edge vignette, faint
                    HUD-free — no screen overlay, ever
```

**Below 5 minutes:** breathing becomes laboured, vision edges darken slightly.

**At zero:** the player blacks out. Screen fades. They wake at the same position with the cabin 6°C colder, the air timer reset to 15 minutes from a reserve bottle, and any completed phases still completed.

This is a **setback, not a failure.** It costs margin, not progress. Three blackouts and the scenario ends with a survival-but-barely outcome rather than a game over.

### Cabin temperature

A secondary, slower clock. Starts at 4°C and drops roughly 0.5°C per minute until heaters come online.

**Effects by threshold:**
```
Below 0°C:   visible breath vapor
Below -5°C:  hand tremor on fine controls — slight input jitter
Below -10°C: valve wheels require more rotations (stiff grease)
```

Never lethal within the scenario's length. It exists to make you feel the ship fighting you.

---

## PART 5 — SYSTEM SPECIFICATIONS

### 5.1 — Ship State Subsystem

**Class:** `UShipStateSubsystem` — World Subsystem

Single source of truth for every ship system. All consoles, gauges, and lights read from it. Nothing holds its own state.

```
Tracked state:
  BatteryBusLive          bool
  EmergencyBusLive        bool
  MainBusLive             bool
  EnvironmentalBusLive    bool

  BreakerC7Reset          bool
  CoolantValveMain        float 0.0–1.0
  CoolantValveReturn      float 0.0–1.0
  CoolantPumpRunning      bool
  CoolantPressure         float  kPa
  CoolantFlow             float  L/min

  RodBankA/B/C            int 0–10 (withdrawal position)
  NeutronFlux             float
  ReactorTemp             float  °C
  ReactorScrammed         bool
  ReactorPower            float 0.0–1.0

  ScrubberRunning         bool
  HeatersRunning          bool
  CabinPressure           float  kPa
  CabinTemp               float  °C
  CabinO2                 float  %

  SuitAirRemaining        float  seconds
  BlackoutCount           int
```

**Events dispatched:**
```
OnBusStateChanged(EBusType, bool Live)
OnPhaseCompleted(int PhaseIndex)
OnReactorScram()
OnCavitation()
OnBlackout()
```

**Tick:** disabled. Runs on a 0.25s timer for physical simulation (pressure, temperature, flux), event-driven for everything else.

### 5.2 — Physical control components

Build these once, reuse everywhere. Each is an Actor Component attached to a mesh.

| Component | Behavior |
|---|---|
| `BPC_ToggleSwitch` | Two-position, haptic click, optional guard cover |
| `BPC_GuardCover` | Hinged, must be lifted before the switch beneath responds |
| `BPC_PushBreaker` | Press to reset, pops out when tripped, visible state |
| `BPC_RotarySelector` | Detented positions, haptic per detent, N positions |
| `BPC_ValveWheel` | Continuous rotation, tracks cumulative turns, resistance curve |
| `BPC_Lever` | Single-axis throw, spring return optional |
| `BPC_AnalogGauge` | Needle driven by a float, with redline band |
| `BPC_IndicatorLamp` | On/off/flashing, emissive material driven |

**Feedback without haptics.** There are no controllers, so there is nothing to vibrate. Every control's response must be carried by audio and visual channels instead. See Part 5.6 for the full specification — but as a rule for every component above: the sound fires on physical contact, not on state change, and the rendered hand visibly reacts to the surface.

### 5.3 — Drone system

**Drone actor:** `BP_MaintenanceDrone`

```
Movement:     two-axis (forward/back, yaw) plus vertical
Speed:        0.4 m/s — deliberately slow
Camera:       forward-facing, 60° FOV, renders to RT_DroneFeed
Light:        spot, 25° cone, 3m range
Manipulator:  single actuator, interacts with BPC_PushBreaker only in Scenario 1
Battery:      8 minutes in Scenario 1 (generous), tighter later
```

**Feed rendering — the single largest performance risk on Quest 3:**

A render target is a second full scene render. On mobile hardware this is the most expensive thing in the project by a wide margin.

```
Render Target resolution:  320 × 240
Update rate:               12 fps (every 6th frame at 72fps)
Camera:                    no post-process volume, no shadows,
                           no reflections, Unlit or Mobile Default lit
Only renders when:         the console is displaying drone feed
                           AND the player is within 2m
                           AND the console is in the player's view frustum
Otherwise:                 freeze the last frame, stop rendering entirely
```

**Degradation happens in the display material, not the camera.** Scanlines, noise, monochrome conversion, and dropout frames are all cheap operations in the material that samples the render target onto the console screen mesh. Doing them as a post-process pass on the second camera roughly doubles the cost for identical visual results.

**The conduit must be geometrically trivial.** Budget under 2,000 triangles for the entire conduit interior, unlit or single-bounce lit, with one unshadowed spot light on the drone. The whole point of putting the breaker somewhere unreachable is that the unreachable place costs almost nothing to render.

The low resolution and noise are not compromises. A clean feed looks like a video game. A degraded feed looks like a real remote camera, and it hides every rendering shortcut you take.

**Control interface:** a two-axis controller physically mounted on the Systems Status console. The player grabs it. No thumbstick-on-controller abstraction — they operate a physical stick that operates the drone.

### 5.4 — Lighting states

Lighting is the primary feedback channel for progress. The player should be able to tell what phase they're in with their eyes closed, then opened.

**On Quest 3 native, all lighting is baked.** Lumen is not available. The phase transitions are achieved through **Lighting Scenarios** — Unreal's feature for baking multiple lighting states into separate sublevels and swapping them at runtime.

```
Scenario A (dark):      no artificial light baked
                        glow stick on harness — the one dynamic light
                        starlight through viewport, very dim blue

Scenario B (emergency): red emergency strips baked at low intensity
                        swapped in at Phase 1

Scenario C (main bus):  white overhead baked at full
                        swapped in at Phase 5
```

**Three scenarios, not four.** Each scenario stores its own lightmap set, so memory cost scales linearly. Phase 6's "full brightness" is achieved by raising emissive intensities and enabling additional emissive accents on Scenario C, not by baking a fourth set.

**Emissive materials do the heavy lifting.** Indicator lamps, gauge faces, console backlighting, and warning strips are all emissive and change freely at runtime with no lightmap involvement. In a dark room these read enormously and cost essentially nothing. Most of the moment-to-moment lighting feedback — a lamp coming on, a gauge backlighting — happens here rather than in the baked scenarios.

**Dynamic lights budget: one.** The player's glow stick in Phase 0, and the drone's spot light while the feed is rendering. Never both at full cost simultaneously — the glow stick can drop to an unshadowed point light once emergency lighting is up.

**Lightmap resolution:** keep modest. The compartment is small, which helps, but three scenarios means three lightmap sets resident. Budget accordingly and bake at the lowest resolution that doesn't produce visible blotching on the bulkheads.

### 5.5 — The procedures binder

A physical object on the Systems Status console. Grabbable, with turnable pages.

Contains the reactor startup rod sequence, the coolant priming order, and a conduit schematic. **This is the only place the correct sequences appear.** No UI, no hints, no quest marker.

Implementation: a mesh with a page-turn animation, pages as textures on a render target or as swapped materials. Eight pages is sufficient.

This single object carries most of the game's tutorial load and it does it diegetically.

---

### 5.6 — Hand tracking (no controllers)

**This game uses hand tracking exclusively. There are no controllers, and there is no controller fallback.**

The design supports this unusually well because the room-scale constraint already removed everything hand tracking is bad at. No thumbstick locomotion, no snap turn, no teleport ray. Every interaction in the game is reach-and-manipulate, which is what hands do best.

#### Configuration

```
OVRManager → Hand Tracking Support:  Hands Only
                                     (NOT "Controllers And Hands" —
                                      mixed mode adds code paths
                                      this project never uses)
Hand skeleton:   26 joints per hand via OpenXR,
                 OVRHand / OVRSkeleton for pinch strength
                 and confidence values
```

#### Interaction verbs

| Verb | Hand pose | Used for |
|---|---|---|
| **Poke** | Index extended | Pushbuttons, breakers, the Phase 0 button |
| **Pinch** | Thumb + index | Small toggles, binder pages, glow stick |
| **Grab** | Full hand close | Levers, valve wheels, the drone, the mask |
| **Two-hand grab** | Both hands | Valve wheels (preferred), drone controller |

#### Replacing haptics

With no controller there is no vibration. Rebuild the feedback in two channels.

**Audio is load-bearing.** Every control gets a distinct sound, triggered on *physical contact* rather than on state change, so it fires the instant the finger touches rather than when the action completes.

```
Toggle switch     sharp click, two different pitches for on/off
Push breaker      heavy mechanical thunk with a slight ring
Rotary selector   detent tick per position, same sample pitched
Valve wheel       continuous scrape loop, pitch and volume
                  follow angular velocity, stops dead on release
Guard cover       hinge squeak on lift, light clack on close
Lever             spring tension rising, hard stop at travel end
```

**The hand must visibly react.** On contact, the rendered hand stops at the surface rather than passing through. Fingers pose to the control — wrapping the valve wheel, flattening against a panel, index curling onto a button.

**Cap the divergence.** If the player's real hand pushes more than roughly 4cm past the virtual surface, break contact and snap the rendered hand back to the real position. A rendered hand stretched far from the real one is deeply uncomfortable. Snapping is less bad than stretching.

#### Hit volumes

Fingertip tracking carries real jitter. Every interactive volume is larger than its visible mesh.

```
Visible mesh        Trigger volume
50mm button    →    70mm sphere
Toggle switch  →    40mm sphere around the bat handle
Valve wheel    →    full rim torus + 20mm
Breaker        →    50mm box
```

#### Destructive actions need two steps

A tracking glitch that scrams the reactor at minute eighteen is a worse experience than a controller misclick, because the player will not believe it was their fault.

- **Scram handle** — already under a guard cover. The cover is the confirmation.
- **Rod bank selectors** — require a deliberate grab-and-hold of at least 0.3s, not a brush. Rotation only registers while held.
- **Battery isolation** — guard cover.
- **Pump start** — no confirmation needed. Getting it wrong causes cavitation, which is a teaching moment, not a loss.

#### Tracking loss

Design for dropout, not just jitter. Hands occlude each other, leave the camera frustum when reaching low or behind, and degrade when the player's **real room** is dimly lit.

```
Confidence high      normal rendering and interaction
Confidence low       hand renders at 50% opacity
Confidence lost      fade hand out over 0.2s
                     release any held control gracefully
                     valve wheel holds its position, does not spin
                     grabbed objects return to their cradle
```

**Never freeze a hand mid-air.** A ghost hand stuck on a valve is worse than no hand.

#### Real-room lighting prompt

The virtual darkness in Phase 0 does not affect tracking — the cameras see the player's actual room. But a dark living room does.

Before the headset goes dark, show a brief setup prompt asking the player to ensure their physical space is adequately lit. This is the one piece of non-diegetic text permitted in the project, and it belongs in the pre-session flow, not in the scenario.

#### Where hands beat controllers

Worth leaning into rather than merely accommodating:

- **The valve wheel.** Two hands on a rim, turning, with the scrape loop responding to velocity. Bimanual coordination sells this in a way a controller grip never does. This should be the most satisfying thirty seconds in the scenario.
- **The guard covers.** Pinching a hinged cover and lifting it is a small, precise, real-feeling motion.
- **The binder.** Pinching and turning a page.
- **The 50mm button.** Pressing a chunky industrial button with one finger is exactly what a finger is for.

#### Plugin caution

**Verify VRExpansion works with hand tracking on a Quest build before committing the control kit to it.** VRExpansion is controller-centric by heritage. If it fights hand tracking, Meta's own interaction components are the better foundation for a hands-only project — and discovering that after twelve interaction components are built on top of it is expensive.

Test this in Phase 1, not Phase 3.

---

## PART 6 — ASSETS

### Always free

| Source | Use |
|---|---|
| **Quixel Megascans** (Fab, permanently free) | Every surface. Scuffed metal, grime, painted steel, rust. Player is inches from these. |
| **NASA 3D Resources** (nasa3d.arc.nasa.gov) | Public domain spacecraft hardware, panel reference, authentic console density |
| **Quaternius Modular Sci-Fi MegaKit** (CC0) | Bulkhead panels, structural pieces |
| **Kenney Modular Space Kit** (CC0) | Blockout only |
| **Poly Haven / ambientCG** (CC0) | HDRI starfield, additional PBR materials |
| **Freesound** | Machinery, hum, hiss, mechanical clunks — verify per-file licenses |

### Epic samples

- **Stack O Bot** — repurpose the robot as the maintenance drone. Already rigged, saves modeling and animating the thing the game revolves around.
- **Content Examples** — render target reference

### Fab rotating free content

Epic releases limited-time free packs on roughly a two-week cycle and sci-fi recurs often. **Claim everything sci-fi whether or not you need it yet — once claimed, it's permanently yours.** Packs listing UE 4.27+ import fine into 5.8.

### Build yourself

The free packs give you bulkheads and pipes. They will not give you the thing that makes this game work: **physical controls.**

Model a kit of roughly a dozen pieces — toggle switch, guard cover, push breaker, rotary selector, valve wheel, lever, gauge bezel, indicator lamp, placard blank, conduit hatch. Every console in the game assembles from these.

Apollo-era panel photography is public domain and the best available reference for high-density physical controls.

### Reference material

- Fleet Type Submarine manuals (NAVPERS 16160) — public domain, exhaustive system detail
- Apollo flight documentation — public domain
- Museum ships: USS Pampanito, USS Cod, USS Midway. Photogrammetry-friendly, authentic control density.

---

## PART 7 — TECHNICAL SPECIFICATION

### Engine configuration — Quest 3 native

```
Unreal Engine 5.8.3
Template: VR Template
Build target: Android (arm64), OpenXR + Meta XR plugin

Rendering path:     Forward Shading (NOT deferred)
Anti-aliasing:      MSAA 4x (NOT TAA — ghosts badly in VR)
Global Illumination: Baked only — Lumen is NOT available
Geometry:           Standard static meshes with LODs
                    Nanite is NOT supported on Quest
Shadows:            Baked. Virtual Shadow Maps NOT available.
                    One unshadowed dynamic light maximum.
Reflections:        Reflection Captures (baked). No screen-space.
Textures:           ASTC compression, mandatory
Stereo:             Mobile Multiview enabled
Foveation:          Fixed Foveated Rendering, level 2–3
World Partition:    DISABLED (single compartment)
Mobile HDR:         Disabled unless a specific effect requires it
```

**Mobile renderer settings to verify in Project Settings:**
```
Mobile Shading:                 Forward
Mobile Anti-Aliasing:           MSAA
Mobile MSAA Sample Count:       4x
Support Mobile Multiview:       true
Mobile Static Branch Shader:    true (reduces permutations)
Allow Static Lighting:          true (required for baked)
```

### Plugins

```
VR Template (built in)
Meta XR Plugin (OVRPlugin)
VRExpansion Plugin (free, open source — verify Quest build compatibility)
Enhanced Input
Niagara (sparingly — GPU particles only)
MetaSounds
Modeling Tools Editor
```

A note on VRExpansion: it is excellent and it is heavier than the stock VR Template. Verify it packages and performs on-device early rather than after the control kit is built on top of it.

### VR specifics

```
Tracking origin:    Floor level
Target framerate:   72fps (set in OVRManager; 90 only if you have headroom)
Locomotion:         NONE. Physical room scale only.
Turning:            NONE. Physical turning only.
Comfort options:    Not required — no artificial motion exists
Height calibration: Mandatory at session start
Passthrough:        Available if desired for boundary warnings
```

**There is no locomotion system in this game.** That is the single biggest design advantage of the room-scale constraint and it should be defended. If a later scenario needs the player elsewhere, move the player via an in-fiction transition (a hatch, a fade, a lift) rather than adding a thumbstick.

### Performance budget — Quest 3 native

```
Framerate:              72fps mandatory, no drops
GPU frame time:         < 11ms (target, leaves headroom from 13.8ms)
CPU frame time:         < 11ms
Draw calls:             < 200
Triangles visible:      < 500,000
Texture memory:         < 1.5 GB
Total app memory:       < 3.5 GB
Dynamic lights:         1 maximum
Render targets:         1, at 320×240, 12fps, conditionally rendered
Audio voices:           < 16 simultaneous, pooled
Lightmap sets:          3 (one per Lighting Scenario)
```

### Draw call strategy

A room full of individually interactive switches, gauges, and breakers is a draw call problem. Mitigations in priority order:

1. **Merge all static bulkhead and structural geometry** into a small number of meshes per wall
2. **Instanced Static Meshes** for non-interactive repeated detail — rivets, conduit clamps, panel screws, grating
3. **Shared material instances** across all controls — one master material, parameter variation only. Every unique material is a draw call boundary.
4. **Texture atlasing** for placards and labels — one atlas, UV offsets, rather than a texture per sign
5. **Interactive controls stay separate actors** (they have to), but keep their meshes simple and their materials shared

### Texture budget

Megascans ship at 4K. That will not fit.

```
Bulkheads and large surfaces:   1024 × 1024, tiled
Control components:              512 × 512, atlased where possible
Placards and labels:             single 2048 atlas for all signage
Gauge faces:                     512 × 512, atlased
Normal maps:                     half the albedo resolution
Compression:                     ASTC throughout
```

Downscale on import. Do not rely on mip bias at runtime — the memory is allocated regardless.

### On-device validation

Profile on hardware from Phase 2 onward, not at the end.

```
OVR Metrics Tool          — live FPS, GPU/CPU utilization, thermal state
stat unit                 — frame, game, draw, GPU breakdown
stat rhi                  — draw calls, triangles
RenderDoc for Oculus      — GPU frame capture when something is wrong
```

**Watch for thermal throttling.** Quest 3 will sustain full clocks for roughly ten to fifteen minutes under load, then step down. A scenario designed to run 25–40 minutes must hold frame rate *after* throttling, not just at launch. Test a full-length session, not a two-minute check.

---

## PART 8 — AUDIO

Audio carries more of this experience than visuals do.

### Layers

```
Mask breathing       — always present, rate tied to air remaining
Hull creak           — random interval, tied to temperature
Fan spin-up          — on bus energize, satisfying ramp
Reactor hum          — appears at criticality, builds with power
Coolant flow         — pump running, pitch tied to flow rate
Mechanical clunks    — every switch, breaker, valve detent
Drone motor          — in-world when near, through-feed when remote
Silence              — Phase 0. Almost nothing. The absence is the point.
```

### Mixer structure

```
Master
  Ambience      — hull, hum, flow
  Mechanical    — controls, switches, valves
  Suit          — breathing, mask, wrist gauge
  DroneFeed     — heavily filtered, bandpass, distinct from in-world
  Alerts        — scram klaxon, pressure warning
```

**Reverb:** tight, small-room, metallic. One reverb zone for the bridge, a different filtered one applied to the drone feed audio so remote and local sound unmistakably different.

**The drone feed audio should be bad.** Bandpass filtered, compressed, with dropouts matching the video. Two channels of degradation reinforcing each other.

---

## PART 9 — IMPLEMENTATION PHASES

### Phase 1 — Project setup
1. UE 5.8.3, VR Template
2. Folder structure, naming conventions
3. Git + LFS with file locking
4. VRExpansion installed and verified
5. Confirm a packaged VR build runs before writing gameplay

### Phase 2 — Space validation
6. Grey-box the 2.7m × 2.7m compartment
7. Height calibration system
8. **Walk it in the headset.** Verify reach to all four bulkheads without approaching guardian
9. Place grey cubes at every intended control position, confirm reachability for a 1.6m and 1.9m player
10. **Do not proceed until this is right**

### Phase 3 — Physical control kit
11. `BPC_ToggleSwitch`, `BPC_GuardCover`, `BPC_PushBreaker`
12. `BPC_RotarySelector`, `BPC_ValveWheel`, `BPC_Lever`
13. Haptics on all of them
14. Test each in isolation — a switch should feel good to flip with no game attached

### Phase 4 — Ship state
15. `UShipStateSubsystem` with full state model
16. Physical simulation on timer: pressure, temperature, flux
17. Debug overlay showing all state values
18. Wire controls to state, state to indicator lamps and gauges

### Phase 5 — The dependency chain
19. Phase 1–2: battery, emergency bus, fault tree console
20. Phase 4: coolant valves, pump, cavitation failure case
21. Phase 5: rod banks, flux simulation, scram logic
22. Phase 6: environmental bus, scrubber, heaters
23. Playtest the full chain without the drone — temporarily make C-7 hand-reachable

### Phase 6 — The drone
24. `BP_MaintenanceDrone` with movement and camera
25. Render target feed with degradation post-process
26. Physical two-axis controller on the console
27. Conduit geometry and C-7 placement
28. Deployment, docking, battery

### Phase 7 — Pressure systems
29. Air timer, wrist gauge, breathing audio
30. Blackout and recovery
31. Cabin temperature, breath vapor, control stiffness

### Phase 8 — The binder
32. Grabbable binder with page turns
33. Eight pages of content: rod sequence, coolant order, conduit schematic

### Phase 9 — Art pass
34. Megascans on blockout geometry
35. Modular sci-fi kit replacing grey walls
36. Physical control kit modeled and placed
37. Placards, labels, wear decals
38. **Layout does not change in this phase**

### Phase 10 — Lighting and audio
39. Four lighting states with transitions
40. Emissive pass on all instruments
41. Full audio implementation
42. Drone feed audio degradation

### Phase 11 — Optimization
43. Profile with `stat unit`, Unreal Insights
44. Verify render target cost at the worst case
45. LODs, cull distances
46. Zero GC allocations per frame

---

## PART 10 — PROMPT SEQUENCE

```
1.  "Set up the project per this plan — folder structure, naming
     conventions, Git LFS gitignore for UE 5.8.3, VRExpansion."

2.  "Build the room blockout at 2.7m × 2.7m with the four-station
     layout, plus the height calibration system."

3.  "Create BPC_ToggleSwitch and BPC_GuardCover with haptics."

4.  "Create BPC_PushBreaker and BPC_RotarySelector with detents."

5.  "Create BPC_ValveWheel with cumulative rotation tracking and a
     resistance curve."

6.  "Create BPC_AnalogGauge and BPC_IndicatorLamp driven by float
     and bool inputs."

7.  "Implement UShipStateSubsystem with the full state model and
     event dispatchers."

8.  "Add the physical simulation — coolant pressure and flow,
     reactor flux and temperature, cabin temperature — on a 0.25s
     timer."

9.  "Build a debug overlay widget showing all ship state values."

10. "Implement Phase 1 and 2 — battery isolation, emergency bus,
     fault tree console."

11. "Implement Phase 4 — coolant valves, pump, pressure response,
     and the cavitation failure case."

12. "Implement Phase 5 — rod bank selectors, flux simulation, scram
     logic, and criticality hold."

13. "Implement Phase 6 — environmental bus, scrubber, heaters,
     cabin recovery."

14. "Build BP_MaintenanceDrone with movement, camera, light, and
     manipulator."

15. "Implement the drone feed render target with monochrome,
     scanline, and noise post-processing at 20fps."

16. "Build the physical two-axis drone controller on the console."

17. "Implement the air timer, diegetic wrist gauge, breathing audio,
     and blackout recovery."

18. "Build the grabbable procedures binder with page turning."

19. "Implement the four lighting states with transitions."

20. "Set up the audio mixer, reverb zones, and drone feed audio
     degradation."

21. "Create a VR performance profiling checklist and optimization
     pass."
```

---

## PART 11 — NOTES FOR CLAUDE

1. **UE 5.8.3 APIs only.** Enhanced Input, not legacy bindings. XRI/VR Template conventions.
2. **Blueprint-first.** Note where C++ helps; assume Blueprint unless asked.
3. **All content original.** Hard sci-fi genre conventions are free to use. Do not reproduce ship names, terminology, or designs from existing franchises.
4. **No locomotion. Ever.** Physical room scale only. If a design problem seems to need locomotion, redesign the problem.
5. **Hand tracking only — no controllers, no haptics.** Feedback comes from audio on physical contact plus visible hand reaction. See Part 5.6 before implementing any interaction.
6. **No screen-space UI.** No HUD, no floating text, no quest markers. All information is diegetic — gauges, lamps, placards, the binder.
7. **Object pooling** for audio sources and any runtime spawns.
8. **No Event Tick by default.** Timers and events. The ship state simulation runs on a 0.25s timer, not per-frame.
9. **Avoid hard references.** Blueprint Interfaces over casting. Everything reads from the Ship State Subsystem.
10. **Render target budget is one.** The drone feed is the only live render target, and it only renders when actually displayed and observed.
11. **Validate reach before building.** Phase 2 is a hard gate. Controls the player can't comfortably reach are worse than no controls.

---

## PART 12 — WHAT COMES NEXT

Scenario 1 establishes the vessel, the controls, and the drone. Planned follow-ons, each reusing the same room:

**Scenario 2 — Breach.** Hull penetration in an adjacent compartment. Drone deploys to patch while you manage pressure from the bridge. Introduces drone-under-time-pressure and multi-system juggling.

**Scenario 3 — Transit.** First piloting. Navigation console, burn planning, thrust and attitude. The room never moves; the view does. Introduces the orbital mechanics layer.

**Scenario 4 — Salvage.** Drone deploys outside the hull. EVA-range piloting, signal degradation with distance, battery as a hard constraint.

The room-scale constraint means every scenario is the same physical space with different problems. That is the strength of the design, not a limitation — the player learns one cockpit deeply rather than many shallowly.

---

*Document version 1.0 — Unreal Engine 5.8.3 — Room-scale VR, 10ft × 10ft*
