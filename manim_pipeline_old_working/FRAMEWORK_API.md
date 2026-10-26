# Manim 2D/3D Editorial Engine - Master API Reference

> **Canonical Repository**: [https://github.com/nilesh288/manim_animation](https://github.com/nilesh288/manim_animation)  
> **Raw API Reference**: [https://raw.githubusercontent.com/nilesh288/manim_animation/manim_antigravity_v1/FRAMEWORK_API.md](https://raw.githubusercontent.com/nilesh288/manim_animation/manim_antigravity_v1/FRAMEWORK_API.md)  
> **Target Framework**: Manim Community Edition `v0.22.x` + `engine_2d`

This document is the single source of truth for AI code generators (Claude, ChatGPT, etc.) to produce 100% executable, broadcast-grade Manim Python code that complies with the local `engine_2d` animation framework.

---

## 1. Canonical Import Skeleton

Every generated scene MUST use this exact import pattern:

```python
#!/usr/bin/env python3
from manim import *
import numpy as np

from engine_2d import (
    EditorialScene,
    PALETTE,
    FONT_SIZES,
    FONTS,
    # Physical Actors (select as needed):
    MotherboardSection,
    ChipSoC,
    QuartzOscillator,
    ATX24PinConnector,
    CapacitorBank,
    RamModuleActor,
    NvmeSsdActor,
    StorageSectorArray,
    UsbFlashDriveActor,
    SpiFlashRom,
    MechanicalStepperRelay,
    CrossbarRoutingMatrix,
    RotaryDispatchSwitch,
    FilesystemHierarchyTree,
    FilesystemNodeActor,
    CyberneticTurbineHub,
    MacBookDevice,
    PhoneDevice,
    ModernRouter,
    ServerRackActor,
    DataPacketActor,
    FiberOpticConduit,
    DiagnosticSpeaker,
    CryptographicPadlock,
    HighSpeedTrain,
    EddyBrakeAssembly,
    PlanetEarth,
    SatelliteActor,
    # UI Components & Primitives:
    MacOSPill,
    TechCard,
    VisualCard,
    MilestoneTimeline,
    SleekArrow,
)
```

---

## 2. Universal 5-Zone Canvas Spatial Matrix (Zero Collisions & Zero Occlusion)

The 16:9 1080p canvas spans `x ∈ [-7.1, 7.1]` and `y ∈ [-4.0, 4.0]`. To guarantee that generated code for **ANY TOPIC** is visually balanced and 100% collision-free, all actors must be mapped to dedicated spatial zones:

```
+-------------------------------------------------------------------------+
| ZONE 1: TOP PROGRESSION / ROADMAP ZONE (y = 2.4 to 3.2)                 |
| [MilestoneTimeline(all_up=True), Topic Header Pills, Chapter Badges]    |
+-------------------------------------------------------------------------+
|                                                                         |
| ZONE 2: MAIN STAGE / PHYSICAL ACTORS ZONE (y = -1.6 to 1.6)             |
|                                                                         |
|  [LAYOUT A: Single Subject]       Centered at [0.0, 0.0]                |
|                                                                         |
|  [LAYOUT B: Dual Subject / Split] Left: [-2.8, 0.0]  Right: [+2.8, 0.0] |
|                                   (Min horizontal gap >= 1.2 units)     |
|                                                                         |
|  [LAYOUT C: 3-Stage Pipeline]     Left: [-3.5, 0.0]  Center: [0.0, 0.0] |
|                                   Right: [+3.5, 0.0]                    |
|                                                                         |
+-------------------------------------------------------------------------+
| ZONE 3: BOTTOM STATUS & TELEMETRY ZONE (y = -2.7 to -3.3)               |
| [self.beat(..., transient=[{"type": "badge", "position": [0.0, -3.1]}])]|
+-------------------------------------------------------------------------+
```

### Strict Non-Occlusion Laws
1. **Never Stack Cards Over Devices**: A `TechCard` (width 4.5) must NEVER be centered over a `MacBookDevice` (width 2.4). Use **Layout B (Split Screen)**: Laptop at `[-2.6, 0.0]`, Terminal Card at `[+2.4, 0.0]`.
2. **Never Move an Actor Onto an Occupied Coordinate**: If Actor A is at `[-1.8, 0.0]`, NEVER move Actor B to `[-1.8, 0.0]` without first fading out Actor A (`FadeOut(actor_a)`).
3. **Container Actor Rule**: If using a container like `MotherboardSection`, `ServerRackActor`, or `ModernRouter`, do NOT drop duplicate external sub-actors (e.g. `CapacitorBank`, `ATX24PinConnector`) directly on top of it. Place external components in clear peripheral zones with connecting conduits.
4. **Timelines Must Use `all_up=True`**: When instantiating `MilestoneTimeline(...)` near the top of the screen (`y >= 2.2`), ALWAYS set `all_up=True`. This forces all milestone ticks and labels upward into the top margin, preventing collisions with stage actors below.

---

## 3. Scene Architecture & Scoping Pattern

To eliminate `NameError` and scoping traps, all scenes must follow the **Outer-Scope Variable Declaration Pattern**:

```python
class Scene01(EditorialScene):
    def construct(self):
        # 1. Total Target Duration (Must match timed_storyboard.json exactly)
        self.target_duration = 61.77

        # 2. Outer-Scope Actor Declarations (Instantiate ALL persistent actors here)
        laptop = MacBookDevice(scale=1.05, url_text="tty1: Linux").move_to([-2.6, 0.0, 0.0])
        log_card = TechCard(title="Kernel Console [tty1]", width=4.5, height=2.4).move_to([2.4, 0.0, 0.0])
        timeline = MilestoneTimeline(
            milestones=["1. FIRMWARE", "2. BOOTLOADER", "3. KERNEL", "4. PID 1"],
            length=10.0,
            y_pos=2.5,
            all_up=True,
        )

        # 3. Synchronized Choreographed Beats (Pure animation actions: NO self.wait inside!)
        def act_1_1():
            # Total run_time inside action MUST equal motion_time (2.0 + 3.0 + 2.58 = 7.58s)
            self.play(FadeIn(laptop, shift=UP * 0.3), FadeIn(log_card, shift=LEFT * 0.3), run_time=2.0)
            self.play(laptop.animate.scale(1.02), run_time=3.0)
            self.play(log_card.animate.scale(1.02), run_time=2.58)
            # NEVER CALL self.wait() INSIDE act_X_Y! self.beat handles hold_time automatically!

        self.beat(
            "1.1",
            "Have you ever pressed that power button and waited...",
            act_1_1,
            motion_time=7.58,
            hold_time=1.80,
            transient=[
                {"type": "badge", "text": "ACPI POWER-ON EVENT", "position": [0.0, -3.1], "fill_token": "indigo", "text_color": "#FFFFFF"}
            ]
        )
```

---

## 4. Choreography & Beat Timing API

The framework provides an exact, drift-free synchronization mechanism via `self.beat(...)`.

### Method Signature
```python
self.beat(
    beat_id: str,
    narration: str,
    action: callable,
    motion_time: float,
    hold_time: float,
    transient: list = None
)
```

### Parameters
* `beat_id`: Clause identifier string using underscores in corresponding actions (e.g. `"1.1"` -> `def act_1_1():`).
* `narration`: The exact spoken script clause.
* `action`: Callable function (`def act_X_Y():`) containing the active `self.play(...)` animations. Must NOT call `self.wait(...)`.
* `motion_time`: Exact active animation duration in seconds. Sum of `run_time` inside `action()` must equal `motion_time`.
* `hold_time`: Rest/narration pause duration. `self.beat(...)` handles this automatically with drift compensation.
* `transient`: List of temporary callouts or badges to display during this beat. The framework automatically materializes, times, and dissolves them with zero drift.

### Transient Dictionary Schema
Transient elements passed to `transient=[...]` are defined as structured dictionaries:
```python
transient=[
    # High-contrast rounded pill/badge:
    {"type": "badge", "text": "LINUX BOOT SEQUENCE", "position": [0.0, -3.1], "fill_token": "indigo", "text_color": "#FFFFFF"},
    # Explanatory annotation label:
    {"type": "annotation", "text": "3.3V / 5V / 12V RAILS", "position": [-2.0, 1.2], "color_token": "amber"}
]
```

---

## 5. Built-in Physical Actor Catalog (`engine_2d.objects`)

### Standard Animation Verb Whitelist (Zero Method Inventions)
- **PROHIBITION**: NEVER invent custom animation methods like `.animate.fire_diagnostic_pulses()`, `.animate.verify_chips()`, `.animate.emit_waves()`.
- **MANDATORY**: Use ONLY standard Manim animation primitives:
  - `FadeIn(mob, shift=...)`, `FadeOut(mob, shift=...)`
  - `Create(path_or_wave)`, `Transform(mob_a, mob_b)`
  - `mob.animate.move_to(...)`, `mob.animate.shift(...)`, `mob.animate.scale(...)`
  - `mob.animate.set_color(...)`, `mob.animate.set_fill(...)`, `mob.animate.set_stroke(...)`
  - Data pulses: Animate a simple `Dot` traveling along a `Line` or path.

### Hardware & Silicon
| Actor Class | Visual Representation | Key Parameters & Notes |
| :--- | :--- | :--- |
| `MotherboardSection` | Authentic emerald green/black PCB with copper power traces, built-in ATX socket, and VRM caps | `MotherboardSection(width=8.6, height=4.0)`. Do NOT place duplicate ATX/caps on top. |
| `ChipSoC` | Ceramic processor package with gold pins and glowing silicon die core | `ChipSoC(size=1.8, core_color=PALETTE["amber"])`. Silicon core is `cpu_chip.core`. |
| `QuartzOscillator` | Metallic rectangular crystal oscillator can with laser frequency markings | `QuartzOscillator(frequency_label="3.60 GHz", scale=0.9)` |
| `ATX24PinConnector` | 24-pin dual-row power block with colored 3.3V/5V/12V/GND wires & clip | `ATX24PinConnector(scale=0.9)` |
| `CapacitorBank` | Row of 3-4 cylindrical VRM capacitors with stamped X-vents | `CapacitorBank(count=3, scale=0.9)` |
| `DiagnosticSpeaker` | Motherboard piezo buzzer for POST error beep codes | `DiagnosticSpeaker(scale=1.0)` |

### Storage & Memory
| Actor Class | Visual Representation | Key Parameters & Notes |
| :--- | :--- | :--- |
| `RamModuleActor` | DDR5 DIMM memory stick with gold edge fingers, DRAM ICs, and LEDs | `RamModuleActor(capacity_label="16 GB DDR5 RAM")` |
| `NvmeSsdActor` | M.2 2280 NVMe SSD card with controller chip, 3D NAND flash, and gold notch | `NvmeSsdActor(capacity_label="1 TB NVMe SSD")` |
| `StorageSectorArray` | Horizontal strip array of 512-byte disk sectors highlighting Sector 0 (MBR) | `StorageSectorArray(scale=1.0)` |
| `UsbFlashDriveActor` | USB 3.0 Type-A thumb drive stick with blue insulator and activity LED | `UsbFlashDriveActor(scale=1.0)` |

### Firmware & Operating Systems
| Actor Class | Visual Representation | Key Parameters & Notes |
| :--- | :--- | :--- |
| `SpiFlashRom` | 8-pin SOIC / DIP SPI Flash ROM chip where BIOS/UEFI firmware resides | `SpiFlashRom(scale=1.0, label="SPI FLASH ROM", sublabel="BIOS / UEFI")` |
| `MechanicalStepperRelay`| Vintage rotary stepper relay selector representing 16-bit BIOS mode | `MechanicalStepperRelay(scale=1.0)` |
| `CrossbarRoutingMatrix`| High-tech multi-lane crossbar bus matrix representing UEFI routing | `CrossbarRoutingMatrix(scale=1.0)` |
| `RotaryDispatchSwitch` | GRUB multi-boot selection switch with rotary selector dial | `RotaryDispatchSwitch(scale=1.0)` |
| `FilesystemHierarchyTree` | Linux directory hierarchy tree starting at root `/` branching to `/bin`, `/lib`, `/etc` | `FilesystemHierarchyTree(apex_position=[...], branch_positions=[...])` |
| `FilesystemNodeActor` | Standalone executable node card representing `/sbin/init` | `FilesystemNodeActor(path="/sbin/init")` |
| `CyberneticTurbineHub` | High-velocity circular supervisor turbine engine representing `systemd` (PID 1) | `CyberneticTurbineHub(scale=1.0)` |

### Networking, Physics & Security
| Actor Class | Visual Representation | Key Parameters & Notes |
| :--- | :--- | :--- |
| `MacBookDevice` | Aluminum unibody laptop workstation with terminal/app screen | `MacBookDevice(url_text="tty1: Linux")` |
| `PhoneDevice` | Sleek smartphone receiver with glass screen and status radar dot | `PhoneDevice(scale=1.0)` |
| `ModernRouter` | Wi-Fi 6 router with glowing status LEDs and multi-band radio arcs | `ModernRouter(scale=1.0)` |
| `ServerRackActor` | 42U datacenter server rack with modular blades and blinking LEDs | `ServerRackActor(scale=1.0)` |
| `DataPacketActor` | High-speed data packet capsule with jewel header and payload body | `DataPacketActor(scale=1.0)` |
| `FiberOpticConduit` | Duplex optical LC fiber transceiver emitting laser light pulses | `FiberOpticConduit(scale=1.0)` |
| `CryptographicPadlock`| Heavy chrome shackle padlock representing Secure Boot / TLS encryption | `CryptographicPadlock(scale=1.0)` |
| `HighSpeedTrain` | Aerodynamic high-speed bullet train with livery on rails | `HighSpeedTrain(scale=1.0)` |
| `EddyBrakeAssembly` | Electromagnet C-core with magnetic flux lines and eddy current loops | `EddyBrakeAssembly(scale=1.0)` |
| `PlanetEarth` | 3D orbital Earth sphere with continents | `PlanetEarth(radius=1.5)` |
| `SatelliteActor` | Orbital satellite with gold foil bus, solar panels, and dish | `SatelliteActor(scale=1.0)` |

---

## 6. UI Primitives & Containers (`engine_2d.primitives`)

* `MacOSPill`: High-contrast status pill badge (`MacOSPill("RESET VECTOR: 0xFFFFFFF0", color=PALETTE["blue"], is_solid=True)`).
* `TechCard`: Elegant container with title header (`TechCard(width=4.5, height=2.4, title="SPECIFICATIONS")`). **Never add traffic-light buttons (🔴🟡🟢)**.
* `VisualCard`: Minimalist framed container for diagrams and waveforms.
* `MilestoneTimeline`: Stepped process progression indicator. **Always use `all_up=True` when positioned near the top of the screen (`y >= 2.2`)**. Dot mobjects are accessible via `timeline.dots[i]`.
* `SleekArrow`: High-contrast directed vector with modern arrowhead.

---

## 7. Guaranteed High-Contrast Color Matrix

| Background / Surface | Required Text / Stroke Color | Prohibited Colors |
| :--- | :--- | :--- |
| **Canvas Background** (`PALETTE["bg"]` = `#F8F9FA`) | `PALETTE["text"]` (`#1A202C`), `PALETTE["stroke"]` (`#2D3748`) | `#FFFFFF`, `text_light`, yellow |
| **Arctic White Cards** (`PALETTE["surface_card"]` = `#FFFFFF`) | `PALETTE["text"]` (`#1A202C`), `PALETTE["blue"]`, `PALETTE["mint"]` | Pure white text |
| **Dark Emerald PCB / Dark Graphite Surface** (`#132B22`, `#2A3238`) | `"#FFFFFF"`, `PALETTE["text_light"]`, `PALETTE["amber"]` | `PALETTE["text"]` (black), `text_dim`, `blue` |
| **Dark Solid Pills** (`indigo`, `blue`, `coral`, `surface_dark`) | `text_color="#FFFFFF"` | Dark text, blue on indigo |
| **Bright Solid Pills** (`amber`, `mint`, `bg_subtle`) | `text_color="#1A202C"` | White text |

---

## 8. Strict Code Safety & Syntax Rules

1. **Underscores Only in Function Identifiers (NO DOTS)**:
   - Always name action functions `def act_1_1():`, `def act_8_2():`.
   - **FATAL ERROR**: `def act_8.2():` causes `SyntaxError: expected '('`. Dots are strictly forbidden.
2. **Scoping**: All persistent mobjects must be declared at the top of `construct()` before any `def act_*` function.
3. **Pure Action Functions (No `self.wait`)**: `act_X_Y()` must contain ONLY `self.play(...)` calls whose `run_time` values sum to `motion_time`.
4. **Spatial Clearance**: Follow the 5-Zone Canvas Spatial Matrix. Never stack cards over devices or overlap actors.
5. **Stage Eviction**: Evict outgoing actors with `FadeOut(...)` when transitioning between conceptual stages.
6. **No Semantic Inventions**: Use only standard Manim transform/color/fade primitives.
7. **No Slide Rule**: Never create a scene that is just a bulleted text box. Every beat must be anchored by a concrete physical actor.
