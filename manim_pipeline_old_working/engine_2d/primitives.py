"""
engine_2d/primitives.py
Universal 2D infographic primitives for broadcast-quality technical animation:
leaders, rulers, vectors, particle streams, tech nodes, pipeline stages, and reticles.
Features dynamic auto-tracking for moving actors and Kurzgesagt Editorial vector styling.
"""
from manim import *
import numpy as np
from .theme import PALETTE, FONTS


# =====================================================================
# 1. ANNOTATION & TELEMETRY PRIMITIVES
# =====================================================================
class AttachedLabel(Text):
    """
    Dynamic label that automatically locks to and follows a moving target mobject
    without requiring manual coordinate keyframing.
    """
    def __init__(
        self,
        target_mobject,
        text: str,
        direction=UP,
        buff: float = 0.18,
        color=None,
        font_size: int = 12,
        weight=BOLD,
        font=FONTS["sans"],
        **kwargs
    ):
        col = color or PALETTE["text"]
        super().__init__(text, font=font, weight=weight, font_size=font_size, color=col, **kwargs)
        self.tracked_target = target_mobject
        self.direction = direction
        self.buff = buff
        self.next_to(self.tracked_target, self.direction, buff=self.buff)
        self.add_updater(lambda m: getattr(m, "tracked_target", None) is not None and m.next_to(m.tracked_target, m.direction, buff=m.buff))


class LeaderCallout(VGroup):
    """
    Clean technical callout with an angled leader line, dot anchor,
    bold headline, and monospace metadata subtitle.
    Features automatic screen-margin clamping/flipping to prevent off-screen truncation,
    and optional auto-tracking for moving targets.
    """
    def __init__(
        self,
        target_point_or_mob,
        title: str,
        subtitle: str = None,
        direction=UP + RIGHT,
        length: float = 1.2,
        color=None,
        auto_track: bool = False,
        **kwargs
    ):
        # Resilient parameter alias resolution
        direction = kwargs.pop("leader_dir", kwargs.pop("dir", direction))
        length = kwargs.pop("arm_length", kwargs.pop("arm", length))
        
        super().__init__(**kwargs)
        self.stroke_col = color or PALETTE["stroke"]
        self.accent_col = PALETTE["coral"]
        self.norm_dir = normalize(np.array(direction, dtype=float))
        self.length = length
        self.title_text = title
        self.sub_text = subtitle
        self.target_mob = None

        if isinstance(target_point_or_mob, (Mobject, VGroup)):
            self.target_mob = target_point_or_mob
            if self.norm_dir[1] > 0.3:
                self.target_pt = target_point_or_mob.get_top()
            elif self.norm_dir[1] < -0.3:
                self.target_pt = target_point_or_mob.get_bottom()
            elif self.norm_dir[0] > 0:
                self.target_pt = target_point_or_mob.get_right()
            else:
                self.target_pt = target_point_or_mob.get_left()
        else:
            self.target_pt = np.array(target_point_or_mob, dtype=float)

        self._build()

        if auto_track and self.target_mob is not None:
            self.add_updater(lambda mob: mob._update_position())

    def _build(self):
        self.submobjects.clear()
        elbow_pt = self.target_pt + self.norm_dir * 0.70
        is_right = self.norm_dir[0] >= 0

        # Boundary guard: flip leader arm if close to camera edge
        if is_right and (elbow_pt[0] + self.length > 5.0):
            is_right = False
        elif not is_right and (elbow_pt[0] - self.length < -5.0):
            is_right = True

        end_pt = elbow_pt + (RIGHT if is_right else LEFT) * self.length

        self.anchor_dot = Dot(self.target_pt, radius=0.07, color=self.accent_col)
        self.leader_line = VMobject(color=self.stroke_col, stroke_width=2.8)
        self.leader_line.set_points_as_corners([self.target_pt, elbow_pt, end_pt])

        self.title_mob = Text(
            self.title_text,
            font=FONTS["sans"],
            weight=BOLD,
            font_size=14,
            color=PALETTE["text"],
        )
        self.title_mob.next_to(
            end_pt,
            UP,
            buff=0.09,
            aligned_edge=LEFT if is_right else RIGHT,
        )

        self.add(self.anchor_dot, self.leader_line, self.title_mob)

        if self.sub_text:
            self.sub_mob = Text(
                self.sub_text,
                font=FONTS["mono"],
                weight=BOLD,
                font_size=10,
                color=PALETTE["text_dim"],
            )
            self.sub_mob.next_to(
                end_pt,
                DOWN,
                buff=0.08,
                aligned_edge=LEFT if is_right else RIGHT,
            )
            self.add(self.sub_mob)

    def _update_position(self):
        if self.target_mob is None:
            return
        if self.norm_dir[1] > 0.3:
            self.target_pt = self.target_mob.get_top()
        elif self.norm_dir[1] < -0.3:
            self.target_pt = self.target_mob.get_bottom()
        elif self.norm_dir[0] > 0:
            self.target_pt = self.target_mob.get_right()
        else:
            self.target_pt = self.target_mob.get_left()
        self._build()


