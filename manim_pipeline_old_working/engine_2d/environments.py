"""
engine_2d/environments.py
The 4 Universal Spatial Environments for technical infographics.
"""
from manim import *
import numpy as np
from .theme import PALETTE


class SurfaceGround(VGroup):
    """Ground plane with baseline, depth shading, and tick marks for physics/mechanics."""
    def __init__(self, ground_y=-2.0, color=None, **kwargs):
        super().__init__(**kwargs)
        col = color or PALETTE["stroke_light"]
        
        self.line = Line(LEFT * 6.5 + UP * ground_y, RIGHT * 6.5 + UP * ground_y, color=col, stroke_width=2.0)
        self.shading = Polygon(
            LEFT * 6.5 + UP * ground_y,
            RIGHT * 6.5 + UP * ground_y,
            RIGHT * 6.5 + DOWN * 4.0,
            LEFT * 6.5 + DOWN * 4.0,
            color=PALETTE["bg_subtle"],
            fill_color=PALETTE["bg_subtle"],
            fill_opacity=0.7,
            stroke_width=0
        ).set_z_index(-1)
        
        # Subtle measurement tick marks
        ticks = VGroup()
        for x in np.linspace(-6.0, 6.0, 13):
            ticks.add(Line(UP * ground_y + RIGHT * x, UP * (ground_y - 0.12) + RIGHT * x, color=col, stroke_width=1.2))
            
        self.add(self.shading, self.line, ticks)
        self.ground_y = ground_y


class MacroHorizon(VGroup):
    """Curved planetary horizon with atmospheric boundary arc for space/telecom."""
    def __init__(self, center=DOWN * 6.5 + LEFT * 3.5, surface_radius=5.2, atmo_radius=6.6, **kwargs):
        super().__init__(**kwargs)
        self.center = center
        
        self.surface = Arc(
            radius=surface_radius, start_angle=0.15, angle=1.25,
            arc_center=center, color=PALETTE["stroke_light"], stroke_width=2.5
        )
        self.atmo = Arc(
            radius=atmo_radius, start_angle=0.18, angle=1.15,
            arc_center=center, color=PALETTE["blue"], stroke_width=1.5
        ).set_stroke(opacity=0.45)
        
        self.surface_fill = Sector(
            radius=surface_radius - 0.05, start_angle=0.15, angle=1.25,
            arc_center=center, color=PALETTE["bg_subtle"], fill_opacity=0.6, stroke_width=0
        ).set_z_index(-1)
        
        self.add(self.surface_fill, self.surface, self.atmo)


class ParticleField(VGroup):
    """Concentric lattice rings for nuclear, chemical, and microscopic phenomena."""
    def __init__(self, center=ORIGIN, radii=(1.4, 2.4, 3.4), **kwargs):
        super().__init__(**kwargs)
        for r in radii:
            self.add(Circle(radius=r, arc_center=center, color=PALETTE["stroke_muted"], stroke_width=1.2).set_z_index(-1))


class FlowAxes(VGroup):
    """Clean Cartesian coordinate frame for algorithms, metrics, and trends."""
    def __init__(self, x_length=7.0, y_length=4.5, x_range=[0, 10, 2], y_range=[0, 10, 2], **kwargs):
        super().__init__(**kwargs)
        self.axes = Axes(
            x_range=x_range, y_range=y_range,
            x_length=x_length, y_length=y_length,
            axis_config={"color": PALETTE["stroke_light"], "stroke_width": 1.8},
            tips=False
        ).shift(DOWN * 0.4 + LEFT * 0.5)
        self.add(self.axes)
