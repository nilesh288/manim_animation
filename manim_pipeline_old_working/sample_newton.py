"""
sample_newton.py - Editorial Infographic Scene: Newton & The Apple Tree
10-Second synchronized demonstration with clean vector illustration.
"""
from manim import *
import numpy as np

# Editorial Pastel Palette
PALETTE = {
    "bg": "#F8F9FA",           # Warm off-white
    "stroke": "#2D3748",       # Deep slate charcoal
    "stroke_light": "#CBD5E0", # Subtle gray for grid / leaders
    "text": "#1A202C",         # Slate black
    "text_dim": "#718096",     # Muted caption gray
    "mint": "#48BB78",         # Tree foliage (pastel green)
    "mint_dark": "#2F855A",    # Foliage stroke
    "wood": "#718096",         # Minimalist trunk / branches
    "coral": "#E53E3E",        # Apple / force vector
    "amber": "#ED8936",        # Measurement ruler / insight
    "indigo": "#5A67D8",       # Newton's notebook / accents
}


class StickmanNewton(VGroup):
    """Minimalist, clean vector stick figure sitting under the tree."""
    def __init__(self, position=ORIGIN, **kwargs):
        super().__init__(**kwargs)
        col = PALETTE["stroke"]

        # 1. Head (tilted slightly up in thought)
        head = Circle(radius=0.18, color=col, stroke_width=2.5, fill_color=PALETTE["bg"], fill_opacity=1)
        head.move_to(position + UP * 0.95 + RIGHT * 0.05)

        # 2. Torso (leaning comfortably against the trunk)
        spine_top = head.get_bottom()
        hip = position + DOWN * 0.05
        spine = Line(spine_top, hip, stroke_width=2.8, color=col)

        # 3. Seated Legs
        # Thighs extending forward, knees raised slightly
        knee = position + RIGHT * 0.5 + UP * 0.25
        foot = position + RIGHT * 0.9 + DOWN * 0.05
        leg = VMobject(color=col, stroke_width=2.6)
        leg.set_points_as_corners([hip, knee, foot])

        # 4. Arms holding a small open notebook in lap
        shoulder = spine_top + DOWN * 0.18
        hand = position + RIGHT * 0.35 + UP * 0.15
        arm = VMobject(color=col, stroke_width=2.4)
        arm.set_points_as_corners([shoulder, hand])

        # Small notebook in hands
        book = Rectangle(width=0.28, height=0.18, color=PALETTE["indigo"], fill_color=PALETTE["indigo"], fill_opacity=0.3, stroke_width=1.5)
        book.move_to(hand + RIGHT * 0.05).rotate(0.2)

        self.add(spine, leg, arm, book, head)
        self.head = head


class InfographicTree(VGroup):
    """Editorial vector tree with organic pastel canopy and branches."""
    def __init__(self, position=ORIGIN, **kwargs):
        super().__init__(**kwargs)
        wood_col = PALETTE["wood"]
        leaf_fill = PALETTE["mint"]
        leaf_stroke = PALETTE["mint_dark"]

        # 1. Curved Trunk (minimalist tapered strokes)
        trunk_path = VMobject(color=wood_col, stroke_width=5.0)
        trunk_path.set_points_smoothly([
            position + DOWN * 0.05,
            position + UP * 0.8 + RIGHT * 0.1,
            position + UP * 1.8 + LEFT * 0.1,
            position + UP * 2.6 + RIGHT * 0.2,
        ])

        # Branches reaching into canopy
        branch_r = VMobject(color=wood_col, stroke_width=3.0)
        branch_r.set_points_smoothly([
            position + UP * 1.8 + LEFT * 0.1,
            position + UP * 2.2 + RIGHT * 0.8,
            position + UP * 2.4 + RIGHT * 1.4,
        ])

        branch_l = VMobject(color=wood_col, stroke_width=3.0)
        branch_l.set_points_smoothly([
            position + UP * 1.9,
            position + UP * 2.3 + LEFT * 0.7,
        ])

        # 2. Layered Cloud-like Foliage Canopies
        c1 = Circle(radius=1.1, color=leaf_stroke, fill_color=leaf_fill, fill_opacity=0.35, stroke_width=1.5).move_to(position + UP * 2.8 + LEFT * 0.3)
        c2 = Circle(radius=0.9, color=leaf_stroke, fill_color=leaf_fill, fill_opacity=0.35, stroke_width=1.5).move_to(position + UP * 2.6 + RIGHT * 0.8)
        c3 = Circle(radius=0.8, color=leaf_stroke, fill_color=leaf_fill, fill_opacity=0.35, stroke_width=1.5).move_to(position + UP * 2.3 + LEFT * 0.9)
        c4 = Circle(radius=1.0, color=leaf_stroke, fill_color=leaf_fill, fill_opacity=0.45, stroke_width=1.5).move_to(position + UP * 3.3 + RIGHT * 0.2)

        foliage = VGroup(c1, c2, c3, c4)

        # 3. Passive Apples hanging in the tree
        app1 = Dot(position + UP * 2.7 + LEFT * 0.5, radius=0.07, color=PALETTE["coral"])
        app2 = Dot(position + UP * 2.9 + RIGHT * 0.9, radius=0.07, color=PALETTE["coral"])

        self.add(trunk_path, branch_l, branch_r, foliage, app1, app2)
        self.branch_tip = position + UP * 2.4 + RIGHT * 1.4


