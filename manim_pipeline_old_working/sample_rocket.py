"""
sample_rocket.py - Editorial Infographic Scene: Rocket Launch & Satellite Deployment
11-Second synchronized demonstration with vector staging and orbital insertion.
"""
from manim import *
import numpy as np

# Editorial Pastel Palette
PALETTE = {
    "bg": "#F8F9FA",           # Warm off-white
    "stroke": "#2D3748",       # Slate charcoal
    "stroke_light": "#CBD5E0", # Subtle gray for orbit & trajectory
    "text": "#1A202C",         # Deep slate black
    "text_dim": "#718096",     # Secondary telemetry gray
    "indigo": "#5A67D8",       # Satellite bus & payload
    "blue": "#4299E1",         # Atmosphere & orbital path
    "amber": "#ED8936",        # Rocket engine plume & telemetry
    "coral": "#E53E3E",        # Stage separation / booster
    "mint": "#38A169",         # Nominal orbit confirmation
}


class VectorRocket(VGroup):
    """Modular two-stage rocket with detachable booster and fairings."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        col_body = PALETTE["stroke"]
        
        # --- Stage 1: Booster ---
        self.stage1_body = Rectangle(
            width=0.22, height=0.7,
            color=col_body, fill_color="#E2E8F0", fill_opacity=1.0, stroke_width=2.0
        )
        fin_l = Polygon(
            [-0.11, -0.35, 0], [-0.22, -0.35, 0], [-0.11, -0.15, 0],
            color=col_body, fill_color=PALETTE["coral"], fill_opacity=0.8, stroke_width=1.5
        )
        fin_r = Polygon(
            [0.11, -0.35, 0], [0.22, -0.35, 0], [0.11, -0.15, 0],
            color=col_body, fill_color=PALETTE["coral"], fill_opacity=0.8, stroke_width=1.5
        )
        self.plume = Polygon(
            [-0.08, -0.35, 0], [0.08, -0.35, 0], [0, -0.65, 0],
            color=PALETTE["amber"], fill_color=PALETTE["amber"], fill_opacity=0.85, stroke_width=0
        )
        self.stage1 = VGroup(self.stage1_body, fin_l, fin_r, self.plume)

        # --- Stage 2 & Fairing ---
        self.stage2_body = Rectangle(
            width=0.20, height=0.45,
            color=col_body, fill_color=PALETTE["bg"], fill_opacity=1.0, stroke_width=2.0
        ).next_to(self.stage1_body, UP, buff=0.03)

        self.fairing_l = Polygon(
            [-0.10, 0, 0], [0, 0.35, 0], [0, 0, 0],
            color=col_body, fill_color="#EDF2F7", fill_opacity=1.0, stroke_width=1.8
        ).next_to(self.stage2_body, UP, buff=0.01).align_to(self.stage2_body, LEFT)

        self.fairing_r = Polygon(
            [0.10, 0, 0], [0, 0.35, 0], [0, 0, 0],
            color=col_body, fill_color="#EDF2F7", fill_opacity=1.0, stroke_width=1.8
        ).next_to(self.stage2_body, UP, buff=0.01).align_to(self.stage2_body, RIGHT)

        self.stage2 = VGroup(self.stage2_body, self.fairing_l, self.fairing_r)
        self.add(self.stage1, self.stage2)


class RocketLaunchScene(Scene):
    def construct(self):
        self.camera.background_color = PALETTE["bg"]

        # ---------------------------------------------------------
        # Spatial Geometry & Launch Path Setup
        # ---------------------------------------------------------
        earth_center = DOWN * 6.5 + LEFT * 3.5

        # 1. Earth Surface & Atmospheric Karman Line Arc
        earth_surface = Arc(
            radius=5.2, start_angle=0.15, angle=1.25,
            arc_center=earth_center, color=PALETTE["stroke_light"], stroke_width=2.5
        )
        atmo_boundary = Arc(
            radius=6.6, start_angle=0.18, angle=1.15,
            arc_center=earth_center, color=PALETTE["blue"], stroke_width=1.5
        ).set_stroke(opacity=0.5)

        # Uses point_from_proportion (native to all Manim curves)
        atmo_tag = Text("KÁRMÁN LINE // 100 km", font="sans-serif", font_size=10, color=PALETTE["blue"])
        atmo_tag.next_to(atmo_boundary.point_from_proportion(0.6), UP + LEFT, buff=0.1)

        # 2. Gravity Turn Trajectory (Cubic Bezier path to orbit)
        launch_pt = LEFT * 3.8 + DOWN * 1.3
        staging_pt = LEFT * 0.8 + UP * 0.6
        orbit_pt = RIGHT * 3.2 + UP * 2.2

        trajectory = CubicBezier(
            launch_pt,
            launch_pt + UP * 1.8 + RIGHT * 0.4,
            staging_pt + LEFT * 1.0 + DOWN * 0.4,
            staging_pt,
            color=PALETTE["stroke_light"], stroke_width=1.5
        )

        orbit_arc = Arc(
            radius=7.8, start_angle=0.55, angle=0.85,
            arc_center=earth_center, color=PALETTE["indigo"], stroke_width=1.8
        )

        # 3. The Rocket Actor
        rocket = VectorRocket().scale(0.8).move_to(launch_pt).rotate(-0.1)

        # ---------------------------------------------------------
        # BEAT 1: Liftoff & Atmospheric Ascent (Duration: 3.50s)
        # Motion: 1.30s | Hold: 2.20s
        # ---------------------------------------------------------
        launch_tag_path = VMobject(color=PALETTE["stroke_light"], stroke_width=1.4)
        launch_tag_path.set_points_as_corners([
            launch_pt + RIGHT * 0.3,
            launch_pt + RIGHT * 1.2 + UP * 0.5,
            launch_pt + RIGHT * 2.0 + UP * 0.5
        ])
        launch_tag = Text("LIFTOFF // MAX-Q", font="sans-serif", font_size=12, color=PALETTE["text"]).next_to(launch_tag_path.get_end(), UP, buff=0.06, aligned_edge=LEFT)
        vel_tag = Text("v = 1.8 km/s", font="sans-serif", font_size=10, color=PALETTE["amber"]).next_to(launch_tag_path.get_end(), DOWN, buff=0.06, aligned_edge=LEFT)
        callout_1 = VGroup(launch_tag_path, launch_tag, vel_tag)

        self.play(
            Create(earth_surface, run_time=1.0),
            Create(atmo_boundary, run_time=1.2),
            Write(atmo_tag, run_time=0.8),
            FadeIn(rocket, run_time=0.8),
            Create(trajectory, run_time=1.2),
            Write(callout_1, run_time=0.8),
        )

        # Rocket curves along the ascent path
        self.play(
            MoveAlongPath(rocket, trajectory, rate_func=rate_functions.ease_in_out_sine, run_time=1.2),
            rocket.animate(run_time=1.2).rotate(-0.45),
            FadeOut(callout_1, run_time=0.4),
        )
        self.wait(2.20)

        # ---------------------------------------------------------
        # BEAT 2: MECO & Stage Separation (Duration: 3.50s)
        # Motion: 1.30s | Hold: 2.20s
        # ---------------------------------------------------------
        booster = rocket.stage1
        upper_stage = rocket.stage2

        sep_marker = Circle(radius=0.18, arc_center=staging_pt, color=PALETTE["coral"], stroke_width=2.0)
        stage_label = Text("MECO // STAGE SEPARATION", font="sans-serif", font_size=11, color=PALETTE["coral"]).next_to(staging_pt, DOWN + RIGHT * 0.4, buff=0.15)
        v_orbital = Text("ORBITAL VELOCITY: 7.8 km/s", font="sans-serif", font_size=11, color=PALETTE["amber"]).next_to(stage_label, DOWN, buff=0.08, aligned_edge=LEFT)

        upper_stage_path = Line(staging_pt, orbit_pt, color=PALETTE["stroke_light"], stroke_width=1.4)

        self.play(
            FadeOut(rocket.plume, run_time=0.2),
            Create(sep_marker, run_time=0.5),
            Write(stage_label, run_time=0.7),
            Write(v_orbital, run_time=0.8),
            # Booster drops away and dims
            booster.animate(rate_func=rate_functions.ease_out_quad, run_time=1.3).shift(DOWN * 1.4 + LEFT * 0.8).rotate(0.6).set_opacity(0.35),
            # Upper stage continues to orbit
            upper_stage.animate(rate_func=rate_functions.ease_out_quad, run_time=1.3).move_to(orbit_pt).rotate(-0.25),
            Create(upper_stage_path, run_time=1.2),
        )
        self.wait(2.20)

        # ---------------------------------------------------------
        # BEAT 3: Fairing Jettison & Satellite Deploys (Duration: 4.00s)
        # Motion: 1.40s | Hold: 2.60s
        # ---------------------------------------------------------
        sat_body = Circle(radius=0.12, color=PALETTE["indigo"], fill_color=PALETTE["indigo"], fill_opacity=0.3, stroke_width=2.0).move_to(orbit_pt)
        solar_l = Rectangle(width=0.32, height=0.14, color=PALETTE["blue"], fill_color=PALETTE["blue"], fill_opacity=0.4, stroke_width=1.5).next_to(sat_body, LEFT, buff=0.04)
        solar_r = Rectangle(width=0.32, height=0.14, color=PALETTE["blue"], fill_color=PALETTE["blue"], fill_opacity=0.4, stroke_width=1.5).next_to(sat_body, RIGHT, buff=0.04)
        satellite = VGroup(solar_l, sat_body, solar_r).rotate(0.35)

        sat_callout_path = VMobject(color=PALETTE["stroke_light"], stroke_width=1.4)
        sat_callout_path.set_points_as_corners([
            orbit_pt + RIGHT * 0.3,
            orbit_pt + RIGHT * 0.8 + UP * 0.5,
            orbit_pt + RIGHT * 1.6 + UP * 0.5
        ])
        sat_tag = Text("PAYLOAD DEPLOYED", font="sans-serif", font_size=12, color=PALETTE["text"]).next_to(sat_callout_path.get_end(), UP, buff=0.06, aligned_edge=LEFT)
        orbit_tag = Text("LEO // ALTITUDE: 450 km", font="sans-serif", font_size=10, color=PALETTE["mint"]).next_to(sat_callout_path.get_end(), DOWN, buff=0.06, aligned_edge=LEFT)
        sat_callout = VGroup(sat_callout_path, sat_tag, orbit_tag)

        beacon_waves = VGroup(*[
            Circle(radius=0.1, arc_center=orbit_pt, color=PALETTE["indigo"], stroke_width=1.8)
            for _ in range(3)
        ])

        self.play(
            FadeOut(stage_label, v_orbital, sep_marker, rocket.stage2_body, run_time=0.4),
            # Fairing halves jettison away
            rocket.fairing_l.animate(run_time=0.8).shift(UP * 0.6 + LEFT * 0.3).set_opacity(0),
            rocket.fairing_r.animate(run_time=0.8).shift(DOWN * 0.4 + RIGHT * 0.4).set_opacity(0),
            # Satellite reveals and deploys solar panels
            FadeIn(sat_body, scale=0.5, run_time=0.6),
            GrowFromCenter(solar_l, run_time=0.8),
            GrowFromCenter(solar_r, run_time=0.8),
            Create(orbit_arc, run_time=1.2),
            Write(sat_callout, run_time=0.8),
        )

        # Pulse radio beacon down to Earth
        self.play(
            LaggedStart(
                *[
                    w.animate(rate_func=rate_functions.ease_out_quad).scale(18.0).set_stroke(opacity=0)
                    for w in beacon_waves
                ],
                lag_ratio=0.3,
                run_time=1.4
            )
        )
        self.wait(2.60)
