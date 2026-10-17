#!/usr/bin/env python3
"""Validate timed storyboard JSON without modifying the source file."""

import argparse
import json
import math
import sys
from pathlib import Path


def close(a, b, tolerance):
    return math.isclose(a, b, rel_tol=0.0, abs_tol=tolerance)


def number(value):
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


class TimingValidator:
    def __init__(self, tolerance=0.15, long_hold=2.0):
        self.tolerance = tolerance
        self.long_hold = long_hold
        self.errors = 0
        self.warnings = 0
        self.checks = 0

    def error(self, message):
        self.errors += 1
        print(f"ERROR: {message}")

    def warning(self, message):
        self.warnings += 1
        print(f"WARNING: {message}")

    def check_duration(self, label, actual, expected):
        self.checks += 1
        if not close(actual, expected, self.tolerance):
            self.error(
                f"{label}: duration {actual:.3f}s does not match "
                f"expected {expected:.3f}s "
                f"(tolerance ±{self.tolerance:.3f}s)"
            )

    def validate_interval(self, obj, label):
        """Return (start, end, duration), or None if required fields are invalid."""
        start = obj.get("start_time")
        end = obj.get("end_time")
        duration = obj.get("duration")

        valid = True
        for field, value in (
            ("start_time", start),
            ("end_time", end),
            ("duration", duration),
        ):
            if not number(value):
                self.error(f"{label}: missing or invalid {field}")
                valid = False

        if not valid:
            return None

        if start < 0:
            self.error(f"{label}: start_time cannot be negative")

        if end < start:
            self.error(f"{label}: end_time is earlier than start_time")
            return None

        self.check_duration(f"{label} (end - start)", end - start, duration)
        return start, end, duration

    def validate_subbeat(self, subbeat, label):
        interval = self.validate_interval(subbeat, label)
        if interval is None:
            return None

        start, end, duration = interval
        motion = subbeat.get("motion_time")
        hold = subbeat.get("hold_time")

        if not number(motion):
            self.error(f"{label}: missing or invalid motion_time")
        elif motion < 0:
            self.error(f"{label}: motion_time cannot be negative")

        if not number(hold):
            self.error(f"{label}: missing or invalid hold_time")
        elif hold < 0:
            self.error(f"{label}: hold_time cannot be negative")

        if number(motion) and number(hold):
            self.check_duration(
                f"{label} (motion_time + hold_time)",
                motion + hold,
                duration,
            )

        if number(hold) and hold > self.long_hold:
            reason = (
                subbeat.get("hold_reason")
                or subbeat.get("reason")
                or subbeat.get("activity_during_hold")
            )
            suffix = (
                f" Reason/activity: {reason}"
                if reason
                else " Consider adding ongoing visual activity or a reason."
            )
            self.warning(
                f"{label}: hold_time is {hold:.2f}s "
                f"(over {self.long_hold:.2f}s).{suffix}"
            )

        return start, end, duration

    def validate_sequence(self, items, label, expected_start=None,
                          expected_end=None):
        """Check ordering and unexpected gaps/overlaps in timed children."""
        intervals = []

        for index, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                self.error(f"{label} item {index} is not an object")
                continue
            interval = self.validate_interval(
                item, f"{label} item {index}"
            )
            if interval is not None:
                intervals.append((interval[0], interval[1], index))

        intervals.sort(key=lambda x: x[0])

        for previous, current in zip(intervals, intervals[1:]):
            prev_start, prev_end, prev_index = previous
            cur_start, cur_end, cur_index = current

            if cur_start < prev_end - self.tolerance:
                self.error(
                    f"{label}: item {cur_index} overlaps item "
                    f"{prev_index} ({cur_start:.2f}s < {prev_end:.2f}s)"
                )
            elif cur_start > prev_end + self.tolerance:
                self.warning(
                    f"{label}: gap between item {prev_index} and "
                    f"item {cur_index}: {cur_start - prev_end:.2f}s"
                )

        if intervals and expected_start is not None:
            first_start = intervals[0][0]
            if first_start > expected_start + self.tolerance:
                self.warning(
                    f"{label}: starts {first_start - expected_start:.2f}s "
                    f"after its parent's start"
                )

        if intervals and expected_end is not None:
            last_end = intervals[-1][1]
            if last_end < expected_end - self.tolerance:
                self.warning(
                    f"{label}: ends {expected_end - last_end:.2f}s "
                    f"before its parent's end"
                )

    def validate_storyboard(self, data):
        if not isinstance(data, dict):
            self.error("Root JSON value must be an object")
            return

        master_duration = data.get("master_audio_total_duration")
        if master_duration is not None and (
            not number(master_duration) or master_duration <= 0
        ):
            self.error("master_audio_total_duration must be a positive number")
            master_duration = None

        scenes = data.get("scenes")
        if not isinstance(scenes, list) or not scenes:
            self.error("Root must contain a non-empty 'scenes' array")
            return

        scene_intervals = []

        for scene_index, scene in enumerate(scenes, start=1):
            if not isinstance(scene, dict):
                self.error(f"Scene {scene_index} is not an object")
                continue

            scene_id = scene.get("scene_id", f"scene_{scene_index}")
            label = f"Scene {scene_id}"

            scene_start = scene.get("audio_start_time")
            scene_end = scene.get("audio_end_time")
            scene_duration = scene.get("total_duration")

            fields_valid = all(
                number(v)
                for v in (scene_start, scene_end, scene_duration)
            )
            if not fields_valid:
                self.error(
                    f"{label}: audio_start_time, audio_end_time, "
                    "and total_duration must all be numbers"
                )
            else:
                if scene_start < 0 or scene_end < scene_start:
                    self.error(f"{label}: invalid audio start/end times")
                self.check_duration(
                    f"{label} (audio_end_time - audio_start_time)",
                    scene_end - scene_start,
                    scene_duration,
                )
                scene_intervals.append(
                    (scene_start, scene_end, scene_id)
                )

                if master_duration is not None:
                    if scene_end > master_duration + self.tolerance:
                        self.error(
                            f"{label}: ends at {scene_end:.2f}s, beyond "
                            f"master audio duration {master_duration:.2f}s"
                        )

            beats = scene.get("beats")
            if not isinstance(beats, list) or not beats:
                self.error(f"{label}: missing or empty 'beats' array")
                continue

            beat_intervals = []

            for beat_index, beat in enumerate(beats, start=1):
                if not isinstance(beat, dict):
                    self.error(f"{label}: beat {beat_index} is not an object")
                    continue

                beat_id = beat.get("beat_id", f"beat_{beat_index}")
                beat_label = f"{label}, beat {beat_id}"
                beat_interval = self.validate_interval(beat, beat_label)

                if beat_interval is not None:
                    beat_start, beat_end, beat_duration = beat_interval
                    beat_intervals.append(
                        (beat_start, beat_end, beat_index)
                    )

                    if fields_valid:
                        if beat_start < scene_start - self.tolerance:
                            self.error(f"{beat_label}: starts before its scene")
                        if beat_end > scene_end + self.tolerance:
                            self.error(f"{beat_label}: ends after its scene")

                # Support both the existing pipeline schema and the
                # normalized schema used by newer pipeline components.
                subbeats = beat.get("visual_sub_beats")
                if subbeats is None:
                    subbeats = beat.get("sub_beats")
                if subbeats is None:
                    subbeats = beat.get("subbeats")

                if not isinstance(subbeats, list) or not subbeats:
                    self.error(
                        f"{beat_label}: missing or empty 'sub_beats' array"
                    )
                    continue

                subbeat_intervals = []
                for sub_index, subbeat in enumerate(subbeats, start=1):
                    if not isinstance(subbeat, dict):
                        self.error(
                            f"{beat_label}: sub-beat {sub_index} "
                            "is not an object"
                        )
                        continue

                    sub_id = subbeat.get(
                        "sub_beat_id", f"subbeat_{sub_index}"
                    )
                    sub_label = f"{beat_label}, sub-beat {sub_id}"
                    interval = self.validate_subbeat(subbeat, sub_label)
                    if interval is not None:
                        subbeat_intervals.append(
                            (interval[0], interval[1], sub_index)
                        )

                        if beat_interval is not None:
                            if interval[0] < beat_interval[0] - self.tolerance:
                                self.error(
                                    f"{sub_label}: starts before its beat"
                                )
                            if interval[1] > beat_interval[1] + self.tolerance:
                                self.error(
                                    f"{sub_label}: ends after its beat"
                                )

                self.validate_sequence(
                    subbeats,
                    f"{beat_label} sub-beats",
                    expected_start=beat_interval[0] if beat_interval else None,
                    expected_end=beat_interval[1] if beat_interval else None,
                )

                if beat_interval is not None:
                    valid_subbeats = [
                        s for s in subbeats if isinstance(s, dict)
                    ]
                    if valid_subbeats and all(
                        number(s.get("duration")) for s in valid_subbeats
                    ):
                        self.check_duration(
                            f"{beat_label} (sum of sub-beat durations)",
                            sum(s["duration"] for s in valid_subbeats),
                            beat_interval[2],
                        )

            self.validate_sequence(
                beats,
                f"{label} beats",
                expected_start=scene_start if fields_valid else None,
                expected_end=scene_end if fields_valid else None,
            )

            valid_beats = [b for b in beats if isinstance(b, dict)]
            if valid_beats and all(
                number(b.get("duration")) for b in valid_beats
            ) and fields_valid:
                self.check_duration(
                    f"{label} (sum of beat durations)",
                    sum(b["duration"] for b in valid_beats),
                    scene_duration,
                )

        scene_intervals.sort(key=lambda x: x[0])
        for previous, current in zip(scene_intervals, scene_intervals[1:]):
            if current[0] < previous[1] - self.tolerance:
                self.error(
                    f"Scene {current[2]} overlaps scene {previous[2]}"
                )
            elif current[0] > previous[1] + self.tolerance:
                self.warning(
                    f"Gap between scene {previous[2]} and scene "
                    f"{current[2]}: {current[0] - previous[1]:.2f}s"
                )

        if master_duration is not None and scene_intervals:
            last_scene_end = max(end for _, end, _ in scene_intervals)
            if last_scene_end < master_duration - self.tolerance:
                self.warning(
                    f"Last scene ends {master_duration - last_scene_end:.2f}s "
                    "before the master audio ends"
                )

    def report(self):
        print("\n--- Timing validation summary ---")
        print(f"Checks performed: {self.checks}")
        print(f"Errors:            {self.errors}")
        print(f"Warnings:          {self.warnings}")

        if self.errors:
            print("RESULT: FAIL")
            return 1

        print("RESULT: PASS (warnings may still need review)")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description="Validate timed storyboard JSON without modifying it."
    )
    parser.add_argument(
        "storyboard",
        nargs="?",
        default="blueprints/timed_storyboard.json",
        help="Path to timed storyboard JSON",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=0.15,
        help="Allowed duration difference in seconds (default: 0.15)",
    )
    parser.add_argument(
        "--long-hold",
        type=float,
        default=2.0,
        help="Warn when hold_time exceeds this many seconds (default: 2.0)",
    )
    args = parser.parse_args()

    if args.tolerance < 0 or args.long_hold < 0:
        parser.error("--tolerance and --long-hold must be non-negative")

    path = Path(args.storyboard)
    if not path.is_file():
        print(f"ERROR: Storyboard file not found: {path}", file=sys.stderr)
        print(
            "Tip: pass the path explicitly, for example:\n"
            "  python scripts/validate_timing.py blueprints/my_storyboard.json",
            file=sys.stderr,
        )
        return 2

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        print(
            f"ERROR: Invalid JSON in {path}, line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}",
            file=sys.stderr,
        )
        return 2
    except OSError as exc:
        print(f"ERROR: Cannot read {path}: {exc}", file=sys.stderr)
        return 2

    print(f"Validating: {path}")
    print(f"Allowed duration tolerance: ±{args.tolerance:.2f}s")
    print(f"Long-hold warning threshold: {args.long_hold:.2f}s\n")

    validator = TimingValidator(
        tolerance=args.tolerance,
        long_hold=args.long_hold,
    )
    validator.validate_storyboard(data)
    return validator.report()


if __name__ == "__main__":
    sys.exit(main())
