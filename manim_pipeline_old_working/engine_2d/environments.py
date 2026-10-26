"""
engine_2d/environments.py
Universal Spatial Environments for technical infographics and system visualizations.
Tuned for the Kurzgesagt Editorial aesthetic (warm eggshell canvas, bold charcoal contours).
"""
from manim import *
import numpy as np
from .theme import PALETTE


class SurfaceGround(VGroup):
    """Calibrated bedrock runway for mechanical tracks, physics baselines, and robotics."""
    def __init__(self, ground_y: float = None, y_pos: float = None, width: float = 15.0, color=None, **kwargs):
        super().__init__(**kwargs)
        gy = ground_y if ground_y is not None else (y_pos if y_pos is not None else -1.2)
        col = color or PALETTE["stroke"]
        w = width or 15.0

        self.line = Line([-w / 2, gy, 0], [w / 2, gy, 0], color=col, stroke_width=3.6)
        self.shading = Rectangle(
            width=w,
            height=3.0,
            color=PALETTE["surface_ground"],
            fill_color=PALETTE["surface_ground"],
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0.0, gy - 1.5, 0.0])

        ticks = VGroup()
        for x in np.linspace(-w / 2 + 0.5, w / 2 - 0.5, 15):
            ticks.add(
                Line([x, gy, 0], [x, gy - 0.16, 0], color=PALETTE["stroke_light"], stroke_width=1.6)
            )

        self.add(self.shading, self.line, ticks)
        self.ground_y = gy


class MacroHorizon(VGroup):
    """Planetary curvature and atmospheric horizon for aerospace, telecom, and global cloud systems."""
    def __init__(
        self,
        center=DOWN * 7.2 + LEFT * 1.5,
        surface_radius: float = 5.6,
        atmo_radius: float = 6.8,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.surface = Arc(
            radius=surface_radius,
            start_angle=0.15,
            angle=1.25,
            arc_center=center,
            color=PALETTE["stroke"],
            stroke_width=3.6,
        )
        self.atmo = Arc(
            radius=atmo_radius,
            start_angle=0.18,
            angle=1.15,
            arc_center=center,
            color=PALETTE["sky"],
            stroke_width=2.6,
        ).set_stroke(opacity=0.75)

        self.surface_fill = Sector(
            radius=surface_radius - 0.05,
            start_angle=0.15,
            angle=1.25,
            arc_center=center,
            color=PALETTE["surface_ground"],
            fill_color=PALETTE["surface_ground"],
            fill_opacity=1.0,
            stroke_width=0,
        ).set_z_index(-1)

        self.add(self.surface_fill, self.surface, self.atmo)


class ParticleField(VGroup):
    """Concentric lattice rings for semiconductor physics, quantum states, and cryptographic rings."""
    def __init__(self, center=ORIGIN, radii=(1.4, 2.5, 3.6), **kwargs):
        super().__init__(**kwargs)
        for r in radii:
            self.add(
                Circle(
                    radius=r,
                    arc_center=center,
                    color=PALETTE["stroke_muted"],
                    stroke_width=1.6,
                ).set_z_index(-1)
            )


class FlowAxes(VGroup):
    """Clean Cartesian coordinate frame for performance benchmarks, latency curves, and data trends."""
    def __init__(
        self,
        x_length: float = 7.2,
        y_length: float = 4.2,
        x_range=(0, 10, 2),
        y_range=(0, 10, 2),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.axes = Axes(
            x_range=list(x_range),
            y_range=list(y_range),
            x_length=x_length,
            y_length=y_length,
            axis_config={"color": PALETTE["stroke_light"], "stroke_width": 2.2},
            tips=False,
        ).shift(DOWN * 0.4 + LEFT * 0.4)
        self.add(self.axes)


class TechGrid(VGroup):
    """Matrix dot-grid backdrop for systems architecture, chip layouts, and neural networks."""
    def __init__(
        self,
        x_range=(-6.5, 6.5, 1.0),
        y_range=(-3.2, 3.2, 1.0),
        dot_radius: float = 0.03,
        color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        col = color or PALETTE["stroke_muted"]
        xs = np.arange(x_range[0], x_range[1] + 0.1, x_range[2])
        ys = np.arange(y_range[0], y_range[1] + 0.1, y_range[2])
        dots = VGroup(*[
            Dot([x, y, 0], radius=dot_radius, color=col).set_opacity(0.55)
            for x in xs
            for y in ys
        ]).set_z_index(-2)
        self.add(dots)


__all__ = [
    "SurfaceGround",
    "MacroHorizon",
    "ParticleField",
    "FlowAxes",
    "TechGrid",
]
