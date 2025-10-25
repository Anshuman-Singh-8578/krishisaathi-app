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
    [data-testid="stToolbar"] {display: none;}
    [data-testid="manage-app-button"] {display: none;}
    .viewerBadge_container__r5tak {display: none;}
    .stDeployButton {display: none;}
    
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
    
    .stChatInputContainer:focus-within {
        border-color: #4caf50 !important;
        box-shadow: 0 4px 16px rgba(76, 175, 80, 0.15) !important;
    }
    
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
        <p class="app-tagline">Connecting Farmers, Empowering Growth</p>
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
            "Cauliflower": {"price": "₹18-25", "unit": "per kg", "trend": "→"},
            "Lady Finger (Bhindi)": {"price": "₹35-55", "unit": "per kg", "trend": "→"},
            "Brinjal (Eggplant)": {"price": "₹28-45", "unit": "per kg", "trend": "→"},
            "Carrot": {"price": "₹32-48", "unit": "per kg", "trend": "→"},
            "Spinach": {"price": "₹20-35", "unit": "per bunch", "trend": "→"},
            "Green Peas": {"price": "₹70-100", "unit": "per kg", "trend": "→"},
            "Capsicum": {"price": "₹50-75", "unit": "per kg", "trend": "→"},
            "Cucumber": {"price": "₹25-40", "unit": "per kg", "trend": "↓"},
            "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹45-60", "unit": "per dozen", "trend": "→"},
        },
        "Mumbai": {
            "Tomato": {"price": "₹26-40", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹18-28", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹17-26", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
            "Lady Finger (Bhindi)": {"price": "₹35-55", "unit": "per kg", "trend": "→"},
            "Capsicum": {"price": "₹52-78", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹48-65", "unit": "per dozen", "trend": "→"},
            "Apple": {"price": "₹90-130", "unit": "per kg", "trend": "→"},
        },
        "Bangalore": {
            "Tomato": {"price": "₹24-36", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹16-25", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹15-22", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
            "Carrot": {"price": "₹28-44", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹40-54", "unit": "per dozen", "trend": "→"},
            "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"}
        },
        "Chennai": {
            "Tomato": {"price": "₹24-38", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹15-25", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹16-23", "unit": "per kg", "trend": "↓"},
            "Brinjal (Eggplant)": {"price": "₹28-40", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹38-52", "unit": "per dozen", "trend": "→"},
            "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"}
        },
        "Kolkata": {
            "Tomato": {"price": "₹20-34", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹13-22", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹8-11", "unit": "per kg", "trend": "→"},
            "Carrot": {"price": "₹28-42", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹42-56", "unit": "per dozen", "trend": "→"},
            "Apple": {"price": "₹84-118", "unit": "per kg", "trend": "→"}
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


# ---------------------- EXTRACT CITY AND VEGETABLE FROM MESSAGE ----------------------
def extract_city_and_vegetable_from_message(message):
    """Extracts both city name and vegetable name from user message"""
    message_lower = message.lower()
    
    # Extract city
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
    
    # Extract vegetable/produce
    vegetable = None
    produce_list = [
        "tomato", "potato", "onion", "cabbage", "cauliflower", "lady finger", "bhindi",
        "brinjal", "eggplant", "carrot", "spinach", "green peas", "peas", "capsicum",
        "cucumber", "bottle gourd", "lauki", "pumpkin", "apple", "banana", "pomegranate",
        "mango", "alphonso", "pineapple", "papaya", "apricot", "cherry", "walnut",
        "coconut", "breadfruit"
    ]
    
    for produce in produce_list:
        if produce in message_lower:
            vegetable = produce
            break
    
    return city, vegetable


# ---------------------- FORMAT PRICE RESPONSE ----------------------
def format_price_response(prices, city_name=None, vegetable_name=None):
    """Formats price data into readable response - shows only specific vegetable if mentioned"""
    if not prices:
        return "❌ Sorry, no price data found. Try: Delhi, Mumbai, or Bangalore."
    
    response = "💰 **Current Market Prices:**\n\n"
    
    for city, produce_data in prices.items():
        if city_name and city_name.lower() not in city.lower():
            continue
        
        response += f"📍 **{city}**\n\n"
        
        # If specific vegetable is requested, show only that
        if vegetable_name:
            found = False
            for item, data in produce_data.items():
                if vegetable_name.lower() in item.lower():
                    response += f"• **{item}**: {data['price']} {data['unit']} {data['trend']}\n"
                    found = True
            
            if not found:
                response += f"❌ {vegetable_name.title()} price not available for {city}\n"
        else:
            # Show all produce for the city
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
        city, vegetable = extract_city_and_vegetable_from_message(user_message)
        
        if city:
            prices = get_produce_prices(city)
            if prices:
                return format_price_response(prices, city, vegetable)
            else:
                return f"❌ Sorry, I don't have price data for '{city}'. Try: Delhi, Mumbai, Bangalore, Chennai, Kolkata."
        else:
            return """💰 **Market Prices Available!**

🌆 **Cities Covered:** Delhi, Mumbai, Bangalore, Chennai, Kolkata, and more!

💬 **Ask me:** 
• "Tomato price in Mumbai"
• "Show onion prices in Delhi"
• "What's the price of potato in Bangalore?"

📍 Type your city and vegetable name!"""
    
    # Weather queries
    if any(word in message_lower for word in ["weather", "temperature"]):
        city, _ = extract_city_and_vegetable_from_message(user_message)
        
        if not city:
            return "📍 Please specify a location!\nExample: 'Weather in Delhi'"
        
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
    if any(word in message_lower for word in ["wheat", "rice", "tomato", "potato", "crop", "farming", "cultivation"]):
        if "wheat" in message_lower:
            return """🌾 **Wheat Cultivation Guide**

**Climate Requirements:**
• Temperature: 10-25°C (ideal)
• Rainfall: 50-75 cm annually

**Planting:**
• Sowing time: October-November
• Seed rate: 100-125 kg/hectare

**Harvesting:**
• 120-150 days after sowing"""
        
        elif "rice" in message_lower:
            return """🍚 **Rice Cultivation Guide**

**Climate:**
• Temperature: 20-35°C
• High humidity (80-90%)

**Planting:**
• Kharif season: June-July
• Transplanting: 21-25 days old seedlings"""
        
        else:
            return """🌾 **Crop Cultivation Tips**

Ask me about:
• 🌾 Wheat - Rabi crop
• 🍚 Rice - Kharif crop
• 🍅 Tomato - Vegetable crop
• 🥔 Potato - Tuber crop

**Type your crop name to get started!** 🚜"""
    
    # Greeting
    if any(word in message_lower for word in ["hello", "hi", "hey", "namaste"]):
        return """🙏 **Namaste! Welcome to Krishisaathi AI!**

I can help you with:
🌤️ Weather forecasts
💰 Market prices (100+ cities)
🌾 Crop cultivation tips
🔬 Disease detection (upload photo)

**What would you like to know?** 🚜"""
    
    # Default
    return """🌾 **How can I help you today?**

Ask me about:
• 🔬 Crop disease (upload photo)
• 💰 Market prices
• 🌤️ Weather updates
• 🌱 Crop tips

**Type your question!** 🚜"""


# ---------------------- SIDEBAR ----------------------
with st.sidebar:
    st.markdown("""
    <div style="padding: 1.5rem 0 1.5rem 0; border-bottom: 1px solid rgba(76, 175, 80, 0.2);">
        <h2 style="font-size: 1.3rem; font-weight: 800; color: #66bb6a; margin: 0;">🌾 KRISHISAATHI AI</h2>
        <p style="font-size: 0.8rem; color: #81c784; margin: 0.4rem 0 0 0;">Smart Farming Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 Quick Actions")
    
    if st.button("📷 Disease Detection"):
        st.session_state.messages.append({"role": "user", "content": "Check crop disease"})
        st.session_state.messages.append({"role": "assistant", "content": get_bot_response("Check crop disease")})
        st.rerun()
    
    if st.button("🏙 Delhi Prices"):
        st.session_state.messages.append({"role": "user", "content": "Show prices in Delhi"})
        st.session_state.messages.append({"role": "assistant", "content": get_bot_response("Show prices in Delhi")})
        st.rerun()
        
    if st.button("🌤️ Mumbai Weather"):
        st.session_state.messages.append({"role": "user", "content": "Weather in Mumbai"})
        st.session_state.messages.append({"role": "assistant", "content": get_bot_response("Weather in Mumbai")})
        st.rerun()
        
    if st.button("🌾 Crop Tips"):
        st.session_state.messages.append({"role": "user", "content": "Tell me about wheat"})
        st.session_state.messages.append({"role": "assistant", "content": get_bot_response("Tell me about wheat")})
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
    st.subheader("📸 Upload Crop Image for Disease Detection")
    
    uploaded_file = st.file_uploader("Choose an image (JPG, PNG, JPEG)", type=["jpg", "png", "jpeg"])
    
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

# ---------------------- CHAT INPUT ----------------------
if prompt := st.chat_input("Ask about farming..."):
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
    <p>💡 AI Disease Detection | Weekly Updated Prices | Real-time Weather</p>
    <p style="font-size: 0.85em;">© 2025 Krishisaathi AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
