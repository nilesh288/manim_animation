"""
engine_2d - Resilient Infographic Engine for Manim
Universal Type Sanitization, Builtin Easing Injection & Attribute Shield
"""
from manim import *
import manim.utils.rate_functions as _rf
import numpy as np
import builtins

# =====================================================================
# 1. GLOBAL RATE FUNCTIONS & UNIVERSAL BUILTIN INJECTION
# =====================================================================
def ease_in_quad(t): return float(t) ** 2
def ease_out_quad(t): t = float(t); return t * (2.0 - t)
def ease_in_out_quad(t): t = float(t); return 2.0 * t * t if t < 0.5 else -1.0 + (4.0 - 2.0 * t) * t
def ease_in_cubic(t): return float(t) ** 3
def ease_out_cubic(t): return (float(t) - 1.0) ** 3 + 1.0
def ease_in_out_cubic(t): t = float(t); return 4.0 * t ** 3 if t < 0.5 else (t - 1.0) * (2.0 * t - 2.0) ** 2 + 1.0
def ease_in_sine(t): return 1.0 - np.cos((float(t) * np.pi) / 2.0)
def ease_out_sine(t): return np.sin((float(t) * np.pi) / 2.0)
def ease_in_out_sine(t): return -(np.cos(np.pi * float(t)) - 1.0) / 2.0
def ease_overshoot(t, s=1.15): t = float(t) - 1.0; return 1.0 + (s + 1.0) * (t ** 3) + s * (t ** 2)
def ease_heavy_inertia(t): return rush_into(t)
def ease_light_snap(t): return rush_from(t)

_all_easings = {
    "ease_in_quad": ease_in_quad,
    "ease_out_quad": ease_out_quad,
    "ease_in_out_quad": ease_in_out_quad,
    "ease_in_cubic": ease_in_cubic,
    "ease_out_cubic": ease_out_cubic,
    "ease_in_out_cubic": ease_in_out_cubic,
    "ease_in_sine": ease_in_sine,
    "ease_out_sine": ease_out_sine,
    "ease_in_out_sine": ease_in_out_sine,
    "ease_overshoot": ease_overshoot,
    "ease_heavy_inertia": ease_heavy_inertia,
    "ease_light_snap": ease_light_snap,
    "linear": linear,
    "smooth": smooth,
    "rush_into": rush_into,
    "rush_from": rush_from,
}

for _k in dir(_rf):
    if not _k.startswith("_"):
        _fn = getattr(_rf, _k)
        if callable(_fn):
            _all_easings[_k] = _fn

for _name, _func in _all_easings.items():
    setattr(builtins, _name, _func)

class EasingDict(dict):
    def _resolve(self, key):
        k = str(key).lower().replace("-", "_")
        if k in self:
            return super().__getitem__(k)
        if hasattr(_rf, k):
            return getattr(_rf, k)
        return smooth

    def __getitem__(self, key):
        return self._resolve(key)

    def get(self, key, default=None):
        res = self._resolve(key)
        return res if res is not smooth else (default if default is not None else smooth)

EASINGS = EasingDict(_all_easings)
LINEAR = linear
SMOOTH = smooth
RUSH_INTO = rush_into
RUSH_FROM = rush_from

