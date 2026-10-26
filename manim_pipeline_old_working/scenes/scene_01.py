#!/usr/bin/env python3
"""
scenes/scene_01.py
Topic: The Linux Boot Process: From Power Button to PID 1
Scene 01: Power On & The Reset Vector (0.00s -> 61.77s)
Style: Broadcast-Grade Editorial Vector Infographics, Warm Off-White Canvas (#F8F9FA),
       Mathematically Exact Zero-Drift Synchronization, Collision-Free Physical Hardware Actors.
"""
from manim import *
import numpy as np

from engine_2d import (
    EditorialScene,
    PALETTE,
    FONT_SIZES,
    FONTS,
    MacBookDevice,
    MotherboardSection,
    ChipSoC,
    QuartzOscillator,
    SpiFlashRom,
    MacOSPill,
    TechCard,
    MilestoneTimeline,
)


class Scene01(EditorialScene):
    def construct(self):
        self.target_duration = 61.77  # Exact duration from timed_storyboard.json

        # =========================================================================
        # 1. OUTER-SCOPE VARIABLE DECLARATIONS (Spatially Isolated Regions)
        # =========================================================================

        # --- Beat 1.1: Laptop Workstation & Kernel Console Window ---
        # Symmetrical side-by-side layout: Laptop on left, Kernel Console on right
        laptop = MacBookDevice(scale=1.05, url_text="Linux Kernel 6.8", show_traffic_lights=False).move_to([-2.6, -0.2, 0.0])
        pwr_dot = Dot(laptop.base.get_top() + RIGHT * 0.90, radius=0.06, color=PALETTE["mint"])
        pwr_pulse = Circle(radius=0.18, color=PALETTE["mint"], stroke_width=2.0).move_to(pwr_dot.get_center())

        log_card = TechCard(title="Kernel Console [tty1]", width=4.5, height=2.4, is_dark=False).move_to([2.4, -0.2, 0.0])
        log_t1 = Text("[  0.000000] Linux version 6.8.0-generic", font=FONTS["mono"], font_size=11, color=PALETTE["blue"]).move_to(log_card.body.get_center() + UP * 0.45)
        log_t2 = Text("[  0.001240] Command line: BOOT_IMAGE=/vmlinuz ...", font=FONTS["mono"], font_size=10, color=PALETTE["text"]).next_to(log_t1, DOWN, buff=0.14)
        log_t3 = Text("[  0.045100] x86/fpu: Supporting XSAVE feature 0x001", font=FONTS["mono"], font_size=10, color=PALETTE["mint"]).next_to(log_t2, DOWN, buff=0.14)
        log_group = VGroup(log_card, log_t1, log_t2, log_t3)

        # --- Beat 1.2: Motherboard PCB & 4 Boot Milestones Roadmap ---
        # Roadmap sits at top (y=2.5) with all_up=True so labels have 1.1 units of clear space above motherboard
        timeline = MilestoneTimeline(
            milestones=["1. FIRMWARE (POST)", "2. BOOTLOADER (GRUB)", "3. KERNEL (initramfs)", "4. PID 1 (systemd)"],
            length=10.2,
            y_pos=2.5,
            color=PALETTE["stroke"],
            all_up=True,
        )
        mobo = MotherboardSection(width=8.6, height=4.0, scale=1.0).move_to([0.0, -0.6, 0.0])
        cpu_chip = ChipSoC(size=1.8, core_color=PALETTE["amber"]).move_to([0.0, -0.6, 0.0])

        # --- Beat 1.3: Hardware Master Clock & Power Delivery ---
        # Quartz Oscillator sits cleanly in upper-left quadrant of motherboard
        clock_crystal = QuartzOscillator(frequency_label="3.60 GHz", scale=0.88).move_to([-2.6, 0.4, 0.0])
        clock_wave = FunctionGraph(
            lambda x: 0.15 * np.sin(x * 8.0),
            x_range=[-1.0, 1.0],
            color=PALETTE["blue"],
            stroke_width=2.4,
        ).move_to([-2.6, -0.2, 0.0])

        # Trace running from clock crystal to CPU
        clock_trace = Line(clock_crystal.get_right(), cpu_chip.get_left(), color=PALETTE["stroke_light"], stroke_width=2.5)

        # --- Beat 1.5: SPI Flash ROM & Reset Vector Bus ---
        # Ample clearance between CPU on left and SPI ROM on right
        bios_rom = SpiFlashRom(scale=1.05, label="SPI FLASH ROM", sublabel="BIOS / UEFI").move_to([2.7, -0.6, 0.0])
        spi_bus_line = Line(
            [-1.5, -0.6, 0.0],
            [1.7, -0.6, 0.0],
            color=PALETTE["stroke_light"],
            stroke_width=3.5,
        )
        spi_pulse_dot = Dot(radius=0.09, color=PALETTE["sky"]).move_to(spi_bus_line.get_start())
        # Positioned with ample clearance at y=0.95
        reset_vector_pill = MacOSPill(
            "RESET VECTOR: 0xFFFFFFF0 (Top of 4GB Space)",
            color=PALETTE["blue"],
            is_solid=True,
            font_size=11,
            height=0.40
        ).move_to([0.5, 0.95, 0.0])

        # =========================================================================
        # 2. CHOREOGRAPHED BEATS (Zero-Drift Narration Lock)
        # =========================================================================

        # -------------------------------------------------------------------------
        # BEAT 1.1 (0.00s - 9.38s | Motion: 7.58s | Hold: 1.80s)
        # "Have you ever pressed that power button on your Linux machine..."
        # -------------------------------------------------------------------------
        def act_1_1():
            self.play(
                FadeIn(laptop, shift=UP * 0.3),
                FadeIn(log_group, shift=LEFT * 0.3),
                run_time=1.80
            )
            self.play(
                FadeIn(pwr_dot),
                pwr_pulse.animate.scale(2.2).set_opacity(0.0),
                run_time=1.60
            )
            self.play(
                log_t1.animate.set_color(PALETTE["indigo"]),
                log_t2.animate.set_color(PALETTE["text"]),
                run_time=2.00
            )
            self.play(
                log_t3.animate.set_color(PALETTE["mint"]),
                run_time=2.18
            )

        self.beat(
            "1.1",
            "Have you ever pressed that power button on your Linux machine and wondered: what is actually happening right now? In just a few seconds, your computer goes from cold, dead silicon to a fully running operating system, ready for your commands.",
            act_1_1,
            motion_time=7.58,
            hold_time=1.80,
            transient=[
                {"type": "badge", "text": "ACPI POWER-ON EVENT • COLD BOOT", "position": [0.0, -3.1], "fill_token": "indigo", "text_color": "#FFFFFF"}
            ]
        )

        # -------------------------------------------------------------------------
        # BEAT 1.2 (9.38s - 28.26s | Motion: 17.08s | Hold: 1.80s)
        # "But what actually happened during those few seconds? ... This is the Linux boot process..."
        # -------------------------------------------------------------------------
        def act_1_2():
            self.play(
                FadeOut(laptop, shift=DOWN * 0.3),
                FadeOut(pwr_dot),
                FadeOut(log_group, shift=DOWN * 0.3),
                run_time=2.00
            )
            self.play(
                FadeIn(mobo, scale=0.95),
                FadeIn(cpu_chip, scale=0.95),
                run_time=3.00
            )
            self.play(FadeIn(timeline, shift=DOWN * 0.2), run_time=2.50)
            self.play(
                timeline.dots[0].animate.set_color(PALETTE["indigo"]).scale(1.35),
                run_time=4.00
            )
            self.play(
                cpu_chip.die.animate.set_stroke(PALETTE["stroke_light"], width=2.5),
                run_time=5.58
            )

        self.beat(
            "1.2",
            "But what actually happened during those few seconds? Today, we're going on a journey inside your computer, from the very moment you press that power button all the way to the beautiful desktop you're staring at. Buckle up! This is the Linux boot process, and it's honestly one of the coolest things happening right under your nose.",
            act_1_2,
            motion_time=17.08,
            hold_time=1.80,
            transient=[
                {"type": "badge", "text": "LINUX BOOT SEQUENCE: 4 CORE PHASES", "position": [0.0, -3.1], "fill_token": "indigo", "text_color": "#FFFFFF"}
            ]
        )

        # -------------------------------------------------------------------------
        # BEAT 1.3 (28.26s - 34.62s | Motion: 5.09s | Hold: 1.27s)
        # "So, let's start at the very beginning. The moment you press the power button, what happens first?"
        # -------------------------------------------------------------------------
        def act_1_3():
            # CPU shifts slightly to [0.8, -0.6] for power subsystem balance
            self.play(
                cpu_chip.animate.move_to([0.8, -0.6, 0.0]),
                run_time=1.50
            )
            # Power-Good LED illuminates amber, oscillator & wave appear cleanly in upper left
            self.play(
                mobo.pwr_led.animate.set_fill(PALETTE["amber"], opacity=1.0).set_color(PALETTE["amber"]),
                FadeIn(clock_crystal, shift=DOWN * 0.2),
                Create(clock_trace),
                run_time=1.50
            )
            # Master clock locks frequency and sine wave creates
            self.play(
                Create(clock_wave),
                clock_crystal.animate.scale(1.04),
                run_time=2.09
            )

        self.beat(
            "1.3",
            "So, let's start at the very beginning. The moment you press the power button, what happens first?",
            act_1_3,
            motion_time=5.09,
            hold_time=1.27,
            transient=[
                {"type": "badge", "text": "POWER-GOOD SIGNAL: +3.3V / +5V / +12V STABILIZED", "position": [0.0, -3.1], "fill_token": "amber", "text_color": "#1A202C"},
                {"type": "annotation", "text": "3.60 GHz MASTER CLOCK LOCK", "position": [-2.6, -0.6], "color_token": "text_light"}
            ]
        )

        # -------------------------------------------------------------------------
        # BEAT 1.4 (34.62s - 46.01s | Motion: 9.59s | Hold: 1.80s)
        # "The CPU wakes up. But here's the thing: the CPU doesn't immediately know how to start Linux..."
        # -------------------------------------------------------------------------
        def act_1_4():
            # Pulse flows along clock/power trace into the CPU socket
            pwr_dot = Dot(radius=0.10, color=PALETTE["amber"]).move_to(clock_trace.get_start())
            self.play(
                FadeIn(pwr_dot),
                pwr_dot.animate.move_to(clock_trace.get_end()),
                run_time=2.50
            )
            # CPU silicon core energizes bright amber
            self.play(
                FadeOut(pwr_dot),
                cpu_chip.core.animate.set_color(PALETTE["amber"]),
                cpu_chip.die.animate.set_stroke(PALETTE["amber"], width=3.0),
                run_time=3.50
            )
            # CPU is awake, but system memory is uninitialized
            self.play(
                cpu_chip.core.animate.scale(1.2),
                run_time=3.59
            )

        self.beat(
            "1.4",
            "The CPU wakes up. But here's the thing: the CPU doesn't immediately know how to start Linux. It doesn't automatically understand your operating system or know which files to load.",
            act_1_4,
            motion_time=9.59,
            hold_time=1.80,
            transient=[
                {"type": "badge", "text": "CPU WAKES • SYSTEM RAM IS EMPTY (NO OS IN MEMORY)", "position": [0.0, -3.1], "fill_token": "coral", "text_color": "#FFFFFF"}
            ]
        )

        # -------------------------------------------------------------------------
        # BEAT 1.5 (46.01s - 61.77s | Motion: 13.96s | Hold: 1.80s)
        # "Instead, it begins executing instructions from a predefined location..."
        # -------------------------------------------------------------------------
        def act_1_5():
            # Cleanly dissolve clock crystal & trace to prepare spacious CPU <-> SPI ROM stage
            self.play(
                FadeOut(clock_crystal),
                FadeOut(clock_wave),
                FadeOut(clock_trace),
                run_time=2.00
            )
            # CPU moves to [-2.5, -0.6], SPI ROM appears at [2.7, -0.6], SPI bus is drawn
            self.play(
                cpu_chip.animate.move_to([-2.5, -0.6, 0.0]),
                FadeIn(bios_rom, shift=LEFT * 0.4),
                Create(spi_bus_line),
                run_time=2.50
            )
            # Reset Vector Callout Badge appears high above the bus at y=0.9
            self.play(FadeIn(reset_vector_pill, shift=DOWN * 0.2), run_time=1.50)
            # Reset Vector pulse travels along SPI bus toward Flash ROM
            spi_pulse_dot.move_to(spi_bus_line.get_start())
            self.play(
                FadeIn(spi_pulse_dot),
                spi_pulse_dot.animate.move_to(spi_bus_line.get_end()),
                run_time=3.00
            )
            # SPI Flash ROM illuminates with Indigo firmware halo
            self.play(
                bios_rom.animate.set_color(PALETTE["indigo"]),
                run_time=2.00
            )
            # Firmware instruction stream flows back into CPU
            self.play(
                spi_pulse_dot.animate.set_color(PALETTE["indigo"]).move_to(spi_bus_line.get_start()),
                run_time=2.96
            )

        self.beat(
            "1.5",
            "Instead, it begins executing instructions from a predefined location, determined by its hardware architecture. Those initial instructions lead it to firmware stored on your motherboard, commonly known as BIOS or, on modern systems, UEFI.",
            act_1_5,
            motion_time=13.96,
            hold_time=1.80,
            transient=[
                {"type": "annotation", "text": "SPI BUS CONDUIT • MEMORY-MAPPED I/O", "position": [0.3, -1.6], "color_token": "text_light"}
            ]
        )
