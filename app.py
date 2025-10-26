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
# Using deep-translator (more stable than googletrans)
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
    'mr': {'name': 'मराठी', 'flag': '🇮🇳'},
    'ta': {'name': 'தமிழ்', 'flag': '🇮🇳'},
    'te': {'name': 'తెలుగు', 'flag': '🇮🇳'},
    'bn': {'name': 'বাংলা', 'flag': '🇮🇳'},
    'gu': {'name': 'ગુજરાતી', 'flag': '🇮🇳'},
    'kn': {'name': 'ಕನ್ನಡ', 'flag': '🇮🇳'},
    'ml': {'name': 'മലയാളം', 'flag': '🇮🇳'},
    'pa': {'name': 'ਪੰਜਾਬੀ', 'flag': '🇮🇳'}
}

# ---------------------- TRANSLATION FUNCTIONS ----------------------
def translate_text(text, target_lang='en', source_lang='auto'):
    """Translate text to target language"""
    if not TRANSLATION_AVAILABLE or target_lang == 'en':
        return text
    
    try:
        translator = GoogleTranslator(source='auto', target=target_lang)
        return translator.translate(text)
    except Exception as e:
        return text  # Return original text if translation fails

def get_greeting_by_language(lang_code):
    """Return appropriate greeting based on language"""
    greetings = {
        'en': 'Namaste! Welcome to Krishisaathi AI!',
        'hi': 'नमस्ते! कृषिसाथी एआई में आपका स्वागत है!',
        'mr': 'नमस्कार! कृषिसाथी एआय मध्ये आपले स्वागत आहे!',
        'ta': 'வணக்கம்! கிருஷிசாத்தி AI-க்கு வரவேற்கிறோம்!',
        'te': 'నమస్కారం! కృషిసాతి AI కి స్వాగతం!',
        'bn': 'নমস্কার! কৃষিসাথী AI তে স্বাগতম!',
        'gu': 'નમસ્તે! કૃષિસાથી AI માં તમારું સ્વાગત છે!',
        'kn': 'ನಮಸ್ಕಾರ! ಕೃಷಿಸಾಥಿ AI ಗೆ ಸ್ವಾಗತ!',
        'ml': 'നമസ്കാരം! കൃഷിസാഥി AI യിലേക്ക് സ്വാഗതം!',
        'pa': 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਕ੍ਰਿਸ਼ੀਸਾਥੀ AI ਵਿੱਚ ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ!'
    }
    return greetings.get(lang_code, greetings['en'])

