"""Reusable, unboxed technical graphics for 2D explanatory scenes."""

import numpy as np
from manim import Arrow, Dot, DoubleArrow, Line, MathTex, Text, VGroup, UP, WHITE, GREY_B


class VectorArrow(Arrow):
    """Arrow with no automatic endpoint gap, suitable for vectors and flows."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("buff", 0)
        kwargs.setdefault("stroke_width", 3)
        super().__init__(*args, **kwargs)


class DirectLeaderLabel(VGroup):
    """A direct text label connected to a target by a leader line, never a card."""

    def __init__(
        self,
        text,
        target,
        direction=UP,
        buff=0.18,
        color=WHITE,
        line_color=GREY_B,
        font_size=20,
        math=False,
        show_anchor_dot=True,
        **kwargs,
    ):
        if hasattr(target, "get_center"):
            target_point = np.array(target.get_center(), dtype=float)
        else:
            target_point = np.array(target, dtype=float).flatten()
            if target_point.size == 2:
                target_point = np.array([target_point[0], target_point[1], 0.0])
            if target_point.size != 3:
                raise ValueError("target must be a 2D/3D point or a Manim mobject")

        label_cls = MathTex if math else Text
        label = label_cls(str(text), color=color, font_size=font_size, **kwargs)
        label.next_to(target_point, direction, buff=buff)
        leader = Line(
            target_point,
            label.get_edge_center(-direction),
            color=line_color,
            stroke_width=1.5,
        )
        members = [leader]
        anchor_dot = None
        if show_anchor_dot:
            anchor_dot = Dot(target_point, radius=0.035, color=line_color)
            members.append(anchor_dot)
        members.append(label)
        super().__init__(*members)
        self.label = label
        self.leader = leader
        self.anchor_dot = anchor_dot


class DimensionRuler(VGroup):
    """A dimension arrow with a readable label placed directly beside it."""

    def __init__(
        self,
        start,
        end,
        label,
        label_direction=UP,
        color=WHITE,
        font_size=18,
        buff=0.12,
    ):
        start_point = np.array(start, dtype=float)
        end_point = np.array(end, dtype=float)
        if start_point.size == 2:
            start_point = np.array([start_point[0], start_point[1], 0.0])
        if end_point.size == 2:
            end_point = np.array([end_point[0], end_point[1], 0.0])
        ruler = DoubleArrow(
            start_point,
            end_point,
            buff=0,
            color=color,
            stroke_width=1.8,
            max_tip_length_to_length_ratio=0.12,
        )
        label_mob = Text(str(label), color=color, font_size=font_size)
        label_mob.next_to((start_point + end_point) / 2, label_direction, buff=buff)
        super().__init__(ruler, label_mob)
        self.ruler = ruler
        self.label = label_mob
