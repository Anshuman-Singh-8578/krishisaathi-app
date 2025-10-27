import streamlit as st
import random
import requests
from datetime import datetime
import re

# ---------------------- STREAMLIT CONFIG ----------------------
st.set_page_config(
    page_title="🌾 Krishisaathi AI", 
    page_icon="🌱", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------- TRANSLATION SETUP ----------------------
try:
    from deep_translator import GoogleTranslator
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False
    st.warning("⚠️ Translation library not available. Install: pip install deep-translator")

# ---------------------- SPEECH RECOGNITION SETUP ----------------------
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    st.warning("⚠️ Speech recognition not available. Install: pip install SpeechRecognition pyaudio")

# ---------------------- LANGUAGE CONFIGURATION ----------------------
SUPPORTED_LANGUAGES = {
    'en': {'name': 'English', 'flag': '🇬🇧', 'sr_code': 'en-US'},
    'hi': {'name': 'हिन्दी', 'flag': '🇮🇳', 'sr_code': 'hi-IN'},
    'mr': {'name': 'मराठी', 'flag': '🇮🇳', 'sr_code': 'mr-IN'},
    'ta': {'name': 'தமிழ்', 'flag': '🇮🇳', 'sr_code': 'ta-IN'},
    'te': {'name': 'తెలుగు', 'flag': '🇮🇳', 'sr_code': 'te-IN'},
    'bn': {'name': 'বাংলা', 'flag': '🇮🇳', 'sr_code': 'bn-IN'},
    'gu': {'name': 'ગુજરાતી', 'flag': '🇮🇳', 'sr_code': 'gu-IN'},
    'kn': {'name': 'ಕನ್ನಡ', 'flag': '🇮🇳', 'sr_code': 'kn-IN'},
    'ml': {'name': 'മലയാളം', 'flag': '🇮🇳', 'sr_code': 'ml-IN'},
    'pa': {'name': 'ਪੰਜਾਬੀ', 'flag': '🇮🇳', 'sr_code': 'pa-IN'}
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
        'upload_image': '📸 Upload Crop Image',
        'choose_image': 'Choose an image',
        'uploaded_image': 'Uploaded Image',
        'analyzing': '🔬 Analyzing...',
        'detection_complete': '✅ Detection Complete!',
        'disease': 'Disease',
        'confidence': 'Confidence',
        'done': '✅ Done',
        'chat_placeholder': 'Ask about farming...',
        'thinking': '🌱 Thinking...',
        'footer_title': '🌾 Krishisaathi AI',
        'footer_tagline': 'Empowering Farmers with Technology',
        'footer_copyright': '© 2025 Krishisaathi AI. All rights reserved.',
        'smart_assistant': 'Smart Farming Assistant',
        'show_prices': 'Show prices in',
        'weather_in': 'Weather in',
        'tell_about': 'Tell me about wheat',
        'check_disease': 'Check crop disease',
        'voice_input': '🎤 Voice Input',
        'start_recording': '🎙️ Start Recording',
        'stop_recording': '⏹️ Stop Recording',
        'recording': '🔴 Recording...',
        'processing_audio': '⚙️ Processing audio...',
        'voice_detected': '✅ Voice detected:',
        'no_speech': '❌ No speech detected. Please try again.',
        'voice_error': '❌ Voice recognition error. Please try again.',
        'listening': '👂 Listening...',
        'speak_now': '🗣️ Speak now in any language!'
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
        'upload_image': '📸 फसल की तस्वीर अपलोड करें',
        'choose_image': 'एक तस्वीर चुनें',
        'uploaded_image': 'अपलोड की गई तस्वीर',
        'analyzing': '🔬 विश्लेषण कर रहे हैं...',
        'detection_complete': '✅ पहचान पूर्ण!',
        'disease': 'रोग',
        'confidence': 'विश्वास',
        'done': '✅ पूर्ण',
        'chat_placeholder': 'खेती के बारे में पूछें...',
        'thinking': '🌱 सोच रहे हैं...',
        'footer_title': '🌾 कृषिसाथी एआई',
        'footer_tagline': 'प्रौद्योगिकी से किसानों को सशक्त बनाना',
        'footer_copyright': '© 2025 कृषिसाथी एआई। सर्वाधिकार सुरक्षित।',
        'smart_assistant': 'स्मार्ट खेती सहायक',
        'show_prices': 'कीमतें दिखाएं',
        'weather_in': 'मौसम',
        'tell_about': 'गेहूं के बारे में बताएं',
        'check_disease': 'फसल रोग जांचें',
        'voice_input': '🎤 आवाज इनपुट',
        'start_recording': '🎙️ रिकॉर्डिंग शुरू करें',
        'stop_recording': '⏹️ रिकॉर्डिंग बंद करें',
        'recording': '🔴 रिकॉर्ड हो रहा है...',
        'processing_audio': '⚙️ ऑडियो प्रोसेस हो रहा है...',
        'voice_detected': '✅ आवाज पहचानी गई:',
        'no_speech': '❌ कोई भाषण नहीं पहचाना गया। कृपया पुनः प्रयास करें।',
        'voice_error': '❌ आवाज पहचान त्रुटि। कृपया पुनः प्रयास करें।',
        'listening': '👂 सुन रहे हैं...',
        'speak_now': '🗣️ अब किसी भी भाषा में बोलें!'
    }
}

