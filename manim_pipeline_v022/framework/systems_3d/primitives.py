"""Small, explicit helpers for world-space and screen-space 3D annotations."""

import numpy as np
from manim import Line, MathTex, Text, UP, LEFT, WHITE, GREY_B


def _point3(point):
    result = np.array(point, dtype=float).flatten()
    if result.size == 2:
        return np.array([result[0], result[1], 0.0])
    if result.size != 3:
        raise ValueError("point must contain two or three coordinates")
    return result


def world_label(
    scene,
    text,
    point,
    direction=UP,
    buff=0.18,
    color=WHITE,
    font_size=20,
    math=False,
):
    """Place a camera-facing label at a point in 3D world space."""
    label_cls = MathTex if math else Text
    label = label_cls(str(text), color=color, font_size=font_size)
    position = _point3(point) + _point3(direction) * float(buff)
    label.move_to(position)
    scene.add_world_labels(label)
    return label


def hud_label(
    scene,
    text,
    position=UP * 3.2 + LEFT * 5.0,
    color=WHITE,
    font_size=18,
    math=False,
):
    """Place a label in screen space so it does not rotate with the 3D world."""
    label_cls = MathTex if math else Text
    label = label_cls(str(text), color=color, font_size=font_size)
    label.move_to(position)
    scene.add_hud(label)
    return label


def leader_line_3d(start, end, color=GREY_B, stroke_width=1.8):
    """Create a simple 3D-space leader line between two 3D points."""
    return Line(
        _point3(start),
        _point3(end),
        color=color,
        stroke_width=stroke_width,
    )
