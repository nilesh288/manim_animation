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


class Scene05(InfographicScene):
    target_duration = 67.97

    def construct(self):
        # =========================================================
        # BEAT 1: Electrostatic Coordinate Landscape
        # =========================================================

        # Sub-beat 1.1: Concentric electrostatic potential rings
        self.potential_rings = VGroup(*[
            Circle(
                radius=r,
                stroke_color=PALETTE["stroke"],
                stroke_width=1.2,
                stroke_opacity=0.35,
            )
            for r in [1.2, 2.2, 3.2]
        ])

        def sub_beat_1_1():
            self.play(
                Create(self.potential_rings),
                run_time=2.07,
            )

        self.beat(
            2.07,
            0.69,
            sub_beat_1_1,
            "Establish concentric electrostatic potential rings on quantum coordinate canvas",
        )

        # Sub-beat 1.2: Delicate radial field lines expand outwards
        self.field_lines = VGroup(*[
            Line(
                start=[0, 0, 0],
                end=[3.5 * np.cos(a), 3.5 * np.sin(a), 0],
                stroke_color=PALETTE["blue"],
                stroke_width=1.5,
                stroke_opacity=0.6,
            )
            for a in np.linspace(0, 2 * PI, 8, endpoint=False)
        ])

        def sub_beat_1_2():
            self.play(
                Create(self.field_lines),
                run_time=2.94,
            )

        self.beat(
            2.94,
            0.74,
            sub_beat_1_2,
            "Expand delicate radial electrostatic field lines from coordinate origin",
        )

        # =========================================================
        # BEAT 2: Bohr Model Nucleus & Concentric Shells
        # =========================================================

        # Sub-beat 2.1: Clean Cartesian coordinate crosshairs initialize
        self.crosshairs = VGroup(
            Line([-2.8, 0, 0], [2.8, 0, 0], stroke_color=PALETTE["stroke"], stroke_width=1.2),
            Line([0, -2.8, 0], [0, 2.8, 0], stroke_color=PALETTE["stroke"], stroke_width=1.2),
        )

        def sub_beat_2_1():
            self.play(
                FadeOut(self.field_lines),
                Create(self.crosshairs),
                run_time=1.30,
            )

        self.beat(
            1.30,
            0.44,
            sub_beat_2_1,
            "Initialize central Cartesian coordinate crosshairs at origin",
        )

        # Sub-beat 2.2: Dense positive nucleus with external '+e' charge indicator
        self.nucleus = RigidDisc(
            radius=0.45,
            core_color=PALETTE["coral"],
            is_hollow=False,
        ).move_to([0, 0, 0])

        self.charge_label = Text(
            "+e",
            font_size=20,
            color=PALETTE["coral"],
            weight=BOLD,
        ).next_to(self.nucleus, UR, buff=0.25)

        def sub_beat_2_2():
            self.play(
                FadeIn(self.nucleus, scale=0.5),
                FadeIn(self.charge_label),
                run_time=3.35,
            )

        self.beat(
            3.35,
            0.84,
            sub_beat_2_2,
            "Dense positively charged nucleus anchors at origin with external charge marker",
        )

        # Sub-beat 2.3: Concentric hairline electron shells (r1, r2, r3)
        self.shells = VGroup(*[
            Circle(
                radius=r,
                stroke_color=PALETTE["stroke"],
                stroke_width=1.2,
                stroke_opacity=0.55,
            )
            for r in [1.1, 1.8, 2.6]
        ])

        def sub_beat_2_3():
            self.play(
                FadeOut(self.potential_rings),
                Create(self.shells),
                run_time=1.90,
            )

        self.beat(
            1.90,
            0.63,
            sub_beat_2_3,
            "Sweep concentric hairline electron shells outward at discrete radii",
        )

        # =========================================================
        # BEAT 3: Electron Orbit & Quantum Bohr Radius
        # =========================================================

        # Sub-beat 3.1: Orbiting electrons race along tracks
        self.electrons = VGroup(
            Dot(point=[1.1, 0, 0], radius=0.08, color=PALETTE["blue"]),
            Dot(point=[-1.8, 0, 0], radius=0.08, color=PALETTE["blue"]),
        )

        def sub_beat_3_1():
            self.play(
                Rotate(self.electrons, angle=PI * 1.5, about_point=ORIGIN),
                run_time=2.48,
                rate_func=rate_functions.linear,
            )

        self.beat(
            2.48,
            0.82,
            sub_beat_3_1,
            "Negative electron particles race along circular orbital tracks",
        )

        # Sub-beat 3.2: Radial DimensionRuler displays Bohr radius
        self.bohr_ruler = DimensionRuler(
            start_point=[0, 0, 0],
            end_point=[1.1, 0, 0],
            label="r₀ = 52.9 pm",
            color=PALETTE["stroke"],
        )

        def sub_beat_3_2():
            self.play(
                Create(self.bohr_ruler),
                run_time=2.23,
            )

        self.beat(
            2.23,
            0.74,
            sub_beat_3_2,
            "Deploy radial DimensionRuler displaying precision quantum Bohr radius",
        )

        # =========================================================
        # BEAT 4: Hydrogen Simplification & Lone Valence Electron
        # =========================================================

        # Sub-beat 4.1: Unboxed '¹H' types onto canvas beside proton core
        self.h_symbol = Text(
            "¹H",
            font_size=32,
            color=PALETTE["text"],
            weight=BOLD,
        ).move_to([-2.5, 1.8, 0])

        def sub_beat_4_1():
            self.play(
                FadeOut(self.bohr_ruler),
                FadeOut(self.electrons),
                FadeIn(self.h_symbol, shift=DOWN * 0.2),
                run_time=1.52,
            )

        self.beat(
            1.52,
            0.51,
            sub_beat_4_1,
            "Snap hydrogen element identifier ¹H beside single-proton core",
        )

        # Sub-beat 4.2: Lone valence electron highlighted by open targeting ring
        self.valence_electron = Dot(point=[2.6, 0, 0], radius=0.10, color=PALETTE["mint"])
        self.targeting_ring = Circle(
            radius=0.22,
            stroke_color=PALETTE["mint"],
            stroke_width=1.8,
        ).move_to([2.6, 0, 0])

        def sub_beat_4_2():
            self.play(
                FadeIn(self.valence_electron),
                Create(self.targeting_ring),
                run_time=2.46,
            )

        self.beat(
            2.46,
            0.82,
            sub_beat_4_2,
            "Single lone valence electron highlighted along outer rim by targeting ring",
        )

        # =========================================================
        # BEAT 5: Rapid Orbital Spin & Electrostatic Shield
        # =========================================================

        # Sub-beat 5.1: Electron accelerates leaving continuous luminous trail
        self.luminous_trail = Circle(
            radius=2.6,
            stroke_color=PALETTE["mint"],
            stroke_width=2.5,
        )

        def sub_beat_5_1():
            self.play(
                FadeOut(self.targeting_ring),
                Create(self.luminous_trail),
                run_time=1.73,
            )

        self.beat(
            1.73,
            0.57,
            sub_beat_5_1,
            "Valence electron accelerates leaving continuous coherent orbital ring",
        )

        # Sub-beat 5.2: Translucent negative potential shell expands outward
        self.shield_halo = Circle(
            radius=2.8,
            fill_color=PALETTE["blue"],
            fill_opacity=0.16,
            stroke_color=PALETTE["blue"],
            stroke_width=1.6,
        )

        def sub_beat_5_2():
            self.play(
                FadeIn(self.shield_halo, scale=0.85),
                run_time=3.53,
            )

        self.beat(
            3.53,
            0.88,
            sub_beat_5_2,
            "Translucent negative potential shell expands outward forming protective boundary",
        )

        # =========================================================
        # BEAT 6: Dual Atom Manifestation & Mutual Approach
        # =========================================================

        # Construct twin identical atoms with unified clouds
        self.atom_left = VGroup(
            RigidDisc(radius=0.35, core_color=PALETTE["coral"], is_hollow=False),
            Circle(
                radius=1.35,
                fill_color=PALETTE["blue"],
                fill_opacity=0.16,
                stroke_color=PALETTE["blue"],
                stroke_width=1.6,
            ),
        ).move_to([-2.4, 0, 0])

        self.atom_right = VGroup(
            RigidDisc(radius=0.35, core_color=PALETTE["coral"], is_hollow=False),
            Circle(
                radius=1.35,
                fill_color=PALETTE["blue"],
                fill_opacity=0.16,
                stroke_color=PALETTE["blue"],
                stroke_width=1.6,
            ),
        ).move_to([5.5, 0, 0])

        # Sub-beat 6.1: Second identical hydrogen atom enters from right
        def sub_beat_6_1():
            self.play(
                FadeOut(self.h_symbol),
                FadeOut(self.shells),
                FadeOut(self.crosshairs),
                FadeOut(self.nucleus),
                FadeOut(self.charge_label),
                FadeOut(self.valence_electron),
                FadeOut(self.luminous_trail),
                FadeOut(self.shield_halo),
                FadeIn(self.atom_left),
                self.atom_right.animate.move_to([2.4, 0, 0]),
                run_time=2.21,
            )

        self.beat(
            2.21,
            0.74,
            sub_beat_6_1,
            "Twin hydrogen atoms manifest enveloped in matching negative electrostatic clouds",
        )

        # Sub-beat 6.2: Both atoms drift toward central axis and decelerate
        def sub_beat_6_2():
            self.play(
                self.atom_left.animate.shift(RIGHT * 1.05),
                self.atom_right.animate.shift(LEFT * 1.05),
                run_time=3.78,
                rate_func=rate_functions.ease_out_quad,
            )

        self.beat(
            3.78,
            0.94,
            sub_beat_6_2,
            "Both atoms drift toward each other along central axis slowing near perimeter bounds",
        )

        # =========================================================
        # BEAT 7: Negative Polarity & Mutual Coulomb Repulsion
        # =========================================================

        # Sub-beat 7.1: Negative polarity tags illuminate on facing perimeters
        self.tag_left = Text("−", font_size=28, color=PALETTE["blue"], weight=BOLD).move_to(
            [-0.18, 0.45, 0]
        )
        self.tag_right = Text("−", font_size=28, color=PALETTE["blue"], weight=BOLD).move_to(
            [0.18, 0.45, 0]
        )

        def sub_beat_7_1():
            self.play(
                FadeIn(self.tag_left),
                FadeIn(self.tag_right),
                run_time=1.11,
            )

        self.beat(
            1.11,
            0.37,
            sub_beat_7_1,
            "Negative polarity tags illuminate on facing boundaries of electron clouds",
        )

        # Sub-beat 7.2: Diverging vector arrows snap pointing away
        self.repel_left = Arrow(
            start=[-0.15, 0, 0],
            end=[-1.1, 0, 0],
            color=PALETTE["coral"],
            buff=0,
            stroke_width=4.5,
        )
        self.repel_right = Arrow(
            start=[0.15, 0, 0],
            end=[1.1, 0, 0],
            color=PALETTE["coral"],
            buff=0,
            stroke_width=4.5,
        )

        def sub_beat_7_2():
            self.play(
                FadeOut(self.tag_left),
                FadeOut(self.tag_right),
                GrowArrow(self.repel_left),
                GrowArrow(self.repel_right),
                run_time=1.26,
            )

        self.beat(
            1.26,
            0.42,
            sub_beat_7_2,
            "Diverging vector arrows snap into existence pointing aggressively away",
        )

        # =========================================================
        # BEAT 8: Forced Approach & Coulomb Law (F_c ∝ 1/r²)
        # =========================================================

        # Sub-beat 8.1: Atoms close distance against repulsive field
        def sub_beat_8_1():
            self.play(
                FadeOut(self.repel_left),
                FadeOut(self.repel_right),
                self.atom_left.animate.shift(RIGHT * 0.35),
                self.atom_right.animate.shift(LEFT * 0.35),
                run_time=2.04,
            )

        self.beat(
            2.04,
            0.68,
            sub_beat_8_1,
            "Atoms close distance to within fraction of atomic diameter",
        )

        # Sub-beat 8.2: Compressed electrostatic field lines & Coulomb formula
        self.coulomb_formula = Text(
            "F_c ∝ 1/r²",
            font_size=30,
            color=PALETTE["coral"],
            weight=BOLD,
        ).move_to([0, 1.8, 0])

        self.compressed_lines = VGroup(*[
            Arc(
                radius=0.4 + i * 0.25,
                start_angle=-PI / 2,
                angle=PI,
                arc_center=[-0.1 - i * 0.08, 0, 0],
                color=PALETTE["coral"],
                stroke_width=1.5,
            )
            for i in range(3)
        ])

        def sub_beat_8_2():
            self.play(
                FadeIn(self.coulomb_formula, shift=DOWN * 0.2),
                Create(self.compressed_lines),
                run_time=3.02,
            )

        self.beat(
            3.02,
            0.75,
            sub_beat_8_2,
            "Electrostatic field lines compress as Coulomb formula F_c ∝ 1/r² flashes",
        )

        # =========================================================
        # BEAT 9: Low Energy State & Elastic Rebound Spring
        # =========================================================

        # Sub-beat 9.1: Low velocity indicators float above nuclei
        self.v_tag_a = Text("v_initial ≈ 0", font_size=20, color=PALETTE["text_dim"]).next_to(
            self.atom_left, UP, buff=0.4
        )
        self.v_tag_b = Text("v_initial ≈ 0", font_size=20, color=PALETTE["text_dim"]).next_to(
            self.atom_right, UP, buff=0.4
        )

        def sub_beat_9_1():
            self.play(
                FadeOut(self.coulomb_formula),
                FadeOut(self.compressed_lines),
                FadeIn(self.v_tag_a),
                FadeIn(self.v_tag_b),
                run_time=1.34,
            )

        self.beat(
            1.34,
            0.44,
            sub_beat_9_1,
            "Low-velocity indicators v_initial ≈ 0 float above approaching nuclei",
        )

        # Sub-beat 9.2: Compressed geometric spring appears between clouds
        self.spring_curve = VMobject().set_points_as_corners([
            [-0.6, 0, 0],
            [-0.4, 0.22, 0],
            [-0.2, -0.22, 0],
            [0.0, 0.22, 0],
            [0.2, -0.22, 0],
            [0.4, 0.22, 0],
            [0.6, 0, 0],
        ]).set_stroke(color=PALETTE["amber"], width=3.5)

        def sub_beat_9_2():
            self.play(
                Create(self.spring_curve),
                run_time=2.35,
            )

        self.beat(
            2.35,
            0.78,
            sub_beat_9_2,
            "Stylized geometric spring appears compressed between approaching clouds",
        )

        # Sub-beat 9.3: Spring releases, deflecting atoms apart
        def sub_beat_9_3():
            self.play(
                FadeOut(self.spring_curve),
                FadeOut(self.v_tag_a),
                FadeOut(self.v_tag_b),
                self.atom_left.animate.shift(LEFT * 1.5),
                self.atom_right.animate.shift(RIGHT * 1.5),
                run_time=2.94,
                rate_func=rate_functions.ease_out_quad,
            )

        self.beat(
            2.94,
            0.73,
            sub_beat_9_3,
            "Virtual spring releases bouncing hydrogen atoms apart along incoming paths",
        )

        # =========================================================
        # BEAT 10: Potential Energy Hill & Activation Barrier (E_a)
        # =========================================================

        # Sub-beat 10.1: Potential energy hill elevates between atoms
        self.potential_hill = FunctionGraph(
            lambda x: 2.1 * np.exp(-(x**2) / 0.7) - 1.0,
            x_range=[-2.5, 2.5],
            color=PALETTE["stroke"],
            stroke_width=2.5,
        )

        def sub_beat_10_1():
            self.play(
                Create(self.potential_hill),
                run_time=1.46,
            )

        self.beat(
            1.46,
            0.49,
            sub_beat_10_1,
            "Smooth potential energy curve elevates between atoms forming potential hill",
        )

        # Sub-beat 10.2: Vertical DimensionRuler crowns peak with activation label
        self.barrier_ruler = DimensionRuler(
            start_point=[0, -1.0, 0],
            end_point=[0, 1.1, 0],
            label="E_a: ACTIVATION BARRIER",
            color=PALETTE["coral"],
        )

        def sub_beat_10_2():
            self.play(
                Create(self.barrier_ruler),
                run_time=2.04,
            )

        self.beat(
            2.04,
            0.68,
            sub_beat_10_2,
            "Vertical DimensionRuler crowns peak labeled E_a: ACTIVATION BARRIER",
        )

        # =========================================================
        # BEAT 11: Insufficient Momentum & Bond Dissolution
        # =========================================================

        # Sub-beat 11.1: Weak momentum vector rolls halfway and slides down
        self.p_weak = Arrow(
            start=[-2.2, -1.0, 0],
            end=[-1.6, -0.6, 0],
            color=PALETTE["indigo"],
            buff=0,
            stroke_width=4.0,
        )

        def sub_beat_11_1():
            self.play(
                GrowArrow(self.p_weak),
                self.p_weak.animate.move_to([-0.8, 0.1, 0]),
                run_time=0.80,
            )
            self.play(
                self.p_weak.animate.move_to([-1.9, -0.9, 0]),
                run_time=0.73,
                rate_func=rate_functions.ease_in_quad,
            )

        self.beat(
            1.53,
            0.51,
            sub_beat_11_1,
            "Momentum vector rolls halfway up potential slope, halts, and slides back down",
        )

        # Sub-beat 11.2: Dashed link breaks apart with dissolution effect
        self.dashed_bond = DashedLine(
            start=[-2.5, -0.2, 0],
            end=[2.5, -0.2, 0],
            color=PALETTE["stroke"],
            stroke_width=2.0,
            dash_length=0.15,
        )

        def sub_beat_11_2():
            self.play(
                Create(self.dashed_bond),
                run_time=0.60,
            )
            self.play(
                FadeOut(self.dashed_bond),
                FadeOut(self.p_weak),
                FadeOut(self.barrier_ruler),
                run_time=1.03,
            )

        self.beat(
            1.63,
            0.54,
            sub_beat_11_2,
            "Dashed link between atoms breaks apart confirming failure to form bond",
        )

        # ---------------------------------------------------------
        # FINAL RUNTIME VALIDATION
        # ---------------------------------------------------------
        self.finalize()
