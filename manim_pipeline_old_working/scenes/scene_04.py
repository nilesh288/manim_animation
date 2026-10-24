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


class Scene04(InfographicScene):
    target_duration = 38.88

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

        # Macroscopic colliding pair
        self.body_a = RigidDisc(
            radius=0.75,
            core_color=PALETTE["indigo"],
            is_hollow=False,
        ).move_to([-3.2, -0.25, 0])

        self.body_b = RigidDisc(
            radius=0.75,
            core_color=PALETTE["surface_card"],
            is_hollow=False,
        ).move_to([0.75, -0.25, 0])

        self.add(self.body_a, self.body_b)

        # =========================================================
        # BEAT 1: Inelastic Real-World Collision & Perimeter Buckling
        # =========================================================

        # Sub-beat 1.1: Realistic macroscopic bodies collide under imperfect contact
        def sub_beat_1_1():
            self.play(
                self.body_a.animate.move_to([-0.75, -0.25, 0]),
                run_time=1.69,
                rate_func=rate_functions.ease_in_quad,
            )

        self.beat(
            1.69,
            0.56,
            sub_beat_1_1,
            "Two macroscopic structural bodies collide on runway under imperfect contact",
        )

        # Sub-beat 1.2: Geometric perimeters buckle with microscopic asymmetric notches
        self.notch_lines = VGroup(*[
            Line(
                start=[-0.08, -0.25 + dy, 0],
                end=[0.08, -0.25 + dy + 0.05, 0],
                stroke_color=PALETTE["stroke"],
                stroke_width=3.0,
            )
            for dy in [-0.35, -0.15, 0.1, 0.3]
        ])

        def sub_beat_1_2():
            self.play(
                Create(self.notch_lines),
                run_time=1.75,
            )

        self.beat(
            1.75,
            0.58,
            sub_beat_1_2,
            "Contact boundary buckles with microscopic asymmetric strain notches",
        )

        # =========================================================
        # BEAT 2: Shockwave & Mechanical Energy Dissipation
        # =========================================================

        # Sub-beat 2.1: Violent mechanical shockwave ring radiates from interface
        self.shockwave = Circle(
            radius=0.2,
            color=PALETTE["coral"],
            stroke_width=5.0,
        ).move_to([0.0, -0.25, 0])

        def sub_beat_2_1():
            self.play(
                FadeOut(self.notch_lines),
                Create(self.shockwave),
                self.shockwave.animate.scale(4.5).set_stroke(opacity=0.0),
                run_time=1.78,
            )

        self.beat(
            1.78,
            0.60,
            sub_beat_2_1,
            "Violent mechanical shockwave radiates from collision contact interface",
        )

        # Sub-beat 2.2: Truncated exit velocity vector and ΔE_loss label deploy
        self.loss_label = Text(
            "ΔE_loss",
            font_size=28,
            color=PALETTE["coral"],
            weight=BOLD,
        ).move_to([0.0, 1.45, 0])

        self.exit_v = Arrow(
            start=[1.5, -0.25, 0],
            end=[2.4, -0.25, 0],
            color=PALETTE["blue"],
            buff=0,
            stroke_width=4.0,
        )

        def sub_beat_2_2():
            self.play(
                FadeIn(self.loss_label, shift=DOWN * 0.2),
                GrowArrow(self.exit_v),
                self.body_b.animate.shift(RIGHT * 0.4),
                run_time=3.26,
            )

        self.beat(
            3.26,
            0.82,
            sub_beat_2_2,
            "Exit velocity vector deploys noticeably shorter alongside ΔE_loss metric",
        )

        # =========================================================
        # BEAT 3: Material Interior & Lattice Stress Waves
        # =========================================================

        # Build interior lattice grid
        grid_rows, grid_cols = 3, 5
        x_coords = np.linspace(-3.0, 3.0, grid_cols)
        y_coords = np.linspace(-1.2, 0.8, grid_rows)

        lattice_nodes = []
        lattice_bonds = []
        for y in y_coords:
            for x in x_coords:
                lattice_nodes.append(
                    Dot(point=[x, y, 0], radius=0.10, color=PALETTE["indigo"])
                )

        for i in range(grid_rows):
            for j in range(grid_cols):
                idx = i * grid_cols + j
                if j < grid_cols - 1:
                    lattice_bonds.append(
                        Line(
                            [x_coords[j], y_coords[i], 0],
                            [x_coords[j + 1], y_coords[i], 0],
                            stroke_color=PALETTE["stroke_light"],
                            stroke_width=1.5,
                        )
                    )
                if i < grid_rows - 1:
                    lattice_bonds.append(
                        Line(
                            [x_coords[j], y_coords[i], 0],
                            [x_coords[j], y_coords[i + 1], 0],
                            stroke_color=PALETTE["stroke_light"],
                            stroke_width=1.5,
                        )
                    )

        self.lattice_group = VGroup(*lattice_bonds, *lattice_nodes)

        # Sub-beat 3.1: Camera pushes into material revealing lattice network
        def sub_beat_3_1():
            self.play(
                FadeOut(self.runway),
                FadeOut(self.ticks),
                FadeOut(self.body_a),
                FadeOut(self.body_b),
                FadeOut(self.exit_v),
                FadeOut(self.loss_label),
                FadeIn(self.lattice_group),
                run_time=2.51,
            )

        self.beat(
            2.51,
            0.84,
            sub_beat_3_1,
            "Push into material interior revealing interconnected atomic lattice network",
        )

        # Sub-beat 3.2: High-frequency stress ripples surge across lattice bonds
        stress_bonds = VGroup(*[
            b.copy().set_stroke(color=PALETTE["amber"], width=3.5)
            for b in lattice_bonds[:8]
        ])

        def sub_beat_3_2():
            self.play(
                Create(stress_bonds),
                run_time=2.10,
            )

        self.beat(
            2.10,
            0.70,
            sub_beat_3_2,
            "High-frequency stress ripples surge across lattice bonds",
        )

        # =========================================================
        # BEAT 4: Conservation Axiom & Protective Shield
        # =========================================================

        # Sub-beat 4.1: Constant energy metric E_total = const anchors in Zone 1
        self.e_const_label = Text(
            "E_total = const",
            font_size=30,
            color=PALETTE["text"],
            weight=BOLD,
        ).move_to([0.0, 2.7, 0])

        def sub_beat_4_1():
            self.play(
                FadeOut(stress_bonds),
                FadeIn(self.e_const_label, shift=DOWN * 0.2),
                run_time=0.48,
            )

        self.beat(
            0.48,
            0.35,
            sub_beat_4_1,
            "Anchor conservation axiom indicator E_total = const across upper stage",
        )

        # Sub-beat 4.2: Protective enclosing halo pulses with zero leakage
        self.boundary_halo = RoundedRectangle(
            corner_radius=0.4,
            width=7.2,
            height=3.0,
            stroke_color=PALETTE["mint"],
            stroke_width=2.5,
            fill_opacity=0.08,
            fill_color=PALETTE["mint"],
        ).move_to([0.0, -0.2, 0])

        def sub_beat_4_2():
            self.play(
                Create(self.boundary_halo),
                run_time=1.00,
            )

        self.beat(
            1.00,
            0.35,
            sub_beat_4_2,
            "Protective enclosing halo pulses outward showing zero system leakage",
        )

        # =========================================================
        # BEAT 5: Micro-Vector Shatter & Chaotic Oscillations
        # =========================================================

        # Sub-beat 5.1: Ordered forward vector shatters into micro-vectors
        primary_vector = Arrow(
            start=[-2.5, 1.4, 0],
            end=[0.5, 1.4, 0],
            color=PALETTE["blue"],
            buff=0,
            stroke_width=5.0,
        )
        micro_vectors = VGroup(*[
            Arrow(
                start=[x, y, 0],
                end=[x + 0.35 * np.cos(k), y + 0.35 * np.sin(k), 0],
                color=PALETTE["blue"],
                buff=0,
                stroke_width=2.2,
            )
            for k, (x, y) in enumerate(zip(x_coords[:3], y_coords[:3]))
        ])

        def sub_beat_5_1():
            self.play(
                FadeOut(self.e_const_label),
                FadeOut(self.boundary_halo),
                GrowArrow(primary_vector),
                run_time=0.55,
            )
            self.play(
                ReplacementTransform(primary_vector, micro_vectors),
                run_time=0.76,
            )

        self.beat(
            1.31,
            0.44,
            sub_beat_5_1,
            "Ordered forward vector shatters into micro-vectors across the grid",
        )

        # Sub-beat 5.2: Individual lattice nodes oscillate rapidly in jagged patterns
        def sub_beat_5_2():
            self.play(
                self.lattice_group.animate.shift(UP * 0.08 + RIGHT * 0.08),
                run_time=1.20,
            )
            self.play(
                self.lattice_group.animate.shift(DOWN * 0.08 + LEFT * 0.08),
                run_time=1.21,
            )

        self.beat(
            2.41,
            0.80,
            sub_beat_5_2,
            "Individual lattice nodes oscillate rapidly in random angular directions",
        )

        # =========================================================
        # BEAT 6: Ordered Rows to Frantic Thermal Scattering
        # =========================================================

        # Sub-beat 6.1: Structured row of atomic circles moves in unison
        atomic_row = VGroup(*[
            RigidDisc(radius=0.28, core_color=PALETTE["indigo"], is_hollow=False).move_to(
                [x, -0.2, 0]
            )
            for x in np.linspace(-3.6, 3.6, 5)
        ])
        uniform_vectors = VGroup(*[
            Arrow(
                start=[disc.get_center()[0], 0.3, 0],
                end=[disc.get_center()[0] + 0.8, 0.3, 0],
                color=PALETTE["indigo"],
                buff=0,
                stroke_width=3.5,
            )
            for disc in atomic_row
        ])
        self.atomic_system = VGroup(atomic_row, uniform_vectors)

        def sub_beat_6_1():
            self.play(
                FadeOut(micro_vectors),
                FadeOut(self.lattice_group),
                FadeIn(self.atomic_system),
                run_time=2.18,
            )

        self.beat(
            2.18,
            0.73,
            sub_beat_6_1,
            "Structured array of atomic circles moves initially in unison along parallel paths",
        )

        # Sub-beat 6.2: Aligned velocity arrows scatter into frantic multi-directional jiggles
        chaotic_arrows = VGroup(*[
            Arrow(
                start=[disc.get_center()[0], 0.3, 0],
                end=[
                    disc.get_center()[0] + 0.65 * np.cos(idx * 1.3),
                    0.3 + 0.65 * np.sin(idx * 1.3),
                    0,
                ],
                color=PALETTE["amber"] if idx % 2 == 0 else PALETTE["coral"],
                buff=0,
                stroke_width=3.5,
            )
            for idx, disc in enumerate(atomic_row)
        ])

        def sub_beat_6_2():
            self.play(
                ReplacementTransform(uniform_vectors, chaotic_arrows),
                run_time=2.46,
            )

        self.beat(
            2.46,
            0.82,
            sub_beat_6_2,
            "Velocity arrows scatter into frantic multi-directional thermal oscillations",
        )

        # =========================================================
        # BEAT 7: Macro Decay & Thermal Energy Conversion
        # =========================================================

        # Sub-beat 7.1: Single bold translational track line fades out
        self.macro_track = Line(
            start=[-4.5, -0.9, 0],
            end=[4.5, -0.9, 0],
            stroke_color=PALETTE["stroke"],
            stroke_width=3.0,
        )

        def sub_beat_7_1():
            self.play(
                FadeIn(self.macro_track),
                self.macro_track.animate.set_stroke(opacity=0.0),
                run_time=0.77,
            )

        self.beat(
            0.77,
            0.35,
            sub_beat_7_1,
            "Single bold translational track fades out symbolizing macro loss",
        )

        # Sub-beat 7.2: Warm thermal field diffuses with label 'THERMAL ENERGY'
        self.thermal_field = RoundedRectangle(
            corner_radius=0.5,
            width=8.5,
            height=2.8,
            fill_color=PALETTE["amber"],
            fill_opacity=0.16,
            stroke_color=PALETTE["amber"],
            stroke_width=1.5,
        ).move_to([0.0, -0.2, 0])

        self.thermal_label = Text(
            "THERMAL ENERGY",
            font_size=32,
            color=PALETTE["amber"],
            weight=BOLD,
        ).move_to([0.0, 1.8, 0])

        def sub_beat_7_2():
            self.play(
                FadeOut(chaotic_arrows),
                FadeIn(self.thermal_field),
                FadeIn(self.thermal_label, shift=DOWN * 0.2),
                run_time=1.28,
            )

        self.beat(
            1.28,
            0.42,
            sub_beat_7_2,
            "Warm thermal field diffuses across matrix with unboxed THERMAL ENERGY typography",
        )

        # =========================================================
        # BEAT 8: Peripheral Evacuation & Deep Atomic Zoom
        # =========================================================

        # Sub-beat 8.1: Background particles gently drift outward clearing center
        def sub_beat_8_1():
            self.play(
                FadeOut(self.thermal_field),
                FadeOut(self.thermal_label),
                atomic_row[0].animate.shift(LEFT * 2.5),
                atomic_row[1].animate.shift(LEFT * 1.5),
                atomic_row[3].animate.shift(RIGHT * 1.5),
                atomic_row[4].animate.shift(RIGHT * 2.5),
                run_time=2.00,
            )

        self.beat(
            2.00,
            0.66,
            sub_beat_8_1,
            "Peripheral vibrating particles drift outward clearing the central stage",
        )

        # Sub-beat 8.2: Dive into central node expanding it into orbital sphere
        self.orbital_sphere = Circle(
            radius=2.0,
            color=PALETTE["indigo"],
            stroke_width=2.5,
        ).move_to([0.0, 0.0, 0])

        self.nucleus_core = Dot(
            point=[0.0, 0.0, 0],
            radius=0.22,
            color=PALETTE["coral"],
        )

        def sub_beat_8_2():
            self.play(
                FadeOut(atomic_row[0]),
                FadeOut(atomic_row[1]),
                FadeOut(atomic_row[3]),
                FadeOut(atomic_row[4]),
                ReplacementTransform(atomic_row[2], self.nucleus_core),
                Create(self.orbital_sphere),
                run_time=2.16,
            )

        self.beat(
            2.16,
            0.72,
            sub_beat_8_2,
            "Deep zoom into central node expanding into an orbital sphere",
        )

        # ---------------------------------------------------------
        # FINAL RUNTIME VALIDATION
        # ---------------------------------------------------------
        self.finalize()
