import argparse
import json
import re
import sys
from pathlib import Path

parser = argparse.ArgumentParser(
    description="Validate storyboard JSON structure and narration-anchor integrity."
)
parser.add_argument(
    "storyboard",
    nargs="?",
    default="blueprints/test_satellite_storyboard.json",
    help="Path to storyboard JSON."
)
parser.add_argument(
    "--require-premium",
    action="store_true",
    help="Require the complete premium Visual Director schema; do not accept legacy storyboards."
)
parser.add_argument(
    "--untimed",
    action="store_true",
    help="Reject timing fields; use this for Master Prompt 1 output before audio alignment."
)
args = parser.parse_args()
path = Path(args.storyboard)

errors = []
warnings = []

try:
    data = json.loads(path.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError) as exc:
    print(f"FAIL: Cannot read valid JSON: {exc}")
    raise SystemExit(1)

if not isinstance(data, dict):
    print("FAIL: Root JSON value must be an object.")
    raise SystemExit(1)

if not isinstance(data.get("project"), str) or not data["project"].strip():
    errors.append("'project' must be a non-empty string.")

scenes = data.get("scenes")
if not isinstance(scenes, list):
    errors.append("'scenes' must be an array.")
    scenes = []

total_scenes = data.get("total_scenes")
if (
    not isinstance(total_scenes, int)
    or isinstance(total_scenes, bool)
    or total_scenes != len(scenes)
):
    errors.append("'total_scenes' must be an integer matching scenes array length.")

allowed_environments = {
    "SurfaceGround", "MacroHorizon", "ParticleField", "FlowAxes"
}
allowed_archetypes = {
    "Establishment",
    "Continuous Physics",
    "Morph / Scale Shift",
    "Physical Reaction / Resonance",
    "Telemetry Lock",
    "Focal Resolution",
}
allowed_strategies = {
    "Cinematic 3D Reveal",
    "3D Cutaway / Internal Anatomy",
    "Exploded View / Assembly",
    "Spatial Simulation",
    "Macro-to-Micro Journey",
    "Technical Schematic",
    "Process / Flow Diagram",
    "Data Visualization / Telemetry",
    "Timeline / Historical Reconstruction",
    "Mathematical / Abstract Visualization",
    "Hybrid Explanatory Sequence",
}
premium_scene_fields = {
    "visual_strategy", "visual_rationale", "learning_goal", "visual_style",
    "palette", "composition_plan", "camera_language", "transition_in", "transition_out",
}
required_scene_fields = {
    "scene_id", "title", "environment", "environment_intent",
    "visual_strategy", "visual_rationale", "learning_goal", "visual_style",
    "palette", "composition_plan", "camera_language", "transition_in", "transition_out",
    "beats",
}
required_beat_fields = {"beat_id", "full_sentence", "visual_sub_beats"}
required_subbeat_fields = {
    "sub_beat_id", "narration_anchor", "kinetic_archetype",
    "actors_involved", "visual_action",
}
snake_case = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")
palette_string_fields = {
    "background_color", "primary_text_color", "secondary_text_color",
    "accent_color", "motion_or_signal_color", "highlight_color",
    "muted_or_inactive_color", "outline_and_annotation_color",
}
palette_array_fields = {"primary_object_colors", "secondary_object_colors"}


def valid_hex_color(value):
    return (
        isinstance(value, str)
        and re.fullmatch(r"#[0-9A-Fa-f]{6}", value) is not None
    )

is_premium = args.require_premium or any(
    isinstance(scene, dict) and bool(premium_scene_fields & scene.keys())
    for scene in scenes
)
mode = "premium-required" if args.require_premium else (
    "premium" if is_premium else "legacy-compatible"
)

if args.untimed:
    timing_fields = {
        "master_audio_total_duration", "audio_start_time", "audio_end_time",
        "total_duration", "start_time", "end_time", "duration",
        "motion_time", "hold_time",
    }

    def find_timing_fields(value, location="$"):
        if isinstance(value, dict):
            for key, child in value.items():
                child_location = f"{location}.{key}"
                if key in timing_fields:
                    errors.append(
                        f"{child_location}: timing field is not allowed in untimed storyboard output."
                    )
                find_timing_fields(child, child_location)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                find_timing_fields(child, f"{location}[{index}]")

    find_timing_fields(data)

if not scenes:
    errors.append("Storyboard must contain at least one scene.")

scene_ids = set()
beat_ids = set()
beat_count = 0
subbeat_count = 0

