from manim import *
import random
import numpy as np


class SatellitePOC(Scene):
    def construct(self):
        self.camera.background_color = "#030711"
        random.seed(22)

        # -------------------------------------------------
        # 1. Background starfield
        # -------------------------------------------------
        stars = VGroup()
        for _ in range(150):
            x = random.uniform(-7.0, 7.0)
            y = random.uniform(-3.8, 3.8)
            r = random.uniform(0.008, 0.025)
            star = Dot(
                point=[x, y, 0],
                radius=r,
                color=random.choice(["#FFFFFF", "#8FCBFF", "#477CA8"])
            )
            star.set_opacity(random.uniform(0.25, 0.8))
            stars.add(star)

        self.add(stars)
        self.wait(1)

        # -------------------------------------------------
        # 2. Earth, positioned on the left
        # -------------------------------------------------
        earth_center = LEFT * 2.25

        atmosphere = Circle(
            radius=1.62,
            color="#168BFF",
            stroke_width=5,
        ).move_to(earth_center).set_opacity(0.65)

        earth = Circle(
            radius=1.48,
            stroke_color="#58B9FF",
            stroke_width=2,
            fill_color="#073B70",
            fill_opacity=1,
        ).move_to(earth_center)

        # Simplified land masses, constructed in Manim
        land1 = Polygon(
            [-3.05, 0.72, 0],
            [-2.63, 1.05, 0],
            [-2.18, 0.78, 0],
            [-2.32, 0.30, 0],
            [-2.68, 0.12, 0],
            [-2.90, 0.42, 0],
            color="#48C99A",
            fill_color="#168D78",
            fill_opacity=0.9,
            stroke_width=1,
        )

        land2 = Polygon(
            [-2.25, -0.12, 0],
            [-1.94, -0.32, 0],
            [-2.05, -0.83, 0],
            [-2.35, -1.16, 0],
            [-2.52, -0.60, 0],
            color="#48C99A",
            fill_color="#168D78",
            fill_opacity=0.9,
            stroke_width=1,
        )

        land3 = Polygon(
            [-3.45, -0.32, 0],
            [-3.20, -0.15, 0],
            [-3.04, -0.48, 0],
            [-3.25, -0.70, 0],
            color="#48C99A",
            fill_color="#168D78",
            fill_opacity=0.9,
            stroke_width=1,
        )

        # Longitude and latitude curves
        longitude1 = Ellipse(
            width=0.72, height=2.86,
            color="#61BFFF", stroke_width=1.1
        ).move_to(earth_center)

        longitude2 = Ellipse(
            width=1.75, height=2.86,
            color="#61BFFF", stroke_width=0.8
        ).move_to(earth_center)

        latitude1 = Ellipse(
            width=2.90, height=0.72,
            color="#61BFFF", stroke_width=1
        ).move_to(earth_center)

        latitude2 = Ellipse(
            width=2.90, height=1.60,
            color="#61BFFF", stroke_width=0.8
        ).move_to(earth_center)

        # Mask grid and land at the Earth boundary using an overlay.
        # All geometry remains native Manim vector artwork.
        grid = VGroup(
            longitude1, longitude2, latitude1, latitude2
        )

        earth_surface = VGroup(
            earth, land1, land2, land3, grid
        )

        # Draw the globe first, then a subtle atmospheric outline.
        self.play(
            FadeIn(earth),
            FadeIn(land1),
            FadeIn(land2),
            FadeIn(land3),
            run_time=2,
        )
        self.play(
            Create(grid),
            FadeIn(atmosphere),
            run_time=1.5,
        )

        # -------------------------------------------------
        # 3. Orbital trajectory
        # -------------------------------------------------
        orbit = Ellipse(
            width=6.45,
            height=3.55,
            color="#287ED8",
            stroke_width=2,
        ).move_to(earth_center)

        orbit.set_opacity(0.9)
        self.play(Create(orbit), run_time=1.5)

        # -------------------------------------------------
        # 4. Satellite built entirely with Manim geometry
        # -------------------------------------------------
        body = Rectangle(
            width=0.38,
            height=0.34,
            stroke_color="#E9F4FF",
            stroke_width=1.5,
            fill_color="#A9C7DC",
            fill_opacity=1,
        )

        left_panel = Rectangle(
            width=0.62,
            height=0.36,
            stroke_color="#72C7FF",
            stroke_width=1.2,
            fill_color="#0750A0",
            fill_opacity=1,
        ).next_to(body, LEFT, buff=0.04)

        right_panel = Rectangle(
            width=0.62,
            height=0.36,
            stroke_color="#72C7FF",
            stroke_width=1.2,
            fill_color="#0750A0",
            fill_opacity=1,
        ).next_to(body, RIGHT, buff=0.04)

        panel_lines = VGroup()
        for panel in [left_panel, right_panel]:
            panel_lines.add(
                Line(
                    panel.get_top(),
                    panel.get_bottom(),
                    color="#72C7FF",
                    stroke_width=0.8,
                )
            )
            panel_lines.add(
                Line(
                    panel.get_left(),
                    panel.get_right(),
                    color="#72C7FF",
                    stroke_width=0.8,
                )
            )

        antenna = Line(
            body.get_top(),
            body.get_top() + UP * 0.27,
            color="#FFFFFF",
            stroke_width=2,
        )

        antenna_tip = Dot(
            body.get_top() + UP * 0.27,
            radius=0.035,
            color="#65D9FF",
        )

        satellite = VGroup(
            left_panel, right_panel, body,
            panel_lines, antenna, antenna_tip
        )

        satellite.move_to(orbit.point_from_proportion(0))

        self.play(FadeIn(satellite), run_time=1)

        # -------------------------------------------------
        # 5. Satellite completes an orbital journey
        # -------------------------------------------------
        self.play(
            MoveAlongPath(
                satellite,
                orbit,
                rate_func=linear,
            ),
            run_time=6,
        )

        # -------------------------------------------------
        # 6. Signal travelling between satellite and Earth
        # -------------------------------------------------
        signal_path = Line(
            satellite.get_center(),
            earth_center + RIGHT * 0.75,
            color="#48DFFF",
            stroke_width=2,
        )

        self.play(
            Create(signal_path),
            run_time=0.5,
        )

        pulses = VGroup()
        for i in range(3):
            pulse = Dot(
                radius=0.075,
                color="#8AF4FF",
            )
            pulse.move_to(signal_path.get_start())
            pulses.add(pulse)

        self.add(pulses)

        # Animate the pulses in sequence.
        for pulse in pulses:
            self.play(
                MoveAlongPath(
                    pulse,
                    signal_path,
                    rate_func=linear,
                ),
                run_time=0.65,
            )
            self.remove(pulse)

        self.play(FadeOut(signal_path), run_time=0.2)

        # -------------------------------------------------
        # 7. Documentary title reveal
        # -------------------------------------------------
        title = Text(
            "SATELLITE",
            font_size=43,
            weight=BOLD,
            color="#F2F8FF",
        )

        title.move_to([3.55, 0.45, 0])

        underline = Line(
            title.get_left(),
            title.get_left() + RIGHT * 1.15,
            color="#27BFFF",
            stroke_width=4,
        ).next_to(title, DOWN, aligned_edge=LEFT, buff=0.17)

        subtitle = Text(
            "CONNECTING OUR WORLD",
            font_size=15,
            color="#82CFFF",
        ).next_to(underline, DOWN, aligned_edge=LEFT, buff=0.20)

        self.play(
            FadeIn(title, shift=UP * 0.18),
            Create(underline),
            run_time=1.5,
        )

        self.play(FadeIn(subtitle), run_time=0.5)
        self.wait(1.3)
