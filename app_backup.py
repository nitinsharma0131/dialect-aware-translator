import streamlit as st
import google.generativeai as genai
import json
import re
import tempfile
from gtts import gTTS

# =========================
# CONFIG
# =========================

genai.configure(api_key="AIzaSyAd-3ciZd9tzGOrj7robtHQvRyMvTWZ4_A")

DETECT_MODEL = genai.GenerativeModel("models/gemini-flash-lite-latest")
TRANSLATE_MODEL = genai.GenerativeModel("models/gemini-flash-latest")
AUDIO_MODEL = genai.GenerativeModel("models/gemini-2.5-flash-native-audio-latest")

st.set_page_config(
    page_title="AI Multilingual Translator",
    page_icon="🌍",
    layout="wide"
)

# =========================
# UTILITY FUNCTIONS
# =========================

@st.cache_data(show_spinner=False)
def detect_language_and_dialect(text):
    prompt = f"""
Return ONLY valid JSON. No markdown. No explanation.

{{
  "language": "",
  "dialect": "",
  "state_region": "",
  "tone": ""
}}

Text:
{text}
"""
    response = DETECT_MODEL.generate_content(prompt)

    cleaned = re.sub(r"```json|```", "", response.text).strip()
    return json.loads(cleaned)


def map_detected_to_target(detected):
    dialect = detected.get("dialect", "").lower()

    if "bhojpuri" in dialect:
        return "Bhojpuri (Bihar / UP)"
    if "haryanvi" in dialect:
        return "Haryanvi (Haryana)"
    if "awadhi" in dialect:
        return "Awadhi (UP)"
    if "bundeli" in dialect:
        return "Bundeli (MP)"
    if "rajasthani" in dialect:
        return "Rajasthani"

    return "Standard Hindi"


def text_to_speech(text):
    tts = gTTS(text=text, lang="hi")
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    return temp_audio.name


def transcribe_audio(audio_file):
    prompt = "Transcribe this audio into accurate text."
    response = AUDIO_MODEL.generate_content(
        [
            prompt,
            {"mime_type": audio_file.type, "data": audio_file.read()},
        ]
    )
    return response.text.strip()

# =========================
# UI
# =========================

st.title("🌍 AI Multilingual Translator")
st.caption("Dialect-aware Indian language translation with voice input & output")

col1, col2 = st.columns(2)

# ---------- LEFT COLUMN ----------
with col1:
    text = st.text_area("Enter text", height=160)
    auto_detect = st.checkbox("🔍 Auto-detect Hindi dialect", value=True)

    audio_input = st.file_uploader(
        "🎙️ Or upload voice (Hindi / English)",
        type=["wav", "mp3", "m4a"]
    )

    if audio_input:
        with st.spinner("Transcribing audio..."):
            text = transcribe_audio(audio_input)
        st.success("Audio transcribed")
        st.text_area("Transcribed text", text, height=120)

    if st.button("🔍 Detect Input Dialect"):
        if not text.strip():
            st.warning("Please enter some text")
        else:
            with st.spinner("Detecting language & dialect..."):
                detected = detect_language_and_dialect(text)
                st.session_state["detected"] = detected
                st.session_state["auto_dialect"] = map_detected_to_target(detected)

            st.subheader("Detected Language & Dialect")
            st.json(detected)

# ---------- RIGHT COLUMN ----------
with col2:
    target_language = st.selectbox(
        "Translate to",
        [
            "Hindi (Formal)",
            "Hindi (Casual)",
            "Spanish",
            "French",
            "German",
            "Tamil",
            "Telugu",
        ]
    )

    target_dialect = st.selectbox(
        "Translate into Hindi dialect",
        [
            "Standard Hindi",
            "Haryanvi (Haryana)",
            "Bhojpuri (Bihar / UP)",
            "Awadhi (UP)",
            "Bundeli (MP)",
            "Rajasthani",
            "Punjabi-influenced Hindi",
        ],
        index=0,
    )

    if auto_detect and "auto_dialect" in st.session_state:
        target_dialect = st.session_state["auto_dialect"]
        st.info(f"🎯 Auto-selected dialect: {target_dialect}")

# =========================
# TRANSLATION
# =========================

if st.button("🚀 Translate"):
    if not text.strip():
        st.warning("Please enter text to translate")
        st.stop()

    detected_info = st.session_state.get("detected", {})

    prompt = f"""
Detected input details:
{detected_info}

Translate the following text into {target_dialect}.

Rules:
- Preserve regional meaning
- Use natural local expressions
- Avoid textbook or overly formal Hindi

Text:
{text}
"""

    try:
        with st.spinner("Translating..."):
            response = TRANSLATE_MODEL.generate_content(prompt)

        translated_text = response.text.strip()

        st.success("Translation complete")
        st.text_area("Output", translated_text, height=160)

        audio_path = text_to_speech(translated_text)
        st.audio(audio_path, format="audio/mp3")

    except Exception:
        st.error("⚠️ API quota exceeded. Please wait and try again later.")
