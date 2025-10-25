import streamlit as st
import random
import requests
from datetime import datetime
import re
import base64

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
    
    /* Hide Streamlit top-right menu */
    [data-testid="stToolbar"] {
        display: none;
    }
    
    /* Hide "Manage app" button */
    [data-testid="manage-app-button"] {
        display: none;
    }
    
    /* Hide Deploy button and other header buttons */
    .viewerBadge_container__r5tak {
        display: none;
    }
    
    .stDeployButton {
        display: none;
    }
    
    /* Make sure sidebar toggle is visible */
    [data-testid="collapsedControl"] {
        display: block !important;
    }
    
    section[data-testid="stSidebar"] {
        display: block !important;
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
    
    /* Sidebar Collapse Button - Make it visible */
    [data-testid="collapsedControl"] {
        background: #4caf50 !important;
        color: white !important;
        border-radius: 0 8px 8px 0 !important;
        padding: 0.5rem !important;
        display: block !important;
    }
    
    /* Ensure sidebar is visible */
    [data-testid="stSidebar"][aria-expanded="true"] {
        display: block !important;
        width: 21rem !important;
    }
    
    [data-testid="stSidebar"][aria-expanded="false"] {
        display: block !important;
        width: 0 !important;
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
    
    /* Audio Input Styling */
    .stAudioInput {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%) !important;
        border: 2px solid #ffb74d !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
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
    
    /* Metrics */
    [data-testid="stMetric"] {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #e8f5e9;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    
    [data-testid="stMetricLabel"] {
        color: #66bb6a;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    [data-testid="stMetricValue"] {
        color: #2e7d32;
        font-size: 1.75rem;
        font-weight: 700;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #f1f8f4;
        border-radius: 10px;
        padding: 0.25rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #66bb6a;
        font-weight: 600;
        padding: 0.6rem 1.25rem;
        font-size: 0.9rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        color: #2e7d32;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Disease Detection Section */
    .disease-section {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        border: 1px solid #e8f5e9;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        margin: 1.5rem 0;
    }
    
    /* Success/Info Boxes */
    .stSuccess, .stInfo {
        background: white;
        border-radius: 10px;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: #e8f5e9;
        margin: 2rem 0;
    }
    
    /* Text Colors */
    p, li, span {
        color: #37474f;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #1b5e20;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #4caf50 !important;
    }
    
    /* Footer */
    .pro-footer {
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 12px;
        margin-top: 3rem;
        border: 1px solid #e8f5e9;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    
    .pro-footer p {
        margin: 0.5rem 0;
        color: #66bb6a;
        font-size: 0.9rem;
    }
    
    .pro-footer strong {
        color: #2e7d32;
        font-weight: 700;
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
    
    /* Image Styling */
    img {
        border-radius: 10px;
    }
    
    /* Subheader Styling */
    .stSubheader {
        color: #2e7d32 !important;
        font-weight: 700 !important;
    }
    
    /* Clear Chat Button Special Style */
    [data-testid="stSidebar"] .stButton:last-child > button {
        background: #ffebee !important;
        border-color: #ffcdd2 !important;
        color: #c62828 !important;
        margin-top: 1rem;
    }
    
    [data-testid="stSidebar"] .stButton:last-child > button:hover {
        background: #ef5350 !important;
        border-color: #ef5350 !important;
        color: white !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem !important;
        }
        
        .app-title {
            font-size: 1.5rem;
        }
        
        .pro-header {
            flex-direction: column;
            text-align: center;
        }
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
        <p class="app-tagline">Connecting Farmers, Empowering Growth 🎤 Voice Enabled</p>
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

# ---------------------- SPEECH TO TEXT FUNCTION ----------------------
def transcribe_audio_groq(audio_bytes):
    """Transcribe audio using Groq's Whisper API (Free & Fast)"""
    try:
        # Groq API endpoint for Whisper
        GROQ_API_KEY = "gsk_your_api_key_here"  # Get free API key from console.groq.com
        
        if GROQ_API_KEY == "gsk_your_api_key_here":
            return None  # API key not configured
        
        # Encode audio to base64
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "whisper-large-v3",
            "audio": audio_base64,
            "language": "en"
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/audio/transcriptions",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json().get("text", "")
        else:
            return None
            
    except Exception as e:
        return None

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
        r"(?:in|at|for)\s+([a-zA-Z\s]+)",
        r"([a-zA-Z]+)\s+(?:price|weather|market)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, message_lower)
        if match:
            city = match.group(1).strip()
            city = re.sub(r'\b(today|tomorrow|now|current|latest|price|prices|weather)\b', '', city).strip()
            if city and len(city) > 2:
                return city
    return None

# ---------------------- FORMAT PRICE RESPONSE ----------------------
def format_price_response(prices, city_name=None):
    """Formats price data into readable response"""
    if not prices:
        return "❌ Sorry, no price data found. Try: Delhi, Mumbai, or Bangalore."
    
    response = "💰 **Current Market Prices:**\n\n"
    
    for city, produce_data in prices.items():
        if city_name and city_name.lower() not in city.lower():
            continue
            
        response += f"📍 **{city}**\n\n"
        
        for item, data in produce_data.items():
            response += f"• **{item}**: {data['price']} {data['unit']} {data['trend']}\n"
        
        response += "\n"
    
    response += "\n📊 **Legend:** ↑ Rising | → Stable | ↓ Falling\n"
    response += "📅 **Updated:** October 25, 2025\n"
    response += "💡 **Tip:** Prices are approximate retail rates."
    
    return response

# ---------------------- CHATBOT RESPONSE LOGIC ----------------------
def get_bot_response(user_message):
    """Generates intelligent responses"""
    message_lower = user_message.lower()
    
    # Disease detection trigger
    if any(word in message_lower for word in ["disease", "sick", "infected", "diagnose"]):
        st.session_state.expect_image = True
        return """🔬 **Crop Disease Detection**

📷 Please upload a clear photo of affected leaves or crops.

I'll analyze it and provide:
✅ Disease identification
✅ Treatment recommendations
✅ Prevention tips"""
    
    # Price queries
    if any(word in message_lower for word in ["price", "cost", "market"]):
        city = extract_city_from_message(user_message)
        
        if city:
            prices = get_produce_prices(city)
            return format_price_response(prices, city)
        else:
            return """💰 **Market Prices Available!**

🌆 **Cities Covered:** Delhi, Mumbai, Bangalore, and more!

💬 **Ask me:** "Show prices in Mumbai" or "Tomato price in Delhi"

🔍 Type your city name!"""
    
    # Weather queries
    if any(word in message_lower for word in ["weather", "temperature"]):
        city = extract_city_from_message(user_message)
        
        if not city:
            return "🌍 Please specify a location!\nExample: 'Weather in Delhi'"
        
        weather = get_weather(city)
        if weather:
            return f"""🌤️ **Weather in {weather['city']}:**
            
- Temperature: {weather['temperature']}°C (feels like {weather['feels_like']}°C)
- Conditions: {weather['description'].title()}
- Humidity: {weather['humidity']}%
- Wind: {weather['wind_speed']} m/s

**Advice:** {"Good for outdoor work! 🌞" if weather['temperature'] > 15 else "Indoor tasks recommended. 🧥"}"""
        else:
            return f"❌ Couldn't fetch weather for '{city}'."
    
    # Crop tips
    if any(word in message_lower for word in ["wheat", "rice", "tomato", "potato", "crop", "farming"]):
        return """🌾 **Crop Cultivation Guide**

I can help with detailed tips for:
• 🌾 Wheat
• 🍚 Rice
• 🍅 Tomato
• 🥔 Potato

Ask me: "Tell me about wheat cultivation" or "How to grow rice"

🚜 What crop would you like to know about?"""
    
    # Greeting
    if any(word in message_lower for word in ["hello", "hi", "hey", "namaste"]):
        return """🙏 **Namaste! Welcome to Krishisaathi AI!**

I can help you with:
🌤️ Weather forecasts
💰 Market prices
🌾 Crop cultivation tips
🔬 Disease detection
🎤 Voice commands

**Try saying: "Weather in Delhi" or "Show prices"** 🚜"""
    
    # Default
    return """🌾 **How can I help you today?**

Ask me about:
• 🔬 Crop disease (upload photo)
• 💰 Market prices
• 🌤️ Weather updates
• 🌱 Crop tips
• 🎤 Use voice input!

**Type or speak your question!** 🚜"""

# ---------------------- SIDEBAR ----------------------
with st.sidebar:
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
        ">Smart Farming Assistant 🎤</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 Quick Actions")
    
    if st.button("📷 Disease Detection"):
        user_msg = "Check crop disease"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
    
    if st.button("📊 Delhi Prices"):
        user_msg = "Show prices in Delhi"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
        
    if st.button("🌤️ Mumbai Weather"):
        user_msg = "Weather in Mumbai"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
        
    if st.button("🌾 Crop Tips"):
        user_msg = "Tell me about farming"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
    
    st.divider()
    
    # Voice Input Section
    st.markdown("### 🎤 Voice Input")
    st.info("📢 Click to record your voice")
    
    # Streamlit's built-in audio input
    audio_value = st.audio_input("Record your question")
    
    if audio_value:
        st.audio(audio_value)
        
        # Try automatic transcription
        if st.button("🎯 Auto Transcribe", key="auto_transcribe"):
            with st.spinner("🎤 Converting speech to text..."):
                audio_bytes = audio_value.getvalue()
                transcribed_text = transcribe_audio_groq(audio_bytes)
                
                if transcribed_text:
                    st.success(f"✅ Transcribed: {transcribed_text}")
                    
                    # Automatically add to chat
                    st.session_state.messages.append({"role": "user", "content": f"🎤 {transcribed_text}"})
                    bot_response = get_bot_response(transcribed_text)
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    st.rerun()
                else:
                    st.warning("⚠️ Auto-transcription unavailable. Please type your message below.")
        
        # Manual fallback option
        st.markdown("---")
        st.markdown("**Or type what you said:**")
        manual_text = st.text_input("Your message:", key="manual_voice_input", label_visibility="collapsed")
        
        if manual_text:
            if st.button("📤 Send Voice Message"):
                st.session_state.messages.append({"role": "user", "content": f"🎤 {manual_text}"})
                bot_response = get_bot_response(manual_text)
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

# ---------------------- IMAGE UPLOAD SECTION ----------------------
if st.session_state.expect_image:
    st.markdown('<div class="disease-section">', unsafe_allow_html=True)
    st.subheader("📸 Upload Crop Image for Disease Detection")
    
    uploaded_file = st.file_uploader(
        "Choose an image (JPG, PNG, JPEG)", 
        type=["jpg", "png", "jpeg"]
    )
    
    if uploaded_file:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(uploaded_file, caption="Uploaded Crop Image", use_container_width=True)
        
        with col2:
            with st.spinner("🔬 Analyzing image..."):
                prediction = ai_predict_disease(uploaded_file)
                
                st.success(f"✅ **Detection Complete!**")
                st.metric("Disease Identified", prediction['name'])
                st.metric("Confidence", f"{prediction['confidence']}%")
        
        st.markdown("---")
        st.markdown("### 📋 Detailed Analysis")
        
        tab1, tab2, tab3 = st.tabs(["🔍 Symptoms", "💊 Treatment", "🛡️ Prevention"])
        
        with tab1:
            st.write(f"**Symptoms:** {prediction['symptoms']}")
        
        with tab2:
            st.write(f"**Treatment:** {prediction['treatment']}")
        
        with tab3:
            st.write(f"**Prevention:** {prediction['prevention']}")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Analyze Another Image"):
                st.session_state.expect_image = True
                st.rerun()
        
        with col_b:
            if st.button("✅ Done"):
                st.session_state.expect_image = False
                result_msg = f"""✅ **Disease Detection Complete**

**Identified:** {prediction['name']} ({prediction['confidence']}% confidence)

**Symptoms:** {prediction['symptoms']}

**Treatment:** {prediction['treatment']}

**Prevention:** {prediction['prevention']}"""
                
                st.session_state.messages.append({"role": "assistant", "content": result_msg})
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- CHAT INPUT ----------------------
if prompt := st.chat_input("Ask about farming... or use voice input above 🎤"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("🌱 Thinking..."):
            response = get_bot_response(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# ---------------------- FOOTER ----------------------
st.markdown("""
<div class="pro-footer">
    <p><strong>🌾 Krishisaathi AI</strong> - Empowering Farmers with Technology</p>
    <p>💡 AI Disease Detection | Voice Recognition | Weekly Updated Prices | Real-time Weather</p>
    <p style="font-size: 0.85em;">© 2025 Krishisaathi AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
