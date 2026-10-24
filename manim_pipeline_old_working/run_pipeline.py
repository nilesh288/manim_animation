#!/usr/bin/env python3
"""
run_pipeline.py - Master Pipeline CLI for 2D Infographics
Automates directory structure, scene compilation, and rendering.
"""
import sys
import subprocess
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DIRS = {
    "timings": BASE_DIR / "audio_timings",
    "blueprints": BASE_DIR / "blueprints",
    "scenes": BASE_DIR / "scenes",
    "renders": BASE_DIR / "renders",
}

def init_environment():
    """Ensure all working directories exist."""
    for path in DIRS.values():
        path.mkdir(parents=True, exist_ok=True)

def render_scene(scene_file: Path, scene_name: str, quality: str = "l", preview: bool = True):
    """Executes Manim inside the current environment."""
    if not scene_file.exists():
        print(f"❌ Error: Scene file not found: {scene_file}")
        sys.exit(1)

    flag = f"-pq{quality}" if preview else f"-q{quality}"
    cmd = [
        "manim",
        flag,
        str(scene_file),
        scene_name,
        "--media_dir", str(DIRS["renders"])
    ]

    print(f"\n🎬 Rendering {scene_name} from {scene_file.name} (Quality: {quality.upper()})...")
    env = dict(PYTHONPATH=str(BASE_DIR))
    import os
    env.update(os.environ)

    try:
        subprocess.run(cmd, env=env, check=True)
        print(f"\n✅ Render complete. Saved in: {DIRS['renders']}")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Manim render failed with exit code {e.returncode}")
        sys.exit(e.returncode)

def main():
    parser = argparse.ArgumentParser(description="2D Infographic Render Orchestrator")
    parser.add_argument("scene_file", help="Path or filename of the Python scene in scenes/")
    parser.add_argument("scene_class", help="PascalCase Scene Class Name (e.g., CpuCache01)")
    parser.add_argument("-q", "--quality", choices=["l", "m", "h", "k"], default="l",
                        help="Render quality: l (480p), m (720p), h (1080p), k (4K). Default: l")
    parser.add_argument("--no-preview", action="store_true", help="Do not open video preview automatically")

    args = parser.parse_args()
    init_environment()

    target_file = Path(args.scene_file)
    if not target_file.is_file():
        target_file = DIRS["scenes"] / args.scene_file
        if not target_file.suffix:
            target_file = target_file.with_suffix(".py")

    render_scene(target_file, args.scene_class, quality=args.quality, preview=not args.no_preview)

if __name__ == "__main__":
    main()
