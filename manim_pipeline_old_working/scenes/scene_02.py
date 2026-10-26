from manim import *
from engine_2d import (
    EditorialScene,
    PALETTE,
    FONT_SIZES,
    SpiFlashRom,
    ChipSoC,
    RamModuleActor,
    NvmeSsdActor,
    DiagnosticSpeaker,
)


class Scene02(EditorialScene):
    def construct(self):
        self.target_duration = 51.19  # Exact total duration of this scene from JSON

        # =========================================================================
        # 1. OUTER-SCOPE VARIABLE DECLARATIONS (all persistent actors)
        # =========================================================================
        bios_rom = SpiFlashRom().move_to([-3.2, 0.5, 0.0])
        cpu_core = ChipSoC().move_to([0.0, 1.2, 0.0])
        ddr5_dimm = RamModuleActor().move_to([0.0, -1.0, 0.0])
        nvme_drive = NvmeSsdActor().move_to([3.2, 0.0, 0.0])
        piezo_buzzer = DiagnosticSpeaker().move_to([3.2, -1.0, 0.0])

        # Diagnostic trace branches from BIOS ROM (Beat 2.1)
        trace_cpu = Line([-2.6, 0.6, 0.0], [-0.8, 1.1, 0.0], color=PALETTE["text_dim"], stroke_width=3)
        trace_ram = Line([-2.6, 0.4, 0.0], [-0.8, -0.9, 0.0], color=PALETTE["text_dim"], stroke_width=3)
        trace_nvme = Line([-2.6, 0.5, 0.0], [2.4, 0.0, 0.0], color=PALETTE["text_dim"], stroke_width=3)

        # Diagnostic probe pulses (Beats 2.2 - 2.3)
        probe_cpu = Dot(radius=0.09, color=PALETTE["blue"]).move_to([-2.6, 0.6, 0.0])
        probe_ram = Dot(radius=0.09, color=PALETTE["blue"]).move_to([-2.6, 0.4, 0.0])

        # POST fault current + acoustic arcs (Beat 2.4)
        fault_dot = Dot(radius=0.09, color=PALETTE["coral"]).move_to([0.4, -1.0, 0.0])
        sound_waves = VGroup(*[
            Arc(radius=r, start_angle=-PI / 4, angle=PI / 2, color=PALETTE["coral"], stroke_width=3)
            .move_arc_center_to([3.2, -1.0, 0.0])
            for r in (0.6, 0.9, 1.2)
        ])

        # =========================================================================
        # 2. CHOREOGRAPHED BEATS
        # =========================================================================

        # ---- Beat 2.1 : BIOS micro-sequencer spins up (motion 8.7 + hold 1.8) ----
        def act_2_1():
            self.play(
                FadeIn(bios_rom),
                FadeIn(cpu_core),
                FadeIn(ddr5_dimm),
                FadeIn(nvme_drive),
                run_time=3.0,
            )
            self.play(bios_rom.animate.set_color(PALETTE["indigo"]), run_time=2.2)
            self.play(Create(trace_cpu), Create(trace_ram), Create(trace_nvme), run_time=1.5)
            self.play(bios_rom.animate.scale(1.08), run_time=1.0)
            self.play(bios_rom.animate.scale(1 / 1.08), run_time=1.0)
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

        # ---- Beat 2.2 : POST probe pulses toward CPU and RAM (motion 8.32 + hold 1.8) ----
        def act_2_2():
            self.add(probe_cpu, probe_ram)
            self.play(
                probe_cpu.animate.move_to([-0.8, 1.1, 0.0]),
                probe_ram.animate.move_to([-0.8, -0.9, 0.0]),
                run_time=3.5,
            )
            self.play(
                cpu_core.animate.scale(1.05),
                ddr5_dimm.animate.scale(1.05),
                run_time=2.41,
            )
            self.play(
                cpu_core.animate.scale(1 / 1.05),
                ddr5_dimm.animate.scale(1 / 1.05),
                run_time=2.41,
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

        # ---- Beat 2.3 : probe verifies CPU -> RAM -> NVMe (motion 14.6 + hold 1.8) ----
        def act_2_3():
            self.play(
                cpu_core.animate.move_to([-0.5, 1.1, 0.0]),
                ddr5_dimm.animate.move_to([-0.5, -1.0, 0.0]),
                run_time=2.0,
            )
            self.play(cpu_core.animate.set_color(PALETTE["mint"]), run_time=2.5)
            self.play(probe_cpu.animate.move_to([-0.5, -0.6, 0.0]), run_time=2.5)
            self.play(ddr5_dimm.animate.set_color(PALETTE["mint"]), run_time=3.0)
            self.play(probe_cpu.animate.move_to([2.6, 0.0, 0.0]), run_time=2.0)
            self.play(nvme_drive.animate.set_color(PALETTE["mint"]), run_time=2.6)
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

        # ---- Beat 2.4 : DRAM fault -> beep code (motion 12.37 + hold 1.8) ----
        def act_2_4():
            self.add(fault_dot)
            self.play(
                ddr5_dimm.animate.set_color(PALETTE["coral"]),
                FadeIn(piezo_buzzer),
                run_time=1.5,
            )
            self.play(fault_dot.animate.move_to([2.6, -1.0, 0.0]), run_time=2.5)
            self.play(piezo_buzzer.animate.scale(1.1), run_time=1.0)
            self.play(piezo_buzzer.animate.scale(1 / 1.1), run_time=1.0)
            self.play(
                LaggedStart(*[FadeIn(arc) for arc in sound_waves], lag_ratio=0.4),
                run_time=3.0,
            )
            self.play(
                ddr5_dimm.animate.set_color(PALETTE["mint"]),
                FadeOut(sound_waves),
                FadeOut(fault_dot),
                run_time=3.37,
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