# ---------------------- CSS ----------------------
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
    
    .app-title {
        font-size: 2rem;
        font-weight: 800;
        color: #2e7d32;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .app-tagline {
        color: #81c784;
        font-size: 0.95rem;
        font-weight: 500;
        margin: 0.25rem 0 0 0;
    }
    
   /* Input fields dark theme */
    .stTextInput input, .stChatInput textarea {
        background: #2d2d2d !important;
        color: #e0e0e0 !important;
        border: 1px solid #4caf50 !important;
        border-radius: 10px !important;
    }
    
    .stTextInput input:focus, .stChatInput textarea:focus {
        border-color: #66bb6a !important;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2) !important;
    }
    
    /* Chat input container fix */
    .stChatInput {
        background: transparent !important;
    }
    
    .stChatInput > div {
        background: #2d2d2d !important;
        border: 2px solid #4caf50 !important;
        border-radius: 12px !important;
        padding: 0 !important;
    }
    
    .stChatInput textarea {
        padding: 1rem 1.5rem !important;
        min-height: 50px !important;
        font-size: 0.95rem !important;
    }
    
    .stChatInput button {
        background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%) !important;
        border: none !important;
        border-radius: 8px !important;
        margin: 4px !important;
        padding: 0.5rem 1rem !important;
    }
    
    .stChatInput button:hover {
        background: linear-gradient(135deg, #66bb6a 0%, #81c784 100%) !important;
        transform: scale(1.05);
    }
    
    /* File uploader dark theme */
    [data-testid="stFileUploader"] {
        background: #2d2d2d !important;
        border: 2px dashed #4caf50 !important;
        border-radius: 12px !important;
        padding: 2rem !important;
    }
    
    [data-testid="stFileUploader"] * {
        color: #e0e0e0 !important;
    }
    
    /* Metric cards dark theme */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #2d2d2d 0%, #242424 100%) !important;
        border: 1px solid #4caf50 !important;
        border-radius: 10px !important;
        padding: 1rem !important;
    }
    
    [data-testid="stMetric"] * {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #81c784 !important;
    }
    
    /* Select box dark theme */
    .stSelectbox select {
        background: #2d2d2d !important;
        color: #e0e0e0 !important;
        border: 1px solid #4caf50 !important;
    }
    
    /* Spinner dark theme */
    .stSpinner > div {
        border-top-color: #66bb6a !important;
    }
    
    /* Divider */
    hr {
        border-color: #4caf50 !important;
        opacity: 0.3;
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

# ---------------------- HEADER ----------------------
header_col1, header_col2 = st.columns([1, 5])

with header_col1:
    st.markdown('<div style="font-size: 4rem; text-align: center;">🌾</div>', unsafe_allow_html=True)

with header_col2:
    st.markdown("""
    <div style="display: flex; flex-direction: column; justify-content: center; height: 100%;">
        <h1 class="app-title">KRISHISAATHI AI</h1>
        <p class="app-tagline">Connecting Farmers, Empowering Growth</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr>', unsafe_allow_html=True)

# ---------------------- LANGUAGE SELECTOR ----------------------
st.markdown('<div class="language-selector">', unsafe_allow_html=True)
col_lang1, col_lang2 = st.columns([3, 1])

with col_lang1:
    st.markdown("**🌐 Select Your Language / अपनी भाषा चुनें**")

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

# ---------------------- WEATHER FUNCTION ----------------------
def get_weather(city):
    """Fetches real-time weather data"""
    API_KEY = "bc072ed23f5983aac7f32d666efe49af"
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    
    try:
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"]
            }
    except:
        pass
    return None

# ---------------------- DISEASE DETECTION ----------------------
def ai_predict_disease(image_file):
    """Placeholder for future ML model"""
    diseases = {
        "Tomato - Late Blight": {
            "symptoms": "Dark brown spots on leaves, white mold on undersides",
            "treatment": "Remove infected leaves, apply copper-based fungicide, improve air circulation",
            "prevention": "Avoid overhead watering, use resistant varieties"
        },
        "Potato - Early Blight": {
            "symptoms": "Circular brown spots with concentric rings on older leaves",
            "treatment": "Apply fungicide (Mancozeb), remove infected leaves",
            "prevention": "Crop rotation, proper spacing, mulching"
        },
        "Healthy Crop": {
            "symptoms": "No disease detected",
            "treatment": "Continue regular care and monitoring",
            "prevention": "Maintain good agricultural practices"
        }
    }
    
    disease_name = random.choice(list(diseases.keys()))
    disease_info = diseases[disease_name]
    
    return {
        "name": disease_name,
        "confidence": random.randint(75, 98),
        **disease_info
    }

# ---------------------- PRICE FUNCTION ----------------------
def get_produce_prices(state="all"):
    """Sample prices"""
    sample_prices = {
        # ========== NORTH INDIA ==========
        # Delhi NCR Updated Dataset (October 2025)

    "Delhi": {
        "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹14-24", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-10", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹18-25", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹35-55", "unit": "per kg", "trend": "↑"},
        "Brinjal (Eggplant)": {"price": "₹28-45", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹32-48", "unit": "per kg", "trend": "↑"},
        "Spinach": {"price": "₹20-35", "unit": "per bunch", "trend": "↑"},
        "Green Peas": {"price": "₹70-100", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹50-75", "unit": "per kg", "trend": "→"},
        "Cucumber": {"price": "₹25-40", "unit": "per kg", "trend": "↓"},
        "Pumpkin": {"price": "₹18-30", "unit": "per kg", "trend": "→"},
        "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹45-60", "unit": "per dozen", "trend": "→"},
        "Pomegranate": {"price": "₹120-160", "unit": "per kg", "trend": "↑"}
    },

    "Noida": {
        "Tomato": {"price": "₹23-37", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹15-25", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹16-24", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-11", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹18-26", "unit": "per kg", "trend": "→"},
        "Brinjal (Eggplant)": {"price": "₹30-44", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹34-50", "unit": "per kg", "trend": "↑"},
        "Carrot": {"price": "₹30-45", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹52-78", "unit": "per kg", "trend": "→"},
        "Cucumber": {"price": "₹26-40", "unit": "per kg", "trend": "↓"},
        "Green Peas": {"price": "₹72-98", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹48-62", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹90-125", "unit": "per kg", "trend": "→"}
    },

    "Gurgaon": {
        "Tomato": {"price": "₹24-38", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹16-26", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹16-24", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹19-26", "unit": "per kg", "trend": "→"},
        "Capsicum": {"price": "₹55-80", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹36-52", "unit": "per kg", "trend": "↑"},
        "Spinach": {"price": "₹22-36", "unit": "per bunch", "trend": "↑"},
        "Bottle Gourd (Lauki)": {"price": "₹25-38", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹30-44", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹46-60", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"}
    },

    "Faridabad": {
        "Tomato": {"price": "₹23-37", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹15-25", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹16-24", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-11", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹18-25", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹34-52", "unit": "per kg", "trend": "↑"},
        "Brinjal (Eggplant)": {"price": "₹29-43", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹31-46", "unit": "per kg", "trend": "↑"},
        "Bottle Gourd (Lauki)": {"price": "₹22-35", "unit": "per kg", "trend": "→"},
        "Capsicum": {"price": "₹52-74", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹45-58", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹88-122", "unit": "per kg", "trend": "→"}
    },

    "Ghaziabad": {
        "Tomato": {"price": "₹23-37", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹15-25", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹16-24", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-11", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹18-25", "unit": "per kg", "trend": "→"},
        "Brinjal (Eggplant)": {"price": "₹29-42", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹34-50", "unit": "per kg", "trend": "↑"},
        "Spinach": {"price": "₹20-34", "unit": "per bunch", "trend": "↑"},
        "Capsicum": {"price": "₹50-72", "unit": "per kg", "trend": "→"},
        "Green Peas": {"price": "₹70-95", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹46-60", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹85-118", "unit": "per kg", "trend": "→"}
    },

        # Punjab Updated Dataset (October 2025)

    "Chandigarh": {
        "Tomato": {"price": "₹20-34", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹14-24", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-11", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹18-26", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹32-50", "unit": "per kg", "trend": "↑"},
        "Brinjal (Eggplant)": {"price": "₹26-40", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹30-45", "unit": "per kg", "trend": "↑"},
        "Spinach": {"price": "₹18-30", "unit": "per bunch", "trend": "↑"},
        "Green Peas": {"price": "₹68-95", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹48-72", "unit": "per kg", "trend": "→"},
        "Cucumber": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
        "Bottle Gourd (Lauki)": {"price": "₹20-32", "unit": "per kg", "trend": "→"},
        "Pumpkin": {"price": "₹16-28", "unit": "per kg", "trend": "→"},
        "Apple": {"price": "₹80-115", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹42-58", "unit": "per dozen", "trend": "→"},
        "Pomegranate": {"price": "₹110-150", "unit": "per kg", "trend": "↑"}
    },

    "Ludhiana": {
        "Tomato": {"price": "₹18-32", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹12-22", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹13-21", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹7-10", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹16-24", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹30-48", "unit": "per kg", "trend": "↑"},
        "Brinjal (Eggplant)": {"price": "₹25-38", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹28-42", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹46-70", "unit": "per kg", "trend": "→"},
        "Spinach": {"price": "₹18-28", "unit": "per bunch", "trend": "↑"},
        "Cucumber": {"price": "₹22-34", "unit": "per kg", "trend": "↓"},
        "Green Peas": {"price": "₹65-92", "unit": "per kg", "trend": "↑"},
        "Bottle Gourd (Lauki)": {"price": "₹18-30", "unit": "per kg", "trend": "→"},
        "Pumpkin": {"price": "₹16-27", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹40-55", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹82-118", "unit": "per kg", "trend": "→"}
    },

    "Amritsar": {
        "Tomato": {"price": "₹19-33", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹13-23", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-10", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹17-25", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹32-50", "unit": "per kg", "trend": "↑"},
        "Brinjal (Eggplant)": {"price": "₹26-39", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹30-44", "unit": "per kg", "trend": "↑"},
        "Spinach": {"price": "₹20-32", "unit": "per bunch", "trend": "↑"},
        "Capsicum": {"price": "₹48-70", "unit": "per kg", "trend": "→"},
        "Cucumber": {"price": "₹23-36", "unit": "per kg", "trend": "↓"},
        "Bottle Gourd (Lauki)": {"price": "₹20-32", "unit": "per kg", "trend": "→"},
        "Pumpkin": {"price": "₹17-28", "unit": "per kg", "trend": "→"},
        "Green Peas": {"price": "₹68-96", "unit": "per kg", "trend": "↑"},
        "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹42-58", "unit": "per dozen", "trend": "→"}
    },

    "Jalandhar": {
        "Tomato": {"price": "₹19-33", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹13-23", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-10", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹17-25", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹31-48", "unit": "per kg", "trend": "↑"},
        "Brinjal (Eggplant)": {"price": "₹26-38", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹29-43", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹48-72", "unit": "per kg", "trend": "→"},
        "Spinach": {"price": "₹19-30", "unit": "per bunch", "trend": "↑"},
        "Cucumber": {"price": "₹22-35", "unit": "per kg", "trend": "↓"},
        "Green Peas": {"price": "₹66-94", "unit": "per kg", "trend": "↑"},
        "Bottle Gourd (Lauki)": {"price": "₹19-31", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹41-57", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹84-118", "unit": "per kg", "trend": "→"}
    },

    "Patiala": {
        "Tomato": {"price": "₹19-33", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹13-23", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-10", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹17-25", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹31-48", "unit": "per kg", "trend": "↑"},
        "Brinjal (Eggplant)": {"price": "₹25-38", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹29-43", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹47-70", "unit": "per kg", "trend": "→"},
        "Cucumber": {"price": "₹22-35", "unit": "per kg", "trend": "↓"},
        "Spinach": {"price": "₹19-30", "unit": "per bunch", "trend": "↑"},
        "Bottle Gourd (Lauki)": {"price": "₹19-31", "unit": "per kg", "trend": "→"},
        "Pumpkin": {"price": "₹17-28", "unit": "per kg", "trend": "→"},
        "Green Peas": {"price": "₹68-95", "unit": "per kg", "trend": "↑"},
        "Apple": {"price": "₹84-118", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹42-58", "unit": "per dozen", "trend": "→"}
    }
,

        
        # Haryana (October 2025)

    "Gurugram": {
        "Tomato": {"price": "₹24-38", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹16-26", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹16-24", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹18-27", "unit": "per kg", "trend": "→"},
        "Brinjal (Eggplant)": {"price": "₹26-39", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹32-48", "unit": "per kg", "trend": "↑"},
        "Carrot": {"price": "₹30-44", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹48-70", "unit": "per kg", "trend": "→"},
        "Cucumber": {"price": "₹22-34", "unit": "per kg", "trend": "↓"},
        "Banana": {"price": "₹44-60", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"}
    },
    "Faridabad": {
        "Tomato": {"price": "₹23-37", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹15-25", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹16-24", "unit": "per kg", "trend": "↓"},
        "Carrot": {"price": "₹30-42", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹42-58", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹84-118", "unit": "per kg", "trend": "→"}
    },
    "Panipat": {
        "Tomato": {"price": "₹22-35", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹14-24", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-11", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹18-26", "unit": "per kg", "trend": "→"},
        "Apple": {"price": "₹80-115", "unit": "per kg", "trend": "→"}
    }
,
        
        # Rajasthan (October 2025)

    "Jaipur": {
        "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹14-23", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹18-27", "unit": "per kg", "trend": "→"},
        "Brinjal (Eggplant)": {"price": "₹26-40", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹32-46", "unit": "per kg", "trend": "↑"},
        "Carrot": {"price": "₹28-42", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹48-70", "unit": "per kg", "trend": "→"},
        "Cucumber": {"price": "₹22-33", "unit": "per kg", "trend": "↓"},
        "Banana": {"price": "₹42-58", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹86-120", "unit": "per kg", "trend": "→"}
    },
    "Jodhpur": {
        "Tomato": {"price": "₹23-37", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹15-25", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹16-24", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-11", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹18-25", "unit": "per kg", "trend": "→"},
        "Apple": {"price": "₹82-118", "unit": "per kg", "trend": "→"},
        "Pomegranate": {"price": "₹110-150", "unit": "per kg", "trend": "↑"}
    },
    "Udaipur": {
        "Tomato": {"price": "₹21-35", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹14-23", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-22", "unit": "per kg", "trend": "↓"},
        "Carrot": {"price": "₹28-40", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹40-55", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹84-118", "unit": "per kg", "trend": "→"}
    }
,
        
        # Uttar Pradesh (October 2025)

    "Lucknow": {
        "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹14-24", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-10", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹18-25", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹34-52", "unit": "per kg", "trend": "↑"},
        "Carrot": {"price": "₹30-46", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹50-72", "unit": "per kg", "trend": "→"},
        "Spinach": {"price": "₹20-32", "unit": "per bunch", "trend": "↑"},
        "Banana": {"price": "₹44-58", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹82-118", "unit": "per kg", "trend": "→"}
    },
    "Kanpur": {
        "Tomato": {"price": "₹21-35", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹13-23", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-10", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹18-25", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹29-43", "unit": "per kg", "trend": "↑"},
        "Brinjal (Eggplant)": {"price": "₹26-40", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹42-56", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹84-118", "unit": "per kg", "trend": "→"}
    },
    "Varanasi": {
        "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹14-24", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-11", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹30-44", "unit": "per kg", "trend": "↑"},
        "Spinach": {"price": "₹20-33", "unit": "per bunch", "trend": "↑"},
        "Capsicum": {"price": "₹52-74", "unit": "per kg", "trend": "→"},
        "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"}
    }
,
        
        # Uttarakhand (October 2025)

    "Dehradun": {
        "Tomato": {"price": "₹24-40", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹15-25", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-24", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹19-28", "unit": "per kg", "trend": "→"},
        "Brinjal (Eggplant)": {"price": "₹28-42", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹34-50", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹50-72", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹32-46", "unit": "per kg", "trend": "↑"},
        "Cucumber": {"price": "₹22-34", "unit": "per kg", "trend": "↓"},
        "Banana": {"price": "₹44-60", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹90-130", "unit": "per kg", "trend": "↑"},
        "Peas (Green)": {"price": "₹60-80", "unit": "per kg", "trend": "↑"}
    },
    "Haridwar": {
        "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹14-23", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-11", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹42-56", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹88-122", "unit": "per kg", "trend": "↑"}
    }
,
        
        # Himachal Pradesh (October 2025)

    "Shimla": {
        "Tomato": {"price": "₹25-40", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹15-25", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-13", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹19-28", "unit": "per kg", "trend": "→"},
        "Brinjal (Eggplant)": {"price": "₹26-38", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹30-45", "unit": "per kg", "trend": "↑"},
        "Carrot": {"price": "₹30-44", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹48-70", "unit": "per kg", "trend": "→"},
        "Cucumber": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
        "Banana": {"price": "₹42-58", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹100-140", "unit": "per kg", "trend": "↑"},
        "Peas (Green)": {"price": "₹70-95", "unit": "per kg", "trend": "↑"}
    },
    "Manali": {
        "Tomato": {"price": "₹26-42", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹16-26", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-24", "unit": "per kg", "trend": "↓"},
        "Carrot": {"price": "₹32-46", "unit": "per kg", "trend": "↑"},
        "Apple": {"price": "₹110-150", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹44-60", "unit": "per dozen", "trend": "→"}
    }

,
        
        # ========== WEST INDIA ==========
        # Maharashtra Updated Dataset (October 2025)

    "Mumbai": {
        "Tomato": {"price": "₹26-40", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹18-28", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹17-26", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹20-28", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹35-55", "unit": "per kg", "trend": "↑"},
        "Brinjal (Eggplant)": {"price": "₹28-42", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹34-50", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹52-78", "unit": "per kg", "trend": "→"},
        "Spinach": {"price": "₹22-34", "unit": "per bunch", "trend": "↑"},
        "Cucumber": {"price": "₹24-38", "unit": "per kg", "trend": "↓"},
        "Bottle Gourd (Lauki)": {"price": "₹22-35", "unit": "per kg", "trend": "→"},
        "Pumpkin": {"price": "₹18-30", "unit": "per kg", "trend": "→"},
        "Green Peas": {"price": "₹70-95", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹48-65", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹90-130", "unit": "per kg", "trend": "→"},
        "Pomegranate": {"price": "₹120-165", "unit": "per kg", "trend": "↑"},
        "Mango (Alphonso)": {"price": "₹150-200", "unit": "per kg", "trend": "↑"}
    },

    "Pune": {
        "Tomato": {"price": "₹25-38", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹17-27", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹16-25", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-11", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹18-27", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹34-52", "unit": "per kg", "trend": "↑"},
        "Brinjal (Eggplant)": {"price": "₹27-41", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹32-48", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹50-76", "unit": "per kg", "trend": "→"},
        "Spinach": {"price": "₹20-32", "unit": "per bunch", "trend": "↑"},
        "Cucumber": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
        "Green Peas": {"price": "₹68-94", "unit": "per kg", "trend": "↑"},
        "Bottle Gourd (Lauki)": {"price": "₹21-33", "unit": "per kg", "trend": "→"},
        "Pumpkin": {"price": "₹18-28", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹46-62", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹88-125", "unit": "per kg", "trend": "→"},
        "Pomegranate": {"price": "₹118-160", "unit": "per kg", "trend": "↑"}
    },

    "Nagpur": {
        "Tomato": {"price": "₹23-36", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹16-26", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-24", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-11", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹17-26", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹33-50", "unit": "per kg", "trend": "↑"},
        "Brinjal (Eggplant)": {"price": "₹26-40", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹30-46", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹48-70", "unit": "per kg", "trend": "→"},
        "Cucumber": {"price": "₹22-35", "unit": "per kg", "trend": "↓"},
        "Spinach": {"price": "₹18-30", "unit": "per bunch", "trend": "↑"},
        "Bottle Gourd (Lauki)": {"price": "₹20-32", "unit": "per kg", "trend": "→"},
        "Pumpkin": {"price": "₹17-27", "unit": "per kg", "trend": "→"},
        "Green Peas": {"price": "₹68-92", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹45-60", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"},
        "Pomegranate": {"price": "₹115-155", "unit": "per kg", "trend": "↑"}
    },

    "Nashik": {
        "Tomato": {"price": "₹22-35", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹15-25", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-10", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹17-25", "unit": "per kg", "trend": "→"},
        "Brinjal (Eggplant)": {"price": "₹25-39", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹32-50", "unit": "per kg", "trend": "↑"},
        "Carrot": {"price": "₹30-45", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹48-72", "unit": "per kg", "trend": "→"},
        "Cucumber": {"price": "₹21-33", "unit": "per kg", "trend": "↓"},
        "Spinach": {"price": "₹18-30", "unit": "per bunch", "trend": "↑"},
        "Green Peas": {"price": "₹68-90", "unit": "per kg", "trend": "↑"},
        "Bottle Gourd (Lauki)": {"price": "₹19-31", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹44-58", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹84-118", "unit": "per kg", "trend": "→"},
        "Pomegranate": {"price": "₹110-150", "unit": "per kg", "trend": "↑"}
    },

    "Aurangabad": {
        "Tomato": {"price": "₹23-36", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹16-26", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-10", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹17-25", "unit": "per kg", "trend": "→"},
        "Brinjal (Eggplant)": {"price": "₹26-40", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹33-50", "unit": "per kg", "trend": "↑"},
        "Carrot": {"price": "₹30-45", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹48-70", "unit": "per kg", "trend": "→"},
        "Cucumber": {"price": "₹22-35", "unit": "per kg", "trend": "↓"},
        "Spinach": {"price": "₹18-30", "unit": "per bunch", "trend": "↑"},
        "Bottle Gourd (Lauki)": {"price": "₹20-32", "unit": "per kg", "trend": "→"},
        "Pumpkin": {"price": "₹17-28", "unit": "per kg", "trend": "→"},
        "Green Peas": {"price": "₹68-92", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹45-60", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"},
        "Pomegranate": {"price": "₹115-155", "unit": "per kg", "trend": "↑"}
    }
,

        
       # Gujarat (October 2025)

    "Ahmedabad": {
        "Tomato": {"price": "₹24-38", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹16-26", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹16-24", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹20-28", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹32-46", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹50-74", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹35-52", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹44-60", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹86-122", "unit": "per kg", "trend": "→"}
    },
    "Surat": {
        "Tomato": {"price": "₹23-36", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹15-25", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹16-24", "unit": "per kg", "trend": "↓"},
        "Brinjal (Eggplant)": {"price": "₹28-42", "unit": "per kg", "trend": "→"},
        "Cucumber": {"price": "₹25-40", "unit": "per kg", "trend": "↓"},
        "Green Peas": {"price": "₹70-95", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹46-60", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹84-118", "unit": "per kg", "trend": "→"}
    }
,
        
        # ========== SOUTH INDIA ==========
        # Karnataka (October 2025)

    "Bengaluru": {
        "Tomato": {"price": "₹24-36", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹16-25", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-22", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹20-28", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹28-44", "unit": "per kg", "trend": "↑"},
        "Spinach": {"price": "₹20-34", "unit": "per bunch", "trend": "↑"},
        "Capsicum": {"price": "₹50-76", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹40-54", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"}
    },
    "Mysuru": {
        "Tomato": {"price": "₹23-35", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹15-24", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-11", "unit": "per kg", "trend": "→"},
        "Brinjal (Eggplant)": {"price": "₹27-40", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹33-48", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹42-56", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹84-118", "unit": "per kg", "trend": "→"}
    }
,
        
       # Tamil Nadu (October 2025)

    "Chennai": {
        "Tomato": {"price": "₹24-38", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹15-25", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹16-23", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹19-28", "unit": "per kg", "trend": "→"},
        "Brinjal (Eggplant)": {"price": "₹28-40", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹34-50", "unit": "per kg", "trend": "↑"},
        "Carrot": {"price": "₹30-44", "unit": "per kg", "trend": "↑"},
        "Spinach": {"price": "₹22-34", "unit": "per bunch", "trend": "↑"},
        "Capsicum": {"price": "₹50-74", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹38-52", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"}
    },
    "Coimbatore": {
        "Tomato": {"price": "₹23-36", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹15-24", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-11", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹18-26", "unit": "per kg", "trend": "→"},
        "Brinjal (Eggplant)": {"price": "₹27-39", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹28-42", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹48-70", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹40-54", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹82-118", "unit": "per kg", "trend": "→"}
    }
,
        
        # Telangana (October 2025)

    "Hyderabad": {
        "Tomato": {"price": "₹22-38", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹16-25", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹19-28", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹34-52", "unit": "per kg", "trend": "↑"},
        "Brinjal (Eggplant)": {"price": "₹26-40", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹30-46", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹52-76", "unit": "per kg", "trend": "→"},
        "Green Peas": {"price": "₹68-92", "unit": "per kg", "trend": "↑"},
        "Cucumber": {"price": "₹24-38", "unit": "per kg", "trend": "↓"},
        "Spinach": {"price": "₹22-34", "unit": "per bunch", "trend": "↑"},
        "Banana": {"price": "₹42-56", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹84-118", "unit": "per kg", "trend": "→"},
        "Pomegranate": {"price": "₹110-150", "unit": "per kg", "trend": "↑"}
    },
    "Warangal": {
        "Tomato": {"price": "₹21-35", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹15-24", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-11", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹32-50", "unit": "per kg", "trend": "↑"},
        "Brinjal (Eggplant)": {"price": "₹25-38", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹28-44", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹40-54", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹82-116", "unit": "per kg", "trend": "→"}
    }
,
# Telangana (October 2025)

    "Hyderabad": {
        "Tomato": {"price": "₹22-38", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹16-25", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹19-28", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹34-52", "unit": "per kg", "trend": "↑"},
        "Brinjal (Eggplant)": {"price": "₹26-40", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹30-46", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹52-76", "unit": "per kg", "trend": "→"},
        "Green Peas": {"price": "₹68-92", "unit": "per kg", "trend": "↑"},
        "Cucumber": {"price": "₹24-38", "unit": "per kg", "trend": "↓"},
        "Spinach": {"price": "₹22-34", "unit": "per bunch", "trend": "↑"},
        "Banana": {"price": "₹42-56", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹84-118", "unit": "per kg", "trend": "→"},
        "Pomegranate": {"price": "₹110-150", "unit": "per kg", "trend": "↑"}
    },
    "Warangal": {
        "Tomato": {"price": "₹21-35", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹15-24", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-11", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹32-50", "unit": "per kg", "trend": "↑"},
        "Brinjal (Eggplant)": {"price": "₹25-38", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹28-44", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹40-54", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹82-116", "unit": "per kg", "trend": "→"}
    }
,
       # Kerala (October 2025)

    "Kochi": {
        "Tomato": {"price": "₹25-40", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹17-26", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹16-25", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹10-14", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹22-32", "unit": "per kg", "trend": "→"},
        "Brinjal (Eggplant)": {"price": "₹28-42", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹36-52", "unit": "per kg", "trend": "↑"},
        "Carrot": {"price": "₹34-50", "unit": "per kg", "trend": "↑"},
        "Spinach": {"price": "₹24-36", "unit": "per bunch", "trend": "↑"},
        "Banana": {"price": "₹46-60", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹88-124", "unit": "per kg", "trend": "→"},
        "Pineapple": {"price": "₹38-54", "unit": "per piece", "trend": "→"}
    },
    "Thiruvananthapuram": {
        "Tomato": {"price": "₹24-38", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹16-25", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹16-24", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹10-13", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹32-48", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹44-58", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹86-122", "unit": "per kg", "trend": "→"}
    }
,
        
        # ========== EAST INDIA ==========
        # West Bengal (October 2025)

    "Kolkata": {
        "Tomato": {"price": "₹20-34", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹13-22", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-11", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹18-25", "unit": "per kg", "trend": "→"},
        "Brinjal (Eggplant)": {"price": "₹26-38", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹30-46", "unit": "per kg", "trend": "↑"},
        "Carrot": {"price": "₹28-42", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹48-70", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹42-56", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹84-118", "unit": "per kg", "trend": "→"},
        "Pumpkin": {"price": "₹20-34", "unit": "per kg", "trend": "→"}
    },
    "Siliguri": {
        "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹14-24", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹30-46", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹40-54", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹82-120", "unit": "per kg", "trend": "→"}
    }
,
        
       # Bihar (October 2025)

    "Patna": {
        "Tomato": {"price": "₹21-34", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹13-23", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-11", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹18-26", "unit": "per kg", "trend": "→"},
        "Brinjal (Eggplant)": {"price": "₹26-38", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹32-48", "unit": "per kg", "trend": "↑"},
        "Carrot": {"price": "₹28-42", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹48-70", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹42-56", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹82-118", "unit": "per kg", "trend": "→"}
    },
    "Gaya": {
        "Tomato": {"price": "₹22-35", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹14-24", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹29-44", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹40-54", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹84-120", "unit": "per kg", "trend": "→"}
    }
,
        
        # Jharkhand
        
    "Ranchi": {
        "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹14-24", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-11", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹18-26", "unit": "per kg", "trend": "→"},
        "Brinjal (Eggplant)": {"price": "₹26-38", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹30-46", "unit": "per kg", "trend": "↑"},
        "Carrot": {"price": "₹28-42", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹46-68", "unit": "per kg", "trend": "→"},
        "Cucumber": {"price": "₹22-34", "unit": "per kg", "trend": "↓"},
        "Green Peas": {"price": "₹60-80", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹40-54", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹82-118", "unit": "per kg", "trend": "→"},
        "Mango": {"price": "₹90-130", "unit": "per kg", "trend": "↓"}
    },
    "Dhanbad": {
        "Tomato": {"price": "₹23-37", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹15-25", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-11", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹30-44", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹40-54", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹84-120", "unit": "per kg", "trend": "→"},
        "Pineapple": {"price": "₹40-56", "unit": "per piece", "trend": "→"}
    },
    "Jamshedpur": {
        "Tomato": {"price": "₹22-35", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹14-23", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Brinjal (Eggplant)": {"price": "₹25-38", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹32-48", "unit": "per kg", "trend": "↑"},
        "Apple": {"price": "₹85-122", "unit": "per kg", "trend": "→"}
    }
,
        
        # Odisha
        
    "Bhubaneswar": {
        "Tomato": {"price": "₹20-34", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹13-22", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-10", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹18-25", "unit": "per kg", "trend": "→"},
        "Brinjal (Eggplant)": {"price": "₹25-37", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹30-45", "unit": "per kg", "trend": "↑"},
        "Carrot": {"price": "₹28-40", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹46-68", "unit": "per kg", "trend": "→"},
        "Spinach": {"price": "₹20-32", "unit": "per bunch", "trend": "↑"},
        "Cucumber": {"price": "₹22-35", "unit": "per kg", "trend": "↓"},
        "Banana": {"price": "₹40-55", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹80-115", "unit": "per kg", "trend": "→"},
        "Mango": {"price": "₹85-120", "unit": "per kg", "trend": "↓"}
    },
    "Cuttack": {
        "Tomato": {"price": "₹21-35", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹14-23", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-10", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹29-42", "unit": "per kg", "trend": "↑"},
        "Brinjal (Eggplant)": {"price": "₹26-38", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹42-56", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹82-118", "unit": "per kg", "trend": "→"}
    },
    "Puri": {
        "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹14-23", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Carrot": {"price": "₹30-44", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹42-58", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹84-118", "unit": "per kg", "trend": "→"},
        "Papaya": {"price": "₹30-45", "unit": "per kg", "trend": "→"}
    }
,
        
        # Assam & Northeast

    "Guwahati": {
        "Tomato": {"price": "₹23-38", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹15-25", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹16-24", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹19-28", "unit": "per kg", "trend": "→"},
        "Brinjal (Eggplant)": {"price": "₹27-40", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹32-48", "unit": "per kg", "trend": "↑"},
        "Carrot": {"price": "₹30-44", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹50-72", "unit": "per kg", "trend": "→"},
        "Cucumber": {"price": "₹23-36", "unit": "per kg", "trend": "↓"},
        "Green Peas": {"price": "₹65-85", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹44-58", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹86-122", "unit": "per kg", "trend": "→"},
        "Pineapple": {"price": "₹38-52", "unit": "per piece", "trend": "→"}
    },
    "Dibrugarh": {
        "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹14-23", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Carrot": {"price": "₹30-45", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹42-56", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹84-120", "unit": "per kg", "trend": "→"},
        "Papaya": {"price": "₹28-42", "unit": "per kg", "trend": "→"}
    },
    "Silchar": {
        "Tomato": {"price": "₹24-38", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹16-25", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹16-24", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
        "Brinjal (Eggplant)": {"price": "₹28-40", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹45-60", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹88-125", "unit": "per kg", "trend": "→"}
    }
,
        
        # ========== CENTRAL INDIA ==========
        # Madhya Pradesh

    "Bhopal": {
        "Tomato": {"price": "₹20-34", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹13-22", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-10", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹18-26", "unit": "per kg", "trend": "→"},
        "Brinjal (Eggplant)": {"price": "₹26-38", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹30-46", "unit": "per kg", "trend": "↑"},
        "Carrot": {"price": "₹28-42", "unit": "per kg", "trend": "↑"},
        "Capsicum": {"price": "₹44-68", "unit": "per kg", "trend": "→"},
        "Spinach": {"price": "₹18-30", "unit": "per bunch", "trend": "↑"},
        "Banana": {"price": "₹38-54", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹80-115", "unit": "per kg", "trend": "→"},
        "Mango": {"price": "₹85-120", "unit": "per kg", "trend": "↓"}
    },
    "Indore": {
        "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹14-24", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-11", "unit": "per kg", "trend": "→"},
        "Carrot": {"price": "₹30-44", "unit": "per kg", "trend": "↑"},
        "Brinjal (Eggplant)": {"price": "₹26-40", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹40-56", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹84-120", "unit": "per kg", "trend": "→"},
        "Papaya": {"price": "₹30-45", "unit": "per kg", "trend": "→"}
    },
    "Gwalior": {
        "Tomato": {"price": "₹21-34", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹13-23", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
        "Cauliflower": {"price": "₹19-27", "unit": "per kg", "trend": "→"},
        "Capsicum": {"price": "₹46-70", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹40-54", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹82-116", "unit": "per kg", "trend": "→"}
    }
,
        
        # Chhattisgarh

    "Raipur": {
        "Tomato": {"price": "₹20-34", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹13-22", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-10", "unit": "per kg", "trend": "→"},
        "Cauliflower": {"price": "₹18-26", "unit": "per kg", "trend": "→"},
        "Brinjal (Eggplant)": {"price": "₹25-38", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹30-46", "unit": "per kg", "trend": "↑"},
        "Carrot": {"price": "₹28-42", "unit": "per kg", "trend": "↑"},
        "Cucumber": {"price": "₹22-34", "unit": "per kg", "trend": "↓"},
        "Banana": {"price": "₹38-52", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹80-114", "unit": "per kg", "trend": "→"}
    },
    "Bilaspur": {
        "Tomato": {"price": "₹21-35", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹14-23", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Carrot": {"price": "₹29-43", "unit": "per kg", "trend": "↑"},
        "Brinjal (Eggplant)": {"price": "₹25-39", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹40-55", "unit": "per dozen", "trend": "→"},
        "Papaya": {"price": "₹30-44", "unit": "per kg", "trend": "→"}
    },
    "Durg": {
        "Tomato": {"price": "₹20-34", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹13-22", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
        "Capsicum": {"price": "₹46-68", "unit": "per kg", "trend": "→"},
        "Cucumber": {"price": "₹22-34", "unit": "per kg", "trend": "↓"},
        "Apple": {"price": "₹82-116", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹40-54", "unit": "per dozen", "trend": "→"}
    }
,
        
        # ========== UNION TERRITORIES ==========
     "Chandigarh": {
        "Tomato": {"price": "₹20-34", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹14-24", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
        "Apple": {"price": "₹80-115", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹42-56", "unit": "per dozen", "trend": "→"},
        "Papaya": {"price": "₹30-46", "unit": "per kg", "trend": "→"}
    },
    "Puducherry": {
        "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹15-25", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹16-24", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
        "Lady Finger (Bhindi)": {"price": "₹32-46", "unit": "per kg", "trend": "↑"},
        "Banana": {"price": "₹40-54", "unit": "per dozen", "trend": "→"},
        "Mango": {"price": "₹85-118", "unit": "per kg", "trend": "↓"}
    },
    "Jammu & Kashmir": {
        "Tomato": {"price": "₹26-40", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹16-26", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹17-25", "unit": "per kg", "trend": "↓"},
        "Apple": {"price": "₹60-90", "unit": "per kg", "trend": "→"},
        "Apricot": {"price": "₹120-160", "unit": "per kg", "trend": "↑"},
        "Cherry": {"price": "₹180-250", "unit": "per kg", "trend": "↑"},
        "Walnut": {"price": "₹350-420", "unit": "per kg", "trend": "→"}
    },
    "Ladakh": {
        "Tomato": {"price": "₹32-50", "unit": "per kg", "trend": "→"},
        "Potato": {"price": "₹20-30", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹22-32", "unit": "per kg", "trend": "↓"},
        "Apple": {"price": "₹90-120", "unit": "per kg", "trend": "→"},
        "Apricot": {"price": "₹130-180", "unit": "per kg", "trend": "↑"}
    },
    "Lakshadweep": {
        "Coconut": {"price": "₹25-35", "unit": "per piece", "trend": "→"},
        "Banana": {"price": "₹45-60", "unit": "per dozen", "trend": "→"},
        "Papaya": {"price": "₹35-50", "unit": "per kg", "trend": "→"},
        "Breadfruit": {"price": "₹50-70", "unit": "per kg", "trend": "→"}
    },
    "Andaman & Nicobar Islands": {
        "Tomato": {"price": "₹26-42", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹18-28", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹20-30", "unit": "per kg", "trend": "↓"},
        "Coconut": {"price": "₹30-45", "unit": "per piece", "trend": "→"},
        "Banana": {"price": "₹50-65", "unit": "per dozen", "trend": "→"},
        "Pineapple": {"price": "₹40-55", "unit": "per piece", "trend": "→"}
    },
    "Dadra and Nagar Haveli & Daman and Diu": {
        "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
        "Potato": {"price": "₹14-24", "unit": "per kg", "trend": "→"},
        "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        "Cabbage": {"price": "₹8-11", "unit": "per kg", "trend": "→"},
        "Banana": {"price": "₹40-54", "unit": "per dozen", "trend": "→"},
        "Apple": {"price": "₹82-118", "unit": "per kg", "trend": "→"}
    }
}
    
    if state.lower() == "all":
        return sample_prices
    else:
        matched_cities = {}
        search_term = state.lower()
        
        for city, prices in sample_prices.items():
            if search_term in city.lower():
                matched_cities[city] = prices
        
        return matched_cities if matched_cities else None

# ---------------------- EXTRACT CITY ----------------------
def extract_city_and_vegetable_from_message(message):
    """Extracts both city name and vegetable name from user message"""
    message_lower = message.lower()
    
    city = None
    city_patterns = [
        r"(?:in|at|for)\s+([a-zA-Z\s]+?)(?:\s+price|\s+market|$)",
        r"([a-zA-Z]+)\s+(?:price|weather|market)",
    ]
    
    for pattern in city_patterns:
        match = re.search(pattern, message_lower)
        if match:
            potential_city = match.group(1).strip()
            potential_city = re.sub(r'\b(today|tomorrow|now|current|latest|price|prices|weather)\b', '', potential_city).strip()
            if potential_city and len(potential_city) > 2:
                city = potential_city
                break
    
    vegetable = None
    produce_list = ["tomato", "potato", "onion", "cabbage"]
    
    for produce in produce_list:
        if produce in message_lower:
            vegetable = produce
            break
    
    return city, vegetable

# ---------------------- FORMAT PRICE RESPONSE ----------------------
def format_price_response(prices, city_name=None, vegetable_name=None):
    """Formats price data into readable response"""
    if not prices:
        return "❌ Sorry, no price data found. Try: Delhi or Mumbai."
    
    response = "💰 **Current Market Prices:**\n\n"
    
    for city, produce_data in prices.items():
        if city_name and city_name.lower() not in city.lower():
            continue
        
        response += f"📍 **{city}**\n\n"
        
        if vegetable_name:
            found = False
            for item, data in produce_data.items():
                if vegetable_name.lower() in item.lower():
                    response += f"• **{item}**: {data['price']} {data['unit']} {data['trend']}\n"
                    found = True
            
            if not found:
                response += f"❌ {vegetable_name.title()} price not available for {city}\n"
        else:
            for item, data in produce_data.items():
                response += f"• **{item}**: {data['price']} {data['unit']} {data['trend']}\n"
        
        response += "\n"
    
    response += "\n📊 **Legend:** ↑ Rising | → Stable | ↓ Falling\n"
    
    return response

# ---------------------- CHATBOT RESPONSE LOGIC ----------------------
def get_bot_response(user_message, user_lang='en'):
    """Generates intelligent responses"""
    message_lower = user_message.lower()
    response_en = ""
    
    # Disease detection trigger
    if any(word in message_lower for word in ["disease", "sick", "infected", "diagnose"]):
        st.session_state.expect_image = True
        response_en = """🔬 **Crop Disease Detection**

📷 Please upload a clear photo of affected leaves or crops.

I'll analyze it and provide:
✅ Disease identification
✅ Treatment recommendations
✅ Prevention tips"""
    
    # Price queries
    elif any(word in message_lower for word in ["price", "cost", "market"]):
        city, vegetable = extract_city_and_vegetable_from_message(user_message)
        
        if city:
            prices = get_produce_prices(city)
            if prices:
                response_en = format_price_response(prices, city, vegetable)
            else:
                response_en = f"❌ Sorry, I don't have price data for '{city}'. Try: Delhi or Mumbai."
        else:
            response_en = """💰 **Market Prices Available!**

🌆 **Cities Covered:** Delhi, Mumbai, and more!

💬 **Ask me:** 
• "Tomato price in Mumbai"
• "Show onion prices in Delhi"

📝 Type your city and vegetable name!"""
    
    # Weather queries
    elif any(word in message_lower for word in ["weather", "temperature"]):
        city, _ = extract_city_and_vegetable_from_message(user_message)
        
        if not city:
            response_en = "📍 Please specify a location!\nExample: 'Weather in Delhi'"
        else:
            weather = get_weather(city)
            if weather:
                response_en = f"""🌤️ **Weather in {weather['city']}:**
            
- Temperature: {weather['temperature']}°C (feels like {weather['feels_like']}°C)
- Conditions: {weather['description'].title()}
- Humidity: {weather['humidity']}%
- Wind: {weather['wind_speed']} m/s

**Advice:** {"Good for outdoor work! 🌞" if weather['temperature'] > 15 else "Indoor tasks recommended. 🧥"}"""
            else:
                response_en = f"❌ Couldn't fetch weather for '{city}'."
    
    # Crop tips
    if any(word in message_lower for word in ["wheat", "rice", "tomato", "potato", "crop", "farming", "cultivation"]):
        if "wheat" in message_lower:
            return """🌾 **Wheat Cultivation Guide**

**Climate Requirements:**
• Temperature: 10-25°C (ideal)
• Rainfall: 50-75 cm annually
• Cool, moist climate preferred

**Soil:**
• Well-drained loamy or clay-loam soil
• pH: 6.0-7.0
• Deep soil with good water retention

**Planting:**
• Sowing time: October-November (Rabi season)
• Seed rate: 100-125 kg/hectare
• Row spacing: 20-22 cm

**Fertilizers:**
• Nitrogen: 120-150 kg/ha
• Phosphorus: 60 kg/ha
• Potassium: 40 kg/ha
• Apply farmyard manure before sowing

**Irrigation:**
• 4-6 irrigations needed
• Critical stages: Crown root, tillering, flowering, grain filling
• Avoid waterlogging

**Harvesting:**
• 120-150 days after sowing
• When grains are hard and golden
• Moisture content: 20-25%

**Common Issues:**
• Rust diseases: Use resistant varieties
• Aphids: Apply neem oil or insecticides
• Weeds: Manual weeding or herbicides

💡 **Pro Tips:**
✅ Use certified seeds
✅ Crop rotation with legumes
✅ Proper drainage to prevent diseases
✅ Store in dry, cool place"""
        
        elif "rice" in message_lower:
            return """🍚 **Rice Cultivation Guide**

**Climate:**
• Temperature: 20-35°C
• High humidity (80-90%)
• Warm, tropical/subtropical regions

**Soil:**
• Clayey or loamy soil that retains water
• pH: 5.5-6.5
• Flooded fields (puddled soil)

**Planting:**
• Kharif season: June-July
• Transplanting: 21-25 days old seedlings
• Spacing: 15×15 cm or 20×15 cm

**Water Management:**
• Continuous flooding during growth
• 5-10 cm water depth
• Drain before harvesting

**Fertilizers:**
• Nitrogen: 80-120 kg/ha (in splits)
• Phosphorus: 40-60 kg/ha
• Potassium: 40 kg/ha
• Zinc: 25 kg/ha (if deficient)

**Harvesting:**
• 110-140 days (variety dependent)
• When 80% grains turn golden
• Sun-dry to 14% moisture

**Pest Control:**
• Stem borer: Pheromone traps
• Brown plant hopper: Neem extracts
• Blast disease: Use resistant varieties

💡 **Best Practices:**
✅ System of Rice Intensification (SRI)
✅ Alternate wetting and drying
✅ Proper leveling of fields
✅ Use disease-free seeds"""
        
        elif "tomato" in message_lower:
            return """🍅 **Tomato Cultivation Guide**

**Climate:**
• Temperature: 20-30°C (day), 15-20°C (night)
• Warm, sunny weather
• Avoid frost and excessive rain

**Soil:**
• Well-drained loamy soil
• pH: 6.0-6.8
• Rich in organic matter

**Planting:**
• Nursery: Raise seedlings first (3-4 weeks)
• Transplanting: 15-20 cm tall seedlings
• Spacing: 60×45 cm or 75×60 cm
• Season: Feb-Mar (summer), Jun-Jul (rainy)

**Support:**
• Use stakes or cages for support
• Height: 4-5 feet
• Tie plants gently

**Fertilizers:**
• Compost: 20-25 tons/ha
• NPK: 100:50:50 kg/ha
• Calcium for preventing blossom end rot

**Irrigation:**
• Regular, moderate watering
• Drip irrigation recommended
• Avoid overhead watering (disease risk)
• Mulching helps retain moisture

**Common Diseases:**
• Late blight: Remove infected leaves, copper fungicide
• Early blight: Mancozeb spray
• Leaf curl virus: Control whiteflies

**Pests:**
• Fruit borer: Bt spray
• Aphids: Neem oil
• Whiteflies: Yellow sticky traps

**Harvesting:**
• 60-90 days after transplanting
• Pick when firm and colored
• Harvest regularly (2-3 days interval)

💡 **Tips:**
✅ 6-8 hours daily sunlight
✅ Prune suckers for better yield
✅ Rotate crops annually
✅ Use resistant varieties"""
        
        elif "potato" in message_lower:
            return """🥔 **Potato Cultivation Guide**

**Climate:**
• Temperature: 15-20°C (ideal)
• Cool weather crop
• Avoid high temperatures during tuber formation

**Soil:**
• Loose, well-drained sandy loam
• pH: 5.0-6.0 (slightly acidic)
• Good organic matter content

**Planting:**
• Season: October-November (plains), April-May (hills)
• Seed rate: 2-2.5 tons/ha
• Spacing: 50×20 cm
• Depth: 5-7 cm

**Seed Treatment:**
• Use disease-free seed tubers
• Cut large tubers (50-60g pieces)
• Treat with fungicide before planting

**Earthing Up:**
• Important operation 2-3 times
• Prevents greening of tubers
• Controls weeds

**Fertilizers:**
• FYM: 20-25 tons/ha
• Nitrogen: 120-150 kg/ha
• Phosphorus: 80 kg/ha
• Potassium: 100 kg/ha

**Irrigation:**
• 6-8 irrigations needed
• Critical: Flowering and tuber formation
• Avoid waterlogging

**Diseases:**
• Late blight: Mancozeb spray
• Early blight: Crop rotation
• Black scurf: Seed treatment

**Harvesting:**
• 90-120 days after planting
• When leaves turn yellow
• Cure tubers in shade 10-15 days

💡 **Storage:**
✅ Cool (2-4°C), dark place
✅ Prevent sprouting
✅ Good ventilation
✅ Check regularly for rot"""
        
        else:
            return """🌾 **Crop Cultivation Tips**

I can help you with detailed cultivation guides for:

**Major Crops:**
• 🌾 Wheat - Rabi crop
• 🍚 Rice - Kharif crop
• 🍅 Tomato - Vegetable crop
• 🥔 Potato - Tuber crop
• 🌽 Maize - Cereal crop
• 🌶️ Chili - Spice crop

**What I can tell you:**
• Climate and soil requirements
• Planting time and methods
• Fertilizer recommendations
• Irrigation schedules
• Pest and disease management
• Harvesting techniques
• Storage tips

**Ask me like:**
• "Tell me about wheat cultivation"
• "How to grow rice?"
• "Tomato farming tips"
• "Best time to plant potato"

**Type your crop name to get started!** 🚜"""
    
    # Greeting
    elif any(word in message_lower for word in ["hello", "hi", "hey", "namaste"]):
        response_en = f"""{get_greeting_by_language(user_lang)}

I can help you with:
🌤️ Weather forecasts
💰 Market prices
🌾 Crop cultivation tips
🔬 Disease detection (upload photo)

**What would you like to know?** 🚜"""
    
    # Default
    else:
        response_en = """🌾 **How can I help you today?**

Ask me about:
• 🔬 Crop disease (upload photo)
• 💰 Market prices
• 🌤️ Weather updates
• 🌱 Crop tips

**Type your question!** 🚜"""
    
    # Translate response if needed
    if user_lang != 'en':
        return translate_text(response_en, target_lang=user_lang)
    
    return response_en

# ---------------------- SIDEBAR ----------------------
with st.sidebar:
    st.markdown("""
    <div style="padding: 1.5rem 0 1.5rem 0; border-bottom: 1px solid rgba(76, 175, 80, 0.2);">
        <h2 style="font-size: 1.3rem; font-weight: 800; color: #66bb6a; margin: 0;">🌾 KRISHISAATHI AI</h2>
        <p style="font-size: 0.8rem; color: #81c784; margin: 0.4rem 0 0 0;">Smart Farming Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 Quick Actions")
    
    if st.button("🔷 Disease Detection"):
        user_msg = "Check crop disease"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg, st.session_state.selected_language)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
    
    if st.button("🏙️ Delhi Prices"):
        user_msg = "Show prices in Delhi"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg, st.session_state.selected_language)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
        
    if st.button("🌤️ Mumbai Weather"):
        user_msg = "Weather in Mumbai"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg, st.session_state.selected_language)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
        
    if st.button("🌾 Crop Tips"):
        user_msg = "Tell me about wheat"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg, st.session_state.selected_language)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
    
    st.divider()
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.expect_image = False
        st.rerun()

