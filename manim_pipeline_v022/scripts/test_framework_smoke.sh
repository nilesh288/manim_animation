#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -d /dev/shm ]]; then
    echo "ERROR: /dev/shm is required so smoke renders do not write temporary video data to the microSD."
    exit 2
fi

VERSION="$(manim --version 2>&1)"
echo "Manim: $VERSION"
if ! grep -Eq 'v0\.22\.' <<< "$VERSION"; then
    echo "ERROR: Framework smoke tests require Manim Community v0.22.x."
    exit 1
fi

TEMP_BASE="/dev/shm/manim_framework_smoke"
mkdir -p "$TEMP_BASE"
RUN_DIR="$(mktemp -d "$TEMP_BASE/run_XXXXXX")"
trap 'rm -rf -- "$RUN_DIR"' EXIT

check_scene() {
    local file="$1"
    local class_name="$2"
    local expected="$3"

    echo
    echo "===== $class_name: SYNTAX ====="
    python - "$file" <<'PYTHON'
import ast
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
print(f"PASS: {path}")
PYTHON

    echo
    echo "===== $class_name: RENDER TO TMPFS ====="
    PYTHONPATH="$ROOT:$ROOT/engine${PYTHONPATH:+:$PYTHONPATH}" \
        manim "$file" "$class_name" \
        --media_dir "$RUN_DIR/$class_name" \
        --resolution 854,480 \
        --fps 15

    mapfile -t videos < <(
        find "$RUN_DIR/$class_name/videos" -type f -name "$class_name.mp4" \
            ! -path '*/partial_movie_files/*' -print
    )
    if [[ "${#videos[@]}" -ne 1 ]]; then
        echo "ERROR: Expected exactly one rendered MP4 for $class_name; found ${#videos[@]}."
        exit 1
    fi

    local actual
    actual="$(ffprobe -v error -show_entries format=duration \
        -of default=noprint_wrappers=1:nokey=1 "${videos[0]}")"

    python - "$expected" "$actual" <<'PYTHON'
import sys

expected, actual = map(float, sys.argv[1:3])
tolerance = 0.15
print(f"Expected duration: {expected:.3f}s")
print(f"Actual duration:   {actual:.3f}s")
if abs(expected - actual) > tolerance:
    raise SystemExit("FAIL: Rendered duration is outside ±0.15s tolerance.")
print("PASS: Render duration")
PYTHON
}

check_scene "scenes/framework_2d_smoke_test.py" "Framework2DSmokeTest" "2.0"
check_scene "scenes/framework_3d_smoke_test.py" "Framework3DSmokeTest" "3.0"

echo
echo "PASS: Both framework smoke renders completed. Temporary outputs will be removed."