# =====================================================================
# 2. SELF-HEALING PALETTE & FONTS
# =====================================================================
class PaletteDict(dict):
    _ALIASES = {
        "red": "#FF4D4D", "coral": "#FF4D4D",
        "green": "#00C9A7", "mint": "#00C9A7", "cyan": "#00C9A7",
        "yellow": "#FF9900", "amber": "#FF9900", "orange": "#FF9900",
        "blue": "#1E60FF", "cobalt": "#1E60FF",
        "purple": "#635BFF", "indigo": "#635BFF", "violet": "#635BFF",
        "black": "#0F172A", "stroke": "#0F172A", "obsidian": "#0F172A",
        "dark": "#2A3238", "surface_dark": "#2A3238", "charcoal": "#2A3238",
        "gray": "#475569", "grey": "#475569", "text_dim": "#475569", "slate": "#475569",
        "light_gray": "#94A3B8", "light_grey": "#94A3B8", "stroke_light": "#94A3B8",
        "white": "#FFFFFF", "surface_card": "#FFFFFF",
        "background": "#EDF2F7", "bg": "#EDF2F7", "surface_ground": "#CBDCEB",
        "text": "#0F172A"
    }

    def _resolve(self, key):
        k = str(key).lower().replace("-", "_").strip()
        if k in self:
            return super().__getitem__(k)
        return self._ALIASES.get(k, "#0F172A")

    def __getitem__(self, key):
        return self._resolve(key)

    def get(self, key, default=None):
        k = str(key).lower().replace("-", "_").strip()
        if k in self:
            return super().__getitem__(k)
        if k in self._ALIASES:
            return self._ALIASES[k]
        return default if default is not None else "#0F172A"

PALETTE = PaletteDict({
    "background": "#EDF2F7",
    "surface_ground": "#CBDCEB",
    "surface_card": "#FFFFFF",
    "surface_dark": "#2A3238",
    "stroke": "#0F172A",
    "stroke_light": "#94A3B8",
    "coral": "#FF4D4D",
    "mint": "#00C9A7",
    "amber": "#FF9900",
    "blue": "#1E60FF",
    "indigo": "#635BFF",
    "white": "#FFFFFF",
    "text": "#0F172A",
    "text_dim": "#475569",
})

class FontDict(dict):
    def __missing__(self, key):
        if "mono" in str(key).lower():
            return "monospace"
        return "sans-serif"

    def get(self, key, default=None):
        if "mono" in str(key).lower():
            return "monospace"
        return default if default is not None else "sans-serif"

FONTS = FontDict({
    "sans": "sans-serif",
    "mono": "monospace",
    "headline": "sans-serif",
    "body": "sans-serif",
})

# =====================================================================
# 3. HELPER UTILITIES: POINT NORMALIZATION
# =====================================================================
def _to_3d_point(point_or_mobj):
    if hasattr(point_or_mobj, "get_center"):
        return point_or_mobj.get_center()
    pt = np.array(point_or_mobj, dtype=float).flatten()
    if len(pt) == 2:
        return np.array([pt[0], pt[1], 0.0], dtype=float)
    if len(pt) >= 3:
        return np.array([pt[0], pt[1], pt[2]], dtype=float)
    return np.array([0.0, 0.0, 0.0], dtype=float)

# Stroke Kwarg Sanitizer Shield
_orig_set_stroke = VMobject.set_stroke

def _safe_set_stroke(self, *args, **kwargs):
    if "stroke_color" in kwargs and "color" not in kwargs:
        kwargs["color"] = kwargs["stroke_color"]
    if "stroke_width" in kwargs and "width" not in kwargs:
        kwargs["width"] = kwargs["stroke_width"]
    if "stroke_opacity" in kwargs and "opacity" not in kwargs:
        kwargs["opacity"] = kwargs["stroke_opacity"]
    valid_keys = {"color", "width", "opacity", "background", "recurse"}
    filtered = {k: v for k, v in kwargs.items() if k in valid_keys}
    return _orig_set_stroke(self, *args, **filtered)

VMobject.set_stroke = _safe_set_stroke

