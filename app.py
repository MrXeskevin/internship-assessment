import streamlit as st
from backend.pipeline import run_pipeline
import traceback
import textwrap

# Page configuration
st.set_page_config(
    page_title="JUA — Translate & Summarize",
    page_icon="☀️",
    layout="centered"
)

# 1. ICONS & CONSTANTS
SVG_SUN = '<circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>'
SVG_PIN = '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>'
SVG_MSG = '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'
SVG_RADIO = '<circle cx="12" cy="12" r="2"/><path d="M16.24 7.76a6 6 0 0 1 0 8.49m-8.48-.01a6 6 0 0 1 0-8.49m11.31-2.82a10 10 0 0 1 0 14.14m-14.14 0a10 10 0 0 1 0-14.14"/>'
SVG_HEALTH = '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>'
SVG_LANDMARK = '<line x1="3" y1="22" x2="21" y2="22"/><line x1="6" y1="18" x2="6" y2="11"/><line x1="10" y1="18" x2="10" y2="11"/><line x1="14" y1="18" x2="14" y2="11"/><line x1="18" y1="18" x2="18" y2="11"/><polygon points="12 2 20 7 4 7"/>'
SVG_MEGAPHONE = '<path d="M3 11l19-9-9 19-2-8-8-2z"/>'
SVG_FILE = '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>'
SVG_EDIT = '<path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>'
SVG_MIC = '<path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/>'
SVG_GLOBE = '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>'
SVG_CHECK = '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>'
SVG_ALERT = '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>'
SVG_INFO = '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>'
SVG_SEND = '<line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>'
SVG_VOLUME = '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/>'

