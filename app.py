
import os
import streamlit as st
import google.generativeai as genai
import json
import re
import tempfile
from gtts import gTTS

# =========================
# CONFIG
# =========================
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

DETECT_MODEL = genai.GenerativeModel("models/gemini-flash-lite-latest")
TRANSLATE_MODEL = genai.GenerativeModel("models/gemini-flash-latest")

st.set_page_config(
    page_title="AI Multilingual Translator",
    page_icon="🌍",
    layout="wide"
)

# =========================
# STEP 1: DETECTION
# =========================

@st.cache_data(show_spinner=False)
def detect_hindi_dialect(text):
    prompt = f"""
Return ONLY valid JSON.
No markdown.
No explanation.

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


# =========================
# STEP 2: MAP DIALECT
# =========================

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


# =========================
# STEP 3.1: DROPDOWN INDEX
# =========================

def dialect_to_index(dialect):
    dialects = [
        "Standard Hindi",
        "Haryanvi (Haryana)",
        "Bhojpuri (Bihar / UP)",
        "Awadhi (UP)",
        "Bundeli (MP)",
        "Rajasthani",
        "Punjabi-influenced Hindi",
    ]

    try:
        return dialects.index(dialect)
    except ValueError:
        return 0


# =========================
# VOICE OUTPUT (TTS)
# =========================

def speak_text(text):
    tts = gTTS(text=text, lang="hi")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    return tmp.name


# =========================
# UI
# =========================

st.title("🌍 AI Multilingual Translator")
st.caption("Dialect-aware Indian language translation with voice support")

col1, col2 = st.columns(2)

# ---------- LEFT ----------
with col1:
    text = st.text_area("Enter text", height=160)
    auto_detect = st.checkbox("🔍 Auto-detect Hindi dialect", value=True)

    if st.button("🔍 Detect Input Dialect"):
        if not text.strip():
            st.warning("Please enter text")
        else:
            with st.spinner("Detecting dialect..."):
                detected = detect_hindi_dialect(text)
                st.session_state["detected"] = detected
                st.session_state["auto_dialect"] = map_detected_to_target(detected)

            st.subheader("Detected Language & Dialect")
            st.json(detected)

            # Clean summary (no NameError)
            st.markdown("### 🧠 Detection Summary")
            st.info(
                f"""
**Language:** {detected.get('language', 'N/A')}  
**Dialect:** {detected.get('dialect', 'N/A')}  
**Region:** {detected.get('state_region', 'N/A')}  
**Tone:** {detected.get('tone', 'N/A')}
"""
            )

# ---------- RIGHT ----------
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
        ],
    )

    detected_dialect = st.session_state.get("auto_dialect", "Standard Hindi")

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
        index=dialect_to_index(detected_dialect),
    )

    if auto_detect and "auto_dialect" in st.session_state:
        st.info(f"🎯 Auto-selected dialect: {detected_dialect}")

# =========================
# TRANSLATE BUTTON (BASIC)
# =========================

if st.button("🚀 Translate"):
    if not text.strip():
        st.warning("Please enter text")
        st.stop()

    detected_info = st.session_state.get("detected", {})

    # Decide translation behavior
    if "Hindi" in target_language:
        translation_instruction = f"""
Translate the text into Hindi.
Dialect: {target_dialect}

Rules:
- Preserve regional meaning
- Use natural spoken expressions
- Avoid textbook Hindi
"""
    else:
        translation_instruction = f"""
Translate the text into {target_language}.
Ensure natural, fluent translation.
"""

    prompt = f"""
Detected input:
{detected_info}

{translation_instruction}

