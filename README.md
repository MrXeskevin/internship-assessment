---
title: Sunbird Translator and Summarizer
emoji: 🌻
colorFrom: yellow
colorTo: green
sdk: streamlit
app_file: app.py
pinned: false
license: mit
short_description: 'To translate audio and text to Local Ug Languages'
---
#  Sunbird Translator and Summarizer

Sunbird Summarizer is a premium Streamlit-powered Generative AI application designed to make information accessible across languages in Uganda. The app allows users to input either text or audio, which is then transcribed (if audio), summarised using the state-of-the-art Sunflower LLM, translated into a choice of five major Ugandan languages (Luganda, Runyankole, Ateso, Lugbara, and Acholi), and finally converted back into speech. This end-to-end pipeline leverages Sunbird AI's specialized APIs to bridge communication gaps and provide concise, localized content for all users.

##  Pipeline Overview

The Sunbird Translator and Summarizer uses a multi-stage AI pipeline to process and localize content. Below is the technical architecture:

```text
[ User Input ] ----> (Text or Audio/Recording)
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
[  Translation ]
(Sunflower LLM: /tasks/sunflower_simple)
       |
       v
[  Text-to-Speech ]
(Sunbird API: /tasks/tts)
       |
       v
[ Final Results ]
(Transcript, Summary, Translation, Audio Player)
```

##  Local Setup

Follow these exact steps to run the application on your machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MrXeskevin/internship-assessment.git
   cd internship-assessment
   ```

2. **Activate your virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Create a `.env` file from the provided example and add your Sunbird API token.
   ```bash
   cp .env.example .env
   ```
   *Edit the `.env` file and replace `your_token_here` with your actual token.*

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

##  Environment Variables

| Variable | Description | Requirement |
| :--- | :--- | :--- |
| `SUNBIRD_API_TOKEN` | Your Sunbird AI Bearer Token for authentication. | Required |

##  Usage Walkthrough

1. **Select Language:** Choose your target Ugandan language from the dropdown menu.
2. **Choose Input Mode:** Toggle between "Text", "Audio", or "Record".
3. **Provide Input:**
   - **Text Mode:** Paste the long-form text you want to summarise.
   - **Audio Mode:** Upload an MP3 or WAV file (max 5 minutes).
   - **Record Mode:** Click to record your voice directly in the browser.
4. **Process:** Click the **"Summarise & Translate"** button.
5. **View Results:** The app will display the transcript (for audio), the summary, the translation, and an audio player.
   - *Screenshots of the end-to-end flow are available in the repository's `assets` folder.*

##  Deployed App

You can try the live version of the application here:
 **[Sunbird Translator & Summarizer on Hugging Face Spaces](https://huggingface.co/spaces/Kevin34Mugenyi/Sunbird-Translator-and-Summarizer)**

##  Hugging Face Spaces Deployment

To deploy this app to your own Hugging Face Space:

1. Create a new Space on [Hugging Face](https://huggingface.co/new-space).
2. Select **Streamlit** as the SDK.
3. Upload your project files (ensure `backend/__init__.py` is included for package recognition).
4. Go to **Settings** > **Variables and secrets** in your Space.
5. Add a new **Secret** named `SUNBIRD_API_TOKEN` with your API key.
6. The app will automatically build and deploy.

##  Known Limitations

- **Audio Duration:** Files are limited to 300 seconds (5 minutes) for stability.
- **Supported Languages:** Luganda, Runyankole, Ateso, Lugbara, and Acholi.
- **File Formats:** Supports `.mp3` and `.wav`.
- **API Limits:** Subject to Sunbird AI API rate limits.
