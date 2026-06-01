import re

from app.llm import detect_language

# =========================================
# COMMON STT FIXES
# =========================================

COMMON_FIXES = {

    # flight
    "uflat": "flight",
    "flag": "flight",
    "fly": "flight",

    # booking
    "buk": "booking",
    "book": "booking",

    # jeddah
    "kejidah": "jeddah",
    "jidah": "jeddah",
    "jedah": "jeddah",
    "jepdah": "jeddah",

    # madinah
    "madina": "madinah",

    # visa
    "fisah": "visa",

    # umrah
    "umga": "umrah",
    "umurah": "umrah",
    "omra": "umrah"
}

# =========================================
# NORMALIZE TEXT
# =========================================

def normalize_text(text):

    if not text:
        return ""

    text = text.lower()

    for wrong, correct in COMMON_FIXES.items():

        text = text.replace(
            wrong,
            correct
        )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()

# =========================================
# TAG EXTRACTION
# =========================================

def extract_tags(text):

    if not text:
        return []

    tagmap = {

        "flight": [
            "flight",
            "ticket",
            "pesawat",
            "maskapai"
        ],

        "hotel": [
            "hotel",
            "penginapan",
            "akomodasi"
        ],

        "visa": [
            "visa",
            "dokumen",
            "vaksin"
        ],

        "transport": [
            "transport",
            "bus",
            "kereta",
            "mobil",
            "travel",
            "shuttle"
        ],

        "religious_information": [
            "umrah",
            "haji",
            "madinah",
            "makkah",
            "mekkah",
            "jeddah",
            "ziarah"
        ],

        "travel_booking": [
            "booking",
            "schedule",
            "jadwal",
            "pesan",
            "tiket"
        ]
    }

    tags = []

    for tag, keywords in tagmap.items():

        if any(

            keyword in text

            for keyword in keywords
        ):
            tags.append(tag)

    return tags

# =========================================
# PROCESS TEXT
# =========================================

def process_text(text):

    normalized = normalize_text(
        text
    )

    language = detect_language(
        normalized
    )

    tags = extract_tags(
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

# =========================================
# GIBBERISH DETECTION
# =========================================

def is_gibberish(text):

    if not text:
        return True

    words = text.split()

    if len(words) < 2:
        return True

    weird_count = 0

    for word in words:

        if len(word) > 18:
            weird_count += 1

        if re.search(
            r"[^a-zA-Z0-9\s]",
            word
        ):
            weird_count += 1

    return weird_count >= 3

# =========================================
# CLEAN FOR TTS
# =========================================

def clean_for_tts(text):

    if not text:
        return ""

    text = text.replace("*", "")
    text = text.replace("#", "")
    text = text.replace("`", "")
    text = text.replace("_", "")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()