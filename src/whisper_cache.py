import os
from pathlib import Path

import whisper

default_cache_dir = str(Path(__file__).parent.parent / "cache" / "whisper")

cache_dir = (
    os.environ["WHISPER_CACHE_DIR"]
    if "WHISPER_CACHE_DIR" in os.environ
    else default_cache_dir
)


def load_model(model_name: str):
    return whisper.load_model(model_name, download_root=cache_dir)
