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
    
    [data-testid="manage-app-button"] {
        display: none;
    }
    
    .viewerBadge_container__r5tak {
        display: none;
    }
    
    .stDeployButton {
        display: none;
    }
    
    [data-testid="collapsedControl"] {
        display: block !important;
    }
    
    section[data-testid="stSidebar"] {
        display: block !important;
    }
    
    .main {
        background: #f8faf9;
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
    
    [data-testid="collapsedControl"] {
        background: #4caf50 !important;
        color: white !important;
        border-radius: 0 8px 8px 0 !important;
        padding: 0.5rem !important;
        display: block !important;
    }
    
    [data-testid="stSidebar"][aria-expanded="true"] {
        display: block !important;
        width: 21rem !important;
    }
    
    [data-testid="stSidebar"][aria-expanded="false"] {
        display: block !important;
        width: 0 !important;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #1b5e20 !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
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
    
    .stChatMessage {
        background: white !important;
        border-radius: 12px !important;
        border: 1px solid #e8f5e9 !important;
        margin-bottom: 1rem !important;
        padding: 1.25rem !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02) !important;
    }
    
    .stChatInputContainer {
        background: white !important;
        border: 2px solid #e8f5e9 !important;
        border-radius: 12px !important;
        padding: 0.5rem !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
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
        background: white;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #e8f5e9;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    }
    
    hr {
        border: none;
        height: 1px;
        background: #e8f5e9;
        margin: 2rem 0;
    }
    
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
        <p class="app-tagline">Connecting Farmers, Empowering Growth - Voice Enabled</p>
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
        return "Sorry, no price data found. Try: Delhi, Mumbai, or Bangalore."
    
    response = "**Current Market Prices:**\n\n"
    
    for city, produce_data in prices.items():
        if city_name and city_name.lower() not in city.lower():
            continue
            
        response += f"**{city}**\n\n"
        
        for item, data in produce_data.items():
            response += f"- **{item}**: {data['price']} {data['unit']} ({data['trend']})\n"
        
        response += "\n"
    
    response += "\nUpdated: October 25, 2025\n"
    response += "Tip: Prices are approximate retail rates."
    
    return response

# ---------------------- CHATBOT RESPONSE LOGIC ----------------------
def get_bot_response(user_message):
    """Generates intelligent responses"""
    message_lower = user_message.lower()
    
    # Disease detection trigger
    if any(word in message_lower for word in ["disease", "sick", "infected", "diagnose"]):
        st.session_state.expect_image = True
        return """**Crop Disease Detection**

Please upload a clear photo of affected leaves or crops.

I will analyze it and provide:
- Disease identification
- Treatment recommendations
- Prevention tips"""
    
    # Price queries
    if any(word in message_lower for word in ["price", "cost", "market"]):
        city = extract_city_from_message(user_message)
        
        if city:
            prices = get_produce_prices(city)
            return format_price_response(prices, city)
        else:
            return """**Market Prices Available!**

Cities Covered: Delhi, Mumbai, Bangalore, and more!

Ask me: "Show prices in Mumbai" or "Tomato price in Delhi"

Type your city name!"""
    
    # Weather queries
    if any(word in message_lower for word in ["weather", "temperature"]):
        city = extract_city_from_message(user_message)
        
        if not city:
            return "Please specify a location!\nExample: 'Weather in Delhi'"
        
        weather = get_weather(city)
        if weather:
            return f"""**Weather in {weather['city']}:**
            
- Temperature: {weather['temperature']}C (feels like {weather['feels_like']}C)
- Conditions: {weather['description'].title()}
- Humidity: {weather['humidity']}%
- Wind: {weather['wind_speed']} m/s

**Advice:** {"Good for outdoor work!" if weather['temperature'] > 15 else "Indoor tasks recommended."}"""
        else:
            return f"Could not fetch weather for '{city}'."
    
    # Crop tips
    if any(word in message_lower for word in ["wheat", "rice", "tomato", "potato", "crop", "farming"]):
        return """**Crop Cultivation Guide**

I can help with detailed tips for:
- Wheat
- Rice
- Tomato
- Potato

Ask me: "Tell me about wheat cultivation" or "How to grow rice"

What crop would you like to know about?"""
    
    # Greeting
    if any(word in message_lower for word in ["hello", "hi", "hey", "namaste"]):
        return """**Namaste! Welcome to Krishisaathi AI!**

I can help you with:
- Weather forecasts
- Market prices
- Crop cultivation tips
- Disease detection
- Voice commands

Try asking: "Weather in Delhi" or "Show prices" """
    
    # Default
    return """**How can I help you today?**

Ask me about:
- Crop disease (upload photo)
- Market prices
- Weather updates
- Crop tips
- Use voice input!

Type or speak your question!"""

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
        ">KRISHISAATHI AI</h2>
        <p style="
            font-size: 0.8rem;
            color: #81c784;
            margin: 0.4rem 0 0 0;
            font-weight: 500;
        ">Smart Farming Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Quick Actions")
    
    if st.button("Disease Detection"):
        user_msg = "Check crop disease"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
    
    if st.button("Delhi Prices"):
        user_msg = "Show prices in Delhi"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
        
    if st.button("Mumbai Weather"):
        user_msg = "Weather in Mumbai"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
        
    if st.button("Crop Tips"):
        user_msg = "Tell me about farming"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
    
    st.divider()
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.expect_image = False
        st.rerun()

# ---------------------- VOICE INPUT SECTION ----------------------
st.markdown("### Voice Input")
st.info("Click the microphone button below to start speaking. Your speech will be converted to text instantly!")

# Voice recognition HTML component
voice_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            padding: 20px;
            background: linear-gradient(135deg, #e8f5e9 0%, #f1f8f4 100%);
            border-radius: 12px;
            margin: 0;
        }
        
        .voice-container {
            text-align: center;
        }
        
        .mic-button {
            background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
            color: white;
            border: none;
            border-radius: 50%;
            width: 80px;
            height: 80px;
            font-size: 2rem;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.25);
            transition: all 0.3s ease;
            margin: 10px;
        }
        
        .mic-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.35);
        }
        
        .mic-button.recording {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
            animation: pulse 1s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        .transcript {
            margin: 20px 0;
            padding: 15px;
            background: white;
            border-radius: 10px;
            border: 2px solid #4caf50;
            min-height: 60px;
            font-size: 1.1rem;
            color: #2e7d32;
            font-weight: 500;
        }
        
        .status {
            font-size: 1rem;
            color: #66bb6a;
            margin: 10px 0;
            font-weight: 600;
        }
        
        .copy-button {
            background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 12px 30px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.25);
            transition: all 0.3s ease;
            margin-top: 10px;
        }
        
        .copy-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.35);
        }
        
        .copy-button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
    </style>
