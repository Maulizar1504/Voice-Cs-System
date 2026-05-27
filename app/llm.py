from google import genai
from google.genai import types
import time

from app.config import (
    GEMMA_API_KEY,
    MODEL_NAME
)

from app.prompts import SYSTEM_PROMPT


# =========================================
# INIT CLIENT
# =========================================

client = genai.Client(
    api_key=GEMMA_API_KEY
)


# =========================================
# FALLBACK RESPONSES
# =========================================

FALLBACK_RESPONSES = {

    "Indonesia":
        "Maaf, sistem AI sedang sibuk. Silakan coba lagi sebentar.",

    "English":
        "Sorry, the AI system is busy right now. Please try again shortly.",

    "Arabic":
        "عذرًا، النظام مشغول حاليًا. حاول مرة أخرى لاحقًا."
}


# =========================================
# DETECT LANGUAGE
# =========================================

def detect_language(text):

    # Arabic
    if any('\u0600' <= c <= '\u06FF' for c in text):

        return "Arabic"

    text = text.lower()

    english_words = [

        "hello",
        "flight",
        "ticket",
        "hotel",
        "booking",
        "departure",
        "schedule",
        "airport"
    ]

    if any(word in text for word in english_words):

        return "English"

    return "Indonesia"


# =========================================
# BUILD LANGUAGE PROMPT
# =========================================

def build_language_instruction(
    mode,
    target_lang,
    detected_lang
):

    # =========================
    # PRESERVE
    # =========================
    if mode == "preserve":

        return f"""
Respond using SAME language as the user.
Detected language: {detected_lang}
"""

    # =========================
    # NORMALIZE
    # =========================
    elif mode == "normalize":

        return f"""
Normalize the response into:
{target_lang}

Use only that language consistently.
"""

    # =========================
    # TRANSLATE
    # =========================
    elif mode == "translate":

        return f"""
Translate and respond fully in:
{target_lang}
"""

    # =========================
    # DEFAULT
    # =========================
    return f"""
Respond in:
{target_lang}
"""


# =========================================
# MAIN FUNCTION
# =========================================

def generate_response(

    user_text,

    mode="preserve",

    target_lang="Indonesia"
):

    # =========================
    # DETECT LANGUAGE
    # =========================

    detected_lang = detect_language(
        user_text
    )

    # =========================
    # LANGUAGE RULE
    # =========================

    lang_instruction = build_language_instruction(

        mode,

        target_lang,

        detected_lang
    )

    # =========================
    # FINAL PROMPT
    # =========================

    prompt = f"""

{SYSTEM_PROMPT}

IMPORTANT RULES:

- Sound natural and human
- Keep response concise
- Avoid markdown
- Avoid bullet points
- Make response suitable for voice assistant
- Speak conversationally
- Do not repeat user sentence

LANGUAGE RULE:
{lang_instruction}

USER MESSAGE:
{user_text}

ASSISTANT:
"""

    retries = 5

    for attempt in range(retries):

        try:

            response = client.models.generate_content(

                model=MODEL_NAME,

                contents=prompt,

                config=types.GenerateContentConfig(

                    temperature=0.7,

                    top_p=0.9,

                    top_k=40,

                    max_output_tokens=256
                )
            )

            if response.text:

                clean_text = response.text.strip()

                # remove markdown
                clean_text = clean_text.replace("*", "")
                clean_text = clean_text.replace("#", "")

                if clean_text:

                    return clean_text

            raise Exception(
                "Empty response"
            )

        except Exception as e:

            print(
                f"[Gemma Retry {attempt+1}] {e}"
            )

            wait_time = 2 * (
                attempt + 1
            )

            time.sleep(wait_time)

    # =====================================
    # FINAL FALLBACK
    # =====================================

    return FALLBACK_RESPONSES.get(

        target_lang,

        FALLBACK_RESPONSES[
            "Indonesia"
        ]
    )