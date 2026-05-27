from google import genai
from google.genai import types
import time

from app.config import (
    GEMMA_API_KEY,
    MODEL_NAME
)

from app.prompts import SYSTEM_PROMPT


# =========================
# INIT CLIENT
# =========================
client = genai.Client(
    api_key=GEMMA_API_KEY
)


# =========================
# FALLBACK RESPONSES
# =========================
FALLBACK_RESPONSES = {
    "id": "Maaf, sistem AI sedang sibuk. Bisa coba ulang sebentar lagi?",
    "en": "Sorry, the AI system is busy right now. Please try again shortly.",
    "ar": "عذرًا، النظام مشغول حاليًا. حاول مرة أخرى بعد قليل."
}


# =========================
# SIMPLE LANGUAGE DETECTOR
# =========================
def detect_language(text):

    # Arabic unicode
    if any('\u0600' <= c <= '\u06FF' for c in text):
        return "ar"

    text = text.lower()

    english_words = [
        "flight",
        "ticket",
        "hotel",
        "schedule",
        "booking",
        "departure"
    ]

    if any(word in text for word in english_words):
        return "en"

    return "id"


# =========================
# MAIN FUNCTION
# =========================
def generate_response(
    user_text,
    mode="preserve"
):

    prompt = f"""
{SYSTEM_PROMPT}

IMPORTANT RULES:
- ALWAYS respond in SAME LANGUAGE as user
- Keep response SHORT
- Sound NATURAL and HUMAN
- Use conversational style
- Avoid bullet points
- Avoid markdown

MODE:
{mode}

USER:
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

                if clean_text:
                    return clean_text

            raise Exception("Empty response")

        except Exception as e:

            print(f"[Gemma Retry {attempt+1}] {e}")

            # exponential backoff
            wait_time = 2 * (attempt + 1)
            time.sleep(wait_time)

    # =========================
    # FINAL FALLBACK
    # =========================
    lang = detect_language(user_text)

    return FALLBACK_RESPONSES.get(
        lang,
        FALLBACK_RESPONSES["id"]
    )