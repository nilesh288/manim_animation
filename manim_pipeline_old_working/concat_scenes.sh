#!/bin/bash
set -euo pipefail

# ==============================================================================
# concat_scenes.sh - Seamlessly Stitch All Rendered Scenes
# Uses ffmpeg concat demuxer for lossless stitching.
# ==============================================================================

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RENDERS_DIR="$REPO_DIR/renders"
AUDIO_FILE="${1:-linux_boot.mp3}"
OUTPUT_FILE="$RENDERS_DIR/Full_Linux_Boot_Video.mp4"

cd "$REPO_DIR"

LIST_FILE="$(mktemp /tmp/manim_concat_list_XXXXXX.txt)"
trap 'rm -f "$LIST_FILE"' EXIT

echo "🔍 Collecting rendered scene videos..."
find "$RENDERS_DIR/videos" -type f -name 'Scene*.mp4' ! -path '*/partial_movie_files/*' | sort -V | while read -r video; do
    echo "file '$video'" >> "$LIST_FILE"
    echo "  + Added $(basename "$video") ($(basename "$(dirname "$(dirname "$video")")"))"
done

if [[ ! -s "$LIST_FILE" ]]; then
    # Try looking in renders/
    find "$RENDERS_DIR" -maxdepth 1 -type f -name 'scene_*_1080p.mp4' | sort -V | while read -r video; do
        echo "file '$video'" >> "$LIST_FILE"
        echo "  + Added $(basename "$video")"
    done
fi

COUNT=$(wc -l < "$LIST_FILE" || echo 0)
if [[ "$COUNT" -eq 0 ]]; then
    echo "❌ No rendered scene video files found in $RENDERS_DIR."
    echo "   Render your scenes first with ./render_scene.sh scenes/scene_01.py Scene01"
    exit 1
fi

echo "🎬 Stitching $COUNT scene segments into $OUTPUT_FILE..."

if [[ -f "$AUDIO_FILE" ]]; then
    echo "🎵 Merging master soundtrack: $AUDIO_FILE"
    ffmpeg -y -f concat -safe 0 -i "$LIST_FILE" -i "$AUDIO_FILE" -c:v copy -c:a aac -shortest "$OUTPUT_FILE"
else
    echo "ℹ️ Concatenating video streams without separate master soundtrack..."
    ffmpeg -y -f concat -safe 0 -i "$LIST_FILE" -c copy "$OUTPUT_FILE"
fi

echo "🎉 Master Video Ready: $OUTPUT_FILE"
