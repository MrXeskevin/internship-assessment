import os
import requests
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

def transcribe_audio(file_bytes: bytes, filename: str) -> str:
    url = f"{BASE_URL}/tasks/stt"
    files = {
        'audio': (filename, file_bytes)
    }
    # For multipart/form-data, requests sets the Content-Type automatically with boundary
    headers = _get_headers(content_type=None)
    response = requests.post(url, files=files, headers=headers)
    
    if response.status_code != 200:
        raise RuntimeError(f"STT failed with status {response.status_code}: {response.text}")
    
    data = response.json()
    return data.get("output", {}).get("text", "")

def summarise_text(text: str) -> str:
    url = f"{BASE_URL}/tasks/sunflower_simple"
    payload = {
        "instruction": f"Summarize the following text concisely:\n\n{text}"
    }
    # Sunflower simple requires x-www-form-urlencoded according to past logs
    headers = {
        "Authorization": f"Bearer {SUNBIRD_API_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=payload, headers=headers)
    
    if response.status_code != 200:
        raise RuntimeError(f"Summarisation failed with status {response.status_code}: {response.text}")
    
    data = response.json()
    return data.get("response", "")

def translate_text(text: str, target_language: str) -> str:
    url = f"{BASE_URL}/tasks/sunflower_simple"
    payload = {
        "instruction": f"Translate the following text into {target_language}:\n\n{text}"
    }
    headers = {
        "Authorization": f"Bearer {SUNBIRD_API_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=payload, headers=headers)
    
    if response.status_code != 200:
        raise RuntimeError(f"Translation failed with status {response.status_code}: {response.text}")
    
    data = response.json()
    return data.get("response", "")

def synthesise_speech(text: str, language: str) -> bytes:
    url = f"{BASE_URL}/tasks/tts"
    
    # Mapping languages to speaker IDs based on search results
    speaker_map = {
        "Acholi": 241,
        "Ateso": 242,
        "Runyankole": 243,
        "Lugbara": 245,
        "Luganda": 248
    }
    
    speaker_id = speaker_map.get(language, 248)  # Default to Luganda if not found
    
    payload = {
        "text": text,
        "speaker_id": speaker_id
    }
    response = requests.post(url, json=payload, headers=_get_headers())
    
    if response.status_code != 200:
        raise RuntimeError(f"TTS failed with status {response.status_code}: {response.text}")
    
    data = response.json()
    audio_url = data.get("output", {}).get("audio_url")
    
    if not audio_url:
        raise RuntimeError("TTS response did not contain an audio_url")
    
    # Fetch the audio content
    audio_response = requests.get(audio_url)
    if audio_response.status_code != 200:
        raise RuntimeError(f"Failed to download audio from {audio_url}")
    
    return audio_response.content
