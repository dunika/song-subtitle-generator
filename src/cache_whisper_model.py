import whisper

if __name__ == "__main__":
    model = whisper.load_model("tiny.en")
    model = whisper.load_model("large")
