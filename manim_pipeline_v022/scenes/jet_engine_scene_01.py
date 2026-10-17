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


class JetEngineScene01(InfographicScene):
    def construct(self):
        self.target_duration = 7.09

        # Visual palette from the approved storyboard.
        bg_color = "#101923"
        airflow_color = "#55C7E8"
        steel_color = "#71899D"
        text_color = "#F3F6FA"
        annotation_color = "#D5DEE7"

        self.camera.background_color = bg_color

        # Establish the horizontal engine axis without a chapter title.
        axis = Line(
            LEFT * 6.2,
            RIGHT * 6.2,
            color=steel_color,
            stroke_width=1.2,
        ).set_opacity(0.48)

        # Simplified external engine casing.
        casing = RoundedRectangle(
            width=9.0,
            height=2.05,
            corner_radius=0.42,
            stroke_color=steel_color,
            stroke_width=2.5,
            fill_color="#182635",
            fill_opacity=0.78,
        ).move_to(ORIGIN)

        inlet_lip = Arc(
            radius=0.83,
            start_angle=PI / 2,
            angle=PI,
            color=steel_color,
            stroke_width=4,
        ).move_to(LEFT * 4.48)

        outlet_lip = Arc(
            radius=0.48,
            start_angle=-PI / 2,
            angle=PI,
            color=steel_color,
            stroke_width=3,
        ).move_to(RIGHT * 4.48)

        # A restrained cutaway window reveals internal components.
        cutaway = RoundedRectangle(
            width=7.05,
            height=1.45,
            corner_radius=0.22,
            stroke_color="#A7B8C7",
            stroke_width=1.0,
            fill_color="#0C1520",
            fill_opacity=0.94,
        ).move_to(RIGHT * 0.15)

        fan_center = LEFT * 3.55
        fan_hub = Circle(
            radius=0.20,
            color=steel_color,
            stroke_width=2,
            fill_color="#AAB9C7",
            fill_opacity=0.9,
        ).move_to(fan_center)

        fan_blades = VGroup()
        for angle in np.linspace(0, TAU, 9, endpoint=False):
            blade = Polygon(
                ORIGIN,
                RIGHT * 0.62 + UP * 0.13,
                RIGHT * 0.38 + UP * 0.29,
                stroke_width=0.7,
                stroke_color=airflow_color,
                fill_color=airflow_color,
                fill_opacity=0.88,
            )
            blade.rotate(angle, about_point=ORIGIN)
            blade.move_to(fan_center)
            fan_blades.add(blade)

        # Compressor stages narrow the flow path and suggest rising pressure.
        compressor_stages = VGroup()
        stage_x = [-2.55, -1.95, -1.35, -0.75, -0.15]
        stage_heights = [1.10, 0.98, 0.86, 0.75, 0.64]

        for x, height in zip(stage_x, stage_heights):
            upper = Line(
                [x, height / 2, 0],
                [x + 0.22, 0.10, 0],
                color=steel_color,
                stroke_width=3,
            )
            lower = Line(
                [x, -height / 2, 0],
                [x + 0.22, -0.10, 0],
                color=steel_color,
                stroke_width=3,
            )
            compressor_stages.add(upper, lower)

        # Airflow arrows remain inside the core passage.
        airflow = VGroup()
        for x in [-4.10, -3.05, -2.00, -0.95, 0.10]:
            arrow = Arrow(
                [x, 0, 0],
                [x + 0.52, 0, 0],
                buff=0,
                color=airflow_color,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.22,
            )
            airflow.add(arrow)

        # Labels are anchored to their relevant components.
        fan_label = Text(
            "FRONT FAN",
            font_size=17,
            color=text_color,
            weight=MEDIUM,
        ).next_to(fan_center, DOWN, buff=0.78)

        compressor_target = compressor_stages[4]
        compressor_label = Text(
            "COMPRESSOR STAGES",
            font_size=16,
            color=text_color,
            weight=MEDIUM,
        ).next_to(compressor_target, DOWN, buff=0.48)

        inlet_label = Text(
            "AIR IN",
            font_size=15,
            color=airflow_color,
            weight=MEDIUM,
        ).next_to(casing, LEFT, buff=0.28)

        inlet_arrow = Arrow(
            LEFT * 6.0,
            LEFT * 4.75,
            buff=0,
            color=airflow_color,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.18,
        ).next_to(inlet_label, UP, buff=0.12)

        # Keep annotation leaders light so the cutaway remains the focal point.
        fan_leader = Line(
            fan_label.get_top(),
            fan_center + DOWN * 0.18,
            color=annotation_color,
            stroke_width=1,
        ).set_opacity(0.75)

        compressor_leader = Line(
            compressor_label.get_top(),
            compressor_target.get_center() + DOWN * 0.08,
            color=annotation_color,
            stroke_width=1,
        ).set_opacity(0.75)

        engine_group = VGroup(
            axis,
            casing,
            inlet_lip,
            outlet_lip,
            cutaway,
            fan_blades,
            fan_hub,
            compressor_stages,
        )

        def act_1_1():
            # Reveal the engine shell and establish the left-to-right axis.
            self.play(
                Create(axis),
                FadeIn(casing),
                run_time=1.15,
            )

            # Open the cutaway and introduce the rotating front fan.
            self.play(
                FadeIn(cutaway),
                Create(inlet_lip),
                Create(outlet_lip),
                run_time=0.75,
            )

            self.play(
                LaggedStart(
                    *[FadeIn(blade, scale=0.65) for blade in fan_blades],
                    lag_ratio=0.035,
                ),
                FadeIn(fan_hub, scale=0.75),
                run_time=0.85,
            )

            # Compressor stages emerge sequentially toward the rear.
            self.play(
                LaggedStart(
                    *[Create(stage) for stage in compressor_stages],
                    lag_ratio=0.12,
                ),
                run_time=1.05,
            )

            # Air is visibly drawn in and transported through the core.
            self.play(
                LaggedStart(
                    *[GrowArrow(arrow) for arrow in airflow],
                    lag_ratio=0.12,
                ),
                FadeIn(inlet_label),
                GrowArrow(inlet_arrow),
                run_time=0.85,
            )

            self.play(
                FadeIn(fan_label),
                Create(fan_leader),
                FadeIn(compressor_label),
                Create(compressor_leader),
                run_time=0.65,
            )

            # A brief restrained flow pulse reinforces the direction of travel.
            self.play(
                *[
                    arrow.animate.set_opacity(0.45)
                    for arrow in airflow
                ],
                run_time=0.37,
            )

        self.beat(5.67, 1.42, act_1_1)
        self.finalize()