# =====================================================================
# 4. BASE SCENE CONTROLLER WITH TIMING AUTO-CORRECTION
# =====================================================================
class InfographicScene(MovingCameraScene):
    target_duration = 0.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = PALETTE["background"]
        self.elapsed_time = 0.0
        self._ephemeral_mobjects = []
        self._current_focal_metric = None
        self._active_reticles = None

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

    def set_focal_slot(self, new_mobject, run_time=0.4, **kwargs):
        if isinstance(new_mobject, str):
            new_mobject = Text(new_mobject, font=FONTS["sans"], weight=BOLD, font_size=28, color=PALETTE["text"])
        anims = []
        if self._current_focal_metric and self._current_focal_metric in self.mobjects:
            anims.append(FadeOut(self._current_focal_metric))
            self._current_focal_metric = None
        new_mobject._is_focal = True
        self._current_focal_metric = new_mobject
        anims.append(FadeIn(new_mobject))
        self.play(*anims, run_time=run_time)

    def clear_focal_slot(self, run_time=0.3, **kwargs):
        if self._current_focal_metric and self._current_focal_metric in self.mobjects:
            self.play(FadeOut(self._current_focal_metric), run_time=run_time)
            self._current_focal_metric = None

    def play_impact_recoil(self, body: Mobject, impact_dir=RIGHT, strength=0.18, run_time=0.35):
        t1 = run_time * 0.35
        t2 = run_time * 0.65
        dir_vec = _to_3d_point(impact_dir)
        dim = 0 if abs(dir_vec[0]) >= abs(dir_vec[1]) else 1
        other_dim = 1 - dim
        squash = max(0.2, 1.0 - strength)
        stretch = 1.0 + (strength * 0.75)
        self.play(body.animate.stretch(squash, dim).stretch(stretch, other_dim), run_time=t1, rate_func=rush_into)
        self.play(body.animate.stretch(1.0 / squash, dim).stretch(1.0 / stretch, other_dim), run_time=t2, rate_func=ease_overshoot)

    def play_impact_squash(self, body, impact_dir=RIGHT, strength=0.18, run_time=0.35):
        self.play_impact_recoil(body, impact_dir=impact_dir, strength=strength, run_time=run_time)

    def beat(self, motion_time: float, hold_time: float, action=None, description: str = ""):
        t_start = self.time
        budget = float(motion_time) + float(hold_time)

        if callable(action):
            action()
        elif isinstance(action, Animation):
            self.play(action)
        elif isinstance(action, (list, tuple)):
            anims = [a for a in action if isinstance(a, Animation)]
            if anims:
                self.play(*anims)

        t_action = self.time - t_start
        remaining_wait = budget - t_action
        if remaining_wait > 0.001:
            self.wait(remaining_wait)
        self.elapsed_time += budget

    def spotlight(self, *focal_mobjects, run_time=0.35, **kwargs):
        self.restore_focus(run_time=0.0)
        anims = []
        reticles = []
        for mob in focal_mobjects:
            reticle = FocusReticle(mob)
            reticles.append(reticle)
            self.register_ephemeral(reticle)
            anims.append(FadeIn(reticle, scale=1.1))
        self._active_reticles = VGroup(*reticles) if reticles else None
        if anims:
            self.play(*anims, run_time=run_time)

    def restore_focus(self, run_time=0.25, **kwargs):
        reticles = getattr(self, "_active_reticles", None)
        if reticles is not None and reticles in self.mobjects:
            self.play(FadeOut(reticles, scale=0.9), run_time=run_time)
        self._active_reticles = None

    def finalize(self):
        if self.target_duration <= 0.0 and getattr(self, "elapsed_time", 0.0) > 0.0:
            self.target_duration = self.elapsed_time
        actual_time = self.time
        diff = self.target_duration - actual_time
        if diff > 0.001:
            self.wait(diff)
            actual_time = self.time
        diff_final = abs(actual_time - self.target_duration)
        if diff_final > 0.05:
            print("\n❌ [CRITICAL TIMING DRIFT] Rendered: {:.2f}s | Target: {:.2f}s".format(actual_time, self.target_duration))
        else:
            print("\n🔒 [PERFECT DURATION LOCK] Rendered: {:.2f}s == Target: {:.2f}s".format(actual_time, self.target_duration))

# =====================================================================
# 5. EXPLICIT ALIASED PRIMITIVES
# =====================================================================
class VectorArrow(Arrow):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("buff", 0)
        super().__init__(*args, **kwargs)

