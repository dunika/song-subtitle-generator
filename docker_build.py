#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

# Parse command line arguments
parser = argparse.ArgumentParser(description="Build a Docker image.")

parser.add_argument(
    "--whisper_cache_dir",
    type=str,
    help="Path to the cache directory",
)

parser.add_argument(
    "--t",
    type=str,
    default="whisper",
    help='Tag for the Docker image (default: "whisper")',
)
args = parser.parse_args()

temp_dir = None

# Determine the cache directory
if args.whisper_cache_dir:
    whisper_cache_dir = Path(args.whisper_cache_dir)

    if not whisper_cache_dir.is_dir():
        raise ValueError(f"whisper_cache_dir: {whisper_cache_dir} is not a directory")


else:
    # The COPY command in the Dockerfile requires a directory, so we create a temporary one
    temp_dir = temp_dir = Path.cwd() / "tmp"
    temp_dir.mkdir(exist_ok=True)
    whisper_cache_dir = Path("tmp")


# Build the Docker image
try:
    subprocess.run(
        [
            "docker",
            "build",
            "--build-arg",
            f"WHISPER_CACHE_DIR={str(whisper_cache_dir)}",
            "-t",
            args.t,
            ".",
        ],
        check=True,
    )
except subprocess.CalledProcessError as e:
    print(f"Error building Docker image: {e}", file=sys.stderr)
    exit(1)
except Exception as e:
    print(f"Unexpected error: {e}", file=sys.stderr)
    exit(1)
