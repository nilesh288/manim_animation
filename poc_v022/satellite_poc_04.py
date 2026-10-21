
from manim import *
import numpy as np
import random


class SatellitePOC04(ThreeDScene):
    def construct(self):
        random.seed(44)
        np.random.seed(44)

        self.camera.background_color = "#02040C"
        self.set_camera_orientation(
            phi=68 * DEGREES,
            theta=-48 * DEGREES,
            zoom=0.95,
        )

        earth_center = np.array([-1.65, 0.0, 0.0])
        R = 1.35

        # --------------------------------------------------
        # 1. Deep-space star field
        # --------------------------------------------------
        stars = VGroup()

        for _ in range(130):
            point = np.array([
                random.uniform(-7.2, 7.2),
                random.uniform(-4.0, 4.0),
                random.uniform(-2.5, 2.5),
            ])

            star = Dot3D(
                point=point,
                radius=random.uniform(0.006, 0.017),
                color=random.choice([
                    "#FFFFFF", "#9BCFFF", "#527DA8"
                ]),
            )
            star.set_opacity(random.uniform(0.3, 0.8))
            stars.add(star)

        self.add(stars)

        # --------------------------------------------------
        # 2. Earth and atmospheric rim
        # --------------------------------------------------
        earth = Sphere(
            center=earth_center,
            radius=R,
            resolution=(32, 64),
        )
        earth.set_color("#07509A")
        earth.set_opacity(1)
        earth.set_shade_in_3d(True)
        earth.set_stroke(
            color="#328FE0",
            width=0.45,
            opacity=0.5,
        )

        atmosphere = Sphere(
            center=earth_center,
            radius=R * 1.035,
            resolution=(24, 48),
        )
        atmosphere.set_color("#32A9FF")
        atmosphere.set_opacity(0.055)
        atmosphere.set_stroke(
            color="#55C5FF",
            width=1.0,
            opacity=0.7,
        )

        outer_atmosphere = Sphere(
            center=earth_center,
            radius=R * 1.065,
            resolution=(20, 40),
        )
        outer_atmosphere.set_color("#167BFF")
        outer_atmosphere.set_opacity(0.018)
        outer_atmosphere.set_stroke(
            color="#168CFF",
            width=0.7,
            opacity=0.35,
        )

        self.play(FadeIn(earth), run_time=1.2)
        self.play(
            FadeIn(atmosphere),
            FadeIn(outer_atmosphere),
            run_time=0.6,
        )

        # --------------------------------------------------
        # 3. Globe grid
        # --------------------------------------------------
        grid = VGroup()

        for latitude in [-60, -30, 0, 30, 60]:
            a = latitude * DEGREES
            rr = R * np.cos(a)
            zz = R * np.sin(a)

            curve = ParametricFunction(
                lambda t, r=rr, z=zz: earth_center + np.array([
                    r * np.cos(t),
                    r * np.sin(t),
                    z,
                ]),
                t_range=[0, TAU],
                color="#55BFFF",
                stroke_width=0.6,
            )
            grid.add(curve)

        for longitude in [-60, -30, 0, 30, 60]:
            a = longitude * DEGREES

            curve = ParametricFunction(
                lambda t, ang=a: earth_center + R * np.array([
                    np.cos(t) * np.cos(ang),
                    np.cos(t) * np.sin(ang),
                    np.sin(t),
                ]),
                t_range=[0, TAU],
                color="#55BFFF",
                stroke_width=0.6,
            )
            grid.add(curve)

        grid.set_opacity(0.42)
        self.play(Create(grid), run_time=1.2)

        # --------------------------------------------------
        # 4. Thin orbital path
        # --------------------------------------------------
        def orbit_position(t):
            return earth_center + np.array([
                3.05 * np.cos(t),
                1.95 * np.sin(t),
                0.30 * np.sin(t),
            ])

        orbit = ParametricFunction(
            orbit_position,
            t_range=[0, TAU],
            color="#D8E6F5",
            stroke_width=1.15,
            use_smoothing=False,
        )
        orbit.set_fill(opacity=0)
        orbit.set_stroke(
            color="#D8E6F5",
            width=1.15,
            opacity=0.9,
        )

        self.play(Create(orbit), run_time=1.0)

        # --------------------------------------------------
        # 5. Detailed satellite model
        # --------------------------------------------------
        body = Cube(
            side_length=0.27,
            fill_color="#D4DEE8",
            fill_opacity=1,
            stroke_color="#FFFFFF",
            stroke_width=0.8,
        )

        left_panel = Cube(
            side_length=0.1,
            fill_color="#123B73",
            fill_opacity=1,
            stroke_color="#45C7F4",
            stroke_width=0.7,
        )
        left_panel.stretch(3.5, dim=0)
        left_panel.stretch(0.85, dim=1)
        left_panel.stretch(0.12, dim=2)
        left_panel.move_to([-0.36, 0, 0])

        right_panel = left_panel.copy()
        right_panel.move_to([0.36, 0, 0])

        panel_details = VGroup()
        for x in [-0.36, 0.36]:
            for dx in [-0.08, 0, 0.08]:
                panel_details.add(
                    Line(
                        [x + dx, -0.15, 0.025],
                        [x + dx, 0.15, 0.025],
                        color="#7DD7FF",
                        stroke_width=0.65,
                    )
                )

        antenna = Line(
            [0, 0.12, 0.12],
            [0, 0.42, 0.12],
            color="#FFFFFF",
            stroke_width=1.5,
        )

        antenna_tip = Dot3D(
            point=[0, 0.42, 0.12],
            radius=0.03,
            color="#4CE6FF",
        )

        satellite = VGroup(
            left_panel,
            right_panel,
            panel_details,
            body,
            antenna,
            antenna_tip,
        )
        satellite.move_to(orbit_position(0))

        self.play(FadeIn(satellite), run_time=0.5)

        # Slow camera movement during satellite travel.
        self.move_camera(
            theta=-35 * DEGREES,
            run_time=2.0,
        )

        self.play(
            MoveAlongPath(
                satellite,
                orbit,
                rate_func=linear,
            ),
            run_time=3.0,
        )

        # --------------------------------------------------
        # 6. Ground stations
        # --------------------------------------------------
        def surface_point(direction):
            d = np.array(direction, dtype=float)
            d /= np.linalg.norm(d)
            return earth_center + d * R * 1.012, d

        station_a_point, normal_a = surface_point(
            [0.90, 0.15, 0.55]
        )
        station_b_point, normal_b = surface_point(
            [0.48, 0.78, 0.62]
        )

        def make_station(point, normal, color):
            mast_end = point + normal * 0.18
            return VGroup(
                Dot3D(point=point, radius=0.065, color=color),
                Line(
                    point,
                    mast_end,
                    color=color,
                    stroke_width=2,
                ),
                Dot3D(
                    point=mast_end,
                    radius=0.035,
                    color=color,
                ),
            )

        station_a = make_station(
            station_a_point, normal_a, "#FFD166"
        )
        station_b = make_station(
            station_b_point, normal_b, "#4CE6FF"
        )

        # Fixed screen titles
        title = Text(
            "SATELLITE COMMUNICATION",
            font_size=25,
            weight=BOLD,
            color=WHITE,
        ).to_corner(UL, buff=0.35)

        subtitle = Text(
            "HOW INFORMATION TRAVELS THROUGH SPACE",
            font_size=11,
            color="#A9C2D8",
        ).next_to(title, DOWN, aligned_edge=LEFT, buff=0.08)

        self.add_fixed_in_frame_mobjects(title, subtitle)
        self.play(FadeIn(title), FadeIn(subtitle), run_time=0.5)

        def show_caption(main, detail, color):
            heading = Text(
                main,
                font_size=17,
                weight=BOLD,
                color=color,
            )
            detail_text = Text(
                detail,
                font_size=11,
                color="#A9C2D8",
            )

            group = VGroup(
                heading,
                detail_text,
            ).arrange(
                DOWN,
                aligned_edge=LEFT,
                buff=0.07,
            ).to_corner(DL, buff=0.35)

            self.add_fixed_in_frame_mobjects(group)
            self.play(FadeIn(group), run_time=0.35)
            return group

        # --------------------------------------------------
        # 7. Uplink: station A to satellite
        # --------------------------------------------------
        self.play(FadeIn(station_a), run_time=0.35)

        caption_a = show_caption(
            "UPLINK",
            "Encoded radio signals travel to the satellite",
            "#FFD166",
        )

        satellite_point = satellite.get_center()
        station_a_tip = station_a_point + normal_a * 0.18

        uplink = Line(
            station_a_tip,
            satellite_point,
            color="#FFD166",
            stroke_width=2.0,
        )
        self.play(Create(uplink), run_time=0.5)

        for _ in range(4):
            pulse = Dot3D(
                point=uplink.get_start(),
                radius=0.045,
                color="#FFF0B0",
            )
            self.add(pulse)
            self.play(
                MoveAlongPath(
                    pulse,
                    uplink,
                    rate_func=linear,
                ),
                run_time=0.35,
            )
            self.remove(pulse)

        self.play(
            FadeOut(uplink),
            FadeOut(caption_a),
            run_time=0.3,
        )

        # --------------------------------------------------
        # 8. Downlink: satellite to station B
        # --------------------------------------------------
        self.play(FadeIn(station_b), run_time=0.35)

        caption_b = show_caption(
            "DOWNLINK",
            "The satellite relays information to Earth",
            "#4CE6FF",
        )

        station_b_tip = station_b_point + normal_b * 0.18

        downlink = Line(
            satellite_point,
            station_b_tip,
            color="#4CE6FF",
            stroke_width=2.0,
        )
        self.play(Create(downlink), run_time=0.5)

        for _ in range(4):
            pulse = Dot3D(
                point=downlink.get_start(),
                radius=0.045,
                color="#B7FBFF",
            )
            self.add(pulse)
            self.play(
                MoveAlongPath(
                    pulse,
                    downlink,
                    rate_func=linear,
                ),
                run_time=0.35,
            )
            self.remove(pulse)

        self.play(
            FadeOut(downlink),
            FadeOut(caption_b),
            run_time=0.3,
        )

        # --------------------------------------------------
        # 9. Cinematic pullback and final title
        # --------------------------------------------------
        self.move_camera(
            phi=62 * DEGREES,
            theta=-20 * DEGREES,
            zoom=0.88,
            run_time=1.5,
        )

        final_title = Text(
            "TRANSMIT  •  RELAY  •  RECEIVE",
            font_size=22,
            weight=BOLD,
            color=WHITE,
        ).to_corner(DL, buff=0.35)

        final_subtitle = Text(
            "Connecting distant places through space",
            font_size=12,
            color="#A9C2D8",
        ).next_to(
            final_title,
            DOWN,
            aligned_edge=LEFT,
            buff=0.08,
        )

        self.add_fixed_in_frame_mobjects(
            final_title,
            final_subtitle,
        )
        self.play(
            FadeIn(final_title),
            FadeIn(final_subtitle),
            run_time=0.5,
        )
        self.wait(2)
