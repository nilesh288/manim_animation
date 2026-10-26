from manim import *
from engine_2d.theme import PALETTE, FONT_SIZES
from engine_2d.scene import EditorialScene
from engine_2d.objects import (
    NvmeSsdActor,
    FilesystemHierarchyTree,
    ChipSoC,
    RamModuleActor,
    FilesystemNodeActor,
    CyberneticTurbineHub,
)

class Scene08(EditorialScene):
    def construct(self):
        self.target_duration = 67.06

        # =========================================================================
        # OUTER-SCOPE VARIABLE DECLARATION (Zero-Bug Mandate)
        # =========================================================================
        
        # Scene 8.1 Actors
        root_fs_ssd = NvmeSsdActor().move_to([0.0, -1.6, 0.0])
        root_tree_structure = FilesystemHierarchyTree(
            apex_position=[0.0, 1.4, 0.0],
            branch_positions=[[-1.8, -0.1, 0.0], [0.0, -0.1, 0.0], [1.8, -0.1, 0.0]]
        )

        # Scene 8.2 Additional Actors
        kernel_cpu = ChipSoC().move_to([-3.5, 0.5, 0.0])
        ram_reclaim = RamModuleActor().move_to([-1.0, -1.6, 0.0])

        # Scene 8.3 Additional Actors
        sbin_init_node = FilesystemNodeActor().move_to([0.0, 0.0, 0.0])
        pid_1_systemd = CyberneticTurbineHub().move_to([2.8, 0.0, 0.0])

        # =========================================================================
        # BEAT 8.1 (390.46s - 416.74s, motion: 24.48s)
        # =========================================================================
        def act_8_1():
            self.play(
                FadeIn(root_fs_ssd),
                FadeIn(root_tree_structure),
                run_time=2.0
            )
            self.play(
                root_fs_ssd.animate.rise_filesystem_tree(
                    root_tree_structure,
                    keystone_color=PALETTE["text"],
                    conduit_color=PALETTE["stroke"]
                ),
                run_time=22.48
            )
            self.wait(1.8)

        self.beat(
            "8.1",
            "With the necessary drivers and storage access ready, Linux can move to the next major stage: mounting the root filesystem. Your root filesystem contains the essential directories and files that make up your Linux installation. These include system programs, shared libraries, configuration files, and other resources needed to run the operating system. The root filesystem is conventionally represented by a forward slash.",
            act_8_1,
            motion_time=24.48,
            hold_time=1.8,
            transient=[
                {"type": "badge", "text": "ROOT FILESYSTEM ( / )", "position": [0.0, 2.3], "fill_token": "blue", "text_color": "#FFFFFF"},
                {"type": "annotation", "text": "/bin   /lib   /etc", "position": [0.0, -0.8], "color_token": "text_dim"}
            ]
        )

        # =========================================================================
        # BEAT 8.2 (416.74s - 447.94s, motion: 29.40s)
        # =========================================================================
        def act_8_2():
            root_tree_structure.move_to([1.5, 0.5, 0.0])
            self.play(
                FadeIn(kernel_cpu),
                FadeIn(ram_reclaim),
                run_time=2.0
            )
            self.play(
                kernel_cpu.animate.clamp_to_filesystem_tree(
                    root_tree_structure,
                    bridge_color=PALETTE["accents"]["blue"],
                    lock_color=PALETTE["accents"]["mint"]
                ),
                ram_reclaim.animate.switch_root_reclaim_ram(
                    dissolve_color=PALETTE["accents"]["amber"],
                    clean_color=PALETTE["accents"]["mint"]
                ),
                run_time=27.4
            )
            self.wait(1.8)

        self.beat(
            "8.2",
            "The kernel, working with the early userspace environment when necessary, locates the intended root filesystem and mounts it. Mounting means attaching a filesystem to a location in Linux's directory hierarchy so its contents become accessible. Once the real root filesystem is ready, the system transitions from the temporary startup environment to the main Linux installation. Now the operating system has access to the files and programs it needs to continue starting up. It's like opening the main library of books required to run the entire show.",
            act_8_2,
            motion_time=29.4,
            hold_time=1.8,
            transient=[
                {"type": "annotation", "text": "MOUNT / (READ-WRITE)", "position": [1.5, 1.8], "color_token": "text_primary"}
            ]
        )

        # =========================================================================
        # BEAT 8.3 (447.94s - 457.52s, motion: 7.78s)
        # =========================================================================
        def act_8_3():
            self.play(
                FadeOut(root_fs_ssd),
                FadeOut(root_tree_structure),
                FadeOut(kernel_cpu),
                FadeOut(ram_reclaim),
                FadeIn(sbin_init_node),
                FadeIn(pid_1_systemd),
                run_time=1.5
            )
            self.play(
                sbin_init_node.animate.spin_pid1_turbine(
                    pid_1_systemd,
                    ignition_color=PALETTE["accents"]["mint"],
                    turbine_color=PALETTE["accents"]["indigo"],
                    conduit_color=PALETTE["accents"]["blue"]
                ),
                run_time=6.28
            )
            self.wait(1.8)

        self.beat(
            "8.3",
            "Here comes another important milestone. The kernel starts the very first userspace process: process number one, commonly called PID 1.",
            act_8_3,
            motion_time=7.78,
            hold_time=1.8,
            transient=[
                {"type": "badge", "text": "PID 1: systemd / init", "position": [2.8, 1.8], "fill_token": "mint", "text_color": "#FFFFFF"}
            ]
        )
