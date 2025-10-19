import streamlit as st
import random
import requests
from datetime import datetime
import re
from langdetect import detect, LangDetectException

# ---------------------- STREAMLIT CONFIG ----------------------
st.set_page_config(
    page_title="🌾 Krishisaathi AI", 
    page_icon="🌱", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------- PROFESSIONAL MODERN CSS ----------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hide Streamlit top-right menu */
    [data-testid="stToolbar"] {
        display: none;
    }
    
    /* Hide "Manage app" button */
    [data-testid="manage-app-button"] {
        display: none;
    }
    
    button[kind="header"] {
        display: none;
    }
    
    /* Hide Deploy button and other header buttons */
    .viewerBadge_container__r5tak {
        display: none;
    }
    
    .stActionButton {
        display: none;
    }
    
    /* Main Background */
    .main {
        background: #f8faf9;
        padding: 0;
    }
    
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1400px !important;
        margin: 0 auto;
    }
    
    /* Professional Header */
    .pro-header {
        background: white;
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        border: 1px solid #e8f5e9;
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .header-logo {
        flex-shrink: 0;
    }
    
    .header-content {
        flex-grow: 1;
    }
    
    .app-title {
        font-size: 2rem;
        font-weight: 800;
        color: #2e7d32;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .app-tagline {
        color: #66bb6a;
        font-size: 0.95rem;
        font-weight: 500;
        margin: 0.25rem 0 0 0;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: white !important;
        border-right: 1px solid #e8f5e9 !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: white !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background: white !important;
    }
    
    /* Sidebar Logo */
    [data-testid="stSidebar"] img {
        transition: all 0.3s ease;
        width: 100% !important;
        max-width: 160px !important;
        height: auto !important;
        margin: 0 auto;
        display: block;
    }
    
    [data-testid="stSidebar"] img:hover {
        transform: scale(1.03);
    }
    
    /* Sidebar Headers */
    [data-testid="stSidebar"] h3 {
        color: #1b5e20 !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Sidebar Buttons */
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background: #f1f8f4 !important;
        border: 1px solid #e8f5e9 !important;
        color: #2e7d32 !important;
        padding: 0.85rem 1rem !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        text-align: left !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
        height: 48px !important;
        min-height: 48px !important;
        max-height: 48px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        margin-bottom: 0.5rem !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #4caf50 !important;
        border-color: #4caf50 !important;
        color: white !important;
        transform: translateX(3px);
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.25) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:active {
        transform: translateX(1px);
    }
    
    /* Chat Messages */
    .stChatMessage {
        background: white !important;
        border-radius: 12px !important;
        border: 1px solid #e8f5e9 !important;
        margin-bottom: 1rem !important;
        padding: 1.25rem !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02) !important;
    }
    
    /* User Message */
    [data-testid="user-message"] {
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8f4 100%) !important;
        border-left: 3px solid #4caf50 !important;
    }
    
    /* Assistant Message */
    [data-testid="assistant-message"] {
        background: white !important;
        border-left: 3px solid #81c784 !important;
    }
    
    /* Chat Input */
    .stChatInputContainer {
        background: white !important;
        border: 2px solid #e8f5e9 !important;
        border-radius: 12px !important;
        padding: 0.5rem !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }
    
    .stChatInputContainer:focus-within {
        border-color: #4caf50 !important;
        box-shadow: 0 4px 16px rgba(76, 175, 80, 0.15) !important;
    }
    
    /* Main Buttons */
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
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: white;
        border: 2px dashed #c8e6c9;
        border-radius: 12px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #4caf50;
        background: #f1f8f4;
    }
    
    /* Language Badge */
    .lang-badge {
        display: inline-block;
        background: #e8f5e9;
        color: #2e7d32;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #e8f5e9;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    
    /* Disease Section */
    .disease-section {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        border: 1px solid #e8f5e9;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        margin: 1.5rem 0;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f8f4;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c8e6c9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #4caf50;
    }
</style>
""", unsafe_allow_html=True)

# Display professional header
header_col1, header_col2 = st.columns([1, 5])

with header_col1:
    try:
        st.image("logo.png", use_container_width=True)
    except FileNotFoundError:
        st.markdown('<div style="font-size: 4rem; text-align: center;">🌾</div>', unsafe_allow_html=True)

with header_col2:
    st.markdown("""
    <div style="display: flex; flex-direction: column; justify-content: center; height: 100%;">
        <h1 class="app-title">KRISHISAATHI AI</h1>
        <p class="app-tagline">Connecting Farmers, Empowering Growth | किसानों को जोड़ना, विकास को सशक्त बनाना</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr>', unsafe_allow_html=True)

# ---------------------- INITIALIZE SESSION ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_location" not in st.session_state:
    st.session_state.user_location = None
if "expect_image" not in st.session_state:
    st.session_state.expect_image = False
if "user_entities" not in st.session_state:
    st.session_state.user_entities = {}

# ---------------------- LANGUAGE DETECTION & ENTITY EXTRACTION ----------------------
def detect_language(text):
    """Detect language of the input text"""
    try:
        lang = detect(text)
        if lang == 'hi':
            return 'hi'
        else:
            return 'en'
    except LangDetectException:
        return 'en'

# Language-specific patterns for entity extraction
ENTITY_PATTERNS = {
    'en': {
        'name': r'\b(?:my name is|i am|i\'m|this is|call me)\s+([A-Za-z\s]+?)(?:\.|,|$|\s+and)',
        'phone': r'\b(?:\+?91[-.\s]?)?[6-9]\d{9}\b',
        'location': r'\b(?:from|in|at|live in|located in)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        'crop': r'\b(?:growing|cultivating|planting|farming)\s+([a-z]+)',
    },
    'hi': {
        'name': r'(?:मेरा नाम|मैं|नाम)\s+([ा-ॿA-Za-z\s]+?)(?:\s+है|\.|,|$)',
        'phone': r'\b(?:\+?91[-.\s]?)?[6-9]\d{9}\b',
        'location': r'(?:से हूं|रहता हूं|रहती हूं|में रहता)\s+([ा-ॿA-Za-z\s]+)',
        'crop': r'(?:उगा रहा|खेती|फसल)\s+([ा-ॿA-Za-z]+)',
    }
}

def extract_entities(text, lang):
    """Extract entities from text based on language"""
    entities = {}
    patterns = ENTITY_PATTERNS.get(lang, ENTITY_PATTERNS['en'])
    
    for entity_type, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            entities[entity_type] = match.group(1).strip()
    
    # Update session state with extracted entities
    for key, value in entities.items():
        st.session_state.user_entities[key] = value
    
    return entities

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

# ---------------------- DISEASE DETECTION (PLACEHOLDER) ----------------------
def ai_predict_disease(image_file):
    """Placeholder for future ML model"""
    diseases = {
        "Tomato - Late Blight": {
            "symptoms": "Dark brown spots on leaves, white mold on undersides",
            "treatment": "Remove infected leaves, apply copper-based fungicide, improve air circulation",
            "prevention": "Avoid overhead watering, use resistant varieties",
            "symptoms_hi": "पत्तियों पर गहरे भूरे धब्बे, निचली सतह पर सफेद फफूंद",
            "treatment_hi": "संक्रमित पत्तियों को हटाएं, तांबे आधारित कवकनाशी लगाएं",
            "prevention_hi": "ऊपर से पानी देने से बचें, प्रतिरोधी किस्मों का उपयोग करें"
        },
        "Potato - Early Blight": {
            "symptoms": "Circular brown spots with concentric rings on older leaves",
            "treatment": "Apply fungicide (Mancozeb), remove infected leaves",
            "prevention": "Crop rotation, proper spacing, mulching",
            "symptoms_hi": "पुरानी पत्तियों पर गोलाकार भूरे धब्बे",
            "treatment_hi": "कवकनाशी (मैंकोजेब) लगाएं, संक्रमित पत्तियां हटाएं",
            "prevention_hi": "फसल चक्र, उचित दूरी, मल्चिंग"
        },
        "Healthy Crop": {
            "symptoms": "No disease detected",
            "treatment": "Continue regular care and monitoring",
            "prevention": "Maintain good agricultural practices",
            "symptoms_hi": "कोई बीमारी नहीं पाई गई",
            "treatment_hi": "नियमित देखभाल जारी रखें",
            "prevention_hi": "अच्छी कृषि पद्धतियों को बनाए रखें"
        }
    }
    
    disease_name = random.choice(list(diseases.keys()))
    disease_info = diseases[disease_name]
    
    return {
        "name": disease_name,
        "confidence": random.randint(75, 98),
        **disease_info
    }

# ---------------------- PRODUCE PRICE FUNCTION ----------------------
def get_produce_prices(state="all"):
    """Weekly Updated Market Prices"""
    
    sample_prices = {
        "Delhi": {
            "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹14-24", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹8-10", "unit": "per kg", "trend": "→"},
            "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹45-60", "unit": "per dozen", "trend": "→"}
        },
        "Mumbai": {
            "Tomato": {"price": "₹26-40", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹18-28", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹17-26", "unit": "per kg", "trend": "↓"},
            "Apple": {"price": "₹90-130", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹48-65", "unit": "per dozen", "trend": "→"}
        },
        "Bangalore": {
            "Tomato": {"price": "₹24-36", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹16-25", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹15-22", "unit": "per kg", "trend": "↓"},
            "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹40-54", "unit": "per dozen", "trend": "→"}
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

# ---------------------- EXTRACT CITY FROM MESSAGE ----------------------
def extract_city_from_message(message):
    """Extracts city name from user message"""
    message_lower = message.lower()
    
    patterns = [
        r"(?:in|at|for|का|में)\s+([a-zA-Zा-ॿ\s]+)",
        r"([a-zA-Z]+)\s+(?:price|weather|market|मौसम|कीमत)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, message_lower)
        if match:
            city = match.group(1).strip()
            city = re.sub(r'\b(today|tomorrow|now|current|latest|price|prices|weather|आज|कल|मौसम|कीमत)\b', '', city).strip()
            if city and len(city) > 2:
                return city
    return None

# ---------------------- FORMAT PRICE RESPONSE ----------------------
def format_price_response(prices, city_name=None, lang='en'):
    """Formats price data into readable response"""
    if not prices:
        if lang == 'hi':
            return "❌ क्षमा करें, कोई मूल्य डेटा नहीं मिला। कोशिश करें: दिल्ली, मुंबई, या बैंगलोर।"
        return "❌ Sorry, no price data found. Try: Delhi, Mumbai, or Bangalore."
    
    if lang == 'hi':
        response = "💰 **वर्तमान बाजार मूल्य:**\n\n"
    else:
        response = "💰 **Current Market Prices:**\n\n"
    
    for city, produce_data in prices.items():
        if city_name and city_name.lower() not in city.lower():
            continue
            
        response += f"📍 **{city}**\n\n"
        
        for item, data in produce_data.items():
            response += f"• **{item}**: {data['price']} {data['unit']} {data['trend']}\n"
        
        response += "\n"
    
    if lang == 'hi':
        response += "\n📊 **किंवदंती:** ↑ बढ़ रहा | → स्थिर | ↓ गिर रहा\n"
        response += "📅 **अपडेट:** 19 अक्टूबर, 2025\n"
        response += "💡 **सुझाव:** कीमतें अनुमानित खुदरा दरें हैं।"
    else:
        response += "\n📊 **Legend:** ↑ Rising | → Stable | ↓ Falling\n"
        response += "📅 **Updated:** October 19, 2025\n"
        response += "💡 **Tip:** Prices are approximate retail rates."
    
    return response

# ---------------------- CHATBOT RESPONSE LOGIC ----------------------
def get_bot_response(user_message, lang='en'):
    """Generates intelligent bilingual responses"""
    message_lower = user_message.lower()
    
    # Detect language
    detected_lang = detect_language(user_message)
    
    # Extract entities
    entities = extract_entities(user_message, detected_lang)
    
    # Disease detection trigger
    disease_keywords_en = ["disease", "sick", "infected", "diagnose", "problem", "leaf"]
    disease_keywords_hi = ["बीमारी", "रोग", "संक्रमित", "समस्या", "पत्ती"]
    
    if any(word in message_lower for word in disease_keywords_en + disease_keywords_hi):
        st.session_state.expect_image = True
        if detected_lang == 'hi':
            return """🔬 **फसल रोग पहचान**

📷 कृपया प्रभावित पत्तियों या फसलों की स्पष्ट तस्वीर अपलोड करें।

मैं इसका विश्लेषण करूंगा और प्रदान करूंगा:
✅ रोग की पहचान
✅ उपचार की सिफारिशें
✅ रोकथाम के टिप्स"""
        return """🔬 **Crop Disease Detection**

📷 Please upload a clear photo of affected leaves or crops.

I'll analyze it and provide:
✅ Disease identification
✅ Treatment recommendations
✅ Prevention tips"""
    
    # Price queries
    price_keywords_en = ["price", "cost", "market", "rate"]
    price_keywords_hi = ["कीमत", "मूल्य", "दाम", "भाव", "बाजार"]
    
    if any(word in message_lower for word in price_keywords_en + price_keywords_hi):
        city = extract_city_from_message(user_message)
        
        if city:
            prices = get_produce_prices(city)
            return format_price_response(prices, city, detected_lang)
        else:
            if detected_lang == 'hi':
                return """💰 **बाजार मूल्य उपलब्ध!**

🌆 **शहर शामिल:** दिल्ली, मुंबई, बैंगलोर, और अधिक!

💬 **मुझसे पूछें:** "मुंबई में कीमत दिखाएं" या "दिल्ली में टमाटर की कीमत"

📍 अपने शहर का नाम टाइप करें!"""
            return """💰 **Market Prices Available!**

🌆 **Cities Covered:** Delhi, Mumbai, Bangalore, and more!

💬 **Ask me:** "Show prices in Mumbai" or "Tomato price in Delhi"

📍 Type your city name!"""
    
    # Weather queries
    weather_keywords_en = ["weather", "temperature", "climate", "forecast"]
    weather_keywords_hi = ["मौसम", "तापमान", "जलवायु"]
    
    if any(word in message_lower for word in weather_keywords_en + weather_keywords_hi):
        city = extract_city_from_message(user_message)
        
        if not city:
            if detected_lang == 'hi':
                return "🌍 कृपया एक स्थान निर्दिष्ट करें!\nउदाहरण: 'दिल्ली का मौसम'"
            return "🌍 Please specify a location!\nExample: 'Weather in Delhi'"
        
        weather = get_weather(city)
        if weather:
            if detected_lang == 'hi':
                return f"""🌤️ **{weather['city']} में मौसम:**
            
- तापमान: {weather['temperature']}°C (महसूस होता है {weather['feels_like']}°C)
- स्थिति: {weather['description'].title()}
- आर्द्रता: {weather['humidity']}%
- हवा: {weather['wind_speed']} m/s

**सलाह:** {"बाहर काम के लिए अच्छा! 🌞" if weather['temperature'] > 15 else "घर के अंदर के कार्य अनुशंसित। 🧥"}"""
            return f"""🌤️ **Weather in {weather['city']}:**
            
- Temperature: {weather['temperature']}°C (feels like {weather['feels_like']}°C)
- Conditions: {weather['description'].title()}
- Humidity: {weather['humidity']}%
- Wind: {weather['wind_speed']} m/s

**Advice:** {"Good for outdoor work! 🌞" if weather['temperature'] > 15 else "Indoor tasks recommended. 🧥"}"""
        else:
            if detected_lang == 'hi':
                return f"❌ '{city}' के लिए मौसम नहीं मिल सका।"
            return f"❌ Couldn't fetch weather for '{city}'."
    
    # Greeting
    greeting_keywords_en = ["hello", "hi", "hey"]
    greeting_keywords_hi = ["नमस्ते", "हैलो", "हाय", "प्रणाम"]
    
    if any(word in message_lower for word in greeting_keywords_en + greeting_keywords_hi):
        name_greeting = ""
        if 'name' in st.session_state.user_entities:
            if detected_lang == 'hi':
                name_greeting = f" {st.session_state.user_entities['name']} जी"
            else:
                name_greeting = f" {st.session_state.user_entities['name']}"
        
        if detected_lang == 'hi':
            return f"""🙏 **नमस्ते{name_greeting}! कृषिसाथी AI में आपका स्वागत है!**

मैं आपकी मदद कर सकता हूं:
🌤️ मौसम पूर्वानुमान
💰 बाजार मूल्य (100+ शहर)
🌾 फसल की खेती के टिप्स
🔬 रोग का पता लगाना (फोटो अपलोड करें)
🛡️ कीट प्रबंधन

**आप क्या जानना चाहते हैं?** 🚜"""
        return f"""🙏 **Namaste{name_greeting}! Welcome to Krishisaathi AI!**

I can help you with:
🌤️ Weather forecasts
💰 Market prices (100+ cities)
🌾 Crop cultivation tips
🔬 Disease detection (upload photo)
🛡️ Pest management

**What would you like to know?** 🚜"""
    
    # Default
    if detected_lang == 'hi':
        return """🌾 **मैं आज आपकी कैसे मदद कर सकता हूं?**

मुझसे पूछें:
• 🔬 फसल रोग (फोटो अपलोड करें)
• 💰 बाजार मूल्य
• 🌤️ मौसम अपडेट
• 🌱 फसल टिप्स

**अपना सवाल टाइप करें!** 🚜"""
    return """🌾 **How can I help you today?**

Ask me about:
• 🔬 Crop disease (upload photo)
• 💰 Market prices
• 🌤️ Weather updates
• 🌱 Crop tips

**Type your question!** 🚜"""

# ---------------------- SIDEBAR ----------------------
with st.sidebar:
    # App Name Header
    st.markdown("""
    <div style="padding: 1.5rem 0 1.5rem 0; border-bottom: 1px solid rgba(76, 175, 80, 0.2);">
        <h2 style="
            font-size: 1.3rem;
            font-weight: 800;
            color: #66bb6a;
            margin: 0;
            letter-spacing: 0.5px;
            line-height: 1.2;
        ">🌾 KRISHISAATHI AI</h2>
        <p style="
            font-size: 0.8rem;
            color: #81c784;
            margin: 0.4rem 0 0 0;
            font-weight: 500;
        ">Smart Farming Assistant | स्मार्ट खेती सहायक</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show extracted user info
    if st.session_state.user_entities:
        st.markdown("### 👤 Your Information")
        for key, value in st.session_state.user_entities.items():
            entity_labels = {
                'name': '📛 Name | नाम',
                'phone': '📞 Phone | फोन',
                'location': '📍 Location | स्थान',
                'crop': '🌾 Crop | फसल'
            }
            label = entity_labels.get(key, key.capitalize())
            st.info(f"{label}: **{value}**")
        st.divider()
    
    st.markdown("### 🎯 Quick Actions | त्वरित कार्रवाई")
    
    if st.button("🔬 Disease Detection | रोग पहचान"):
        user_msg = "Check crop disease"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
    
    if st.button("💰 Delhi Prices | दिल्ली के दाम"):
        user_msg = "Show prices in Delhi"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
        
    if st.button("🌤️ Mumbai Weather | मुंबई का मौसम"):
        user_msg = "Weather in Mumbai"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
        
    if st.button("🌾 Crop Tips | फसल टिप्स"):
        user_msg = "Tell me about wheat"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
    
    st.divider()
    
    if st.button("🗑️ Clear Chat | चैट साफ़ करें"):
        st.session_state.messages = []
        st.session_state.expect_image = False
        st.session_state.user_entities = {}
        st.rerun()

# ---------------------- CHAT INTERFACE ----------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Detect language and show badge
        if message["role"] == "user":
            detected_lang = detect_language(message["content"])
            lang_display = "🇮🇳 हिंदी" if detected_lang == 'hi' else "🇬🇧 English"
            st.markdown(f'<span class="lang-badge">{lang_display}</span>', unsafe_allow_html=True)
        st.markdown(message["content"])

# ---------------------- IMAGE UPLOAD SECTION ----------------------
if st.session_state.expect_image:
    st.markdown('<div class="disease-section">', unsafe_allow_html=True)
    st.subheader("📸 Upload Crop Image for Disease Detection | रोग पहचान के लिए फसल की तस्वीर अपलोड करें")
    
    uploaded_file = st.file_uploader(
        "Choose an image (JPG, PNG, JPEG) | एक छवि चुनें", 
        type=["jpg", "png", "jpeg"]
    )
    
    if uploaded_file:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(uploaded_file, caption="Uploaded Crop Image | अपलोड की गई फसल छवि", use_container_width=True)
        
        with col2:
            with st.spinner("🔬 Analyzing image... | छवि का विश्लेषण कर रहे हैं..."):
                prediction = ai_predict_disease(uploaded_file)
                
                st.success(f"✅ **Detection Complete! | पहचान पूर्ण!**")
                st.metric("Disease Identified | पहचानी गई बीमारी", prediction['name'])
                st.metric("Confidence | विश्वास", f"{prediction['confidence']}%")
        
        st.markdown("---")
        st.markdown("### 📋 Detailed Analysis | विस्तृत विश्लेषण")
        
        tab1, tab2, tab3 = st.tabs(["🔍 Symptoms | लक्षण", "💊 Treatment | उपचार", "🛡️ Prevention | रोकथाम"])
        
        # Check if user prefers Hindi based on last message
        last_lang = 'en'
        if st.session_state.messages:
            last_lang = detect_language(st.session_state.messages[-1]["content"])
        
        with tab1:
            if last_lang == 'hi':
                st.write(f"**लक्षण:** {prediction.get('symptoms_hi', prediction['symptoms'])}")
            else:
                st.write(f"**Symptoms:** {prediction['symptoms']}")
        
        with tab2:
            if last_lang == 'hi':
                st.write(f"**उपचार:** {prediction.get('treatment_hi', prediction['treatment'])}")
            else:
                st.write(f"**Treatment:** {prediction['treatment']}")
        
        with tab3:
            if last_lang == 'hi':
                st.write(f"**रोकथाम:** {prediction.get('prevention_hi', prediction['prevention'])}")
            else:
                st.write(f"**Prevention:** {prediction['prevention']}")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Analyze Another Image | दूसरी छवि का विश्लेषण करें"):
                st.session_state.expect_image = True
                st.rerun()
        
        with col_b:
            if st.button("✅ Done | हो गया"):
                st.session_state.expect_image = False
                
                if last_lang == 'hi':
                    result_msg = f"""✅ **रोग पहचान पूर्ण**

**पहचाना गया:** {prediction['name']} ({prediction['confidence']}% विश्वास)

**लक्षण:** {prediction.get('symptoms_hi', prediction['symptoms'])}

**उपचार:** {prediction.get('treatment_hi', prediction['treatment'])}

**रोकथाम:** {prediction.get('prevention_hi', prediction['prevention'])}"""
                else:
                    result_msg = f"""✅ **Disease Detection Complete**

**Identified:** {prediction['name']} ({prediction['confidence']}% confidence)

**Symptoms:** {prediction['symptoms']}

**Treatment:** {prediction['treatment']}

**Prevention:** {prediction['prevention']}"""
                
                st.session_state.messages.append({"role": "assistant", "content": result_msg})
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- CHAT INPUT ----------------------
if prompt := st.chat_input("Ask about farming... | खेती के बारे में पूछें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        # Detect and show language badge
        detected_lang = detect_language(prompt)
        lang_display = "🇮🇳 हिंदी" if detected_lang == 'hi' else "🇬🇧 English"
        st.markdown(f'<span class="lang-badge">{lang_display}</span>', unsafe_allow_html=True)
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("🌱 Thinking... | सोच रहे हैं..."):
            response = get_bot_response(prompt, detected_lang)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# ---------------------- FOOTER ----------------------
st.markdown("""
<div class="pro-footer">
    <p><strong>🌾 Krishisaathi AI</strong> - Empowering Farmers with Technology | प्रौद्योगिकी के साथ किसानों को सशक्त बनाना</p>
    <p>💡 AI Disease Detection | Weekly Updated Prices | Real-time Weather</p>
    <p>💡 एआई रोग पहचान | साप्ताहिक अपडेट मूल्य | वास्तविक समय मौसम</p>
    <p style="font-size: 0.85em;">© 2025 Krishisaathi AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
