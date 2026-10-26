# Manim Technical Animation Pipeline

A production-grade 2D technical infographic animation engine built on **Manim Community Edition (v0.22.x)**.

Features:
- **Object-First Hardware Architecture**: Real, tangible physical actors (Motherboards, RAM DIMMs, NVMe SSDs, Quartz Oscillators, SPI ROMs, Routers, Servers) rather than static PowerPoint-style text slides.
- **Warm Editorial HIG Theme**: Off-white/eggshell canvas (`#F8F9FA`), pure white cards (`#FFFFFF`), high-contrast slate black text (`#1A202C`), and vibrant accents. Clean modern cards with **zero** macOS traffic-light buttons.
- **Broadcast-Grade Typography**: Centralized `FONT_SIZES` hierarchy optimized for 1080p readability.
- **Zero-Drift Narration Timing**: Frame-accurate synchronization between voice narration and animations using `self.beat()`.
- **RAM Filesystem Rendering (`/dev/shm`)**: Intermediate `.mp4` chunks and Cairo frame buffers render 100% in RAM tmpfs, **eliminating SD card write wear** and dramatically speeding up rendering before persisting the final MP4 to disk.

---

## 1. Prerequisites & Environment

Activate the Python virtual environment:
```bash
cd /home/nilesh/manim_animation/manim_pipeline_old_working
source /home/nilesh/manim-env/bin/activate
```

Verify Manim and FFmpeg installation:
```bash
manim --version       # Expected: v0.22.x
ffmpeg -version       # Required for audio muxing
```

---

## 2. Project Directory Structure

```
manim_pipeline_old_working/
├── engine_2d/                  # Core Framework
│   ├── base_scene.py           # InfographicScene with self.beat() zero-drift timing
│   ├── theme.py                # PALETTE, FONTS, and FONT_SIZES design tokens
│   ├── primitives.py           # TechCard, VisualCard, MacOSPill, MetricGauge, etc.
│   └── objects.py              # Physical actors (Motherboard, RAM, SSD, Quartz, Router, etc.)
├── scenes/                     # Your animation scenes
│   └── scene_01_linux_boot.py  # Production scene (POST, Motherboard, RAM, NVMe, SPI ROM)
├── renders/                    # Permanent output directory on SD card storage
│   ├── Linux_Boot_Scene01_1080p.mp4
│   └── videos/
├── linux_boot_sc1.mp3          # Topic master narration audio tracks
├── internet_working.mp3
├── air_break.mp3
├── render_scene.sh             # High-performance bash render script (RAM-backed via /dev/shm)
├── run_pipeline.py             # Python render orchestrator (RAM-backed via /dev/shm)
└── README.md
├── render_scene.sh             # High-performance bash render script (RAM-backed)
├── run_pipeline.py             # Python render orchestrator (RAM-backed)
└── README.md
```

---

## 3. How to Create an Animation Scene Manually

### Step 1: Prepare Your Audio & Timings
Place your audio narration file (e.g., `my_topic.mp3`) in the workspace. Note its exact total duration using `ffprobe`:
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 my_topic.mp3
```

### Step 2: Create Your Scene File
Create a new file in `scenes/`, e.g. `scenes/scene_01_my_topic.py`.

Use the template below, following the **Object-First Law**:

```python
from manim import *
import numpy as np
from engine_2d import (
    InfographicScene,
    PALETTE,
    FONTS,
    FONT_SIZES,
    TechCard,
    MacOSPill,
    # Import physical actors needed for your topic:
    MotherboardSection,
    RamModuleActor,
    NvmeSsdActor,
    QuartzOscillator,
    SpiFlashRom,
    DiagnosticSpeaker,
    MacBookDevice,
    ModernRouter,
    ServerRackActor,
)