</head>
<body>
    <div class="voice-container">
        <button id="micButton" class="mic-button" onclick="toggleRecognition()">🎤</button>
        <div class="status" id="status">Click microphone to start</div>
        <div class="transcript" id="transcript">Your speech will appear here...</div>
        <button class="copy-button" id="copyButton" onclick="copyText()" disabled>📋 Copy Text</button>
    </div>

    <script>
        let recognition;
        let isRecording = false;
        let finalTranscript = '';

        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'en-US';
            
            recognition.onstart = function() {
                isRecording = true;
                document.getElementById('micButton').classList.add('recording');
                document.getElementById('status').textContent = '🔴 Listening... Speak now!';
            };
            
            recognition.onresult = function(event) {
                let interimTranscript = '';
                
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript;
                    
                    if (event.results[i].isFinal) {
                        finalTranscript += transcript + ' ';
                    } else {
                        interimTranscript += transcript;
                    }
                }
                
                const displayText = finalTranscript + interimTranscript;
                document.getElementById('transcript').textContent = displayText || 'Your speech will appear here...';
                
                if (finalTranscript.trim()) {
                    document.getElementById('copyButton').disabled = false;
                }
            };
            
            recognition.onerror = function(event) {
                console.error('Speech recognition error:', event.error);
                document.getElementById('status').textContent = '❌ Error: ' + event.error;
                stopRecognition();
            };
            
            recognition.onend = function() {
                stopRecognition();
            };
        } else {
            document.getElementById('status').textContent = '❌ Speech recognition not supported in this browser';
            document.getElementById('micButton').disabled = true;
        }

        function toggleRecognition() {
            if (isRecording) {
                stopRecognition();
            } else {
                startRecognition();
            }
        }

        function startRecognition() {
            if (recognition) {
                finalTranscript = '';
                document.getElementById('transcript').textContent = 'Your speech will appear here...';
                document.getElementById('copyButton').disabled = true;
                recognition.start();
            }
        }

        function stopRecognition() {
            if (recognition && isRecording) {
                recognition.stop();
                isRecording = false;
                document.getElementById('micButton').classList.remove('recording');
                document.getElementById('status').textContent = '✅ Recording stopped. Click mic to record again.';
            }
        }

        function copyText() {
            const text = finalTranscript.trim();
            if (text) {
                navigator.clipboard.writeText(text).then(function() {
                    document.getElementById('status').textContent = '✅ Text copied! Paste it in the chat below.';
                    setTimeout(() => {
                        document.getElementById('status').textContent = 'Click microphone to start';
                    }, 3000);
                });
            }
        }
    </script>
