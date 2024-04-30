import json
import os

import whisper_cache


def round_to_one_decimal_place(number):
    return round(number, 1)


def convert_seconds_to_milliseconds(seconds):
    return round_to_one_decimal_place(seconds) * 1000


def get_subtitles_and_lyrics(path):
    model = whisper_cache.load_model("large")
    transcription = model.transcribe(
        path,
        word_timestamps=True,
        language="English",
        verbose=True,
        fp16=False,
    )

    lyrics = get_lyrics(transcription)

    subtitles = []
    for segment in transcription["segments"]:
        for word in segment["words"]:
            subtitles.append(
                {
                    "start": convert_seconds_to_milliseconds(word["start"]),
                    "end": convert_seconds_to_milliseconds(word["end"]),
                    "text": clean_word(word["word"]),
                }
            )

    for i, subtitle in enumerate(subtitles):
        next_subtitle = subtitles[i + 1] if i + 1 < len(subtitles) else None
        if next_subtitle:
            subtitles[i] = {
                "start": subtitle["start"],
                "text": subtitle["text"],
            }

    for i, subtitle in enumerate(subtitles):
        next_subtitle = subtitles[i + 1] if i + 1 < len(subtitles) else None

        if next_subtitle:
            duration = next_subtitle["start"] - subtitle["start"]
            if duration < 200:
                next_subtitle["start"] = subtitle["start"] + 200

        else:
            duration = subtitle["end"] - subtitle["start"]
            if duration < 200:
                subtitle["end"] = subtitle["start"] + 200

    return subtitles, lyrics


def write_subtitles_and_lyrics(dir, subtitles, lyrics):
    os.makedirs(dir, exist_ok=True)

    subtitles_path = os.path.join(dir, "subtitles.json")
    with open(subtitles_path, "w") as f:
        f.write(json.dumps(subtitles, indent=2))

    lyrics_path = os.path.join(dir, "lyrics.txt")
    with open(lyrics_path, "w") as f:
        f.write("\n".join(lyrics))


def get_lyrics(subtitles):
    lines = []
    for segment in subtitles["segments"]:
        lines.append(
            segment["text"].strip(),
        )
    return lines


def clean_word(word):
    cleaned = word.lower()
    cleaned = "".join(
        [char for char in cleaned if char.isalpha() or char == "'"]
    ).strip()
    return cleaned