class MyScene01(InfographicScene):
    def construct(self):
        # 1. SET EXACT TARGET DURATION (Seconds)
        self.target_duration = 30.00  # Match your audio duration

        # 2. INSTANTIATE ACTORS IN OUTER SCOPE (Before any beats)
        laptop = MacBookDevice(scale=0.9).move_to([0, 0.4, 0])
        status_pill = MacOSPill("System Initialization", color=PALETTE["blue"]).move_to([0, -2.4, 0])

        ram = RamModuleActor(scale=0.9, capacity_label="16 GB DDR5").move_to([-2.5, 0.5, 0])
        ssd = NvmeSsdActor(scale=0.9, capacity_label="1 TB NVMe SSD").move_to([2.5, 0.5, 0])

        # 3. CHOREOGRAPH BEATS WITH ZERO-DRIFT TIMING
        # Beat 1: Intro (0.00s -> 5.00s | motion: 3.50s, hold: 1.50s)
        self.beat(
            motion_time=3.50,
            hold_time=1.50,
            action=lambda: [
                self.play(FadeIn(laptop), FadeIn(status_pill), run_time=2.00),
                self.play(laptop.screen.animate.set_fill(PALETTE["surface_card"]), run_time=1.50),
            ]
        )

        # Beat 2: Hardware Diagnostics (5.00s -> 15.00s | motion: 7.00s, hold: 3.00s)
        self.beat(
            motion_time=7.00,
            hold_time=3.00,
            action=lambda: [
                self.play(FadeOut(laptop), run_time=1.00),
                self.play(FadeIn(ram), FadeIn(ssd), run_time=2.00),
                # Animate physical action: illuminate DRAM chips
                self.play(
                    ram.chips[0][0].animate.set_fill(PALETTE["mint"]),
                    ram.chips[1][0].animate.set_fill(PALETTE["mint"]),
                    run_time=2.00,
                ),
                self.play(
                    ram.chips[2][0].animate.set_fill(PALETTE["mint"]),
                    ram.chips[3][0].animate.set_fill(PALETTE["mint"]),
                    ssd.led.animate.set_fill(PALETTE["amber"]),
                    run_time=2.00,
                ),
            ]
        )
```

---

## 4. Key Design & Architecture Rules

1. **Concrete Physical Actors (Strict Anti-Slide Law)**:
   - **Never** create static slides with bullet lists in cards.
   - Always choose physical actors from `engine_2d.objects` that act out the concept mechanically or electronically.
   - Text should be limited to 1–2 status pills (`MacOSPill`) or short telemetry badges.
2. **Strict Timing Conservation Law (Zero Drift)**:
   - In each `self.beat(motion_time=M, hold_time=H, action=...)`, the sum of `run_time` across all animations inside `action` **must exactly equal** `motion_time`.
3. **Broadcast-Safe Zone**:
   - Keep all actors and text within `[-5.5, 5.5]` (X-axis) and `[-2.8, 2.8]` (Y-axis).
4. **Standard Typography Scale**:
   - Reference `FONT_SIZES`:
     - `FONT_SIZES["hero"]` (22) for major titles
     - `FONT_SIZES["card_header"]` (14) for card headers
     - `FONT_SIZES["pill"]` (13) for status pills
     - `FONT_SIZES["body"]` (13) for regular text
     - `FONT_SIZES["code"]` (12) for monospace/terminal
     - `FONT_SIZES["marking"]` (10) for hardware IC markings

---

## 5. How to Render the Animation

The framework includes automated **RAM filesystem rendering (`/dev/shm`)** to prevent SD card wear and boost speed.

### Method 1: Using the Bash Renderer Script (`render_scene.sh`)

#### Quick 480p POC Preview (Fast Verification):
```bash
./render_scene.sh scenes/scene_01_my_topic.py MyScene01 -ql my_topic.mp3
```

#### Final Broadcast 1080p Full HD Render:
```bash
./render_scene.sh scenes/scene_01_my_topic.py MyScene01 "-r 1920,1080 --fps 30" my_topic.mp3
```

What the script does automatically:
1. Detects `/dev/shm` (RAM disk tmpfs) and allocates a temporary workspace.
2. Manim writes all intermediate partial chunks directly to RAM (zero SD card wear).
3. Copies the final assembled `.mp4` to `renders/`.
4. Muxes with your audio narration file using FFmpeg into `renders/scene_01_my_topic_1080p.mp4`.
5. Frees the RAM workspace automatically.

---

### Method 2: Using the Python Orchestrator (`run_pipeline.py`)

```bash
# 480p Preview with audio:
python run_pipeline.py scenes/scene_01_my_topic.py MyScene01 -q l --audio my_topic.mp3

