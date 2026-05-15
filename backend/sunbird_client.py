import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

SUNBIRD_API_TOKEN = os.getenv("SUNBIRD_API_TOKEN")
BASE_URL = "https://api.sunbird.ai"

def _get_headers(content_type="application/json"):
    headers = {
        "Authorization": f"Bearer {SUNBIRD_API_TOKEN}"
    }
    if content_type:
        headers["Content-Type"] = content_type
    return headers

def call_with_retry(fn, retries=3, delay=5):
    for attempt in range(retries):
        try:
            return fn()
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise e

def chunk_text(text, max_chars=500):
    if not text:
        return []
    sentences = text.split('. ')
    chunks, current = [], ""
    for sentence in sentences:
        if len(current) + len(sentence) < max_chars:
            current += sentence + '. '
        else:
            chunks.append(current.strip())
            current = sentence + '. '
    if current:
        chunks.append(current.strip())
    return chunks

def transcribe_audio(file_bytes: bytes, filename: str) -> str:
    url = f"{BASE_URL}/tasks/stt"
    files = {
        'audio': (filename, file_bytes)
    }
    headers = _get_headers(content_type=None)
    
    response = call_with_retry(
        lambda: requests.post(url, files=files, headers=headers, timeout=120)
    )
    
    if response.status_code != 200:
        raise RuntimeError(f"STT failed with status {response.status_code}: {response.text}")
    
    data = response.json()
    return data.get("output", {}).get("text", "")

def call_sunflower(instruction: str) -> str:
    """Generic call to Sunbird Sunflower Simple model."""
    url = f"{BASE_URL}/tasks/sunflower_simple"
    payload = {
        "instruction": instruction
    }
    headers = {
        "Authorization": f"Bearer {SUNBIRD_API_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = call_with_retry(
        lambda: requests.post(url, data=payload, headers=headers, timeout=120)
    )
    
    if response.status_code != 200:
        raise RuntimeError(f"Sunflower call failed with status {response.status_code}: {response.text}")
    
    data = response.json()
    return data.get("response", "")

def summarise_text(text: str, instruction: str = None) -> str:
    # Try custom instruction with Sunflower first
    if instruction:
        try:
            return call_sunflower(f"{instruction}\n\n{text}")
        except Exception:
            pass # Fallback to standard summarizer
            
    url = f"{BASE_URL}/tasks/summarise"
    payload = {"text": text}
    
    response = call_with_retry(
        lambda: requests.post(url, json=payload, headers=_get_headers(), timeout=120)
    )
    
    if response.status_code == 200:
        return response.json().get("response", "")
    return ""

def translate_text(text: str, target_language: str) -> str:
    # Map friendly names to ISO codes
    lang_map = {
        "Acholi": "ach",
        "Ateso": "teo",
        "English": "eng",
        "Luganda": "lug",
        "Lugbara": "lgg",
        "Runyankole": "nyn"
    }
    
    target_code = lang_map.get(target_language, target_language.lower()[:3])
    url = f"{BASE_URL}/tasks/translate"
    headers = _get_headers()
    
    # Chunking for translation stability
    chunks = chunk_text(text)
    translated_parts = []
    
    for chunk in chunks:
        payload = {
            "text": chunk,
            "source_language": "eng",
            "target_language": target_code
        }
        
        result = call_with_retry(
            lambda c=chunk: requests.post(url, json=payload, headers=headers, timeout=120)
        )
        
        if result.status_code == 200:
            translated_parts.append(result.json().get("response", ""))
        else:
            raise RuntimeError(f"Translation API failed ({result.status_code}): {result.text}")
            
    return " ".join(translated_parts)

def synthesise_speech(text: str, language: str) -> bytes:
    url = f"{BASE_URL}/tasks/tts"
    
    speaker_map = {
        "Acholi": 241,
        "Ateso": 242,
        "Runyankole": 243,
        "Lugbara": 245,
        "Luganda": 248
    }
    
    speaker_id = speaker_map.get(language, 248)
    
    payload = {
        "text": text,
        "speaker_id": speaker_id
    }
    
    response = call_with_retry(
        lambda: requests.post(url, json=payload, headers=_get_headers(), timeout=120)
    )
    
    if response.status_code != 200:
        raise RuntimeError(f"TTS failed with status {response.status_code}: {response.text}")
    
    data = response.json()
    audio_url = data.get("output", {}).get("audio_url")
    
    if not audio_url:
        raise RuntimeError("TTS response did not contain an audio_url")
    
    audio_response = call_with_retry(
        lambda: requests.get(audio_url, timeout=120)
    )
    
    if audio_response.status_code != 200:
        raise RuntimeError(f"Failed to download audio from {audio_url}")
    
    return audio_response.content
