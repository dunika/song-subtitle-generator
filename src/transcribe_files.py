import os
import subprocess
from pathlib import Path

import captions
import captions_fs

if __name__ == "__main__":
    files_dir = Path(__file__).parent.parent / "bulk_transcription" / "files"
    transcribed_files_dir = (
        Path(__file__).parent.parent / "bulk_transcription" / "transcribed_files"
    )

    file_names = list(files_dir.glob("*."))

    print("Transcribing files...")

    for file_name in file_names:
        print(f"Transcribing {file_name}...")
        file_path = os.path.join(files_dir, file_name)
        captions_config = captions.get(file_path)

        file_stem = file_name.stem

        # final_flame--bridge.wav - songname = final_flame, song_segnemt = bridge
        song_name = file_stem.split("__")[0]

        song_dir = transcribed_files_dir / file_stem

        os.makedirs(song_dir, exist_ok=True)

        captions_fs.write(song_dir, captions_config)

        audio_path = song_dir / "audio.wav"

        # cp file_path audio_path
        subprocess.run(["cp", file_path, audio_path])
