from manim import *
from engine_2d.theme import PALETTE, FONT_SIZES
from engine_2d.scene import EditorialScene
from engine_2d.objects import (
    RotaryDispatchSwitch,
    NvmeSsdActor,
    RamModuleActor,
    DataPacketActor,
    ChipSoC,
)

class Scene05(EditorialScene):
    def construct(self):
        self.target_duration = 53.42

        # =========================================================================
        # OUTER-SCOPE VARIABLE DECLARATION (Zero-Bug Mandate)
        # =========================================================================
        
        # Scene 5.1 Actors
        grub_dispatcher = RotaryDispatchSwitch().move_to([0.0, 0.0, 0.0])
        source_ssd = NvmeSsdActor().move_to([-4.2, 0.0, 0.0])

        # Scene 5.2 Additional Actors
        storage_drive = NvmeSsdActor().move_to([-3.5, -0.5, 0.0])
        system_ram = RamModuleActor().move_to([3.0, -0.5, 0.0])

        # Scene 5.3 Additional Actors
        boot_params_packet = DataPacketActor().move_to([0.0, 0.8, 0.0])
        cpu_core = ChipSoC().move_to([2.2, 1.0, 0.0])

        # =========================================================================
        # BEAT 5.1 (215.47s - 238.37s, motion: 21.10s)
        # =========================================================================
        def act_5_1():
            self.play(
                FadeIn(source_ssd),
                FadeIn(grub_dispatcher),
                run_time=2.0
            )
            self.play(
                grub_dispatcher.animate.dock_crystal_and_dispatch(
                    color=PALETTE["accents"]["indigo"],
                    target_color=PALETTE["accents"]["mint"]
                ),
                run_time=19.1
            )
            self.wait(1.8)

        self.beat(
            "5.1",
            "And here's where things get exciting. The bootloader. On many Linux systems, the bootloader is GRUB, which stands for GRand Unified Bootloader. GRUB is that familiar startup screen you might have seen when your Linux machine displays a menu with options such as Ubuntu, advanced startup options, or Windows Boot Manager on a dual-boot computer.",
            act_5_1,
            motion_time=21.1,
            hold_time=1.8,
            transient=[
                {"type": "badge", "text": "GRUB: GRand Unified Bootloader", "position": [0.0, 2.3], "fill_token": "indigo", "text_color": "#FFFFFF"}
            ]
        )

        # =========================================================================
        # BEAT 5.2 (238.37s - 253.22s, motion: 13.05s)
        # =========================================================================
        def act_5_2():
            self.play(
                FadeOut(source_ssd),
                FadeOut(grub_dispatcher),
                FadeIn(storage_drive),
                FadeIn(system_ram),
                run_time=2.0
            )
            self.play(
                storage_drive.animate.eject_payload_capsules(
                    system_ram,
                    kernel_color=PALETTE["accents"]["indigo"],
                    initramfs_color=PALETTE["accents"]["amber"],
                    bus_color=PALETTE["accents"]["sky"]
                ),
                run_time=11.05
            )
            self.wait(1.8)

        self.beat(
            "5.2",
            "The bootloader's job is to load the Linux kernel and provide the information it needs to continue booting. It locates the kernel image on your storage device, loads it into memory, and typically also loads an initial RAM filesystem image.",
            act_5_2,
            motion_time=13.05,
            hold_time=1.8,
            transient=[
                {"type": "annotation", "text": "vmlinuz (Kernel)", "position": [-0.5, 0.8], "color_token": "indigo"},
                {"type": "annotation", "text": "initramfs", "position": [-0.5, -1.5], "color_token": "amber"}
            ]
        )

        # =========================================================================
        # BEAT 5.3 (253.22s - 268.89s, motion: 13.87s)
        # =========================================================================
        def act_5_3():
            # Re-introduce dispatcher at left, CPU and RAM at right
            grub_dispatcher.move_to([-2.2, 0.5, 0.0])
            cpu_core.move_to([2.2, 1.0, 0.0])
            system_ram.move_to([2.2, -1.0, 0.0])
            self.play(
                FadeOut(storage_drive),
                FadeIn(grub_dispatcher),
                FadeIn(boot_params_packet),
                FadeIn(cpu_core),
                run_time=2.0
            )
            self.play(
                grub_dispatcher.animate.fire_packet_and_hand_baton(
                    boot_params_packet,
                    cpu_core,
                    packet_color=PALETTE["accents"]["blue"],
                    baton_color=PALETTE["accents"]["mint"]
                ),
                run_time=11.87
            )
            self.wait(1.8)

        self.beat(
            "5.3",
            "It can pass kernel parameters that tell Linux how to start, including information about which partition contains the root filesystem. Once everything is ready, GRUB hands control to the kernel. Think of GRUB as a relay runner passing the baton to Linux itself.",
            act_5_3,
            motion_time=13.87,
            hold_time=1.8,
            transient=[
                {"type": "annotation", "text": "root=/dev/nvme0n1p2 ro", "position": [0.0, 1.9], "color_token": "text_primary"}
            ]
        )
