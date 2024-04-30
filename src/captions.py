from pathlib import Path
from typing import Dict

from werkzeug.datastructures import FileStorage

import whisper_cache
import whisper_file_utils


def get(
    input_file: str | Path | bytes | FileStorage,
) -> Dict:  # TODO: improve type hinting
    audio_file_path = whisper_file_utils.prepare_file_for_transcription(input_file)

    model = whisper_cache.load_model("large")
    transcription = model.transcribe(
        str(audio_file_path),
        word_timestamps=True,
        language="English",
        verbose=False,
        fp16=False,
    )

    transcript = get_transcript(transcription)

    captions = []
    for segment in transcription["segments"]:
        for word in segment["words"]:
            captions.append(
                {
                    "start": convert_seconds_to_milliseconds(word["start"]),
                    "end": convert_seconds_to_milliseconds(word["end"]),
                    "text": clean_word(word["word"]),
                }
            )

    for i, subtitle in enumerate(captions):
        next_subtitle = captions[i + 1] if i + 1 < len(captions) else None
        if next_subtitle:
            start_time_difference = next_subtitle["start"] - subtitle["start"]
            duration = next_subtitle["end"] - subtitle["start"]

            if start_time_difference < 200 or duration < 200:
                next_subtitle["start"] = subtitle["start"] + 200
                next_subtitle["end"] = next_subtitle["start"] + 200

            else:
                duration = subtitle["end"] - subtitle["start"]
                if duration < 200:
                    subtitle["end"] = subtitle["start"] + 200

    return {
        "captions": captions,
        "transcript": transcript,
    }


def get_transcript(captions):
    lines = []
    for segment in captions["segments"]:
        text = segment["text"].strip()
        if text:
            lines.append(text)
    return lines


def clean_word(word):
    cleaned = word.lower()
    cleaned = "".join(
        [char for char in cleaned if char.isalpha() or char == "'"]
    ).strip()
    return cleaned


def round_to_one_decimal_place(number):
    return round(number, 1)


def convert_seconds_to_milliseconds(seconds):
    return round_to_one_decimal_place(seconds) * 1000
