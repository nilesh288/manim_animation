# Manim 2D/3D Editorial Engine - Master API Reference

> **Canonical Repository**: [https://github.com/nilesh288/manim_animation](https://github.com/nilesh288/manim_animation)  
> **Raw API Reference**: [https://raw.githubusercontent.com/nilesh288/manim_animation/manim_antigravity_v1/FRAMEWORK_API.md](https://raw.githubusercontent.com/nilesh288/manim_animation/manim_antigravity_v1/FRAMEWORK_API.md)  
> **Target Framework**: Manim Community Edition `v0.22.x` + `engine_2d`

This document is the single source of truth for AI code generators (Claude, ChatGPT, etc.) to produce 100% executable, broadcast-grade Manim Python code that complies with the local `engine_2d` animation framework.

---

## 1. Canonical Import Skeleton

Every generated scene MUST use this exact import pattern:

```python
from manim import *
from engine_2d import (
    EditorialScene,
    PALETTE,
    FONT_SIZES,
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
    MetricGauge,
    MilestoneTimeline,
    SleekArrow,
)
```

---

## 2. Scene Architecture & Scoping Pattern

To eliminate `NameError` and scoping traps, all scenes must follow the **Outer-Scope Variable Declaration Pattern**:

```python
class Scene01(EditorialScene):
    def construct(self):
        # 1. Total Target Duration (Must match timed_storyboard.json exactly)
        self.target_duration = 61.77

        # 2. Outer-Scope Actor Declarations (Instantiate ALL persistent actors here)
        workstation = MacBookDevice().move_to([0.0, -0.3, 0.0])
        cpu_chip = ChipSoC().move_to([0.0, 0.0, 0.0])
        power_conn = ATX24PinConnector().move_to([-4.5, 0.0, 0.0])

        # 3. Synchronized Choreographed Beats
        def act_1_1():
            self.play(FadeIn(workstation, shift=DOWN * 0.5), run_time=2.0)
            self.play(workstation.animate.set_color(PALETTE["sky"]), run_time=3.58)
            self.wait(1.8)

        self.beat(
            "1.1",
            "Have you ever pressed that power button and waited...",
            act_1_1,
            motion_time=7.58,
            hold_time=1.8,
            transient=[]
        )
```

---

## 3. Choreography & Beat Timing API

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
* `beat_id`: Clause identifier string (e.g., `"1.1"`, `"2.3"`).
* `narration`: The exact spoken script clause.
* `action`: Callable function (`def act_X_Y():`) containing the active `self.play(...)` animations.
* `motion_time`: Exact active animation duration in seconds. Sum of `run_time` inside `action()` must equal `motion_time`.
* `hold_time`: Rest/narration pause duration.
* `transient`: List of temporary callouts or badges to display during this beat. The framework automatically materializes, times, and dissolves them with zero drift.

### Transient Dictionary Schema
Transient elements passed to `transient=[...]` can be defined as structured dictionaries:
```python
transient=[
    # High-contrast rounded pill/badge:
    {"type": "badge", "text": "LINUX BOOT SEQUENCE", "position": [0.0, 2.3], "fill_token": "indigo", "text_color": "#FFFFFF"},
    # Explanatory annotation label:
    {"type": "annotation", "text": "3.3V / 5V / 12V RAILS", "position": [-3.4, 1.5], "color_token": "text_primary"}
]
```

---

## 4. Built-in Physical Actor Catalog (`engine_2d.objects`)

All physical actors inherit from `InteractiveActor(VGroup)`:
- **Zero-Crash Animations**: Unknown `.animate.<custom_method>` calls are dynamically bound and handled cleanly without `AttributeError`.
- **Fluid Bounds**: `.surround_bounds(x_bounds=[-4, 4], y_bounds=[-2, 2])` aligns actors dynamically.
- **State Setting**: `.set_state("active", color=PALETTE["mint"])`.

### Hardware & Silicon
| Actor Class | Visual Representation | Key Parameters & Methods |
| :--- | :--- | :--- |
| `MotherboardSection` | Authentic dark green/black PCB with copper power traces and SMD caps | `MotherboardSection(width=7.2, height=3.6)` |
| `ChipSoC` | Ceramic processor package with gold pins and glowing silicon die | `ChipSoC(scale=1.0)` |
| `QuartzOscillator` | Metallic rectangular crystal oscillator can with laser frequency markings | `QuartzOscillator(frequency_label="3.60 GHz")` |
| `ATX24PinConnector` | 24-pin dual-row power block with colored 3.3V/5V/12V/GND wires & clip | `ATX24PinConnector(scale=1.0)` |
| `CapacitorBank` | Row of 3-4 cylindrical VRM capacitors with stamped X-vents | `CapacitorBank(count=3, scale=1.0)` |
| `DiagnosticSpeaker` | Motherboard piezo buzzer for POST error beep codes | `DiagnosticSpeaker(scale=1.0)` |

### Storage & Memory
| Actor Class | Visual Representation | Key Parameters & Methods |
| :--- | :--- | :--- |
| `RamModuleActor` | DDR5 DIMM memory stick with gold edge fingers, DRAM ICs, and LEDs | `RamModuleActor(capacity_label="16 GB DDR5 RAM")` |
| `NvmeSsdActor` | M.2 2280 NVMe SSD card with controller chip, 3D NAND flash, and gold notch | `NvmeSsdActor(capacity_label="1 TB NVMe SSD")` |
| `StorageSectorArray` | Horizontal strip array of 512-byte disk sectors highlighting Sector 0 (MBR) | `StorageSectorArray(scale=1.0)` |
| `UsbFlashDriveActor` | USB 3.0 Type-A thumb drive stick with blue insulator and activity LED | `UsbFlashDriveActor(scale=1.0)` |

### Firmware & Operating Systems
| Actor Class | Visual Representation | Key Parameters & Methods |
| :--- | :--- | :--- |
| `SpiFlashRom` | 8-pin SOIC / DIP SPI Flash ROM chip where BIOS/UEFI firmware resides | `SpiFlashRom(variant="vintage_dip_package" / "wson_low_profile")` |
| `MechanicalStepperRelay`| Vintage rotary stepper relay selector representing 16-bit BIOS mode | `MechanicalStepperRelay(scale=1.0)` |
| `CrossbarRoutingMatrix`| High-tech multi-lane crossbar bus matrix representing UEFI routing | `CrossbarRoutingMatrix(scale=1.0)` |
| `RotaryDispatchSwitch` | GRUB multi-boot selection switch with rotary selector dial | `RotaryDispatchSwitch(scale=1.0)` |
| `FilesystemHierarchyTree` | Linux directory hierarchy tree starting at root `/` branching to `/bin`, `/lib`, `/etc` | `FilesystemHierarchyTree(apex_position=[...], branch_positions=[...])` |
| `FilesystemNodeActor` | Standalone executable node card representing `/sbin/init` | `FilesystemNodeActor(path="/sbin/init")` |
| `CyberneticTurbineHub` | High-velocity circular supervisor turbine engine representing `systemd` (PID 1) | `CyberneticTurbineHub(scale=1.0)` |

### Networking, Physics & Security
| Actor Class | Visual Representation | Key Parameters & Methods |
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

## 5. UI Primitives & Containers (`engine_2d.primitives`)

* `MacOSPill`: High-contrast status pill badge (`MacOSPill("POST SUCCESS", fill_color=PALETTE["mint"])`).
* `TechCard`: Elegant white container with title header (`TechCard(width=4.0, height=2.5, title="SPECIFICATIONS")`). **Never add traffic-light buttons (🔴🟡🟢)**.
* `VisualCard`: Minimalist framed container for diagrams and waveforms.
* `MetricGauge`: Circular or linear parameter dial gauge.
* `MilestoneTimeline`: Stepped process progression indicator.
* `SleekArrow`: High-contrast directed vector with modern arrowhead.

---

## 6. Design Tokens Reference (`engine_2d.theme`)

### Color Palette (`PALETTE`)
* **Foundations**:
  - `PALETTE["bg"]` (`#F8F9FA`): Warm off-white / eggshell canvas.
  - `PALETTE["surface_card"]` (`#FFFFFF`): Clean arctic white card fill.
  - `PALETTE["bg_subtle"]` (`#EDF2F7`): Header shading & subtle ground platforms.
  - `PALETTE["stroke"]` (`#2D3748`): Deep charcoal border outline.
* **Typography**:
  - `PALETTE["text"]` / `PALETTE["text_primary"]` (`#1A202C`): Slate pitch black.
  - `PALETTE["text_dim"]` (`#718096`): Muted secondary annotations.
  - `PALETTE["text_light"]` / `PALETTE["white"]` (`#FFFFFF`): Pure white text for dark badges.
* **Editorial Accents**:
  - `PALETTE["blue"]` (`#1E60FF`): Primary network streams, data flows, clock signals.
  - `PALETTE["sky"]` (`#0284C7`): Cyan bus waves, fiber optic pulses.
  - `PALETTE["mint"]` (`#00C9A7`): Verified hardware, success states, green LEDs.
  - `PALETTE["amber"]` (`#ED8936`): Power rail voltages, thermal warnings, active bus lines.
  - `PALETTE["coral"]` (`#E53E3E`): Error states, collision alerts, opposing forces.
  - `PALETTE["indigo"]` (`#5A67D8`): Cryptography, firmware ROMs, instruction sets.
* *Note*: Nested indexing is fully supported: `PALETTE["accents"]["sky"]` resolves safely to `PALETTE["sky"]`.

### Typography Tokens (`FONT_SIZES`)
Use `FONT_SIZES` for all text to guarantee 1080p broadcast readability:
* `FONT_SIZES["hero"]` = 22 (Major title announcements)
* `FONT_SIZES["title"]` = 18 (Section headers)
* `FONT_SIZES["card_header"]` = 14 (`TechCard` headers)
* `FONT_SIZES["pill"]` = 13 (Status badges / pills)
* `FONT_SIZES["body"]` = 13 (Primary explanatory annotations)
* `FONT_SIZES["code"]` = 12 (Monospace code / terminal logs)
* `FONT_SIZES["label"]` = 11 (Component sub-labels)
* `FONT_SIZES["marking"]` = 10 (Hardware IC laser etchings)

---

## 7. Strict Code Safety & Syntax Rules

1. **Underscores Only in Function Identifiers (NO DOTS)**:
   - Always name action functions `def act_1_1():`, `def act_8_2():`.
   - **FATAL ERROR**: `def act_8.2():` causes `SyntaxError: expected '('`. Dots are strictly forbidden.
2. **16:9 Broadcast Safe Zone**:
   - Keep all primary mobjects within `[-5.5, 5.5]` X and `[-2.8, 2.8]` Y.
3. **Timing Conservation (Zero Drift)**:
   - Sum of `run_time` in all `self.play(...)` calls inside `act_X_Y()` MUST match `motion_time` exactly.
   - Conclude each action function with `self.wait(hold_time)`.
4. **No Slide Rule**:
   - Never create a scene that is just a bulleted text box. Every beat must be anchored by a concrete physical actor.