class LeaderCallout(VGroup):
    def __init__(self, target_point=ORIGIN, title=None, subtitle=None, direction=UP+RIGHT, **kwargs):
        super().__init__()
        t_str = str(title if title is not None else kwargs.get("text", kwargs.get("label", "")))
        c = kwargs.get("color", PALETTE["stroke"])
        font_size = kwargs.get("font_size", 16)

        tp = _to_3d_point(target_point)
        dir_vec = _to_3d_point(direction)
        norm = np.linalg.norm(dir_vec)
        unit = dir_vec / norm if norm > 1e-6 else np.array([1.0, 1.0, 0.0]) / np.sqrt(2)

        elbow_point = tp + unit * 0.75
        shelf_dir = RIGHT if unit[0] >= 0 else LEFT
        text_anchor = elbow_point + (RIGHT * 0.45 if unit[0] >= 0 else LEFT * 0.45)

        pointer = VMobject(color=c, stroke_width=2.8)
        pointer.set_points_as_corners([tp, elbow_point, text_anchor])

        dot = Dot(tp, radius=0.08, color=PALETTE["coral"])

        is_math = any(sym in t_str for sym in ("\\", "_", "^", "{"))
        if is_math:
            try:
                title_mob = MathTex(t_str, color=PALETTE["text"], font_size=max(font_size, 20))
            except Exception:
                title_mob = Text(t_str, font=FONTS["sans"], weight=BOLD, font_size=font_size, color=PALETTE["text"])
        else:
            title_mob = Text(t_str, font=FONTS["sans"], weight=BOLD, font_size=font_size, color=PALETTE["text"])

        if unit[0] >= 0:
            title_mob.next_to(text_anchor, RIGHT, buff=0.14, aligned_edge=LEFT)
        else:
            title_mob.next_to(text_anchor, LEFT, buff=0.14, aligned_edge=RIGHT)

        elements = [dot, pointer, title_mob]
        sub_mob = None
        if subtitle:
            sub_mob = Text(str(subtitle), font=FONTS["mono"], weight=BOLD, font_size=11, color=PALETTE["text_dim"])
            sub_mob.next_to(title_mob, DOWN, buff=0.08, aligned_edge=title_mob.get_edge_center(LEFT if unit[0] >= 0 else RIGHT))
            elements.append(sub_mob)

        self.add(*elements)

        self.dot = dot
        self.pointer = pointer
        self.line = pointer
        self.shelf_line = pointer
        self.leader_line = pointer

        self.title_mob = title_mob
        self.title_mobj = title_mob
        self.title_mobject = title_mob
        self.title = title_mob
        self.text_mob = title_mob
        self.text_mobj = title_mob
        self.text_mobject = title_mob
        self.text = title_mob
        self.label = title_mob

        self.sub_mob = sub_mob
        self.subtitle_mob = sub_mob
        self.subtitle_mobj = sub_mob
        self.subtitle = sub_mob


