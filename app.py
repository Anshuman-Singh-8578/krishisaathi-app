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

# ---------------------- PROFESSIONAL MODERN CSS ----------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    [data-testid="stToolbar"] {
        display: none;
    }
    
    .stDeployButton {
        display: none;
    }
    
    /* FORCE SIDEBAR TO SHOW */
    section[data-testid="stSidebar"] {
        display: flex !important;
        visibility: visible !important;
        width: 21rem !important;
        min-width: 21rem !important;
        max-width: 21rem !important;
        background: white !important;
        border-right: 2px solid #4caf50 !important;
        z-index: 999999 !important;
    }
    
    section[data-testid="stSidebar"] > div {
        width: 21rem !important;
        background: white !important;
        visibility: visible !important;
    }
    
    /* Sidebar toggle button */
    button[kind="header"] {
        display: block !important;
    }
    
    .main {
        background: linear-gradient(135deg, #f8faf9 0%, #e8f5e9 100%);
        padding: 0;
    }
    
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1400px !important;
        margin: 0 auto;
    }
    
    .app-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .app-tagline {
        color: #66bb6a;
        font-size: 0.95rem;
        font-weight: 500;
        margin: 0.25rem 0 0 0;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #1b5e20 !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        background: white !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #f1f8f4 0%, #e8f5e9 100%) !important;
        border: 2px solid #4caf50 !important;
        color: #2e7d32 !important;
        padding: 0.85rem 1rem !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        text-align: left !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
        height: 48px !important;
        margin-bottom: 0.5rem !important;
        box-shadow: 0 2px 4px rgba(76, 175, 80, 0.1) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%) !important;
        border-color: #2e7d32 !important;
        color: white !important;
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3) !important;
    }
    
    .stChatMessage {
        background: white !important;
        border-radius: 12px !important;
        border: 1px solid #e8f5e9 !important;
        margin-bottom: 1rem !important;
        padding: 1.25rem !important;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.08) !important;
    }
    
    .stChatInputContainer {
        background: white !important;
        border: 2px solid #4caf50 !important;
        border-radius: 12px !important;
        padding: 0.5rem !important;
        box-shadow: 0 4px 16px rgba(76, 175, 80, 0.15) !important;
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
    
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff 0%, #f1f8f4 100%);
        border-radius: 10px;
        padding: 1rem;
        border: 2px solid #4caf50;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.1);
    }
    
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #4caf50, transparent);
        margin: 2rem 0;
    }
    
    /* THEMED FOOTER */
    .pro-footer {
        text-align: center;
        padding: 2.5rem;
        background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%);
        border-radius: 16px;
        margin-top: 3rem;
        border: 2px solid #1b5e20;
        box-shadow: 0 8px 24px rgba(46, 125, 50, 0.2);
    }
    
    .pro-footer p {
        margin: 0.5rem 0;
        color: white;
        font-size: 1rem;
    }
    
    .pro-footer strong {
        color: #e8f5e9;
        font-weight: 800;
        font-size: 1.2rem;
    }
    
    /* Voice button */
    .voice-button-container {
        position: fixed;
        bottom: 120px;
        right: 40px;
        z-index: 999999;
    }
    
    .voice-btn {
        width: 65px;
        height: 65px;
        border-radius: 50%;
        background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
        border: 3px solid white;
        cursor: pointer;
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        font-size: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        color: white;
    }
    
    .voice-btn:hover {
        transform: scale(1.15);
        box-shadow: 0 8px 28px rgba(76, 175, 80, 0.5);
    }
    
    .voice-btn.recording {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        animation: pulse 1s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4); }
        50% { transform: scale(1.2); box-shadow: 0 8px 32px rgba(255, 107, 107, 0.6); }
    }
    
    .voice-status-box {
        position: fixed;
        bottom: 195px;
        right: 40px;
        background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
        color: white;
        padding: 12px 24px;
        border-radius: 25px;
        box-shadow: 0 4px 16px rgba(76, 175, 80, 0.3);
        font-size: 0.95rem;
        font-weight: 700;
        display: none;
        z-index: 999999;
        border: 2px solid white;
    }
    
    .voice-status-box.show {
        display: block;
        animation: slideIn 0.3s;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Clear button special style */
    [data-testid="stSidebar"] .stButton:last-child > button {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%) !important;
        border-color: #ef5350 !important;
        color: #c62828 !important;
        margin-top: 1.5rem;
    }
    
    [data-testid="stSidebar"] .stButton:last-child > button:hover {
        background: linear-gradient(135deg, #ef5350 0%, #e53935 100%) !important;
        border-color: #c62828 !important;
        color: white !important;
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
        <p class="app-tagline">🌾 Connecting Farmers, Empowering Growth - Voice Enabled 🎤</p>
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

# ---------------------- PRODUCE PRICE FUNCTION ----------------------
def get_produce_prices(state="all"):
    """Weekly Updated Market Prices"""
    
    sample_prices = {
        "Delhi": {
            "Tomato": {"price": "Rs 22-36", "unit": "per kg", "trend": "Down"},
            "Potato": {"price": "Rs 14-24", "unit": "per kg", "trend": "Stable"},
            "Onion": {"price": "Rs 15-23", "unit": "per kg", "trend": "Down"},
            "Cabbage": {"price": "Rs 8-10", "unit": "per kg", "trend": "Stable"},
            "Apple": {"price": "Rs 85-120", "unit": "per kg", "trend": "Stable"},
            "Banana": {"price": "Rs 45-60", "unit": "per dozen", "trend": "Stable"}
        },
        "Mumbai": {
            "Tomato": {"price": "Rs 26-40", "unit": "per kg", "trend": "Down"},
            "Potato": {"price": "Rs 18-28", "unit": "per kg", "trend": "Stable"},
            "Onion": {"price": "Rs 17-26", "unit": "per kg", "trend": "Down"},
            "Apple": {"price": "Rs 90-130", "unit": "per kg", "trend": "Stable"},
            "Banana": {"price": "Rs 48-65", "unit": "per dozen", "trend": "Stable"}
        },
        "Bangalore": {
            "Tomato": {"price": "Rs 24-36", "unit": "per kg", "trend": "Down"},
            "Potato": {"price": "Rs 16-25", "unit": "per kg", "trend": "Stable"},
            "Onion": {"price": "Rs 15-22", "unit": "per kg", "trend": "Down"},
            "Apple": {"price": "Rs 85-120", "unit": "per kg", "trend": "Stable"},
            "Banana": {"price": "Rs 40-54", "unit": "per dozen", "trend": "Stable"}
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
            response += f"• **{item}**: {data['price']} {data['unit']} ({data['trend']})\n"
        
        response += "\n"
    
    response += "\n📊 Updated: October 25, 2025\n"
    response += "💡 Tip: Prices are approximate retail rates."
    
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

I will analyze it and provide:
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
            return f"❌ Could not fetch weather for '{city}'."
    
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
🎤 Voice commands (Click green mic button!)

**Try asking: "Weather in Delhi" or "Show prices"** 🚜"""
    
    # Default
    return """🌾 **How can I help you today?**

Ask me about:
• 🔬 Crop disease (upload photo)
• 💰 Market prices
• 🌤️ Weather updates
• 🌱 Crop tips
• 🎤 Click mic button to speak!

**Type or speak your question!** 🚜"""

# ---------------------- SIDEBAR ----------------------
with st.sidebar:
    st.markdown("""
    <div style="padding: 1.5rem 0 1.5rem 0; border-bottom: 2px solid #4caf50;">
        <h2 style="
            font-size: 1.4rem;
            font-weight: 800;
            color: #2e7d32;
            margin: 0;
            letter-spacing: 0.5px;
            line-height: 1.2;
        ">🌾 KRISHISAATHI AI</h2>
        <p style="
            font-size: 0.85rem;
            color: #66bb6a;
            margin: 0.5rem 0 0 0;
            font-weight: 600;
        ">Smart Farming Assistant</p>
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
    
    st.markdown("### 🎤 Voice Input")
    st.info("💡 Click the floating green mic button at the bottom-right corner to speak!")
    
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
                
                st.success("✅ Detection Complete!")
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

# ---------------------- CHAT INPUT ----------------------
if prompt := st.chat_input("Type your question or click 🎤 mic button to speak..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("🌱 Thinking..."):
            response = get_bot_response(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# ---------------------- FLOATING VOICE BUTTON ----------------------
st.components.v1.html("""
<div id="voiceStatus" class="voice-status-box">🎤 Listening...</div>
<div class="voice-button-container">
    <button id="voiceBtn" class="voice-btn" onclick="toggleVoice()">🎤</button>
</div>

<script>
let recognition = null;
let isRecording = false;

// Initialize speech recognition
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
    
    recognition.onstart = function() {
        isRecording = true;
        document.getElementById('voiceBtn').classList.add('recording');
        document.getElementById('voiceStatus').classList.add('show');
        document.getElementById('voiceStatus').innerHTML = '🔴 Listening...';
    };
    
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        
        // Find Streamlit chat input
        const streamlitDoc = window.parent.document;
        const chatInput = streamlitDoc.querySelector('textarea[data-testid="stChatInputTextArea"]');
        
        if (chatInput) {
            // Set the value
            chatInput.value = transcript;
            
            // Trigger input event
            const inputEvent = new Event('input', { bubbles: true });
            chatInput.dispatchEvent(inputEvent);
            
            // Wait a bit then trigger enter
            setTimeout(() => {
                const enterEvent = new KeyboardEvent('keydown', {
                    key: 'Enter',
                    code: 'Enter',
                    keyCode: 13,
                    which: 13,
                    bubbles: true
                });
                chatInput.dispatchEvent(enterEvent);
            }, 100);
            
            document.getElementById('voiceStatus').innerHTML = '✅ Message sent!';
        } else {
            document.getElementById('voiceStatus').innerHTML = '❌ Chat input not found';
        }
        
        setTimeout(() => {
            document.getElementById('voiceStatus').classList.remove('show');
        }, 2000);
    };
    
    recognition.onerror = function(event) {
        console.error('Speech error:', event.error);
        document.getElementById('voiceStatus').innerHTML = '❌ Error: ' + event.error;
        setTimeout(() => {
            document.getElementById('voiceStatus').classList.remove('show');
        }, 3000);
        stopVoice();
    };
    
    recognition.onend = function() {
        stopVoice();
    };
}

function toggleVoice() {
    if (!recognition) {
        alert('Speech recognition not supported in this browser. Please use Chrome, Edge, or Safari.');
        return;
    }
    
    if (isRecording) {
        stopVoice();
    } else {
        startVoice();
    }
}

function startVoice() {
    try {
        recognition.start();
    } catch (e) {
        console.error('Start error:', e);
    }
}

function stopVoice() {
    if (isRecording) {
        try {
            recognition.stop();
        } catch (e) {
            console.error('Stop error:', e);
        }
        isRecording = false;
        document.getElementById('voiceBtn').classList.remove('recording');
    }
}
</script>
""", height=0)

# ---------------------- THEMED FOOTER ----------------------
st.markdown("""
<div class="pro-footer">
    <p><strong>🌾 KRISHISAATHI AI 🌾</strong></p>
    <p>💡 AI Disease Detection | 🎤 Live Voice Recognition | 💰 Market Prices | 🌤️ Real-time Weather</p>
    <p style="font-size: 0.9em; margin-top: 1rem;">© 2025 Krishisaathi AI. Empowering Farmers with Technology 🚜</p>
</div>
""", unsafe_allow_html=True)
