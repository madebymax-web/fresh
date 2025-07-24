import whisper
import config

model = whisper.load_model(config.MODEL_NAME)

def transcribe_file(filepath):
    result = model.transcribe(filepath)
    return result["text"].strip()
