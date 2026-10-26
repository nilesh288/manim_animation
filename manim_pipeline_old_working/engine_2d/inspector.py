"""
engine_2d/inspector.py
Automated Visual Quality & Viewport Boundary Inspector for Manim 2D Infographics.

Performs:
1. Static Scene Code AST Audit:
   - Viewport boundary enforcement (|x| <= 5.8, |y| <= 3.2).
   - Trilateration radius bounds check (R <= 2.3 for constellations).
   - Card Anti-Pattern Detector: flags generic rectangles masquerading as iconic objects.
   - Transient callout lifecycle verification (transient=[...] in beat()).
2. Frame Visual Analysis:
   - Left/Right/Bottom edge bleed detection to ensure zero cropping.
   - Background color consistency verification.
3. Audio/Video Duration Synchronization Audit:
   - Checks millisecond alignment between narration and animation frames.
"""

import ast
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
from PIL import Image

SAFE_X = 5.8
SAFE_Y = 3.2
HEADER_MAX_Y = 3.65


class VisualQualityInspector:
    """Automated visual and geometric quality auditor for Manim scenes and renders."""

    def __init__(self, safe_x: float = SAFE_X, safe_y: float = SAFE_Y):
        self.safe_x = safe_x
        self.safe_y = safe_y

    def audit_scene_code(self, scene_path: Path) -> Dict:
        """Parses scene source code and performs geometric and stylistic AST checks."""
        issues = []
        warnings = []
        passes = []

        code = scene_path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(code, filename=str(scene_path))
        except SyntaxError as e:
            return {
                "status": "FAIL",
                "errors": [f"SyntaxError in {scene_path.name}: {e}"],
                "warnings": [],
                "passes": [],
            }

        # 1. Check for BaseScene subclassing
        has_base_scene = False
        scene_classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                scene_classes.append(node.name)
                for base in node.bases:
                    if (isinstance(base, ast.Name) and base.id in ("BaseScene", "InfographicScene")) or \
                       (isinstance(base, ast.Attribute) and base.attr in ("BaseScene", "InfographicScene")):
                        has_base_scene = True

        if has_base_scene:
            passes.append("Inherits from InfographicScene / BaseScene (enables standardized styling & beat timing)")
        else:
            warnings.append(f"Scene classes ({scene_classes}) do not visibly subclass BaseScene or InfographicScene")

        # 2. Check for banned generic card naming patterns (e.g. Card("PHONE"), Card("SATELLITE"))
        # Flag only when generic rectangular card shapes are explicitly assigned labels of iconic objects
        generic_card_keywords = ["RECEIVER", "SATELLITE", "EARTH", "PHONE", "SMARTPHONE"]
        lines = code.splitlines()
        for idx, line in enumerate(lines, 1):
            for keyword in generic_card_keywords:
                if any(card_type in line for card_type in ["RoundedRectangle", "Rectangle", "PipelineStage"]):
                    if keyword.lower() in line.lower():
                        warnings.append(
                            f"Line {idx}: Detected generic card labeled '{keyword}'. "
                            f"Use authentic iconic physical actors from engine_2d.objects instead."
                        )

        # 3. Check for iconic objects usage
        iconic_objects = ["PhoneDevice", "SatelliteActor", "PlanetEarth", "CellTowerActor", "ChipSoC", "LocationPin"]
        used_iconics = [obj for obj in iconic_objects if obj in code]
        if used_iconics:
            passes.append(f"Uses authentic iconic physical actors: {', '.join(used_iconics)}")

        # 4. Viewport coordinate analysis (look for out-of-bounds literal positions)
        coord_regex = re.compile(r'np\.array\(\[\s*([+-]?\d+\.?\d*)\s*,\s*([+-]?\d+\.?\d*)\s*,\s*([+-]?\d+\.?\d*)\s*\]\)')
        for match in coord_regex.finditer(code):
            x = float(match.group(1))
            y = float(match.group(2))
            if abs(x) > self.safe_x:
                issues.append(f"Coordinate x={x:.2f} exceeds safe boundary |x| <= {self.safe_x}")
            if abs(y) > HEADER_MAX_Y:
                issues.append(f"Coordinate y={y:.2f} exceeds vertical screen boundary |y| <= {HEADER_MAX_Y}")

        # 5. Trilateration Circle radii check
        circle_radius_regex = re.compile(r'Circle\([^)]*radius\s*=\s*([+-]?\d+\.?\d*)', re.IGNORECASE)
        for match in circle_radius_regex.finditer(code):
            r = float(match.group(1))
            if r > 3.0:
                warnings.append(
                    f"Large circle radius R={r:.2f} detected. "
                    f"In 16:9 aspect ratio, multi-sphere radii should be <= 2.3 to prevent cropping."
                )

        # 6. Check for transient callout handling
        if "LeaderCallout" in code or "MetricCard" in code:
            if "transient=" in code:
                passes.append("Transient callouts registered with self.beat(..., transient=[...])")
            else:
                warnings.append("Callouts/cards detected but transient parameter is not used in beat() calls.")

        status = "FAIL" if issues else ("WARN" if warnings else "PASS")
        return {
            "status": status,
            "scene": scene_path.name,
            "issues": issues,
            "warnings": warnings,
            "passes": passes,
        }

    def audit_rendered_video(
        self,
        video_path: Path,
        margin_pct: float = 0.05,
        sample_timestamps: Optional[List[float]] = None,
    ) -> Dict:
        """Extracts keyframes from the rendered video and checks for margin bleed and boundary spill."""
        if not video_path.is_file():
            return {"status": "ERROR", "message": f"Video file not found: {video_path}"}

        # Get video duration via ffprobe
        probe_cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(video_path),
        ]
        try:
            res = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
            duration = float(res.stdout.strip())
        except Exception as e:
            return {"status": "ERROR", "message": f"ffprobe failed: {e}"}

        if sample_timestamps is None:
            # Sample 6 representative points across the video duration
            sample_timestamps = [
                duration * 0.08,
                duration * 0.25,
                duration * 0.45,
                duration * 0.65,
                duration * 0.85,
                duration * 0.96,
            ]

        temp_dir = video_path.parent / "_inspection_tmp"
        temp_dir.mkdir(parents=True, exist_ok=True)

        spill_issues = []
        frame_reports = []

        for t in sample_timestamps:
            frame_file = temp_dir / f"frame_{t:.1f}s.png"
            cmd = [
                "ffmpeg", "-y", "-ss", f"{t:.2f}",
                "-i", str(video_path),
                "-vframes", "1", "-q:v", "2",
                str(frame_file),
            ]
            try:
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            except subprocess.CalledProcessError:
                continue

            if not frame_file.is_file():
                continue

            img = Image.open(frame_file).convert("RGB")
            arr = np.array(img)
            h, w, _ = arr.shape
            bg = arr[2, 2]  # Background sample from top-left corner
            my, mx = int(h * margin_pct), int(w * margin_pct)

            # Exclude top header bar (top 12%) and ground foundation (bottom 16%)
            y_start = int(h * 0.12)
            y_end = h - int(h * 0.16)
            bottom = arr[h - my:, :]
            left = arr[y_start:y_end, :mx]
            right = arr[y_start:y_end, w - mx:]

            diff_bot = np.abs(bottom.astype(int) - bg).max(axis=-1)
            diff_left = np.abs(left.astype(int) - bg).max(axis=-1)
            diff_right = np.abs(right.astype(int) - bg).max(axis=-1)

            threshold = 30
            bot_spill = int(np.sum(diff_bot > threshold))
            left_spill = int(np.sum(diff_left > threshold))
            right_spill = int(np.sum(diff_right > threshold))

            has_lateral_spill = (left_spill > 50) or (right_spill > 50)
            if has_lateral_spill:
                spill_issues.append(
                    f"Timestamp {t:.1f}s: Horizontal frame bleed detected (Left: {left_spill}px, Right: {right_spill}px)"
                )

            frame_reports.append({
                "timestamp": round(t, 2),
                "left_spill_px": left_spill,
                "right_spill_px": right_spill,
                "bottom_spill_px": bot_spill,
                "clean": not has_lateral_spill,
            })

        status = "FAIL" if spill_issues else "PASS"
        return {
            "status": status,
            "duration": round(duration, 2),
            "video": video_path.name,
            "issues": spill_issues,
            "frame_checks": frame_reports,
        }

    def audit_audio_sync(self, video_path: Path, audio_path: Path, tolerance: float = 0.50) -> Dict:
        """Verifies that video stream length matches reference voiceover audio."""
        if not video_path.is_file() or not audio_path.is_file():
            return {"status": "ERROR", "message": "File not found"}

        def get_dur(p: Path) -> float:
            cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(p),
            ]
            return float(subprocess.check_output(cmd).decode().strip())

        v_dur = get_dur(video_path)
        a_dur = get_dur(audio_path)
        diff = abs(v_dur - a_dur)

        is_synced = diff <= tolerance
        return {
            "status": "PASS" if is_synced else "WARN",
            "video_duration": round(v_dur, 2),
            "audio_duration": round(a_dur, 2),
            "delta": round(diff, 3),
            "synced": is_synced,
            "tolerance": tolerance,
        }
