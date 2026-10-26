#!/bin/bash
set -euo pipefail

# ==============================================================================
# render_scene.sh - High-Performance Manim Renderer with RAM Filesystem
# Renders all intermediate partial movie chunks in /dev/shm (tmpfs RAM)
# and persists only the final video to SD card storage (renders/).
# ==============================================================================

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIM_BIN="/home/nilesh/manim-env/bin/manim"
PYTHON_BIN="/home/nilesh/manim-env/bin/python"

SCENE_FILE="${1:-}"
SCENE_CLASS="${2:-}"
QUALITY="${3:--qh}"    # Default: -qh (1080p 60fps) or -ql (480p 15fps)
AUDIO_FILE="${4:-}"

if [[ -z "$SCENE_FILE" || -z "$SCENE_CLASS" ]]; then
    echo "Usage: ./render_scene.sh <scene_file.py> <SceneClass> [quality_flag: -qh|-ql] [optional_audio.mp3]"
    echo "Example: ./render_scene.sh scenes/scene_01_linux_boot.py Scene01 -qh linux_boot_sc1.mp3"
    exit 1
fi

cd "$REPO_DIR"

if [[ "$SCENE_FILE" != /* ]]; then
    SCENE_FILE="$REPO_DIR/$SCENE_FILE"
fi

if [[ ! -f "$SCENE_FILE" ]]; then
    echo "ERROR: Scene file not found: $SCENE_FILE"
    exit 1
fi

# Detect RAM disk (/dev/shm)
USE_RAM=0
RAM_DIR=""
if [[ -d "/dev/shm" && -w "/dev/shm" ]]; then
    FREE_MB=$(df -m /dev/shm | awk 'NR==2 {print $4}')
    if [[ "$FREE_MB" -ge 300 ]]; then
        USE_RAM=1
        RAM_DIR="$(mktemp -d /dev/shm/manim_render_XXXXXX)"
        echo "⚡ RAM Filesystem Active: $RAM_DIR ($FREE_MB MB available in /dev/shm)"
        echo "   (Intermediate chunks written directly to RAM, saving SD card write wear)"
    fi
fi

if [[ "$USE_RAM" -eq 1 ]]; then
    MEDIA_DIR="$RAM_DIR"
else
    MEDIA_DIR="$REPO_DIR/renders"
    echo "💾 Using SD card storage for media: $MEDIA_DIR"
fi

# Cleanup trap to ensure RAM is freed even on failure
cleanup() {
    if [[ -n "$RAM_DIR" && -d "$RAM_DIR" ]]; then
        echo "🧹 Cleaning up RAM workspace: $RAM_DIR"
        rm -rf -- "$RAM_DIR"
    fi
}
trap cleanup EXIT

# Automated Pre-Flight Sanitization
if [[ -f "$REPO_DIR/sanitize_scene.py" ]]; then
    "$PYTHON_BIN" "$REPO_DIR/sanitize_scene.py" "$SCENE_FILE"
fi

echo "🎬 Rendering $SCENE_CLASS from $(basename "$SCENE_FILE") (Flags: $QUALITY)..."
PYTHONPATH="$REPO_DIR" "$MANIM_BIN" render $QUALITY \
    --media_dir "$MEDIA_DIR" \
    "$SCENE_FILE" "$SCENE_CLASS"

# Find final rendered MP4 (excluding partial movie files)
VIDEO_FILE="$(find "$MEDIA_DIR/videos" -type f -name '*.mp4' ! -path '*/partial_movie_files/*' | head -n 1 || true)"

if [[ -z "$VIDEO_FILE" || ! -f "$VIDEO_FILE" ]]; then
    echo "ERROR: Manim render succeeded but no output video was found."
    exit 1
fi

PERM_DEST="$REPO_DIR/renders/videos/$(basename "$SCENE_FILE" .py)/$(basename "$(dirname "$VIDEO_FILE")")/$(basename "$VIDEO_FILE")"
mkdir -p "$(dirname "$PERM_DEST")"

if [[ "$USE_RAM" -eq 1 ]]; then
    echo "💾 Copying final video from RAM to SD card: $PERM_DEST"
    cp "$VIDEO_FILE" "$PERM_DEST"
else
    PERM_DEST="$VIDEO_FILE"
fi

echo "✅ Video saved: $PERM_DEST"

# Audio Muxing
if [[ -n "$AUDIO_FILE" ]]; then
    if [[ "$AUDIO_FILE" != /* ]]; then
        AUDIO_FILE="$REPO_DIR/$AUDIO_FILE"
    fi

    if [[ -f "$AUDIO_FILE" ]]; then
        SCENE_STEM="$(basename "$SCENE_FILE" .py)"
        RES_TAG="1080p"
        if [[ "$QUALITY" == *"-ql"* ]]; then
            RES_TAG="480p"
        elif [[ "$QUALITY" == *"-qm"* ]]; then
            RES_TAG="720p"
        elif [[ "$QUALITY" == *"-qk"* ]]; then
            RES_TAG="4k"
        fi
        OUT_MUX="$REPO_DIR/renders/${SCENE_STEM}_${RES_TAG}.mp4"
        echo "🎵 Muxing audio ($AUDIO_FILE) with video..."
        ffmpeg -y -i "$PERM_DEST" -i "$AUDIO_FILE" -c:v copy -c:a aac -shortest "$OUT_MUX"
        if [[ "$SCENE_STEM" == *"linux_boot"* && "$RES_TAG" == "1080p" ]]; then
            cp "$OUT_MUX" "$REPO_DIR/renders/Linux_Boot_Scene01_1080p.mp4"
        fi
        echo "🎉 Complete Production Video Ready: $OUT_MUX"
    else
        echo "⚠️ Warning: Audio file not found: $AUDIO_FILE"
    fi
fi
