from manim import *
from engine_2d.theme import PALETTE, FONT_SIZES
from engine_2d.scene import EditorialScene
from engine_2d.objects import (
    ChipSoC,
    CryptographicPadlock,
    NvmeSsdActor,
    RamModuleActor,
)

class Scene07(EditorialScene):
    def construct(self):
        self.target_duration = 68.31

        # =========================================================================
        # OUTER-SCOPE VARIABLE DECLARATION (Zero-Bug Mandate)
        # =========================================================================
        
        # Scene 7.1 Actors
        kernel_cpu = ChipSoC().move_to([-3.2, 0.0, 0.0])
        storage_gate_lock = CryptographicPadlock().move_to([1.2, 0.0, 0.0])
        locked_nvme = NvmeSsdActor().move_to([3.0, 0.0, 0.0])

        # Scene 7.2 Additional Actors
        ram_with_initramfs = RamModuleActor().move_to([0.0, -1.2, 0.0])

        # Scene 7.3 Additional Actors
        ram_workshop = RamModuleActor().move_to([-1.5, -1.4, 0.0])
        unlocked_nvme = NvmeSsdActor().move_to([3.0, 0.3, 0.0])

        # =========================================================================
        # BEAT 7.1 (322.15s - 345.68s, motion: 21.73s)
        # =========================================================================
        def act_7_1():
            self.play(
                FadeIn(kernel_cpu),
                FadeIn(storage_gate_lock),
                FadeIn(locked_nvme),
                run_time=2.0
            )
            self.play(
                kernel_cpu.animate.probe_locked_storage(
                    locked_nvme,
                    probe_color=PALETTE["accents"]["blue"],
                    fault_color=PALETTE["accents"]["coral"]
                ),
                run_time=19.73
            )
            self.wait(1.8)

        self.beat(
            "7.1",
            "But the kernel faces an interesting problem during startup. It needs to access the storage device to load the files required for the rest of the boot process. However, the drivers or tools needed to access that storage might themselves be located on the storage device. How can Linux load the tools it needs from a device it cannot access yet? It's a classic chicken-and-egg problem.",
            act_7_1,
            motion_time=21.73,
            hold_time=1.8,
            transient=[
                {"type": "badge", "text": "DEADLOCK: DRIVER INSIDE LOCKED STORAGE", "position": [0.0, 2.2], "fill_token": "coral", "text_color": "#FFFFFF"}
            ]
        )

        # =========================================================================
        # BEAT 7.2 (345.68s - 362.18s, motion: 14.70s)
        # =========================================================================
        def act_7_2():
            self.play(
                FadeOut(kernel_cpu),
                FadeOut(storage_gate_lock),
                FadeOut(locked_nvme),
                FadeIn(ram_with_initramfs),
                run_time=2.0
            )
            self.play(
                ram_with_initramfs.animate.unfold_initramfs_workshop(
                    capsule_color=PALETTE["accents"]["amber"],
                    gear_color=PALETTE["accents"]["mint"]
                ),
                run_time=12.7
            )
            self.wait(1.8)

        self.beat(
            "7.2",
            "Linux solves this with something called initramfs, short for initial RAM filesystem. Think of initramfs as a tiny temporary environment that lives in memory and gives the kernel the tools it needs to continue booting. The bootloader loads this image into RAM alongside the kernel.",
            act_7_2,
            motion_time=14.7,
            hold_time=1.8,
            transient=[
                {"type": "badge", "text": "initramfs: Initial RAM Filesystem", "position": [0.0, 2.2], "fill_token": "amber", "text_color": "#FFFFFF"}
            ]
        )

        # =========================================================================
        # BEAT 7.3 (362.18s - 390.46s, motion: 26.48s)
        # =========================================================================
        def act_7_3():
            kernel_cpu.move_to([-3.2, 0.3, 0.0])
            storage_gate_lock.move_to([1.5, 0.3, 0.0])
            self.play(
                FadeOut(ram_with_initramfs),
                FadeIn(ram_workshop),
                FadeIn(kernel_cpu),
                FadeIn(storage_gate_lock),
                FadeIn(unlocked_nvme),
                run_time=2.0
            )
            self.play(
                ram_workshop.animate.dispatch_driver_and_unlock(
                    storage_gate_lock,
                    unlocked_nvme,
                    key_color=PALETTE["accents"]["mint"],
                    vault_color=PALETTE["accents"]["mint"]
                ),
                run_time=24.48
            )
            self.wait(1.8)

        self.beat(
            "7.3",
            "After initializing enough of the system to run it, the kernel uses initramfs to execute early userspace programs and scripts. These can load additional drivers, discover storage devices, unlock encrypted volumes, or assemble storage configurations such as RAID arrays. Once the necessary storage is accessible, the system can locate and prepare the real root filesystem. It's like carrying a spare key in your wallet to open the room where your main set of keys is stored.",
            act_7_3,
            motion_time=26.48,
            hold_time=1.8,
            transient=[
                {"type": "annotation", "text": "NVMe DRIVER LOADED", "position": [2.2, 1.8], "color_token": "mint"}
            ]
        )