# 1080p Full HD with audio:
python run_pipeline.py scenes/scene_01_my_topic.py MyScene01 -q h --audio my_topic.mp3
```

---

## 6. Inspecting Quality & Keyframes

Extract keyframe stills from the rendered video to visually verify contrast, typography, and object placement:
```bash
# Extract frame at 10.5 seconds:
ffmpeg -y -ss 00:00:10.500 -i renders/scene_01_my_topic_1080p.mp4 -vframes 1 frame_10s.png
```

---

## 7. Available Physical Actors Reference Table

| Category | Actor Class | Description / Visual Elements |
| :--- | :--- | :--- |
| **Computers & Devices** | `MacBookDevice` | Modern unibody laptop with screen bezel, keyboard base, and notch. |
| | `PhoneDevice` | Modern smartphone with front glass screen and dynamic status bar. |
| **Hardware Components** | `MotherboardSection` | Multilayer green PCB, 24-pin ATX socket, VRM chokes/caps, copper conduits, Power-Good LED. |
| | `RamModuleActor` | DDR5 DIMM stick with gold contact teeth, notch, DRAM memory chips, and heat spreader. |
| | `NvmeSsdActor` | M.2 2280 NVMe SSD with gold M-key edge connector, controller ASIC, 3D NAND flash, and LED. |
| | `QuartzOscillator` | Silver metallic hermetic crystal oscillator can (`3.60 GHz XTAL OSC`) with solder leads. |
| | `SpiFlashRom` | 8-pin SOIC firmware chip with pin 1 index dot, soldered leads, and SPI bus traces. |
| | `DiagnosticSpeaker` | Motherboard piezo buzzer cylinder with polarity marker emitting acoustic sound waves. |
| | `ChipSoC` | CPU/SoC chip package with grid pin pads, silicon core die, and heat shield. |
| **Networking & Cloud** | `ModernRouter` | Enterprise router with dual antennas, RJ45 Ethernet ports, and link activity LEDs. |
| | `ServerRackActor` | Data center server chassis with front ventilation grills and status lights. |
| | `DataPacketActor` | Structured network packet actor with header, payload segment, and transport indicator. |
| | `CellTowerActor` | Telecom mast tower broadcasting RF cellular signal arcs. |
| **Physics & Transport**| `HighSpeedTrain` | Aerodynamic high-speed bullet train car with bogie wheel assemblies. |
| | `EddyBrakeAssembly` | Electromagnet poles (North/South) interacting with conductive track via eddy current loops. |
| | `PlanetEarth` | Planetary sphere with continental landmasses, equator, and atmospheric haze. |
| | `SatelliteActor` | Orbital satellite with gold payload bus body, photovoltaic solar wings, and telemetry dish. |
| **Security & Logic** | `CryptographicPadlock` | Metallic padlock with hardened shackle and keyhole for TLS/Secure Boot trust. |
| **UI Containers** | `TechCard` | Arctic white technical container with subtle header bar and deep charcoal border. |
| | `VisualCard` | Compact card container with bold headline, monospace subtitle, and drop shadow. |
| | `MacOSPill` | Rounded capsule status badge with bold typography and high-contrast fill. |
| | `MetricGauge` | Horizontal technical progress bar with percentage indicator. |
