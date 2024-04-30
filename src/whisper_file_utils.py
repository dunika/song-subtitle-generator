import mimetypes
import os
import subprocess
import tempfile
from pathlib import Path

import magic
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

supported_file_types = ["m4a", "mp3", "webm", "mp4", "mpga", "wav", "mpeg"]


def extract_audio_from_media(input_file, output_file):
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


def prepare_file_for_transcription(
    input_file: str | Path | bytes | FileStorage,
) -> Path:
    # Create a temporary directory to store files
    tmp_dir = tempfile.mkdtemp()
    audio_file_path = None

    # Check if input_file is a FileStorage instance (commonly used with Flask file uploads)
    if isinstance(input_file, FileStorage):
        safe_filename = secure_filename(input_file.filename)
        tmp_path = Path(os.path.join(tmp_dir, safe_filename))
        input_file.save(tmp_path)
        audio_file_path = tmp_path

    # Check if input_file is a bytes object (in-memory data)
    elif isinstance(input_file, bytes):
        magic_obj = magic.Magic(mime=True)
        mime_type = magic_obj.from_buffer(input_file)
        file_extension = mimetypes.guess_extension(mime_type)

        # Handle the bytes data
        tmp_path = Path(os.path.join(tmp_dir, f"tmp_file.{file_extension}"))
        with open(tmp_path, "wb") as f:
            f.write(input_file)

        audio_file_path = tmp_path

    # Check if input_file is a string path
    elif isinstance(input_file, str) or isinstance(input_file, Path):
        # Check if the file path actually exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"The file {input_file} does not exist")
        # Use the string path as is
        audio_file_path = (
            input_file if isinstance(input_file, Path) else Path(input_file)
        )

    else:
        # Raise an error or handle other types as needed
        raise ValueError("Unsupported file type provided")

    # Get the file extension
    file_extension = audio_file_path.suffix[1:]

    # Check if the file type is supported
    if file_extension not in supported_file_types:
        try:
            output_file_path = str(audio_file_path).replace(file_extension, "wav")
            extract_audio_from_media(
                input_file,
                output_file_path,
            )
            audio_file_path = Path(output_file_path)
        except:
            raise ValueError("Unsupported file type: " + input_file)

    return audio_file_path