def get_ui_text(key, lang='en'):
    """Get translated UI text"""
    return UI_TRANSLATIONS.get(lang, UI_TRANSLATIONS['en']).get(key, UI_TRANSLATIONS['en'][key])

# ---------------------- TRANSLATION FUNCTIONS ----------------------
def translate_text(text, target_lang='en', source_lang='auto'):
    """Translate text to target language"""
    if not TRANSLATION_AVAILABLE or target_lang == 'en':
        return text
    
    try:
        translator = GoogleTranslator(source='auto', target=target_lang)
        return translator.translate(text)
    except Exception as e:
        return text

def detect_language(text):
    """Detect the language of input text"""
    if not TRANSLATION_AVAILABLE:
        return 'en'
    
    try:
        from langdetect import detect
        detected = detect(text)
        # Map detected language to our supported languages
        lang_map = {
            'en': 'en', 'hi': 'hi', 'mr': 'mr', 'ta': 'ta', 
            'te': 'te', 'bn': 'bn', 'gu': 'gu', 'kn': 'kn', 
            'ml': 'ml', 'pa': 'pa'
        }
        return lang_map.get(detected, 'en')
    except:
        return 'en'

# ---------------------- VOICE RECOGNITION FUNCTION ----------------------
def recognize_speech_from_mic(language_code='en-US'):
    """
    Capture audio from microphone and convert to text
    Returns: (success, text/error_message)
    """
    if not SPEECH_RECOGNITION_AVAILABLE:
        return False, "Speech recognition not available. Please install: pip install SpeechRecognition pyaudio"
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    try:
        # Adjust for ambient noise
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            st.info("🎤 Listening... Speak now!")
            
            # Listen for audio input
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        
        st.info("⚙️ Processing your speech...")
        
        # Try to recognize speech in multiple languages
        recognized_text = None
        detected_lang = None
        
        # Try all supported languages
        for lang_code, lang_info in SUPPORTED_LANGUAGES.items():
            try:
                text = recognizer.recognize_google(audio, language=lang_info['sr_code'])
                if text:
                    recognized_text = text
                    detected_lang = lang_code
                    break
            except:
                continue
        
        if recognized_text:
            return True, recognized_text, detected_lang
        else:
            return False, "Could not understand audio. Please try again.", None
            
    except sr.WaitTimeoutError:
        return False, "No speech detected. Please try again.", None
    except sr.UnknownValueError:
        return False, "Could not understand audio. Please speak clearly.", None
    except sr.RequestError as e:
        return False, f"Could not request results; {e}", None
    except Exception as e:
        return False, f"Error: {str(e)}", None

