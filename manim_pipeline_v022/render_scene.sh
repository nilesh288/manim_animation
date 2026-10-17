#!/usr/bin/env bash
set -Eeuo pipefail

# Usage:
# ./render_scene.sh SCENE_FILE CLASS_NAME STORYBOARD_JSON SCENE_ID [preview|final]

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

SCENE_FILE="${1:-}"
CLASS_NAME="${2:-}"
STORYBOARD="${3:-}"
SCENE_ID="${4:-}"
MODE="${5:-preview}"

if [[ -z "$SCENE_FILE" || -z "$CLASS_NAME" || -z "$STORYBOARD" || -z "$SCENE_ID" ]]; then
    echo "Usage: $0 SCENE_FILE CLASS_NAME STORYBOARD_JSON SCENE_ID [preview|final]"
    exit 2
fi

[[ -f "$SCENE_FILE" ]] || { echo "ERROR: Scene file not found: $SCENE_FILE"; exit 2; }
[[ -f "$STORYBOARD" ]] || { echo "ERROR: Storyboard not found: $STORYBOARD"; exit 2; }
[[ -f "config.json" ]] || { echo "ERROR: config.json not found"; exit 2; }

case "$MODE" in
    preview)
        WIDTH=854
        HEIGHT=480
        FPS=15
        ;;
    final)
        WIDTH=1920
        HEIGHT=1080
        FPS=30
        ;;
    *)
        echo "ERROR: Mode must be preview or final."
        exit 2
        ;;
esac

TEMP_BASE="$(python -c 'import json; print(json.load(open("config.json"))["paths"]["temporary_render"])')"
TOLERANCE="$(python -c 'import json; print(json.load(open("config.json"))["timing"]["duration_tolerance_seconds"])')"
LONG_HOLD="$(python -c 'import json; print(json.load(open("config.json"))["timing"]["long_hold_warning_seconds"])')"

if [[ ! -d /dev/shm ]]; then
    echo "ERROR: /dev/shm is unavailable."
    exit 2
fi

mkdir -p "$TEMP_BASE" render_output logs
RUN_DIR="$(mktemp -d "$TEMP_BASE/run_XXXXXX")"
LOG_FILE="logs/render_$(basename "$SCENE_FILE" .py)_${MODE}_$(date +%Y%m%d_%H%M%S).log"

cleanup() {
    if [[ -n "${RUN_DIR:-}" && -d "$RUN_DIR" ]]; then
        rm -rf -- "$RUN_DIR"
    fi
}
trap cleanup EXIT

echo "===== MANIM VERSION ====="
manim --version
MANIM_VERSION="$(manim --version 2>&1)"
if ! grep -Eq 'v0\.22\.' <<< "$MANIM_VERSION"; then
    echo "ERROR: This project requires Manim Community v0.22.x."
    exit 1
fi

echo
echo "===== PYTHON SYNTAX (NO BYTECODE FILE) ====="
python - "$SCENE_FILE" <<'PYTHON'
import ast
import pathlib
import sys

scene_path = pathlib.Path(sys.argv[1])
try:
    ast.parse(scene_path.read_text(encoding="utf-8"), filename=str(scene_path))
except (SyntaxError, UnicodeDecodeError) as exc:
    print(f"ERROR: Python syntax check failed: {exc}", file=sys.stderr)
    raise SystemExit(1)

print(f"PASS: Python syntax is valid: {scene_path}")
PYTHON

echo
echo "===== STORYBOARD STRUCTURE VALIDATION ====="
python scripts/validate_storyboard.py "$STORYBOARD"

echo
echo "===== STORYBOARD TIMING VALIDATION ====="
python scripts/validate_timing.py "$STORYBOARD" \
    --tolerance "$TOLERANCE" --long-hold "$LONG_HOLD"

echo
echo "===== CHECK SCENE ID AND TARGET DURATION ====="
EXPECTED_DURATION="$(python - "$STORYBOARD" "$SCENE_ID" <<'PY'
import json
import sys

path, scene_id = sys.argv[1:3]
with open(path, encoding="utf-8") as f:
    data = json.load(f)

matches = [s for s in data.get("scenes", []) if s.get("scene_id") == scene_id]
if len(matches) != 1:
    raise SystemExit(f"Expected exactly one scene with scene_id={scene_id!r}; found {len(matches)}")

duration = float(matches[0]["total_duration"])
if duration <= 0:
    raise SystemExit(f"Invalid scene duration: {duration}")

print(f"{duration:.6f}")
PY
)"

echo "Scene ID: $SCENE_ID"
echo "Target duration: ${EXPECTED_DURATION}s"
echo "Mode: $MODE (${WIDTH}x${HEIGHT} @ ${FPS} FPS)"

echo
echo "===== RENDER TO TEMPORARY STORAGE ====="
set +e
PYTHONPATH="$ROOT:$ROOT/engine${PYTHONPATH:+:$PYTHONPATH}" \
    manim "$SCENE_FILE" "$CLASS_NAME" \
    --media_dir "$RUN_DIR" \
    --resolution "${WIDTH},${HEIGHT}" \
    --fps "$FPS" 2>&1 | tee "$LOG_FILE"
RENDER_STATUS=${PIPESTATUS[0]}
set -e

if [[ "$RENDER_STATUS" -ne 0 ]]; then
    echo "ERROR: Manim render failed (exit $RENDER_STATUS)."
    exit "$RENDER_STATUS"
fi

echo
echo "===== LOCATE RENDERED MP4 ====="
mapfile -t VIDEOS < <(
    find "$RUN_DIR/videos" -type f -name "${CLASS_NAME}.mp4" \
        ! -path '*/partial_movie_files/*' -print
)

if [[ "${#VIDEOS[@]}" -ne 1 ]]; then
    echo "ERROR: Expected exactly one final MP4 for $CLASS_NAME; found ${#VIDEOS[@]}."
    find "$RUN_DIR/videos" -type f -name '*.mp4' -print || true
    exit 1
fi

VIDEO="${VIDEOS[0]}"

echo
echo "===== VERIFY VIDEO METADATA AND DURATION ====="
ACTUAL_DURATION="$(ffprobe -v error -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 "$VIDEO")"

python - "$EXPECTED_DURATION" "$ACTUAL_DURATION" "$TOLERANCE" <<'PY'
import sys

expected, actual, tolerance = map(float, sys.argv[1:4])
difference = abs(expected - actual)
print(f"Expected duration: {expected:.3f}s")
print(f"Actual duration:   {actual:.3f}s")
print(f"Difference:        {difference:.3f}s")
print(f"Allowed tolerance: {tolerance:.3f}s")
if difference > tolerance:
    raise SystemExit("FAIL: Rendered duration is outside the configured tolerance.")
print("PASS: Rendered duration is within tolerance.")
PY

ffprobe -v error \
    -show_entries stream=width,height,r_frame_rate \
    -show_entries format=duration,size \
    -of default=noprint_wrappers=1 "$VIDEO"

echo
echo "===== COPY VERIFIED VIDEO TO PERMANENT STORAGE ====="
DEST_DIR="render_output/$MODE"
mkdir -p "$DEST_DIR"
DEST="$DEST_DIR/${SCENE_ID}.mp4"
cp -- "$VIDEO" "$DEST"
sync -f "$DEST" 2>/dev/null || true

echo "SUCCESS: $DEST"
echo "Render log: $LOG_FILE"
