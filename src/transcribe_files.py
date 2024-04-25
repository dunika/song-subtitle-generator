import os
import subprocess
from pathlib import Path

from subtitles import get_subtitles_and_lyrics, write_subtitles_and_lyrics

# os.environ["KMP_DUPLICATE_LIB_OK"] = "True"


def extract_audio(input_file, output_file):
    # Command to extract audio using FFmpeg and save it as a WAV file
    command = [
        "ffmpeg",
        "-i",
        input_file,
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "44100",
        "-ac",
        "2",
        output_file,
    ]

    # Execute the command
    subprocess.run(command, check=True)


# Extract audio from the .mov file

if __name__ == "__main__":
    files_dir = Path(__file__).parent.parent / "bulk_transcription" / "files"
    transcribed_files_dir = (
        Path(__file__).parent.parent / "bulk_transcription" / "transcribed_files"
    )

    video_files = list(files_dir.glob("*.mov"))
    for video_file in video_files:
        print("Converting video to audio...")

        audio_file = files_dir / (video_file.stem + ".wav")
        extract_audio(video_file, audio_file)

    audio_files = list(files_dir.glob("*.wav"))

    print("Transcribing files...")

    for file in audio_files:
        file_path = os.path.join(files_dir, file)
        subtitles, lyrics = get_subtitles_and_lyrics(file_path)

        file_stem = file.stem

        # final_flame--bridge.wav - songname = final_flame, song_segnemt = bridge
        song_name = file_stem.split("__")[0]

        song_dir = transcribed_files_dir / file_stem

        os.makedirs(song_dir, exist_ok=True)

        write_subtitles_and_lyrics(
            song_dir,
            subtitles,
            lyrics,
        )

        audio_path = song_dir / "audio.wav"

        # cp file_path audio_path
        subprocess.run(["cp", file_path, audio_path])
