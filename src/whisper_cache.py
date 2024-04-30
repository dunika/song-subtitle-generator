import os

import whisper

# os.environ["KMP_DUPLICATE_LIB_OK"] = "True"


def load_model(
    model_name: str,
    cache_dir: str | None = os.environ["WHISPER_CACHE_DIR"],
):
    return whisper.load_model(model_name, download_root=cache_dir)
