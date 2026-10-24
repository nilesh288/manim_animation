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


class Scene01(InfographicScene):
    target_duration = 48.50

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

        # =========================================================
        # BEAT 1: Kinematic Genesis & Universal Motion
        # =========================================================

        # Sub-beat 1.1: Draw horizontal runway & isometric ticks
        def sub_beat_1_1():
            self.play(
                Create(self.runway),
                Create(self.ticks),
                run_time=2.02,
            )

        self.beat(
            2.02,
            0.67,
            sub_beat_1_1,
            "Establish horizontal bedrock runway with calibrated metric subdivisions",
        )

        # Sub-beat 1.2: Elliptical orbit morphs into linked atomic pair
        orbit = Ellipse(
            width=5.2,
            height=2.2,
            color=PALETTE["indigo"],
            stroke_width=2.5,
        ).move_to([0, 1.6, 0])

        atom_a = Dot(point=[-0.9, 1.6, 0], radius=0.12, color=PALETTE["indigo"])
        atom_b = Dot(point=[0.9, 1.6, 0], radius=0.12, color=PALETTE["indigo"])
        bond_line = DashedLine(
            start=[-0.9, 1.6, 0],
            end=[0.9, 1.6, 0],
            dash_length=0.1,
            dashed_ratio=0.5,
            color=PALETTE["mint"],
            stroke_width=2.5,
        )
        self.bond_pair = VGroup(atom_a, atom_b, bond_line)

        def sub_beat_1_2():
            self.play(Create(orbit), run_time=1.83)
            self.play(ReplacementTransform(orbit, self.bond_pair), run_time=1.83)

        self.beat(
            3.66,
            0.92,
            sub_beat_1_2,
            "Macro elliptical orbit sweeps and collapses into atomic pair",
        )

        # Sub-beat 1.3: Editorial 'MOTION' text snaps above baseline arrow
        self.motion_label = Text(
            "MOTION",
            font_size=40,
            color=PALETTE["text"],
            weight=BOLD,
        ).move_to([0, 1.5, 0])

        self.motion_arrow = Arrow(
            start=[-2.8, 0.8, 0],
            end=[2.8, 0.8, 0],
            color=PALETTE["coral"],
            buff=0,
            stroke_width=4.5,
            max_tip_length_to_length_ratio=0.15,
        )

        def sub_beat_1_3():
            self.play(
                FadeOut(self.bond_pair),
                FadeIn(self.motion_label, shift=DOWN * 0.2),
                GrowArrow(self.motion_arrow),
                run_time=2.86,
            )

        self.beat(
            2.86,
            0.71,
            sub_beat_1_3,
            "Snap editorial 'MOTION' typography and directional baseline vector",
        )

        # =========================================================
        # BEAT 2: Classical Mechanics & Resting Mass
        # =========================================================

        # Sub-beat 2.1: Orthographic camera profile & illuminate zero-friction hashmarks
        def sub_beat_2_1():
            self.play(
                FadeOut(self.motion_label),
                FadeOut(self.motion_arrow),
                self.ticks.animate.set_stroke(color=PALETTE["stroke"], width=2.0),
                run_time=1.24,
            )

        self.beat(
            1.24,
            0.42,
            sub_beat_2_1,
            "Transition to orthographic frictionless baseline profile",
        )

        # Sub-beat 2.2: Rigid disc drops onto frictionless runway
        self.mass = RigidDisc(radius=0.75, core_color=PALETTE["indigo"], is_hollow=False)
        self.mass.move_to([-2.5, 2.5, 0])

        def sub_beat_2_2():
            self.play(
                self.mass.animate.move_to([-2.5, -0.25, 0]),
                run_time=2.07,
                rate_func=rate_functions.ease_in_quad,
            )

        self.beat(
            2.07,
            0.69,
            sub_beat_2_2,
            "Rigid disc drops onto frictionless runway settling at origin",
        )

        # Sub-beat 2.3: Hairline ring pulses and pins origin x = 0
        self.pulse_ring = Circle(
            radius=0.9,
            color=PALETTE["stroke"],
            stroke_width=1.5,
        ).move_to([-2.5, -0.25, 0])

        self.origin_mark = Dot(point=[-2.5, -1.0, 0], radius=0.06, color=PALETTE["stroke"])
        self.origin_tag = Text("x = 0", font_size=20, color=PALETTE["text_dim"]).next_to(
            self.origin_mark, DOWN, buff=0.15
        )

        def sub_beat_2_3():
            self.play(
                Create(self.pulse_ring),
                FadeIn(self.origin_mark),
                FadeIn(self.origin_tag),
                run_time=1.01,
            )

        self.beat(
            1.01,
            0.35,
            sub_beat_2_3,
            "Hairline ring pulses and anchors origin coordinate x = 0",
        )

        # =========================================================
        # BEAT 3: Velocity and Momentum Readouts
        # =========================================================

        # Sub-beat 3.1: Leader callout locks velocity v = 0.0 m/s
        self.v_callout = LeaderCallout(
            target_point=[-2.5, 0.5, 0],
            title="v = 0.0 m/s",
            direction=UP + RIGHT,
        )

        def sub_beat_3_1():
            self.play(
                FadeOut(self.pulse_ring),
                Create(self.v_callout),
                run_time=1.20,
            )

        self.beat(
            1.20,
            0.40,
            sub_beat_3_1,
            "Leader callout locks velocity telemetry v = 0.0 m/s",
        )

        # Sub-beat 3.2: Deploy dormant momentum metric p = 0 and dashed box
        self.p_metric = Text("p = 0", font_size=24, color=PALETTE["indigo"], weight=BOLD).next_to(
            self.v_callout, DOWN, buff=0.25, aligned_edge=LEFT
        )
        self.p_dashed_box = DashedVMobject(
            Rectangle(width=0.8, height=0.35, color=PALETTE["indigo"], stroke_width=1.5),
            num_dashes=12,
        ).next_to(self.p_metric, RIGHT, buff=0.15)

        def sub_beat_3_2():
            self.play(
                FadeIn(self.p_metric),
                Create(self.p_dashed_box),
                run_time=1.92,
            )

        self.beat(
            1.92,
            0.64,
            sub_beat_3_2,
            "Deploy dormant momentum metric p = 0 and dashed vector indicator",
        )

        # =========================================================
        # BEAT 4: External Unbalanced Force Impact
        # =========================================================

        # Sub-beat 4.1: Bold force arrow strikes rear perimeter of mass
        self.force_arrow = Arrow(
            start=[-5.4, -0.25, 0],
            end=[-3.25, -0.25, 0],
            color=PALETTE["coral"],
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.2,
        )
        self.contact_highlight = Dot(
            point=[-3.25, -0.25, 0],
            radius=0.14,
            color=PALETTE["coral"],
        )

        def sub_beat_4_1():
            self.play(
                FadeOut(self.v_callout),
                FadeOut(self.p_metric),
                FadeOut(self.p_dashed_box),
                GrowArrow(self.force_arrow),
                FadeIn(self.contact_highlight, scale=1.5),
                run_time=3.48,
            )

        self.beat(
            3.48,
            0.87,
            sub_beat_4_1,
            "External force vector strikes rear perimeter of mass disc",
        )

        # Sub-beat 4.2: Mint streaks backward as mass shifts right
        self.motion_streaks = VGroup(*[
            Line(
                start=[-3.2 - i * 0.4, -0.6 - i * 0.15, 0],
                end=[-4.8 - i * 0.4, -0.6 - i * 0.15, 0],
                stroke_color=PALETTE["mint"],
                stroke_width=2.5 - i * 0.5,
                stroke_opacity=0.8 - i * 0.2,
            )
            for i in range(3)
        ])

        def sub_beat_4_2():
            self.play(
                FadeOut(self.contact_highlight),
                self.mass.animate.shift(RIGHT * 1.5),
                self.force_arrow.animate.shift(RIGHT * 1.5),
                Create(self.motion_streaks),
                run_time=2.18,
                rate_func=rate_functions.ease_in_quad,
            )

        self.beat(
            2.18,
            0.73,
            sub_beat_4_2,
            "Displacement begins with mint motion streaks trailing baseline",
        )

        # =========================================================
        # BEAT 5: Newton's Second Law & Acceleration
        # =========================================================

        # Sub-beat 5.1: Lock dynamic force tracking labeled F = m · a
        self.f_label = Text("F = m · a", font_size=28, color=PALETTE["coral"], weight=BOLD).move_to(
            [-1.625, 0.65, 0]
        )

        def sub_beat_5_1():
            self.play(
                FadeOut(self.motion_streaks),
                self.mass.animate.shift(RIGHT * 1.2),
                self.force_arrow.animate.shift(RIGHT * 1.2),
                FadeIn(self.f_label),
                run_time=3.29,
            )

        self.beat(
            3.29,
            0.82,
            sub_beat_5_1,
            "Lock dynamic force tracking vector labeled with Newton's second law",
        )

        # Sub-beat 5.2: Double-chevron acceleration indicator deploys
        self.chevrons = Text("»", font_size=42, color=PALETTE["amber"]).move_to([2.3, -0.25, 0])

        def sub_beat_5_2():
            self.play(
                self.mass.animate.shift(RIGHT * 0.8),
                self.force_arrow.animate.shift(RIGHT * 0.8),
                self.f_label.animate.shift(RIGHT * 0.8),
                FadeIn(self.chevrons, shift=RIGHT * 0.4),
                run_time=2.16,
                rate_func=rate_functions.ease_in_quad,
            )

        self.beat(
            2.16,
            0.72,
            sub_beat_5_2,
            "Deploy acceleration chevron accents indicating speed increase",
        )

        # =========================================================
        # BEAT 6: Mechanical Work & Energy Accumulation
        # =========================================================

        # Sub-beat 6.1: Horizontal DimensionRuler Δx expands along runway
        self.dx_ruler = DimensionRuler(
            start_point=[-2.5, -1.6, 0],
            end_point=[1.0, -1.6, 0],
            label="Δx",
            color=PALETTE["stroke"],
        )

        def sub_beat_6_1():
            self.play(
                FadeOut(self.chevrons),
                Create(self.dx_ruler),
                run_time=1.77,
            )

        self.beat(
            1.77,
            0.59,
            sub_beat_6_1,
            "Expand displacement DimensionRuler Δx between origin and mass",
        )

        # Sub-beat 6.2: Work integral band and unboxed formula W = ∫ F dx
        self.work_band = Polygon(
            [-2.5, -1.0, 0],
            [1.0, -1.0, 0],
            [1.0, -0.25, 0],
            [-2.5, -0.25, 0],
            fill_color=PALETTE["blue"],
            fill_opacity=0.22,
            stroke_width=0,
        )
        self.work_label = Text("W = ∫ F dx", font_size=28, color=PALETTE["blue"], weight=BOLD).move_to(
            [-0.825, 1.4, 0]
        )

        def sub_beat_6_2():
            self.play(
                FadeOut(self.f_label),
                FadeIn(self.work_label),
                FadeIn(self.work_band),
                run_time=1.31,
            )

        self.beat(
            1.31,
            0.44,
            sub_beat_6_2,
            "Sweep mechanical work integral ribbon W = ∫ F dx",
        )

        # Sub-beat 6.3: Kinetic energy halo blooms inside moving mass
        self.halo = Annulus(
            inner_radius=0.18,
            outer_radius=0.68,
            color=PALETTE["mint"],
            fill_opacity=0.35,
            stroke_color=PALETTE["mint"],
            stroke_width=2.0,
        ).move_to(self.mass.get_center())

        def sub_beat_6_3():
            self.play(
                FadeOut(self.work_band),
                FadeIn(self.halo, scale=0.4),
                self.halo.animate.scale(1.4),
                run_time=3.18,
            )

        self.beat(
            3.18,
            0.79,
            sub_beat_6_3,
            "Concentric kinetic energy halo blooms inside moving mass",
        )

        # =========================================================
        # BEAT 7: Sustained Force & Acquired Momentum
        # =========================================================

        # Sub-beat 7.1: Continuous push across baseline increments
        new_dx_ruler = DimensionRuler(
            start_point=[-2.5, -1.6, 0],
            end_point=[1.8, -1.6, 0],
            label="Δx",
            color=PALETTE["stroke"],
        )

        def sub_beat_7_1():
            self.play(
                self.mass.animate.shift(RIGHT * 0.8),
                self.halo.animate.shift(RIGHT * 0.8),
                self.force_arrow.animate.shift(RIGHT * 0.8),
                self.work_label.animate.shift(RIGHT * 0.8),
                Transform(self.dx_ruler, new_dx_ruler),
                run_time=1.18,
            )

        self.beat(
            1.18,
            0.39,
            sub_beat_7_1,
            "Sustained push advances mass and expands displacement ruler",
        )

        # Sub-beat 7.2: Forward velocity vector elongates with numeric readout
        self.v_arrow = Arrow(
            start=[2.55, -0.25, 0],
            end=[4.55, -0.25, 0],
            color=PALETTE["blue"],
            buff=0,
            stroke_width=5.0,
        )
        self.v_readout = Text("v = 4.8 m/s", font_size=24, color=PALETTE["blue"], weight=BOLD).next_to(
            self.v_arrow, UP, buff=0.25
        )

        def sub_beat_7_2():
            self.play(
                FadeOut(self.work_label),
                GrowArrow(self.v_arrow),
                FadeIn(self.v_readout),
                run_time=1.33,
            )

        self.beat(
            1.33,
            0.44,
            sub_beat_7_2,
            "Elongate forward velocity vector with real-time numeric readout",
        )

        # Sub-beat 7.3: Heavy momentum vector p = m · v thickens in Zone 4
        self.p_arrow = Arrow(
            start=[-0.5, -1.6, 0],
            end=[2.8, -1.6, 0],
            color=PALETTE["indigo"],
            buff=0,
            stroke_width=7.5,
        )
        self.p_readout = Text("p = m · v", font_size=22, color=PALETTE["indigo"], weight=BOLD).next_to(
            self.p_arrow, DOWN, buff=0.18
        )

        def sub_beat_7_3():
            self.play(
                FadeOut(self.dx_ruler),
                GrowArrow(self.p_arrow),
                FadeIn(self.p_readout),
                run_time=1.54,
            )

        self.beat(
            1.54,
            0.51,
            sub_beat_7_3,
            "Deploy heavy momentum vector p = m · v symbolizing acquired momentum",
        )

        # ---------------------------------------------------------
        # FINAL RUNTIME VALIDATION
        # ---------------------------------------------------------
        self.finalize()
