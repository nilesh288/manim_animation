"""
sample_scene.py - 10-Second Bright Editorial 2D Infographic Preview
Renders without external assets or card containers.
"""
from manim import *
import numpy as np

# Editorial Pastel Palette
PALETTE = {
    "bg": "#F8F9FA",           # Warm off-white
    "stroke": "#2D3748",       # Deep charcoal
    "stroke_light": "#CBD5E0", # Subtle gray
    "text": "#1A202C",         # Ink black
    "text_dim": "#718096",     # Muted slate
    "indigo": "#5A67D8",       # Satellite / primary
    "blue": "#4299E1",         # Secondary waves
    "amber": "#ED8936",        # Telemetry / ruler
    "coral": "#E53E3E",        # Focal receiver
    "mint": "#38A169",         # Success / lock
}


class InfographicDemo(Scene):
    def construct(self):
        self.camera.background_color = PALETTE["bg"]

        # ---------------------------------------------------------
        # Spatial Anchors & Geometry Setup
        # ---------------------------------------------------------
        sat_pos = RIGHT * 3.5 + UP * 2.0
        rec_pos = LEFT * 1.5 + DOWN * 0.8
        earth_anchor = DOWN * 4.4 + LEFT * 1.0

        # 1. Earth Horizon (Clean curved boundary, not a boxed card)
        earth_surface = Arc(
            radius=6.2,
            start_angle=PI * 0.22,
            angle=PI * 0.48,
            color=PALETTE["stroke_light"],
            stroke_width=2.5,
        ).move_to(earth_anchor)

        earth_fill = Sector(
            radius=6.15,
            start_angle=PI * 0.22,
            angle=PI * 0.48,
            color="#EDF2F7",
            fill_opacity=0.6,
            stroke_width=0,
        ).move_to(earth_anchor).set_z_index(-1)

        grid_arc = Arc(
            radius=5.5,
            start_angle=PI * 0.25,
            angle=PI * 0.42,
            color="#E2E8F0",
            stroke_width=1.2,
        ).move_to(earth_anchor)

        # 2. Vector Satellite (Geometric schematic, no external SVG needed)
        sat_core = Circle(
            radius=0.18,
            color=PALETTE["indigo"],
            fill_color=PALETTE["indigo"],
            fill_opacity=0.2,
            stroke_width=2.0,
        )
        panel_l = Rectangle(
            width=0.45,
            height=0.2,
            color=PALETTE["blue"],
            fill_color=PALETTE["blue"],
            fill_opacity=0.3,
            stroke_width=1.5,
        ).next_to(sat_core, LEFT, buff=0.08)
        panel_r = Rectangle(
            width=0.45,
            height=0.2,
            color=PALETTE["blue"],
            fill_color=PALETTE["blue"],
            fill_opacity=0.3,
            stroke_width=1.5,
        ).next_to(sat_core, RIGHT, buff=0.08)

        sat_glyph = (
            VGroup(panel_l, sat_core, panel_r).move_to(sat_pos).rotate(-0.4)
        )
        sat_label = Text(
            "SAT_04 // [ORBIT: 20,200 km]",
            font="sans-serif",
            font_size=13,
            color=PALETTE["text_dim"],
        ).next_to(sat_glyph, UP, buff=0.2)

        # 3. Receiver Element
        rec_dot = Dot(rec_pos, radius=0.09, color=PALETTE["coral"])
        rec_ring = Circle(
            radius=0.22,
            arc_center=rec_pos,
            color=PALETTE["coral"],
            stroke_width=1.5,
        )

        # Angled leader line callout (No card container)
        leader_start = rec_pos
        leader_mid = rec_pos + LEFT * 0.8 + UP * 0.6
        leader_end = leader_mid + LEFT * 1.0
        leader_path = VMobject(color=PALETTE["stroke_light"], stroke_width=1.5)
        leader_path.set_points_as_corners(
            [leader_start, leader_mid, leader_end]
        )

        rec_label = Text(
            "SURFACE RECEIVER",
            font="sans-serif",
            font_size=14,
            color=PALETTE["text"],
        ).next_to(leader_end, UP, buff=0.08, aligned_edge=LEFT)
        rec_coord = Text(
            "32.08° N, 74.12° E",
            font="sans-serif",
            font_size=11,
            color=PALETTE["text_dim"],
        ).next_to(leader_end, DOWN, buff=0.08, aligned_edge=LEFT)
        rec_group = VGroup(
            rec_dot, rec_ring, leader_path, rec_label, rec_coord
        )

        # ---------------------------------------------------------
        # BEAT 1: Establish Satellite in Orbit (Duration: 3.50s)
        # Motion: 1.20s | Hold: 2.30s
        # ---------------------------------------------------------
        self.play(
            FadeIn(earth_fill, run_time=1.0),
            Create(earth_surface, run_time=1.2),
            Create(grid_arc, run_time=1.2),
            FadeIn(sat_glyph, shift=DOWN * 0.3, run_time=1.0),
            Write(sat_label, run_time=0.8),
        )
        self.wait(2.30)

        # ---------------------------------------------------------
        # BEAT 2: Signal Broadcast & Target Lock (Duration: 3.00s)
        # Motion: 1.20s | Hold: 1.80s
        # ---------------------------------------------------------
        waves = VGroup(*[
            Arc(
                radius=r,
                start_angle=-2.8,
                angle=1.0,
                arc_center=sat_pos,
                color=PALETTE["indigo"],
                stroke_width=2.0,
            )
            for r in [1.2, 2.4, 3.6]
        ])

        wave_anim = LaggedStart(
            *[
                w.animate(
                    rate_func=rate_functions.ease_out_quad
                ).set_stroke(opacity=0).scale(1.8)
                for w in waves
            ],
            lag_ratio=0.3,
            run_time=1.2,
        )

        self.play(
            wave_anim,
            FadeIn(rec_group, scale=0.85, run_time=1.0),
        )
        self.wait(1.80)

        # ---------------------------------------------------------
        # BEAT 3: Distance Metric & Time Resolution (Duration: 3.50s)
        # Motion: 1.20s | Hold: 2.30s
        # ---------------------------------------------------------
        ruler = DashedLine(
            sat_pos,
            rec_pos,
            color=PALETTE["amber"],
            stroke_width=1.8,
            dash_length=0.14,
        )

        metric_badge = Text(
            "Δt = 67.4 ms  ->  d = 20,200 km",
            font="sans-serif",
            font_size=15,
            color=PALETTE["amber"],
        )
        metric_badge.next_to(ruler.get_center(), UP + LEFT * 0.4, buff=0.15)
        metric_badge.rotate(ruler.get_angle())

        pulse_burst = Circle(
            radius=0.22,
            arc_center=rec_pos,
            color=PALETTE["coral"],
            stroke_width=2.0,
        )

        self.play(
            Create(ruler, run_time=1.0),
            Write(metric_badge, run_time=0.9),
            pulse_burst.animate(run_time=1.0).scale(3.0).set_stroke(opacity=0),
        )
        self.wait(2.30)
