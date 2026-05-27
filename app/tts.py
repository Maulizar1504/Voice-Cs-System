import edge_tts
import os
import re
import asyncio

from pydub import AudioSegment

from app.config import OUTPUT_AUDIO_DIR
from app.utils import generate_filename


# =========================================
# FIXED MALE VOICE
# =========================================

GLOBAL_VOICE = "id-ID-ArdiNeural"

# suara cowok Indonesia
# natural dan stabil
# tetap bisa baca EN + AR


# =========================================
# SPLIT SENTENCES
# =========================================

def split_sentences(text):

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    cleaned = []

    for s in sentences:

        s = s.strip()

        if len(s) > 1:
            cleaned.append(s)

    return cleaned


# =========================================
# CLEAN TEXT
# =========================================

def clean_tts_text(text):

    if not text:
        return "Maaf, tidak ada respon."

    text = text.replace("*", "")
    text = text.replace("#", "")
    text = text.replace("_", "")
    text = text.replace("\n", ". ")

    text = re.sub(
        r'\s+',
        ' ',
        text
    )

    return text.strip()


# =========================================
# GENERATE AUDIO CHUNK
# =========================================

async def generate_chunk(
    text,
    output_path
):

    try:

        communicate = edge_tts.Communicate(

            text=text,

            voice=GLOBAL_VOICE,

            rate="-5%",

            pitch="+0Hz"
        )

        await communicate.save(output_path)

        return True

    except Exception as e:

        print(f"TTS chunk error: {e}")

        return False


# =========================================
# MAIN TTS
# =========================================

async def text_to_speech(text):

    text = clean_tts_text(text)

    sentences = split_sentences(text)

    if len(sentences) == 0:

        raise Exception(
            "No valid sentence for TTS."
        )

    base_name = generate_filename("")

    final_output = os.path.join(
        OUTPUT_AUDIO_DIR,
        f"{base_name}.wav"
    )

    combined_audio = AudioSegment.empty()

    success_count = 0

    for idx, sentence in enumerate(sentences):

        temp_file = os.path.join(
            OUTPUT_AUDIO_DIR,
            f"temp_{idx}.mp3"
        )

        success = await generate_chunk(
            sentence,
            temp_file
        )

        if not success:
            continue

        try:

            if os.path.exists(temp_file):

                audio = AudioSegment.from_file(
                    temp_file
                )

                combined_audio += audio

                success_count += 1

                os.remove(temp_file)

        except Exception as e:

            print(f"Audio merge error: {e}")

            continue

    # =====================================
    # FALLBACK
    # =====================================

    if success_count == 0:

        raise Exception(
            "All TTS chunks failed."
        )

    # =====================================
    # EXPORT FINAL AUDIO
    # =====================================

    combined_audio.export(
        final_output,
        format="wav"
    )

    return final_output