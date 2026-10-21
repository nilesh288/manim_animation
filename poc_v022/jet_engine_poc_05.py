from manim import *
import numpy as np

# POC 5: How a Jet Engine Works
# Manim Community Edition 0.22.0
# Preview: 854x480 at 15 FPS
# All rendering output is directed to /dev/shm

config.background_color = "#07111F"


class JetEnginePOC05(Scene):
    def construct(self):
        self.camera.background_color = "#07111F"

        # --------------------------------------------------
        # COLORS
        # --------------------------------------------------
        STEEL = "#A9B9C9"
        STEEL_DARK = "#40546A"
        CYAN = "#36D9FF"
        BLUE = "#188DFF"
        ORANGE = "#FF8A35"
        YELLOW = "#FFD166"
        WHITE = "#F1F6FC"
        MUTED = "#8195AB"

        # --------------------------------------------------
        # TITLE
        # --------------------------------------------------
        title = Text(
            "INSIDE A JET ENGINE",
            font_size=29,
            weight=BOLD,
            color=WHITE,
        ).to_edge(UP, buff=0.3)

        subtitle = Text(
            "HOW AIR BECOMES THRUST",
            font_size=13,
            color=CYAN,
        ).next_to(title, DOWN, buff=0.08)

        self.play(
            FadeIn(title, shift=DOWN * 0.2),
            FadeIn(subtitle),
            run_time=1.2,
        )

        # --------------------------------------------------
        # ENGINE CUTAWAY OUTLINE
        # --------------------------------------------------
        # Engine runs horizontally from left to right.
        # Each section has a distinct technical color.

        top_points = [
            [-5.9, 0.72, 0],
            [-5.15, 1.30, 0],
            [-3.85, 1.15, 0],
            [-2.2, 0.95, 0],
            [-0.55, 0.82, 0],
            [0.75, 0.80, 0],
            [2.3, 0.92, 0],
            [3.6, 1.05, 0],
            [5.45, 0.58, 0],
        ]

        bottom_points = [
            [5.45, -0.58, 0],
            [3.6, -1.05, 0],
            [2.3, -0.92, 0],
            [0.75, -0.80, 0],
            [-0.55, -0.82, 0],
            [-2.2, -0.95, 0],
            [-3.85, -1.15, 0],
            [-5.15, -1.30, 0],
            [-5.9, -0.72, 0],
        ]

        top_shell = VMobject(
            stroke_color=STEEL,
            stroke_width=3,
        ).set_points_as_corners(top_points)

        bottom_shell = VMobject(
            stroke_color=STEEL,
            stroke_width=3,
        ).set_points_as_corners(bottom_points)

        rear_edge = Line(
            [5.45, -0.58, 0],
            [5.45, 0.58, 0],
            color=STEEL,
            stroke_width=2,
        )

        self.play(
            Create(top_shell),
            Create(bottom_shell),
            Create(rear_edge),
            run_time=1.4,
        )

        # --------------------------------------------------
        # COMPONENT HELPER FUNCTIONS
        # --------------------------------------------------
        def stage_blades(x, count, height, color, lean=0.18):
            blades = VGroup()

            for i in range(count):
                y = np.interp(i, [0, count - 1],
                              [-height, height])

                blade = Polygon(
                    [x - lean, y - 0.13, 0],
                    [x + lean, y + 0.10, 0],
                    [x + lean * 0.35, y + 0.25, 0],
                    [x - lean * 0.55, y + 0.04, 0],
                    stroke_color=color,
                    stroke_width=1,
                    fill_color=color,
                    fill_opacity=0.85,
                )
                blades.add(blade)

            return blades

        def stage_ring(x, height, color=STEEL_DARK):
            return VGroup(
                Line(
                    [x, -height, 0],
                    [x, height, 0],
                    color=color,
                    stroke_width=2,
                ),
                Circle(
                    radius=0.07,
                    color=color,
                    fill_opacity=1,
                ).move_to([x, 0, 0]),
            )

        def component_label(text, point, color=WHITE, above=True):
            label = Text(
                text,
                font_size=15,
                weight=BOLD,
                color=color,
            )

            label.move_to(point)

            end_y = point[1] - 0.45 if above else point[1] + 0.45
            connector = Line(
                [point[0], end_y, 0],
                [point[0], point[1] - 0.18 if above
                 else point[1] + 0.18, 0],
                color=color,
                stroke_width=1.3,
            )

            return VGroup(label, connector)

        # --------------------------------------------------
        # 1. FRONT FAN
        # --------------------------------------------------
        fan_x = -4.85

        fan_hub = Circle(
            radius=0.20,
            color=CYAN,
            fill_color="#16394B",
            fill_opacity=1,
            stroke_width=2,
        ).move_to([fan_x, 0, 0])

        fan_blades = VGroup()

        for i in range(12):
            angle = i * TAU / 12

            inner = np.array([
                fan_x + 0.18 * np.cos(angle),
                0.18 * np.sin(angle),
                0,
            ])

            outer = np.array([
                fan_x + 0.18 * np.cos(angle + 0.22),
                0.94 * np.sin(angle + 0.22),
                0,
            ])

            blade = Line(
                inner,
                outer,
                color=CYAN,
                stroke_width=4,
            )
            fan_blades.add(blade)

        fan_label = Text(
            "FAN",
            font_size=15,
            color=CYAN,
            weight=BOLD,
        ).move_to([-4.85, 1.65, 0])

        self.play(
            LaggedStart(
                *[Create(b) for b in fan_blades],
                lag_ratio=0.04,
            ),
            FadeIn(fan_hub),
            FadeIn(fan_label),
            run_time=1.4,
        )

        # --------------------------------------------------
        # 2. COMPRESSOR STAGES
        # --------------------------------------------------
        compressor = VGroup()

        compressor_xs = [-3.95, -3.45, -2.95, -2.45, -1.95]

        for i, x in enumerate(compressor_xs):
            height = 0.80 - i * 0.07

            compressor.add(stage_ring(x, height))
            compressor.add(
                stage_blades(
                    x + 0.12,
                    7,
                    height * 0.82,
                    BLUE,
                    lean=0.12,
                )
            )

        compressor_label = Text(
            "COMPRESSOR",
            font_size=15,
            color=BLUE,
            weight=BOLD,
        ).move_to([-3.0, 1.55, 0])

        self.play(
            FadeIn(compressor_label),
            LaggedStart(
                *[Create(obj) for obj in compressor],
                lag_ratio=0.08,
            ),
            run_time=1.8,
        )

        # --------------------------------------------------
        # 3. COMBUSTION CHAMBER
        # --------------------------------------------------
        combustor_body = RoundedRectangle(
            width=1.55,
            height=1.12,
            corner_radius=0.18,
            stroke_color=ORANGE,
            stroke_width=2.5,
            fill_color="#351B20",
            fill_opacity=0.9,
        ).move_to([-0.45, 0, 0])

        flame_shapes = VGroup()

        for i in range(5):
            x = -1.00 + i * 0.24

            flame = Polygon(
                [x, -0.36, 0],
                [x + 0.18, 0.02, 0],
                [x + 0.05, 0.37, 0],
                [x + 0.34, 0.06, 0],
                [x + 0.30, -0.36, 0],
                stroke_width=0,
                fill_color=ORANGE if i % 2 == 0 else YELLOW,
                fill_opacity=0.82,
            )
            flame_shapes.add(flame)

        flame_shapes.move_to([-0.45, 0, 0])

        combustor_label = Text(
            "COMBUSTION",
            font_size=15,
            color=ORANGE,
            weight=BOLD,
        ).move_to([-0.45, 1.55, 0])

        self.play(
            Create(combustor_body),
            FadeIn(combustor_label),
            run_time=0.8,
        )

        self.play(
            LaggedStart(
                *[FadeIn(f) for f in flame_shapes],
                lag_ratio=0.08,
            ),
            run_time=1.1,
        )

        self.play(
            combustor_body.animate.set_fill(
                color="#6A2920",
                opacity=1,
            ),
            flame_shapes.animate.set_opacity(1),
            run_time=0.7,
        )

        # --------------------------------------------------
        # 4. TURBINE
        # --------------------------------------------------
        turbine_xs = [0.85, 1.35, 1.85, 2.35]

        turbine = VGroup()

        for i, x in enumerate(turbine_xs):
            height = 0.70 + i * 0.055

            turbine.add(stage_ring(x, height, STEEL))
            turbine.add(
                stage_blades(
                    x + 0.10,
                    7,
                    height * 0.83,
                    ORANGE,
                    lean=-0.13,
                )
            )

        turbine_label = Text(
            "TURBINE",
            font_size=15,
            color=YELLOW,
            weight=BOLD,
        ).move_to([1.65, 1.55, 0])

        self.play(
            FadeIn(turbine_label),
            LaggedStart(
                *[Create(obj) for obj in turbine],
                lag_ratio=0.07,
            ),
            run_time=1.6,
        )

        # --------------------------------------------------
        # 5. EXHAUST NOZZLE
        # --------------------------------------------------
        nozzle = VGroup(
            Line(
                [3.0, 0.80, 0],
                [4.0, 0.50, 0],
                color=STEEL,
                stroke_width=3,
            ),
            Line(
                [3.0, -0.80, 0],
                [4.0, -0.50, 0],
                color=STEEL,
                stroke_width=3,
            ),
            Line(
                [4.0, 0.50, 0],
                [5.45, 0.58, 0],
                color=STEEL,
                stroke_width=3,
            ),
            Line(
                [4.0, -0.50, 0],
                [5.45, -0.58, 0],
                color=STEEL,
                stroke_width=3,
            ),
        )

        exhaust_label = Text(
            "EXHAUST",
            font_size=15,
            color=ORANGE,
            weight=BOLD,
        ).move_to([4.25, 1.25, 0])

        self.play(
            Create(nozzle),
            FadeIn(exhaust_label),
            run_time=1.0,
        )

        # --------------------------------------------------
        # 6. AIRFLOW ANIMATION
        # --------------------------------------------------
        inlet_air = VGroup()

        for i in range(9):
            dot = Dot(
                point=[-6.4 + i * 0.16, 0, 0],
                radius=0.045,
                color=CYAN,
            )
            inlet_air.add(dot)

        inlet_label = Text(
            "COLD AIR IN",
            font_size=13,
            color=CYAN,
        ).move_to([-5.3, -1.72, 0])

        self.play(FadeIn(inlet_label), FadeIn(inlet_air))

        self.play(
            inlet_air.animate.shift(RIGHT * 2.5),
            run_time=1.8,
            rate_func=linear,
        )

        self.play(
            FadeOut(inlet_air),
            run_time=0.3,
        )

        # Air through compressor
        compression_air = VGroup()

        for i in range(13):
            x = -4.0 + i * 0.20
            dot = Dot(
                [x, 0, 0],
                radius=0.045,
                color=BLUE,
            )
            compression_air.add(dot)

        self.play(FadeIn(compression_air), run_time=0.3)

        self.play(
            compression_air.animate.shift(RIGHT * 2.1),
            run_time=1.4,
            rate_func=linear,
        )

        self.play(
            FadeOut(compression_air),
            run_time=0.3,
        )

        # Hot gases through turbine and exhaust
        hot_gas = VGroup()

        for i in range(18):
            x = -0.15 + i * 0.24
            dot = Dot(
                [x, 0, 0],
                radius=0.055,
                color=ORANGE if i % 2 else YELLOW,
            )
            hot_gas.add(dot)

        self.play(FadeIn(hot_gas), run_time=0.3)

        self.play(
            hot_gas.animate.shift(RIGHT * 2.8),
            run_time=1.5,
            rate_func=linear,
        )

        self.play(
            FadeOut(hot_gas),
            run_time=0.3,
        )

        # --------------------------------------------------
        # 7. EXHAUST PLUME
        # --------------------------------------------------
        plume_layers = VGroup()

        for i in range(7):
            y = -0.32 + i * 0.105

            line = Line(
                [5.25, y, 0],
                [6.35, y * 1.5, 0],
                color=ORANGE if i % 2 == 0 else YELLOW,
                stroke_width=3 if i % 2 == 0 else 2,
            )

            plume_layers.add(line)

        thrust_label = Text(
            "THRUST",
            font_size=17,
            color=ORANGE,
            weight=BOLD,
        ).move_to([5.9, 1.25, 0])

        self.play(
            FadeIn(thrust_label),
            LaggedStart(
                *[Create(line) for line in plume_layers],
                lag_ratio=0.1,
            ),
            run_time=1.0,
        )

        # Animate exhaust plume motion
        self.play(
            plume_layers.animate.shift(RIGHT * 0.35),
            run_time=0.8,
            rate_func=linear,
        )

        # --------------------------------------------------
        # 8. FINAL ENGINE OVERVIEW
        # --------------------------------------------------
        summary = Text(
            "COMPRESS  →  COMBUST  →  EXPAND  →  THRUST",
            font_size=18,
            weight=BOLD,
            color=WHITE,
        ).to_edge(DOWN, buff=0.30)

        summary_background = SurroundingRectangle(
            summary,
            color=CYAN,
            buff=0.12,
            corner_radius=0.08,
            stroke_width=1.5,
        )

        self.play(
            FadeIn(summary_background),
            FadeIn(summary, shift=UP * 0.15),
            run_time=1.0,
        )

        self.wait(2)