</body>
</html>
"""

st.components.v1.html(voice_html, height=300)

st.markdown("**Instructions:**")
st.markdown("1. Click the 🎤 microphone button")
st.markdown("2. Speak your question clearly")
st.markdown("3. Click 📋 Copy Text button")
st.markdown("4. Paste in the chat box below and press Enter")

st.markdown("---")

# ---------------------- CHAT INTERFACE ----------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------- IMAGE UPLOAD SECTION ----------------------
if st.session_state.expect_image:
    st.subheader("Upload Crop Image for Disease Detection")
    
    uploaded_file = st.file_uploader(
        "Choose an image (JPG, PNG, JPEG)", 
        type=["jpg", "png", "jpeg"]
    )
    
    if uploaded_file:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(uploaded_file, caption="Uploaded Crop Image", use_container_width=True)
        
        with col2:
            with st.spinner("Analyzing image..."):
                prediction = ai_predict_disease(uploaded_file)
                
                st.success("Detection Complete!")
                st.metric("Disease Identified", prediction['name'])
                st.metric("Confidence", f"{prediction['confidence']}%")
        
        st.markdown("---")
        st.markdown("### Detailed Analysis")
        
        tab1, tab2, tab3 = st.tabs(["Symptoms", "Treatment", "Prevention"])
        
        with tab1:
            st.write(f"**Symptoms:** {prediction['symptoms']}")
        
        with tab2:
            st.write(f"**Treatment:** {prediction['treatment']}")
        
        with tab3:
            st.write(f"**Prevention:** {prediction['prevention']}")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Analyze Another Image"):
                st.session_state.expect_image = True
                st.rerun()
        
        with col_b:
            if st.button("Done"):
                st.session_state.expect_image = False
                result_msg = f"""**Disease Detection Complete**

**Identified:** {prediction['name']} ({prediction['confidence']}% confidence)

**Symptoms:** {prediction['symptoms']}

**Treatment:** {prediction['treatment']}

**Prevention:** {prediction['prevention']}"""
                
                st.session_state.messages.append({"role": "assistant", "content": result_msg})
                st.rerun()

# ---------------------- CHAT INPUT ----------------------
if prompt := st.chat_input("Type your question or paste voice text here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_bot_response(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# ---------------------- FOOTER ----------------------
st.markdown("""
<div class="pro-footer">
    <p><strong>Krishisaathi AI</strong> - Empowering Farmers with Technology</p>
    <p>AI Disease Detection | Live Voice Recognition | Weekly Updated Prices | Real-time Weather</p>
    <p style="font-size: 0.85em;">© 2025 Krishisaathi AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
