
from manim import *
import numpy as np

# POC 6A — 3D Jet Engine
# Manim Community Edition 0.22.0
# Preview: 854x480, 15 FPS
# Render media under /dev/shm

config.background_color = "#07111F"


class JetEnginePOC06A(ThreeDScene):
    def construct(self):
        CYAN = "#36D9FF"
        BLUE = "#188DFF"
        ORANGE = "#FF8736"
        GOLD = "#FFD166"
        STEEL = "#A9B9C9"
        DARK_STEEL = "#40546A"
        WHITE = "#F1F6FC"

        self.camera.background_color = "#07111F"

        # --------------------------------------------------
        # CAMERA
        # Engine axis is the X axis.
        # --------------------------------------------------
        self.set_camera_orientation(
            phi=72 * DEGREES,
            theta=-22 * DEGREES,
            zoom=0.92,
        )

        # --------------------------------------------------
        # TITLE — fixed to the screen
        # --------------------------------------------------
        title = Text(
            "INSIDE A JET ENGINE",
            font_size=27,
            color=WHITE,
            weight=BOLD,
        ).to_edge(UP, buff=0.25)

        subtitle = Text(
            "FROM AIRFLOW TO THRUST",
            font_size=13,
            color=CYAN,
        ).next_to(title, DOWN, buff=0.06)

        self.add_fixed_in_frame_mobjects(title, subtitle)
        self.play(FadeIn(title), FadeIn(subtitle), run_time=0.8)

        # --------------------------------------------------
        # ENGINE SHAFT
        # --------------------------------------------------
        shaft = Cylinder(
            radius=0.105,
            height=8.0,
            direction=RIGHT,
            resolution=(12, 24),
            fill_color=STEEL,
            fill_opacity=0.95,
            stroke_color=WHITE,
            stroke_width=0.4,
        ).move_to([-0.2, 0, 0])

        self.play(FadeIn(shaft), run_time=0.5)

        # --------------------------------------------------
        # HELPER: DISK AT AN X POSITION
        # --------------------------------------------------
        def disk(x, radius, color, opacity=0.9):
            obj = Cylinder(
                radius=radius,
                height=0.11,
                direction=RIGHT,
                resolution=(16, 32),
                fill_color=color,
                fill_opacity=opacity,
                stroke_color=STEEL,
                stroke_width=0.5,
            )
            return obj.move_to([x, 0, 0])

        # --------------------------------------------------
        # HELPER: RADIAL BLADES
        # Blade meshes are thin boxes positioned around shaft.
        # Each stage is grouped so it can rotate around X.
        # --------------------------------------------------
        def make_blade_stage(x, radius, count, color, blade_length=0.55):
            blades = VGroup()

            for i in range(count):
                angle = TAU * i / count

                # Blade begins near the shaft and extends radially.
                blade = Cube(
                    side_length=1,
                    fill_color=color,
                    fill_opacity=0.95,
                    stroke_color=STEEL,
                    stroke_width=0.35,
                ).stretch(0.13, dim=0).stretch(
                    blade_length, dim=1
                ).stretch(0.105, dim=2)


                r = radius * 0.56
                blade.move_to([
                    x,
                    r * np.cos(angle),
                    r * np.sin(angle),
                ])

                blade.rotate(
                    angle,
                    axis=RIGHT,
                    about_point=[x, 0, 0],
                )

                blades.add(blade)

            hub = Cylinder(
                radius=0.22,
                height=0.18,
                direction=RIGHT,
                resolution=(12, 24),
                fill_color=STEEL,
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=0.4,
            ).move_to([x, 0, 0])

            return VGroup(hub, blades)

        # --------------------------------------------------
        # FRONT FAN
        # --------------------------------------------------
        fan_disk = disk(-4.1, 1.05, DARK_STEEL)
        fan_stage = make_blade_stage(
            x=-4.0,
            radius=1.0,
            count=12,
            color=CYAN,
            blade_length=0.75,
        )

        fan_ring = Torus(
            major_radius=1.0,
            minor_radius=0.055,
            resolution=(24, 48),
            color=CYAN,
        ).rotate(90 * DEGREES, axis=UP).move_to([-4.0, 0, 0])

        self.play(
            FadeIn(fan_disk),
            FadeIn(fan_ring),
            FadeIn(fan_stage),
            run_time=1.0,
        )

        # --------------------------------------------------
        # COMPRESSOR STAGES
        # --------------------------------------------------
        compressor = VGroup()
        compressor_stages = []

        compressor_positions = [-3.25, -2.65, -2.05, -1.45]

        for i, x in enumerate(compressor_positions):
            radius = 0.87 - i * 0.09

            rotor_disk = disk(x, radius, DARK_STEEL, 0.95)
            rotor = make_blade_stage(
                x=x,
                radius=radius,
                count=10,
                color=BLUE,
                blade_length=0.46,
            )

            compressor.add(rotor_disk, rotor)
            compressor_stages.append(rotor)

        self.play(FadeIn(compressor), run_time=1.0)

        # --------------------------------------------------
        # COMBUSTION CHAMBER
        # --------------------------------------------------
        combustion_shell = Cylinder(
            radius=0.70,
            height=1.35,
            direction=RIGHT,
            resolution=(20, 40),
            fill_color="#51251F",
            fill_opacity=0.72,
            stroke_color=ORANGE,
            stroke_width=1.4,
        ).move_to([-0.55, 0, 0])

        flame_core = Cylinder(
            radius=0.40,
            height=1.12,
            direction=RIGHT,
            resolution=(16, 32),
            fill_color=ORANGE,
            fill_opacity=0.7,
            stroke_color=GOLD,
            stroke_width=0.5,
        ).move_to([-0.55, 0, 0])

        flame_inner = Cylinder(
            radius=0.22,
            height=1.15,
            direction=RIGHT,
            resolution=(12, 24),
            fill_color=GOLD,
            fill_opacity=0.65,
            stroke_width=0,
        ).move_to([-0.55, 0, 0])

        self.play(
            FadeIn(combustion_shell),
            FadeIn(flame_core),
            FadeIn(flame_inner),
            run_time=1.0,
        )

        # --------------------------------------------------
        # TURBINE STAGES
        # --------------------------------------------------
        turbine = VGroup()
        turbine_stages = []

        turbine_positions = [0.55, 1.25, 1.95]

        for i, x in enumerate(turbine_positions):
            radius = 0.68 + i * 0.07

            rotor_disk = disk(x, radius, DARK_STEEL)
            rotor = make_blade_stage(
                x=x,
                radius=radius,
                count=10,
                color=ORANGE,
                blade_length=0.43,
            )

            turbine.add(rotor_disk, rotor)
            turbine_stages.append(rotor)

        self.play(FadeIn(turbine), run_time=1.0)

        # --------------------------------------------------
        # EXHAUST NOZZLE
        # --------------------------------------------------
        nozzle_outer = Cone(
            base_radius=0.82,
            height=1.45,
            direction=RIGHT,
            resolution=(24, 48),
            fill_color=STEEL,
            fill_opacity=0.24,
            stroke_color=STEEL,
            stroke_width=1.0,
        ).move_to([3.15, 0, 0])

        nozzle_ring = Torus(
            major_radius=0.65,
            minor_radius=0.045,
            resolution=(24, 48),
            color=STEEL,
        ).rotate(90 * DEGREES, axis=UP).move_to([3.75, 0, 0])

        self.play(
            FadeIn(nozzle_outer),
            FadeIn(nozzle_ring),
            run_time=0.8,
        )

        # --------------------------------------------------
        # 3D AIRFLOW PARTICLES
        # --------------------------------------------------
        def make_flow(x_start, x_end, count, color, radius=0.035):
            particles = VGroup()

            for i in range(count):
                x = x_start + (x_end - x_start) * i / max(count - 1, 1)
                y = 0.12 * np.sin(i * 1.7)
                z = 0.12 * np.cos(i * 1.3)

                dot = Sphere(
                    radius=radius,
                    resolution=(5, 8),
                    color=color,
                    fill_opacity=0.95,
                    stroke_width=0,
                ).move_to([x, y, z])

                particles.add(dot)

            return particles

        inlet_flow = make_flow(-5.7, -4.3, 9, CYAN)
        compressor_flow = make_flow(-3.7, -1.2, 13, BLUE)
        hot_flow = make_flow(-0.2, 3.7, 17, ORANGE, 0.04)

        self.play(FadeIn(inlet_flow), run_time=0.3)
        self.play(
            inlet_flow.animate.shift(RIGHT * 1.7),
            run_time=1.1,
            rate_func=linear,
        )
        self.play(FadeOut(inlet_flow), run_time=0.2)

        self.play(FadeIn(compressor_flow), run_time=0.3)
        self.play(
            compressor_flow.animate.shift(RIGHT * 2.4),
            run_time=1.2,
            rate_func=linear,
        )
        self.play(FadeOut(compressor_flow), run_time=0.2)

        self.play(FadeIn(hot_flow), run_time=0.3)
        self.play(
            hot_flow.animate.shift(RIGHT * 1.5),
            run_time=1.0,
            rate_func=linear,
        )
        self.play(FadeOut(hot_flow), run_time=0.2)

        # --------------------------------------------------
        # ROTATING ROTOR STAGES
        # Rotate individual blade groups around the engine axis.
        # --------------------------------------------------
        self.play(
            Rotate(
                fan_stage,
                angle=1.5 * TAU,
                axis=RIGHT,
                about_point=[-4.0, 0, 0],
            ),
            *[
                Rotate(
                    stage,
                    angle=1.0 * TAU,
                    axis=RIGHT,
                    about_point=[x, 0, 0],
                )
                for stage, x in zip(
                    compressor_stages,
                    compressor_positions,
                )
            ],
            *[
                Rotate(
                    stage,
                    angle=-1.25 * TAU,
                    axis=RIGHT,
                    about_point=[x, 0, 0],
                )
                for stage, x in zip(
                    turbine_stages,
                    turbine_positions,
                )
            ],
            run_time=2.5,
            rate_func=linear,
        )

        # --------------------------------------------------
        # LABELS — FIXED TO SCREEN
        # --------------------------------------------------
        labels = VGroup(
            Text("FAN", font_size=14, color=CYAN, weight=BOLD),
            Text("COMPRESSOR", font_size=14, color=BLUE, weight=BOLD),
            Text("COMBUSTION", font_size=14, color=ORANGE, weight=BOLD),
            Text("TURBINE", font_size=14, color=GOLD, weight=BOLD),
            Text("EXHAUST", font_size=14, color=ORANGE, weight=BOLD),
        )

        label_positions = [
            [-4.1, -1.65, 0],
            [-2.5, -1.65, 0],
            [-0.55, -1.65, 0],
            [1.4, -1.65, 0],
            [3.4, -1.65, 0],
        ]

        for label, pos in zip(labels, label_positions):
            label.move_to(pos)

        self.add_fixed_in_frame_mobjects(labels)
        self.play(FadeIn(labels), run_time=0.8)

        # --------------------------------------------------
        # CINEMATIC CAMERA MOVE
        # --------------------------------------------------
        self.move_camera(
            phi=65 * DEGREES,
            theta=15 * DEGREES,
            zoom=0.88,
            run_time=2.0,
        )

        # --------------------------------------------------
        # FINAL MESSAGE
        # --------------------------------------------------
        summary = Text(
            "COMPRESS  →  COMBUST  →  EXPAND  →  THRUST",
            font_size=17,
            color=WHITE,
            weight=BOLD,
        ).to_edge(DOWN, buff=0.25)

        self.add_fixed_in_frame_mobjects(summary)
        self.play(FadeIn(summary), run_time=0.8)

        self.wait(2)