class DimensionRuler(VGroup):
    """
    Dynamic engineering measurement line with orthogonal boundary ticks
    and a parallel rotated metric label.
    """
    def __init__(
        self,
        start_point_or_mob,
        end_point_or_mob,
        label: str,
        color=None,
        buff: float = 0.15,
        offset: float = 0.0,
        **kwargs
    ):
        offset = kwargs.pop("offset", offset)
        super().__init__(**kwargs)
        col = color or PALETTE["amber"]

        start = start_point_or_mob.get_center() if isinstance(start_point_or_mob, Mobject) else np.array(start_point_or_mob, dtype=float)
        end = end_point_or_mob.get_center() if isinstance(end_point_or_mob, Mobject) else np.array(end_point_or_mob, dtype=float)
        dist = np.linalg.norm(end - start)

        if dist < 0.35:
            return  # Suppress degenerate microscopic rulers

        if abs(offset) > 1e-4 and dist > 1e-4:
            unit_dir = (end - start) / dist
            perp_dir = np.array([-unit_dir[1], unit_dir[0], 0.0])
            start = start + perp_dir * offset
            end = end + perp_dir * offset

        main_line = DashedLine(
            start,
            end,
            buff=buff,
            stroke_width=2.6,
            dash_length=0.12,
            color=col,
        )

        direction = normalize(end - start)
        normal = rotate_vector(direction, PI / 2) * 0.16
        cap_start = Line(start - normal, start + normal, color=col, stroke_width=2.6)
        cap_end = Line(end - normal, end + normal, color=col, stroke_width=2.6)

        tag = Text(label, font=FONTS["mono"], weight=BOLD, font_size=13, color=col)
        tag.next_to(main_line.get_center(), UP, buff=0.14)

        angle = np.arctan2(direction[1], direction[0])
        if angle > PI / 2 or angle < -PI / 2:
            angle += PI
        tag.rotate(angle, about_point=tag.get_center())

        self.add(main_line, cap_start, cap_end, tag)


class VectorArrow(VGroup):
    """High-contrast directional vector for velocities, forces, signals, and trends."""
    def __init__(
        self,
        start_point,
        end_point,
        label: str = None,
        color=None,
        stroke_width: float = 3.6,
        **kwargs
    ):
        super().__init__(**kwargs)
        col = color or PALETTE["sky"]
        self.arrow = Arrow(
            start_point,
            end_point,
            buff=0,
            stroke_width=stroke_width,
            max_tip_length_to_length_ratio=0.28,
            color=col,
        )
        self.add(self.arrow)

        if label:
            tag = Text(label, font=FONTS["mono"], weight=BOLD, font_size=13, color=col)
            tag.next_to(self.arrow.get_center(), UP, buff=0.14)
            self.add(tag)


