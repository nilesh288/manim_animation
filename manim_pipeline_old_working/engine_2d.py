"""
engine_2d - Core 2D Technical Infographic Engine for Manim
Rich High-Contrast Edition with Built-In Collision-Proof Primitives
"""
from manim import *
import numpy as np

# =====================================================================
# 1. COLOR DESIGN SYSTEM
# =====================================================================
PALETTE = {
    "background": "#EDF2F7",      # Cool mist canvas
    "surface_ground": "#CBDCEB",  # Solid bedrock runway platform
    "surface_card": "#FFFFFF",    # Arctic white card fill
    "surface_dark": "#2A3238",    # Deep graphite charcoal
    "stroke": "#0F172A",          # Heavy obsidian boundary ink (4.0px rail)
    "stroke_light": "#94A3B8",    # Architectural ticks and dividers
    "coral": "#FF4D4D",           # Vibrant salmon-coral
    "mint": "#00C9A7",            # Electric cyan-mint
    "amber": "#FF9900",           # Rich tangerine-amber
    "blue": "#1E60FF",            # Pure electric cobalt
    "indigo": "#635BFF",          # Deep vibrant royal violet
    "white": "#FFFFFF",           # Pure white wireframe glyphs
    "text": "#0F172A",            # Pitch headline typography
    "text_dim": "#475569",        # Dense slate for secondary labels
}

FONTS = {
    "sans": "sans-serif",
    "mono": "monospace",
}

SCREEN_SAFE_X = 5.8
SCREEN_SAFE_Y = 3.2


# =====================================================================
# 2. SCENE CONTROLLER WITH AUTO-EVICTING FOCAL SLOT
# =====================================================================
class InfographicScene(Scene):
    target_duration = 0.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = PALETTE["background"]
        self.elapsed_time = 0.0
        self._ephemeral_mobjects = []
        self._current_focal_metric = None

    def register_ephemeral(self, *mobjects):
        for m in mobjects:
            if m not in self._ephemeral_mobjects:
                self._ephemeral_mobjects.append(m)

    def clear_ephemerals(self, run_time=0.3):
        if self._ephemeral_mobjects:
            to_remove = []
            for m in self._ephemeral_mobjects:
                if m in self.mobjects and m not in to_remove:
                    to_remove.append(m)
                for sub in getattr(m, "submobjects", []):
                    if sub in self.mobjects and sub not in to_remove:
                        to_remove.append(sub)
            if to_remove:
                self.play(*[FadeOut(m) for m in to_remove], run_time=run_time)
            self._ephemeral_mobjects.clear()

    def set_focal_slot(self, new_mobject, run_time=0.4):
        """
        Permanently prevents double-exposure text collisions in Zone 2.
        Automatically evicts the prior metric before displaying the new one.
        """
        anims = []
        if self._current_focal_metric and self._current_focal_metric in self.mobjects:
            anims.append(FadeOut(self._current_focal_metric))
        
        self._current_focal_metric = new_mobject
        anims.append(FadeIn(new_mobject))
        self.play(*anims, run_time=run_time)

    def beat(self, motion_time: float, hold_time: float, action: callable, description: str = ""):
        action()
        if hold_time > 0:
            self.wait(hold_time)
        self.elapsed_time += motion_time + hold_time

    def finalize(self):
        actual_time = self.time
        diff = abs(actual_time - self.target_duration)
        if diff > 0.2:
            print(f"⚠️ DURATION MISMATCH: Actual Video Time = {actual_time:.2f}s | Target = {self.target_duration:.2f}s (Diff: {diff:.2f}s)")
        else:
            print(f"✅ RUNTIME PERFECT: Actual Video Time = {actual_time:.2f}s (Target: {self.target_duration:.2f}s)")


# =====================================================================
# 3. COLLISION-FREE INFOGRAPHIC PRIMITIVES
# =====================================================================
class MilestoneTimeline(VGroup):
    """
    Automated timeline that permanently eliminates horizontal text collisions
    by strictly alternating labels (Odd = UP, Even = DOWN) with connecting ticks.
    """
    def __init__(self, milestones: list, length=10.0, y_pos=-2.4, color=PALETTE["stroke"], **kwargs):
        super().__init__(**kwargs)
        self.line = Line([-length / 2, y_pos, 0], [length / 2, y_pos, 0], color=color, stroke_width=3.0)
        self.add(self.line)

        n = len(milestones)
        step = length / max(n - 1, 1)

        self.markers = VGroup()
        self.labels = VGroup()

        for i, item in enumerate(milestones):
            x = -length / 2 + i * step
            pt = np.array([x, y_pos, 0])
            dot = Dot(pt, radius=0.08, color=PALETTE["coral"] if i == 0 else PALETTE["indigo"])
            self.markers.add(dot)

            # Alternate directions: 0 = DOWN, 1 = UP, 2 = DOWN, 3 = UP
            direction = UP if (i % 2 == 1) else DOWN
            lbl_color = PALETTE["indigo"] if (i % 2 == 1) else PALETTE["text"]
            
            lbl = Text(item, font=FONTS["sans"], weight=BOLD, font_size=12, color=lbl_color)
            lbl.next_to(dot, direction, buff=0.28)
            self.labels.add(lbl)

        self.add(self.markers, self.labels)


