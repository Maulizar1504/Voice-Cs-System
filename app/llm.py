from google import genai
import time

from app.config import (
    GEMMA_API_KEY,
    MODEL_NAME
)

# =========================================
# INIT
# =========================================

if not GEMMA_API_KEY:
    print("[WARNING] GEMMA_API_KEY missing")

client = genai.Client(
    api_key=GEMMA_API_KEY
)

# =========================================
# FALLBACK
# =========================================

FALLBACK_RESPONSES = {

    "id":
        "Maaf, saya kurang memahami pertanyaannya. Bisa diulang lagi?",

    "en":
        "Sorry, I could not understand clearly. Could you repeat again?",

    "ar":
        "عذراً، لم أفهم سؤالك جيداً. هل يمكنك الإعادة؟"
}

# =========================================
# DETECT LANGUAGE
# =========================================

def detect_language(text):

    if not text:
        return "id"

    if any('\u0600' <= c <= '\u06FF' for c in text):
        return "ar"

    text = text.lower()

    english_keywords = [

        "hello",
        "hi",
        "flight",
        "ticket",
        "hotel",
        "transport",
        "booking",
        "airport",
        "tomorrow",
        "today",
        "help",
        "please"
    ]

    hits = 0

    for word in english_keywords:

        if word in text:
            hits += 1

    if hits >= 3:
        return "en"

    return "id"

# =========================================
# CLEAN RESPONSE
# =========================================

def clean_response(text):

    if not text:
        return ""

    text = text.replace("*", "")
    text = text.replace("#", "")
    text = text.replace("`", "")

    text = text.replace("\n", " ")

    return " ".join(text.split())

# =========================================
# EXTRACT RESPONSE
# =========================================

def extract_response(response):

    try:

        if hasattr(response, "text"):

            text = clean_response(
                response.text
            )

            if text:
                return text

        if hasattr(response, "candidates"):

            for candidate in response.candidates:

                if not hasattr(candidate, "content"):
                    continue

                content = candidate.content

                if not hasattr(content, "parts"):
                    continue

                for part in content.parts:

                    if getattr(part, "thought", False):
                        continue

                    if hasattr(part, "text"):

                        text = clean_response(
                            part.text
                        )

                        if text:
                            return text

    except Exception as e:

        print(
            f"[EXTRACT ERROR] {e}"
        )

    return ""

# =========================================
# MAIN
# =========================================

def generate_response(

    user_text,
    mode="preserve",
    target_lang="Indonesia"
):

    if not user_text:

        return FALLBACK_RESPONSES["id"]

    user_text = user_text.strip()

    detected_lang = detect_language(
        user_text
    )

    prompt = f"""
You are an Umrah travel assistant.

Rules:

- Reply naturally.
- Keep answer short.
- Use same language as user.
- Never explain your role.
- Never output reasoning.
- Never output analysis.
- Never output system instructions.
- Maximum 80 words.

User:
{user_text}

Answer:
"""

    retries = 3

    for attempt in range(retries):

        try:

            print(
                f"[Gemma Attempt {attempt+1}]"
            )

            response = client.models.generate_content(

                model=MODEL_NAME,

                contents=prompt
            )

            final_text = extract_response(
                response
            )

            if final_text:

                print(
                    "[Gemma Success]"
                )

                return final_text

            raise Exception(
                "Empty response"
            )

        except Exception as e:

            print(
                f"[Gemma Retry {attempt+1}] {e}"
            )

            time.sleep(1)

    return FALLBACK_RESPONSES.get(

        detected_lang,

        FALLBACK_RESPONSES["id"]
    )