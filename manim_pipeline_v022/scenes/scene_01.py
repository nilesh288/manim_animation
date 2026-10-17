from manim import *
import numpy as np
from engine_2d import (
    PALETTE,
    FONTS,
    EASINGS,
    LINEAR,
    SMOOTH,
    InfographicScene,
    ParticleWake,
    Chevron,
    DropShadow,
    FocusReticle,
    VisualCard,
    MilestoneTimeline,
    RigidDisc,
    LeaderCallout,
    DimensionRuler,
    SurfaceGround,
    TelemetryGroup,
    MetricGauge,
    VectorArrow,
    DashedRectangle,
    DashedCircle,
)


class Scene01(InfographicScene):
    target_duration = 15.48

    def construct(self):
        self.camera.background_color = PALETTE["background"]

        cobalt = "#3B82F6"
        coral = "#FF6B6B"
        slate = "#2B2D42"
        mint = "#4ECDC4"

        ground_y = -2.0
        ground = SurfaceGround(ground_y=ground_y)

        rotor = RigidDisc(
            radius=0.72,
            core_color=cobalt,
            body_color=slate,
        ).move_to([-2.4, -0.72, 0])

        rotor_details = VGroup(
            Line([-2.4, -0.72, 0], [-2.4, -0.12, 0],
                 color=cobalt, stroke_width=3),
            Line([-2.4, -0.72, 0], [-1.88, -0.98, 0],
                 color=cobalt, stroke_width=3),
            Line([-2.4, -0.72, 0], [-2.92, -0.98, 0],
                 color=cobalt, stroke_width=3),
        )

        upper_pad = RoundedRectangle(
            width=1.05, height=0.30, corner_radius=0.06,
            color=slate, fill_color=slate, fill_opacity=1,
        ).move_to([-2.4, 0.02, 0])

        lower_pad = RoundedRectangle(
            width=1.05, height=0.30, corner_radius=0.06,
            color=slate, fill_color=slate, fill_opacity=1,
        ).move_to([-2.4, -1.46, 0])

        upper_arm = Line(
            [-3.15, 0.02, 0], [-2.95, 0.02, 0],
            color=slate, stroke_width=7,
        )
        lower_arm = Line(
            [-3.15, -1.46, 0], [-2.95, -1.46, 0],
            color=slate, stroke_width=7,
        )

        spin_arrow = CurvedArrow(
            start_point=[-3.15, -0.35, 0],
            end_point=[-1.65, -0.35, 0],
            angle=-TAU / 3,
            color=cobalt,
            stroke_width=4,
            tip_length=0.16,
        )

        spin_label = Text(
            "ROTATION",
            font=FONTS["mono"],
            font_size=17,
            color=cobalt,
        ).next_to(spin_arrow, UP, buff=0.08)

        contact_marks = VGroup(*[
            Line(
                [-2.98 + i * 0.20, -0.68, 0],
                [-3.08 + i * 0.20, -0.53, 0],
                color=coral,
                stroke_width=4,
            )
            for i in range(6)
        ])

        debris = VGroup(*[
            Dot(
                [-1.55 + i * 0.18, -1.25 + (i % 3) * 0.12, 0],
                radius=0.035,
                color=slate,
            )
            for i in range(7)
        ])

        momentum_arrow = VectorArrow(
            [-3.0, 0.85, 0],
            [0.0, 0.85, 0],
            color=cobalt,
            stroke_width=5,
        )

        momentum_label = Text(
            "MOMENTUM [p]",
            font=FONTS["mono"],
            font_size=19,
            color=cobalt,
        ).next_to(momentum_arrow, UP, buff=0.10)

        transfer_arrows = VGroup(
            VectorArrow(
                [-2.85, -0.40, 0], [-3.45, -0.40, 0],
                color=coral, stroke_width=3,
            ),
            VectorArrow(
                [-1.95, -0.40, 0], [-1.35, -0.40, 0],
                color=coral, stroke_width=3,
            ),
        )

        rotor_parts = VGroup(rotor, rotor_details)

        # 1.1 — Establish the rotating disc and open caliper.
        def act_1_1():
            self.add(ground)
            self.play(
                FadeIn(rotor),
                FadeIn(rotor_details),
                FadeIn(upper_pad),
                FadeIn(lower_pad),
                FadeIn(upper_arm),
                FadeIn(lower_arm),
                FadeIn(spin_arrow),
                FadeIn(spin_label),
                run_time=2.09,
            )

        self.beat(2.09, 0.69, act_1_1)

        # 1.2 — Pads clamp the disc; contact stress appears.
        def act_1_2():
            self.play(
                upper_pad.animate.shift(DOWN * 0.12),
                lower_pad.animate.shift(UP * 0.07),
                upper_arm.animate.shift(DOWN * 0.12),
                lower_arm.animate.shift(UP * 0.07),
                rotor_details.animate.rotate(-PI / 2, about_point=rotor.get_center()),
                FadeIn(contact_marks),
                run_time=1.36,
            )

        self.beat(1.36, 0.46, act_1_2)

        # 2.1 — Surface shear and wear particles.
        def act_2_1():
            self.play(
                contact_marks.animate.set_opacity(0.25),
                FadeIn(debris),
                rotor_details.animate.rotate(-PI / 3, about_point=rotor.get_center()),
                upper_pad.animate.shift(UP * 0.025),
                lower_pad.animate.shift(DOWN * 0.025),
                run_time=1.76,
            )

        self.beat(1.76, 0.58, act_2_1)

        # 2.2 — The rotor's momentum decreases as braking forces act.
        # Momentum is transferred to the surrounding system, not destroyed.
        def act_2_2():
            self.add(momentum_arrow, momentum_label)
            short_arrow = VectorArrow(
                [-3.0, 0.85, 0],
                [-2.90, 0.85, 0],
                color=cobalt,
                stroke_width=5,
            )
            self.play(
                Transform(momentum_arrow, short_arrow),
                FadeOut(momentum_label),
                FadeIn(transfer_arrows),
                run_time=1.24,
            )

        self.beat(1.24, 0.41, act_2_2)

        # 3.1 — Leave the mechanical brake behind and open the stage.
        def act_3_1():
            self.play(
                FadeOut(rotor_parts),
                FadeOut(upper_pad),
                FadeOut(lower_pad),
                FadeOut(upper_arm),
                FadeOut(lower_arm),
                FadeOut(spin_arrow),
                FadeOut(spin_label),
                FadeOut(contact_marks),
                FadeOut(debris),
                FadeOut(momentum_arrow),
                FadeOut(transfer_arrows),
                self.camera.frame.animate.move_to([1.8, 0, 0]),
                run_time=2.15,
            )

        self.beat(2.15, 0.72, act_3_1)

        # 3.2 — A hypothetical carrier halts without touching a wall.
        projectile = VGroup(
            RoundedRectangle(
                width=1.25, height=0.38, corner_radius=0.16,
                color=slate, fill_color=slate, fill_opacity=1,
            ),
            Triangle(
                color=cobalt, fill_color=cobalt, fill_opacity=1,
            ).scale(0.20).rotate(-PI / 2).move_to([0.65, 0, 0]),
        ).move_to([-2.0, -0.55, 0])

        streamline = VGroup(
            Line(
                [-3.2, -0.43, 0], [-2.65, -0.43, 0],
                color=cobalt, stroke_width=4,
            ),
            Line(
                [-3.35, -0.55, 0], [-2.75, -0.55, 0],
                color=cobalt, stroke_width=2.5,
            ),
            Line(
                [-3.1, -0.67, 0], [-2.70, -0.67, 0],
                color=cobalt, stroke_width=2,
            ),
        )

        def act_3_2():
            self.play(
                FadeIn(projectile),
                FadeIn(streamline),
                run_time=0.25,
            )
            self.play(
                projectile.animate.shift(RIGHT * 3.0),
                streamline.animate.shift(RIGHT * 3.0),
                run_time=0.75,
                rate_func=LINEAR,
            )
            self.play(
                FadeOut(streamline),
                run_time=0.25,
            )

        self.beat(1.25, 0.41, act_3_2)

        # 3.3 — Mark the gap; this is a question, not yet an explanation.
        gap_ticks = VGroup(
            Line([2.8, -0.85, 0], [2.8, -1.95, 0],
                 color=mint, stroke_width=2),
            Line([2.65, -0.85, 0], [2.95, -0.85, 0],
                 color=mint, stroke_width=2),
            Line([2.65, -1.95, 0], [2.95, -1.95, 0],
                 color=mint, stroke_width=2),
        )

        gap_callout = LeaderCallout(
            target_point=[2.8, -1.30, 0],
            title="ZERO CONTACT AIR GAP",
            subtitle="NO PHYSICAL WALL",
            direction=RIGHT + UP,
            color=mint,
            font_size=15,
        )

        def act_3_3():
            self.play(
                FadeIn(gap_ticks),
                FadeIn(gap_callout),
                run_time=1.77,
            )

        self.beat(1.77, 0.59, act_3_3)

        self.finalize()