class MetricGauge(VGroup):
    def __init__(self, label=None, value_text=None, bar_color=None, bar_width=2.4, **kwargs):
        super().__init__()
        lbl_str = label if label is not None else kwargs.get("title", kwargs.get("text", kwargs.get("name", "")))
        val_str = value_text if value_text is not None else kwargs.get("value_label", kwargs.get("value", kwargs.get("val", kwargs.get("init_val", kwargs.get("initial_val", "")))))
        c = bar_color if bar_color is not None else kwargs.get("color", PALETTE["amber"])

        lbl = Text(str(lbl_str), font=FONTS["sans"], weight=BOLD, font_size=13, color=PALETTE["text"])
        bar_bg = RoundedRectangle(
            corner_radius=0.1, width=bar_width, height=0.22,
            color=PALETTE["surface_ground"], fill_color=PALETTE["surface_ground"], fill_opacity=1.0, stroke_width=1.5
        )
        bar_fill = RoundedRectangle(
            corner_radius=0.08, width=bar_width * 0.96, height=0.16,
            color=c, fill_color=c, fill_opacity=1.0, stroke_width=0
        ).align_to(bar_bg, LEFT).shift(RIGHT * 0.05)
        val = Text(str(val_str), font=FONTS["mono"], weight=BOLD, font_size=13, color=c)

        bar_group = VGroup(bar_bg, bar_fill)
        self.add(lbl, bar_group, val)
        self.arrange(RIGHT, buff=0.28)

        self.lbl = lbl
        self.label = lbl
        self.title = lbl
        self.label_mob = lbl
        self.label_mobj = lbl
        self.label_mobject = lbl

        self.val = val
        self.value = val
        self.value_label = val
        self.value_mob = val
        self.value_mobj = val
        self.value_mobject = val

        self.bar = bar_fill
        self.bar_fill = bar_fill
        self.bar_bg = bar_bg

    def animate_value(self, target_value, max_value=100.0, **kwargs):
        if isinstance(target_value, (int, float)):
            num = float(target_value)
            new_text_str = f"{int(num) if num.is_integer() else num:.1f}%"
            fraction = max(0.01, min(1.0, num / max_value))
        else:
            new_text_str = str(target_value)
            try:
                num = float(new_text_str.replace("%", "").strip())
                fraction = max(0.01, min(1.0, num / max_value))
            except ValueError:
                fraction = 0.5

        target_width = max(0.05, self.bar_bg.width * 0.96 * fraction)
        target_bar = RoundedRectangle(
            corner_radius=0.08, width=target_width, height=self.bar_fill.height,
            color=self.bar_fill.get_color(), fill_color=self.bar_fill.get_fill_color(),
            fill_opacity=self.bar_fill.get_fill_opacity(), stroke_width=0
        ).align_to(self.bar_bg, LEFT).shift(RIGHT * 0.05)

        new_val = Text(new_text_str, font=FONTS["mono"], weight=BOLD, font_size=13, color=self.val.get_color()).move_to(self.val.get_center())
        return AnimationGroup(Transform(self.bar_fill, target_bar), Transform(self.val, new_val), **kwargs)

    def set_value(self, target_value, max_value=100.0):
        if isinstance(target_value, (int, float)):
            num = float(target_value)
            new_text_str = f"{int(num) if num.is_integer() else num:.1f}%"
            fraction = max(0.01, min(1.0, num / max_value))
        else:
            new_text_str = str(target_value)
            try:
                num = float(new_text_str.replace("%", "").strip())
                fraction = max(0.01, min(1.0, num / max_value))
            except ValueError:
                fraction = 0.5

        target_width = max(0.05, self.bar_bg.width * 0.96 * fraction)
        self.bar_fill.stretch_to_fit_width(target_width).align_to(self.bar_bg, LEFT).shift(RIGHT * 0.05)
        new_val = Text(new_text_str, font=FONTS["mono"], weight=BOLD, font_size=13, color=self.val.get_color()).move_to(self.val.get_center())
        self.val.become(new_val)
        return self

    def update_value(self, target_value, max_value=100.0, **kwargs):
        return self.animate_value(target_value, max_value=max_value, **kwargs)


class FocusReticle(VGroup):
    def __init__(self, target=None, buff=0.25, color=None, **kwargs):
        super().__init__()
        c = color or kwargs.get("stroke_color", PALETTE["coral"])

        if target is not None and hasattr(target, "width") and hasattr(target, "height"):
            w = target.width + buff * 2
            h = target.height + buff * 2
            center = target.get_center()
        elif target is not None and isinstance(target, (list, tuple, np.ndarray)):
            size = kwargs.get("size", 1.2)
            w = float(kwargs.get("width", kwargs.get("w", size)))
            h = float(kwargs.get("height", kwargs.get("h", size)))
            center = _to_3d_point(target)
        else:
            size = kwargs.get("size", 1.2)
            w = float(kwargs.get("width", kwargs.get("w", size)))
            h = float(kwargs.get("height", kwargs.get("h", size)))
            center = _to_3d_point(kwargs.get("point", kwargs.get("center", ORIGIN)))

        d = min(w, h) * 0.22
        corners = []
        for sx, sy in [(-1, 1), (1, 1), (1, -1), (-1, -1)]:
            cx, cy = center[0] + sx * (w / 2), center[1] + sy * (h / 2)
            p1, p2, p3 = [cx - sx * d, cy, 0], [cx, cy, 0], [cx, cy - sy * d, 0]
            b = VMobject(color=c, stroke_width=2.5)
            b.set_points_as_corners([p1, p2, p3])
            corners.append(b)

        self.corners = VGroup(*corners)
        self.halo = Annulus(
            inner_radius=max(w, h) * 0.45, outer_radius=max(w, h) * 0.55,
            color=c, fill_opacity=0.15, stroke_width=0
        ).move_to(center)
        self.add(self.halo, self.corners)


