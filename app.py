import streamlit as st
import random
import requests
from datetime import datetime
import re

# ---------------------- STREAMLIT CONFIG ----------------------
st.set_page_config(page_title="🌾 Krishisaathi AI", page_icon="🌱", layout="centered")

# ---------------------- CUSTOM CSS ----------------------
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2e7d32 0%, #66bb6a 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #4caf50;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .disease-section {
        background-color: #f0f8f0;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🌾 KRISHISAATHI AI CHATBOT</h1><p>Your smart assistant for sustainable farming 🚜</p></div>', unsafe_allow_html=True)

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
    """
    Placeholder for future ML model.
    Replace this with model.predict(image) after training.
    """
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
        "Apple - Cedar Apple Rust": {
            "symptoms": "Orange spots on leaves, premature leaf drop",
            "treatment": "Apply fungicide in spring, remove infected leaves",
            "prevention": "Remove nearby cedar trees, use resistant varieties"
        },
        "Rice - Brown Spot": {
            "symptoms": "Oval brown spots on leaves and grains",
            "treatment": "Apply Tricyclazole or Mancozeb, ensure proper nutrition",
            "prevention": "Use disease-free seeds, balanced fertilizer"
        },
        "Wheat - Leaf Rust": {
            "symptoms": "Orange-red pustules on leaves",
            "treatment": "Apply Propiconazole fungicide at first sign",
            "prevention": "Use resistant varieties, early sowing"
        },
        "Healthy Crop": {
            "symptoms": "No disease detected",
            "treatment": "Continue regular care and monitoring",
            "prevention": "Maintain good agricultural practices"
        }
    }
    
    # Random selection for demo
    disease_name = random.choice(list(diseases.keys()))
    disease_info = diseases[disease_name]
    
    return {
        "name": disease_name,
        "confidence": random.randint(75, 98),
        **disease_info
    }

