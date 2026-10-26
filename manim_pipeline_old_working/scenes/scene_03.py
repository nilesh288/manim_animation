from manim import *
from engine_2d.theme import PALETTE, FONT_SIZES
from engine_2d.scene import EditorialScene
from engine_2d.objects import (
    SpiFlashRom,
    NvmeSsdActor,
    CryptographicPadlock,
    MechanicalStepperRelay,
    CrossbarRoutingMatrix,
)

class Scene03(EditorialScene):
    def construct(self):
        self.target_duration = 41.73

        # =========================================================================
        # OUTER-SCOPE VARIABLE DECLARATION (Zero-Bug Mandate)
        # =========================================================================
        
        # Scene 3.1 Actors
        legacy_dip_rom = SpiFlashRom(variant="vintage_dip_package").move_to([-2.8, 0.0, 0.0])
        modern_uefi_rom = SpiFlashRom(variant="wson_low_profile").move_to([2.8, 0.0, 0.0])

        # Scene 3.2 Additional Actors
        gpt_nvme_drive = NvmeSsdActor().move_to([1.8, 0.8, 0.0])
        secure_boot_lock = CryptographicPadlock().move_to([1.8, -1.0, 0.0])

        # Scene 3.3 Additional Actors
        bios_stepper = MechanicalStepperRelay().move_to([-2.8, 0.0, 0.0])
        uefi_router_matrix = CrossbarRoutingMatrix().move_to([2.2, 0.0, 0.0])

        # =========================================================================
        # BEAT 3.1 (112.96s - 123.09s, motion: 8.33s)
        # =========================================================================
        def act_3_1():
            self.play(
                FadeIn(legacy_dip_rom),
                FadeIn(modern_uefi_rom),
                run_time=2.0
            )
            self.play(
                legacy_dip_rom.animate.stream_legacy_bits(color=PALETTE["accents"]["amber"]),
                modern_uefi_rom.animate.stream_parallel_lanes(
                    colors=[PALETTE["accents"]["indigo"], PALETTE["accents"]["sky"]]
                ),
                run_time=6.33
            )
            self.wait(1.8)

        self.beat(
            "3.1",
            "Now, modern computers generally use UEFI instead of traditional BIOS. UEFI stands for Unified Extensible Firmware Interface.",
            act_3_1,
            motion_time=8.33,
            hold_time=1.8,
            transient=[
                {"type": "badge", "text": "UEFI: Unified Extensible Firmware Interface", "position": [0.0, 2.3], "fill_token": "indigo", "text_color": "#FFFFFF"}
            ]
        )

        # =========================================================================
        # BEAT 3.2 (123.09s - 136.30s, motion: 11.41s)
        # =========================================================================
        def act_3_2():
            # Shift uefi rom left slightly to make room for GPT drive and padlock
            self.play(
                modern_uefi_rom.animate.move_to([-2.5, 0.0, 0.0]),
                FadeIn(gpt_nvme_drive),
                FadeIn(secure_boot_lock),
                run_time=2.5
            )
            self.play(
                modern_uefi_rom.animate.project_laser_scanner(gpt_nvme_drive, color=PALETTE["accents"]["sky"]),
                secure_boot_lock.animate.engage_lock(color=PALETTE["accents"]["mint"]),
                run_time=8.91
            )
            self.wait(1.8)

        self.beat(
            "3.2",
            "Think of it as a more flexible and modern successor to the old BIOS approach. It supports modern disk layouts, larger storage devices, configurable boot entries, and security features such as Secure Boot.",
            act_3_2,
            motion_time=11.41,
            hold_time=1.8,
            transient=[
                {"type": "annotation", "text": "SECURE BOOT VERIFIED", "position": [1.8, -2.1], "color_token": "mint"}
            ]
        )

        # =========================================================================
        # BEAT 3.3 (136.30s - 154.69s, motion: 16.59s)
        # =========================================================================
        def act_3_3():
            self.play(
                FadeOut(modern_uefi_rom),
                FadeOut(gpt_nvme_drive),
                FadeOut(secure_boot_lock),
                FadeIn(bios_stepper),
                FadeIn(uefi_router_matrix),
                run_time=2.0
            )
            self.play(
                bios_stepper.animate.step_contacts(),
                uefi_router_matrix.animate.illuminate_parallel_pathways(color=PALETTE["accents"]["blue"]),
                run_time=14.59
            )
            self.wait(1.8)

        self.beat(
            "3.3",
            "If traditional BIOS is an old-school paper checklist, UEFI is more like a digital management system with additional capabilities. Both perform the fundamental job of initializing the platform and finding something to boot from, but UEFI provides a more advanced and flexible framework.",
            act_3_3,
            motion_time=16.59,
            hold_time=1.8,
            transient=[
                {"type": "annotation", "text": "16-BIT REAL MODE", "position": [-2.8, 1.6], "color_token": "text_dim"},
                {"type": "annotation", "text": "64-BIT EXTENSIBLE", "position": [2.2, 1.6], "color_token": "text_primary"}
            ]
        )
