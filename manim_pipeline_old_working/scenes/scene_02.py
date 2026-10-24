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


class Scene02(InfographicScene):
    target_duration = 37.14

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

        # Primary projectile mass disc entering from the left runway track
        self.projectile = RigidDisc(
            radius=0.75,
            core_color=PALETTE["indigo"],
            is_hollow=False,
        ).move_to([-5.2, -0.25, 0])
        self.add(self.projectile)

        # =========================================================
        # BEAT 1: Linear Momentum & Resistance to Stopping
        # =========================================================

        # Sub-beat 1.1: Threshold barriers appear; projectile blasts through
        self.threshold_lines = VGroup(*[
            DashedLine(
                start=[-3.2 + i * 1.1, -1.0, 0],
                end=[-3.2 + i * 1.1, 0.9, 0],
                color=PALETTE["stroke"],
                stroke_width=2.0,
                dash_length=0.15,
            )
            for i in range(3)
        ])

        def sub_beat_1_1():
            self.play(
                Create(self.threshold_lines),
                self.projectile.animate.shift(RIGHT * 3.5),
                run_time=2.98,
                rate_func=rate_functions.linear,
            )

        self.beat(
            2.98,
            0.74,
            sub_beat_1_1,
            "Dashed runway barriers appear as speeding disc blasts through without decelerating",
        )

        # Sub-beat 1.2: Rigid momentum streamers trail behind moving body
        self.streamers = VGroup(*[
            Line(
                start=[-2.45 - i * 0.2, -0.25 + (i - 1) * 0.3, 0],
                end=[-4.15 - i * 0.2, -0.25 + (i - 1) * 0.3, 0],
                stroke_color=PALETTE["indigo"],
                stroke_width=2.5,
                stroke_opacity=0.75,
            )
            for i in range(3)
        ])

        def sub_beat_1_2():
            self.play(
                FadeOut(self.threshold_lines),
                Create(self.streamers),
                run_time=0.96,
            )

        self.beat(
            0.96,
            0.35,
            sub_beat_1_2,
            "Deploy parallel kinetic streamers trailing behind projectile mass",
        )

        # =========================================================
        # BEAT 2: Momentum Definition (p = m · v)
        # =========================================================

        # Sub-beat 2.1: Unboxed typography 'p =' anchors above traveling mass
        self.p_eq = Text(
            "p =",
            font_size=32,
            color=PALETTE["text"],
            weight=BOLD,
        ).move_to([-2.3, 1.35, 0])

        def sub_beat_2_1():
            self.play(
                FadeOut(self.streamers),
                FadeIn(self.p_eq, shift=DOWN * 0.2),
                run_time=1.00,
            )

        self.beat(
            1.00,
            0.35,
            sub_beat_2_1,
            "Anchor momentum equation label 'p =' directly above traveling mass",
        )

        # Sub-beat 2.2: Terms 'm' and 'v' glide horizontally into place
        m_term = Text("m", font_size=32, color=PALETTE["indigo"], weight=BOLD)
        dot_term = Text("·", font_size=32, color=PALETTE["text"], weight=BOLD)
        v_term = Text("v", font_size=32, color=PALETTE["blue"], weight=BOLD)
        self.terms_group = VGroup(m_term, dot_term, v_term).arrange(RIGHT, buff=0.15)
        self.terms_group.next_to(self.p_eq, RIGHT, buff=0.2).shift(RIGHT * 0.8)

        def sub_beat_2_2():
            self.play(
                self.terms_group.animate.shift(LEFT * 0.8),
                FadeIn(self.terms_group),
                run_time=1.78,
            )

        self.beat(
            1.78,
            0.60,
            sub_beat_2_2,
            "Glide mass and velocity terms horizontally into place with multiplication dot",
        )

        # =========================================================
        # BEAT 3: Dynamic Tracking & Directional Influence Corridor
        # =========================================================

        # Sub-beat 3.1: Relative tracking pan shifts background runway hashmarks
        def sub_beat_3_1():
            self.play(
                FadeOut(self.p_eq),
                FadeOut(self.terms_group),
                self.ticks.animate.shift(LEFT * 2.5),
                self.projectile.animate.shift(RIGHT * 0.5),
                run_time=1.95,
            )

        self.beat(
            1.95,
            0.65,
            sub_beat_3_1,
            "Track projectile translation laterally as runway hashmarks slide across stage",
        )

        # Sub-beat 3.2: Translucent directional corridor projects forward
        self.influence_corridor = Polygon(
            [-0.45, 0.45, 0],
            [5.5, 0.45, 0],
            [5.5, -0.95, 0],
            [-0.45, -0.95, 0],
            fill_color=PALETTE["mint"],
            fill_opacity=0.18,
            stroke_color=PALETTE["mint"],
            stroke_width=1.5,
            stroke_opacity=0.55,
        )

        def sub_beat_3_2():
            self.play(
                Create(self.influence_corridor),
                run_time=3.28,
            )

        self.beat(
            3.28,
            0.82,
            sub_beat_3_2,
            "Project mint directional influence corridor across forward baseline track",
        )

        # =========================================================
        # BEAT 4: Target Manifestation & Trajectory Ray Lock
        # =========================================================

        # Sub-beat 4.1: Hollow target disc manifests at rest downstream
        self.target_mass = RigidDisc(
            radius=0.75,
            core_color=PALETTE["surface_card"],
            is_hollow=True,
        ).move_to([2.5, -0.25, 0])

        def sub_beat_4_1():
            self.play(
                FadeOut(self.influence_corridor),
                FadeIn(self.target_mass, scale=0.85),
                run_time=3.40,
            )

        self.beat(
            3.40,
            0.85,
            sub_beat_4_1,
            "Stationary target disc manifests at rest downstream on runway baseline",
        )

        # Sub-beat 4.2: Dashed trajectory vector locks into target center
        line_part = DashedLine(
            start=[-0.45, -0.25, 0],
            end=[2.5, -0.25, 0],
            dash_length=0.15,
            color=PALETTE["coral"],
            stroke_width=3.5,
        )
        tip_part = ArrowTriangleFilledTip(color=PALETTE["coral"]).move_to([2.5, -0.25, 0])
        self.trajectory_ray = VGroup(line_part, tip_part)

        def sub_beat_4_2():
            self.play(
                Create(self.trajectory_ray),
                run_time=1.50,
            )

        self.beat(
            1.50,
            0.50,
            sub_beat_4_2,
            "Straight dashed trajectory arrow locks from projectile into center of target",
        )

        # =========================================================
        # BEAT 5: Closing Distance & Directional Energy Reservoir
        # =========================================================

        # Sub-beat 5.1: Dynamic DimensionRuler Δx rapidly compresses
        self.inter_ruler = DimensionRuler(
            start_point=[-0.45, -1.6, 0],
            end_point=[1.75, -1.6, 0],
            label="Δx",
            color=PALETTE["stroke"],
        )
        compressed_ruler = DimensionRuler(
            start_point=[0.6, -1.6, 0],
            end_point=[1.75, -1.6, 0],
            label="Δx",
            color=PALETTE["stroke"],
        )

        def sub_beat_5_1():
            self.play(
                FadeOut(self.trajectory_ray),
                Create(self.inter_ruler),
                run_time=0.82,
            )
            self.play(
                self.projectile.animate.shift(RIGHT * 1.8),
                Transform(self.inter_ruler, compressed_ruler),
                run_time=1.60,
                rate_func=rate_functions.ease_in_quad,
            )

        self.beat(
            2.42,
            0.81,
            sub_beat_5_1,
            "Inter-body DimensionRuler Δx rapidly compresses as projectile hurtles forward",
        )

        # Sub-beat 5.2: Radial energy reservoir gauge wraps projectile disc
        self.energy_radial_gauge = Annulus(
            inner_radius=0.80,
            outer_radius=0.96,
            color=PALETTE["amber"],
            stroke_width=1.5,
            stroke_color=PALETTE["amber"],
            fill_opacity=0.6,
        ).move_to(self.projectile.get_center())

        def sub_beat_5_2():
            self.play(
                FadeOut(self.inter_ruler),
                Create(self.energy_radial_gauge),
                run_time=3.28,
            )

        self.beat(
            3.28,
            0.82,
            sub_beat_5_2,
            "Deploy glowing radial energy gauge around projectile carrying kinetic reservoir",
        )

        # =========================================================
        # BEAT 6: Impending Contact & Conservation Law
        # =========================================================

        # Sub-beat 6.1: Precision tangent contact reticle snaps into place
        reticle_v = Line([1.75, 0.65, 0], [1.75, -1.15, 0], color=PALETTE["coral"], stroke_width=1.5)
        reticle_h = Line([1.55, -0.25, 0], [1.95, -0.25, 0], color=PALETTE["coral"], stroke_width=1.5)
        reticle_c = Circle(radius=0.2, color=PALETTE["coral"], stroke_width=1.5).move_to([1.75, -0.25, 0])
        self.reticle = VGroup(reticle_v, reticle_h, reticle_c)

        def sub_beat_6_1():
            self.play(
                self.projectile.animate.shift(RIGHT * 0.4),
                self.energy_radial_gauge.animate.shift(RIGHT * 0.4),
                run_time=2.13,
            )
            self.play(
                Create(self.reticle),
                run_time=2.20,
            )

        self.beat(
            4.33,
            1.08,
            sub_beat_6_1,
            "Projectile reaches contact position; hairline reticle snaps onto tangent seam",
        )

        # Sub-beat 6.2: Editorial header 'Σp_initial = Σp_final' draws in Zone 2
        self.conservation_eq = Text(
            "Σp_initial = Σp_final",
            font_size=30,
            color=PALETTE["indigo"],
            weight=BOLD,
        ).move_to([1.75, 1.4, 0])

        def sub_beat_6_2():
            self.play(
                FadeIn(self.conservation_eq, shift=DOWN * 0.2),
                run_time=2.02,
            )

        self.beat(
            2.02,
            0.67,
            sub_beat_6_2,
            "Draw momentum conservation header 'Σp_initial = Σp_final' above contact boundary",
        )

        # ---------------------------------------------------------
        # FINAL RUNTIME VALIDATION
        # ---------------------------------------------------------
        self.finalize()
