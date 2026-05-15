---
title: JUA — Translate & Summarize
emoji: ☀️
colorFrom: blue
colorTo: orange
sdk: streamlit
app_file: app.py
pinned: false
license: mit
short_description: 'AI localization for Ugandan languages (Text & Audio)'
---

# ☀️ JUA — Translate & Summarize

**JUA** (Swahili for "Know") is a premium, AI-powered localization platform designed to bridge communication gaps in Uganda. Built for the MUST (Mbarara University of Science and Technology) community and beyond, JUA simplifies complex information—from government notices to WhatsApp forwards—into concise, understandable summaries in major Ugandan local languages.

[![Live App](https://img.shields.io/badge/Hugging%20Face-Spaces-blue?logo=huggingface)](https://huggingface.co/spaces/Kevin34Mugenyi/Sunbird-Translator-and-Summarizer)

## ✨ Key Features

### 1. Intelligent Source Categorization
JUA isn't just a translator; it understands the *context* of your information. Choose from 8 specialized source types to get tailored analysis:
*   **WhatsApp Messages:** Cut through the noise of group chats.
*   **Radio Announcements:** Record and summarize what you heard on air.
*   **Health Bulletins:** Get clear action points from medical notices.
*   **Government Notices:** Simplify official circulars and notices.
*   **Community Announcements:** Stay informed about local developments.
*   **Multi-modal Input:** Type text, upload files, or **record your voice** directly in the browser.

### 2. Deep Analysis & Actionable Insights
*   **Summarized Analysis:** Get the "big picture" in seconds.
*   **Action Points:** Clear "What you should do" instructions derived from the input.
*   **Misinformation Flagging:** A built-in "Heads Up" feature that alerts users to unverified claims or potential misinformation.
*   **Simplified Broadcasts:** Generates ready-to-share text snippets for sharing back to community groups.

### 3. Local Language Localization
Translate and synthesize speech in 5 major Ugandan languages:
*   🇺🇬 **Luganda**
*   🇺🇬 **Runyankole**
*   🇺🇬 **Ateso**
*   🇺🇬 **Lugbara**
*   🇺🇬 **Acholi**

## 🛠️ Technical Pipeline

The JUA engine orchestrates a sophisticated multi-stage AI pipeline using Sunbird AI APIs:

```text
[ User Input ] ----> (Text / Audio / Recording)
       |
       v
[  Speech-to-Text ] ----> (Audio Mode Only)
(Sunbird API: /tasks/stt)
       |
       v
[  Summarisation ]
(Sunflower LLM: /tasks/sunflower_simple)
       |
       v
[  Action Extraction ]
(Sunflower LLM: /tasks/sunflower_simple)
       |
       v
[  Translation ]
(Sunflower LLM: /tasks/sunflower_simple)
       |
       v
[  Text-to-Speech ]
(Sunbird API: /tasks/tts)
       |
       v
[  Final Results ]
(Summary, Actions, Translation, Audio Player)
```

## 🚀 Local Setup

### Prerequisites
*   Python 3.9+
*   Sunbird AI API Token ([Get one here](https://docs.sunbird.ai/))

### Installation
1. **Clone the repo:**
   ```bash
   git clone https://github.com/MrXeskevin/internship-assessment.git
   cd internship-assessment
   ```

2. **Setup Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Secrets:**
   Create a `.env` file:
   ```env
   SUNBIRD_API_TOKEN=your_actual_token_here
   ```

4. **Run App:**
   ```bash
   streamlit run app.py
   ```

## 🌐 Deployment

### Hugging Face Spaces
1. Create a new Streamlit Space.
2. Push this repository to the Space's remote.
3. Add `SUNBIRD_API_TOKEN` as a **Secret** in the Space settings.

## 📝 Known Limitations
*   **Audio Cap:** Maximum 5 minutes (300s) per recording/upload.
*   **Language Scope:** Currently optimized for the 5 supported Ugandan languages.
*   **API Stability:** Performance depends on Sunbird AI API availability; chunking is used to improve stability for long texts.

---
*Built with ❤️ at MUST. Powered by Sunbird AI.*
