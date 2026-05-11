import io
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from .sunbird_client import transcribe_audio, summarise_text, translate_text, synthesise_speech

def run_pipeline(text_input=None, audio_file=None, audio_filename=None, target_language="Luganda"):
    """
    Runs the full summarisation and translation pipeline.
    
    Returns dict with keys: transcript, summary, translated_summary, audio_bytes
    """
    results = {
        "transcript": None,
        "summary": None,
        "translated_summary": None,
        "audio_bytes": None
    }
    
    source_text = ""
    
    # 1. Input Processing & STT
    if audio_file:
        # Check audio duration
        try:
            audio_data = audio_file.read()
            audio_file.seek(0) # Reset for later use if needed
            
            # Simple duration check
            if audio_filename.lower().endswith('.mp3'):
                audio = MP3(io.BytesIO(audio_data))
                duration = audio.info.length
            elif audio_filename.lower().endswith('.wav'):
                audio = WAVE(io.BytesIO(audio_data))
                duration = audio.info.length
            else:
                # For other formats, we might need a more general approach or assume it's okay
                # But the prompt says .mp3, .wav only in Streamlit part
                duration = 0 # Default if unknown
            
            if duration > 300:
                raise ValueError("Audio file exceeds the 5-minute limit.")
                
            results["transcript"] = transcribe_audio(audio_data, audio_filename)
            source_text = results["transcript"]
        except Exception as e:
            if isinstance(e, ValueError):
                raise e
            raise RuntimeError(f"Speech-to-Text failed: {str(e)}")
    elif text_input:
        source_text = text_input
        results["transcript"] = None
    else:
        raise ValueError("No input provided. Please provide text or an audio file.")

    # 2. Summarisation
    try:
        results["summary"] = summarise_text(source_text)
    except Exception as e:
        raise RuntimeError(f"Summarisation failed: {str(e)}")
        
    # 3. Translation
    try:
        results["translated_summary"] = translate_text(results["summary"], target_language)
    except Exception as e:
        raise RuntimeError(f"Translation failed: {str(e)}")
        
    # 4. TTS
    try:
        results["audio_bytes"] = synthesise_speech(results["translated_summary"], target_language)
    except Exception as e:
        raise RuntimeError(f"Speech synthesis failed: {str(e)}")
        
    return results
