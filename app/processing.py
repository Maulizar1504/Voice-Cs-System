import re
from langdetect import detect


# =========================
# NORMALIZATION
# =========================
def normalize_text(text):

    text = text.strip()

    text = re.sub(r'\s+', ' ', text)

    return text


# =========================
# CLEAN FOR TTS
# =========================
def clean_for_tts(text):

    text = re.sub(r'\*+', '', text)
    text = re.sub(r'#+', '', text)

    text = re.sub(r'\n+', '. ', text)

    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# =========================
# LANGUAGE DETECTION
# =========================
def detect_language(text):

    try:
        return detect(text)

    except:
        return "unknown"


# =========================
# SIMPLE NLP TAGGING
# =========================
def tag_text(text):

    tags = []

    text_lower = text.lower()

    # booking intent
    booking_keywords = [
        "book",
        "flight",
        "ticket",
        "hotel",
        "transport"
    ]

    # religious intent
    religion_keywords = [
        "umrah",
        "hajj",
        "ramadan",
        "fasting",
        "makkah",
        "madinah"
    ]

    # visa intent
    visa_keywords = [
        "visa",
        "passport",
        "document"
    ]

    if any(word in text_lower for word in booking_keywords):
        tags.append("travel_booking")

    if any(word in text_lower for word in religion_keywords):
        tags.append("religious_information")

    if any(word in text_lower for word in visa_keywords):
        tags.append("visa_process")

    if len(tags) == 0:
        tags.append("general_conversation")

    return tags


# =========================
# MAIN PROCESSING
# =========================
def process_text(text):

    normalized = normalize_text(text)

    language = detect_language(
        normalized
    )

    tags = tag_text(
        normalized
    )

    return {

        "normalized_text":
            normalized,

        "language":
            language,

        "tags":
            tags
    }