from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os

from app.config import TEMP_DIR, LOG_DIR

from app.utils import (
    generate_filename,
    save_log,
    timestamp
)

from app.stt import transcribe_audio

from app.processing import (
    process_text,
    clean_for_tts
)

from app.llm import generate_response
from app.tts import text_to_speech

app = FastAPI(
    title="Voice CS System",
    version="1.0"
)

@app.get("/")
def root():

    return {
        "message": "System Running"
    }


@app.post("/voice-chat")
async def voice_chat(
    audio: UploadFile = File(...),
    mode: str = Form("preserve")
):

    temp_name = generate_filename("wav")

    temp_path = os.path.join(
        TEMP_DIR,
        temp_name
    )

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    try:

        # =====================
        # STT
        # =====================

        stt_result = transcribe_audio(
            temp_path
        )

        # =====================
        # PROCESSING
        # =====================

        processed = process_text(
            stt_result["text"]
        )

        # =====================
        # LLM
        # =====================

        response_text = generate_response(
            processed["normalized_text"],
            mode
        )

        # =====================
        # CLEAN TEXT FOR TTS
        # =====================

        clean_response = clean_for_tts(
            response_text
        )

        # =====================
        # TTS
        # =====================

        output_audio = await text_to_speech(
            clean_response
        )

        # =====================
        # LOGGING
        # =====================

        log_data = {

            "time":
                timestamp(),

            "transcript":
                stt_result["text"],

            "normalized":
                processed["normalized_text"],

            "language":
                processed["language"],

            "tags":
                processed["tags"],

            "response":
                response_text,

            "mode":
                mode
        }

        save_log(
            log_data,
            os.path.join(
                LOG_DIR,
                "processing_logs.jsonl"
            )
        )

        # =====================
        # API RESPONSE
        # =====================

        return {

            "transcript":
                stt_result["text"],

            "normalized":
                processed["normalized_text"],

            "language":
                processed["language"],

            "tags":
                processed["tags"],

            "response":
                response_text,

            "audio_path":
                output_audio
        }

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)