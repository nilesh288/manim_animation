#!/usr/bin/env python3
"""
scene_01_linux_boot.py
Topic: The Linux Boot Process: From Power Button to PID 1
Scene 01: From Power Button to Firmware & POST (0.00s -> 152.04s)
Style: Concrete Physical Hardware Actors (Motherboard, RAM DIMM, NVMe SSD, SPI ROM, Quartz Clock, Piezo Buzzer)
       Warm Editorial Light Canvas (#F8F9FA), Zero-Drift Synchronization (152.04s).
"""
from manim import *
import numpy as np
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine_2d import (
    InfographicScene,
    PALETTE,
    FONTS,
    MacBookDevice,
    ChipSoC,
    MotherboardSection,
    RamModuleActor,
    NvmeSsdActor,
    QuartzOscillator,
    SpiFlashRom,
    DiagnosticSpeaker,
    CryptographicPadlock,
    TechCard,
    MacOSPill,
    VisualCard,
    SleekArrow,
    MetricGauge,
    MilestoneTimeline,
    ease_out_cubic,
    ease_in_out_quad,
)


class Scene01(InfographicScene):
    target_duration = 152.04

    def construct(self):
        # =============================================================
        # 1. PHYSICAL HARDWARE ACTOR DECLARATIONS
        # =============================================================
        # Act 1: Laptop Workstation & Power Button
        laptop = MacBookDevice(scale=1.1, url_text="tty1: Linux Login", show_traffic_lights=False).move_to([0, 0.2, 0])
        pwr_dot = Dot(laptop.base.get_top() + RIGHT * 0.95, radius=0.06, color=PALETTE["mint"])
        pwr_pulse = Circle(radius=0.18, color=PALETTE["mint"], stroke_width=2.0).move_to(pwr_dot.get_center())
        pwr_pill = MacOSPill("ACPI Power Button Pressed", color=PALETTE["mint"], is_solid=True).move_to([0, -2.4, 0])

        dmesg_card = TechCard(title="Kernel Console [tty1]", width=5.6, height=2.3, is_dark=False).move_to([0, 0.2, 0])
        dmesg_t1 = Text("[  0.000000] Linux version 6.8.0-generic", font=FONTS["mono"], font_size=12, color=PALETTE["blue"]).move_to(dmesg_card.body.get_center() + UP * 0.32)
        dmesg_t2 = Text("[  0.001240] Command line: BOOT_IMAGE=/vmlinuz root=UUID=...", font=FONTS["mono"], font_size=11, color=PALETTE["text"]).next_to(dmesg_t1, DOWN, buff=0.13)
        dmesg_t3 = Text("[  0.045100] x86/fpu: Supporting XSAVE feature 0x001", font=FONTS["mono"], font_size=11, color=PALETTE["mint"]).next_to(dmesg_t2, DOWN, buff=0.13)
        dmesg_group = VGroup(dmesg_card, dmesg_t1, dmesg_t2, dmesg_t3)
        desktop_pill = MacOSPill("GUI Desktop Environment Reached", color=PALETTE["blue"], is_solid=True).move_to([0, -2.4, 0])

        # Act 2: Physical Quartz Crystal Clock Oscillator
        clock_xtal = QuartzOscillator(frequency_label="3.60 GHz", scale=1.3).move_to([0, 0.5, 0])
        # Clock Sine Wave Signal
        clock_wave = FunctionGraph(
            lambda x: 0.25 * np.sin(x * 6.0),
            x_range=[-3.0, 3.0],
            color=PALETTE["blue"],
            stroke_width=2.5,
        ).move_to([0, -0.6, 0])
        clock_tag = Text("3.60 GHz Hardware Master Clock Signal", font=FONTS["mono"], font_size=12, color=PALETTE["blue"]).next_to(clock_wave, DOWN, buff=0.18)
        clock_group = VGroup(clock_xtal, clock_wave, clock_tag)
        inspect_pill = MacOSPill("Hardware Architecture Reset Vector", color=PALETTE["blue"], is_solid=True).move_to([0, -2.4, 0])

        # Act 3: 4 Boot Milestones Roadmap
        timeline = MilestoneTimeline(
            milestones=["1. FIRMWARE (POST)", "2. BOOTLOADER (GRUB)", "3. KERNEL (initramfs)", "4. USERSPACE (PID 1)"],
            length=9.5,
            y_pos=0.4,
            color=PALETTE["stroke"],
        )
        roadmap_pill = MacOSPill("Linux Boot Architecture: 4 Core Phases", color=PALETTE["indigo"], is_solid=True).move_to([0, -2.4, 0])

        # Act 4: Hero Title Window
        hero_win = TechCard(title="Linux Architecture Series", width=7.0, height=2.4, is_dark=False).move_to([0, 0.2, 0])
        hero_t1 = Text("THE LINUX BOOT PROCESS", font=FONTS["sans"], weight=BOLD, font_size=20, color=PALETTE["text"]).move_to(hero_win.body.get_center() + UP * 0.28)
        hero_t2 = Text("From Power Button Press to Userspace PID 1", font=FONTS["mono"], weight=BOLD, font_size=13, color=PALETTE["blue"]).next_to(hero_t1, DOWN, buff=0.16)
        hero_group = VGroup(hero_win, hero_t1, hero_t2)
        hero_pill = MacOSPill("Complete Systems Deep Dive", color=PALETTE["amber"], is_solid=True).move_to([0, -2.4, 0])

        # Act 5 & 6: Physical Motherboard PCB & Power Delivery
        mobo = MotherboardSection(width=7.2, height=3.6, scale=1.0).move_to([0, 0.2, 0])
        pwr_flow_dot = Dot(mobo.pcb.get_left() + RIGHT * 1.0 + DOWN * 1.0, radius=0.12, color=PALETTE["amber"])
        pwr_good_pill = MacOSPill("Power-Good Signal: +12V/+5V Rails Stabilized", color=PALETTE["amber"], is_solid=True).move_to([0, -2.4, 0])

        # Act 7: CPU SoC Wakeup on Socket & Reset Vector Address
        cpu_chip = ChipSoC(size=1.8, core_color=PALETTE["amber"]).move_to([0, 0.65, 0])
        cpu_wake_pill = MacOSPill("CPU Wakes Up: Execution Reset Vector", color=PALETTE["amber"], is_solid=True).move_to([0, -2.4, 0])
        uninit_pill = MacOSPill("RAM Uninitialized • No OS Files in Memory", color=PALETTE["coral"], is_solid=True).move_to([0, -2.4, 0])

        reset_vec_pill = MacOSPill("CS:IP = 0xFFFF:0000 ➔ 0xFFFFFFF0 (Top of 4GB Space)", color=PALETTE["blue"], is_solid=True, font_size=12, height=0.44).move_to([0, -0.75, 0])

        # Act 8 & 9: Physical SPI Flash ROM Chip & Bus Traces
        spi_rom = SpiFlashRom(scale=1.1, label="SPI FLASH ROM", sublabel="BIOS / UEFI").move_to([2.6, 0.35, 0])
        cpu_left = ChipSoC(size=1.6, core_color=PALETTE["blue"]).move_to([-2.6, 0.35, 0])
        # Bus Lines (Clock, MOSI, MISO)
        bus_line1 = Line(cpu_left.package.get_right() + UP * 0.25, spi_rom.body.get_left() + UP * 0.25, color=PALETTE["blue"], stroke_width=2.5)
        bus_line2 = Line(cpu_left.package.get_right(), spi_rom.body.get_left(), color=PALETTE["sky"], stroke_width=2.5)
        bus_line3 = Line(cpu_left.package.get_right() + DOWN * 0.25, spi_rom.body.get_left() + DOWN * 0.25, color=PALETTE["indigo"], stroke_width=2.5)
        bus_group = VGroup(bus_line1, bus_line2, bus_line3)

        bios_pill = MacOSPill("SPI Bus: 8-Pin Firmware ROM Exchanging Init Code", color=PALETTE["blue"], is_solid=True).move_to([0, -2.4, 0])

        # Act 10 - 13: Physical POST Hardware Diagnostic Testing (RAM, Storage, Chipset)
        ram_stick = RamModuleActor(scale=0.9, capacity_label="16 GB DDR5 RAM").move_to([-2.4, 0.55, 0])
        nvme_ssd = NvmeSsdActor(scale=0.9, capacity_label="1 TB NVMe PCIe SSD").move_to([2.4, 0.55, 0])
        post_cpu_tag = Text("✔ CPU Core: [ OK ]", font=FONTS["mono"], font_size=12, weight=BOLD, color=PALETTE["mint"]).move_to([-3.0, -0.65, 0])
        post_ram_tag = Text("✔ System RAM: [ 16384 MB VERIFIED ]", font=FONTS["mono"], font_size=12, weight=BOLD, color=PALETTE["mint"]).move_to([0, -0.65, 0])
        post_ssd_tag = Text("✔ NVMe Storage: [ READY TO BOOT ]", font=FONTS["mono"], font_size=12, weight=BOLD, color=PALETTE["mint"]).move_to([3.0, -0.65, 0])
        post_tags = VGroup(post_cpu_tag, post_ram_tag, post_ssd_tag)

        post_gauge = MetricGauge("POST VERIFICATION", "100%", bar_color=PALETTE["mint"]).move_to([0, -2.4, 0])

        # Act 14 & 15: Motherboard Piezo Diagnostic Speaker (Beep Codes)
        buzzer = DiagnosticSpeaker(scale=1.3).move_to([0, 0.45, 0])
        buzz_wave1 = Circle(radius=1.1, color=PALETTE["mint"], stroke_width=2.5).move_to(buzzer.housing.get_center())
        buzz_wave2 = Circle(radius=1.8, color=PALETTE["mint"], stroke_width=2.0).move_to(buzzer.housing.get_center())
        beep_pill = MacOSPill("Motherboard Piezo Speaker: 1 Short Beep (POST Success)", color=PALETTE["mint"], is_solid=True).move_to([0, -2.4, 0])
        beep_err_pill = MacOSPill("Hardware Fault Alert: POST Diagnostic Beep Sequences", color=PALETTE["coral"], is_solid=True).move_to([0, -2.4, 0])

        # Act 16 - 20: BIOS vs Modern UEFI & Storage Handoff to RAM
        # Left: Legacy BIOS representation
        bios_card = TechCard(title="Legacy BIOS (1981)", width=4.0, height=3.1, is_dark=False).move_to([-2.6, 0.4, 0])
        b_txt1 = Text("• 16-Bit Real Mode (1 MB Limit)", font=FONTS["mono"], font_size=11, color=PALETTE["text"]).move_to(bios_card.body.get_center() + UP * 0.45)
        b_txt2 = Text("• MBR Partition Table (Max 2 TB)", font=FONTS["mono"], font_size=11, color=PALETTE["coral"]).next_to(b_txt1, DOWN, buff=0.14)
        b_txt3 = Text("• Unsigned Assembly Boot Code", font=FONTS["mono"], font_size=11, color=PALETTE["coral"]).next_to(b_txt2, DOWN, buff=0.14)
        bios_cmp = VGroup(bios_card, b_txt1, b_txt2, b_txt3)

        # Right: Modern UEFI with Secure Boot Padlock
        uefi_card = TechCard(title="Modern UEFI (Unified EFI)", width=4.0, height=3.1, is_dark=False).move_to([2.6, 0.4, 0])
        u_txt1 = Text("• 64-Bit Native Execution", font=FONTS["mono"], font_size=11, color=PALETTE["blue"]).move_to(uefi_card.body.get_center() + UP * 0.45)
        u_txt2 = Text("• GPT Disks > 9 Zettabytes", font=FONTS["mono"], font_size=11, color=PALETTE["mint"]).next_to(u_txt1, DOWN, buff=0.14)
        u_txt3 = Text("• Secure Boot Cryptographic Trust", font=FONTS["mono"], font_size=11, color=PALETTE["indigo"]).next_to(u_txt2, DOWN, buff=0.14)
        padlock = CryptographicPadlock(scale=0.6).move_to(uefi_card.body.get_center() + DOWN * 0.70)
        uefi_cmp = VGroup(uefi_card, u_txt1, u_txt2, u_txt3, padlock)

        uefi_pill = MacOSPill("Modern UEFI: 64-Bit Secure Platform Firmware", color=PALETTE["blue"], is_solid=True).move_to([0, -2.4, 0])

        # Final Handoff: NVMe SSD transferring bootloader to RAM
        handoff_arrow = SleekArrow(nvme_ssd.pcb.get_left(), ram_stick.pcb.get_right(), color=PALETTE["amber"], stroke_width=3.5)
        handoff_pill = MacOSPill("Firmware Handoff: Loading Bootloader (GRUB) into RAM", color=PALETTE["amber"], is_solid=True).move_to([0, -2.4, 0])

        # =============================================================
        # 2. BEAT CHOREOGRAPHY EXECUTION (0.00s -> 152.04s)
        # =============================================================

        # -------------------------------------------------------------
        # BEAT 01: Power Button Press & Desktop Transition (0.00s -> 9.14s)
        # -------------------------------------------------------------
        # Sub 1.1 (0.00s -> 3.40s | mot: 2.72s, hld: 0.68s)
        self.beat(
            motion_time=2.72,
            hold_time=0.68,
            action=lambda: self.play(
                FadeIn(laptop, shift=UP * 0.3),
                FadeIn(pwr_dot),
                Create(pwr_pulse),
                FadeIn(pwr_pill),
                run_time=2.72,
                rate_func=ease_out_cubic,
            ),
            transient=[pwr_dot, pwr_pulse, pwr_pill],
            description="Power button press initiated on laptop workstation",
        )

        # Sub 1.2 (3.40s -> 9.14s | mot: 4.59s, hld: 1.15s)
        self.beat(
            motion_time=4.59,
            hold_time=1.15,
            action=lambda: [
                self.play(FadeIn(dmesg_group), run_time=2.30),
                self.play(FadeIn(desktop_pill), laptop.screen.animate.set_fill(PALETTE["blue"], opacity=0.8), run_time=2.29),
            ],
            transient=[laptop, dmesg_group, desktop_pill],
            description="Screen flickers, dmesg logs scroll, desktop appears",
        )

        # -------------------------------------------------------------
        # BEAT 02: Hardware Master Clock Crystal Oscillator (9.14s -> 11.94s)
        # -------------------------------------------------------------
        # Sub 2.1 (9.14s -> 11.94s | mot: 2.24s, hld: 0.56s)
        self.beat(
            motion_time=2.24,
            hold_time=0.56,
            action=lambda: [
                self.play(FadeIn(clock_xtal, scale=1.1), run_time=1.20),
                self.play(Create(clock_wave), FadeIn(clock_tag), FadeIn(inspect_pill), run_time=1.04),
            ],
            transient=[clock_group, inspect_pill],
            description="Quartz crystal master oscillator pulsing at 3.60 GHz",
        )

        # -------------------------------------------------------------
        # BEAT 03: Linux Boot Roadmap Timeline (11.94s -> 21.36s)
        # -------------------------------------------------------------
        # Sub 3.1 (11.94s -> 21.36s | mot: 7.92s, hld: 1.50s)
        self.beat(
            motion_time=7.92,
            hold_time=1.50,
            action=lambda: [
                self.play(Create(timeline.line), run_time=2.50),
                self.play(FadeIn(timeline.markers), FadeIn(timeline.labels), run_time=2.80),
                self.play(FadeIn(roadmap_pill), run_time=2.62),
            ],
            transient=[timeline, roadmap_pill],
            description="4 Boot Milestones Roadmap displayed",
        )

        # -------------------------------------------------------------
        # BEAT 04: Hero Title Card (21.36s -> 27.92s)
        # -------------------------------------------------------------
        # Sub 4.1 (21.36s -> 27.92s | mot: 5.25s, hld: 1.31s)
        self.beat(
            motion_time=5.25,
            hold_time=1.31,
            action=lambda: [
                self.play(FadeIn(hero_win, scale=1.05), run_time=2.60),
                self.play(FadeIn(hero_t1), FadeIn(hero_t2), FadeIn(hero_pill), run_time=2.65),
            ],
            transient=[hero_group, hero_pill],
            description="Hero title card: The Linux Boot Process",
        )

        # -------------------------------------------------------------
        # BEAT 05 & 06: Motherboard Power Planes & Voltage Surge (27.92s -> 34.14s)
        # -------------------------------------------------------------
        # Sub 5.1 (27.92s -> 30.78s | mot: 2.29s, hld: 0.57s)
        self.beat(
            motion_time=2.29,
            hold_time=0.57,
            action=lambda: self.play(FadeIn(mobo, scale=1.05), run_time=2.29),
            description="Stage reset: Inside the computer on the Motherboard PCB",
        )

        # Sub 6.1 (30.78s -> 34.14s | mot: 2.69s, hld: 0.67s)
        self.beat(
            motion_time=2.69,
            hold_time=0.67,
            action=lambda: [
                self.play(FadeIn(pwr_flow_dot), mobo.pwr_led.animate.set_color(PALETTE["mint"]), run_time=1.35),
                self.play(pwr_flow_dot.animate.move_to(mobo.pcb.get_center()), FadeIn(pwr_good_pill), run_time=1.34),
            ],
            transient=[mobo, pwr_flow_dot, pwr_good_pill],
            description="Power delivery: ATX rails stabilize, Power-Good signal triggers",
        )

        # -------------------------------------------------------------
        # BEAT 07: CPU SoC Wakeup & Hardware Reset Vector (34.14s -> 52.86s)
        # -------------------------------------------------------------
        # Sub 7.1 (34.14s -> 40.70s | mot: 5.25s, hld: 1.31s)
        self.beat(
            motion_time=5.25,
            hold_time=1.31,
            action=lambda: [
                self.play(FadeIn(cpu_chip, scale=1.1), run_time=2.60),
                self.play(FadeIn(cpu_wake_pill), cpu_chip.die_core.animate.scale(1.4), run_time=2.65),
            ],
            transient=[cpu_wake_pill],
            description="CPU awakens in socket; die core illuminates",
        )

        # Sub 7.2 (40.70s -> 45.70s | mot: 4.00s, hld: 1.00s)
        self.beat(
            motion_time=4.00,
            hold_time=1.00,
            action=lambda: self.play(FadeIn(uninit_pill), run_time=4.00),
            transient=[uninit_pill],
            description="CPU has no OS understanding or RAM loaded",
        )

        # Sub 7.3 (45.70s -> 52.86s | mot: 5.73s, hld: 1.43s)
        self.beat(
            motion_time=5.73,
            hold_time=1.43,
            action=lambda: self.play(
                FadeIn(reset_vec_pill, shift=UP * 0.2),
                cpu_chip.die.animate.set_stroke(PALETTE["blue"], width=2.5),
                run_time=5.73,
                rate_func=ease_out_cubic,
            ),
            transient=[cpu_chip, reset_vec_pill],
            description="Hardware Reset Vector executed at 0xFFFFFFF0",
        )

        # -------------------------------------------------------------
        # BEAT 08 & 09: Physical SPI Flash ROM Chip & Bus Traces (52.86s -> 68.12s)
        # -------------------------------------------------------------
        # Sub 8.1 (52.86s -> 61.40s | mot: 7.04s, hld: 1.50s)
        self.beat(
            motion_time=7.04,
            hold_time=1.50,
            action=lambda: [
                self.play(FadeIn(cpu_left), FadeIn(spi_rom), run_time=3.50),
                self.play(Create(bus_group), FadeIn(bios_pill), run_time=3.54),
            ],
            description="Initial instructions lead to physical SPI Flash ROM chip",
        )

        # Sub 9.1 (61.40s -> 68.12s | mot: 5.38s, hld: 1.34s)
        packet_pulse = Dot(bus_line2.get_right(), radius=0.10, color=PALETTE["blue"])
        self.beat(
            motion_time=5.38,
            hold_time=1.34,
            action=lambda: [
                self.play(FadeIn(packet_pulse), run_time=1.50),
                self.play(packet_pulse.animate.move_to(bus_line2.get_left()), run_time=3.88),
            ],
            transient=[cpu_left, spi_rom, bus_group, packet_pulse, bios_pill],
            description="BIOS firmware code fetched over high-speed SPI bus",
        )

        # -------------------------------------------------------------
        # BEAT 10 - 13: POST Hardware Verification (RAM, Storage, CPU) (68.12s -> 97.38s)
        # -------------------------------------------------------------
        # Sub 10.1 (68.12s -> 71.50s | mot: 2.70s, hld: 0.68s)
        self.beat(
            motion_time=2.70,
            hold_time=0.68,
            action=lambda: self.play(
                FadeIn(ram_stick, shift=RIGHT * 0.3),
                FadeIn(nvme_ssd, shift=LEFT * 0.3),
                run_time=2.70,
                rate_func=ease_out_cubic,
            ),
            description="Motherboard components entered for POST diagnostic verification",
        )

        # Sub 11.1 (71.50s -> 80.68s | mot: 7.68s, hld: 1.50s)
        self.beat(
            motion_time=7.68,
            hold_time=1.50,
            action=lambda: [
                # Sequential verification illumination of DRAM chips
                self.play(*[c[0].animate.set_fill(PALETTE["mint"], opacity=0.7) for c in ram_stick.chips[:2]], run_time=3.80),
                self.play(*[c[0].animate.set_fill(PALETTE["mint"], opacity=0.7) for c in ram_stick.chips[2:]], run_time=3.88),
            ],
            description="System RAM memory banks verified OK",
        )

        # Sub 12.1 (80.68s -> 90.18s | mot: 8.00s, hld: 1.50s)
        self.beat(
            motion_time=8.00,
            hold_time=1.50,
            action=lambda: [
                self.play(FadeIn(post_ram_tag), run_time=2.60),
                self.play(nvme_ssd.led.animate.set_color(PALETTE["mint"]), FadeIn(post_ssd_tag), run_time=2.70),
                self.play(FadeIn(post_cpu_tag), run_time=2.70),
            ],
            description="Storage controller and processor confirmed ready",
        )

        # Sub 13.1 (90.18s -> 97.38s | mot: 5.76s, hld: 1.44s)
        self.beat(
            motion_time=5.76,
            hold_time=1.44,
            action=lambda: self.play(FadeIn(post_gauge), run_time=5.76),
            transient=[ram_stick, nvme_ssd, post_tags, post_gauge],
            description="POST verification reaches 100% verified status",
        )

        # -------------------------------------------------------------
        # BEAT 14 & 15: Motherboard Piezo Diagnostic Speaker (97.38s -> 112.14s)
        # -------------------------------------------------------------
        # Sub 14.1 (97.38s -> 105.52s | mot: 6.64s, hld: 1.50s)
        self.beat(
            motion_time=6.64,
            hold_time=1.50,
            action=lambda: [
                self.play(FadeIn(buzzer), FadeIn(beep_err_pill), run_time=3.30),
                self.play(Create(buzz_wave2), run_time=3.34),
            ],
            transient=[beep_err_pill],
            description="Diagnostic error beep codes explained",
        )

        # Sub 15.1 (105.52s -> 112.14s | mot: 5.30s, hld: 1.32s)
        self.beat(
            motion_time=5.30,
            hold_time=1.32,
            action=lambda: [
                self.play(Create(buzz_wave1), FadeIn(beep_pill), run_time=2.65),
                self.play(FadeOut(buzz_wave1), FadeOut(buzz_wave2), run_time=2.65),
            ],
            transient=[buzzer, beep_pill],
            description="Single short beep: All hardware checks passed",
        )

        # -------------------------------------------------------------
        # BEAT 16 - 20: Legacy BIOS vs Modern UEFI & Storage Handoff (112.14s -> 152.04s)
        # -------------------------------------------------------------
        # Sub 16.1 (112.14s -> 117.28s | mot: 4.11s, hld: 1.03s)
        self.beat(
            motion_time=4.11,
            hold_time=1.03,
            action=lambda: self.play(FadeIn(uefi_cmp), run_time=4.11),
            description="Modern computers transition to UEFI platform",
        )

        # Sub 17.1 (117.28s -> 121.54s | mot: 3.41s, hld: 0.85s)
        self.beat(
            motion_time=3.41,
            hold_time=0.85,
            action=lambda: self.play(FadeIn(uefi_pill), run_time=3.41),
            transient=[uefi_pill],
            description="UEFI acronym expansion",
        )

        # Sub 18.1 (121.54s -> 126.88s | mot: 4.27s, hld: 1.07s)
        self.beat(
            motion_time=4.27,
            hold_time=1.07,
            action=lambda: [
                self.play(FadeIn(bios_cmp), run_time=2.13),
                self.play(padlock.shackle.animate.shift(DOWN * 0.12), run_time=2.14),
            ],
            description="UEFI capabilities: GPT disks > 9ZB, Secure Boot Cryptographic lock",
        )

        # Sub 19.1 (126.88s -> 141.68s | mot: 13.30s, hld: 1.50s)
        uefi_mgmt_pill = MacOSPill("Modern UEFI: Digital Platform Management Architecture", color=PALETTE["mint"], is_solid=True).move_to([0, -2.4, 0])
        self.beat(
            motion_time=13.30,
            hold_time=1.50,
            action=lambda: [
                self.play(FadeIn(uefi_mgmt_pill), run_time=4.00),
                self.play(u_txt1.animate.set_color(PALETTE["amber"]), run_time=4.00),
                self.play(u_txt2.animate.set_color(PALETTE["amber"]), run_time=5.30),
            ],
            transient=[bios_cmp, uefi_cmp, uefi_mgmt_pill],
            description="Paper checklist vs Digital Management System comparison",
        )

        # Sub 20.1 (141.68s -> 152.04s | mot: 8.86s, hld: 1.50s)
        # Final Handoff: NVMe SSD transferring bootloader code into RAM
        handoff_ram = RamModuleActor(scale=0.85, capacity_label="16 GB RAM").move_to([-2.6, 0.4, 0])
        handoff_ssd = NvmeSsdActor(scale=0.85, capacity_label="NVMe Boot Device").move_to([2.6, 0.4, 0])
        boot_packet = Rectangle(width=0.55, height=0.35, color=PALETTE["stroke"], fill_color=PALETTE["amber"], fill_opacity=1.0).move_to(handoff_ssd.pcb.get_center())
        boot_tag = Text("GRUB", font=FONTS["mono"], font_size=10, weight=BOLD, color=PALETTE["text_light"]).move_to(boot_packet.get_center())
        boot_block = VGroup(boot_packet, boot_tag)

        self.beat(
            motion_time=8.86,
            hold_time=1.50,
            action=lambda: [
                self.play(FadeIn(handoff_ram), FadeIn(handoff_ssd), FadeIn(handoff_pill), run_time=3.00),
                self.play(FadeIn(boot_block), run_time=1.50),
                self.play(boot_block.animate.move_to(handoff_ram.pcb.get_center()), run_time=4.36),
            ],
            description="Both initialize platform; handoff to secondary storage boot device",
        )

        self.finalize()
