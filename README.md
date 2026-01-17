# 🌍 Dialect-Aware Multilingual Translator

This project is an AI-powered Streamlit application that detects Indian
languages and Hindi dialects (such as Bhojpuri, Haryanvi, Awadhi, etc.)
and translates text into the selected dialect using natural, regional expressions.
It also provides voice output for translated text.

---

## 🚀 Features

- 🔍 Automatic language & Hindi dialect detection  
- 🗺️ Recognizes regional Hindi variants (Bhojpuri, Haryanvi, Awadhi, etc.)  
- 🎯 Auto-selects target dialect based on detected input  
- 🔊 Text-to-Speech voice output for translated text  
- 🌐 Supports multiple target languages  
- 🖥️ Simple and clean Streamlit UI  

---

## 🛠️ Tech Stack

- Python 3.11  
- Streamlit  
- Google Gemini API  
- gTTS (Text-to-Speech)  

---

## 📦 Installation

Install the required dependencies:
```bash
pip install -r requirements.txt

---

##▶️ How to Run the App

- Run the Streamlit application:
- streamlit run app.py
- Open your browser at:http://localhost:8501

---

##🔐 API Key Setup

- This project uses the Google Gemini API.
- Set your API key as an environment variable.
- Windows (PowerShell)
  setx GEMINI_API_KEY "your_api_key_here"
- macOS / Linux
  export GEMINI_API_KEY="your_api_key_here"

---

##📌 Project Objective

To build a dialect-aware AI translation system that:
- Detects Indian languages and Hindi dialects
- Translates text into regionally accurate language
- Supports voice output for better accessibility

---

##👨‍🎓 Academic Use

This project is developed as part of an academic submission and demonstrates:
- NLP-based language understanding
- Dialect-aware translation
- Practical AI application using Streamlit
