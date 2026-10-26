#!/usr/bin/env python3
"""
run_pipeline.py - Master Pipeline CLI for 2D Infographics
Automates directory structure, pre-flight AST code sanitization, and Manim rendering.
"""
import sys
import shutil
import subprocess
import argparse
import tempfile
import os
from pathlib import Path
from sanitize_scene import sanitize_file

BASE_DIR = Path(__file__).resolve().parent
DIRS = {
    "timings": BASE_DIR / "audio_timings",
    "blueprints": BASE_DIR / "blueprints",
    "scenes": BASE_DIR / "scenes",
    "renders": BASE_DIR / "renders",
}

DEFAULT_MANIM_PATHS = [
    Path("/home/nilesh/manim-env/bin/manim"),
    Path(sys.executable).parent / "manim",
]


def resolve_manim_binary() -> str:
    which_path = shutil.which("manim")
    if which_path:
        return which_path
    for p in DEFAULT_MANIM_PATHS:
        if p.is_file() and os.access(p, os.X_OK):
            return str(p)
    return "manim"


def init_environment():
    """Ensure all working directories exist."""
    for path in DIRS.values():
        path.mkdir(parents=True, exist_ok=True)


def get_ram_media_dir() -> Path | None:
    """Allocates a temporary workspace on RAM filesystem (/dev/shm) to eliminate SD card wear."""
    shm_dir = Path("/dev/shm")
    if shm_dir.exists() and os.access(shm_dir, os.W_OK):
        try:
            stat = os.statvfs(shm_dir)
            free_mb = (stat.f_bavail * stat.f_frsize) / (1024 * 1024)
            if free_mb >= 300:
                ram_dir = Path(tempfile.mkdtemp(prefix="manim_render_", dir=shm_dir))
                return ram_dir
            else:
                print(f"⚠️ /dev/shm has only {free_mb:.1f} MB free; falling back to disk.")
        except Exception as e:
            print(f"⚠️ Unable to query /dev/shm: {e}")
    return None


def render_scene(
    scene_file: Path,
    scene_name: str,
    quality: str = "h",
    preview: bool = False,
    audio_file: str | None = None,
    use_ram: bool = True,
):
    """
    Executes Manim inside the current environment with pre-flight sanitization.
    Renders chunks in RAM filesystem (/dev/shm) and persists final video to SD card storage.
    """
    if not scene_file.exists():
        print(f"❌ Error: Scene file not found: {scene_file}")
        sys.exit(1)

    # 1. Pre-flight Sanitization
    print(f"\n🔍 Pre-flight checking: {scene_file.name}...")
    if not sanitize_file(scene_file):
        print(f"❌ Rendering aborted due to syntax errors in {scene_file.name}.")
        sys.exit(1)

    manim_bin = resolve_manim_binary()
    flag = f"-pq{quality}" if preview else f"-q{quality}"

    ram_media_dir = get_ram_media_dir() if use_ram else None
    if ram_media_dir:
        print(f"⚡ RAM Filesystem Active: Rendering intermediate chunks in {ram_media_dir} (/dev/shm)")
        print("   (Zero SD-card wear & accelerated rendering I/O)")
        active_media_dir = ram_media_dir
    else:
        print(f"💾 Using disk storage: {DIRS['renders']}")
        active_media_dir = DIRS["renders"]

    cmd = [
        manim_bin,
        flag,
        str(scene_file),
        scene_name,
        "--media_dir", str(active_media_dir)
    ]

    print(f"\n🎬 Rendering {scene_name} from {scene_file.name} (Quality: {quality.upper()})...")
    env = dict(PYTHONPATH=str(BASE_DIR))
    env.update(os.environ)

    try:
        subprocess.run(cmd, env=env, check=True)
        print(f"\n✅ Manim render finished successfully.")

        # Locate final generated MP4 files
        video_search_dir = active_media_dir / "videos"
        final_mp4s = []
        if video_search_dir.exists():
            for mp4 in video_search_dir.rglob("*.mp4"):
                if "partial_movie_files" not in mp4.parts:
                    final_mp4s.append(mp4)

        target_video = None
        if ram_media_dir and final_mp4s:
            # Copy final MP4s from RAM to permanent SD card storage
            for mp4 in final_mp4s:
                rel_path = mp4.relative_to(active_media_dir)
                dest = DIRS["renders"] / rel_path
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(mp4, dest)
                target_video = dest
                print(f"💾 Persisted final video to SD card: {dest}")
        elif final_mp4s:
            target_video = final_mp4s[0]

        # Optional Audio Muxing
        if audio_file and target_video and target_video.exists():
            audio_path = Path(audio_file)
            if not audio_path.is_file():
                audio_path = BASE_DIR / audio_file

            if audio_path.is_file():
                output_muxed = DIRS["renders"] / f"{scene_name}_{quality.upper()}D_muxed.mp4"
                print(f"\n🎵 Muxing audio ({audio_path.name}) with video ({target_video.name})...")
                mux_cmd = [
                    "ffmpeg", "-y",
                    "-i", str(target_video),
                    "-i", str(audio_path),
                    "-c:v", "copy",
                    "-c:a", "aac",
                    "-shortest",
                    str(output_muxed)
                ]
                subprocess.run(mux_cmd, check=True)
                print(f"🎉 Complete production video ready: {output_muxed}")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Manim render failed with exit code {e.returncode}")
        sys.exit(e.returncode)
    finally:
        if ram_media_dir and ram_media_dir.exists():
            shutil.rmtree(ram_media_dir, ignore_errors=True)
            print(f"🧹 Cleaned up temporary RAM workspace.")


def main():
    parser = argparse.ArgumentParser(description="2D Infographic Render Orchestrator")
    parser.add_argument("scene_file", help="Path or filename of the Python scene in scenes/")
    parser.add_argument("scene_class", help="PascalCase Scene Class Name (e.g., CpuCache01)")
    parser.add_argument("-q", "--quality", choices=["l", "m", "h", "k"], default="h",
                        help="Render quality: l (480p), m (720p), h (1080p), k (4K). Default: h")
    parser.add_argument("--preview", action="store_true", help="Open video preview after render")
    parser.add_argument("--audio", help="Optional path to audio narration file to automatically mux")
    parser.add_argument("--no-ram", action="store_true", help="Disable RAM filesystem rendering")

    args = parser.parse_args()
    init_environment()

    target_file = Path(args.scene_file)
    if not target_file.is_file():
        target_file = DIRS["scenes"] / args.scene_file
        if not target_file.suffix:
            target_file = target_file.with_suffix(".py")

    render_scene(
        target_file,
        args.scene_class,
        quality=args.quality,
        preview=args.preview,
        audio_file=args.audio,
        use_ram=not args.no_ram,
    )


if __name__ == "__main__":
    import os
    main()
