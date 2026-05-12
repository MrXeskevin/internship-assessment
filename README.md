---
title: Sunbird Translator and Summarizer
emoji: 🌻
colorFrom: yellow
colorTo: green
sdk: streamlit
app_file: app.py
pinned: false
---
#  Sunbird Translator and Summarizer

Sunbird Summarizer is a premium Streamlit-powered Generative AI application designed to make information accessible across languages in Uganda. The app allows users to input either text or audio, which is then transcribed (if audio), summarised using the state-of-the-art Sunflower LLM, translated into a choice of five major Ugandan languages (Luganda, Runyankole, Ateso, Lugbara, and Acholi), and finally converted back into speech. This end-to-end pipeline leverages Sunbird AI's specialized APIs to bridge communication gaps and provide concise, localized content for all users.

##  Pipeline Overview

Below is the ASCII representation of the processing pipeline:

```text
[ User Input ]
(Text or Audio)
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
[  Final Results ]
(Transcript, Summary, Translation, Audio Player)
```

##  Local Setup

Since the repository is already cloned, follow these steps to get started:

1. **Activate your virtual environment:**
   ```bash
   source venv/bin/activate  # On macOS/Linux
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Copy the example environment file and add your Sunbird API token.
   ```bash
   cp .env.example .env
   ```
   Open `.env` and replace `your_token_here` with your actual token.

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

##  Environment Variables

| Variable | Description | Requirement |
| :--- | :--- | :--- |
| `SUNBIRD_API_TOKEN` | Your Sunbird AI Bearer Token | Required |

##  Usage Walkthrough

1. **Select Language:** Choose your target Ugandan language from the dropdown menu.
2. **Choose Input Mode:** Toggle between "Text" and "Audio" using the radio buttons.
3. **Provide Input:**
   - **Text Mode:** Paste the long-form text you want to summarise.
   - **Audio Mode:** Upload an MP3 or WAV file (max 5 minutes). You can preview the audio before processing.
4. **Process:** Click the "Summarise & Translate" button.
5. **View Results:** The app will display the transcript (for audio), the summary, the translation, and an audio player to listen to the translated summary.

##  Hugging Face Spaces Deployment

To deploy this app to Hugging Face Spaces:

1. Create a new Space on [Hugging Face](https://huggingface.co/new-space).
2. Select **Streamlit** as the SDK.
3. Upload your project files (excluding `.env`, which should be ignored by `.gitignore`).
4. Go to **Settings** > **Variables and secrets** in your Space.
5. Add a new **Secret** named `SUNBIRD_API_TOKEN` with your API key.
6. The app will automatically build and deploy.

##  Known Limitations

- **Audio Duration:** Files are limited to 300 seconds (5 minutes) to ensure optimal processing.
- **Supported Languages:** Currently supports Luganda, Runyankole, Ateso, Lugbara, and Acholi.
- **File Formats:** Only `.mp3` and `.wav` audio formats are supported for direct upload.
- **Rate Limits:** Subject to Sunbird AI API rate limits based on your account tier.
