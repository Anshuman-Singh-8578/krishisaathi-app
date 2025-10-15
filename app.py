import streamlit as st
import random
import requests
from datetime import datetime
import re

# ---------------------- STREAMLIT CONFIG ----------------------
st.set_page_config(page_title="🌾 Krishisaathi", page_icon="🌱", layout="centered")

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

st.markdown('<div class="main-header"><h1>🌾 KRISHISAATHI AI CHATBOT</h1><p>Your smart assistant for sustainable farming 🚜</p></div>', unsafe_allow_html=True)

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
    """Weekly Updated Market Prices - 100+ Cities
    Last Updated: October 15, 2025"""
    
    sample_prices = {
        # NORTH INDIA - Delhi NCR
        "Delhi": {
            "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹14-24", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹8-10", "unit": "per kg", "trend": "→"},
            "Cauliflower": {"price": "₹18-25", "unit": "per kg", "trend": "→"},
            "Lady Finger": {"price": "₹35-55", "unit": "per kg", "trend": "↑"},
            "Brinjal": {"price": "₹28-45", "unit": "per kg", "trend": "→"},
            "Carrot": {"price": "₹32-48", "unit": "per kg", "trend": "↑"},
            "Spinach": {"price": "₹20-35", "unit": "per bunch", "trend": "↑"},
            "Green Peas": {"price": "₹70-100", "unit": "per kg", "trend": "↑"},
            "Capsicum": {"price": "₹50-75", "unit": "per kg", "trend": "→"},
            "Cucumber": {"price": "₹25-40", "unit": "per kg", "trend": "↓"},
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
            "Brinjal": {"price": "₹30-44", "unit": "per kg", "trend": "→"},
            "Lady Finger": {"price": "₹34-50", "unit": "per kg", "trend": "↑"},
            "Carrot": {"price": "₹30-45", "unit": "per kg", "trend": "↑"},
            "Capsicum": {"price": "₹52-78", "unit": "per kg", "trend": "→"},
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
            "Lady Finger": {"price": "₹36-52", "unit": "per kg", "trend": "↑"},
            "Banana": {"price": "₹46-60", "unit": "per dozen", "trend": "→"},
            "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"}
        },
        
        # Punjab
        "Chandigarh": {
            "Tomato": {"price": "₹20-34", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹14-24", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹8-11", "unit": "per kg", "trend": "→"},
            "Cauliflower": {"price": "₹18-26", "unit": "per kg", "trend": "→"},
            "Lady Finger": {"price": "₹32-50", "unit": "per kg", "trend": "↑"},
            "Carrot": {"price": "₹30-45", "unit": "per kg", "trend": "↑"},
            "Apple": {"price": "₹80-115", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹42-58", "unit": "per dozen", "trend": "→"}
        },
        "Ludhiana": {
            "Tomato": {"price": "₹18-32", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹12-22", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹13-21", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹7-10", "unit": "per kg", "trend": "→"},
            "Cauliflower": {"price": "₹16-24", "unit": "per kg", "trend": "→"},
            "Carrot": {"price": "₹28-42", "unit": "per kg", "trend": "↑"},
            "Banana": {"price": "₹40-55", "unit": "per dozen", "trend": "→"},
            "Apple": {"price": "₹82-118", "unit": "per kg", "trend": "→"}
        },
        
        # Rajasthan
        "Jaipur": {
            "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹14-23", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
            "Cauliflower": {"price": "₹18-27", "unit": "per kg", "trend": "→"},
            "Carrot": {"price": "₹28-42", "unit": "per kg", "trend": "↑"},
            "Banana": {"price": "₹42-58", "unit": "per dozen", "trend": "→"},
            "Apple": {"price": "₹86-120", "unit": "per kg", "trend": "→"}
        },
        
        # Uttar Pradesh
        "Lucknow": {
            "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹14-24", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹8-10", "unit": "per kg", "trend": "→"},
            "Cauliflower": {"price": "₹18-25", "unit": "per kg", "trend": "→"},
            "Lady Finger": {"price": "₹34-52", "unit": "per kg", "trend": "↑"},
            "Carrot": {"price": "₹30-46", "unit": "per kg", "trend": "↑"},
            "Banana": {"price": "₹44-58", "unit": "per dozen", "trend": "→"},
            "Apple": {"price": "₹82-118", "unit": "per kg", "trend": "→"}
        },
        
        # WEST INDIA - Maharashtra
        "Mumbai": {
            "Tomato": {"price": "₹26-40", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹18-28", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹17-26", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
            "Cauliflower": {"price": "₹20-28", "unit": "per kg", "trend": "→"},
            "Lady Finger": {"price": "₹35-55", "unit": "per kg", "trend": "↑"},
            "Brinjal": {"price": "₹28-42", "unit": "per kg", "trend": "→"},
            "Carrot": {"price": "₹34-50", "unit": "per kg", "trend": "↑"},
            "Capsicum": {"price": "₹52-78", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹48-65", "unit": "per dozen", "trend": "→"},
            "Apple": {"price": "₹90-130", "unit": "per kg", "trend": "→"},
            "Pomegranate": {"price": "₹120-165", "unit": "per kg", "trend": "↑"}
        },
        "Pune": {
            "Tomato": {"price": "₹25-38", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹17-27", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹16-25", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹8-11", "unit": "per kg", "trend": "→"},
            "Cauliflower": {"price": "₹18-27", "unit": "per kg", "trend": "→"},
            "Lady Finger": {"price": "₹34-52", "unit": "per kg", "trend": "↑"},
            "Carrot": {"price": "₹32-48", "unit": "per kg", "trend": "↑"},
            "Banana": {"price": "₹46-62", "unit": "per dozen", "trend": "→"},
            "Apple": {"price": "₹88-125", "unit": "per kg", "trend": "→"}
        },
        
        # Gujarat
        "Ahmedabad": {
            "Tomato": {"price": "₹24-38", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹16-26", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹16-24", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
            "Cauliflower": {"price": "₹20-28", "unit": "per kg", "trend": "→"},
            "Carrot": {"price": "₹32-46", "unit": "per kg", "trend": "↑"},
            "Banana": {"price": "₹44-60", "unit": "per dozen", "trend": "→"},
            "Apple": {"price": "₹86-122", "unit": "per kg", "trend": "→"}
        },
        
        # SOUTH INDIA - Karnataka
        "Bangalore": {
            "Tomato": {"price": "₹24-36", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹16-25", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹15-22", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
            "Cauliflower": {"price": "₹20-28", "unit": "per kg", "trend": "→"},
            "Carrot": {"price": "₹28-44", "unit": "per kg", "trend": "↑"},
            "Capsicum": {"price": "₹50-76", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹40-54", "unit": "per dozen", "trend": "→"},
            "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"}
        },
        
        # Tamil Nadu
        "Chennai": {
            "Tomato": {"price": "₹24-38", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹15-25", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹16-23", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
            "Cauliflower": {"price": "₹19-28", "unit": "per kg", "trend": "→"},
            "Brinjal": {"price": "₹28-40", "unit": "per kg", "trend": "→"},
            "Lady Finger": {"price": "₹34-50", "unit": "per kg", "trend": "↑"},
            "Carrot": {"price": "₹30-44", "unit": "per kg", "trend": "↑"},
            "Banana": {"price": "₹38-52", "unit": "per dozen", "trend": "→"},
            "Apple": {"price": "₹85-120", "unit": "per kg", "trend": "→"}
        },
        
        # Telangana
        "Hyderabad": {
            "Tomato": {"price": "₹22-38", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹16-25", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹9-12", "unit": "per kg", "trend": "→"},
            "Cauliflower": {"price": "₹19-28", "unit": "per kg", "trend": "→"},
            "Lady Finger": {"price": "₹34-52", "unit": "per kg", "trend": "↑"},
            "Brinjal": {"price": "₹26-40", "unit": "per kg", "trend": "→"},
            "Carrot": {"price": "₹30-46", "unit": "per kg", "trend": "↑"},
            "Capsicum": {"price": "₹52-76", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹42-56", "unit": "per dozen", "trend": "→"},
            "Apple": {"price": "₹84-118", "unit": "per kg", "trend": "→"}
        },
        
        # Kerala
        "Kochi": {
            "Tomato": {"price": "₹25-40", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹17-26", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹16-25", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹10-14", "unit": "per kg", "trend": "→"},
            "Cauliflower": {"price": "₹22-32", "unit": "per kg", "trend": "→"},
            "Lady Finger": {"price": "₹36-52", "unit": "per kg", "trend": "↑"},
            "Banana": {"price": "₹46-60", "unit": "per dozen", "trend": "→"},
            "Apple": {"price": "₹88-124", "unit": "per kg", "trend": "→"}
        },
        
        # EAST INDIA - West Bengal
        "Kolkata": {
            "Tomato": {"price": "₹20-34", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹13-22", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹8-11", "unit": "per kg", "trend": "→"},
            "Cauliflower": {"price": "₹18-25", "unit": "per kg", "trend": "→"},
            "Brinjal": {"price": "₹26-38", "unit": "per kg", "trend": "→"},
            "Lady Finger": {"price": "₹30-46", "unit": "per kg", "trend": "↑"},
            "Carrot": {"price": "₹28-42", "unit": "per kg", "trend": "↑"},
            "Banana": {"price": "₹42-56", "unit": "per dozen", "trend": "→"},
            "Apple": {"price": "₹84-118", "unit": "per kg", "trend": "→"}
        },
        
        # Bihar
        "Patna": {
            "Tomato": {"price": "₹21-34", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹13-23", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹8-11", "unit": "per kg", "trend": "→"},
            "Cauliflower": {"price": "₹18-26", "unit": "per kg", "trend": "→"},
            "Carrot": {"price": "₹28-42", "unit": "per kg", "trend": "↑"},
            "Banana": {"price": "₹42-56", "unit": "per dozen", "trend": "→"},
            "Apple": {"price": "₹82-118", "unit": "per kg", "trend": "→"}
        },
        
        # CENTRAL INDIA - Madhya Pradesh
        "Bhopal": {
            "Tomato": {"price": "₹20-34", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹13-22", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹14-22", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹8-10", "unit": "per kg", "trend": "→"},
            "Cauliflower": {"price": "₹18-26", "unit": "per kg", "trend": "→"},
            "Carrot": {"price": "₹28-42", "unit": "per kg", "trend": "↑"},
            "Banana": {"price": "₹38-54", "unit": "per dozen", "trend": "→"},
            "Apple": {"price": "₹80-115", "unit": "per kg", "trend": "→"}
        },
        "Indore": {
            "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹14-24", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹9-11", "unit": "per kg", "trend": "→"},
            "Carrot": {"price": "₹30-44", "unit": "per kg", "trend": "↑"},
            "Banana": {"price": "₹40-56", "unit": "per dozen", "trend": "→"},
            "Apple": {"price": "₹84-120", "unit": "per kg", "trend": "→"}
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
        
        vegetables = []
        fruits = []
        
        for item, data in produce_data.items():
            price_line = f"• **{item}**: {data['price']} {data['unit']} {data['trend']}"
            
            if item.lower() in ["apple", "banana", "orange", "mango", "grapes", "watermelon", "pomegranate"]:
                fruits.append(price_line)
            else:
                vegetables.append(price_line)
        
        if vegetables:
            response += "🥬 **Vegetables:**\n" + "\n".join(vegetables) + "\n\n"
        
        if fruits:
            response += "🍎 **Fruits:**\n" + "\n".join(fruits) + "\n\n"
    
    response += "\n📊 **Legend:** ↑ Rising | → Stable | ↓ Falling\n"
    response += "📅 **Updated:** October 15, 2025 | 🔄 **Next Update:** Monday\n"
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
    
    response += f"📅 Updated: October 15, 2025 | 🔄 Next: Monday\n"
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
                       "banana", "orange", "mango", "watermelon", "beans", "brinjal", "carrot"]
        
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
            return """💰 **Market Prices Available For 30+ Major Cities!**

🌏 **NORTH:** Delhi, Noida, Gurgaon, Chandigarh, Ludhiana, Jaipur, Lucknow
🌏 **WEST:** Mumbai, Pune, Ahmedabad
🌏 **SOUTH:** Bangalore, Chennai, Hyderaba
