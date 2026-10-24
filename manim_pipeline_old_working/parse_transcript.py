#!/usr/bin/env python3
"""
parse_transcript.py
Audio-Synchronized Transcript Parser & Scene Manifest Generator.
Anchors beats to absolute audio timeline timestamps to eliminate drift.
"""
import re
import json
import argparse
import subprocess
from pathlib import Path


def parse_timestamp(ts: str) -> float:
    """Converts MM:SS or HH:MM:SS to seconds float."""
    parts = list(map(float, ts.split(":")))
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    elif len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    return float(parts[0])


def get_audio_duration(audio_path: Path) -> float:
    """Probes exact duration of an audio file using ffprobe."""
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(audio_path)
        ]
        out = subprocess.check_output(cmd, text=True).strip()
        return round(float(out), 2)
    except Exception:
        return None


def calculate_pacing(total_beat_time: float):
    """
    Allocates snappy visual motion and reserves the remainder for hold.
    """
    if total_beat_time <= 1.5:
        motion_t = round(total_beat_time * 0.6, 2)
    elif total_beat_time < 2.5:
        motion_t = round(total_beat_time * 0.5, 2)
    else:
        motion_t = 1.20  # Standard snappy infographic motion window
    hold_t = round(total_beat_time - motion_t, 2)
    return motion_t, hold_t


def parse_transcript_lines(file_path: Path):
    """
    Extracts explicit scene tags and timestamped lines.
    Preserves exact absolute start times from [MM:SS].
    """
    raw_entries = []
    pattern_dur = re.compile(
        r"^(?:\d+[\.\)])?\s*\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s*\[(\d+(?:\.\d+)?)\]\s*(.*)$"
    )
    pattern_scene_tag = re.compile(r"^\[SCENE(?::\s*(.*?))?\]$", re.IGNORECASE)

    with open(file_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line_str = raw_line.strip()
            if not line_str or line_str.startswith("#"):
                continue

            if line_str == "---" or pattern_scene_tag.match(line_str):
                tag_match = pattern_scene_tag.match(line_str)
                title = tag_match.group(1).strip() if (tag_match and tag_match.group(1)) else None
                raw_entries.append({"type": "SCENE_BREAK", "title": title})
                continue

            match = pattern_dur.match(line_str)
            if match:
                start_sec = parse_timestamp(match.group(1))
                spoken_dur = float(match.group(2))
                text = match.group(3).strip()
                raw_entries.append({
                    "type": "LINE",
                    "start": start_sec,
                    "spoken_duration": spoken_dur,
                    "sentence": text
                })

    return raw_entries


def build_scenes(raw_entries, total_audio_override=None):
    """
    Groups lines into scenes, calculating exact durations from timeline deltas.
    Absorbs inter-line breathing pauses directly into hold_time.
    """
    lines = [e for e in raw_entries if e["type"] == "LINE"]
    if not lines:
        return []

    # Calculate actual beat duration anchored to the start of the next line
    for i in range(len(lines)):
        curr_line = lines[i]
        if i + 1 < len(lines):
            next_start = lines[i + 1]["start"]
            curr_line["beat_duration"] = round(max(curr_line["spoken_duration"], next_start - curr_line["start"]), 2)
        else:
            if total_audio_override and total_audio_override > curr_line["start"]:
                curr_line["beat_duration"] = round(total_audio_override - curr_line["start"], 2)
            else:
                curr_line["beat_duration"] = curr_line["spoken_duration"]

    scenes = []
    current_beats = []
    current_title = "Scene 01"
    scene_counter = 1
    scene_start_sec = lines[0]["start"]

    for entry in raw_entries:
        if entry["type"] == "SCENE_BREAK":
            if current_beats:
                scene_end_sec = current_beats[-1]["start"] + current_beats[-1]["line_duration"]
                scene_dur = round(scene_end_sec - scene_start_sec, 2)
                scenes.append({
                    "scene_id": f"scene_{scene_counter:02d}",
                    "title": current_title,
                    "audio_start_time": scene_start_sec,
                    "audio_end_time": scene_end_sec,
                    "total_duration": scene_dur,
                    "beats": current_beats
                })
                scene_counter += 1
                current_beats = []

            current_title = entry["title"] or f"Scene {scene_counter:02d}"
            continue

        line_data = entry
        motion_t, hold_t = calculate_pacing(line_data["beat_duration"])
        
        if not current_beats:
            scene_start_sec = line_data["start"]

        current_beats.append({
            "beat_id": len(current_beats) + 1,
            "sentence": line_data["sentence"],
            "start": line_data["start"],
            "line_duration": line_data["beat_duration"],
            "motion_time": motion_t,
            "hold_time": hold_t
        })

    if current_beats:
        scene_end_sec = current_beats[-1]["start"] + current_beats[-1]["line_duration"]
        scene_dur = round(scene_end_sec - scene_start_sec, 2)
        scenes.append({
            "scene_id": f"scene_{scene_counter:02d}",
            "title": current_title,
            "audio_start_time": scene_start_sec,
            "audio_end_time": scene_end_sec,
            "total_duration": scene_dur,
            "beats": current_beats
        })

    return scenes


def main():
    parser = argparse.ArgumentParser(description="Audio-Locked Transcript Manifest Generator")
    parser.add_argument("transcript", type=str, help="Path to transcript file")
    parser.add_argument("-a", "--audio", type=str, default=None,
                        help="Optional path to master audio file (.wav/.mp3) to lock end duration")
    parser.add_argument("-o", "--output", type=str, default=None,
                        help="Path for output JSON manifest (default: audio_timings/<name>_manifest.json)")
    parser.add_argument("--project-name", type=str, default=None,
                        help="Project title")

    args = parser.parse_args()
    input_path = Path(args.transcript)
    if not input_path.exists():
        print(f"❌ Error: Transcript file not found: {input_path}")
        return

    total_audio_time = None
    if args.audio:
        audio_file = Path(args.audio)
        if audio_file.exists():
            total_audio_time = get_audio_duration(audio_file)
            print(f"🎧 Master Audio Detected: {audio_file.name} ({total_audio_time:.2f}s)")

    out_path = Path(args.output) if args.output else Path("audio_timings") / f"{input_path.stem}_manifest.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    raw_entries = parse_transcript_lines(input_path)
    scenes = build_scenes(raw_entries, total_audio_override=total_audio_time)

    if not scenes:
        print("❌ Error: No scenes generated. Verify timestamps in transcript.")
        return

    total_video_duration = round(scenes[-1]["audio_end_time"] - scenes[0]["audio_start_time"], 2)

    manifest = {
        "project": args.project_name or input_path.stem,
        "master_audio_total_duration": total_video_duration,
        "total_scenes": len(scenes),
        "scenes": scenes
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"\n✅ Audio-Locked Manifest Generated: {out_path}")
    print(f"   • Total Video Runtime: {total_video_duration:.2f}s (Anchored to Audio)")
    print(f"   • Scene Count:         {len(scenes)}")
    for s in scenes:
        print(f"     - {s['scene_id']} [{s['audio_start_time']}s -> {s['audio_end_time']}s]: "
              f"Duration {s['total_duration']:.2f}s ({len(s['beats'])} beats)")


if __name__ == "__main__":
    main()