class RigidDisc(VGroup):
    def __init__(self, radius=0.75, core_color=PALETTE["indigo"], is_hollow=False, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.body = Circle(
            radius=radius,
            color=PALETTE["stroke"],
            stroke_width=4.5,
            fill_color=PALETTE["surface_card"],
            fill_opacity=1.0,
        )
        self.add(self.body)

        if not is_hollow:
            self.core = Dot(radius=0.22, color=core_color).move_to(self.body.get_center())
            self.add(self.core)
        else:
            self.core = Circle(
                radius=0.22,
                color=PALETTE["stroke_light"],
                stroke_width=2.5,
                fill_color=PALETTE["surface_ground"],
                fill_opacity=1.0,
            ).move_to(self.body.get_center())
            self.add(self.core)


class SurfaceGround(VGroup):
    def __init__(self, ground_y=-1.0, **kwargs):
        super().__init__(**kwargs)
        self.line = Line([-7.2, ground_y, 0], [7.2, ground_y, 0], color=PALETTE["stroke"], stroke_width=4.0)
        self.shading = Rectangle(
            width=14.4,
            height=2.8,
            color=PALETTE["surface_ground"],
            fill_color=PALETTE["surface_ground"],
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to([0.0, ground_y - 1.4, 0.0])
        self.add(self.shading, self.line)


class TelemetryGroup(VGroup):
    def __init__(self, *items, direction=RIGHT, buff=1.4, **kwargs):
        super().__init__(**kwargs)
        for item in items:
            self.add(item)
        self.arrange(direction, buff=buff)


class MetricGauge(VGroup):
    def __init__(self, label: str, value_text: str, bar_color=PALETTE["amber"], bar_width=2.4, **kwargs):
        super().__init__(**kwargs)
        self.lbl = Text(label, font=FONTS["sans"], weight=BOLD, font_size=13, color=PALETTE["text"])
        self.bar_bg = RoundedRectangle(
            corner_radius=0.1,
            width=bar_width,
            height=0.22,
            color=PALETTE["surface_ground"],
            fill_color=PALETTE["surface_ground"],
            fill_opacity=1.0,
            stroke_width=1.5,
        )
        self.bar_fill = RoundedRectangle(
            corner_radius=0.08,
            width=bar_width * 0.96,
            height=0.16,
            color=bar_color,
            fill_color=bar_color,
            fill_opacity=1.0,
            stroke_width=0,
        ).align_to(self.bar_bg, LEFT).shift(RIGHT * 0.05)
        
        self.val = Text(value_text, font=FONTS["mono"], weight=BOLD, font_size=13, color=bar_color)
        bar_group = VGroup(self.bar_bg, self.bar_fill)
        self.add(self.lbl, bar_group, self.val)
        self.arrange(RIGHT, buff=0.28)


class LeaderCallout(VGroup):
    def __init__(self, target_point, title: str, subtitle: str = None, direction=UP+RIGHT, **kwargs):
        super().__init__(**kwargs)
        norm_dir = normalize(direction)
        elbow_point = target_point + norm_dir * 0.75
        text_anchor = elbow_point + (RIGHT * 0.45 if norm_dir[0] >= 0 else LEFT * 0.45)

        pointer = VMobject(color=PALETTE["stroke"], stroke_width=2.8)
        pointer.set_points_as_corners([target_point, elbow_point, text_anchor])

        dot = Dot(target_point, radius=0.08, color=PALETTE["coral"])
        title_mob = Text(title, font=FONTS["sans"], weight=BOLD, font_size=15, color=PALETTE["text"])

        if norm_dir[0] >= 0:
            title_mob.next_to(text_anchor, RIGHT, buff=0.14, aligned_edge=LEFT)
        else:
            title_mob.next_to(text_anchor, LEFT, buff=0.14, aligned_edge=RIGHT)

        elements = [dot, pointer, title_mob]
        if subtitle:
            sub_mob = Text(subtitle, font=FONTS["mono"], weight=BOLD, font_size=11, color=PALETTE["text_dim"])
            sub_mob.next_to(title_mob, DOWN, buff=0.08, aligned_edge=title_mob.get_edge_center(LEFT if norm_dir[0] >= 0 else RIGHT))
            elements.append(sub_mob)

        self.add(*elements)


class DimensionRuler(VGroup):
    def __init__(self, start_point, end_point, label: str, color=PALETTE["stroke"], **kwargs):
        super().__init__(**kwargs)
        start = np.array(start_point)
        end = np.array(end_point)
        dist = np.linalg.norm(end - start)
        if dist < 0.4:
            return

        main_line = Line(start, end, color=color, stroke_width=2.8)
        normal = rotate_vector(normalize(end - start), PI / 2) * 0.14
        cap_start = Line(start - normal, start + normal, color=color, stroke_width=2.8)
        cap_end = Line(end - normal, end + normal, color=color, stroke_width=2.8)
        tag = Text(label, font=FONTS["sans"], weight=BOLD, font_size=14, color=color).next_to(main_line, DOWN, buff=0.14)
        self.add(main_line, cap_start, cap_end, tag)


__all__ = [
    "PALETTE",
    "FONTS",
    "InfographicScene",
    "MilestoneTimeline",
    "RigidDisc",
    "LeaderCallout",
    "DimensionRuler",
    "SurfaceGround",
    "TelemetryGroup",
    "MetricGauge",
]
