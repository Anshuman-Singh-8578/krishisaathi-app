import streamlit as st
import random
import requests
from datetime import datetime
import re

# ---------------------- VOICE RECOGNITION SETUP ----------------------
try:
    import speech_recognition as sr
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

# ---------------------- STREAMLIT CONFIG ----------------------
st.set_page_config(
    page_title="🌾 Krishisaathi AI", 
    page_icon="🌱", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Show voice warning only if not available
if not VOICE_AVAILABLE:
    st.sidebar.warning("⚠️ Voice recognition not available. Install: pip install SpeechRecognition pyaudio")

# ---------------------- TRANSLATION SETUP ----------------------
try:
    from deep_translator import GoogleTranslator
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False
    st.warning("⚠️ Translation library not available. Install: pip install deep-translator")

# ---------------------- LANGUAGE CONFIGURATION ----------------------
SUPPORTED_LANGUAGES = {
    'en': {'name': 'English', 'flag': '🇬🇧'},
    'hi': {'name': 'हिन्दी', 'flag': '🇮🇳'},
}

# ---------------------- UI TEXT TRANSLATIONS ----------------------
UI_TRANSLATIONS = {
    'en': {
        'app_title': 'KRISHISAATHI AI',
        'app_tagline': 'Connecting Farmers, Empowering Growth',
        'select_language': 'Select Your Language',
        'quick_actions': '🎯 Quick Actions',
        'disease_detection': '📷 Disease Detection',
        'delhi_prices': '🏙️ Delhi Prices',
        'mumbai_weather': '🌤️ Mumbai Weather',
        'crop_tips': '🌾 Crop Tips',
        'clear_chat': '🗑️ Clear Chat',
        'voice_input': '🎤 Voice Input',
        'chat_placeholder': 'Ask about farming...',
    },
    'hi': {
        'app_title': 'कृषिसाथी एआई',
        'app_tagline': 'किसानों को जोड़ना, विकास को सशक्त बनाना',
        'select_language': 'अपनी भाषा चुनें',
        'quick_actions': '🎯 त्वरित कार्य',
        'disease_detection': '📷 रोग पहचान',
        'delhi_prices': '🏙️ दिल्ली की कीमतें',
        'mumbai_weather': '🌤️ मुंबई का मौसम',
        'crop_tips': '🌾 फसल सुझाव',
        'clear_chat': '🗑️ चैट साफ करें',
        'voice_input': '🎤 वॉइस इनपुट',
        'chat_placeholder': 'खेती के बारे में पूछें...',
    }
}

def get_ui_text(key, lang='en'):
    """Get translated UI text"""
    return UI_TRANSLATIONS.get(lang, UI_TRANSLATIONS['en']).get(key, UI_TRANSLATIONS['en'][key])

# ---------------------- VOICE RECOGNITION FUNCTION ----------------------
def recognize_speech():
    """Capture and recognize speech from microphone"""
    if not VOICE_AVAILABLE:
        return None, "Voice recognition library not installed"
    
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening... Please speak now (5 seconds)")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            st.info("🔄 Processing voice...")
            text = recognizer.recognize_google(audio, language='en-IN')
            return text, None
            
    except sr.WaitTimeoutError:
        return None, "⏱️ Timeout: No speech detected. Please try again."
    except sr.UnknownValueError:
        return None, "❓ Could not understand audio. Please speak clearly."
    except sr.RequestError:
        return None, "🌐 Network error: Could not reach Google Speech API."
    except Exception as e:
        return None, f"⚠️ Error: {str(e)}"

# ---------------------- INITIALIZE SESSION STATE ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_language" not in st.session_state:
    st.session_state.selected_language = 'en'

current_lang = st.session_state.selected_language

# ---------------------- SIMPLE CSS ----------------------
st.markdown("""
<style>
    .main {background: #1a1a1a;}
    .stChatMessage {
        background: #2d2d2d !important;
        border-radius: 12px !important;
        border: 1px solid #4caf50 !important;
        color: #e0e0e0 !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------- HEADER ----------------------
st.title(f"🌾 {get_ui_text('app_title', current_lang)}")
st.caption(get_ui_text('app_tagline', current_lang))
st.divider()

# ---------------------- SIDEBAR ----------------------
with st.sidebar:
    st.markdown(f"### {get_ui_text('quick_actions', current_lang)}")
    
    # Language selector
    selected_lang = st.selectbox(
        get_ui_text('select_language', current_lang),
        options=list(SUPPORTED_LANGUAGES.keys()),
        format_func=lambda x: f"{SUPPORTED_LANGUAGES[x]['flag']} {SUPPORTED_LANGUAGES[x]['name']}",
        index=list(SUPPORTED_LANGUAGES.keys()).index(st.session_state.selected_language)
    )
    
    if selected_lang != st.session_state.selected_language:
        st.session_state.selected_language = selected_lang
        st.rerun()
    
    st.divider()
    
    # Voice input button
    if VOICE_AVAILABLE:
        if st.button(get_ui_text('voice_input', current_lang), use_container_width=True):
            text, error = recognize_speech()
            
            if error:
                st.error(error)
            elif text:
                st.success(f"✅ Voice captured: {text}")
                st.session_state.messages.append({"role": "user", "content": text})
                st.session_state.messages.append({"role": "assistant", "content": f"You said: {text}"})
                st.rerun()
    
    st.divider()
    
    if st.button(get_ui_text('clear_chat', current_lang), use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------------------- CHAT INTERFACE ----------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------- CHAT INPUT ----------------------
if prompt := st.chat_input(get_ui_text('chat_placeholder', current_lang)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = f"You asked: {prompt}\n\nI'm Krishisaathi AI, your farming assistant! 🌾"
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
