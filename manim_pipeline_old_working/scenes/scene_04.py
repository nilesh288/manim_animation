from manim import *
from engine_2d.theme import PALETTE, FONT_SIZES
from engine_2d.scene import EditorialScene
from engine_2d.objects import (
    SpiFlashRom,
    NvmeSsdActor,
    UsbFlashDriveActor,
    FiberOpticConduit,
    StorageSectorArray,
)

class Scene04(EditorialScene):
    def construct(self):
        self.target_duration = 60.78

        # =========================================================================
        # OUTER-SCOPE VARIABLE DECLARATION (Zero-Bug Mandate)
        # =========================================================================
        
        # Scene 4.1 Actors
        uefi_firmware = SpiFlashRom().move_to([-4.0, 0.0, 0.0])
        boot_target_ssd = NvmeSsdActor().move_to([2.0, 1.4, 0.0])
        boot_target_usb = UsbFlashDriveActor().move_to([2.0, 0.0, 0.0])
        boot_target_pxe = FiberOpticConduit().move_to([2.0, -1.4, 0.0])

        # Scene 4.2 Actors
        legacy_disk_sectors = StorageSectorArray().surround_bounds(
            x_bounds=[-4.0, 4.0], y_bounds=[0.2, 1.4]
        )

        # Scene 4.3 Actors
        uefi_nvme_ssd = NvmeSsdActor().surround_bounds(
            x_bounds=[-4.2, 4.2], y_bounds=[-1.2, 0.5]
        )

        # =========================================================================
        # BEAT 4.1 (154.69s - 172.09s, motion: 15.60s)
        # =========================================================================
        def act_4_1():
            self.play(
                FadeIn(uefi_firmware),
                FadeIn(boot_target_ssd),
                FadeIn(boot_target_usb),
                FadeIn(boot_target_pxe),
                run_time=2.0
            )
            self.play(
                uefi_firmware.animate.sweep_multiplexing_selector(
                    [boot_target_ssd, boot_target_usb, boot_target_pxe],
                    target=boot_target_ssd,
                    color=PALETTE["accents"]["sky"],
                    lock_color=PALETTE["accents"]["mint"]
                ),
                run_time=13.6
            )
            self.wait(1.8)

        self.beat(
            "4.1",
            "Once the initial hardware checks are complete, the firmware needs to find the operating system. It consults its boot configuration and looks for an available boot device. That might be your SSD, an internal hard drive, a USB drive, or even a network boot source.",
            act_4_1,
            motion_time=15.6,
            hold_time=1.8,
            transient=[
                {"type": "annotation", "text": "BOOT PRIORITY #1", "position": [-1.0, 1.6], "color_token": "text_primary"}
            ]
        )

        # =========================================================================
        # BEAT 4.2 (172.09s - 191.14s, motion: 17.25s)
        # =========================================================================
        def act_4_2():
            self.play(
                FadeOut(uefi_firmware),
                FadeOut(boot_target_ssd),
                FadeOut(boot_target_usb),
                FadeOut(boot_target_pxe),
                FadeIn(legacy_disk_sectors),
                run_time=2.0
            )
            self.play(
                legacy_disk_sectors.animate.read_sector_zero(
                    position=[-3.5, 0.8, 0.0],
                    color=PALETTE["accents"]["amber"]
                ),
                run_time=15.25
            )
            self.wait(1.8)

        self.beat(
            "4.2",
            "On a traditional BIOS system, the firmware commonly reads the first 512 bytes of the selected boot device. This area is known as the MBR, or Master Boot Record. Think of it like the index at the beginning of a book. It contains a small amount of information that helps the system begin loading the boot software.",
            act_4_2,
            motion_time=17.25,
            hold_time=1.8,
            transient=[
                {"type": "badge", "text": "MBR: Master Boot Record (512 Bytes)", "position": [-1.8, 2.1], "fill_token": "amber", "text_color": "#FFFFFF"}
            ]
        )

        # =========================================================================
        # BEAT 4.3 (191.14s - 215.47s, motion: 22.53s)
        # =========================================================================
        def act_4_3():
            self.play(
                FadeOut(legacy_disk_sectors),
                FadeIn(uefi_nvme_ssd),
                run_time=2.0
            )
            self.play(
                uefi_nvme_ssd.animate.split_partitions_and_extract_crystal(
                    partition_pos=[-2.2, -0.3, 0.0],
                    chamber_color=PALETTE["accents"]["blue"],
                    crystal_color=PALETTE["accents"]["indigo"],
                    trace_color=PALETTE["accents"]["sky"]
                ),
                run_time=20.53
            )
            self.wait(1.8)

        self.beat(
            "4.3",
            "On UEFI systems, the process is different. The firmware typically looks for a bootloader on a special partition called the EFI System Partition, or ESP. This partition contains EFI applications that the firmware can launch directly. The exact process depends on the boot configuration, but the objective is the same: locate the program that will continue the startup process.",
            act_4_3,
            motion_time=22.53,
            hold_time=1.8,
            transient=[
                {"type": "badge", "text": "ESP: EFI System Partition", "position": [-2.0, 1.4], "fill_token": "blue", "text_color": "#FFFFFF"},
                {"type": "annotation", "text": "/EFI/ubuntu/grubx64.efi", "position": [1.5, 1.4], "color_token": "text_primary"}
            ]
        )
