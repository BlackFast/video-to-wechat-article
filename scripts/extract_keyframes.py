#!/usr/bin/env python3
"""Extract keyframes from a video at a regular interval."""

import argparse
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Extract keyframes from video at regular intervals")
    parser.add_argument("input", type=Path, help="Input video file")
    parser.add_argument("--out", type=Path, required=True, help="Output directory for keyframe images")
    parser.add_argument("--interval", type=int, default=30, help="Seconds between keyframes (default: 30)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing output directory")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    if args.out.exists():
        if not args.force:
            print(f"Error: output directory exists: {args.out} (use --force to overwrite)", file=sys.stderr)
            sys.exit(1)
        # Clean old keyframes so counts don't include stale frames
        for old in args.out.glob("frame_*.jpg"):
            old.unlink()
    else:
        args.out.mkdir(parents=True, exist_ok=True)

    output_pattern = str(args.out / "frame_%03d.jpg")

    cmd = [
        "ffmpeg",
        "-i", str(args.input),
        "-vf", f"fps=1/{args.interval}",
        "-q:v", "2",
        "-y" if args.force else "-n",
        output_pattern,
    ]

    try:
        subprocess.run(cmd, check=True)
        frames = sorted(args.out.glob("frame_*.jpg"))
        print(f"Extracted {len(frames)} keyframes to {args.out}")
        for f in frames:
            print(f"  {f.name}")
    except FileNotFoundError:
        print("Error: ffmpeg not found. Install ffmpeg to use this script.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error: ffmpeg failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
