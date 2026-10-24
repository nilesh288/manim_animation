from manim import *
import numpy as np
from engine_2d import (
    PALETTE,
    FONTS,
    InfographicScene,
    RigidDisc,
    VisualCard,
    LeaderCallout,
    DimensionRuler,
    SurfaceGround,
    TelemetryGroup,
    MetricGauge,
)


class Scene03(InfographicScene):
    target_duration = 35.96

    def construct(self):
        # ---------------------------------------------------------
        # ENVIRONMENT SETUP
        # ---------------------------------------------------------
        self.runway = SurfaceGround(ground_y=-1.0)
        self.ticks = VGroup(*[
            Line(
                start=[x, -1.0, 0],
                end=[x, -1.18, 0],
                stroke_color=PALETTE["stroke_light"],
                stroke_width=1.5,
            )
            for x in np.arange(-7.0, 7.5, 1.0)
        ])
        self.add(self.runway, self.ticks)

        # Pre-positioned mass bodies at impending contact seam (x = 0.0)
        self.projectile = RigidDisc(
            radius=0.75,
            core_color=PALETTE["indigo"],
            is_hollow=False,
        ).move_to([-0.75, -0.25, 0])

        self.target = RigidDisc(
            radius=0.75,
            core_color=PALETTE["surface_card"],
            is_hollow=True,
        ).move_to([0.75, -0.25, 0])

        self.add(self.projectile, self.target)

        # =========================================================
        # BEAT 1: Millisecond of Impact & Impulse Law
        # =========================================================

        # Sub-beat 1.1: Visual tempo slows; vertical dilation lines radiate from seam
        self.dilation_lines = VGroup(*[
            Line(
                start=[dx, -1.0, 0],
                end=[dx * 1.35, 1.8, 0],
                stroke_color=PALETTE["stroke"],
                stroke_width=1.2,
                stroke_opacity=0.45,
            )
            for dx in np.linspace(-1.2, 1.2, 7)
        ])

        def sub_beat_1_1():
            self.play(
                Create(self.dilation_lines),
                run_time=1.18,
            )

        self.beat(
            1.18,
            0.40,
            sub_beat_1_1,
            "Visual tempo slows with subtle time-dilation lines radiating from meeting point",
        )

        # Sub-beat 1.2: Impulse formula J = ∫ F dt emerges with energy flux lines
        self.impulse_label = Text(
            "J = ∫ F dt",
            font_size=30,
            color=PALETTE["coral"],
            weight=BOLD,
        ).move_to([0, 1.45, 0])

        self.flux_lines = VGroup(*[
            Line(
                start=[-0.45, -0.25 + dy, 0],
                end=[0.45, -0.25 + dy, 0],
                stroke_color=PALETTE["coral"],
                stroke_width=2.5,
            )
            for dy in [-0.3, 0.0, 0.3]
        ])

        def sub_beat_1_2():
            self.play(
                FadeOut(self.dilation_lines),
                FadeIn(self.impulse_label, shift=DOWN * 0.2),
                Create(self.flux_lines),
                run_time=2.44,
            )

        self.beat(
            2.44,
            0.82,
            sub_beat_1_2,
            "Deploy impulse callout J = ∫ F dt with directional energy flux lines",
        )

        # =========================================================
        # BEAT 2: Elastic Boundary & Conservation Meters
        # =========================================================

        # Sub-beat 2.1: Spring-like geometric rings envelop contact interfaces
        ring_left = Arc(
            radius=0.75,
            start_angle=-PI / 3,
            angle=2 * PI / 3,
            arc_center=[-0.75, -0.25, 0],
            color=PALETTE["mint"],
            stroke_width=3.5,
        )
        ring_right = Arc(
            radius=0.75,
            start_angle=2 * PI / 3,
            angle=2 * PI / 3,
            arc_center=[0.75, -0.25, 0],
            color=PALETTE["mint"],
            stroke_width=3.5,
        )
        self.elastic_rings = VGroup(ring_left, ring_right)

        def sub_beat_2_1():
            self.play(
                FadeOut(self.flux_lines),
                Create(self.elastic_rings),
                run_time=1.73,
            )

        self.beat(
            1.73,
            0.58,
            sub_beat_2_1,
            "Spring-like geometric rings envelop interfaces of elastic collision",
        )

        # Sub-beat 2.2: Telemetry meters (E_k and P) lock at 100% in Zone 1
        gauge_ek = MetricGauge(
            label="E_k",
            value_text="100%",
            bar_color=PALETTE["mint"],
            bar_width=2.0,
        )
        gauge_p = MetricGauge(
            label="P",
            value_text="100%",
            bar_color=PALETTE["indigo"],
            bar_width=2.0,
        )
        self.telemetry = TelemetryGroup(gauge_ek, gauge_p, direction=RIGHT, buff=0.9).move_to([0, 2.65, 0])

        def sub_beat_2_2():
            self.play(
                FadeOut(self.impulse_label),
                FadeIn(self.telemetry, shift=DOWN * 0.3),
                run_time=3.79,
            )

        self.beat(
            3.79,
            0.95,
            sub_beat_2_2,
            "Twin horizontal telemetry meters lock kinetic energy and momentum at 100%",
        )

        # =========================================================
        # BEAT 3: Dynamic Deceleration, Reaction Forces, & Stress Wave
        # =========================================================

        # Sub-beat 3.1: Projectile forward vector violently contracts into rearward braking arrow
        self.brake_arrow = Arrow(
            start=[-0.75, -0.25, 0],
            end=[-2.35, -0.25, 0],
            color=PALETTE["coral"],
            buff=0,
            stroke_width=5.5,
        )

        def sub_beat_3_1():
            self.play(
                FadeOut(self.elastic_rings),
                GrowArrow(self.brake_arrow),
                run_time=3.19,
            )

        self.beat(
            3.19,
            0.80,
            sub_beat_3_1,
            "Forward vector violently contracts into rearward braking arrow on projectile",
        )

        # Sub-beat 3.2: Opposing action-reaction vectors (-F and +F) erupt from contact seam
        f_action = Arrow(
            start=[0, 0.65, 0],
            end=[1.55, 0.65, 0],
            color=PALETTE["blue"],
            buff=0,
            stroke_width=4.5,
        )
        f_action_label = Text("+F", font_size=22, color=PALETTE["blue"], weight=BOLD).next_to(
            f_action, UP, buff=0.15
        )
        f_reaction = Arrow(
            start=[0, 0.65, 0],
            end=[-1.55, 0.65, 0],
            color=PALETTE["coral"],
            buff=0,
            stroke_width=4.5,
        )
        f_reaction_label = Text("-F", font_size=22, color=PALETTE["coral"], weight=BOLD).next_to(
            f_reaction, UP, buff=0.15
        )
        self.force_pair = VGroup(f_action, f_action_label, f_reaction, f_reaction_label)

        def sub_beat_3_2():
            self.play(
                FadeOut(self.brake_arrow),
                Create(self.force_pair),
                run_time=2.42,
            )

        self.beat(
            2.42,
            0.80,
            sub_beat_3_2,
            "Opposing vector arrows erupt outward in Newton-third equilibrium",
        )

        # Sub-beat 3.3: Compressive stress wave punches horizontally through target disc
        stress_wave_1 = Arc(
            radius=0.35,
            start_angle=-PI / 2,
            angle=PI,
            arc_center=[0.1, -0.25, 0],
            color=PALETTE["mint"],
            stroke_width=3.5,
        )
        stress_wave_2 = Arc(
            radius=0.6,
            start_angle=-PI / 2,
            angle=PI,
            arc_center=[0.45, -0.25, 0],
            color=PALETTE["mint"],
            stroke_width=3.0,
        )
        self.stress_waves = VGroup(stress_wave_1, stress_wave_2)

        def sub_beat_3_3():
            self.play(
                FadeOut(self.force_pair),
                Create(self.stress_waves),
                run_time=3.13,
            )

        self.beat(
            3.13,
            0.78,
            sub_beat_3_3,
            "Compressive kinetic stress wave punches through diameter of stationary target",
        )

        # =========================================================
        # BEAT 4: Velocity Vector Transfer
        # =========================================================

        # Sub-beat 4.1: Razor-thin vertical flash illuminates tangent seam
        self.seam_flash = Line(
            start=[0, -1.0, 0],
            end=[0, 0.5, 0],
            stroke_color=PALETTE["mint"],
            stroke_width=4.0,
        )

        def sub_beat_4_1():
            self.play(
                FadeOut(self.stress_waves),
                Create(self.seam_flash),
                run_time=1.15,
            )

        self.beat(
            1.15,
            0.38,
            sub_beat_4_1,
            "Razor-thin vertical flash illuminates tangent seam between bodies",
        )

        # Sub-beat 4.2: Velocity vector slides seamlessly from projectile to target body
        v_initial = Arrow(
            start=[-0.75, -0.25, 0],
            end=[0.75, -0.25, 0],
            color=PALETTE["blue"],
            buff=0,
            stroke_width=4.5,
        )
        self.target_v_arrow = Arrow(
            start=[0.75, -0.25, 0],
            end=[2.25, -0.25, 0],
            color=PALETTE["blue"],
            buff=0,
            stroke_width=4.5,
        )

        def sub_beat_4_2():
            self.play(
                FadeOut(self.seam_flash),
                GrowArrow(v_initial),
                run_time=0.64,
            )
            self.play(
                ReplacementTransform(v_initial, self.target_v_arrow),
                run_time=1.00,
            )

        self.beat(
            1.64,
            0.55,
            sub_beat_4_2,
            "Velocity vector slides seamlessly across seam and anchors into target body",
        )

        # =========================================================
        # BEAT 5: Decoupled Departure & Momentum Propagation
        # =========================================================

        # Sub-beat 5.1: Projectile freezes in place; neutralizes kinetic contour
        def sub_beat_5_1():
            self.play(
                self.projectile.animate.set_opacity(0.65),
                run_time=1.90,
            )

        self.beat(
            1.90,
            0.63,
            sub_beat_5_1,
            "Original body halts abruptly and settles into neutral stationary contour",
        )

        # Sub-beat 5.2: Target mass launches forward along runway
        def sub_beat_5_2():
            self.play(
                self.target.animate.shift(RIGHT * 3.2),
                self.target_v_arrow.animate.shift(RIGHT * 3.2),
                run_time=2.53,
                rate_func=rate_functions.ease_in_quad,
            )

        self.beat(
            2.53,
            0.84,
            sub_beat_5_2,
            "Target mass accelerates down runway inheriting forward momentum",
        )

        # Sub-beat 5.3: Bold momentum vector tracks under target mass into distance
        self.p_track = Arrow(
            start=[2.4, -1.5, 0],
            end=[5.0, -1.5, 0],
            color=PALETTE["indigo"],
            buff=0,
            stroke_width=6.5,
        )
        self.p_track_label = Text(
            "p = m · v",
            font_size=20,
            color=PALETTE["indigo"],
            weight=BOLD,
        ).next_to(self.p_track, DOWN, buff=0.15)

        def sub_beat_5_3():
            self.play(
                FadeOut(self.target_v_arrow),
                GrowArrow(self.p_track),
                FadeIn(self.p_track_label),
                self.target.animate.shift(RIGHT * 1.5),
                run_time=2.50,
            )

        self.beat(
            2.50,
            0.83,
            sub_beat_5_3,
            "Bold momentum vector tracks under target mass as it recedes into distance",
        )

        # ---------------------------------------------------------
        # FINAL RUNTIME VALIDATION
        # ---------------------------------------------------------
        self.finalize()
