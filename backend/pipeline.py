import io
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from .sunbird_client import transcribe_audio, summarise_text, translate_text, synthesise_speech, call_sunflower

def run_pipeline(text_input=None, audio_file=None, audio_filename=None, target_language="Luganda", source_type="text"):
    """
    Runs the full JUA pipeline.
    
    Returns dict with keys: transcript, summary, action_points, translated_summary, 
    translated_action_points, misinformation_flag, audio_bytes
    """
    results = {
        "transcript": None,
        "summary": None,
        "action_points": None,
        "translated_summary": None,
        "translated_action_points": None,
        "misinformation_flag": False,
        "audio_bytes": None
    }
    
    source_text = ""
    
    # 1. Input Processing & STT
    if audio_file:
        try:
            audio_data = audio_file.read()
            audio_file.seek(0)
            
            if audio_filename.lower().endswith('.mp3'):
                audio = MP3(io.BytesIO(audio_data))
                duration = audio.info.length
            elif audio_filename.lower().endswith('.wav'):
                audio = WAVE(io.BytesIO(audio_data))
                duration = audio.info.length
            else:
                duration = 0
            
            if duration > 300:
                raise ValueError("Audio file exceeds the 5-minute limit.")
                
            results["transcript"] = transcribe_audio(audio_data, audio_filename)
            source_text = results["transcript"]
        except Exception as e:
            if isinstance(e, ValueError): raise e
            raise RuntimeError(f"Speech-to-Text failed: {str(e)}")
    elif text_input:
        source_text = text_input
    else:
        raise ValueError("No input provided.")

    # 2. Advanced Analysis (Always using Sunflower for quality)
    instructions = {
        "whatsapp": "Extract: (1) main claim, (2) target audience, (3) required actions.",
        "radio": "Extract: (1) what was announced, (2) who it affects, (3) dates/actions.",
        "health": "Extract: (1) health issue, (2) risk factors, (3) prevention steps.",
        "government": "Extract: (1) what is announced, (2) who it applies to, (3) deadlines.",
        "community": "Extract: (1) event/update, (2) participants, (3) logistics.",
        "text": "Simplify and explain the following text in plain, clear English for a general audience.",
        "audio": "Summarize the key points of this spoken information clearly."
    }
    
    is_structured = source_type not in ["text", "audio"]
    instr = instructions.get(source_type, "Summarize and analyze the key information.")
    
    try:
        # Generate a structured analysis for ALL types to ensure quality
        analysis_prompt = f"Act as an expert information officer. {instr} Return the analysis in plain English. If appropriate, add 2-3 numbered action points at the end starting with 'ACTION POINTS:'.\n\n{source_text}"
        
        combined_response = call_sunflower(analysis_prompt)
        
        if "ACTION POINTS:" in combined_response:
            parts = combined_response.split("ACTION POINTS:", 1)
            results["summary"] = parts[0].strip()
            results["action_points"] = parts[1].strip()
        else:
            results["summary"] = combined_response.strip()
            
        # Ultimate Fallback if Sunflower is silent
        if not results["summary"] or len(results["summary"]) < 5:
            results["summary"] = source_text[:500]
            
    except Exception as e:
        # Fallback to basic summarisation
        try:
            results["summary"] = summarise_text(source_text)
        except:
            results["summary"] = source_text[:500]

    # 3. Misinformation check
    if source_type in ["whatsapp", "health", "other", "text"]:
        try:
            check_instr = f"Does this message contain potential misinformation, unverified health claims, or miracle promises? Reply only with YES or NO.\n\n{source_text}"
            response = call_sunflower(check_instr)
            results["misinformation_flag"] = "YES" in response.upper()
        except Exception:
            pass

    # 4. Translation
    try:
        if results.get("summary"):
            # Try Sunflower for translation first as it's often more reliable for short summaries
            try:
                trans_prompt = f"Translate the following English text into {target_language}. Provide only the translation, no other text.\n\n{results['summary']}"
                results["translated_summary"] = call_sunflower(trans_prompt)
            except:
                # Fallback to dedicated translation API
                results["translated_summary"] = translate_text(results["summary"], target_language)
        
        if is_structured and results.get("action_points"):
            results["translated_action_points"] = translate_text(results["action_points"], target_language)
    except Exception:
        pass
        
    # 5. TTS
    if results.get("translated_summary"):
        try:
            results["audio_bytes"] = synthesise_speech(results["translated_summary"], target_language)
        except Exception:
            pass
        
    return results