# =====================================================================
# 2. PARTICLES & DYNAMIC RETICLES
# =====================================================================
class ParticleStream(VGroup):
    """
    Staggered flow of particles along a trajectory (ideal for data flow,
    electron currents, network packets, or radio waves).
    """
    @staticmethod
    def create_burst(
        start_point_or_mob,
        end_point_or_mob,
        count: int = 12,
        radius: float = 0.065,
        color=None,
        run_time: float = 1.4,
        lag_ratio: float = 0.08,
    ):
        col = color or PALETTE["sky"]
        start = start_point_or_mob.get_center() if isinstance(start_point_or_mob, Mobject) else np.array(start_point_or_mob, dtype=float)
        end = end_point_or_mob.get_center() if isinstance(end_point_or_mob, Mobject) else np.array(end_point_or_mob, dtype=float)
        disp = end - start

        particles = []
        for i in range(count):
            jitter = np.array([
                -0.08 + 0.16 * ((i * 7) % 11) / 10.0,
                -0.08 + 0.16 * ((i * 13) % 11) / 10.0,
                0.0,
            ])
            p = Dot(start + jitter, radius=radius, color=col).set_opacity(0.95)
            particles.append(p)

        particle_group = VGroup(*particles)

        anim = LaggedStart(
            *[
                p.animate(rate_func=rate_functions.ease_out_quad)
                .shift(disp)
                .set_opacity(0.0)
                for p in particles
            ],
            lag_ratio=lag_ratio,
            run_time=run_time,
        )
        return particle_group, anim


class PulseReticle:
    """Expanding radial shockwave/sonar ping for physical impacts or state activations."""
    @staticmethod
    def create_burst(center_or_mob, color=None, max_scale: float = 3.5, run_time: float = 0.8):
        col = color or PALETTE["coral"]
        center = center_or_mob.get_center() if isinstance(center_or_mob, Mobject) else np.array(center_or_mob, dtype=float)
        ring = Circle(radius=0.18, arc_center=center, color=col, stroke_width=3.2)
        anim = (
            ring.animate(rate_func=rate_functions.ease_out_cubic, run_time=run_time)
            .scale(max_scale)
            .set_stroke(opacity=0)
        )
        return ring, anim


class WaveEmitter:
    """Concentric multi-wave ripple burst."""
    @staticmethod
    def create_burst(center_or_mob, count: int = 3, max_radius: float = 3.0, color=None, run_time: float = 1.2):
        col = color or PALETTE["sky"]
        center = center_or_mob.get_center() if isinstance(center_or_mob, Mobject) else np.array(center_or_mob, dtype=float)
        waves = VGroup(*[
            Circle(radius=0.15, arc_center=center, color=col, stroke_width=2.8)
            for _ in range(count)
        ])
        anim = LaggedStart(
            *[
                w.animate(rate_func=rate_functions.ease_out_quad)
                .scale(max_radius * 6.0)
                .set_stroke(opacity=0)
                for w in waves
            ],
            lag_ratio=0.25,
            run_time=run_time,
        )
        return waves, anim


