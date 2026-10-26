"""
engine_2d/base_scene.py
Base Scene with strict beat-synchronization, auto-evicting focal slots,
automatic transient element lifecycle cleanup, and universal easing injection.
"""
import builtins
import numpy as np
from manim import Scene, ThreeDScene, FadeIn, FadeOut, rate_functions, Text, RoundedRectangle, VGroup, VMobject, Mobject
from .theme import PALETTE, FONT_SIZES


# =====================================================================
# UNIVERSAL EASING FUNCTIONS (Injected into Builtins)
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
def ease_heavy_inertia(t): return rate_functions.rush_into(t)
def ease_light_snap(t): return rate_functions.rush_from(t)

EASINGS = {
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
    "linear": rate_functions.linear,
    "smooth": rate_functions.smooth,
}

for name, func in EASINGS.items():
    setattr(builtins, name, func)


BROADCAST_SAFE_X = 5.8
BROADCAST_SAFE_Y = 3.2


# =====================================================================
# CORE INFOGRAPHIC CONTROLLER
# =====================================================================
class InfographicScene(Scene):
    target_duration = 0.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = PALETTE["background"]
        self.elapsed_time = 0.0
        self._ephemeral_mobjects = []
        self._current_focal_metric = None
        self._pending_transients = []

    def setup(self):
        super().setup()
        self.camera.background_color = PALETTE["background"]

    def fit_to_safe_zone(self, mobject, padding: float = 0.4):
        """Scale and center mobject if it exceeds the broadcast safe viewport."""
        max_w = 2.0 * (BROADCAST_SAFE_X - padding)
        max_h = 2.0 * (BROADCAST_SAFE_Y - padding)
        if mobject.width > max_w or mobject.height > max_h:
            mobject.scale_to_fit_width(max_w)
            if mobject.height > max_h:
                mobject.scale_to_fit_height(max_h)
        return mobject

    def clamp_mobject(self, mobject, margin: float = 0.3):
        """Clamp mobject within screen boundaries [-7.1+margin, 7.1-margin] and [-4.0+margin, 4.0-margin]."""
        p_min = mobject.get_corner(np.array([-1, -1, 0]))
        p_max = mobject.get_corner(np.array([1, 1, 0]))
        shift = np.zeros(3)
        if p_min[0] < -7.1 + margin:
            shift[0] = (-7.1 + margin) - p_min[0]
        elif p_max[0] > 7.1 - margin:
            shift[0] = (7.1 - margin) - p_max[0]
        if p_min[1] < -4.0 + margin:
            shift[1] = (-4.0 + margin) - p_min[1]
        elif p_max[1] > 4.0 - margin:
            shift[1] = (4.0 - margin) - p_max[1]
        mobject.shift(shift)
        return mobject

    def register_ephemeral(self, *mobjects):
        """Register ephemeral objects for batched removal."""
        for m in mobjects:
            if m not in self._ephemeral_mobjects:
                self._ephemeral_mobjects.append(m)

    def register_transient(self, *mobjects):
        """Dynamically register temporary mobjects created during action() for lifecycle fade-out."""
        for m in mobjects:
            if m not in self._ephemeral_mobjects:
                self._ephemeral_mobjects.append(m)

    def clear_ephemerals(self, run_time: float = 0.25):
        """Fades out all registered temporary ephemerals."""
        if self._ephemeral_mobjects:
            to_remove = [
                m for m in self._ephemeral_mobjects
                if m in self.mobjects
            ]
            if to_remove:
                self.play(*[FadeOut(m) for m in to_remove], run_time=run_time)
            self._ephemeral_mobjects.clear()

    def set_focal_slot(self, new_mobject, run_time: float = 0.4):
        """
        Permanently eliminates text/formula collisions in Zone 2.
        Smoothly fades out the prior focal equation/callout before introducing the new one.
        """
        anims = []
        if self._current_focal_metric is not None and self._current_focal_metric in self.mobjects:
            anims.append(FadeOut(self._current_focal_metric))

        self._current_focal_metric = new_mobject
        anims.append(FadeIn(new_mobject))
        self.play(*anims, run_time=run_time)

    def _create_transient_mobject(self, item):
        """Builds a temporary high-contrast badge or annotation from a storyboard transient dictionary."""
        if not isinstance(item, dict):
            return item

        t_type = item.get("type", "badge").lower()
        text_str = str(item.get("text", ""))
        pos = item.get("position", [0.0, 0.0, 0.0])
        if len(pos) == 2:
            pos = [pos[0], pos[1], 0.0]

        if t_type in ("badge", "pill", "card"):
            fill_tok = item.get("fill_token", "indigo")
            fill_c = PALETTE[fill_tok] if isinstance(fill_tok, str) else fill_tok
            border_tok = item.get("border_token", item.get("stroke_token", None))
            stroke_c = PALETTE[border_tok] if border_tok else fill_c
            text_tok = item.get("text_color", item.get("color_token", "#FFFFFF"))
            text_c = PALETTE[text_tok] if isinstance(text_tok, str) else text_tok

            label_text = Text(
                text_str,
                font="SF Pro Display",
                weight="SEMIBOLD",
                font_size=FONT_SIZES.get("badge", 13),
                color=text_c,
            )
            bg = RoundedRectangle(
                corner_radius=0.18,
                width=max(1.8, label_text.width + 0.44),
                height=0.42,
                fill_color=fill_c,
                fill_opacity=1.0,
                stroke_color=stroke_c,
                stroke_width=1.2,
            )
            badge = VGroup(bg, label_text)
            label_text.move_to(bg.get_center())
            badge.move_to(pos)
            return badge
        else:
            color_tok = item.get("color_token", item.get("text_color", "text_dim"))
            text_c = PALETTE[color_tok] if isinstance(color_tok, str) else color_tok
            ann = Text(
                text_str,
                font="SF Pro Display",
                weight="MEDIUM",
                font_size=FONT_SIZES.get("caption", 14),
                color=text_c,
            )
            ann.move_to(pos)
            return ann

    def beat(
        self,
        *args,
        motion_time: float = None,
        hold_time: float = None,
        action=None,
        description: str = "",
        transient: list = None,
        clear_previous_transients: bool = True,
        fade_transients: bool = True,
        **kwargs
    ):
        """
        Executes a synchronized beat with mathematically exact Zero-Drift timing.
        Supports both positional and keyword calling conventions:
          - beat(beat_id, narration, action, motion_time=..., hold_time=..., transient=[...])
          - beat(motion_time, hold_time, action=...)
          - beat(action, motion_time=..., hold_time=...)
        """
        beat_id = kwargs.pop("beat_id", None)
        narration = kwargs.pop("narration", kwargs.pop("description", description))

        # Parse positional args if passed
        pos_args = list(args)
        if pos_args:
            if isinstance(pos_args[0], str):
                beat_id = pos_args.pop(0)
                if pos_args and isinstance(pos_args[0], str):
                    narration = pos_args.pop(0)
                if pos_args and callable(pos_args[0]):
                    action = pos_args.pop(0)
            elif callable(pos_args[0]):
                action = pos_args.pop(0)
            elif isinstance(pos_args[0], (int, float)):
                motion_time = float(pos_args.pop(0))
                if pos_args and isinstance(pos_args[0], (int, float)):
                    hold_time = float(pos_args.pop(0))
                if pos_args and callable(pos_args[0]):
                    action = pos_args.pop(0)

        for pa in pos_args:
            if callable(pa) and action is None:
                action = pa
            elif isinstance(pa, (int, float)):
                if motion_time is None:
                    motion_time = float(pa)
                elif hold_time is None:
                    hold_time = float(pa)

        # Resilient target duration resolution
        if "duration" in kwargs:
            target_total = float(kwargs.pop("duration"))
        elif motion_time is not None and hold_time is not None:
            target_total = float(motion_time) + float(hold_time)
        elif motion_time is not None:
            target_total = float(motion_time)
        else:
            target_total = 1.5

        # 1. Clean up transients from prior beats if requested
        if clear_previous_transients and self._pending_transients:
            to_clear = []
            for m in self._pending_transients:
                if m in self.mobjects and m not in to_clear:
                    to_clear.append(m)
                elif hasattr(m, "get_family"):
                    for sub in m.get_family():
                        if sub in self.mobjects and sub not in to_clear:
                            to_clear.append(sub)
            if to_clear:
                self.remove(*to_clear)
            self._pending_transients.clear()

        # 2. Materialize transient items for this beat if provided
        active_transients = []
        if transient:
            t_items = transient if isinstance(transient, (list, tuple)) else [transient]
            for it in t_items:
                if isinstance(it, dict):
                    mob = self._create_transient_mobject(it)
                    if mob:
                        self.add(mob)
                        active_transients.append(mob)
                elif isinstance(it, (VGroup, VMobject, Mobject)):
                    active_transients.append(it)

        # 3. Execute active choreography and measure exact elapsed time
        t_before = self.time
        if action is not None:
            action()
        t_action = self.time - t_before

        # Collect any additional ephemeral mobjects registered inside action()
        if self._ephemeral_mobjects:
            for m in self._ephemeral_mobjects:
                if m not in active_transients:
                    active_transients.append(m)
            self._ephemeral_mobjects.clear()

        # 4. Dynamically calibrate remaining hold time to enforce ZERO drift
        remaining_hold = max(0.0, target_total - t_action)

        # 5. Narration hold with optional smooth transient dissolve
        if active_transients and fade_transients and remaining_hold >= 0.45:
            fade_duration = min(0.40, remaining_hold * 0.45)
            static_hold = remaining_hold - fade_duration
            if static_hold > 0:
                self.wait(static_hold)
            to_fade = []
            for m in active_transients:
                if m in self.mobjects and m not in to_fade:
                    to_fade.append(m)
                elif hasattr(m, "get_family"):
                    for sub in m.get_family():
                        if sub in self.mobjects and sub not in to_fade:
                            to_fade.append(sub)
            if to_fade:
                self.play(*[FadeOut(m) for m in to_fade], run_time=fade_duration)
            else:
                self.wait(fade_duration)
        elif remaining_hold > 0:
            self.wait(remaining_hold)

        # Ensure any active transients remaining on screen are queued for clean eviction
        if active_transients:
            for item in active_transients:
                is_on_canvas = item in self.mobjects or (
                    hasattr(item, "get_family") and any(sub in self.mobjects for sub in item.get_family())
                )
                if is_on_canvas and item not in self._pending_transients:
                    self._pending_transients.append(item)

        self.elapsed_time += target_total

    def finalize(self):
        """Validates actual elapsed time against target duration and cleans transients."""
        if self._pending_transients:
            to_clear = []
            for m in self._pending_transients:
                if m in self.mobjects and m not in to_clear:
                    to_clear.append(m)
                elif hasattr(m, "get_family"):
                    for sub in m.get_family():
                        if sub in self.mobjects and sub not in to_clear:
                            to_clear.append(sub)
            if to_clear:
                self.remove(*to_clear)
            self._pending_transients.clear()

        actual_time = self.time
        diff = abs(actual_time - self.target_duration)
        if diff > 0.25:
            print(f"⚠️ DURATION CHECK: Actual = {actual_time:.2f}s | Target = {self.target_duration:.2f}s (Diff: {diff:.2f}s)")
        else:
            print(f"✅ RUNTIME PERFECT: {actual_time:.2f}s (Target: {self.target_duration:.2f}s)")