# ---------------------- CHAT INTERFACE ----------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------- IMAGE UPLOAD ----------------------
if st.session_state.expect_image:
    st.subheader("📸 Upload Crop Image")
    
    uploaded_file = st.file_uploader(
        "Choose an image", 
        type=["jpg", "png", "jpeg"]
    )
    
    if uploaded_file:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        
        with col2:
            with st.spinner("🔬 Analyzing..."):
                prediction = ai_predict_disease(uploaded_file)
                
                st.success(f"✅ Detection Complete!")
                st.metric("Disease", prediction['name'])
                st.metric("Confidence", f"{prediction['confidence']}%")
        
        if st.button("✅ Done"):
            st.session_state.expect_image = False
            result_msg = f"""✅ **Disease Detection Complete**

**Identified:** {prediction['name']} ({prediction['confidence']}% confidence)

**Symptoms:** {prediction['symptoms']}

**Treatment:** {prediction['treatment']}"""
            
            if st.session_state.selected_language != 'en':
                result_msg = translate_text(result_msg, target_lang=st.session_state.selected_language)
            
            st.session_state.messages.append({"role": "assistant", "content": result_msg})
            st.rerun()

# ---------------------- CHAT INPUT ----------------------
if prompt := st.chat_input("Ask about farming..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("🌱 Thinking..."):
            response = get_bot_response(prompt, st.session_state.selected_language)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# ---------------------- FOOTER ----------------------
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 12px; margin-top: 3rem; border: 1px solid #4caf50;">
    <p style="color: #66bb6a; font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem;">🌾 Krishisaathi AI</p>
    <p style="color: #81c784; font-size: 0.9rem; margin-bottom: 0;">Empowering Farmers with Technology</p>
    <p style="color: #a5d6a7; font-size: 0.8rem; margin-top: 1rem;">© 2025 Krishisaathi AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