class RigidDisc(VGroup):
    def __init__(self, radius=0.75, core_color=None, body_color=None, is_hollow=False, **kwargs):
        super().__init__()
        self.radius = radius
        self.r = radius
        b_color = body_color or kwargs.get("stroke_color", kwargs.get("color", PALETTE["stroke"]))
        c_color = core_color or PALETTE["indigo"]
        f_color = kwargs.get("fill_color", PALETTE["surface_card"])
        sw = kwargs.get("stroke_width", 2.5)

        self.body = Circle(radius=radius, color=b_color, fill_color=f_color, fill_opacity=1.0, stroke_width=sw)
        if is_hollow:
            self.core = Circle(radius=radius * 0.35, color=c_color, stroke_width=1.8, fill_opacity=0.0)
        else:
            self.core = Dot(point=ORIGIN, radius=radius * 0.35, color=c_color)

        self.add(self.body, self.core)
        self.disc = self.body
        self.circle = self.body
        self.outer = self.body
        self.inner = self.core

    @property
    def center(self):
        return self.get_center()


class SurfaceGround(VGroup):
    def __init__(self, ground_y=None, **kwargs):
        super().__init__()
        gy = float(ground_y if ground_y is not None else kwargs.get("y_position", kwargs.get("y_pos", -1.0)))
        l_color = kwargs.get("line_color", kwargs.get("stroke_color", PALETTE["stroke"]))
        p_color = kwargs.get("plane_color", PALETTE["surface_ground"])

        line = Line([-30.0, gy, 0], [30.0, gy, 0], color=l_color, stroke_width=4.0)
        shading = Rectangle(
            width=60.0, height=3.5, color=p_color, fill_color=p_color, fill_opacity=1.0, stroke_width=0
        ).move_to([0.0, gy - 1.75, 0.0])
        ticks = VGroup(*[
            Line([x, gy - 0.08, 0], [x, gy + 0.08, 0], color=PALETTE["stroke_light"], stroke_width=1.5)
            for x in np.arange(-28.0, 28.1, 0.5)
        ])

        self.add(shading, line, ticks)
        self.ground_y = gy
        self.y = gy
        self.y_pos = gy
        self.level = gy

        self.line = line
        self.baseline = line
        self.rail = line
        self.shading = shading
        self.plane = shading
        self.ticks = ticks
        self.hashmarks = ticks