# 2. CUSTOM CSS
st.markdown(textwrap.dedent("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
    }

    .block-container {
        max-width: 720px !important;
        padding-top: 2rem !important;
    }

    /* Landing Page Styles */
    .landing-container {
        text-align: center;
        padding: 4rem 1rem;
    }
    .landing-hero {
        font-size: clamp(2.5rem, 6vw, 4.5rem);
        font-weight: 900;
        color: #111827;
        line-height: 1.1;
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: -0.02em;
    }
    .landing-hero span {
        color: #1488fc;
    }
    .pill-container {
        display: flex;
        justify-content: center;
        gap: 12px;
        flex-wrap: wrap;
        margin: 2.5rem 0;
    }
    .pill {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 9999px;
        padding: 10px 20px;
        font-size: 14px;
        color: #374151;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }

    /* Header */
    .header-container {
        text-align: center;
        margin-bottom: 3.5rem;
    }

    .jua-title {
        font-size: 3.5rem;
        font-weight: 900;
        color: #111827;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 16px;
        margin-bottom: 0.2rem;
        letter-spacing: -0.03em;
    }

    .jua-subtitle {
        color: #6b7280;
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }

    /* Source Type Cards */
    .source-card-unit {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 16px;
        min-height: 110px;
        border-radius: 12px;
        border: 1px solid #ddd;
        background: white;
        transition: all 0.2s ease;
        position: relative;
    }
    .source-card-unit.selected {
        background: #1488fc !important;
        border-color: #1488fc !important;
        box-shadow: 0 4px 15px rgba(20, 136, 252, 0.4) !important;
    }
    .source-card-unit svg {
        stroke-width: 1.5;
    }
    .source-card-label {
        font-size: 14px;
        font-weight: 500;
    }

    /* Button Hacks - REMOVING BLACK BOXES COMPLETELY */
    .source-grid-container div[data-testid="stButton"] {
        background: transparent !important;
        border: none !important;
        margin: 0 !important;
        padding: 0 !important;
        height: 0 !important; /* Move it up */
    }
    .source-grid-container div[data-testid="stButton"] button {
        position: relative !important;
        top: -122px !important; /* Hover exactly over the card */
        width: 100% !important;
        height: 110px !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: transparent !important;
        z-index: 10 !important;
    }
    .source-grid-container div[data-testid="stButton"] button:hover,
    .source-grid-container div[data-testid="stButton"] button:active,
    .source-grid-container div[data-testid="stButton"] button:focus {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: transparent !important;
    }

    /* Main CTA Buttons - FORCE BLUE NOT RED */
    .stButton > button[kind="primary"], 
    div[data-testid="stButton"] button[kind="primary"],
    .main-cta-btn div[data-testid="stButton"] button {
        background-color: #1488fc !important;
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        padding: 16px 48px !important;
        border-radius: 9999px !important;
        box-shadow: 0 8px 24px rgba(20,136,252,0.3) !important;
        border: none !important;
        transition: all 0.3s ease !important;
        width: auto !important;
        min-width: 240px;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(20,136,252,0.4) !important;
        background-color: #0076e4 !important;
    }

    /* Output Cards */
    .output-card {
        background: white !important;
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 20px;
        border: 1px solid #eeeeee;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04);
        color: #111827 !important; /* Force dark text color */
    }
    .output-card p, .output-card div {
        color: #111827 !important;
        line-height: 1.6;
        font-size: 1.05rem;
    }
    .alert-card {
        background: #fffbeb !important;
        border: 1px solid #f59e0b !important;
    }
    
    /* Steps */
    .step-label {
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #666;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* UI Fixes */
    div[data-testid="stMarkdownContainer"] p { margin-bottom: 0; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Status visibility */
    div[data-testid="stStatusWidget"] {
        background-color: #f0f7ff !important;
        border: 1px solid #1488fc !important;
        border-radius: 12px !important;
    }
    div[data-testid="stStatusWidget"] label {
        color: #1488fc !important;
        font-weight: 700 !important;
    }
    </style>
"""), unsafe_allow_html=True)

# 3. HELPER FUNCTIONS
def render_svg(path, size=20, color="currentColor", stroke_width=1.5):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle;">{path}</svg>"""

def render_step_label(text, icon_path):
    st.markdown(f'<div class="step-label">{render_svg(icon_path, 16, "#1488fc")} {text}</div>', unsafe_allow_html=True)

# 4. INITIALIZE STATE
if "show_landing" not in st.session_state:
    st.session_state.show_landing = True
if "source_type" not in st.session_state:
    st.session_state.source_type = "text"
if "results" not in st.session_state:
    st.session_state.results = None

# 5. LANDING PAGE
if st.session_state.show_landing:
    st.markdown(textwrap.dedent(f"""
        <div class="landing-container">
            <div style="margin-bottom: 3rem;">
                {render_svg(SVG_SUN, 48, "#F5A623", 2)}
                <div style="font-size: 3rem; font-weight: 900; color: #111827; letter-spacing: -0.03em;">JUA</div>
                <div style="font-size: 1rem; color: #6b7280; font-weight: 500;">Translate & Summarize to Ugandan Local Languages</div>
            </div>
            <div class="landing-hero">
                Understand what<br>you <span>receive.</span>
            </div>
            <div style="font-size: 1rem; color: #6b7280; max-width: 480px; margin: 0 auto; line-height: 1.6;">
                WhatsApp forwards. Radio announcements. Health bulletins. Government notices.
            </div>
            <div class="pill-container">
                <div class="pill">{render_svg(SVG_SUN, 14, "#F5A623")} Simplified for everyone</div>
                <div class="pill">{render_svg(SVG_GLOBE, 14, "#1488fc")} 5 Ugandan languages</div>
                <div class="pill">{render_svg(SVG_CHECK, 14, "#10b981")} Misinformation flagging</div>
            </div>
        </div>
    """), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="main-cta-btn" style="text-align: center;">', unsafe_allow_html=True)
        if st.button("Get Started →", use_container_width=True, key="get_started"):
            st.session_state.show_landing = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(textwrap.dedent("""
        <div style="margin-top: 4rem; text-align: center;">
            <div style="font-size: 11px; color: #9ca3af; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 40px;">
                Powered by Sunbird AI
            </div>
            <div style="width:100%; background:#0f0f0f; padding: 48px 24px; text-align:center; border-radius: 16px 16px 0 0;">
                <p style="font-size: clamp(2rem, 5vw, 3.5rem); font-weight:900; color:white; margin-bottom:24px;">
                    Ready to understand?
                </p>
                <div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap; margin-bottom:32px;">
                    <a style="background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); color:white; padding:12px 28px; border-radius:9999px; font-size:14px; font-weight:600; text-decoration:none; cursor:pointer;">Privacy Policy</a>
                    <a style="background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); color:white; padding:12px 28px; border-radius:9999px; font-size:14px; font-weight:600; text-decoration:none; cursor:pointer;">About JUA</a>
                    <a style="background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); color:white; padding:12px 28px; border-radius:9999px; font-size:14px; font-weight:600; text-decoration:none; cursor:pointer;">Sunbird AI</a>
                </div>
                <p style="color:#4b5563; font-size:11px; letter-spacing:0.1em; text-transform:uppercase;">
                    © 2026 JUA · Powered by Sunbird AI · Built at MUST
                </p>
            </div>
        </div>
    """), unsafe_allow_html=True)

# 6. MAIN APP
else:
    # Header
    st.markdown(textwrap.dedent(f"""
        <div class="header-container">
            <div class="jua-title">
                {render_svg(SVG_SUN, 48, "#F5A623", 2.5)} JUA
            </div>
            <div class="jua-subtitle">Translate & Summarize to Ugandan Local Languages</div>
        </div>
    """), unsafe_allow_html=True)

    # STEP 1 — LANGUAGE
    render_step_label("TRANSLATE INTO", SVG_PIN)
    target_language = st.selectbox(
        "Target Language",
        ["Luganda", "Runyankole", "Ateso", "Lugbara", "Acholi"],
        label_visibility="collapsed"
    )

    # STEP 2 — SOURCE TYPE
    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
    render_step_label("SOURCE TYPE", SVG_FILE)

    source_options = [
        ("whatsapp", SVG_MSG, "WhatsApp Message"),
        ("radio", SVG_RADIO, "Radio Announcement"),
        ("health", SVG_HEALTH, "Health Bulletin"),
        ("government", SVG_LANDMARK, "Government Notice"),
        ("community", SVG_MEGAPHONE, "Community Announcement"),
        ("other", SVG_FILE, "Other Document"),
        ("text", SVG_EDIT, "Type / Paste Text"),
        ("audio", SVG_MIC, "Record / Upload Audio")
    ]

    st.markdown('<div class="source-grid-container" style="position: relative;">', unsafe_allow_html=True)
    
    # 2-column grid for all 8 options
    for i in range(0, 8, 2):
        cols = st.columns(2)
        for j in range(2):
            idx = i + j
            if idx < len(source_options):
                key, icon, label = source_options[idx]
                with cols[j]:
                    is_selected = st.session_state.source_type == key
                    card_class = "source-card-unit selected" if is_selected else "source-card-unit"
                    icon_color = "#ffffff" if is_selected else "#6b7280"
                    label_color = "#ffffff" if is_selected else "#374151"
                    
                    # Unified Card with Absolute Overlay Button
                    st.markdown(textwrap.dedent(f"""
                        <div class="{card_class}" style="margin-bottom: 12px;">
                            {render_svg(icon, 24, icon_color, 1.5)}
                            <div class="source-card-label" style="color: {label_color};">{label}</div>
                        </div>
                    """), unsafe_allow_html=True)
                    
                    if st.button(" ", key=f"btn_{key}", use_container_width=True):
                        st.session_state.source_type = key
                        st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

    # 8. STEP 3 — DYNAMIC INPUT CARD
    st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
    source_type = st.session_state.source_type
    
    input_title = "RECORD OR UPLOAD AUDIO" if source_type == "audio" else "INPUT INFORMATION"
    input_icon = SVG_MIC if source_type == "audio" else SVG_EDIT
    render_step_label(input_title, input_icon)

    source_text = None
    audio_file = None
    audio_filename = None

    placeholders = {
        "whatsapp": "Paste the WhatsApp message here...",
        "radio": "Type or paste what was announced on radio...",
        "health": "Paste the health bulletin or notice...",
        "government": "Paste the government circular or announcement...",
        "community": "Paste or type the community announcement...",
        "other": "Paste your text here...",
        "text": "Paste or type your text here..."
    }

    # Unified Input Container
    with st.container(border=True):
        if source_type == "audio":
            audio_file = st.file_uploader("Upload Audio", type=["mp3", "wav"], label_visibility="collapsed")
            recorded_audio = st.audio_input("Record audio", label_visibility="collapsed")
            if recorded_audio:
                audio_file = recorded_audio
                audio_filename = "recording.wav"
            elif audio_file:
                audio_filename = audio_file.name
            st.markdown('<div style="color: #888; font-size: 13px; margin-top: 8px; text-align: center;">Maximum 5 minutes. MP3 or WAV supported.</div>', unsafe_allow_html=True)
        else:
            source_text = st.text_area(
                "Input Area",
                placeholder=placeholders.get(source_type, "Paste your text here..."),
                height=250,
                label_visibility="collapsed"
            )
            if source_text:
                st.markdown(f'<div style="text-align: right; color: #888; font-size: 12px; margin-top: 4px;">{len(source_text)} characters</div>', unsafe_allow_html=True)
            else:
                st.info("💡 **Tip**: Once you paste text, click anywhere outside the box or press `Cmd+Enter` to enable the button.")

    # 9. PROCESS BUTTON
    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
    can_process = (source_text and len(source_text.strip()) > 0) or audio_file

    st.markdown('<div class="main-cta-btn">', unsafe_allow_html=True)
    process_btn = st.button("Understand & Translate →", use_container_width=True, disabled=not can_process, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    if process_btn:
        try:
            st.session_state.results = None
            with st.status("Analyzing your information... (Chunking for stability)", expanded=True) as status:
                st.write("Fetching source content...")
                results = run_pipeline(
                    text_input=source_text,
                    audio_file=audio_file,
                    audio_filename=audio_filename,
                    target_language=target_language,
                    source_type=source_type
                )
                st.session_state.results = results
                status.update(label="Analysis complete!", state="complete", expanded=False)
        except Exception as e:
            err_msg = str(e).lower()
            if "timed out" in err_msg or "read timeout" in err_msg:
                st.error("⏱️ The request is taking too long. JUA is currently chunking your text to improve success. Please try a slightly shorter version or wait a moment.")
            else:
                st.error(f"Something went wrong: {str(e)}")

    # 10. OUTPUT SECTION
    if st.session_state.results:
        results = st.session_state.results
        st.markdown('<div style="margin-top: 3rem;"></div>', unsafe_allow_html=True)
        
        # Determine visibility
        is_structured = source_type not in ["text", "audio"]
        
        # 1. WHAT THIS SAYS (Show for ALL types)
        if results.get("summary"):
            st.markdown(f'<div class="step-label">{render_svg(SVG_INFO, 16, "#666")} SUMMARIZED ANALYSIS</div>', unsafe_allow_html=True)
            st.markdown(textwrap.dedent(f'<div class="output-card"><p>{results["summary"]}</p></div>'), unsafe_allow_html=True)

        # 2. WHAT YOU SHOULD DO (Only for structured)
        if is_structured and results.get("action_points"):
            st.markdown(f'<div class="step-label">{render_svg(SVG_CHECK, 16, "#666")} WHAT YOU SHOULD DO</div>', unsafe_allow_html=True)
            st.markdown(textwrap.dedent(f'<div class="output-card"><p>{results["action_points"]}</p></div>'), unsafe_allow_html=True)

        # 3. HEADS UP (Misinformation)
        if results.get("misinformation_flag"):
            st.markdown(f'<div class="step-label" style="color: #b45309;">{render_svg(SVG_ALERT, 16, "#b45309")} HEADS UP</div>', unsafe_allow_html=True)
            st.markdown(textwrap.dedent(f'<div class="output-card alert-card"><p style="color: #92400e; font-weight: 500;">This message contains claims we could not verify. Please confirm with your health worker, local authority, or trusted source before acting.</p></div>'), unsafe_allow_html=True)

        # 4. TRANSLATION (With Fallback)
        display_text = results.get("translated_summary")
        trans_label = f"LOCAL TRANSLATION ({target_language.upper()})"
        is_fallback = False
        
        if not display_text and results.get("summary"):
            display_text = results.get("summary")
            trans_label = f"SUMMARY (TRANSLATION UNAVAILABLE)"
            is_fallback = True
            
        if display_text:
            st.markdown(f'<div class="step-label">{render_svg(SVG_GLOBE, 16, "#666")} {trans_label}</div>', unsafe_allow_html=True)
            st.markdown(textwrap.dedent(f'<div class="output-card"><p>{"<em>(Showing English version as translation is pending or unavailable)</em><br><br>" if is_fallback else ""}{display_text}</p></div>'), unsafe_allow_html=True)

        # 5. SIMPLIFIED BROADCAST
        if is_structured and results.get("translated_action_points"):
            st.markdown(f'<div class="step-label">{render_svg(SVG_SEND, 16, "#666")} SIMPLIFIED BROADCAST</div>', unsafe_allow_html=True)
            source_label = next((l for k, i, l in source_options if k == source_type), "Information")
            broadcast_text = f"☀️ JUA — {source_label} · {target_language}\n\n{results['translated_action_points']}\n\n— JUA | Powered by Sunbird AI"
            st.markdown('<div class="output-card">', unsafe_allow_html=True)
            st.markdown(f'<p style="white-space: pre-wrap;">{broadcast_text}</p>', unsafe_allow_html=True)
            st.code(broadcast_text, language=None)
            st.markdown('</div>', unsafe_allow_html=True)

        # 6. LISTEN
        if results.get("audio_bytes"):
            st.markdown(f'<div class="step-label">{render_svg(SVG_VOLUME, 16, "#666")} LISTEN</div>', unsafe_allow_html=True)
            st.audio(results["audio_bytes"], format="audio/mp3")

        if st.button("Reset Analysis", use_container_width=True):
            st.session_state.results = None
            st.rerun()