class FocusReticle(VGroup):
    """
    Technical corner viewfinder brackets (┌ ┐ └ ┘) that lock viewer attention onto an actor.
    Supports auto-tracking: automatically stays centered if the target moves.
    """
    def __init__(
        self,
        target_mobject,
        buff: float = 0.22,
        bracket_len: float = 0.35,
        color=None,
        auto_track: bool = True,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.tracked_target = target_mobject
        self.buff = buff
        self.bracket_len = bracket_len
        self.col = color or PALETTE["coral"]

        self._build_brackets()

        if auto_track:
            self.add_updater(lambda mob: mob._update_position())

    def _build_brackets(self):
        self.submobjects.clear()
        target = getattr(self, "tracked_target", None)
        if target is None:
            return
        p_min = target.get_corner(DL) - np.array([self.buff, self.buff, 0])
        p_max = target.get_corner(UR) + np.array([self.buff, self.buff, 0])

        tl = np.array([p_min[0], p_max[1], 0])
        tr = np.array([p_max[0], p_max[1], 0])
        bl = np.array([p_min[0], p_min[1], 0])
        br = np.array([p_max[0], p_min[1], 0])

        self.c_tl = VMobject(color=self.col, stroke_width=3.0).set_points_as_corners(
            [tl + RIGHT * self.bracket_len, tl, tl + DOWN * self.bracket_len]
        )
        self.c_tr = VMobject(color=self.col, stroke_width=3.0).set_points_as_corners(
            [tr + LEFT * self.bracket_len, tr, tr + DOWN * self.bracket_len]
        )
        self.c_bl = VMobject(color=self.col, stroke_width=3.0).set_points_as_corners(
            [bl + RIGHT * self.bracket_len, bl, bl + UP * self.bracket_len]
        )
        self.c_br = VMobject(color=self.col, stroke_width=3.0).set_points_as_corners(
            [br + LEFT * self.bracket_len, br, br + UP * self.bracket_len]
        )

        self.add(self.c_tl, self.c_tr, self.c_bl, self.c_br)

    def _update_position(self):
        target = getattr(self, "tracked_target", None)
        if target is None:
            return
        p_min = target.get_corner(DL) - np.array([self.buff, self.buff, 0])
        p_max = target.get_corner(UR) + np.array([self.buff, self.buff, 0])

        tl = np.array([p_min[0], p_max[1], 0])
        tr = np.array([p_max[0], p_max[1], 0])
        bl = np.array([p_min[0], p_min[1], 0])
        br = np.array([p_max[0], p_min[1], 0])

        self.c_tl.set_points_as_corners([tl + RIGHT * self.bracket_len, tl, tl + DOWN * self.bracket_len])
        self.c_tr.set_points_as_corners([tr + LEFT * self.bracket_len, tr, tr + DOWN * self.bracket_len])
        self.c_bl.set_points_as_corners([bl + RIGHT * self.bracket_len, bl, bl + UP * self.bracket_len])
        self.c_br.set_points_as_corners([br + LEFT * self.bracket_len, br, br + UP * self.bracket_len])


# =====================================================================
# 3. TOPIC-AGNOSTIC ARCHITECTURAL TECH COMPONENTS
# =====================================================================
class TechNode(VGroup):
    """
    Universal computing or network node (servers, satellites, receivers, chips, microservices).
    Features a crisp white solid body, bold charcoal outline, vibrant status glow, and label.
    """
    def __init__(
        self,
        label: str,
        sublabel: str = None,
        radius: float = 0.70,
        status_color=None,
        is_square: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        accent = status_color or PALETTE["mint"]

        if is_square:
            self.shell = RoundedRectangle(
                corner_radius=0.18,
                width=radius * 2.1,
                height=radius * 2.1,
                color=PALETTE["stroke"],
                stroke_width=3.2,
                fill_color=PALETTE["surface_card"],
                fill_opacity=1.0,
            )
            self.glow = RoundedRectangle(
                corner_radius=0.22,
                width=radius * 2.25,
                height=radius * 2.25,
                color=accent,
                stroke_width=2.0,
            ).set_stroke(opacity=0.85)
        else:
            self.shell = Circle(
                radius=radius,
                color=PALETTE["stroke"],
                stroke_width=3.2,
                fill_color=PALETTE["surface_card"],
                fill_opacity=1.0,
            )
            self.glow = Circle(
                radius=radius + 0.08,
                color=accent,
                stroke_width=2.0,
            ).set_stroke(opacity=0.85)

        self.status_dot = Dot(radius=0.11, color=accent).move_to(self.shell.get_center() + UP * 0.22)

        self.text_mob = Text(
            label,
            font=FONTS["sans"],
            weight=BOLD,
            font_size=13,
            color=PALETTE["text"],
        ).move_to(self.shell.get_center() + (DOWN * 0.15 if sublabel else ORIGIN))

        self.add(self.glow, self.shell, self.status_dot, self.text_mob)

        if sublabel:
            self.sub_mob = Text(
                sublabel,
                font=FONTS["mono"],
                weight=BOLD,
                font_size=9,
                color=PALETTE["text_dim"],
            ).next_to(self.text_mob, DOWN, buff=0.06)
            self.add(self.sub_mob)


class PipelineStage(VGroup):
    """
    Modular execution/data pipeline block (Fetch, Decode, Execute, Writeback, Transform, Ingest).
    """
    def __init__(
        self,
        title: str,
        width: float = 2.2,
        height: float = 1.4,
        accent_color=None,
        step_num: str = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        accent = accent_color or PALETTE["lavender"]

        self.body = RoundedRectangle(
            corner_radius=0.14,
            width=width,
            height=height,
            color=PALETTE["stroke"],
            stroke_width=3.0,
            fill_color=PALETTE["surface_card"],
            fill_opacity=1.0,
        )

        self.header_bar = RoundedRectangle(
            corner_radius=0.08,
            width=width * 0.92,
            height=0.12,
            color=accent,
            fill_color=accent,
            fill_opacity=1.0,
            stroke_width=0,
        ).align_to(self.body, UP).shift(DOWN * 0.08)

        title_mob = Text(
            title,
            font=FONTS["sans"],
            weight=BOLD,
            font_size=13,
            color=PALETTE["text"],
        ).move_to(self.body.get_center() + DOWN * 0.05)

        self.add(self.body, self.header_bar, title_mob)

        if step_num:
            num_tag = Text(
                step_num,
                font=FONTS["mono"],
                weight=BOLD,
                font_size=10,
                color=accent,
            ).next_to(title_mob, UP, buff=0.08)
            self.add(num_tag)


class RigidDisc(VGroup):
    """Architectural spinning flywheel, gear, or atomic core with precision hub."""
    def __init__(
        self,
        radius: float = 0.75,
        core_color=None,
        is_hollow: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        accent = core_color or PALETTE["lavender"]
        self.body = Circle(
            radius=radius,
            color=PALETTE["stroke"],
            stroke_width=3.6,
            fill_color=PALETTE["surface_card"],
            fill_opacity=1.0,
        )
        self.add(self.body)

        if not is_hollow:
            self.core = Dot(radius=radius * 0.28, color=accent).move_to(self.body.get_center())
            self.add(self.core)
        else:
            self.core = Circle(
                radius=radius * 0.28,
                color=PALETTE["stroke_light"],
                stroke_width=2.2,
                fill_color=PALETTE["surface_ground"],
                fill_opacity=1.0,
            ).move_to(self.body.get_center())
            self.add(self.core)


class MetricGauge(VGroup):
    """Telemetry HUD gauge with animated progress bar and monospace readout."""
    def __init__(
        self,
        label: str,
        value_text: str,
        bar_color=None,
        bar_width: float = 2.4,
        **kwargs
    ):
        super().__init__(**kwargs)
        col = bar_color or PALETTE["amber"]
        self.lbl = Text(label, font=FONTS["sans"], weight=BOLD, font_size=13, color=PALETTE["text"])
        self.bar_bg = RoundedRectangle(
            corner_radius=0.08,
            width=bar_width,
            height=0.22,
            color=PALETTE["stroke"],
            fill_color=PALETTE["surface_ground"],
            fill_opacity=1.0,
            stroke_width=1.8,
        )
        self.bar_fill = RoundedRectangle(
            corner_radius=0.06,
            width=bar_width * 0.95,
            height=0.16,
            color=col,
            fill_color=col,
            fill_opacity=1.0,
            stroke_width=0,
        ).align_to(self.bar_bg, LEFT).shift(RIGHT * 0.05)

        self.val = Text(value_text, font=FONTS["mono"], weight=BOLD, font_size=13, color=col)
        bar_group = VGroup(self.bar_bg, self.bar_fill)
        self.add(self.lbl, bar_group, self.val)
        self.arrange(RIGHT, buff=0.25)

    @property
    def bar(self):
        return self.bar_fill

    @property
    def value(self):
        return self.val

    @property
    def label(self):
        return self.lbl


class TelemetryGroup(VGroup):
    """Top-of-screen HUD telemetry row."""
    def __init__(self, *items, direction=RIGHT, buff: float = 1.2, **kwargs):
        super().__init__(**kwargs)
        for item in items:
            self.add(item)
        self.arrange(direction, buff=buff)


class MilestoneTimeline(VGroup):
    """
    Collision-free chronological or phase timeline with alternating (UP/DOWN)
    labels and connecting architectural ticks.
    """
    def __init__(
        self,
        milestones: list,
        length: float = 10.0,
        y_pos: float = -2.4,
        color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        col = color or PALETTE["stroke"]
        self.line = Line([-length / 2, y_pos, 0], [length / 2, y_pos, 0], color=col, stroke_width=3.2)
        self.add(self.line)

        n = len(milestones)
        step = length / max(n - 1, 1)

        self.markers = VGroup()
        self.labels = VGroup()

        for i, item in enumerate(milestones):
            x = -length / 2 + i * step
            pt = np.array([x, y_pos, 0])
            accent = PALETTE["coral"] if i == 0 else PALETTE["sky"]
            dot = Dot(pt, radius=0.09, color=accent)

            is_up = (i % 2 == 0)
            tick_dir = UP if is_up else DOWN
            tick = Line(pt, pt + tick_dir * 0.40, color=col, stroke_width=2.0)

            label_txt = str(item)
            text_mob = Text(
                label_txt,
                font=FONTS["mono"],
                weight=BOLD,
                font_size=11,
                color=PALETTE["text"],
            )
            text_mob.next_to(tick.get_end(), tick_dir, buff=0.10)

            self.markers.add(dot, tick)
            self.labels.add(text_mob)

        self.add(self.markers, self.labels)


# =====================================================================
# macOS PRO WINDOW & STATUS CONTAINERS (Light Editorial by Default)
# =====================================================================
class VisualCard(VGroup):
    """
    Standard high-contrast editorial card with rounded corners,
    arctic white surface fill (#FFFFFF), deep charcoal stroke (#2D3748),
    and crisp dark typography.
    """
    def __init__(
        self,
        width: float = 3.2,
        height: float = 1.8,
        title: str = "",
        subtitle: str = "",
        fill_color=None,
        stroke_color=None,
        stroke_width: float = 2.4,
        corner_radius: float = 0.20,
        **kwargs
    ):
        super().__init__(**kwargs)
        fill = fill_color or PALETTE["surface_card"]
        stroke = stroke_color or PALETTE["stroke"]
        self.rect = RoundedRectangle(
            corner_radius=corner_radius,
            width=width,
            height=height,
            color=stroke,
            stroke_width=stroke_width,
            fill_color=fill,
            fill_opacity=1.0,
        )
        self.add(self.rect)
        self.card = self.rect

        labels = []
        if title:
            self.title_mob = Text(
                title,
                font=FONTS["sans"],
                weight=BOLD,
                font_size=14,
                color=PALETTE["text"],
            )
            labels.append(self.title_mob)
        if subtitle:
            self.sub_mob = Text(
                subtitle,
                font=FONTS["mono"],
                font_size=11,
                color=PALETTE["text_dim"],
            )
            labels.append(self.sub_mob)

        if labels:
            self.text_group = VGroup(*labels).arrange(DOWN, buff=0.10).move_to(self.rect.get_center())
            self.add(self.text_group)


class TechCard(VGroup):
    """
    Clean technical infographic container.
    Features:
    - Rounded squircle chassis (corner_radius=0.18)
    - Arctic white surface fill (#FFFFFF) with refined charcoal border (#2D3748)
    - Clean title header bar with high-contrast text and NO macOS traffic lights
    """
    def __init__(
        self,
        title: str = "",
        width: float = 4.2,
        height: float = 2.6,
        is_dark: bool = False,
        accent_color=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        bg_col = PALETTE["surface_dark"] if is_dark else PALETTE["surface_card"]
        stroke_col = PALETTE["stroke"]
        text_col = PALETTE["white"] if is_dark else PALETTE["text"]
        header_bg_col = PALETTE["surface_dark"] if is_dark else PALETTE["bg_subtle"]
        header_height = 0.44 if title else 0.0

        # Outer chassis
        self.body = RoundedRectangle(
            corner_radius=0.18,
            width=width,
            height=height,
            color=stroke_col,
            stroke_width=2.0,
            fill_color=bg_col,
            fill_opacity=1.0,
        )
        self.add(self.body)

        if title:
            # Header title bar
            self.header_bg = RoundedRectangle(
                corner_radius=0.18,
                width=width,
                height=header_height,
                color=stroke_col,
                stroke_width=0,
                fill_color=header_bg_col,
                fill_opacity=1.0,
            ).align_to(self.body, UP)

            self.header_sep = Line(
                self.body.get_left() + UP * (height / 2 - header_height),
                self.body.get_right() + UP * (height / 2 - header_height),
                color=stroke_col,
                stroke_width=1.5,
            )

            self.title_mob = Text(
                title,
                font=FONTS["sans"],
                weight=BOLD,
                font_size=13,
                color=text_col,
            ).move_to(self.header_bg.get_center())

            self.add(self.header_bg, self.header_sep, self.title_mob)

    def get_content_center(self):
        """Returns the center point of the content area below the header."""
        return self.body.get_center() + DOWN * 0.14


class MacOSWindow(TechCard):
    """Backwards compatibility alias for TechCard (traffic lights disabled by default)."""
    def __init__(self, title: str = "", width: float = 4.2, height: float = 2.6, is_dark: bool = False, show_traffic_lights: bool = False, **kwargs):
        super().__init__(title=title, width=width, height=height, is_dark=is_dark, **kwargs)
        if show_traffic_lights and hasattr(self, "header_bg"):
            dot_r = 0.055
            dot_buff = 0.08
            dot_close = Dot(radius=dot_r, color="#FF5F56")
            dot_min = Dot(radius=dot_r, color="#FFBD2E")
            dot_zoom = Dot(radius=dot_r, color="#27C93F")
            traffic_group = VGroup(dot_close, dot_min, dot_zoom).arrange(RIGHT, buff=dot_buff)
            traffic_group.align_to(self.body, LEFT).shift(RIGHT * 0.18)
            traffic_group.match_y(self.header_bg)
            self.add(traffic_group)


class MacOSPill(VGroup):
    """
    macOS status badge / pill tag with rounded ends.
    Guaranteed high contrast: bold white text on vibrant solid fill,
    or crisp dark text on subtle light wash.
    """
    def __init__(
        self,
        text: str,
        color=None,
        is_solid: bool = True,
        font_size: int = 13,
        height: float = 0.42,
        padding: float = 0.26,
        **kwargs
    ):
        super().__init__(**kwargs)
        col = color or PALETTE["blue"]

        txt_col = PALETTE["white"] if is_solid else PALETTE["text"]
        self.label = Text(
            text,
            font=FONTS["sans"],
            weight=BOLD,
            font_size=font_size,
            color=txt_col,
        )

        pill_w = self.label.width + padding * 2
        self.pill = RoundedRectangle(
            corner_radius=height / 2.0,
            width=pill_w,
            height=height,
            color=col if is_solid else PALETTE["stroke"],
            stroke_width=0 if is_solid else 1.8,
            fill_color=col if is_solid else PALETTE["surface_card"],
            fill_opacity=1.0,
        )
        self.label.move_to(self.pill.get_center())
        self.add(self.pill, self.label)


class SleekArrow(VGroup):
    """
    Vibrant directional arrow with clean head geometry.
    """
    def __init__(
        self,
        start,
        end,
        color=None,
        stroke_width: float = 3.2,
        buff: float = 0.12,
        max_tip_length_to_length_ratio: float = 0.25,
        **kwargs
    ):
        super().__init__(**kwargs)
        col = color or PALETTE["blue"]
        p_start = start.get_center() if isinstance(start, Mobject) else np.array(start, dtype=float)
        p_end = end.get_center() if isinstance(end, Mobject) else np.array(end, dtype=float)

        self.arrow = Arrow(
            p_start,
            p_end,
            color=col,
            stroke_width=stroke_width,
            buff=buff,
            max_tip_length_to_length_ratio=max_tip_length_to_length_ratio,
        )
        self.add(self.arrow)


__all__ = [
    "AttachedLabel",
    "LeaderCallout",
    "DimensionRuler",
    "VectorArrow",
    "ParticleStream",
    "PulseReticle",
    "WaveEmitter",
    "FocusReticle",
    "TechNode",
    "PipelineStage",
    "RigidDisc",
    "MetricGauge",
    "TelemetryGroup",
    "MilestoneTimeline",
    "VisualCard",
    "TechCard",
    "MacOSWindow",
    "MacOSPill",
    "SleekArrow",
]