class DimensionRuler(VGroup):
    def __init__(self, start_point=ORIGIN, end_point=RIGHT, label="", **kwargs):
        super().__init__()
        c = kwargs.get("color", PALETTE["stroke"])
        self.tick_size = kwargs.get("tick_size", 0.18)
        self.label_str = str(label or kwargs.get("text", ""))

        s = _to_3d_point(start_point)
        e = _to_3d_point(end_point)

        self.line = Line(s, e, color=c, stroke_width=2.0)
        self.start_cap = Line(UP * (self.tick_size / 2), DOWN * (self.tick_size / 2), color=c, stroke_width=2.0)
        self.end_cap = Line(UP * (self.tick_size / 2), DOWN * (self.tick_size / 2), color=c, stroke_width=2.0)

        is_math = any(sym in self.label_str for sym in ("\\", "_", "^", "{"))
        if is_math:
            try:
                self.label_mob = MathTex(self.label_str, color=c, font_size=18)
            except Exception:
                self.label_mob = Text(self.label_str, font=FONTS["mono"], font_size=13, color=c)
        else:
            self.label_mob = Text(self.label_str, font=FONTS["mono"], font_size=13, color=c)

        self.label = self.label_mob
        self.label_mobj = self.label_mob
        self.label_mobject = self.label_mob
        self.text = self.label_mob
        self.text_mob = self.label_mob

        self.add(self.line, self.start_cap, self.end_cap, self.label_mob)
        self.put_start_and_end_on(s, e)

    def put_start_and_end_on(self, start, end):
        s = _to_3d_point(start)
        e = _to_3d_point(end)
        vec = e - s
        norm = np.linalg.norm(vec)
        if norm < 1e-4:
            e = s + np.array([1e-4, 0.0, 0.0])
            vec = e - s
            norm = 1e-4
        unit = vec / norm
        perp = np.array([-unit[1], unit[0], 0.0])
        self.line.put_start_and_end_on(s, e)
        self.start_cap.put_start_and_end_on(s - perp * (self.tick_size / 2), s + perp * (self.tick_size / 2))
        self.end_cap.put_start_and_end_on(e - perp * (self.tick_size / 2), e + perp * (self.tick_size / 2))
        self.label_mob.move_to((s + e) / 2.0).shift(perp * 0.22)
        self.label_mob.set_opacity(0.0 if norm < 0.35 else 1.0)
        return self


class MilestoneTimeline(VGroup):
    def __init__(self, milestones=None, length=None, y_pos=-2.4, **kwargs):
        super().__init__()
        items = milestones if milestones is not None else kwargs.get("items", [])
        if isinstance(items, dict):
            items = list(items.items())

        total_len = float(length if length is not None else kwargs.get("width", 10.0))
        color = kwargs.get("color", PALETTE["stroke"])
        self.line = Line([-total_len / 2, y_pos, 0], [total_len / 2, y_pos, 0], color=color, stroke_width=3.0)
        self.add(self.line)

        n = len(items)
        step = total_len / max(n - 1, 1)
        self.markers = VGroup()
        self.labels = VGroup()

        for i, item in enumerate(items):
            x = -total_len / 2 + i * step
            dot = Dot([x, y_pos, 0], radius=0.08, color=PALETTE["coral"] if i == 0 else PALETTE["indigo"])
            self.markers.add(dot)
            direction = UP if (i % 2 == 1) else DOWN
            lbl_color = PALETTE["indigo"] if (i % 2 == 1) else PALETTE["text"]

            if isinstance(item, (tuple, list)):
                main_txt = str(item[0])
                sub_txt = str(item[1]) if len(item) > 1 else ""
                t_mob = Text(main_txt, font=FONTS["sans"], weight=BOLD, font_size=12, color=lbl_color)
                if sub_txt:
                    s_mob = Text(sub_txt, font=FONTS["mono"], font_size=10, color=PALETTE["text_dim"])
                    lbl = VGroup(t_mob, s_mob).arrange(DOWN, buff=0.06)
                else:
                    lbl = t_mob
            else:
                lbl = Text(str(item), font=FONTS["sans"], weight=BOLD, font_size=12, color=lbl_color)

            lbl.next_to(dot, direction, buff=0.22)
            self.labels.add(lbl)

        self.add(self.markers, self.labels)
        self.timeline = self.line
        self.axis = self.line
        self.dots = self.markers


class DashedRectangle(DashedVMobject):
    def __init__(self, width=2.0, height=1.0, num_dashes=16, dashed_ratio=0.5, **kwargs):
        rect = Rectangle(width=width, height=height, **kwargs)
        super().__init__(rect, num_dashes=num_dashes, dashed_ratio=dashed_ratio)


class DashedCircle(DashedVMobject):
    def __init__(self, radius=1.0, num_dashes=16, dashed_ratio=0.5, **kwargs):
        circ = Circle(radius=radius, **kwargs)
        super().__init__(circ, num_dashes=num_dashes, dashed_ratio=dashed_ratio)


