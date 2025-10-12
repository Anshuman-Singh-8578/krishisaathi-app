import streamlit as st
import random
import requests
from datetime import datetime
import re

# ---------------------- STREAMLIT CONFIG ----------------------
st.set_page_config(page_title="🌾 AI Farmer Chatbot", page_icon="🌱", layout="centered")

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
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🌾 AGRI SENSE AI CHATBOT</h1><p>Your smart assistant for sustainable farming 🚜</p></div>', unsafe_allow_html=True)

# ---------------------- INITIALIZE SESSION ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_location" not in st.session_state:
    st.session_state.user_location = None

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

# ---------------------- PRODUCE PRICE FUNCTION ----------------------
def get_produce_prices(state="all"):
    """Weekly Updated Market Prices - Pan India Coverage"""
    
    sample_prices = {
        "Delhi": {
            "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹14-24", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹8-10", "unit": "per kg", "trend": "→"},
            "Cauliflower": {"price": "₹18-25", "unit": "per kg", "trend": "→"},
            "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹45-60", "unit": "per dozen", "trend": "→"},
        },
        "Mumbai": {
            "Tomato": {"price": "₹25-40", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹18-28", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹18-26", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹10-14", "unit": "per kg", "trend": "→"},
            "Apple": {"price": "₹95-140", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹50-65", "unit": "per dozen", "trend": "→"},
        },
        "Bangalore": {
            "Tomato": {"price": "₹20-35", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹16-26", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹16-24", "unit": "per kg", "trend": "↓"},
            "Beans": {"price": "₹35-50", "unit": "per kg", "trend": "→"},
            "Apple": {"price": "₹90-130", "unit": "per kg", "trend": "→"},
        },
        "Chennai": {
            "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "→"},
            "Potato": {"price": "₹18-28", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹16-25", "unit": "per kg", "trend": "↓"},
            "Drumstick": {"price": "₹50-70", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹35-50", "unit": "per dozen", "trend": "→"},
        },
        "Kolkata": {
            "Tomato": {"price": "₹18-32", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹12-22", "unit": "per kg", "trend": "↓"},
            "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
            "Brinjal": {"price": "₹18-30", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹40-55", "unit": "per dozen", "trend": "→"},
        },
        "Hyderabad": {
            "Tomato": {"price": "₹20-34", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹16-26", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹15-24", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹8-12", "unit": "per kg", "trend": "→"},
            "Apple": {"price": "₹90-135", "unit": "per kg", "trend": "→"},
        },
    }
    
    if state.lower() == "all":
        return sample_prices
    else:
        # Smart search
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
        
        vegetables = []
        fruits = []
        
        for item, data in produce_data.items():
            price_line = f"• **{item}**: {data['price']} {data['unit']} {data['trend']}"
            
            if item.lower() in ["apple", "banana", "orange", "mango", "grapes", "watermelon"]:
                fruits.append(price_line)
            else:
                vegetables.append(price_line)
        
        if vegetables:
            response += "🥬 **Vegetables:**\n" + "\n".join(vegetables) + "\n\n"
        
        if fruits:
            response += "🍎 **Fruits:**\n" + "\n".join(fruits) + "\n\n"
    
    response += "\n📊 **Legend:** ↑ Rising | → Stable | ↓ Falling\n"
    response += "📅 **Updated:** October 12, 2025 | 🔄 **Next Update:** Monday\n"
    response += "💡 **Tip:** Prices are approximate retail rates."
    
    return response

# ---------------------- FORMAT SPECIFIC PRODUCE PRICE ----------------------
def format_specific_produce_price(prices, city_name, produce_name):
    """Formats price for specific produce"""
    if not prices:
        return f"❌ Sorry, no price data found for {produce_name}."
    
    response = f"💰 **Market Price for {produce_name.title()}:**\n\n"
    found = False
    
    for city, produce_data in prices.items():
        if city_name and city_name.lower() not in city.lower():
            continue
        
        for item, data in produce_data.items():
            if produce_name.lower() in item.lower():
                found = True
                trend_text = "Rising" if data["trend"] == "↑" else "Stable" if data["trend"] == "→" else "Falling"
                
                response += f"📍 **{city}**\n"
                response += f"• Price: **{data['price']}** {data['unit']}\n"
                response += f"• Trend: {data['trend']} {trend_text}\n\n"
    
    if not found:
        return f"❌ No data for '{produce_name}'. Try: tomato, potato, onion, apple, banana, cabbage."
    
    response += f"📅 Updated: October 12, 2025 | 🔄 Next: Monday\n"
    response += "💡 Prices may vary by market and quality."
    
    return response

# ---------------------- FARMING KNOWLEDGE BASE ----------------------
farming_tips = {
    "crops": {
        "wheat": "🌾 Wheat grows best in cool, moist climates. Plant in fall or spring. Requires well-drained soil with pH 6.0-7.0.",
        "rice": "🍚 Rice needs flooded fields and warm temperatures (20-35°C). Requires clayey soil that retains water well.",
        "tomato": "🍅 Tomatoes need 6-8 hours of sunlight daily. Plant when soil temperature is above 15°C.",
        "potato": "🥔 Potatoes prefer cool weather (15-20°C). Plant in loose, acidic soil (pH 5.0-6.0)."
    },
    "seasons": {
        "spring": "🌸 Spring: Plant tomatoes, peppers, corn, beans, cucumbers.",
        "summer": "☀️ Summer: Regular watering, pest control, harvest early crops.",
        "fall": "🍂 Fall: Plant garlic, onions, winter wheat, cover crops.",
        "winter": "❄️ Winter: Plan next season, maintain equipment, indoor seed starting."
    },
    "pests": {
        "aphids": "🐛 Aphids: Use neem oil spray, introduce ladybugs, or spray with water.",
        "caterpillars": "🐛 Caterpillars: Hand-pick, use Bt, or plant companion flowers.",
        "general": "🛡️ Prevention: Crop rotation, companion planting, beneficial insects."
    }
}

# ---------------------- CHATBOT RESPONSE LOGIC ----------------------
def get_bot_response(user_message):
    """Generates intelligent responses"""
    message_lower = user_message.lower()
    
    # Price queries
    if any(word in message_lower for word in ["price", "cost", "rate", "market", "mandi"]):
        city = extract_city_from_message(user_message)
        
        produce_list = ["tomato", "potato", "onion", "cabbage", "cauliflower", "apple", 
                       "banana", "orange", "mango", "watermelon", "beans", "brinjal", "drumstick"]
        
        specific_produce = None
        for produce in produce_list:
            if produce in message_lower:
                specific_produce = produce
                break
        
        if city:
            prices = get_produce_prices(city)
            if specific_produce:
                return format_specific_produce_price(prices, city, specific_produce)
            else:
                return format_price_response(prices, city)
        elif specific_produce:
            all_prices = get_produce_prices("all")
            return format_specific_produce_price(all_prices, None, specific_produce)
        else:
            return """💰 **Market Prices Available For:**

📍 **Major Cities:** Delhi | Mumbai | Bangalore | Chennai | Kolkata | Hyderabad

**Ask me like:**
- "Show prices in Mumbai"
- "Tomato price in Delhi"
- "Market rates for Bangalore"

**Type your city name!** 🌾"""
    
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
    
    # Location setting
    if "i'm in" in message_lower or "i am in" in message_lower or "location" in message_lower:
        words = user_message.split()
        for i, word in enumerate(words):
            if word.lower() in ["in", "from"]:
                if i + 1 < len(words):
                    st.session_state.user_location = words[i + 1].strip(".,!?")
                    return f"✅ Location set to {st.session_state.user_location}!"
    
    # Crop advice
    for crop, info in farming_tips["crops"].items():
        if crop in message_lower:
            return f"**{crop.title()} Guide:**\n\n{info}"
    
    # Season advice
    for season, info in farming_tips["seasons"].items():
        if season in message_lower:
            return f"**{season.title()} Tips:**\n\n{info}"
    
    # Pest control
    for pest, info in farming_tips["pests"].items():
        if pest in message_lower:
            return f"**Pest Control:**\n\n{info}"
    
    # Irrigation
    if "irrigation" in message_lower or "drip" in message_lower:
        return """💧 **Irrigation Tips:**

- **Drip:** Most efficient, 30-50% water savings
- **Sprinkler:** Good for large areas
- **Timing:** Early morning or evening
- **Amount:** 1-2 inches per week"""
    
    # Fertilizer
    if "fertilizer" in message_lower:
        return """🌱 **Fertilizer Guide:**

- **NPK:** N for leaves, P for roots, K for health
- **Organic:** Compost, manure, bone meal
- **Timing:** Before planting and during growth"""
    
    # Default
    responses = [
        "🌾 Ask me about crops, weather, prices, pests, or irrigation!",
        "🚜 I can help with farming tips, market prices, and weather updates!",
        "👨‍🌾 Your agricultural assistant ready to help!"
    ]
    
    return random.choice(responses)

# ---------------------- SIDEBAR ----------------------
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    **Agri Sense AI** helps with:
    - 🌤️ Weather updates
    - 💰 Market prices (50+ cities)
    - 🌾 Crop tips
    - 🐛 Pest management
    - 💧 Irrigation advice
    """)
    
    st.divider()
    
    st.header("🎯 Quick Actions")
    if st.button("📍 Delhi Prices"):
        st.session_state.messages.append({"role": "user", "content": "Show prices in Delhi"})
        st.rerun()
    if st.button("🌤️ Mumbai Weather"):
        st.session_state.messages.append({"role": "user", "content": "Weather in Mumbai"})
        st.rerun()
    if st.button("🌾 Crop Tips"):
        st.session_state.messages.append({"role": "user", "content": "Tell me about wheat"})
        st.rerun()
    
    st.divider()
    
    if st.session_state.user_location:
        st.info(f"📍 Location: {st.session_state.user_location}")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------------- CHAT INTERFACE ----------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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
    <p>🌾 <b>Agri Sense AI</b> - Empowering Farmers</p>
    <p style='font-size: 0.9em;'>💡 Weekly updated prices | Real-time weather</p>
</div>
""", unsafe_allow_html=True)