class NewtonAppleScene(Scene):
    def construct(self):
        self.camera.background_color = PALETTE["bg"]

        # ---------------------------------------------------------
        # Spatial Geometry & Actors
        # ---------------------------------------------------------
        ground_y = -1.8
        tree_x = -2.4

        # 1. Ground Horizon (Clean line with subtle tick marks)
        ground = Line(LEFT * 6.5 + UP * ground_y, RIGHT * 6.5 + UP * ground_y, color=PALETTE["stroke_light"], stroke_width=2.0)
        grass_shading = Polygon(
            LEFT * 6.5 + UP * ground_y,
            RIGHT * 6.5 + UP * ground_y,
            RIGHT * 6.5 + DOWN * 4.0,
            LEFT * 6.5 + DOWN * 4.0,
            color="#EDF2F7",
            fill_color="#EDF2F7",
            fill_opacity=0.7,
            stroke_width=0
        ).set_z_index(-1)

        # 2. Tree & Newton
        tree = InfographicTree(position=RIGHT * tree_x + UP * ground_y)
        newton = StickmanNewton(position=RIGHT * (tree_x + 0.45) + UP * ground_y)

        # 3. The Target Falling Apple (With tiny stem and leaf)
        apple_start = tree.branch_tip + DOWN * 0.15
        apple_core = Circle(radius=0.13, color=PALETTE["coral"], fill_color=PALETTE["coral"], fill_opacity=0.9, stroke_width=1.5)
        apple_stem = Line(apple_core.get_top(), apple_core.get_top() + UP * 0.08 + RIGHT * 0.03, stroke_width=1.5, color=PALETTE["stroke"])
        apple = VGroup(apple_core, apple_stem).move_to(apple_start)

        # 4. Callout annotations
        # Apple label
        elbow_start = apple_start + RIGHT * 0.15
        elbow_mid = elbow_start + RIGHT * 0.6 + UP * 0.4
        elbow_end = elbow_mid + RIGHT * 0.8
        callout_path = VMobject(color=PALETTE["stroke_light"], stroke_width=1.4)
        callout_path.set_points_as_corners([elbow_start, elbow_mid, elbow_end])
        apple_tag = Text("APPLE // MASS m", font="sans-serif", font_size=12, color=PALETTE["text"]).next_to(elbow_end, UP, buff=0.06, aligned_edge=LEFT)
        state_tag = Text("STATUS: EQUILIBRIUM", font="monospace", font_size=10, color=PALETTE["text_dim"]).next_to(elbow_end, DOWN, buff=0.06, aligned_edge=LEFT)
        apple_callout = VGroup(callout_path, apple_tag, state_tag)

        # ---------------------------------------------------------
        # BEAT 1: Establish Newton & Apple Tree (Duration: 3.20s)
        # Motion: 1.20s | Hold: 2.00s
        # ---------------------------------------------------------
        self.play(
            FadeIn(grass_shading, run_time=0.8),
            Create(ground, run_time=1.0),
            FadeIn(tree, shift=UP * 0.2, run_time=1.2),
            FadeIn(newton, run_time=1.0),
            FadeIn(apple, scale=0.5, run_time=0.8),
            Write(apple_callout, run_time=0.9),
        )
        self.wait(2.00)

        # ---------------------------------------------------------
        # BEAT 2: Gravitational Force Resolves (Duration: 3.30s)
        # Motion: 1.20s | Hold: 2.10s
        # ---------------------------------------------------------
        # Force vector pulling straight down
        force_arrow = Arrow(
            apple_start + DOWN * 0.2,
            apple_start + DOWN * 1.4,
            buff=0,
            stroke_width=2.6,
            max_tip_length_to_length_ratio=0.25,
            color=PALETTE["coral"]
        )
        force_label = Text("F_g = m · g", font="monospace", font_size=13, color=PALETTE["coral"]).next_to(force_arrow, RIGHT, buff=0.12)

        # Dimension ruler for height h
        h_line = DashedLine(
            RIGHT * 1.2 + UP * apple_start[1],
            RIGHT * 1.2 + UP * ground_y,
            stroke_width=1.4,
            dash_length=0.12,
            color=PALETTE["amber"]
        )
        h_label = Text("h = 3.2 m", font="monospace", font_size=12, color=PALETTE["amber"]).next_to(h_line, RIGHT, buff=0.12)

        self.play(
            FadeOut(apple_callout, run_time=0.4),
            Create(force_arrow, run_time=0.9),
            Write(force_label, run_time=0.8),
            Create(h_line, run_time=0.9),
            Write(h_label, run_time=0.8),
        )
        self.wait(2.10)

        # ---------------------------------------------------------
        # BEAT 3: Natural Acceleration Drop (Duration: 3.50s)
        # Motion: 1.20s | Hold: 2.30s
        # ---------------------------------------------------------
        apple_land_pos = [apple_start[0], ground_y + 0.13, 0]

        # Impact ripple on ground
        impact_ripple = Circle(radius=0.1, arc_center=apple_land_pos, color=PALETTE["coral"], stroke_width=2.0)

        # "Insight spark" icon above Newton's head
        spark = Star(n=4, outer_radius=0.22, inner_radius=0.08, color=PALETTE["amber"], fill_color=PALETTE["amber"], fill_opacity=0.8)
        spark.next_to(newton.head, UP + RIGHT * 0.5, buff=0.15)

        self.play(
            FadeOut(force_arrow, force_label, run_time=0.3),
            # Downward motion uses quadratic easing (y = 0.5 * g * t^2)
            apple.animate(rate_func=rate_functions.ease_in_quad, run_time=1.1).move_to(apple_land_pos),
        )
        self.play(
            impact_ripple.animate(run_time=0.8).scale(3.5).set_stroke(opacity=0),
            FadeIn(spark, scale=0.5, run_time=0.6),
        )
        self.wait(2.30)
