import streamlit as st
from backend.pipeline import run_pipeline

# Page configuration
st.set_page_config(
    page_title="Sunbird Translator and Summarizer",
    page_icon="🌻",
    layout="centered"
)

# Custom CSS for Premium Minimalist Aesthetic
st.markdown("""
    <style>
    /* Import Inter from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global Typography */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Constrain main container width */
    .block-container {
        max-width: 720px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    /* Section Labels */
    .section-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #888888;
        margin-bottom: 8px;
        display: block;
    }

    /* Result Card Styling - Forced visibility in both themes */
    .result-card {
        background: #ffffff !important;
        border-radius: 16px;
        padding: 24px 28px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border: 1px solid #eeeeee;
        margin-bottom: 20px;
    }

    .result-card p, .result-card span, .result-card div {
        color: #111111 !important;
        font-size: 15px;
        line-height: 1.7;
        margin: 0;
    }

    /* Character Counter */
    .char-counter {
        text-align: right;
        color: #888888;
        font-size: 12px;
        margin-top: 4px;
    }

    /* Muted small text */
    .muted-note {
        color: #888888;
        font-size: 13px;
        margin-top: 8px;
    }

    /* Center Header */
    .header-container {
        text-align: center;
        margin-bottom: 2.5rem;
    }

    /* Hide Streamlit components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Helper function to render section labels with SVG icons
def render_label(text, icon_paths):
    svg_html = f"""
    <span class="section-label">
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" 
           viewBox="0 0 24 24" fill="none" stroke="#888888" 
           stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
           style="vertical-align: middle; margin-right: 6px;">
        {icon_paths}
      </svg>
      {text}
    </span>
    """
    st.markdown(svg_html, unsafe_allow_html=True)

# Icon Paths
ICON_TRANSCRIPT = '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>'
ICON_SUMMARY = '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>'
ICON_TRANSLATION = '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>'
ICON_LISTEN = '<path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 1 2 2h1a2 2 0 0 1 2-2v-3a2 2 0 0 1-2-2H3z"/>'

# 1. HEADER
st.markdown("""
    <div class="header-container">
        <h1 style="font-weight: 700; margin-bottom: 0.5rem;">
            <span style="color: #F5A623;">🌻</span> Sunbird Translator and Summarizer
        </h1>
        <p style="color: #666666; font-size: 1.1rem;">
            Summarise and translate into Ugandan languages — powered by Sunbird AI
        </p>
    </div>
""", unsafe_allow_html=True)

# 2. SETTINGS ROW
st.markdown('<span class="section-label">Target Language</span>', unsafe_allow_html=True)
target_language = st.selectbox(
    "Target Language Select",
    ["Luganda", "Runyankole", "Ateso", "Lugbara", "Acholi"],
    label_visibility="collapsed"
)

st.markdown('<span class="section-label" style="margin-top: 1.5rem;">Input Mode</span>', unsafe_allow_html=True)
input_mode = st.radio(
    "Input Mode Select",
    ["Text", "Audio", "Record"],
    horizontal=True,
    label_visibility="collapsed"
)

# 3. INPUT AREA
source_text = None
audio_file = None
recorded_audio = None
audio_filename = None

if input_mode == "Text":
    source_text = st.text_area(
        "Input Text",
        height=200,
        placeholder="Paste or type text to summarise...",
        label_visibility="collapsed"
    )
    char_count = len(source_text) if source_text else 0
    st.markdown(f'<div class="char-counter">{char_count} characters</div>', unsafe_allow_html=True)
elif input_mode == "Audio":
    audio_file = st.file_uploader(
        "Upload Audio",
        type=["mp3", "wav"],
        label_visibility="collapsed"
    )
    if audio_file:
        audio_filename = audio_file.name
        st.audio(audio_file)
    st.markdown('<div class="muted-note">Maximum 5 minutes. Supported formats: MP3, WAV</div>', unsafe_allow_html=True)
else: # Record Mode
    recorded_audio = st.audio_input("Click to record", label_visibility="collapsed")
    if recorded_audio:
        audio_filename = "recording.wav"
    st.markdown('<div class="muted-note">Recording will be transcribed using Sunbird STT</div>', unsafe_allow_html=True)

# 4. ACTION BUTTON
st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
# Enable button if any of the modes have input
can_process = (input_mode == "Text" and source_text) or \
              (input_mode == "Audio" and audio_file) or \
              (input_mode == "Record" and recorded_audio)

process_btn = st.button(
    "Summarise & Translate",
    use_container_width=True,
    disabled=not can_process
)
st.divider()

# 5. RESULTS
if process_btn:
    try:
        with st.spinner("Processing... this may take a few seconds"):
            # Determine active audio input
            active_audio = recorded_audio if input_mode == "Record" else (audio_file if input_mode == "Audio" else None)
            
            # Execute pipeline
            results = run_pipeline(
                text_input=source_text if input_mode == "Text" else None,
                audio_file=active_audio,
                audio_filename=audio_filename,
                target_language=target_language
            )
            
            # Display results
            
            # a) TRANSCRIPT
            if results.get("transcript"):
                render_label("TRANSCRIPT", ICON_TRANSCRIPT)
                st.markdown(f"""
                    <div class="result-card">
                        <p>{results['transcript']}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # b) SUMMARY
            if results.get("summary"):
                summary_text = results['summary']
                word_count = len(summary_text.split())
                render_label(f"SUMMARY &middot; {word_count} words", ICON_SUMMARY)
                st.markdown(f"""
                    <div class="result-card">
                        <p>{summary_text}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # c) TRANSLATION
            if results.get("translated_summary"):
                translated_text = results['translated_summary']
                word_count = len(translated_text.split())
                render_label(f"TRANSLATION INTO {target_language.upper()} &middot; {word_count} words", ICON_TRANSLATION)
                st.markdown(f"""
                    <div class="result-card">
                        <p>{translated_text}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # d) LISTEN
            if results.get("audio_bytes"):
                render_label("LISTEN", ICON_LISTEN)
                st.audio(results["audio_bytes"], format="audio/mp3")
                
    except Exception as e:
        st.error(f"System Error: {str(e)}")
