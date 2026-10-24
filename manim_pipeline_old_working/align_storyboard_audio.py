#!/usr/bin/env python3
"""
align_storyboard_audio.py
Audio-Synchronized Timestamp Injector for Visual Director Storyboards.
Uses Faster-Whisper word-level alignment and SequenceMatcher to inject
exact start_time, end_time, motion_time, and hold_time into the storyboard JSON.
"""

import sys
import re
import json
import difflib
import argparse
from pathlib import Path


def clean_word(w: str) -> str:
    """Normalizes words for robust diff matching."""
    return re.sub(r'[^a-z0-9]', '', w.lower())


def round_boundaries(bounds, min_duration=0.5, ndigits=2):
    """
    Rounds boundaries sequentially once so start + duration == next start
    and total sum equals audio duration.
    """
    out = [0.0]
    for value in bounds[1:]:
        out.append(round(max(out[-1] + min_duration, value), ndigits))
    return out


def calculate_pacing(sub_beat_duration: float):
    """
    Dynamic Infographic Pacing:
    - Active motion carries the duration.
    - Hold/rest time is capped at 1.0s - 1.8s max to eliminate screen freeze.
    """
    if sub_beat_duration <= 1.5:
        hold_t = round(max(0.35, sub_beat_duration * 0.25), 2)
    elif sub_beat_duration <= 3.5:
        hold_t = round(min(1.20, sub_beat_duration * 0.25), 2)
    else:
        hold_t = round(min(1.80, sub_beat_duration * 0.20), 2)

    motion_t = round(sub_beat_duration - hold_t, 2)
    return motion_t, hold_t


def assign_words_to_sub_beats(whisper_words, flattened_sub_beats):
    """
    Maps Whisper words to sub-beat indices using difflib + nearest-neighbor interpolation.
    Adapted from the reference alignment script.
    """
    s_words = []
    s_word_to_target = []

    for target_idx, sb in enumerate(flattened_sub_beats):
        anchor_text = sb.get("narration_anchor", "")
        for w in anchor_text.split():
            cw = clean_word(w)
            if cw:
                s_words.append(cw)
                s_word_to_target.append(target_idx)

    w_words = [w['clean'] for w in whisper_words]
    assign = [-1] * len(w_words)

    sm = difflib.SequenceMatcher(None, w_words, s_words, autojunk=False)
    for block in sm.get_matching_blocks():
        for i in range(block.size):
            assign[block.a + i] = s_word_to_target[block.b + i]

    # Interpolate unmatched words from nearest matched neighbour
    n = len(assign)
    for i in range(n):
        if assign[i] != -1:
            continue
        left_target = right_target = -1
        left_dist = right_dist = 10 ** 9
        for j in range(i - 1, -1, -1):
            if assign[j] != -1:
                left_target, left_dist = assign[j], i - j
                break
        for j in range(i + 1, n):
            if assign[j] != -1:
                right_target, right_dist = assign[j], j - i
                break
        if left_target != -1 and right_target != -1:
            assign[i] = left_target if left_dist <= right_dist else right_target
        elif left_target != -1:
            assign[i] = left_target
        elif right_target != -1:
            assign[i] = right_target
        else:
            assign[i] = 0

    # Outlier filter: if isolated word differs from both identical neighbors
    for i in range(1, n - 1):
        if assign[i - 1] == assign[i + 1] and assign[i] != assign[i - 1]:
            assign[i] = assign[i - 1]

    # Monotonicity check: narration is strictly sequential
    for i in range(1, n):
        if assign[i] < assign[i - 1]:
            assign[i] = assign[i - 1]

    return assign


