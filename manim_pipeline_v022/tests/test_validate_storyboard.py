import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_storyboard.py"
BLUEPRINTS = ROOT / "blueprints"
PYTHON = Path.home() / "manim-env" / "bin" / "python"


class StoryboardValidatorTests(unittest.TestCase):
    def run_validator(self, data_or_path, *options):
        temp_path = None

        if isinstance(data_or_path, Path):
            storyboard_path = data_or_path
        else:
            handle = tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", encoding="utf-8", delete=False
            )
            json.dump(data_or_path, handle)
            handle.close()
            temp_path = Path(handle.name)
            storyboard_path = temp_path

        try:
            return subprocess.run(
                [str(PYTHON), str(VALIDATOR), str(storyboard_path), *options],
                capture_output=True,
                text=True,
                check=False,
            )
        finally:
            if temp_path:
                temp_path.unlink(missing_ok=True)

    def load(self, filename):
        return json.loads((BLUEPRINTS / filename).read_text(encoding="utf-8"))

    def assert_valid(self, filename, *options):
        result = self.run_validator(BLUEPRINTS / filename, *options)
        self.assertEqual(
            result.returncode, 0,
            f"{filename} should pass:\n{result.stdout}\n{result.stderr}",
        )
        self.assertIn("RESULT: PASS", result.stdout)

    def assert_invalid(self, data, expected_error, *options):
        result = self.run_validator(data, *options)
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn(expected_error, output)

    # Existing real-world fixtures
    def test_premium_fixture(self):
        self.assert_valid("jet_engine_storyboard.json", "--require-premium")

    def test_timed_premium_fixture(self):
        self.assert_valid(
            "jet_engine_storyboard_timed.json", "--require-premium"
        )

    def test_legacy_magnetic_braking_fixture(self):
        self.assert_valid("magnetic_braking_storyboard.json")

    def test_legacy_satellite_fixture(self):
        self.assert_valid("test_satellite_storyboard.json")

    # Schema and identity regressions
    def test_boolean_scene_count_is_rejected(self):
        data = self.load("jet_engine_storyboard.json")
        data["total_scenes"] = True
        self.assert_invalid(data, "'total_scenes' must be an integer")

    def test_duplicate_scene_id_is_rejected(self):
        data = self.load("jet_engine_storyboard.json")
        data["scenes"][1]["scene_id"] = data["scenes"][0]["scene_id"]
        self.assert_invalid(data, "duplicate scene_id", "--require-premium")

    def test_duplicate_project_wide_beat_id_is_rejected(self):
        data = self.load("jet_engine_storyboard.json")
        self.assertGreaterEqual(len(data["scenes"]), 2)
        first = data["scenes"][0]["beats"][0]["beat_id"]
        data["scenes"][1]["beats"][0]["beat_id"] = first
        self.assert_invalid(
            data, "duplicate project-wide beat_id", "--require-premium"
        )

    def test_duplicate_subbeat_id_within_beat_is_rejected(self):
        data = self.load("jet_engine_storyboard.json")
        beat = data["scenes"][0]["beats"][0]
        duplicate = copy.deepcopy(beat["visual_sub_beats"][0])
        beat["visual_sub_beats"].append(duplicate)
        self.assert_invalid(data, "duplicate sub_beat_id", "--require-premium")

    def test_invalid_environment_is_rejected(self):
        data = self.load("jet_engine_storyboard.json")
        data["scenes"][0]["environment"] = "UnknownEnvironment"
        self.assert_invalid(data, "invalid environment", "--require-premium")

    def test_invalid_visual_strategy_is_rejected(self):
        data = self.load("jet_engine_storyboard.json")
        data["scenes"][0]["visual_strategy"] = "Unsupported Strategy"
        self.assert_invalid(data, "invalid visual_strategy", "--require-premium")

    def test_invalid_kinetic_archetype_is_rejected(self):
        data = self.load("jet_engine_storyboard.json")
        data["scenes"][0]["beats"][0]["visual_sub_beats"][0][
            "kinetic_archetype"
        ] = "Unsupported Archetype"
        self.assert_invalid(data, "invalid kinetic_archetype", "--require-premium")

    def test_broken_narration_partition_is_rejected(self):
        data = self.load("jet_engine_storyboard.json")
        data["scenes"][0]["beats"][0]["visual_sub_beats"][0][
            "narration_anchor"
        ] = "BROKEN TEXT"
        self.assert_invalid(
            data, "narration anchors do not reconstruct", "--require-premium"
        )

    def test_non_snake_case_actor_is_rejected(self):
        data = self.load("jet_engine_storyboard.json")
        data["scenes"][0]["beats"][0]["visual_sub_beats"][0][
            "actors_involved"
        ] = ["PrimaryActor"]
        self.assert_invalid(data, "must use snake_case", "--require-premium")

    def test_invalid_palette_color_is_rejected(self):
        data = self.load("jet_engine_storyboard.json")
        data["scenes"][0]["palette"]["background_color"] = "navy"
        self.assert_invalid(
            data, "must be a six-digit hex color", "--require-premium"
        )

    def test_missing_palette_field_is_rejected(self):
        data = self.load("jet_engine_storyboard.json")
        del data["scenes"][0]["palette"]["object_colors"]
        self.assert_invalid(
            data, "missing required field 'object_colors'", "--require-premium"
        )

    def test_unexpected_palette_field_is_rejected(self):
        data = self.load("jet_engine_storyboard.json")
        data["scenes"][0]["palette"]["legacy_color"] = "#FFFFFF"
        self.assert_invalid(
            data, "unexpected field 'legacy_color'", "--require-premium"
        )

    def test_timed_storyboard_is_rejected_in_untimed_mode(self):
        data = self.load("jet_engine_storyboard_timed.json")
        self.assert_invalid(
            data, "timing field is not allowed", "--untimed"
        )

    def test_legacy_fixture_is_rejected_when_premium_required(self):
        result = self.run_validator(
            BLUEPRINTS / "magnetic_braking_storyboard.json",
            "--require-premium",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("RESULT: FAIL", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