# ---------------------- CSS (Same as before, with additions) ----------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {display: none;}
    
    .main {
        background: #1a1a1a;
        padding: 0;
    }
    
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1400px !important;
        margin: 0 auto;
    }
    
    .language-selector {
        background: linear-gradient(135deg, #2d2d2d 0%, #1f1f1f 100%);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        border: 1px solid #4caf50;
    }
    
    .voice-input-container {
        background: linear-gradient(135deg, #2d2d2d 0%, #1f1f1f 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        border: 2px solid #4caf50;
        text-align: center;
    }
    
    .recording-indicator {
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .stChatMessage {
        background: linear-gradient(135deg, #2d2d2d 0%, #242424 100%) !important;
        border-radius: 12px !important;
        border: 1px solid #4caf50 !important;
        margin-bottom: 1rem !important;
        padding: 1.25rem !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stChatMessage p, .stChatMessage div {
        color: #e0e0e0 !important;
    }
    
    .stChatMessage strong {
        color: #66bb6a !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.75rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.25);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.35);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1f1f1f 0%, #2d2d2d 100%) !important;
        border-right: 2px solid #4caf50 !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #66bb6a !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------- INITIALIZE SESSION ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_location" not in st.session_state:
    st.session_state.user_location = None
if "expect_image" not in st.session_state:
    st.session_state.expect_image = False
if "selected_language" not in st.session_state:
    st.session_state.selected_language = 'en'
if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""
if "detected_voice_lang" not in st.session_state:
    st.session_state.detected_voice_lang = None

# Get current language
current_lang = st.session_state.selected_language

# ---------------------- HEADER ----------------------
header_col1, header_col2 = st.columns([1, 5])

with header_col1:
    st.markdown('<div style="font-size: 4rem; text-align: center;">🌾</div>', unsafe_allow_html=True)

with header_col2:
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; justify-content: center; height: 100%;">
        <h1 class="app-title">{get_ui_text('app_title', current_lang)}</h1>
        <p class="app-tagline">{get_ui_text('app_tagline', current_lang)}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr>', unsafe_allow_html=True)

# ---------------------- LANGUAGE SELECTOR ----------------------
st.markdown('<div class="language-selector">', unsafe_allow_html=True)
col_lang1, col_lang2 = st.columns([3, 1])

with col_lang1:
    st.markdown(f"**🌍 {get_ui_text('select_language', current_lang)}**")

with col_lang2:
    selected_lang = st.selectbox(
        "Language",
        options=list(SUPPORTED_LANGUAGES.keys()),
        format_func=lambda x: f"{SUPPORTED_LANGUAGES[x]['flag']} {SUPPORTED_LANGUAGES[x]['name']}",
        index=list(SUPPORTED_LANGUAGES.keys()).index(st.session_state.selected_language),
        label_visibility="collapsed"
    )
    
    if selected_lang != st.session_state.selected_language:
        st.session_state.selected_language = selected_lang
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- VOICE INPUT SECTION ----------------------
if SPEECH_RECOGNITION_AVAILABLE:
    st.markdown('<div class="voice-input-container">', unsafe_allow_html=True)
    st.markdown(f"### {get_ui_text('voice_input', current_lang)}")
    st.markdown(f"*{get_ui_text('speak_now', current_lang)}*")
    
    col_v1, col_v2, col_v3 = st.columns([1, 2, 1])
    
    with col_v2:
        if st.button(f"🎤 {get_ui_text('start_recording', current_lang)}", use_container_width=True):
            with st.spinner(get_ui_text('listening', current_lang)):
                # Use current selected language as hint
                lang_code = SUPPORTED_LANGUAGES[current_lang]['sr_code']
                success, message, detected_lang = recognize_speech_from_mic(lang_code)
                
                if success:
                    st.success(f"{get_ui_text('voice_detected', current_lang)} {message}")
                    st.session_state.voice_text = message
                    st.session_state.detected_voice_lang = detected_lang if detected_lang else current_lang
                    
                    # Auto-submit the voice input
                    st.session_state.messages.append({"role": "user", "content": message})
                    
                    # Get bot response in detected language
                    response_lang = st.session_state.detected_voice_lang
                    # Import necessary functions (they're defined below in your original code)
                    response = get_bot_response(message, response_lang)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    st.rerun()
                else:
                    st.error(message)
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("🎤 Voice input unavailable. Install: `pip install SpeechRecognition pyaudio`")

# ---------------------- HELPER FUNCTIONS (Keep all your existing functions) ----------------------
# [Include all your existing functions like get_weather, get_produce_prices, etc.]
# I'll include the key ones for the voice functionality to work:

def get_bot_response(user_message, user_lang='en'):
    """Generates intelligent responses with multilingual understanding"""
    
    # Translate user message to English for processing
    message_en = user_message
    if TRANSLATION_AVAILABLE and user_lang != 'en':
        try:
            translator = GoogleTranslator(source='auto', target='en')
            message_en = translator.translate(user_message)
        except:
            pass
    
    # Simple intent detection
    message_lower = message_en.lower()
    
    if any(word in message_lower for word in ['price', 'cost', 'market', 'mandi']):
        response_en = """💰 **Market Prices Available!**

🏆 **Cities Covered:** Delhi, Mumbai, Pune, and more!

💬 **Ask me:** 
• "Tomato price in Mumbai"
• "Show onion prices in Delhi"

📍 Type your city and vegetable name!"""
    
    elif any(word in message_lower for word in ['weather', 'temperature', 'rain', 'climate']):
        response_en = """🌤️ **Weather Information**

📍 I can check weather for any city!

**Ask me:**
• "Weather in Delhi"
• "Mumbai temperature"
• "Rainfall forecast"

What city would you like to know about?"""
    
    elif any(word in message_lower for word in ['disease', 'sick', 'infected', 'problem']):
        st.session_state.expect_image = True
        response_en = """🔬 **Crop Disease Detection**

📷 Please upload a clear photo of affected leaves or crops.

I'll analyze it and provide:
✅ Disease identification
✅ Treatment recommendations
✅ Prevention tips"""
    
    elif any(word in message_lower for word in ['wheat', 'rice', 'crop', 'farming', 'cultivation']):
        response_en = """🌾 **Crop Cultivation Tips**

I can help you with detailed cultivation guides for:

**Major Crops:**
• 🌾 Wheat - Rabi crop
• 🌾 Rice - Kharif crop
• 🍅 Tomato - Vegetable crop
• 🥔 Potato - Tuber crop

**What I can tell you:**
• Climate and soil requirements
• Planting time and methods
• Fertilizer recommendations
• Pest and disease management

Type your crop name to get started! 🚜"""
    
    else:
        response_en = f"""🌾 **Namaste! Welcome to Krishisaathi AI!**

I can help you with:
🌤️ Weather forecasts
💰 Market prices
🌾 Crop cultivation tips
🔬 Disease detection (upload photo)

**What would you like to know?** 🚜"""
    
    # Translate response back to user's language
    if user_lang != 'en' and TRANSLATION_AVAILABLE:
        return translate_text(response_en, target_lang=user_lang)
    
    return response_en

# ---------------------- SIDEBAR ----------------------
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 1.5rem 0 1.5rem 0; border-bottom: 1px solid rgba(76, 175, 80, 0.2);">
        <h2 style="font-size: 1.3rem; font-weight: 800; color: #66bb6a; margin: 0;">🌾 {get_ui_text('app_title', current_lang)}</h2>
        <p style="font-size: 0.8rem; color: #81c784; margin: 0.4rem 0 0 0;">{get_ui_text('smart_assistant', current_lang)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"### {get_ui_text('quick_actions', current_lang)}")
    
    if st.button(get_ui_text('disease_detection', current_lang)):
        user_msg = get_ui_text('check_disease', current_lang)
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg, st.session_state.selected_language)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
    
    if st.button(get_ui_text('delhi_prices', current_lang)):
        user_msg = f"{get_ui_text('show_prices', current_lang)} Delhi"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg, st.session_state.selected_language)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
        
    if st.button(get_ui_text('mumbai_weather', current_lang)):
        user_msg = f"{get_ui_text('weather_in', current_lang)} Mumbai"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg, st.session_state.selected_language)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
        
    if st.button(get_ui_text('crop_tips', current_lang)):
        user_msg = get_ui_text('tell_about', current_lang)
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg, st.session_state.selected_language)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
    
    st.divider()
    
    if st.button(get_ui_text('clear_chat', current_lang)):
        st.session_state.messages = []
        st.session_state.expect_image = False
        st.session_state.voice_text = ""
        st.session_state.detected_voice_lang = None
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
        with st.spinner(get_ui_text('thinking', current_lang)):
            response = get_bot_response(prompt, st.session_state.selected_language)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# ---------------------- FOOTER ----------------------
st.markdown(f"""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 12px; margin-top: 3rem; border: 1px solid #4caf50;">
    <p style="color: #66bb6a; font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem;">{get_ui_text('footer_title', current_lang)}</p>
    <p style="color: #81c784; font-size: 0.9rem; margin-bottom: 0;">{get_ui_text('footer_tagline', current_lang)}</p>
    <p style="color: #a5d6a7; font-size: 0.8rem; margin-top: 1rem;">{get_ui_text('footer_copyright', current_lang)}</p>
</div>
""", unsafe_allow_html=True)
