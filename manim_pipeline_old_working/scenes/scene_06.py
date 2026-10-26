from manim import *
from engine_2d.theme import PALETTE, FONT_SIZES
from engine_2d.scene import EditorialScene
from engine_2d.objects import (
    ChipSoC,
    RamModuleActor,
    NvmeSsdActor,
    ModernRouter,
    MotherboardSection,
)

class Scene06(EditorialScene):
    def construct(self):
        self.target_duration = 53.26

        # =========================================================================
        # OUTER-SCOPE VARIABLE DECLARATION (Zero-Bug Mandate)
        # =========================================================================
        
        # Scene 6.1 Actors
        kernel_cpu_hub = ChipSoC().move_to([0.0, 0.0, 0.0])
        ram_subsystem = RamModuleActor().move_to([-3.8, 1.2, 0.0])
        storage_subsystem = NvmeSsdActor().move_to([-3.8, -1.2, 0.0])
        network_subsystem = ModernRouter().move_to([3.8, 1.2, 0.0])
        io_subsystem = MotherboardSection().move_to([3.8, -1.2, 0.0])

        # Scene 6.2 Additional Actors
        kernel_ram_space = RamModuleActor().move_to([0.0, -0.5, 0.0])

        # Scene 6.3 Additional Actors
        cpu_manager = ChipSoC().move_to([-2.2, 0.5, 0.0])
        paged_ram = RamModuleActor().move_to([2.0, -0.5, 0.0])

        # =========================================================================
        # BEAT 6.1 (268.89s - 286.07s, motion: 15.38s)
        # =========================================================================
        def act_6_1():
            self.play(
                FadeIn(kernel_cpu_hub),
                FadeIn(ram_subsystem),
                FadeIn(storage_subsystem),
                FadeIn(network_subsystem),
                FadeIn(io_subsystem),
                run_time=2.0
            )
            self.play(
                kernel_cpu_hub.animate.establish_feedback_loops(
                    [ram_subsystem, storage_subsystem, network_subsystem, io_subsystem],
                    core_color=PALETTE["accents"]["indigo"],
                    tendril_color=PALETTE["accents"]["blue"]
                ),
                run_time=13.38
            )
            self.wait(1.8)

        self.beat(
            "6.1",
            "Now the Linux kernel enters the picture, and this is the heart of the entire operating system. The kernel is the core software responsible for managing system resources, including processor time, memory, storage, hardware devices, and networking.",
            act_6_1,
            motion_time=15.38,
            hold_time=1.8,
            transient=[
                {"type": "badge", "text": "LINUX KERNEL CORE", "position": [0.0, 2.3], "fill_token": "blue", "text_color": "#FFFFFF"}
            ]
        )

        # =========================================================================
        # BEAT 6.2 (286.07s - 305.37s, motion: 17.50s)
        # =========================================================================
        def act_6_2():
            self.play(
                FadeOut(ram_subsystem),
                FadeOut(storage_subsystem),
                FadeOut(network_subsystem),
                FadeOut(io_subsystem),
                kernel_cpu_hub.animate.move_to([0.0, 1.5, 0.0]),
                FadeIn(kernel_ram_space),
                run_time=2.0
            )
            self.play(
                kernel_ram_space.animate.unfold_kernel_capsule(
                    capsule_color=PALETTE["accents"]["indigo"],
                    lattice_color=PALETTE["accents"]["blue"]
                ),
                run_time=15.5
            )
            self.wait(1.8)

        self.beat(
            "6.2",
            "When the bootloader transfers control to the kernel, the kernel begins setting up the environment in which the rest of Linux will operate. First, the kernel performs its early initialization. Depending on the architecture and kernel image, this includes decompressing the kernel if necessary and preparing its internal data structures.",
            act_6_2,
            motion_time=17.5,
            hold_time=1.8,
            transient=[
                {"type": "annotation", "text": "KERNEL DECOMPRESSION", "position": [0.0, 1.6], "color_token": "text_primary"}
            ]
        )

        # =========================================================================
        # BEAT 6.3 (305.37s - 322.15s, motion: 14.98s)
        # =========================================================================
        def act_6_3():
            self.play(
                FadeOut(kernel_cpu_hub),
                FadeOut(kernel_ram_space),
                FadeIn(cpu_manager),
                FadeIn(paged_ram),
                run_time=2.0
            )
            self.play(
                cpu_manager.animate.project_laser_grid(
                    paged_ram,
                    grid_color=PALETTE["accents"]["sky"],
                    border_color=PALETTE["accents"]["mint"]
                ),
                run_time=12.98
            )
            self.wait(1.8)

        self.beat(
            "6.3",
            "Next, it initializes essential processor functionality, establishes memory management, discovers hardware, and prepares the necessary device drivers and subsystems. Think of it as a new manager walking into an office and immediately taking stock of every resource available.",
            act_6_3,
            motion_time=14.98,
            hold_time=1.8,
            transient=[
                {"type": "annotation", "text": "VIRTUAL MEMORY PAGING", "position": [2.0, 1.2], "color_token": "text_primary"}
            ]
        )
