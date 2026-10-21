
from manim import *
import numpy as np

# Manim Community Edition 0.22.0
# POC 6B: Cinematic Jet Engine Reveal

config.background_color = "#07111F"


class JetEnginePOC06B(ThreeDScene):

    def construct(self):
        # --------------------------------------------------
        # PREMIUM COLOR PALETTE
        # --------------------------------------------------
        BG = "#07111F"
        CYAN = "#36D9FF"
        BLUE = "#188DFF"
        ORANGE = "#FF8736"
        GOLD = "#FFD166"
        STEEL = "#A9B9C9"
        DARK_STEEL = "#40546A"
        WHITE = "#F1F6FC"
        MUTED = "#91A5BA"

        self.camera.background_color = BG

        # Engine axis is X. All major components are centered
        # around y=0, z=0 for consistent alignment.
        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-25 * DEGREES,
            zoom=0.76,
        )

        # --------------------------------------------------
        # FIXED SCREEN TITLES
        # --------------------------------------------------
        title = Text(
            "INSIDE A JET ENGINE",
            font_size=27,
            weight=BOLD,
            color=WHITE,
        ).to_edge(UP, buff=0.25)

        subtitle = Text(
            "ENGINEERING • AIRFLOW • PROPULSION",
            font_size=12,
            color=CYAN,
        ).next_to(title, DOWN, buff=0.08)

        caption = Text(
            "THE COMPLETE ENGINE",
            font_size=16,
            weight=BOLD,
            color=CYAN,
        ).to_edge(DOWN, buff=0.28)

        self.add_fixed_in_frame_mobjects(title, subtitle, caption)

        # --------------------------------------------------
        # ENGINE SHAFT
        # --------------------------------------------------
        shaft = Cylinder(
            radius=0.105,
            height=8.7,
            direction=RIGHT,
            resolution=(16, 32),
            color=STEEL,
            fill_color=STEEL,
            fill_opacity=0.95,
            stroke_width=0.4,
        ).move_to([0, 0, 0])

        self.play(
            FadeIn(shaft),
            run_time=1.2,
        )

        # --------------------------------------------------
        # HELPER: AXIAL DISKS
        # --------------------------------------------------
        def make_disk(x, radius, color, opacity=0.95):
            return Cylinder(
                radius=radius,
                height=0.12,
                direction=RIGHT,
                resolution=(20, 40),
                color=color,
                fill_color=color,
                fill_opacity=opacity,
                stroke_color=STEEL,
                stroke_width=0.45,
            ).move_to([x, 0, 0])

        # --------------------------------------------------
        # HELPER: RADIAL BLADE STAGE
        # Blades are centered on the same X-axis as shaft.
        # --------------------------------------------------
        def make_blade_stage(
            x,
            radius,
            count,
            color,
            blade_length=0.48,
            blade_width=0.13,
        ):
            parts = VGroup()

            disk = make_disk(
                x,
                radius * 0.90,
                DARK_STEEL,
                opacity=0.90,
            )
            parts.add(disk)

            for i in range(count):
                angle = TAU * i / count

                blade = Cube(
                    side_length=1,
                    fill_color=color,
                    fill_opacity=0.98,
                    stroke_color=STEEL,
                    stroke_width=0.35,
                )

                # Slim blade with its long dimension radial.
                blade.stretch(blade_width, dim=0)
                blade.stretch(blade_length, dim=1)
                blade.stretch(0.10, dim=2)

                blade.move_to([
                    x,
                    radius * 0.52 * np.cos(angle),
                    radius * 0.52 * np.sin(angle),
                ])

                blade.rotate(
                    angle,
                    axis=RIGHT,
                    about_point=[x, 0, 0],
                )

                parts.add(blade)

            hub = Cylinder(
                radius=0.22,
                height=0.19,
                direction=RIGHT,
                resolution=(16, 24),
                color=STEEL,
                fill_color=STEEL,
                fill_opacity=1,
                stroke_width=0.4,
            ).move_to([x, 0, 0])

            parts.add(hub)
            return parts

        # --------------------------------------------------
        # FAN
        # --------------------------------------------------
        fan_x = -3.85

        fan_frame = make_disk(
            fan_x,
            1.12,
            BLUE,
            opacity=0.95,
        )

        fan = make_blade_stage(
            x=fan_x,
            radius=1.05,
            count=12,
            color=CYAN,
            blade_length=0.86,
            blade_width=0.12,
        )

        fan_ring = Cylinder(
            radius=1.13,
            height=0.13,
            direction=RIGHT,
            resolution=(24, 48),
            color=STEEL,
            fill_color=DARK_STEEL,
            fill_opacity=0.40,
            stroke_color=CYAN,
            stroke_width=1.2,
        ).move_to([fan_x, 0, 0])

        self.play(
            FadeIn(fan_frame),
            FadeIn(fan_ring),
            FadeIn(fan),
            run_time=1.2,
        )

        # --------------------------------------------------
        # COMPRESSOR STAGES
        # --------------------------------------------------
        compressor_xs = [-2.95, -2.35, -1.75, -1.15]
        compressor_radii = [0.91, 0.81, 0.70, 0.59]
        compressor_stages = VGroup()

        for i, (x, radius) in enumerate(
            zip(compressor_xs, compressor_radii)
        ):
            stage = make_blade_stage(
                x=x,
                radius=radius,
                count=10,
                color=BLUE if i % 2 == 0 else CYAN,
                blade_length=0.55,
                blade_width=0.11,
            )
            compressor_stages.add(stage)

        self.play(
            LaggedStart(
                *[FadeIn(stage) for stage in compressor_stages],
                lag_ratio=0.18,
            ),
            run_time=1.5,
        )

        # --------------------------------------------------
        # COMBUSTION CHAMBER
        # --------------------------------------------------
        combustor_x = -0.15

        combustor_shell = Cylinder(
            radius=0.70,
            height=1.35,
            direction=RIGHT,
            resolution=(24, 48),
            color=ORANGE,
            fill_color="#4B2630",
            fill_opacity=0.42,
            stroke_color=ORANGE,
            stroke_width=1.6,
        ).move_to([combustor_x, 0, 0])

        combustor_front = make_disk(
            combustor_x - 0.48,
            0.66,
            GOLD,
            opacity=0.45,
        )

        combustor_back = make_disk(
            combustor_x + 0.48,
            0.66,
            ORANGE,
            opacity=0.45,
        )

        flame = Sphere(
            radius=0.43,
            resolution=(12, 20),
            color=ORANGE,
            fill_color=ORANGE,
            fill_opacity=0.72,
            stroke_width=0,
        ).stretch(1.65, dim=0).move_to([combustor_x, 0, 0])

        flame_core = Sphere(
            radius=0.24,
            resolution=(12, 20),
            color=GOLD,
            fill_color=GOLD,
            fill_opacity=0.88,
            stroke_width=0,
        ).stretch(1.4, dim=0).move_to([combustor_x, 0, 0])

        combustor = VGroup(
            combustor_shell,
            combustor_front,
            combustor_back,
            flame,
            flame_core,
        )

        self.play(
            FadeIn(combustor_shell),
            FadeIn(combustor_front),
            FadeIn(combustor_back),
            run_time=0.9,
        )

        self.play(
            FadeIn(flame),
            FadeIn(flame_core),
            run_time=0.7,
        )

        # --------------------------------------------------
        # TURBINE STAGES
        # --------------------------------------------------
        turbine_xs = [0.95, 1.65, 2.30]
        turbine_radii = [0.63, 0.77, 0.87]
        turbine_stages = VGroup()

        for i, (x, radius) in enumerate(
            zip(turbine_xs, turbine_radii)
        ):
            stage = make_blade_stage(
                x=x,
                radius=radius,
                count=10,
                color=ORANGE if i == 0 else STEEL,
                blade_length=0.50,
                blade_width=0.12,
            )
            turbine_stages.add(stage)

        self.play(
            LaggedStart(
                *[FadeIn(stage) for stage in turbine_stages],
                lag_ratio=0.20,
            ),
            run_time=1.4,
        )

        # --------------------------------------------------
        # EXHAUST NOZZLE
        # --------------------------------------------------
        nozzle_front = make_disk(
            3.05,
            0.85,
            DARK_STEEL,
            opacity=0.85,
        )

        nozzle_exit = make_disk(
            3.75,
            0.96,
            STEEL,
            opacity=0.80,
        )

        nozzle_rings = VGroup()

        for x, radius in [(3.10, 0.88), (3.80, 0.98)]:
            ring = Torus(
                major_radius=radius * 0.78,
                minor_radius=0.055,
                color=STEEL,
                stroke_width=1.0,
            )
            ring.rotate(PI / 2, axis=UP)
            ring.move_to([x, 0, 0])
            nozzle_rings.add(ring)

        self.play(
            FadeIn(nozzle_front),
            FadeIn(nozzle_exit),
            FadeIn(nozzle_rings),
            run_time=1.0,
        )

        # --------------------------------------------------
        # AIRFLOW PARTICLES
        # --------------------------------------------------
        airflow = VGroup()

        for i in range(24):
            x = -4.35 + (i % 8) * 0.22
            y = 0.14 * np.sin(i * 1.7)
            z = 0.14 * np.cos(i * 1.3)

            dot = Sphere(
                radius=0.035,
                resolution=(6, 8),
                color=CYAN,
                fill_color=CYAN,
                fill_opacity=0.90,
                stroke_width=0,
            ).move_to([x, y, z])

            airflow.add(dot)

        self.add(airflow)

        # --------------------------------------------------
        # FULL ENGINE REVEAL
        # --------------------------------------------------
        engine = VGroup(
            shaft,
            fan_frame,
            fan_ring,
            fan,
            compressor_stages,
            combustor,
            turbine_stages,
            nozzle_front,
            nozzle_exit,
            nozzle_rings,
        )

        self.move_camera(
            phi=65 * DEGREES,
            theta=-15 * DEGREES,
            zoom=0.82,
            run_time=1.5,
        )

        self.play(
            *[
                dot.animate.shift(RIGHT * 8.0)
                for dot in airflow
            ],
            Rotate(
                fan,
                angle=TAU,
                axis=RIGHT,
                about_point=[fan_x, 0, 0],
            ),
            run_time=3.0,
            rate_func=linear,
        )

        # --------------------------------------------------
        # CAMERA CLOSE-UP: FAN
        # --------------------------------------------------
        fan_caption = Text(
            "01  FAN — INTAKE AIR",
            font_size=16,
            weight=BOLD,
            color=CYAN,
        ).to_edge(DOWN, buff=0.28)

        self.play(
            Transform(caption, fan_caption),
            run_time=0.8,
        )

        self.move_camera(
            zoom=0.72,
            run_time=0.8,
        )

        self.move_camera(
            frame_center=[fan_x, 0, 0],
            zoom=1.35,
            run_time=1.5,
        )

        self.play(
            Rotate(
                fan,
                angle=TAU * 1.5,
                axis=RIGHT,
                about_point=[fan_x, 0, 0],
            ),
            run_time=2.0,
            rate_func=linear,
        )

        # --------------------------------------------------
        # CAMERA CLOSE-UP: COMPRESSOR
        # --------------------------------------------------
        compressor_caption = Text(
            "02  COMPRESSOR — PRESSURE RISE",
            font_size=16,
            weight=BOLD,
            color=CYAN,
        ).to_edge(DOWN, buff=0.28)

        self.play(
            Transform(caption, compressor_caption),
            run_time=0.4,
        )

        self.move_camera(
            frame_center=[-2.05, 0, 0],
            zoom=1.32,
            run_time=1.4,
        )

        compressor_rotations = []

        for x in compressor_xs:
            compressor_rotations.append(
                Rotate(
                    compressor_stages[
                        compressor_xs.index(x)
                    ],
                    angle=TAU,
                    axis=RIGHT,
                    about_point=[x, 0, 0],
                )
            )

        self.play(
            *compressor_rotations,
            run_time=2.2,
            rate_func=linear,
        )

        # --------------------------------------------------
        # CAMERA CLOSE-UP: COMBUSTION
        # --------------------------------------------------
        combustion_caption = Text(
            "03  COMBUSTION — ENERGY RELEASE",
            font_size=16,
            weight=BOLD,
            color=ORANGE,
        ).to_edge(DOWN, buff=0.28)

        self.play(
            Transform(caption, combustion_caption),
            run_time=0.4,
        )

        self.move_camera(
            frame_center=[combustor_x, 0, 0],
            zoom=1.35,
            run_time=1.4,
        )

        self.play(
            flame.animate.scale(1.13),
            flame_core.animate.scale(1.16),
            run_time=0.45,
        )

        self.play(
            flame.animate.scale(0.885),
            flame_core.animate.scale(0.862),
            run_time=0.45,
        )

        self.play(
            Indicate(
                combustor_shell,
                color=ORANGE,
                scale_factor=1.04,
            ),
            run_time=0.8,
        )

        # --------------------------------------------------
        # CAMERA CLOSE-UP: TURBINE
        # --------------------------------------------------
        turbine_caption = Text(
            "04  TURBINE — POWER EXTRACTION",
            font_size=16,
            weight=BOLD,
            color=GOLD,
        ).to_edge(DOWN, buff=0.28)

        self.play(
            Transform(caption, turbine_caption),
            run_time=0.4,
        )

        self.move_camera(
            frame_center=[1.65, 0, 0],
            zoom=1.28,
            run_time=1.4,
        )

        turbine_rotations = []

        for i, x in enumerate(turbine_xs):
            turbine_rotations.append(
                Rotate(
                    turbine_stages[i],
                    angle=-TAU,
                    axis=RIGHT,
                    about_point=[x, 0, 0],
                )
            )

        self.play(
            *turbine_rotations,
            run_time=2.2,
            rate_func=linear,
        )

        # --------------------------------------------------
        # EXHAUST FLOW
        # --------------------------------------------------
        exhaust_caption = Text(
            "05  EXHAUST — THRUST",
            font_size=16,
            weight=BOLD,
            color=ORANGE,
        ).to_edge(DOWN, buff=0.28)

        self.play(
            Transform(caption, exhaust_caption),
            run_time=0.4,
        )

        self.move_camera(
            frame_center=[3.1, 0, 0],
            zoom=1.35,
            run_time=1.2,
        )

        exhaust_particles = VGroup()

        for i in range(14):
            y = 0.30 * np.sin(i * 1.7)
            z = 0.30 * np.cos(i * 1.2)

            particle = Sphere(
                radius=0.045,
                resolution=(6, 8),
                color=ORANGE if i % 2 == 0 else GOLD,
                fill_opacity=0.95,
                stroke_width=0,
            ).move_to([3.65, y, z])

            exhaust_particles.add(particle)

        self.add(exhaust_particles)

        self.play(
            *[
                particle.animate.shift(
                    RIGHT * (1.4 + 0.10 * (i % 4))
                ).set_opacity(0)
                for i, particle in enumerate(exhaust_particles)
            ],
            run_time=1.4,
            rate_func=linear,
        )

        # --------------------------------------------------
        # FINAL FULL-ENGINE SHOT
        # --------------------------------------------------
        final_caption = Text(
            "FROM AIRFLOW TO THRUST",
            font_size=18,
            weight=BOLD,
            color=CYAN,
        ).to_edge(DOWN, buff=0.28)

        self.play(
            Transform(caption, final_caption),
            run_time=0.5,
        )

        self.move_camera(
            frame_center=[-0.15, 0, 0],
            phi=68 * DEGREES,
            theta=-22 * DEGREES,
            zoom=0.76,
            run_time=2.2,
        )

        self.play(
            Rotate(
                fan,
                angle=TAU,
                axis=RIGHT,
                about_point=[fan_x, 0, 0],
            ),
            *[
                Rotate(
                    compressor_stages[i],
                    angle=TAU,
                    axis=RIGHT,
                    about_point=[x, 0, 0],
                )
                for i, x in enumerate(compressor_xs)
            ],
            *[
                Rotate(
                    turbine_stages[i],
                    angle=-TAU,
                    axis=RIGHT,
                    about_point=[x, 0, 0],
                )
                for i, x in enumerate(turbine_xs)
            ],
            run_time=2.5,
            rate_func=linear,
        )

        self.wait(1.5)