def align_storyboard_to_audio(audio_path: str, storyboard_json_path: str, output_json_path: str, model_size="base"):
    from faster_whisper import WhisperModel

    audio_file = Path(audio_path)
    storyboard_file = Path(storyboard_json_path)
    out_file = Path(output_json_path)

    if not audio_file.exists():
        print(f"❌ Audio file not found: {audio_file}")
        sys.exit(1)
    if not storyboard_file.exists():
        print(f"❌ Storyboard JSON not found: {storyboard_file}")
        sys.exit(1)

    print(f"Loading Faster-Whisper Model ('{model_size}', device=cpu, int8)...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    print(f"Transcribing audio '{audio_file.name}' for word-level timestamps...")
    segments, info = model.transcribe(str(audio_file), beam_size=5, word_timestamps=True, language="en")

    whisper_words = []
    for segment in segments:
        for word in segment.words:
            cleaned = clean_word(word.word)
            if cleaned:
                whisper_words.append({"clean": cleaned, "start": word.start, "end": word.end})

    if not whisper_words:
        print("❌ No words detected in the audio file.")
        sys.exit(1)

    print(f"Detected {len(whisper_words)} spoken words across {info.duration:.2f}s of audio.")

    # Load Storyboard JSON
    with open(storyboard_file, "r", encoding="utf-8") as f:
        storyboard_data = json.load(f)

    # Flatten all sub-beats into a linear sequence for matching
    flattened_sub_beats = []
    for scene in storyboard_data.get("scenes", []):
        for beat in scene.get("beats", []):
            for sb in beat.get("visual_sub_beats", []):
                flattened_sub_beats.append(sb)

    total_targets = len(flattened_sub_beats)
    print(f"Aligning audio across {total_targets} visual sub-beats...")

    assignments = assign_words_to_sub_beats(whisper_words, flattened_sub_beats)

    # First-word start / last-word end per sub-beat
    sub_beat_times = {}
    for i, w in enumerate(whisper_words):
        target_idx = assignments[i]
        if target_idx not in sub_beat_times:
            sub_beat_times[target_idx] = {'start': w['start'], 'end': w['end']}
        else:
            sub_beat_times[target_idx]['end'] = w['end']

    # Raw start/end calculation with fallback
    raw_start, raw_end = [], []
    for idx in range(total_targets):
        if idx in sub_beat_times:
            s = sub_beat_times[idx]['start']
            e = sub_beat_times[idx]['end']
        else:
            s = raw_end[-1] if raw_end else 0.0
            e = s + 1.2
        raw_start.append(s)
        raw_end.append(e)

    # Midpoint boundary calculation to absorb silence
    total_audio_duration = max(info.duration, raw_end[-1])
    bounds = [0.0]
    for i in range(1, total_targets):
        bounds.append((raw_end[i - 1] + raw_start[i]) / 2.0)
    bounds.append(total_audio_duration)

    # Round boundaries with minimum duration per sub-beat (0.4s)
    calibrated_bounds = round_boundaries(bounds, min_duration=0.40, ndigits=2)

    # Inject calculated timing back into the hierarchical JSON
    global_sb_idx = 0
    for scene in storyboard_data.get("scenes", []):
        for beat in scene.get("beats", []):
            for sb in beat.get("visual_sub_beats", []):
                start = calibrated_bounds[global_sb_idx]
                end = calibrated_bounds[global_sb_idx + 1]
                duration = round(end - start, 2)
                motion_t, hold_t = calculate_pacing(duration)

                sb["start_time"] = start
                sb["end_time"] = end
                sb["duration"] = duration
                sb["motion_time"] = motion_t
                sb["hold_time"] = hold_t

                global_sb_idx += 1

            # Aggregate beat-level metrics
            sub_beats = beat.get("visual_sub_beats", [])
            beat["start_time"] = sub_beats[0]["start_time"]
            beat["end_time"] = sub_beats[-1]["end_time"]
            beat["duration"] = round(beat["end_time"] - beat["start_time"], 2)

        # Aggregate scene-level metrics
        beats = scene.get("beats", [])
        scene["audio_start_time"] = beats[0]["start_time"]
        scene["audio_end_time"] = beats[-1]["end_time"]
        scene["total_duration"] = round(scene["audio_end_time"] - scene["audio_start_time"], 2)

    # Update root metadata
    storyboard_data["master_audio_total_duration"] = round(total_audio_duration, 2)

    # Write formatted output JSON
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as out_f:
        json.dump(storyboard_data, out_f, indent=2)

    print(f"\n✅ Timing Alignment Complete!")
    print(f"   • Output Saved To:     {out_file}")
    print(f"   • Master Audio Length: {total_audio_duration:.2f}s")
    print(f"   • Sub-Beats Timed:     {total_targets}")
    print("\nScene Breakdown:")
    for sc in storyboard_data.get("scenes", []):
        print(f"   - {sc['scene_id']} [{sc['audio_start_time']}s -> {sc['audio_end_time']}s] "
              f"| {sc['total_duration']:.2f}s | {len(sc['beats'])} beats")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize Storyboard JSON with Speech Audio")
    parser.add_argument("audio", type=str, help="Path to voiceover audio file (.mp3 / .wav)")
    parser.add_argument("storyboard", type=str, help="Path to Visual Director output JSON")
    parser.add_argument("-o", "--output", type=str, default="blueprints/timed_storyboard.json",
                        help="Output path for synchronized JSON (default: blueprints/timed_storyboard.json)")
    parser.add_argument("--model", type=str, default="base",
                        help="Whisper model size: tiny, base, small (default: base)")

    args = parser.parse_args()
    align_storyboard_to_audio(args.audio, args.storyboard, args.output, model_size=args.model)