for si, scene in enumerate(scenes, 1):
    prefix = f"scene[{si}]"

    if not isinstance(scene, dict):
        errors.append(f"{prefix} must be an object.")
        continue

    if is_premium:
        missing = required_scene_fields - scene.keys()
        for field in sorted(missing):
            errors.append(f"{prefix}: missing required premium field {field!r}.")

    scene_id = scene.get("scene_id")
    if not isinstance(scene_id, str) or not scene_id.strip():
        errors.append(f"{prefix}: missing valid scene_id.")
    elif scene_id in scene_ids:
        errors.append(f"{prefix}: duplicate scene_id {scene_id!r}.")
    else:
        scene_ids.add(scene_id)

    for field in ("title", "environment_intent"):
        if not isinstance(scene.get(field), str) or not scene[field].strip():
            errors.append(f"{prefix}: {field} must be a non-empty string.")

    if scene.get("environment") not in allowed_environments:
        errors.append(f"{prefix}: invalid environment.")

    if is_premium:
        for field in required_scene_fields - {
            "scene_id", "title", "environment", "environment_intent", "beats",
            "palette",
        }:
            if field in scene and (
                not isinstance(scene[field], str) or not scene[field].strip()
            ):
                errors.append(f"{prefix}: {field} must be a non-empty string.")

        if scene.get("visual_strategy") not in allowed_strategies:
            errors.append(f"{prefix}: invalid visual_strategy.")

        palette = scene.get("palette")
        if not isinstance(palette, dict):
            errors.append(f"{prefix}: palette must be an object.")
        else:
            required_palette_fields = palette_string_fields | palette_array_fields
            missing_palette_fields = required_palette_fields - palette.keys()
            for field in sorted(missing_palette_fields):
                errors.append(f"{prefix}.palette: missing required field {field!r}.")

            for field in sorted(palette_string_fields & palette.keys()):
                if not valid_hex_color(palette[field]):
                    errors.append(
                        f"{prefix}.palette.{field}: must be a six-digit hex color."
                    )

            for field in sorted(palette_array_fields & palette.keys()):
                colors = palette[field]
                if (
                    not isinstance(colors, list)
                    or not colors
                    or not all(valid_hex_color(color) for color in colors)
                ):
                    errors.append(
                        f"{prefix}.palette.{field}: must be a non-empty array "
                        "of six-digit hex colors."
                    )

    beats = scene.get("beats")
    if not isinstance(beats, list) or not beats:
        errors.append(f"{prefix}: beats must be a non-empty array.")
        continue

    for bi, beat in enumerate(beats, 1):
        beat_count += 1
        bp = f"{prefix}.beat[{bi}]"

        if not isinstance(beat, dict):
            errors.append(f"{bp} must be an object.")
            continue

        if is_premium:
            for field in sorted(required_beat_fields - beat.keys()):
                errors.append(f"{bp}: missing required field {field!r}.")

        beat_id = beat.get("beat_id")
        if is_premium:
            if not isinstance(beat_id, str) or not beat_id.strip():
                errors.append(f"{bp}: beat_id must be a non-empty string.")
            elif beat_id in beat_ids:
                errors.append(f"{bp}: duplicate project-wide beat_id {beat_id!r}.")
            else:
                beat_ids.add(beat_id)
        else:
            if (
                isinstance(beat_id, bool)
                or not isinstance(beat_id, (str, int))
                or (isinstance(beat_id, str) and not beat_id.strip())
            ):
                errors.append(f"{bp}: legacy beat_id must be a non-empty string or integer.")
            elif str(beat_id) in beat_ids:
                errors.append(f"{bp}: duplicate project-wide beat_id {beat_id!r}.")
            else:
                beat_ids.add(str(beat_id))

        sentence = beat.get("full_sentence")
        subbeats = beat.get("visual_sub_beats")

        if not isinstance(sentence, str) or not sentence:
            errors.append(f"{bp}: full_sentence must be a non-empty string.")
            sentence = ""

        if not isinstance(subbeats, list) or not subbeats:
            errors.append(f"{bp}: visual_sub_beats must be a non-empty array.")
            continue

        anchors = []
        subbeat_ids = set()

        for ui, subbeat in enumerate(subbeats, 1):
            subbeat_count += 1
            up = f"{bp}.visual_sub_beats[{ui}]"

            if not isinstance(subbeat, dict):
                errors.append(f"{up} must be an object.")
                continue

            if is_premium:
                for field in sorted(required_subbeat_fields - subbeat.keys()):
                    errors.append(f"{up}: missing required field {field!r}.")

            sub_id = subbeat.get("sub_beat_id")
            if not isinstance(sub_id, str) or not sub_id.strip():
                errors.append(f"{up}: invalid sub_beat_id.")
            elif sub_id in subbeat_ids:
                errors.append(f"{up}: duplicate sub_beat_id {sub_id!r}.")
            else:
                subbeat_ids.add(sub_id)

            anchor = subbeat.get("narration_anchor")
            if not isinstance(anchor, str):
                errors.append(f"{up}: narration_anchor must be a string.")
            else:
                anchors.append(anchor)

            if subbeat.get("kinetic_archetype") not in allowed_archetypes:
                errors.append(f"{up}: invalid kinetic_archetype.")

            actors = subbeat.get("actors_involved")
            if not isinstance(actors, list) or not all(
                isinstance(actor, str) and actor.strip() for actor in actors
            ):
                errors.append(f"{up}: actors_involved must be an array of non-empty strings.")
            elif is_premium:
                for actor in actors:
                    if not snake_case.fullmatch(actor):
                        errors.append(
                            f"{up}: actor identifier {actor!r} must use snake_case."
                        )

            action = subbeat.get("visual_action")
            if not isinstance(action, str) or not action.strip():
                errors.append(f"{up}: visual_action must be a non-empty string.")

        if "".join(anchors) != sentence:
            errors.append(
                f"{bp}: narration anchors do not reconstruct full_sentence exactly."
            )

print(f"File: {path}")
print(f"Mode: {mode}")
print(f"Scenes: {len(scenes)}")
print(f"Beats: {beat_count}")
print(f"Visual sub-beats: {subbeat_count}")
print(f"Errors: {len(errors)}")
print(f"Warnings: {len(warnings)}")

for error in errors:
    print(f"ERROR: {error}")

for warning in warnings:
    print(f"WARNING: {warning}")

if errors:
    print("RESULT: FAIL")
    raise SystemExit(1)

print("RESULT: PASS")
