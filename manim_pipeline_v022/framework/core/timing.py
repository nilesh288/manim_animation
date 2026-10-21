"""Strict scene timing contract shared by 2D and 3D scene bases."""

import math

from manim import Animation, config


class TimingContractMixin:
    """Budget every beat and fail fast when generated animation overruns it.

    A scene must set self.target_duration before calling finalize().
    Timed action functions should spend exactly motion_time in animations;
    hold_time is the remaining intentional viewing time.
    """

    timing_tolerance = 0.05

    def initialize_timing_contract(self):
        self.elapsed_time = 0.0
        self.target_duration = 0.0
        self._last_beat_description = ""

    def beat(self, motion_time, hold_time, action=None, description=""):
        values = (motion_time, hold_time)
        if any(
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(float(value))
            or float(value) < 0
            for value in values
        ):
            raise ValueError(
                f"Beat timing must be finite, non-negative numbers; "
                f"got motion_time={motion_time!r}, hold_time={hold_time!r}."
            )

        motion_time = float(motion_time)
        hold_time = float(hold_time)
        budget = motion_time + hold_time
        start_time = float(self.time)
        self._last_beat_description = description or "unnamed beat"

        if callable(action):
            action()
        elif isinstance(action, Animation):
            if motion_time <= 0:
                raise RuntimeError(
                    f"{self._last_beat_description}: animation supplied with "
                    "zero motion_time."
                )
            self.play(action, run_time=motion_time)
        elif isinstance(action, (list, tuple)):
            if action:
                if motion_time <= 0:
                    raise RuntimeError(
                        f"{self._last_beat_description}: animations supplied "
                        "with zero motion_time."
                    )
                self.play(*action, run_time=motion_time)
        elif action is not None:
            raise TypeError(
                f"{self._last_beat_description}: action must be callable, "
                "an Animation, a sequence of Animations, or None."
            )

        action_elapsed = float(self.time) - start_time
        tolerance = self.timing_tolerance

        if action_elapsed > motion_time + tolerance:
            raise RuntimeError(
                f"TIMING OVERRUN in {self._last_beat_description}: action "
                f"used {action_elapsed:.3f}s but motion_time is "
                f"{motion_time:.3f}s."
            )

        if motion_time > tolerance and action_elapsed < motion_time - tolerance:
            raise RuntimeError(
                f"TIMING UNDERRUN in {self._last_beat_description}: action "
                f"used {action_elapsed:.3f}s but motion_time is "
                f"{motion_time:.3f}s. Add the missing animation time or "
                "correct the storyboard timing."
            )

        remaining = budget - action_elapsed
        if remaining > 0.001:
            self.wait(remaining)

        self.elapsed_time += budget

    def finalize(self):
        target = getattr(self, "target_duration", 0.0)
        if (
            isinstance(target, bool)
            or not isinstance(target, (int, float))
            or not math.isfinite(float(target))
            or float(target) <= 0
        ):
            raise RuntimeError(
                "Set a positive numeric self.target_duration from the timed "
                "storyboard before calling finalize()."
            )

        target = float(target)
        frame_rate = float(config.frame_rate)
        frame_tolerance = (1.0 / frame_rate + 0.001) if frame_rate > 0 else 0.0
        actual = float(self.time)
        difference = actual - target

        # Correct a one-frame shortfall instead of merely accepting it.
        if difference < -0.001 and difference >= -frame_tolerance:
            self.wait(-difference)
            actual = float(self.time)
            difference = actual - target

        if abs(difference) > 0.001:
            raise RuntimeError(
                "FINAL TIMING MISMATCH after frame correction: rendered "
                f"scene time is {actual:.3f}s; storyboard target is "
                f"{target:.3f}s (difference {difference:+.3f}s)."
            )

        print(
            f"[TIMING PASS] actual={actual:.3f}s "
            f"target={target:.3f}s difference={difference:+.3f}s"
        )
