"""
Test script untuk debug backend pipeline
"""

import asyncio
import os
from app.config import TEMP_DIR, OUTPUT_AUDIO_DIR, LOG_DIR
from app.stt import transcribe_audio
from app.processing import process_text, clean_for_tts
from app.llm import generate_response
from app.tts import text_to_speech

# =========================================
# TEST TEXT INPUT
# =========================================
test_text = "Saya ingin tahu tentang penerbangan ke Madinah minggu depan"

print("\n" + "="*60)
print("1. PROCESSING TEXT")
print("="*60)
print(f"Input: {test_text}")

processed = process_text(test_text)
print(f"Normalized: {processed['normalized_text']}")
print(f"Language: {processed['language']}")
print(f"Tags: {processed['tags']}")

print("\n" + "="*60)
print("2. GENERATE RESPONSE")
print("="*60)

response_text = generate_response(
    processed["normalized_text"],
    mode="preserve",
    target_lang="Indonesia"
)
print(f"Response: {response_text}")
print(f"Response Length: {len(response_text)}")
print(f"Is Fallback: {'maaf' in response_text.lower()}")

print("\n" + "="*60)
print("3. CLEAN FOR TTS")
print("="*60)

clean_response = clean_for_tts(response_text)
print(f"Cleaned: {clean_response}")

print("\n" + "="*60)
print("4. TEXT TO SPEECH")
print("="*60)

try:
    output_audio = asyncio.run(text_to_speech(clean_response))
    print(f"Audio Output: {output_audio}")
    print(f"Audio Exists: {os.path.exists(output_audio)}")
    print(f"Audio Size: {os.path.getsize(output_audio) if os.path.exists(output_audio) else 'N/A'} bytes")
except Exception as e:
    print(f"TTS Error: {e}")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
