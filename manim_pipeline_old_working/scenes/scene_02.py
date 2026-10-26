from manim import *
from engine_2d.theme import PALETTE, FONT_SIZES
from engine_2d.scene import EditorialScene
from engine_2d.objects import (
    SpiFlashRom,
    ChipSoC,
    RamModuleActor,
    NvmeSsdActor,
    DiagnosticSpeaker,
)

class Scene02(EditorialScene):
    def construct(self):
        self.target_duration = 51.19

        # =========================================================================
        # OUTER-SCOPE VARIABLE DECLARATION (Zero-Bug Mandate)
        # =========================================================================
        
        # Scene 2.1 Actors
        bios_rom = SpiFlashRom().move_to([-3.2, 0.5, 0.0])
        cpu_core = ChipSoC().move_to([0.0, 1.2, 0.0])
        ddr5_dimm = RamModuleActor().move_to([0.0, -1.0, 0.0])
        nvme_drive = NvmeSsdActor().move_to([3.2, 0.0, 0.0])

        # Scene 2.4 Additional Actors
        piezo_buzzer = DiagnosticSpeaker().move_to([3.2, -1.0, 0.0])

        # =========================================================================
        # BEAT 2.1 (61.77s - 72.27s, motion: 8.7s)
        # =========================================================================
        def act_2_1():
            self.play(
                FadeIn(bios_rom),
                FadeIn(cpu_core),
                FadeIn(ddr5_dimm),
                FadeIn(nvme_drive),
                run_time=2.0
            )
            # Epox encapsulation semi-transparent / sequencer spin-up
            self.play(
                bios_rom.animate.set_color(PALETTE["accents"]["indigo"]),
                run_time=6.7
            )
            self.wait(1.8)

        self.beat(
            "2.1",
            "BIOS stands for Basic Input/Output System. It's been around since the early days of personal computing. Think of BIOS as the computer's morning checklist manager.",
            act_2_1,
            motion_time=8.7,
            hold_time=1.8,
            transient=[
                {"type": "badge", "text": "BIOS: Basic Input/Output System", "position": [-2.5, 2.2], "fill_token": "indigo", "text_color": "#FFFFFF"}
            ]
        )

        # =========================================================================
        # BEAT 2.2 (72.27s - 82.39s, motion: 8.32s)
        # =========================================================================
        def act_2_2():
            self.play(
                bios_rom.animate.fire_diagnostic_pulses(
                    [cpu_core, ddr5_dimm], 
                    color=PALETTE["accents"]["blue"]
                ),
                run_time=8.32
            )
            self.wait(1.8)

        self.beat(
            "2.2",
            "As the motherboard powers up, the firmware begins initializing essential hardware and performs a test called POST, which stands for Power-On Self-Test.",
            act_2_2,
            motion_time=8.32,
            hold_time=1.8,
            transient=[
                {"type": "badge", "text": "POST: Power-On Self-Test", "position": [0.0, 2.3], "fill_token": "surface_card", "border_token": "border_stroke", "text_color": "#1A202C"}
            ]
        )

        # =========================================================================
        # BEAT 2.3 (82.39s - 98.79s, motion: 14.6s)
        # =========================================================================
        def act_2_3():
            self.play(
                cpu_core.animate.set_color(PALETTE["accents"]["mint"]),
                run_time=3.0
            )
            self.play(
                ddr5_dimm.animate.verify_chips(color=PALETTE["accents"]["mint"]),
                run_time=8.0
            )
            self.play(
                nvme_drive.animate.flash_controller(color=PALETTE["accents"]["mint"]),
                run_time=3.6
            )
            self.wait(1.8)

        self.beat(
            "2.3",
            "It checks whether essential components are responding correctly. Is the RAM accessible? Is the processor functioning? Are critical hardware devices available? The exact checks depend on the system, but the goal is the same: make sure the computer can proceed with startup.",
            act_2_3,
            motion_time=14.6,
            hold_time=1.8,
            transient=[
                {"type": "badge", "text": "HARDWARE VERIFIED", "position": [0.0, 2.3], "fill_token": "mint", "text_color": "#FFFFFF"}
            ]
        )

        # =========================================================================
        # BEAT 2.4 (98.79s - 112.96s, motion: 12.37s)
        # =========================================================================
        def act_2_4():
            self.play(
                FadeIn(piezo_buzzer),
                run_time=1.0
            )
            self.play(
                ddr5_dimm.animate.trigger_fault(chip_index=5, color=PALETTE["accents"]["coral"]),
                piezo_buzzer.animate.emit_acoustic_waves(color=PALETTE["accents"]["coral"]),
                run_time=9.57
            )
            self.play(
                ddr5_dimm.animate.reset_chip(chip_index=5, color=PALETTE["accents"]["mint"]),
                run_time=1.8
            )
            self.wait(1.8)

        self.beat(
            "2.4",
            "If something goes wrong, you might hear beep codes, see an error message, or notice that the computer refuses to continue booting. In other words, your computer is performing an initial health check before handing control to the next stage.",
            act_2_4,
            motion_time=12.37,
            hold_time=1.8,
            transient=[
                {"type": "annotation", "text": "POST FAULT: BEEP CODE", "position": [3.2, 0.2], "color_token": "coral"}
            ]
        )
