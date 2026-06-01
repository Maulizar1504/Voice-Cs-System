from google import genai
import time

from app.config import (
    GEMMA_API_KEY,
    MODEL_NAME
)

# =========================================
# INIT CLIENT
# =========================================

if not GEMMA_API_KEY:
    print("[WARNING] GEMMA_API_KEY missing")

client = genai.Client(
    api_key=GEMMA_API_KEY
)

# =========================================
# FALLBACK RESPONSES
# =========================================

FALLBACK_RESPONSES = {
    "id": "Maaf, saya kurang memahami pertanyaannya. Bisa diulang lagi?",
    "en": "Sorry, I could not understand clearly. Could you repeat again?",
    "ar": "عذراً، لم أفهم سؤالك جيداً. هل يمكنك الإعادة؟"
}

# =========================================
# LANGUAGE DETECTION
# =========================================

def detect_language(text):
    if not text:
        return "id"

    # Arabic detection
    if any('\u0600' <= c <= '\u06FF' for c in text):
        return "ar"

    text = text.lower()

    english_keywords = [
        "hello", "hi", "flight", "ticket", "hotel",
        "transport", "booking", "airport", "tomorrow",
        "today", "help", "please"
    ]

    hits = sum(1 for word in english_keywords if word in text)

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
# EXTRACT RESPONSE (FIXED & ROBUST)
# =========================================

def extract_response(response):
    try:
        # 1. direct text (new SDK)
        text = getattr(response, "text", None)
        if text and text.strip():
            return clean_response(text)

        # 2. candidates fallback
        candidates = getattr(response, "candidates", None)

        if candidates:
            for c in candidates:

                # debug finish reason (IMPORTANT)
                finish_reason = getattr(c, "finish_reason", None)
                if finish_reason is not None:
                    print("[Gemma finish_reason]", finish_reason)

                content = getattr(c, "content", None)
                if not content:
                    continue

                parts = getattr(content, "parts", None)
                if not parts:
                    continue

                for p in parts:
                    text = getattr(p, "text", None)

                    if text and text.strip():
                        return clean_response(text)

    except Exception as e:
        print(f"[EXTRACT ERROR] {e}")

    return ""

# =========================================
# MAIN GENERATION FUNCTION
# =========================================

def generate_response(
    user_text,
    mode="preserve",
    target_lang="Indonesia"
):

    # input validation
    if not user_text or not user_text.strip():
        return FALLBACK_RESPONSES["id"]

    user_text = user_text.strip()

    detected_lang = detect_language(user_text)

    # improved prompt (less restrictive = better output)
    prompt = f"""
You are an Umrah travel assistant.

Instructions:
- Answer naturally and clearly.
- Keep response short (max 80 words).
- Use the same language as the user.
- Do not include system messages or reasoning.
- Be helpful and direct.

User:
{user_text}

Answer:
"""

    retries = 3

    for attempt in range(retries):

        try:
            print(f"[Gemma Attempt {attempt+1}]")

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            print("[RAW RESPONSE]", response)

            final_text = extract_response(response)

            if final_text and final_text.strip():
                print("[Gemma Success]")
                return final_text

            print("[WARNING] Empty response detected")

        except Exception as e:
            print(f"[Gemma Retry {attempt+1}] {e}")
            time.sleep(1)

    # final fallback
    print("[FALLBACK USED]")
    return FALLBACK_RESPONSES.get(
        detected_lang,
        FALLBACK_RESPONSES["id"]
    )