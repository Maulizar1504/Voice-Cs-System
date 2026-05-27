from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form
)

import shutil
import os

from app.config import (
    TEMP_DIR,
    LOG_DIR
)

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


# =========================================
# FASTAPI
# =========================================

app = FastAPI(
    title="Voice CS System",
    version="2.0"
)


# =========================================
# ROOT
# =========================================

@app.get("/")
def root():

    return {
        "message": "System Running"
    }


# =========================================
# AUDIO CHAT
# =========================================

@app.post("/voice-chat")
async def voice_chat(

    audio: UploadFile = File(...),

    mode: str = Form("preserve"),

    target_lang: str = Form("Indonesia")
):

    temp_name = generate_filename("wav")

    temp_path = os.path.join(
        TEMP_DIR,
        temp_name
    )

    with open(temp_path, "wb") as buffer:

        shutil.copyfileobj(
            audio.file,
            buffer
        )

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
        # AI RESPONSE
        # =====================

        response_text = generate_response(

            processed["normalized_text"],

            mode,

            target_lang
        )

        # =====================
        # CLEAN FOR TTS
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

            "input_type":
                "audio",

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
                mode,

            "target_lang":
                target_lang
        }

        save_log(
            log_data,
            os.path.join(
                LOG_DIR,
                "processing_logs.jsonl"
            )
        )

        # =====================
        # RESPONSE
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


# =========================================
# TEXT CHAT
# =========================================

@app.post("/text-chat")
async def text_chat(

    text: str = Form(None),

    text_file: UploadFile = File(None),

    mode: str = Form("preserve"),

    target_lang: str = Form("Indonesia")
):

    try:

        # =====================
        # GET TEXT
        # =====================

        final_text = ""

        # manual text
        if text and text.strip() != "":

            final_text = text.strip()

        # uploaded file
        elif text_file is not None:

            content = await text_file.read()

            final_text = content.decode(
                "utf-8",
                errors="ignore"
            )

        else:

            return {
                "transcript": "",
                "normalized": "",
                "language": "",
                "tags": [],
                "response":
                    "Masukkan teks atau upload file.",
                "audio_path": None
            }

        # =====================
        # PROCESSING
        # =====================

        processed = process_text(
            final_text
        )

        # =====================
        # AI RESPONSE
        # =====================

        response_text = generate_response(

            processed["normalized_text"],

            mode,

            target_lang
        )

        # =====================
        # CLEAN FOR TTS
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
        # LOG
        # =====================

        log_data = {

            "time":
                timestamp(),

            "input_type":
                "text",

            "transcript":
                final_text,

            "normalized":
                processed["normalized_text"],

            "language":
                processed["language"],

            "tags":
                processed["tags"],

            "response":
                response_text,

            "mode":
                mode,

            "target_lang":
                target_lang
        }

        save_log(
            log_data,
            os.path.join(
                LOG_DIR,
                "processing_logs.jsonl"
            )
        )

        # =====================
        # RESPONSE
        # =====================

        return {

            "transcript":
                final_text,

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

    except Exception as e:

        return {

            "transcript": "",

            "normalized": "",

            "language": "",

            "tags": [],

            "response":
                f"ERROR: {str(e)}",

            "audio_path": None
        }