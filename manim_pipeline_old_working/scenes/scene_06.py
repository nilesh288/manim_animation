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


class Scene06(InfographicScene):
    target_duration = 106.36

    def construct(self):
        # =========================================================
        # BEAT 1: Kinematic Bridge to Molecular Chemistry
        # =========================================================

        # Sub-beat 1.1: Macroscopic cart runway re-emerges in miniature on the left
        self.left_runway = Line(
            start=[-6.2, -0.6, 0],
            end=[-1.2, -0.6, 0],
            stroke_color=PALETTE["stroke"],
            stroke_width=3.0,
        )
        self.left_ticks = VGroup(*[
            Line(
                start=[x, -0.6, 0],
                end=[x, -0.75, 0],
                stroke_color=PALETTE["stroke_light"],
                stroke_width=1.5,
            )
            for x in np.arange(-6.0, -1.0, 0.8)
        ])
        self.mini_cart = RigidDisc(
            radius=0.35,
            core_color=PALETTE["indigo"],
            is_hollow=False,
        ).move_to([-4.8, -0.25, 0])
        self.mini_track_group = VGroup(self.left_runway, self.left_ticks, self.mini_cart)

        def sub_beat_1_1():
            self.play(
                Create(self.left_runway),
                Create(self.left_ticks),
                FadeIn(self.mini_cart),
                run_time=2.18,
            )

        self.beat(
            2.18,
            0.73,
            sub_beat_1_1,
            "Establish macroscopic cart runway in miniature on stage left",
        )

        # Sub-beat 1.2: Luminous mint flow line bridges runway to atomic coordinate grid
        self.bridge_flow = CubicBezier(
            [-1.2, -0.6, 0],
            [0.2, -0.6, 0],
            [0.5, 0.8, 0],
            [2.0, 0.8, 0],
            color=PALETTE["mint"],
            stroke_width=3.5,
        )
        self.atomic_grid = VGroup(
            Circle(radius=1.2, stroke_color=PALETTE["stroke_light"], stroke_width=1.2),
            Line([2.3, -0.4, 0], [4.7, -0.4, 0], stroke_color=PALETTE["stroke_light"], stroke_width=1.2),
            Line([3.5, -1.6, 0], [3.5, 0.8, 0], stroke_color=PALETTE["stroke_light"], stroke_width=1.2),
        ).move_to([3.5, 0.0, 0])

        def sub_beat_1_2():
            self.play(
                Create(self.bridge_flow),
                Create(self.atomic_grid),
                run_time=2.26,
            )

        self.beat(
            2.26,
            0.75,
            sub_beat_1_2,
            "Luminous mint flow line bridges cart track directly to atomic coordinate grid",
        )

        # =========================================================
        # BEAT 2: Activation Barrier Apex & Query Focus
        # =========================================================

        # Sub-beat 2.1: Tall potential energy hill 'E_a' centers on canvas in coral
        self.hill_curve = FunctionGraph(
            lambda x: 2.1 * np.exp(-(x**2) / 0.65) - 0.9,
            x_range=[-3.0, 3.0],
            color=PALETTE["coral"],
            stroke_width=3.5,
        )

        def sub_beat_2_1():
            self.play(
                FadeOut(self.mini_track_group),
                FadeOut(self.bridge_flow),
                FadeOut(self.atomic_grid),
                Create(self.hill_curve),
                run_time=1.21,
            )

        self.beat(
            1.21,
            0.40,
            sub_beat_2_1,
            "Center tall potential energy hill pulsing in warning coral across canvas",
        )

        # Sub-beat 2.2: Dashed query brackets enclose barrier apex with editorial '?'
        self.query_label = Text(
            "?",
            font_size=42,
            color=PALETTE["text"],
            weight=BOLD,
        ).move_to([0, 1.85, 0])
        self.query_box = DashedVMobject(
            Rectangle(width=1.0, height=1.0, stroke_color=PALETTE["stroke_light"], stroke_width=1.8),
            num_dashes=16,
        ).move_to([0, 1.85, 0])

        def sub_beat_2_2():
            self.play(
                Create(self.query_box),
                FadeIn(self.query_label, scale=1.2),
                run_time=1.45,
            )

        self.beat(
            1.45,
            0.48,
            sub_beat_2_2,
            "Dashed query brackets enclose barrier apex querying overcoming mechanism",
        )

        # =========================================================
        # BEAT 3: Kinetic Energy Injection
        # =========================================================

        # Sub-beat 3.1: Radiant energy beam injects from off-screen
        self.injection_beam = Arrow(
            start=[-6.5, 2.2, 0],
            end=[-1.6, 0.8, 0],
            color=PALETTE["amber"],
            stroke_width=6.0,
            buff=0,
        )

        def sub_beat_3_1():
            self.play(
                FadeOut(self.query_box),
                FadeOut(self.query_label),
                GrowArrow(self.injection_beam),
                run_time=1.21,
            )

        self.beat(
            1.21,
            0.40,
            sub_beat_3_1,
            "Vibrant energy beam injects from off-screen into atomic translational axes",
        )

        # Sub-beat 3.2: Bold typography 'ΔE_k >> E_a' ignites in mint
        self.surge_metric = Text(
            "ΔE_k >> E_a",
            font_size=32,
            color=PALETTE["mint"],
            weight=BOLD,
        ).move_to([0, 2.5, 0])

        def sub_beat_3_2():
            self.play(
                FadeIn(self.surge_metric, shift=DOWN * 0.2),
                run_time=0.87,
            )

        self.beat(
            0.87,
            0.35,
            sub_beat_3_2,
            "Ignite bold kinetic energy inequality ΔE_k >> E_a above barrier",
        )

        # =========================================================
        # BEAT 4: Rapid Approach & Momentum Penetration
        # =========================================================

        # Sub-beat 4.1: Twin hydrogen atoms hurtle inward with blue velocity vectors
        self.atom_left = RigidDisc(
            radius=0.45,
            core_color=PALETTE["coral"],
            is_hollow=False,
        ).move_to([-4.5, 0.0, 0])
        self.atom_right = RigidDisc(
            radius=0.45,
            core_color=PALETTE["coral"],
            is_hollow=False,
        ).move_to([4.5, 0.0, 0])
        self.v_arrow_left = Arrow(
            start=[-4.5, 0.0, 0],
            end=[-2.8, 0.0, 0],
            color=PALETTE["blue"],
            stroke_width=4.5,
            buff=0,
        )
        self.v_arrow_right = Arrow(
            start=[4.5, 0.0, 0],
            end=[2.8, 0.0, 0],
            color=PALETTE["blue"],
            stroke_width=4.5,
            buff=0,
        )

        def sub_beat_4_1():
            self.play(
                FadeOut(self.injection_beam),
                FadeOut(self.hill_curve),
                FadeIn(self.atom_left),
                FadeIn(self.atom_right),
                GrowArrow(self.v_arrow_left),
                GrowArrow(self.v_arrow_right),
                self.atom_left.animate.shift(RIGHT * 2.2),
                self.atom_right.animate.shift(LEFT * 2.2),
                run_time=2.46,
            )

        self.beat(
            2.46,
            0.82,
            sub_beat_4_1,
            "Both hydrogen atoms hurtle inward propelled by elongating velocity vectors",
        )

        # Sub-beat 4.2: Heavy momentum vectors pierce through Coulomb repulsion
        self.p_arrow_left = Arrow(
            start=[-2.3, -0.75, 0],
            end=[-0.6, -0.75, 0],
            color=PALETTE["indigo"],
            stroke_width=6.5,
            buff=0,
        )
        self.p_arrow_right = Arrow(
            start=[2.3, -0.75, 0],
            end=[0.6, -0.75, 0],
            color=PALETTE["indigo"],
            stroke_width=6.5,
            buff=0,
        )
        self.coulomb_barrier_lines = VGroup(*[
            Line([0, -0.8 + i * 0.4, 0], [0, -0.6 + i * 0.4, 0], stroke_color=PALETTE["coral"], stroke_width=2.5)
            for i in range(5)
        ])

        def sub_beat_4_2():
            self.play(
                FadeOut(self.v_arrow_left),
                FadeOut(self.v_arrow_right),
                Create(self.coulomb_barrier_lines),
                GrowArrow(self.p_arrow_left),
                GrowArrow(self.p_arrow_right),
                run_time=2.85,
            )

        self.beat(
            2.85,
            0.71,
            sub_beat_4_2,
            "Heavy momentum vectors pierce straight through Coulomb repulsion lines",
        )

        # =========================================================
        # BEAT 5: Macroscopic Cart Overlay & Barrier Shatter
        # =========================================================

        # Sub-beat 5.1: Translucent cart outlines overlay speeding atoms
        self.cart_ghost_left = VisualCard(
            width=1.3,
            height=0.85,
            fill_color=PALETTE["surface_card"],
            border_color=PALETTE["stroke_light"],
        ).move_to(self.atom_left.get_center()).set_opacity(0.45)
        self.cart_ghost_right = VisualCard(
            width=1.3,
            height=0.85,
            fill_color=PALETTE["surface_card"],
            border_color=PALETTE["stroke_light"],
        ).move_to(self.atom_right.get_center()).set_opacity(0.45)

        def sub_beat_5_1():
            self.play(
                FadeIn(self.cart_ghost_left),
                FadeIn(self.cart_ghost_right),
                self.atom_left.animate.shift(RIGHT * 1.0),
                self.atom_right.animate.shift(LEFT * 1.0),
                self.cart_ghost_left.animate.shift(RIGHT * 1.0),
                self.cart_ghost_right.animate.shift(LEFT * 1.0),
                run_time=2.47,
            )

        self.beat(
            2.47,
            0.82,
            sub_beat_5_1,
            "Translucent kinematic cart outlines momentarily overlay accelerating atoms",
        )

        # Sub-beat 5.2: Atomic pair surges over crest; barrier shatters into mint fragments
        self.shatter_fragments = VGroup(*[
            Line(
                [0, -0.6 + i * 0.3, 0],
                [0.4 * np.cos(i * 1.2), -0.6 + i * 0.3 + 0.4 * np.sin(i * 1.2), 0],
                stroke_color=PALETTE["mint"],
                stroke_width=2.5,
            )
            for i in range(5)
        ])

        def sub_beat_5_2():
            self.play(
                FadeOut(self.cart_ghost_left),
                FadeOut(self.cart_ghost_right),
                FadeOut(self.p_arrow_left),
                FadeOut(self.p_arrow_right),
                FadeOut(self.surge_metric),
                self.atom_left.animate.move_to([-0.7, 0, 0]),
                self.atom_right.animate.move_to([0.7, 0, 0]),
                ReplacementTransform(self.coulomb_barrier_lines, self.shatter_fragments),
                run_time=2.23,
            )
            self.play(
                self.shatter_fragments.animate.set_stroke(opacity=0.0).scale(1.8),
                run_time=2.23,
            )

        self.beat(
            4.46,
            1.11,
            sub_beat_5_2,
            "Atomic pair surges over potential crest shattering barrier into mint fragments",
        )

        # =========================================================
        # BEAT 6: Valence Contact & Orbital Intersection
        # =========================================================

        # Sub-beat 6.1: Circular valence perimeters meet and flatten
        self.valence_shell_left = Circle(
            radius=0.9,
            stroke_color=PALETTE["blue"],
            stroke_width=2.0,
        ).move_to([-0.7, 0, 0])
        self.valence_shell_right = Circle(
            radius=0.9,
            stroke_color=PALETTE["blue"],
            stroke_width=2.0,
        ).move_to([0.7, 0, 0])

        def sub_beat_6_1():
            self.play(
                Create(self.valence_shell_left),
                Create(self.valence_shell_right),
                run_time=2.49,
            )

        self.beat(
            2.49,
            0.83,
            sub_beat_6_1,
            "Circular valence shell perimeters meet and press under forward momentum",
        )

        # Sub-beat 6.2: Boundaries intersect forming shared lens of intersection in mint
        self.shared_lens = Intersection(
            Circle(radius=0.9).move_to([-0.55, 0, 0]),
            Circle(radius=0.9).move_to([0.55, 0, 0]),
            fill_color=PALETTE["mint"],
            fill_opacity=0.35,
            stroke_color=PALETTE["mint"],
            stroke_width=2.5,
        )

        def sub_beat_6_2():
            self.play(
                self.valence_shell_left.animate.shift(RIGHT * 0.15),
                self.valence_shell_right.animate.shift(LEFT * 0.15),
                self.atom_left.animate.shift(RIGHT * 0.15),
                self.atom_right.animate.shift(LEFT * 0.15),
                Create(self.shared_lens),
                run_time=1.77,
            )

        self.beat(
            1.77,
            0.59,
            sub_beat_6_2,
            "Valence shells intersect forming shared lens zone highlighted in mint",
        )

        # =========================================================
        # BEAT 7: Boundary Restructuring & Molecular Envelope
        # =========================================================

        # Sub-beat 7.1: Internal dividing walls dissolve into unified boundary
        def sub_beat_7_1():
            self.play(
                FadeOut(self.shared_lens),
                self.valence_shell_left.animate.set_stroke(opacity=0.3),
                self.valence_shell_right.animate.set_stroke(opacity=0.3),
                run_time=2.48,
            )

        self.beat(
            2.48,
            0.82,
            sub_beat_7_1,
            "Internal dividing walls fade out into a unified outer perimeter",
        )

        # Sub-beat 7.2: Shells morph into elongated continuous molecular envelope
        self.peanut_envelope = RoundedRectangle(
            corner_radius=0.75,
            width=3.1,
            height=1.65,
            stroke_color=PALETTE["stroke"],
            stroke_width=2.5,
            fill_color=PALETTE["mint"],
            fill_opacity=0.10,
        ).move_to([0, 0, 0])

        def sub_beat_7_2():
            self.play(
                FadeOut(self.valence_shell_left),
                FadeOut(self.valence_shell_right),
                Create(self.peanut_envelope),
                run_time=1.95,
            )

        self.beat(
            1.95,
            0.65,
            sub_beat_7_2,
            "Circular shells morph into continuous elongated molecular envelope",
        )

        # =========================================================
        # BEAT 8: Valence Electron Liberation & Dissolved Orbits
        # =========================================================

        # Sub-beat 8.1: Electrons break free into expanded trajectories
        self.electron_1 = Dot(point=[-0.55, 0.45, 0], radius=0.08, color=PALETTE["blue"])
        self.electron_2 = Dot(point=[0.55, -0.45, 0], radius=0.08, color=PALETTE["blue"])

        def sub_beat_8_1():
            self.play(
                FadeIn(self.electron_1),
                FadeIn(self.electron_2),
                self.electron_1.animate.shift(UP * 0.25 + RIGHT * 0.2),
                self.electron_2.animate.shift(DOWN * 0.25 + LEFT * 0.2),
                run_time=2.00,
            )

        self.beat(
            2.00,
            0.66,
            sub_beat_8_1,
            "Valence electrons break free from circular Bohr paths into wide trajectories",
        )

        # Sub-beat 8.2: Concentric orbital memory rings dissolve
        self.orbital_memory = DashedVMobject(
            Circle(radius=0.7, stroke_color=PALETTE["stroke_light"], stroke_width=1.2).move_to([-0.55, 0, 0]),
            num_dashes=12,
        )

        def sub_beat_8_2():
            self.play(
                Create(self.orbital_memory),
                self.orbital_memory.animate.set_stroke(opacity=0.0),
                run_time=1.54,
            )

        self.beat(
            1.54,
            0.52,
            sub_beat_8_2,
            "Old monocentric orbital rings dissolve into faint dashed memory traces",
        )

        # =========================================================
        # BEAT 9: Dual Attraction Vectors & Interference Pattern
        # =========================================================

        # Sub-beat 9.1: Dual attractive force vectors shoot from electrons to nuclei
        self.attract_1a = Line(self.electron_1.get_center(), self.atom_left.get_center(), color=PALETTE["blue"], stroke_width=2.0)
        self.attract_1b = Line(self.electron_1.get_center(), self.atom_right.get_center(), color=PALETTE["blue"], stroke_width=2.0)
        self.attract_2a = Line(self.electron_2.get_center(), self.atom_left.get_center(), color=PALETTE["blue"], stroke_width=2.0)
        self.attract_2b = Line(self.electron_2.get_center(), self.atom_right.get_center(), color=PALETTE["blue"], stroke_width=2.0)
        self.attraction_lines = VGroup(self.attract_1a, self.attract_1b, self.attract_2a, self.attract_2b)

        def sub_beat_9_1():
            self.play(
                Create(self.attraction_lines),
                run_time=2.12,
            )

        self.beat(
            2.12,
            0.70,
            sub_beat_9_1,
            "Dual attractive force vectors shoot from each electron toward both nuclei",
        )

        # Sub-beat 9.2: Both nuclei pulse simultaneously with electrostatic interference field
        def sub_beat_9_2():
            self.play(
                self.atom_left.animate.scale(1.2),
                self.atom_right.animate.scale(1.2),
                self.attraction_lines.animate.set_stroke(color=PALETTE["indigo"], width=2.8),
                run_time=1.17,
            )
            self.play(
                self.atom_left.animate.scale(1 / 1.2),
                self.atom_right.animate.scale(1 / 1.2),
                self.attraction_lines.animate.set_stroke(color=PALETTE["blue"], width=2.0),
                run_time=1.17,
            )

        self.beat(
            2.34,
            0.78,
            sub_beat_9_2,
            "Both positive nuclei pulse simultaneously weaving electrostatic interference field",
        )

        # =========================================================
        # BEAT 10: Molecular Orbital Boundary & Shared Orbit
        # =========================================================

        # Sub-beat 10.1: Outer contour solidifies into continuous boundary in mint
        def sub_beat_10_1():
            self.play(
                FadeOut(self.attraction_lines),
                self.peanut_envelope.animate.set_stroke(color=PALETTE["mint"], width=3.2),
                run_time=1.22,
            )

        self.beat(
            1.22,
            0.40,
            sub_beat_10_1,
            "Outer molecular contour solidifies into continuous mint boundary",
        )

        # Sub-beat 10.2: Electrons trace continuous figure-eight path around both nuclei
        fig8_curve = ParametricFunction(
            lambda t: np.array([
                1.2 * np.cos(t),
                0.5 * np.sin(2 * t),
                0,
            ]),
            t_range=[0, 2 * PI],
            color=PALETTE["mint"],
            stroke_width=1.8,
            stroke_opacity=0.6,
        )

        def sub_beat_10_2():
            self.play(
                Create(fig8_curve),
                MoveAlongPath(self.electron_1, fig8_curve),
                run_time=2.18,
            )

        self.beat(
            2.18,
            0.72,
            sub_beat_10_2,
            "Electrons lock into continuous figure-eight path weaving around both nuclei",
        )

        # =========================================================
        # BEAT 11: Bond Axis & Covalent Bond Formation
        # =========================================================

        # Sub-beat 11.1: Bond axis line draws between two locked nuclei
        self.bond_axis = Line(
            start=[-0.55, 0, 0],
            end=[0.55, 0, 0],
            stroke_color=PALETTE["indigo"],
            stroke_width=3.5,
        )

        def sub_beat_11_1():
            self.play(
                Create(self.bond_axis),
                run_time=0.65,
            )

        self.beat(
            0.65,
            0.35,
            sub_beat_11_1,
            "Central horizontal bond axis draws between two locked nuclei",
        )

        # Sub-beat 11.2: Unboxed editorial 'COVALENT BOND' stamps directly above shared density
        self.covalent_label = Text(
            "COVALENT BOND",
            font_size=28,
            color=PALETTE["text"],
            weight=BOLD,
        ).move_to([0, 1.5, 0])

        def sub_beat_11_2():
            self.play(
                FadeIn(self.covalent_label, shift=DOWN * 0.2),
                run_time=1.13,
            )

        self.beat(
            1.13,
            0.38,
            sub_beat_11_2,
            "Unboxed editorial typography COVALENT BOND stamps directly above density",
        )

        # =========================================================
        # BEAT 12: Shared Electron Stability & Potential Well
        # =========================================================

        # Sub-beat 12.1: Electrons settle directly between nuclei
        def sub_beat_12_1():
            self.play(
                FadeOut(fig8_curve),
                self.electron_1.animate.move_to([0, 0.22, 0]),
                self.electron_2.animate.move_to([0, -0.22, 0]),
                run_time=1.52,
            )

        self.beat(
            1.52,
            0.51,
            sub_beat_12_1,
            "Shared electron pair positions directly between nuclei shielding repulsion",
        )

        # Sub-beat 12.2: Potential energy curve plunges into deep well labeled 'ΔV < 0'
        self.potential_well = FunctionGraph(
            lambda x: -1.7 * np.exp(-(x**2) / 0.5) - 0.4,
            x_range=[-2.2, 2.2],
            color=PALETTE["mint"],
            stroke_width=2.5,
        )
        self.well_label = Text(
            "ΔV < 0",
            font_size=24,
            color=PALETTE["mint"],
            weight=BOLD,
        ).move_to([1.8, -1.8, 0])

        def sub_beat_12_2():
            self.play(
                Create(self.potential_well),
                FadeIn(self.well_label),
                run_time=2.91,
            )

        self.beat(
            2.91,
            0.73,
            sub_beat_12_2,
            "Potential energy curve plunges into deep stable potential well labeled ΔV < 0",
        )

        # Sub-beat 12.3: Unboxed label 'H₂ MOLECULE' settles beneath unified body
        self.h2_label = Text(
            "H₂ MOLECULE",
            font_size=28,
            color=PALETTE["indigo"],
            weight=BOLD,
        ).move_to([0, -1.5, 0])

        def sub_beat_12_3():
            self.play(
                FadeOut(self.potential_well),
                FadeOut(self.well_label),
                FadeIn(self.h2_label, shift=UP * 0.2),
                run_time=4.05,
            )

        self.beat(
            4.05,
            1.01,
            sub_beat_12_3,
            "Unboxed label H₂ MOLECULE settles beneath structure as system moves as unified body",
        )

        # =========================================================
        # BEAT 13: Binding Energy Differential & Surplus Energy
        # =========================================================

        # Sub-beat 13.1: Vertical DimensionRuler measures binding energy drop
        self.binding_ruler = DimensionRuler(
            start_point=[-2.0, 1.2, 0],
            end_point=[-2.0, -1.2, 0],
            label="ΔE_bind",
            color=PALETTE["coral"],
        )

        def sub_beat_13_1():
            self.play(
                Create(self.binding_ruler),
                run_time=4.62,
            )

        self.beat(
            4.62,
            1.16,
            sub_beat_13_1,
            "Vertical DimensionRuler measures energy differential between states",
        )

        # Sub-beat 13.2: Energy differential highlights in amber with outward tension
        self.energy_flash = Annulus(
            inner_radius=0.9,
            outer_radius=1.3,
            color=PALETTE["amber"],
            fill_opacity=0.35,
            stroke_color=PALETTE["amber"],
            stroke_width=2.0,
        ).move_to([0, 0, 0])

        def sub_beat_13_2():
            self.play(
                Create(self.energy_flash),
                run_time=2.33,
            )

        self.beat(
            2.33,
            0.78,
            sub_beat_13_2,
            "Surplus binding energy highlights in vibrant amber pulsing with outward tension",
        )

        # =========================================================
        # BEAT 14: Photon Discharge & Thermal Recoil
        # =========================================================

        # Sub-beat 14.1: Sinusoidal photon wave packet flashes diagonally outward
        self.photon_wave = ParametricFunction(
            lambda t: np.array([
                t,
                0.25 * np.sin(10 * t) + 0.6 * t,
                0,
            ]),
            t_range=[0.0, 3.2],
            color=PALETTE["amber"],
            stroke_width=3.2,
        ).move_to([2.6, 1.5, 0])

        def sub_beat_14_1():
            self.play(
                FadeOut(self.binding_ruler),
                FadeOut(self.energy_flash),
                Create(self.photon_wave),
                run_time=3.35,
            )

        self.beat(
            3.35,
            0.84,
            sub_beat_14_1,
            "Sinusoidal wave packet flashes out from bond center toward stage margin",
        )

        # Sub-beat 14.2: Concentric acoustic ripples pulse with label 'hν (PHOTON)'
        self.photon_tag = Text(
            "hν (PHOTON)",
            font_size=24,
            color=PALETTE["coral"],
            weight=BOLD,
        ).next_to(self.photon_wave, UP, buff=0.2)
        self.thermal_ripple = Circle(
            radius=1.8,
            stroke_color=PALETTE["coral"],
            stroke_width=1.8,
            stroke_opacity=0.6,
        ).move_to([0, 0, 0])

        def sub_beat_14_2():
            self.play(
                FadeIn(self.photon_tag),
                Create(self.thermal_ripple),
                run_time=3.32,
            )

        self.beat(
            3.32,
            0.83,
            sub_beat_14_2,
            "Concentric acoustic ripples pulse along molecular bond axis with hν tag",
        )

        # =========================================================
        # BEAT 15: Master Historical Synthesis Timeline
        # =========================================================

        # Sub-beat 15.1: Timeline unrolls across base with 'MECHANICAL WORK'
        self.timeline_axis = Line(
            start=[-5.8, -2.5, 0],
            end=[5.8, -2.5, 0],
            stroke_color=PALETTE["stroke"],
            stroke_width=2.5,
        )
        self.dot_m1 = Dot([-4.5, -2.5, 0], radius=0.09, color=PALETTE["coral"])
        self.label_m1 = Text(
            "MECHANICAL WORK",
            font_size=16,
            color=PALETTE["text"],
            weight=BOLD,
        ).next_to(self.dot_m1, UP, buff=0.15)

        def sub_beat_15_1():
            self.play(
                FadeOut(self.photon_wave),
                FadeOut(self.photon_tag),
                FadeOut(self.thermal_ripple),
                FadeOut(self.covalent_label),
                FadeOut(self.h2_label),
                Create(self.timeline_axis),
                FadeIn(self.dot_m1),
                FadeIn(self.label_m1),
                run_time=3.26,
            )

        self.beat(
            3.26,
            0.81,
            sub_beat_15_1,
            "Horizontal timeline axis unrolls across base with MECHANICAL WORK milestone",
        )

        # Sub-beat 15.2: VectorArrow extends to 'LINEAR MOMENTUM (p)'
        self.arrow_t1 = Arrow(
            start=[-4.5, -2.5, 0],
            end=[-1.5, -2.5, 0],
            color=PALETTE["indigo"],
            stroke_width=3.5,
            buff=0.15,
        )
        self.dot_m2 = Dot([-1.5, -2.5, 0], radius=0.09, color=PALETTE["indigo"])
        self.label_m2 = Text(
            "LINEAR MOMENTUM (p)",
            font_size=16,
            color=PALETTE["indigo"],
            weight=BOLD,
        ).next_to(self.dot_m2, UP, buff=0.15)

        def sub_beat_15_2():
            self.play(
                GrowArrow(self.arrow_t1),
                FadeIn(self.dot_m2),
                FadeIn(self.label_m2),
                run_time=1.91,
            )

        self.beat(
            1.91,
            0.64,
            sub_beat_15_2,
            "Vector arrow extends along timeline to LINEAR MOMENTUM milestone",
        )

        # Sub-beat 15.3: Vector arcs over barrier tagged 'ACTIVATION THRESHOLD (E_a)'
        self.arc_t2 = CurvedArrow(
            start_point=[-1.5, -2.5, 0],
            end_point=[1.5, -2.5, 0],
            color=PALETTE["coral"],
            stroke_width=3.5,
        )
        self.dot_m3 = Dot([1.5, -2.5, 0], radius=0.09, color=PALETTE["coral"])
        self.label_m3 = Text(
            "ACTIVATION THRESHOLD (E_a)",
            font_size=16,
            color=PALETTE["coral"],
            weight=BOLD,
        ).next_to(self.dot_m3, UP, buff=0.15)

        def sub_beat_15_3():
            self.play(
                Create(self.arc_t2),
                FadeIn(self.dot_m3),
                FadeIn(self.label_m3),
                run_time=2.09,
            )

        self.beat(
            2.09,
            0.70,
            sub_beat_15_3,
            "Vector arcs over ACTIVATION THRESHOLD milestone",
        )

        # Sub-beat 15.4: Trajectory terminates in locked molecule icon tagged 'STABLE BOND'
        self.arrow_t3 = Arrow(
            start=[1.5, -2.5, 0],
            end=[4.5, -2.5, 0],
            color=PALETTE["mint"],
            stroke_width=3.5,
            buff=0.15,
        )
        self.dot_m4 = Dot([4.5, -2.5, 0], radius=0.09, color=PALETTE["mint"])
        self.label_m4 = Text(
            "STABLE BOND",
            font_size=16,
            color=PALETTE["mint"],
            weight=BOLD,
        ).next_to(self.dot_m4, UP, buff=0.15)

        def sub_beat_15_4():
            self.play(
                GrowArrow(self.arrow_t3),
                FadeIn(self.dot_m4),
                FadeIn(self.label_m4),
                run_time=3.72,
            )

        self.beat(
            3.72,
            0.93,
            sub_beat_15_4,
            "Timeline terminates in STABLE BOND icon completing transformation sequence",
        )

        # =========================================================
        # BEAT 16: Panoramic Grand Synthesis & Universal Conservation
        # =========================================================

        # Sub-beat 16.1: Master panoramic coordinate link between cart runway and molecule
        self.panoramic_axis = Line(
            start=[-6.2, 0.0, 0],
            end=[6.2, 0.0, 0],
            stroke_color=PALETTE["stroke_light"],
            stroke_width=1.5,
        )

        def sub_beat_16_1():
            self.play(
                Create(self.panoramic_axis),
                run_time=2.24,
            )

        self.beat(
            2.24,
            0.74,
            sub_beat_16_1,
            "Coordinate axis draws unbroken across master wide view linking regimes",
        )

        # Sub-beat 16.2: Continuous mint line threads through stage beneath 'ΔE_UNIVERSE = 0'
        self.universe_line = Line(
            start=[-6.5, 1.8, 0],
            end=[6.5, 1.8, 0],
            stroke_color=PALETTE["mint"],
            stroke_width=4.0,
        )
        self.universe_title = Text(
            "ΔE_UNIVERSE = 0",
            font_size=36,
            color=PALETTE["mint"],
            weight=BOLD,
        ).move_to([0, 2.45, 0])

        def sub_beat_16_2():
            self.play(
                Create(self.universe_line),
                FadeIn(self.universe_title, shift=DOWN * 0.2),
                run_time=3.28,
            )

        self.beat(
            3.28,
            0.82,
            sub_beat_16_2,
            "Continuous mint line anchors master closing conservation law ΔE_UNIVERSE = 0",
        )

        # ---------------------------------------------------------
        # FINAL RUNTIME VALIDATION
        # ---------------------------------------------------------
        self.finalize()