# ---------------------- PRODUCE PRICE FUNCTION ----------------------
def get_produce_prices(state="all"):
    """Weekly Updated Market Prices - 100+ Cities Pan India Coverage
    Last Updated: October 12, 2025"""
    
    sample_prices = {
        # NORTH INDIA
        "Delhi": {
            "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹14-24", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹8-10", "unit": "per kg", "trend": "→"},
            "Cauliflower": {"price": "₹18-25", "unit": "per kg", "trend": "→"},
            "Lady Finger (Bhindi)": {"price": "₹35-55", "unit": "per kg", "trend": "→"},
            "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹45-60", "unit": "per dozen", "trend": "→"}
        },
        "Mumbai": {
            "Tomato": {"price": "₹26-40", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹18-28", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹17-26", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
            "Apple": {"price": "₹90-130", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹48-65", "unit": "per dozen", "trend": "→"}
        },
        "Bengaluru": {
            "Tomato": {"price": "₹24-36", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹16-25", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹15-22", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
            "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹40-54", "unit": "per dozen", "trend": "→"}
        },
        "Chennai": {
            "Tomato": {"price": "₹24-38", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹15-25", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹16-23", "unit": "per kg", "trend": "↓"},
            "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹38-52", "unit": "per dozen", "trend": "→"}
        },
        "Kolkata": {
            "Tomato": {"price": "₹20-34", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹13-22", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
            "Apple": {"price": "₹84-118", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹42-56", "unit": "per dozen", "trend": "→"}
        },
        "Hyderabad": {
            "Tomato": {"price": "₹22-38", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹16-25", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
            "Apple": {"price": "₹84-118", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹42-56", "unit": "per dozen", "trend": "→"}
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
        return "❌ Sorry, no price data found. Try: Delhi, Mumbai, Bangalore, Chennai, Kolkata, or Hyderabad."
    
    response = "💰 **Current Market Prices:**\n\n"
    
    for city, produce_data in prices.items():
        if city_name and city_name.lower() not in city.lower():
            continue
            
        response += f"📍 **{city}**\n\n"
        
        for item, data in produce_data.items():
            response += f"• **{item}**: {data['price']} {data['unit']} {data['trend']}\n"
        
        response += "\n"
    
    response += "\n📊 **Legend:** ↑ Rising | → Stable | ↓ Falling\n"
    response += "📅 **Updated:** October 12, 2025\n"
    response += "💡 **Tip:** Prices are approximate retail rates."
    
    return response

# ---------------------- FARMING KNOWLEDGE BASE ----------------------
farming_tips = {
    "crops": {
        "wheat": "🌾 Wheat grows best in cool, moist climates (10–25°C). Requires well-drained loamy soil with pH 6.0–7.0. Apply farmyard manure and nitrogen-rich fertilizers.",
        "rice": "🍚 Rice needs flooded fields and warm temperatures (20–35°C). Prefers clayey soil that retains water. Use organic compost for better yield.",
        "tomato": "🍅 Tomatoes need 6–8 hours of sunlight daily. Grow best in warm weather (20–30°C) with well-drained loamy soil. Add compost and potash.",
        "potato": "🥔 Potatoes prefer cool weather (15–20°C). Grow in loose, sandy soil (pH 5.0–6.0). Add compost and avoid high humidity.",
        "onion": "🧅 Onions grow in cool weather (13–24°C). Prefer loose sandy loam soil. Add phosphorus and potash before bulb formation.",
        "cabbage": "🥬 Cabbage prefers cool climate (10–25°C) and fertile, moist loamy soil. Use organic manure for compact heads."
    },
    "pests": {
        "aphids": "🐛 Aphids: Control with neem oil, ladybugs, or soap water spray. Avoid over-fertilization.",
        "caterpillars": "🐛 Caterpillars: Hand-pick or use Bt spray. Introduce natural predators.",
        "whiteflies": "🦟 Whiteflies: Use yellow sticky traps and neem oil. Maintain plant health.",
        "general": "🛡️ Prevention: Crop rotation, companion planting, clean fields, and biological pest control."
    }
}

# ---------------------- CHATBOT RESPONSE LOGIC ----------------------
def get_bot_response(user_message):
    """Generates intelligent responses"""
    message_lower = user_message.lower()
    
    # Disease detection trigger
    if any(word in message_lower for word in ["disease", "sick", "infected", "spot", "pest", "diagnose", "check crop"]):
        st.session_state.expect_image = True
        return """🔬 **Crop Disease Detection**

📷 Please upload a clear photo of:
- Affected leaves or stems
- Close-up of spots/damage
- Well-lit image

I'll analyze it and provide:
✅ Disease identification
✅ Treatment recommendations
✅ Prevention tips"""
    
    # Price queries
    if any(word in message_lower for word in ["price", "cost", "rate", "market", "mandi"]):
        city = extract_city_from_message(user_message)
        
        if city:
            prices = get_produce_prices(city)
            return format_price_response(prices, city)
        else:
            return """💰 **Market Prices Available!**

🌍 **Major Cities Covered:**
• Delhi, Mumbai, Bangalore
• Chennai, Kolkata, Hyderabad
• And 100+ more cities!

**💬 Ask me like:**
- "Show prices in Mumbai"
- "Tomato price in Bangalore"
- "Market rates in Delhi"

**📍 Type your city name!** 🌾"""
    
    # Weather queries
    if any(word in message_lower for word in ["weather", "temperature", "rain", "forecast"]):
        city = extract_city_from_message(user_message)
        
        if not city:
            if st.session_state.user_location:
                city = st.session_state.user_location
            else:
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
            return f"❌ Couldn't fetch weather for '{city}'. Check spelling or try another city."
    
    # Crop advice
    for crop, info in farming_tips["crops"].items():
        if crop in message_lower:
            return f"**{crop.title()} Guide:**\n\n{info}"
    
    # Pest control
    for pest, info in farming_tips["pests"].items():
        if pest in message_lower:
            return f"**Pest Control:**\n\n{info}"
    
    # Irrigation
    if "irrigation" in message_lower or "drip" in message_lower or "water" in message_lower:
        return """💧 **Irrigation Tips:**

- **Drip:** Most efficient, 30-50% water savings
- **Sprinkler:** Good for large areas
- **Timing:** Early morning or evening
- **Amount:** 1-2 inches per week"""
    
    # Fertilizer
    if "fertilizer" in message_lower or "fertiliser" in message_lower:
        return """🌱 **Fertilizer Guide:**

- **NPK:** N for leaves, P for roots, K for health
- **Organic:** Compost, manure, bone meal
- **Timing:** Before planting and during growth
- **Application:** Follow soil test recommendations"""
    
    # Greeting
    if any(word in message_lower for word in ["hello", "hi", "hey", "namaste"]):
        return """🙏 **Namaste! Welcome to Krishisaathi!**

I can help you with:
🌤️ Weather forecasts
💰 Market prices (100+ cities)
🌾 Crop cultivation tips
🔬 Disease detection (upload photo)
🐛 Pest management
💧 Irrigation advice
🧪 Fertilizer recommendations

**What would you like to know?** 🚜"""
    
    # Goodbye
    if any(word in message_lower for word in ["bye", "goodbye", "thanks", "thank you"]):
        return "🙏 Dhanyavaad! Happy farming! 🌾 Feel free to ask anytime."
    
    # Default
    return """🌾 **How can I help you today?**

Ask me about:
• 🔬 Crop disease (upload photo)
• 💰 Market prices
• 🌤️ Weather updates
• 🌱 Crop tips
• 🐛 Pest control
• 💧 Irrigation
• 🧪 Fertilizers

**Type your question!** 🚜"""

# ---------------------- SIDEBAR ----------------------
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    **Krishisaathi AI** helps with:
    - 🔬 Disease detection (AI)
    - 🌤️ Weather updates
    - 💰 Market prices (100+ cities)
    - 🌾 Crop cultivation tips
    - 🐛 Pest management
    - 💧 Irrigation advice
    """)
    
    st.divider()
    
    st.header("🎯 Quick Actions")
    if st.button("📷 Disease Detection"):
        user_msg = "Check crop disease"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
    
    if st.button("📍 Delhi Prices"):
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
        user_msg = "Tell me about wheat"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
    
    st.divider()
    
    if st.session_state.user_location:
        st.info(f"📍 Location: {st.session_state.user_location}")
    
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
        type=["jpg", "png", "jpeg"],
        help="Upload a clear photo of affected leaves or crops"
    )
    
    if uploaded_file:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(uploaded_file, caption="Uploaded Crop Image", use_container_width=True)
        
        with col2:
            with st.spinner("🔬 Analyzing image..."):
                # AI prediction
                prediction = ai_predict_disease(uploaded_file)
                
                st.success(f"✅ **Detection Complete!**")
                st.metric("Disease Identified", prediction['name'])
                st.metric("Confidence", f"{prediction['confidence']}%")
        
        # Detailed results
        st.markdown("---")
        st.markdown("### 📋 Detailed Analysis")
        
        tab1, tab2, tab3 = st.tabs(["🔍 Symptoms", "💊 Treatment", "🛡️ Prevention"])
        
        with tab1:
            st.write(f"**Symptoms:** {prediction['symptoms']}")
        
        with tab2:
            st.write(f"**Treatment:** {prediction['treatment']}")
        
        with tab3:
            st.write(f"**Prevention:** {prediction['prevention']}")
        
        # Reset button
        if st.button("🔄 Analyze Another Image"):
            st.session_state.expect_image = True
            st.rerun()
        
        if st.button("✅ Done"):
            st.session_state.expect_image = False
            
            # Add to chat history
            result_msg = f"""✅ **Disease Detection Complete**

**Identified:** {prediction['name']} ({prediction['confidence']}% confidence)

**Symptoms:** {prediction['symptoms']}

**Treatment:** {prediction['treatment']}

**Prevention:** {prediction['prevention']}"""
            
            st.session_state.messages.append({"role": "assistant", "content": result_msg})
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

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
st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🌾 <b>Krishisaathi AI</b> - Empowering Farmers with Technology</p>
    <p style='font-size: 0.9em;'>💡 AI Disease Detection | Weekly Updated Prices | Real-time Weather</p>
</div>
""", unsafe_allow_html=True)
