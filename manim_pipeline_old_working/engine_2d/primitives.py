"""
engine_2d/primitives.py
Universal 2D infographic primitives: leaders, rulers, emitters, conduits, and vectors.
"""
from manim import *
import numpy as np
from .theme import PALETTE, FONTS


class LeaderCallout(VGroup):
    """Clean technical callout with an angled leader line (no background card)."""
    def __init__(self, target_point, title, subtitle=None, direction=UP+RIGHT, length=1.2, **kwargs):
        super().__init__(**kwargs)
        color = PALETTE["stroke_light"]
        
        elbow_start = target_point
        elbow_mid = target_point + direction * 0.6
        elbow_end = elbow_mid + (RIGHT if direction[0] >= 0 else LEFT) * length
        
        line = VMobject(color=color, stroke_width=1.5)
        line.set_points_as_corners([elbow_start, elbow_mid, elbow_end])
        dot = Dot(target_point, radius=0.04, color=color)
        
        t_label = Text(title, font=FONTS["label"], font_size=13, color=PALETTE["text"])
        t_label.next_to(elbow_end, UP, buff=0.08, aligned_edge=LEFT if direction[0] >= 0 else RIGHT)
        
        self.add(dot, line, t_label)
        
        if subtitle:
            sub = Text(subtitle, font=FONTS["mono"], font_size=10, color=PALETTE["text_dim"])
            sub.next_to(elbow_end, DOWN, buff=0.08, aligned_edge=LEFT if direction[0] >= 0 else RIGHT)
            self.add(sub)


class DimensionRuler(VGroup):
    """Dynamic measurement line with parallel rotated metric label."""
    def __init__(self, start, end, label_text, color=None, buff=0.2, **kwargs):
        super().__init__(**kwargs)
        col = color or PALETTE["amber"]
        
        self.line = DashedLine(start, end, buff=buff, stroke_width=1.6, dash_length=0.12, color=col)
        self.label = Text(label_text, font=FONTS["mono"], font_size=14, color=col)
        
        self.label.next_to(self.line.get_center(), UP, buff=0.12)
        angle = self.line.get_angle()
        if angle > PI / 2 or angle < -PI / 2:
            angle += PI
        self.label.rotate(angle, about_point=self.label.get_center())
        
        self.add(self.line, self.label)


class VectorArrow(VGroup):
    """Directional force, trend, or velocity vector with an inline label."""
    def __init__(self, start, end, label=None, color=None, **kwargs):
        super().__init__(**kwargs)
        col = color or PALETTE["coral"]
        self.arrow = Arrow(start, end, buff=0, stroke_width=2.5, max_tip_length_to_length_ratio=0.25, color=col)
        self.add(self.arrow)
        if label:
            t = Text(label, font=FONTS["mono"], font_size=13, color=col)
            t.next_to(self.arrow.get_center(), RIGHT, buff=0.15)
            self.add(t)


class WaveEmitter:
    @staticmethod
    def create_burst(center, count=3, max_radius=3.5, color=None, run_time=1.2):
        col = color or PALETTE["indigo"]
        waves = VGroup(*[
            Circle(radius=0.1, arc_center=center, color=col, stroke_width=2.0)
            for _ in range(count)
        ])
        return LaggedStart(
            *[
                w.animate(rate_func=rate_functions.ease_out_quad)
                 .set_stroke(opacity=0)
                 .scale(max_radius * 10)
                for w in waves
            ],
            lag_ratio=0.3,
            run_time=run_time
        )


class PulseReticle:
    @staticmethod
    def create_burst(center, color=None, run_time=1.0):
        col = color or PALETTE["coral"]
        ring = Circle(radius=0.15, arc_center=center, color=col, stroke_width=2.0)
        return ring.animate(rate_func=rate_functions.ease_out_cubic, run_time=run_time).scale(4.0).set_stroke(opacity=0)