Text:
{text}
"""

    try:
        with st.spinner("Translating..."):
            response = TRANSLATE_MODEL.generate_content(prompt)

        st.success("Translation complete")
        st.text_area("Output", response.text, height=160)

        audio_file = speak_text(response.text)
        st.audio(audio_file, format="audio/mp3")

    except Exception as e:
        st.error("⚠️ API quota exceeded or error occurred.")
        st.exception(e)

import os
import streamlit as st
import google.generativeai as genai
import json
import re
import tempfile
from gtts import gTTS

# =========================
# CONFIG
# =========================
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

DETECT_MODEL = genai.GenerativeModel("models/gemini-flash-lite-latest")
TRANSLATE_MODEL = genai.GenerativeModel("models/gemini-flash-latest")

st.set_page_config(
    page_title="AI Multilingual Translator",
    page_icon="🌍",
    layout="wide"
)

# =========================
# STEP 1: DETECTION
# =========================

@st.cache_data(show_spinner=False)
def detect_hindi_dialect(text):
    prompt = f"""
Return ONLY valid JSON.
No markdown.
No explanation.

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


# =========================
# STEP 2: MAP DIALECT
# =========================

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


# =========================
# STEP 3.1: DROPDOWN INDEX
# =========================

def dialect_to_index(dialect):
    dialects = [
        "Standard Hindi",
        "Haryanvi (Haryana)",
        "Bhojpuri (Bihar / UP)",
        "Awadhi (UP)",
        "Bundeli (MP)",
        "Rajasthani",
        "Punjabi-influenced Hindi",
    ]

    try:
        return dialects.index(dialect)
    except ValueError:
        return 0


# =========================
# VOICE OUTPUT (TTS)
# =========================

def speak_text(text):
    tts = gTTS(text=text, lang="hi")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    return tmp.name


# =========================
# UI
# =========================

st.title("🌍 AI Multilingual Translator")
st.caption("Dialect-aware Indian language translation with voice support")

col1, col2 = st.columns(2)

# ---------- LEFT ----------
with col1:
    text = st.text_area("Enter text", height=160)
    auto_detect = st.checkbox("🔍 Auto-detect Hindi dialect", value=True)

    if st.button("🔍 Detect Input Dialect"):
        if not text.strip():
            st.warning("Please enter text")
        else:
            with st.spinner("Detecting dialect..."):
                detected = detect_hindi_dialect(text)
                st.session_state["detected"] = detected
                st.session_state["auto_dialect"] = map_detected_to_target(detected)

            st.subheader("Detected Language & Dialect")
            st.json(detected)

            # Clean summary (no NameError)
            st.markdown("### 🧠 Detection Summary")
            st.info(
                f"""
**Language:** {detected.get('language', 'N/A')}  
**Dialect:** {detected.get('dialect', 'N/A')}  
**Region:** {detected.get('state_region', 'N/A')}  
**Tone:** {detected.get('tone', 'N/A')}
"""
            )

# ---------- RIGHT ----------
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
        ],
    )

    detected_dialect = st.session_state.get("auto_dialect", "Standard Hindi")

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
        index=dialect_to_index(detected_dialect),
    )

    if auto_detect and "auto_dialect" in st.session_state:
        st.info(f"🎯 Auto-selected dialect: {detected_dialect}")

# =========================
# TRANSLATE BUTTON (BASIC)
# =========================

if st.button("🚀 Translate"):
    if not text.strip():
        st.warning("Please enter text")
        st.stop()

    detected_info = st.session_state.get("detected", {})

    # Decide translation behavior
    if "Hindi" in target_language:
        translation_instruction = f"""
Translate the text into Hindi.
Dialect: {target_dialect}

Rules:
- Preserve regional meaning
- Use natural spoken expressions
- Avoid textbook Hindi
"""
    else:
        translation_instruction = f"""
Translate the text into {target_language}.
Ensure natural, fluent translation.
"""

    prompt = f"""
Detected input:
{detected_info}

{translation_instruction}

Text:
{text}
"""

    try:
        with st.spinner("Translating..."):
            response = TRANSLATE_MODEL.generate_content(prompt)

        st.success("Translation complete")
        st.text_area("Output", response.text, height=160)

        audio_file = speak_text(response.text)
        st.audio(audio_file, format="audio/mp3")

    except Exception as e:
        st.error("⚠️ API quota exceeded or error occurred.")
        st.exception(e)