class DropShadow(VGroup):
    def __init__(self, target: VMobject, offset=np.array([0.08, -0.10, 0]), opacity=0.15, scale=1.02, **kwargs):
        super().__init__()
        c = kwargs.get("color", PALETTE["stroke"])
        shadow = target.copy()
        shadow.set_fill(c, opacity=opacity)
        shadow.set_stroke(c, width=1.5, opacity=opacity * 0.6)
        shadow.scale(scale)
        shadow.shift(offset)
        self.add(shadow)
        self.shadow = shadow
        self.target = target


class VisualCard(VGroup):
    def __init__(self, width=2.4, height=1.6, fill_color=PALETTE["coral"], **kwargs):
        super().__init__()
        border_c = kwargs.get("border_color", kwargs.get("stroke_color"))
        stroke_c = border_c if border_c else fill_color
        stroke_w = 3.0 if border_c else 0.0
        label_str = kwargs.get("label", kwargs.get("title", ""))

        self.card = RoundedRectangle(
            corner_radius=0.25, width=width, height=height,
            color=stroke_c, stroke_width=stroke_w, fill_color=fill_color, fill_opacity=1.0
        )
        self.add(self.card)
        self.lbl = None
        if label_str:
            self.lbl = Text(str(label_str), font=FONTS["sans"], font_size=13, color=PALETTE["text_dim"]).next_to(self.card, DOWN, buff=0.25)
            self.add(self.lbl)

        self.rect = self.card
        self.bg = self.card
        self.background = self.card
        self.label = self.lbl
        self.title = self.lbl
        self.text = self.lbl


class Chevron(VMobject):
    def __init__(self, direction=RIGHT, size=0.25, color=None, stroke_width=3.0, **kwargs):
        super().__init__()
        c = color or PALETTE["amber"]
        self.set_color(c)
        self.set_stroke(color=c, width=stroke_width)
        u = normalize(_to_3d_point(direction))
        n = rotate_vector(u, PI / 2)
        p1 = -u * size + n * size
        p2 = np.array([0.0, 0.0, 0.0])
        p3 = -u * size - n * size
        self.set_points_as_corners([p1, p2, p3])


class ParticleWake(VGroup):
    def __init__(self, target=ORIGIN, trail_dir=LEFT, num_particles=6, **kwargs):
        super().__init__()
        col = kwargs.get("color", PALETTE["mint"])
        length = kwargs.get("length", 1.4)
        spread = kwargs.get("spread", 0.22)
        center = target.get_edge_center(trail_dir) if hasattr(target, "get_edge_center") else _to_3d_point(target)
        unit_dir = normalize(_to_3d_point(trail_dir))
        normal = rotate_vector(unit_dir, PI / 2)
        for i in range(num_particles):
            dist = (i + 1) * (length / (num_particles + 1))
            lateral = np.sin(i * 2.2) * spread
            pos = center + (unit_dir * dist) + (normal * lateral)
            decay = 1.0 - (i / num_particles)
            dot = Dot(point=pos, radius=max(0.045 * decay, 0.015), color=col)
            dot.set_opacity(decay * 0.85)
            self.add(dot)


class TelemetryGroup(VGroup):
    def __init__(self, *items, direction=RIGHT, buff=2.2, **kwargs):
        super().__init__()
        unpacked = []
        for it in items:
            if isinstance(it, (list, tuple)):
                unpacked.extend(it)
            else:
                unpacked.append(it)
        self.add(*unpacked)
        self.arrange(direction, buff=buff)
        self.to_edge(UP, buff=0.8)


builtins.DashedRectangle = DashedRectangle
builtins.DashedCircle = DashedCircle
builtins.VectorArrow = VectorArrow

__all__ = [
    "PALETTE",
    "FONTS",
    "EASINGS",
    "LINEAR",
    "SMOOTH",
    "InfographicScene",
    "ParticleWake",
    "DropShadow",
    "FocusReticle",
    "VisualCard",
    "MilestoneTimeline",
    "Chevron",
    "RigidDisc",
    "LeaderCallout",
    "DimensionRuler",
    "SurfaceGround",
    "TelemetryGroup",
    "MetricGauge",
    "VectorArrow",
    "DashedRectangle",
    "DashedCircle",
]
