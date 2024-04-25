# Song Subitle Generator

This is for personal use. Generates subtitles for a given song.

## Bulk Transcription

Build the app with `docker build --tag whisper`

Add the `.wav` files to `bulk_transcription/files` for the songs you wish to generate subtitles for.

Start the container:
```
docker run -it --rm \
--name whisper \
-v $(pwd)/bulk_transcription/files:/var/app/bulk_transcription/files \
-v $(pwd)/bulk_transcription/transcribed_files:/var/app/bulk_transcription/transcribed_files \
-v $(pwd)/src:/var/app/src \
whisper bash
```

From the container, run `python src/transcribe_files.py`

The files will be generated as follow:
```

bulk_transcription
  transcribed_files
    song_name
      audio.wav
      lyrics.txt
      subtitles.json
```

## Server Upload

From the container, run `python src/server.py` and upload the song you want transcribed.

