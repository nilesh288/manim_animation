from manim import *
from engine_2d.theme import PALETTE, FONT_SIZES
from engine_2d.scene import EditorialScene
from engine_2d.objects import (
    MacBookDevice,
    MotherboardSection,
    ChipSoC,
    ATX24PinConnector,
    CapacitorBank,
    QuartzOscillator,
    SpiFlashRom,
)

class Scene01(EditorialScene):
    def construct(self):
        self.target_duration = 61.77

        # =========================================================================
        # OUTER-SCOPE VARIABLE DECLARATION (Zero-Bug Mandate)
        # =========================================================================
        
        # Scene 1.1 Actors
        workstation_laptop = MacBookDevice().move_to([0.0, -0.3, 0.0])

        # Scene 1.2 Actors
        main_pcb = MotherboardSection()
        cpu_socket = ChipSoC().move_to([0.0, 0.0, 0.0])

        # Scene 1.3 Additional Actors
        atx_power = ATX24PinConnector().move_to([-4.5, 0.0, 0.0])
        vrm_caps = CapacitorBank().move_to([-2.5, 0.8, 0.0])
        clock_crystal = QuartzOscillator().move_to([-2.2, -1.2, 0.0])

        # Scene 1.5 Additional Actors
        bios_uefi_rom = SpiFlashRom().move_to([2.8, 0.2, 0.0])

        # =========================================================================
        # BEAT 1.1 (0.00s - 9.38s, motion: 7.58s)
        # =========================================================================
        def act_1_1():
            self.play(
                FadeIn(workstation_laptop, shift=DOWN * 0.5),
                run_time=2.0
            )
            # Mechanical display panel flicker & workspace illumination
            self.play(
                workstation_laptop.animate.flicker_screen(color=PALETTE["accents"]["sky"]),
                run_time=3.58
            )
            self.wait(1.8)

        self.beat(
            "1.1",
            "Have you ever pressed that power button on your Linux machine and just waited? The screen flickers, some text scrolls by, and then, boom! Your desktop appears.",
            act_1_1,
            motion_time=7.58,
            hold_time=1.8,
            transient=[]
        )

        # =========================================================================
        # BEAT 1.2 (9.38s - 28.26s, motion: 17.08s)
        # =========================================================================
        def act_1_2():
            # Aluminum chassis lifts away vertically, exposing main_pcb & cpu_socket
            self.play(
                workstation_laptop.animate.shift(UP * 2.1).set_opacity(0.3),
                FadeIn(main_pcb),
                FadeIn(cpu_socket),
                run_time=4.0
            )
            self.play(
                cpu_socket.animate.set_state("unpowered"),
                run_time=11.28
            )
            self.wait(1.8)

        self.beat(
            "1.2",
            "But what actually happened during those few seconds? Today, we're going on a journey inside your computer, from the very moment you press that power button all the way to the beautiful desktop you're staring at. Buckle up! This is the Linux boot process, and it's honestly one of the coolest things happening right under your nose.",
            act_1_2,
            motion_time=17.08,
            hold_time=1.8,
            transient=[
                {"type": "badge", "text": "LINUX BOOT SEQUENCE", "position": [0.0, 2.3], "fill_token": "indigo", "text_color": "#FFFFFF"}
            ]
        )

        # =========================================================================
        # BEAT 1.3 (28.26s - 34.62s, motion: 5.09s)
        # =========================================================================
        def act_1_3():
            self.play(
                FadeIn(atx_power, shift=RIGHT * 0.5),
                FadeIn(vrm_caps),
                FadeIn(clock_crystal),
                run_time=1.5
            )
            self.play(
                atx_power.animate.set_color(PALETTE["accents"]["amber"]),
                vrm_caps.animate.charge_capacitors(),
                clock_crystal.animate.emit_pulses(color=PALETTE["accents"]["blue"]),
                run_time=3.59
            )
            self.wait(1.27)

        self.beat(
            "1.3",
            "So, let's start at the very beginning. The moment you press the power button, what happens first?",
            act_1_3,
            motion_time=5.09,
            hold_time=1.27,
            transient=[
                {"type": "annotation", "text": "3.3V / 5V / 12V RAILS", "position": [-3.4, 1.5], "color_token": "text_primary"},
                {"type": "annotation", "text": "CLK LOCK", "position": [-1.2, -1.8], "color_token": "blue"}
            ]
        )

        # =========================================================================
        # BEAT 1.4 (34.62s - 46.01s, motion: 9.59s)
        # =========================================================================
        def act_1_4():
            self.play(
                clock_crystal.animate.strike_perimeter(cpu_socket),
                run_time=3.0
            )
            self.play(
                cpu_socket.animate.set_color(PALETTE["accents"]["amber"]),
                run_time=4.89
            )
            self.wait(1.8)

        self.beat(
            "1.4",
            "The CPU wakes up. But here's the thing: the CPU doesn't immediately know how to start Linux. It doesn't automatically understand your operating system or know which files to load.",
            act_1_4,
            motion_time=9.59,
            hold_time=1.8,
            transient=[]
        )

        # =========================================================================
        # BEAT 1.5 (46.01s - 61.77s, motion: 13.96s)
        # =========================================================================
        def act_1_5():
            # Reposition CPU slightly to leave room for SPI ROM
            self.play(
                cpu_socket.animate.move_to([-1.8, 0.2, 0.0]),
                FadeIn(bios_uefi_rom.move_to([2.8, 0.2, 0.0])),
                run_time=2.5
            )
            self.play(
                cpu_socket.animate.fire_reset_vector(bios_uefi_rom, color=PALETTE["accents"]["sky"]),
                run_time=8.16
            )
            self.wait(1.8)

        self.beat(
            "1.5",
            "Instead, it begins executing instructions from a predefined location, determined by its hardware architecture. Those initial instructions lead it to firmware stored on your motherboard, commonly known as BIOS or, on modern systems, UEFI.",
            act_1_5,
            motion_time=13.96,
            hold_time=1.8,
            transient=[
                {"type": "annotation", "text": "0xFFFFFFF0", "position": [-1.8, 1.5], "color_token": "text_primary"},
                {"type": "annotation", "text": "SPI BUS", "position": [0.5, 0.6], "color_token": "text_dim"}
            ]
        )
