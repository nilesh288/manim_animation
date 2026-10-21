
from manim import *
import numpy as np
import random


class SatellitePOC03(ThreeDScene):
    def construct(self):
        random.seed(43)
        np.random.seed(43)

        self.camera.background_color = "#020610"
        self.set_camera_orientation(
            phi=68 * DEGREES,
            theta=-48 * DEGREES,
            zoom=1.0,
        )

        earth_center = np.array([-2.1, -0.05, 0.0])
        earth_radius = 1.25

        # Cinematic space background
        stars = VGroup()
        for _ in range(100):
            p = np.array([
                random.uniform(-7, 7),
                random.uniform(-3.8, 3.8),
                random.uniform(-2.2, 2.2),
            ])
            star = Dot3D(
                point=p,
                radius=random.uniform(0.008, 0.018),
                color=random.choice(["#FFFFFF", "#9BD8FF", "#4B8FC7"]),
            )
            star.set_opacity(random.uniform(0.3, 0.8))
            stars.add(star)
        self.add(stars)

        # Earth and atmosphere
        earth = Sphere(
            center=earth_center,
            radius=earth_radius,
            resolution=(24, 48),
        )
        earth.set_color("#07509A")
        earth.set_opacity(1)
        earth.set_stroke("#48B8FF", width=0.6, opacity=0.65)

        atmosphere = Sphere(
            center=earth_center,
            radius=earth_radius * 1.045,
            resolution=(20, 40),
        )
        atmosphere.set_color("#48B8FF")
        atmosphere.set_opacity(0.08)
        atmosphere.set_stroke("#48B8FF", width=1.2, opacity=0.7)

        self.play(FadeIn(earth), run_time=1.0)
        self.play(FadeIn(atmosphere), run_time=0.4)

        # Globe grid
        grid = VGroup()

        for latitude in [-50, -25, 0, 25, 50]:
            a = latitude * DEGREES
            r = earth_radius * np.cos(a)
            z = earth_radius * np.sin(a)

            grid.add(ParametricFunction(
                lambda t, rr=r, zz=z: earth_center + np.array([
                    rr * np.cos(t),
                    rr * np.sin(t),
                    zz,
                ]),
                t_range=[0, TAU],
                color="#55BFFF",
                stroke_width=0.65,
            ))

        for longitude in [-60, -30, 0, 30, 60]:
            a = longitude * DEGREES
            grid.add(ParametricFunction(
                lambda t, aa=a: earth_center + earth_radius * np.array([
                    np.cos(t) * np.cos(aa),
                    np.cos(t) * np.sin(aa),
                    np.sin(t),
                ]),
                t_range=[0, TAU],
                color="#55BFFF",
                stroke_width=0.65,
            ))

        grid.set_opacity(0.38)
        self.play(Create(grid), run_time=0.8)

        # Single-line elliptical orbit
        def orbit_position(t):
            return earth_center + np.array([
                2.85 * np.cos(t),
                1.8 * np.sin(t),
                0.42 * np.sin(t),
            ])

        orbit = ParametricFunction(
            orbit_position,
            t_range=[0, TAU],
            color="#D5E3F0",
            stroke_width=1.25,
            use_smoothing=False,
        )
        orbit.set_fill(opacity=0)
        orbit.set_stroke("#D5E3F0", width=1.25, opacity=0.9)
        self.play(Create(orbit), run_time=0.8)

        # Satellite body and solar panels
        body = Cube(
            side_length=0.30,
            fill_color="#C4D2DC",
            fill_opacity=1,
            stroke_color="#FFFFFF",
            stroke_width=0.8,
        )

        left_panel = Cube(
            side_length=0.1,
            fill_color="#123B73",
            fill_opacity=1,
            stroke_color="#45C7F4",
            stroke_width=0.8,
        )
        left_panel.stretch(3.7, dim=0)
        left_panel.stretch(0.82, dim=1)
        left_panel.stretch(0.14, dim=2)
        left_panel.move_to([-0.39, 0, 0])

        right_panel = Cube(
            side_length=0.1,
            fill_color="#123B73",
            fill_opacity=1,
            stroke_color="#45C7F4",
            stroke_width=0.8,
        )
        right_panel.stretch(3.7, dim=0)
        right_panel.stretch(0.82, dim=1)
        right_panel.stretch(0.14, dim=2)
        right_panel.move_to([0.39, 0, 0])

        panel_lines = VGroup()
        for x in [-0.39, 0.39]:
            for dx in [-0.10, 0, 0.10]:
                panel_lines.add(Line(
                    [x + dx, -0.16, 0.025],
                    [x + dx, 0.16, 0.025],
                    color="#7DD7FF",
                    stroke_width=0.7,
                ))

        antenna = Line(
            [0, 0.14, 0.12],
            [0, 0.47, 0.12],
            color="#FFFFFF",
            stroke_width=1.8,
        )
        antenna_tip = Dot3D(
            point=[0, 0.47, 0.12],
            radius=0.035,
            color="#4CE6FF",
        )

        satellite = VGroup(
            left_panel, right_panel, panel_lines,
            body, antenna, antenna_tip,
        )
        satellite.move_to(orbit_position(0))

        self.play(FadeIn(satellite), run_time=0.4)
        self.play(
            MoveAlongPath(satellite, orbit, rate_func=linear),
            run_time=2.5,
        )

        # Surface stations
        def surface_point(direction):
            d = np.array(direction, dtype=float)
            d /= np.linalg.norm(d)
            return earth_center + d * earth_radius * 1.012, d

        station_a_point, station_a_normal = surface_point([0.90, 0.15, 0.55])
        station_b_point, station_b_normal = surface_point([0.48, 0.78, 0.62])

        def make_station(point, normal, color):
            mast_end = point + normal * 0.18
            return VGroup(
                Dot3D(point=point, radius=0.065, color=color),
                Line(point, mast_end, color=color, stroke_width=2.0),
                Dot3D(point=mast_end, radius=0.035, color=color),
            )

        station_a = make_station(
            station_a_point, station_a_normal, "#FFD166"
        )
        station_b = make_station(
            station_b_point, station_b_normal, "#4CE6FF"
        )

        # Fixed-screen documentary title and captions
        title = Text(
            "SATELLITE COMMUNICATION",
            font_size=24,
            weight=BOLD,
            color=WHITE,
        ).to_corner(UL, buff=0.35)

        subtitle = Text(
            "HOW INFORMATION TRAVELS THROUGH SPACE",
            font_size=11,
            color="#A9C2D8",
        ).next_to(title, DOWN, aligned_edge=LEFT, buff=0.08)

        self.add_fixed_in_frame_mobjects(title, subtitle)
        self.play(FadeIn(title), FadeIn(subtitle), run_time=0.4)

        def caption(main, detail, color):
            a = Text(main, font_size=17, weight=BOLD, color=color)
            b = Text(detail, font_size=11, color="#A9C2D8")
            group = VGroup(a, b).arrange(
                DOWN, aligned_edge=LEFT, buff=0.07
            ).to_corner(DL, buff=0.35)
            self.add_fixed_in_frame_mobjects(group)
            return group

        # Uplink: ground station to satellite
        uplink_label = caption(
            "UPLINK | GROUND TO SATELLITE",
            "Radio signals carry encoded information",
            "#FFD166",
        )
        self.play(FadeIn(station_a), FadeIn(uplink_label), run_time=0.4)

        sat_center = satellite.get_center()
        uplink = Line(
            station_a_point + station_a_normal * 0.18,
            sat_center,
            color="#FFD166",
            stroke_width=1.8,
        )
        self.play(Create(uplink), run_time=0.4)

        for _ in range(3):
            pulse = Dot3D(
                point=uplink.get_start(),
                radius=0.05,
                color="#FFF0B0",
            )
            self.add(pulse)
            self.play(
                MoveAlongPath(pulse, uplink, rate_func=linear),
                run_time=0.45,
            )
            self.remove(pulse)

        self.play(FadeOut(uplink_label), run_time=0.25)

        # Downlink: satellite to receiving station
        downlink_label = caption(
            "DOWNLINK | SATELLITE TO GROUND",
            "The signal is relayed to another location",
            "#4CE6FF",
        )
        self.play(
            FadeIn(station_b),
            FadeIn(downlink_label),
            run_time=0.4,
        )

        downlink = Line(
            sat_center,
            station_b_point + station_b_normal * 0.18,
            color="#4CE6FF",
            stroke_width=1.8,
        )
        self.play(Create(downlink), run_time=0.4)

        for _ in range(3):
            pulse = Dot3D(
                point=downlink.get_start(),
                radius=0.05,
                color="#B7FBFF",
            )
            self.add(pulse)
            self.play(
                MoveAlongPath(pulse, downlink, rate_func=linear),
                run_time=0.45,
            )
            self.remove(pulse)

        self.play(
            FadeOut(uplink),
            FadeOut(downlink_label),
            run_time=0.3,
        )

        # Documentary ending
        self.move_camera(theta=-35 * DEGREES, run_time=0.8)

        final_title = Text(
            "TRANSMIT  •  RELAY  •  RECEIVE",
            font_size=22,
            weight=BOLD,
            color=WHITE,
        ).to_corner(DL, buff=0.35)

        final_subtitle = Text(
            "Satellite links extend communication across vast distances",
            font_size=11,
            color="#A9C2D8",
        ).next_to(final_title, DOWN, aligned_edge=LEFT, buff=0.08)

        self.add_fixed_in_frame_mobjects(final_title, final_subtitle)
        self.play(FadeIn(final_title), FadeIn(final_subtitle), run_time=0.4)
        self.wait(1.0)