class InfographicThreeDScene(ThreeDScene):
    """
    3D Infographic Scene controller supporting spherical geometry, orbits,
    ambient camera movement, and HUD overlays with identical Zero-Drift beat timing.
    """
    target_duration = 0.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = PALETTE["background"]
        self.elapsed_time = 0.0
        self._ephemeral_mobjects = []
        self._current_focal_metric = None
        self._pending_transients = []

    def setup(self):
        super().setup()
        self.camera.background_color = PALETTE["background"]

    def register_transient(self, *mobjects):
        for m in mobjects:
            if m not in self._ephemeral_mobjects:
                self._ephemeral_mobjects.append(m)

    def beat(
        self,
        motion_time: float = None,
        hold_time: float = None,
        action=None,
        description: str = "",
        transient: list = None,
        clear_previous_transients: bool = True,
        fade_transients: bool = True,
        **kwargs
    ):
        if "duration" in kwargs:
            target_total = float(kwargs.pop("duration"))
        elif motion_time is not None and hold_time is not None:
            target_total = float(motion_time) + float(hold_time)
        elif motion_time is not None:
            target_total = float(motion_time)
        else:
            target_total = 1.5

        if clear_previous_transients and self._pending_transients:
            to_clear = []
            for m in self._pending_transients:
                if m in self.mobjects and m not in to_clear:
                    to_clear.append(m)
                elif hasattr(m, "get_family"):
                    for sub in m.get_family():
                        if sub in self.mobjects and sub not in to_clear:
                            to_clear.append(sub)
            if to_clear:
                self.remove(*to_clear)
            self._pending_transients.clear()

        t_before = self.time
        if action is not None:
            action()
        t_action = self.time - t_before

        active_transients = []
        if transient:
            if isinstance(transient, (list, tuple)):
                active_transients.extend(transient)
            else:
                active_transients.append(transient)
        if self._ephemeral_mobjects:
            for m in self._ephemeral_mobjects:
                if m not in active_transients:
                    active_transients.append(m)
            self._ephemeral_mobjects.clear()

        remaining_hold = max(0.0, target_total - t_action)

        if active_transients and fade_transients and remaining_hold >= 0.45:
            fade_duration = min(0.40, remaining_hold * 0.45)
            static_hold = remaining_hold - fade_duration
            if static_hold > 0:
                self.wait(static_hold)
            to_fade = []
            for m in active_transients:
                if m in self.mobjects and m not in to_fade:
                    to_fade.append(m)
                elif hasattr(m, "get_family"):
                    for sub in m.get_family():
                        if sub in self.mobjects and sub not in to_fade:
                            to_fade.append(sub)
            if to_fade:
                self.play(*[FadeOut(m) for m in to_fade], run_time=fade_duration)
            else:
                self.wait(fade_duration)
        elif remaining_hold > 0:
            self.wait(remaining_hold)

        # Ensure any active transients remaining on screen are queued for clean eviction
        if active_transients:
            for item in active_transients:
                is_on_canvas = item in self.mobjects or (
                    hasattr(item, "get_family") and any(sub in self.mobjects for sub in item.get_family())
                )
                if is_on_canvas and item not in self._pending_transients:
                    self._pending_transients.append(item)

        self.elapsed_time += target_total

    def finalize(self):
        if self._pending_transients:
            to_clear = []
            for m in self._pending_transients:
                if m in self.mobjects and m not in to_clear:
                    to_clear.append(m)
                elif hasattr(m, "get_family"):
                    for sub in m.get_family():
                        if sub in self.mobjects and sub not in to_clear:
                            to_clear.append(sub)
            if to_clear:
                self.remove(*to_clear)
            self._pending_transients.clear()

        actual_time = self.time
        diff = abs(actual_time - self.target_duration)
        if diff > 0.25:
            print(f"⚠️ DURATION CHECK: Actual = {actual_time:.2f}s | Target = {self.target_duration:.2f}s (Diff: {diff:.2f}s)")
        else:
            print(f"✅ RUNTIME PERFECT: {actual_time:.2f}s (Target: {self.target_duration:.2f}s)")


EditorialScene = InfographicScene

__all__ = [
    "EditorialScene",
    "InfographicScene",
    "InfographicThreeDScene",
    "BROADCAST_SAFE_X",
    "BROADCAST_SAFE_Y",
    "EASINGS",
    "ease_in_quad",
    "ease_out_quad",
    "ease_in_out_quad",
    "ease_in_cubic",
    "ease_out_cubic",
    "ease_in_out_cubic",
    "ease_in_sine",
    "ease_out_sine",
    "ease_in_out_sine",
    "ease_overshoot",
    "ease_heavy_inertia",
    "ease_light_snap",
]
