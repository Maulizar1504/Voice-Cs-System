import whisper

# =========================================
# LOAD MODEL
# =========================================

model = whisper.load_model("base")

# =========================================
# TRANSCRIBE AUDIO
# =========================================

def transcribe_audio(audio_path):

    result = model.transcribe(

        audio_path,

        language="id",

        fp16=False
    )

    text = result["text"].strip()

    return {
        "text": text
    }