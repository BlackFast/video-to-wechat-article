#!/usr/bin/env python3
"""Extract audio from a video file as mono WAV suitable for transcription."""

import argparse
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Extract audio from video for transcription")
    parser.add_argument("input", type=Path, help="Input video file")
    parser.add_argument("--out", type=Path, required=True, help="Output audio file (.wav)")
    parser.add_argument("--sample-rate", type=int, default=16000, help="Sample rate in Hz (default: 16000)")
    parser.add_argument("--force", action="store_true", help="Overwrite output if it exists")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    if args.out.exists() and not args.force:
        print(f"Error: output file exists: {args.out} (use --force to overwrite)", file=sys.stderr)
        sys.exit(1)

    args.out.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-i", str(args.input),
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", str(args.sample_rate),
        "-ac", "1",
        "-y" if args.force else "-n",
        str(args.out),
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Audio extracted: {args.out}")
    except FileNotFoundError:
        print("Error: ffmpeg not found. Install ffmpeg to use this script.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error: ffmpeg failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
