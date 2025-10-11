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
    .price-card {
        background-color: #f1f8f4;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🌾 AGRI SENSE AI CHATBOT</h1><p>Your smart assistant for sustainable farming 🚜</p></div>', unsafe_allow_html=True)

# ---------------------- INITIALIZE SESSION ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "expect_image" not in st.session_state:
    st.session_state.expect_image = False
if "user_location" not in st.session_state:
    st.session_state.user_location = None

# ---------------------- WEATHER FUNCTION ----------------------
def get_weather(city):
    """
    Fetches real-time weather data for the given city using OpenWeatherMap API
    """
    API_KEY = "bc072ed23f5983aac7f32d666efe49af"
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(BASE_URL, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            weather_info = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"]
            }
            return weather_info
        else:
            return None
    except Exception as e:
        return None

# ---------------------- API PRICE FETCHER (GOVERNMENT API ONLY) ----------------------
# ONLY REPLACE THE fetch_prices_from_government_api FUNCTION

def fetch_prices_from_government_api(location):
    """
    Fetches real-time commodity prices from Indian Government API ONLY
    """
    prices_data = {}
    
    try:
        # Commodity mapping for Indian markets
        commodity_mapping = {
            'tomato': 'Tomato',
            'potato': 'Potato',
            'onion': 'Onion',
            'cabbage': 'Cabbage',
            'cauliflower': 'Cauliflower',
            'apple': 'Apple',
            'banana': 'Banana',
            'orange': 'Orange',
            'mango': 'Mango',
            'watermelon': 'Water Melon',
            'carrot': 'Carrot',
            'brinjal': 'Brinjal',
            'beans': 'Beans',
            'spinach': 'Spinach'
        }
        
        # State name to code mapping (expanded)
        state_mapping = {
            'delhi': 'Delhi',
            'mumbai': 'Maharashtra',
            'bangalore': 'Karnataka',
            'bengaluru': 'Karnataka',
            'kolkata': 'West Bengal',
            'chennai': 'Tamil Nadu',
            'hyderabad': 'Telangana',
            'pune': 'Maharashtra',
            'ahmedabad': 'Gujarat',
            'jaipur': 'Rajasthan',
            'lucknow': 'Uttar Pradesh',
            'chandigarh': 'Chandigarh',
            'bhopal': 'Madhya Pradesh',
            'patna': 'Bihar'
        }
        
        location_lower = location.lower() if location != "all" else "delhi"
        state_name = state_mapping.get(location_lower, 'Delhi')
        
        city_prices = {}
        
        # Use the government API
        base_url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
        api_key_gov = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
        
        # Fetch only a few commodities to speed up
        priority_commodities = ['Tomato', 'Potato', 'Onion', 'Cabbage', 'Apple', 'Banana']
        
        for commodity_name in priority_commodities:
            try:
                params = {
                    'api-key': api_key_gov,
                    'format': 'json',
                    'filters[commodity]': commodity_name,
                    'filters[state]': state_name,
                    'limit': 1,
                    'offset': 0
                }
                
                # Increased timeout to 15 seconds
                response = requests.get(base_url, params=params, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    records = data.get('records', [])
                    
                    if records and len(records) > 0:
                        record = records[0]
                        
                        # Get prices from API
                        modal_price = record.get('modal_price', None)
                        min_price = record.get('min_price', None)
                        max_price = record.get('max_price', None)
                        
                        # Skip if no valid price data
                        if not modal_price:
                            continue
                        
                        # Convert quintal prices to per kg (divide by 100)
                        try:
                            modal_kg = float(modal_price) / 100
                            min_kg = float(min_price) / 100 if min_price else modal_kg
                            max_kg = float(max_price) / 100 if max_price else modal_kg
                            
                            # Format price range
                            price_range = f"₹{int(min_kg)}-{int(max_kg)}"
                            
                            # Calculate trend
                            if max_kg > modal_kg * 1.05:
                                trend = "↑"
                            elif min_kg < modal_kg * 0.95:
                                trend = "↓"
                            else:
                                trend = "→"
                            
                            city_prices[commodity_name] = {
                                "price": price_range,
                                "unit": "per kg",
                                "trend": trend,
                                "source": "Live API"
                            }
                        except (ValueError, TypeError):
                            continue
                else:
                    # Log the error for debugging
                    print(f"API Error for {commodity_name}: Status {response.status_code}")
                
            except requests.exceptions.Timeout:
                print(f"Timeout for {commodity_name}")
                continue
            except Exception as e:
                print(f"Error fetching {commodity_name}: {str(e)}")
                continue
        
        if city_prices and len(city_prices) > 0:
            location_formatted = location.title() if location != "all" else "Delhi"
            prices_data[location_formatted] = city_prices
            return prices_data
        else:
            # If no data found, return None to trigger fallback
            print(f"No price data found for {location}")
            return None
            
    except Exception as e:
        print(f"Government API Error: {str(e)}")
        st.error(f"Government API Error: {str(e)}")
    
    return None

# ---------------------- PRODUCE PRICE FUNCTION ----------------------
def get_produce_prices(state="all"):
    """
    Fetches produce prices using Government API with fallback to sample data
    """
    # Try to fetch from Government API first
    try:
        api_prices = fetch_prices_from_government_api(state)
        if api_prices and len(api_prices) > 0:
            # Check if we got actual data (not empty)
            for city, prices in api_prices.items():
                if prices and len(prices) > 0:
                    return api_prices
    except Exception as e:
        st.warning(f"⚠️ Government API temporarily unavailable: {str(e)}")
    
    # Fallback to sample data if API fails
    sample_prices = {
        "Delhi": {
            "Tomato": {"price": "₹25-30", "unit": "per kg", "trend": "↑"},
            "Potato": {"price": "₹20-25", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹30-35", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹15-20", "unit": "per kg", "trend": "→"},
            "Cauliflower": {"price": "₹25-30", "unit": "per kg", "trend": "↑"},
            "Apple": {"price": "₹120-150", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹40-50", "unit": "per dozen", "trend": "→"},
            "Orange": {"price": "₹60-80", "unit": "per kg", "trend": "↑"},
            "Watermelon": {"price": "₹20-25", "unit": "per kg", "trend": "→"}
        },
        "Mumbai": {
            "Tomato": {"price": "₹30-35", "unit": "per kg", "trend": "↑"},
            "Potato": {"price": "₹22-28", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹35-40", "unit": "per kg", "trend": "↓"},
            "Cabbage": {"price": "₹18-22", "unit": "per kg", "trend": "→"},
            "Cauliflower": {"price": "₹28-35", "unit": "per kg", "trend": "↑"},
            "Apple": {"price": "₹130-160", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹45-55", "unit": "per dozen", "trend": "→"},
            "Mango": {"price": "₹80-120", "unit": "per kg", "trend": "↓"},
            "Watermelon": {"price": "₹22-28", "unit": "per kg", "trend": "→"}
        },
        "Bangalore": {
            "Tomato": {"price": "₹28-32", "unit": "per kg", "trend": "→"},
            "Potato": {"price": "₹18-24", "unit": "per kg", "trend": "↓"},
            "Onion": {"price": "₹32-38", "unit": "per kg", "trend": "↑"},
            "Carrot": {"price": "₹35-40", "unit": "per kg", "trend": "→"},
            "Beans": {"price": "₹40-50", "unit": "per kg", "trend": "↑"},
            "Apple": {"price": "₹125-155", "unit": "per kg", "trend": "→"},
            "Grapes": {"price": "₹60-80", "unit": "per kg", "trend": "↓"},
            "Papaya": {"price": "₹30-40", "unit": "per kg", "trend": "→"}
        },
        "Kolkata": {
            "Tomato": {"price": "₹24-28", "unit": "per kg", "trend": "→"},
            "Potato": {"price": "₹16-22", "unit": "per kg", "trend": "↓"},
            "Onion": {"price": "₹28-32", "unit": "per kg", "trend": "→"},
            "Brinjal": {"price": "₹25-30", "unit": "per kg", "trend": "↑"},
            "Spinach": {"price": "₹20-25", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹35-45", "unit": "per dozen", "trend": "→"},
            "Guava": {"price": "₹40-50", "unit": "per kg", "trend": "↓"},
            "Pineapple": {"price": "₹35-45", "unit": "per piece", "trend": "→"}
        },
        "Chennai": {
            "Tomato": {"price": "₹26-30", "unit": "per kg", "trend": "↑"},
            "Potato": {"price": "₹20-26", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹30-36", "unit": "per kg", "trend": "↓"},
            "Drumstick": {"price": "₹40-50", "unit": "per kg", "trend": "→"},
            "Ladies Finger": {"price": "₹30-40", "unit": "per kg", "trend": "↑"},
            "Banana": {"price": "₹30-40", "unit": "per dozen", "trend": "→"},
            "Mango": {"price": "₹70-100", "unit": "per kg", "trend": "↓"},
            "Coconut": {"price": "₹35-45", "unit": "per piece", "trend": "→"}
        },
        "Hyderabad": {
            "Tomato": {"price": "₹24-29", "unit": "per kg", "trend": "↑"},
            "Potato": {"price": "₹18-24", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹28-34", "unit": "per kg", "trend": "↓"},
            "Brinjal": {"price": "₹22-28", "unit": "per kg", "trend": "→"},
            "Cabbage": {"price": "₹16-22", "unit": "per kg", "trend": "↑"},
            "Apple": {"price": "₹115-145", "unit": "per kg", "trend": "→"},
            "Banana": {"price": "₹35-45", "unit": "per dozen", "trend": "→"},
            "Watermelon": {"price": "₹18-24", "unit": "per kg", "trend": "→"}
        }
    }
    
    # Return prices for specific state or show options
    if state.lower() == "all":
        return sample_prices
    else:
        # Find matching city
        for city in sample_prices.keys():
            if state.lower() in city.lower():
                return {city: sample_prices[city]}
        return None

def format_specific_produce_price(prices, city_name, produce_name):
    """
    Formats price data for a specific produce item
    """
    if not prices:
        return f"❌ Sorry, I couldn't find price data for {produce_name}."
    
    response = f"💰 **Current Market Price for {produce_name.title()}:**\n\n"
    found = False
    is_live = False
    
    for city, produce_data in prices.items():
        if city_name and city_name.lower() not in city.lower():
            continue
        
        # Search for the produce (case-insensitive)
        for item, data in produce_data.items():
            if produce_name.lower() in item.lower():
                found = True
                trend_symbol = data["trend"]
                trend_text = "Rising" if trend_symbol == "↑" else "Stable" if trend_symbol == "→" else "Falling"
                
                # Check if from live API
                if data.get("source") == "Live API":
                    is_live = True
                
                response += f"📍 **{city}**\n"
                response += f"• Price: **{data['price']}** {data['unit']}\n"
                response += f"• Trend: {trend_symbol} {trend_text}\n\n"
    
    if not found:
        return f"❌ Sorry, I don't have price data for '{produce_name}' yet. Try: tomato, potato, onion, watermelon, apple, banana, or cabbage."
    
    response += f"📅 Updated: {datetime.now().strftime('%B %d, %Y')}\n"
    
    if is_live:
        response += "📡 **Source:** Government of India Open Data API (Live)\n"
        response += "🎯 **Data Quality:** Real-time mandi prices\n"
    else:
        response += "📊 **Source:** Sample/Cached data\n"
        response += "⚠️ **Note:** Live API data temporarily unavailable\n"
    
    response += "💡 **Tip:** Prices may vary by market and quality."
    
    return response

def format_price_response(prices, city_name=None):
    """
    Formats price data into a readable response
    """
    if not prices:
        return "❌ Sorry, I couldn't find price data for that location. Try: Delhi, Mumbai, Bangalore, Kolkata, or Chennai."
    
    response = "💰 **Current Market Prices (Retail):**\n\n"
    
    for city, produce_data in prices.items():
        if city_name and city_name.lower() not in city.lower():
            continue
            
        response += f"📍 **{city}** (Updated: {datetime.now().strftime('%B %d, %Y')})\n\n"
        
        # Separate vegetables and fruits
        vegetables = []
        fruits = []
        
        for item, data in produce_data.items():
            trend_symbol = data["trend"]
            price_line = f"• **{item}**: {data['price']} {data['unit']} {trend_symbol}"
            
            if item.lower() in ["apple", "banana", "orange", "mango", "grapes", "papaya", "guava", "pineapple", "coconut"]:
                fruits.append(price_line)
            else:
                vegetables.append(price_line)
        
        if vegetables:
            response += "🥬 **Vegetables:**\n"
            response += "\n".join(vegetables) + "\n\n"
        
        if fruits:
            response += "🍎 **Fruits:**\n"
            response += "\n".join(fruits) + "\n\n"
    
    response += "\n📊 **Trend Legend:** ↑ Rising | → Stable | ↓ Falling\n"
    response += "💡 **Tip:** Prices vary by season and market. Buy seasonal produce for best value!"
    
    return response

def extract_city_from_message(message):
    """
    Extracts city name from user message
    """
    message_lower = message.lower()
    
    # Patterns to extract city names
    patterns = [
        r"weather (?:in|at|for|of) ([a-zA-Z\s]+)",
        r"(?:in|at|for) ([a-zA-Z\s]+) weather",
        r"temperature (?:in|at|of) ([a-zA-Z\s]+)",
        r"(?:in|at|of) ([a-zA-Z\s]+) temperature",
        r"forecast (?:for|in|at) ([a-zA-Z\s]+)",
        r"(?:how is|what's|whats) (?:the )?(?:weather|temperature) (?:in|at) ([a-zA-Z\s]+)",
        r"price(?:s)? (?:in|at|for) ([a-zA-Z\s]+)",
        r"(?:in|at|for) ([a-zA-Z\s]+) price(?:s)?",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, message_lower)
        if match:
            city = match.group(1).strip()
            # Clean up common words
            city = re.sub(r'\b(today|tomorrow|now|current|latest)\b', '', city).strip()
            if city:
                return city
    
    return None

# ---------------------- FARMING KNOWLEDGE BASE ----------------------
farming_tips = {
    "crops": {
        "wheat": "🌾 Wheat grows best in cool, moist climates. Plant in fall or spring. Requires well-drained soil with pH 6.0-7.0.",
        "rice": "🍚 Rice needs flooded fields and warm temperatures (20-35°C). Requires clayey soil that retains water well.",
        "corn": "🌽 Corn thrives in warm weather with temperatures 21-30°C. Plant after last frost. Needs nitrogen-rich soil.",
        "tomato": "🍅 Tomatoes need 6-8 hours of sunlight daily. Plant when soil temperature is above 15°C. Water deeply but infrequently.",
        "potato": "🥔 Potatoes prefer cool weather (15-20°C). Plant in loose, acidic soil (pH 5.0-6.0). Hill soil around plants as they grow."
    },
    "seasons": {
        "spring": "🌸 Spring is ideal for planting: tomatoes, peppers, corn, beans, cucumbers, squash, and melons.",
        "summer": "☀️ Summer maintenance: Regular watering, pest control, and harvesting early crops. Plant fall vegetables.",
        "fall": "🍂 Fall planting: Garlic, onions, winter wheat, cover crops. Harvest summer crops and prepare for winter.",
        "winter": "❄️ Winter activities: Plan next season, maintain equipment, indoor seed starting, and cold-frame gardening."
    },
    "pests": {
        "aphids": "🐛 Aphids: Use neem oil spray, introduce ladybugs, or spray with water and mild soap solution.",
        "caterpillars": "🐛 Caterpillars: Hand-pick, use Bacillus thuringiensis (Bt), or plant companion flowers to attract predators.",
        "beetles": "🪲 Beetles: Hand-pick, use row covers, apply diatomaceous earth, or use neem oil spray.",
        "general": "🛡️ Pest prevention: Crop rotation, companion planting, beneficial insects, proper spacing, and healthy soil."
    },
    "soil": {
        "sandy": "Sandy soil: Add compost and organic matter to improve water retention. Good drainage but needs frequent watering.",
        "clay": "Clay soil: Add sand and compost to improve drainage. Rich in nutrients but can become waterlogged.",
        "loamy": "Loamy soil: Ideal for most crops! Balanced mixture of sand, silt, and clay with good drainage and nutrients.",
        "improvement": "Soil improvement: Add compost, use cover crops, practice crop rotation, and test pH regularly."
    }
}

# ---------------------- CHATBOT RESPONSE LOGIC ----------------------
def get_bot_response(user_message):
    """
    Generates intelligent responses based on user queries
    """
    message_lower = user_message.lower()
    
    # Price queries
    if any(word in message_lower for word in ["price", "cost", "rate", "market price", "mandi"]):
        city = extract_city_from_message(user_message)
        
        # Check for specific produce in the query
        specific_produce = None
        produce_list = ["tomato", "potato", "onion", "cabbage", "cauliflower", "apple", "banana", 
                       "orange", "mango", "carrot", "beans", "brinjal", "spinach", "grapes", 
                       "papaya", "guava", "pineapple", "drumstick", "ladies finger", "coconut", "watermelon"]
        
        for produce in produce_list:
            if produce in message_lower:
                specific_produce = produce
                break
        
        if city:
            prices = get_produce_prices(city)
            if specific_produce:
                # Show specific produce price
                return format_specific_produce_price(prices, city, specific_produce)
            else:
                return format_price_response(prices, city)
        elif specific_produce:
            # User asked for specific produce but no city - show all cities
            all_prices = get_produce_prices("all")
            return format_specific_produce_price(all_prices, None, specific_produce)
        else:
            # Show all available cities
            return """💰 **Market Price Information Available For:**

📍 Delhi | Mumbai | Bangalore | Kolkata | Chennai | Hyderabad

**Ask me like:**
- "Show prices in Delhi"
- "What are vegetable prices in Mumbai?"
- "Market rates for Bangalore"
- "Fruit prices in Chennai"
- "Tomato price in Hyderabad"

Or ask about a specific produce: "tomato price", "potato rates", "watermelon price in Delhi", etc."""
    
    # Weather queries
    if any(word in message_lower for word in ["weather", "temperature", "rain", "forecast", "climate"]):
        city = extract_city_from_message(user_message)
        
        if not city:
            if st.session_state.user_location:
                city = st.session_state.user_location
            else:
                return "📍 Please specify a location! You can ask like:\n- 'What's the weather in Delhi?'\n- 'Weather for Mumbai'\n- 'Temperature in Bangalore'\n\nOr set your default location by saying 'I'm in [city name]'"
        
        weather = get_weather(city)
        if weather:
            return f"""🌤️ **Weather in {weather['city']}:**
            
- Temperature: {weather['temperature']}°C (feels like {weather['feels_like']}°C)
- Conditions: {weather['description'].title()}
- Humidity: {weather['humidity']}%
- Wind Speed: {weather['wind_speed']} m/s

**Farming Advice:** {"Good conditions for outdoor work! 🌞" if weather['temperature'] > 15 else "Consider indoor tasks or protective measures. 🧥"}"""
        else:
            return f"❌ Sorry, I couldn't fetch weather data for '{city}'. Please check the spelling or try another city."
    
    # Location setting
    if "location" in message_lower or "i'm in" in message_lower or "i am in" in message_lower:
        words = user_message.split()
        for i, word in enumerate(words):
            if word.lower() in ["in", "location", "from"]:
                if i + 1 < len(words):
                    st.session_state.user_location = words[i + 1].strip(".,!?")
                    return f"✅ Default location set to {st.session_state.user_location}! Now you can ask 'weather' or 'prices' without specifying a city."
    
    # Crop advice
    for crop, info in farming_tips["crops"].items():
        if crop in message_lower:
            return f"**{crop.title()} Farming Guide:**\n\n{info}"
    
    # Season advice
    for season, info in farming_tips["seasons"].items():
        if season in message_lower:
            return f"**{season.title()} Farming Tips:**\n\n{info}"
    
    # Pest control
    for pest, info in farming_tips["pests"].items():
        if pest in message_lower:
            return f"**Pest Control - {pest.title()}:**\n\n{info}"
    
    # Soil queries
    if "soil" in message_lower:
        for soil_type, info in farming_tips["soil"].items():
            if soil_type in message_lower:
                return f"**Soil Information:**\n\n{info}"
        return farming_tips["soil"]["improvement"]
    
    # Irrigation
    if any(word in message_lower for word in ["irrigation", "drip"]) and "water" not in message_lower:
        return """💧 **Irrigation Best Practices:**

- **Drip Irrigation:** Most efficient, delivers water directly to roots, saves 30-50% water
- **Sprinkler:** Good for large areas, mimics rainfall
- **Timing:** Water early morning or evening to reduce evaporation
- **Amount:** Most crops need 1-2 inches per week
- **Check soil:** Water when top 2 inches of soil are dry"""
    
    # Fertilizer
    if "fertilizer" in message_lower or "nutrients" in message_lower:
        return """🌱 **Fertilizer Guide:**

- **NPK Basics:** N (Nitrogen) for leaves, P (Phosphorus) for roots, K (Potassium) for overall health
- **Organic Options:** Compost, manure, bone meal, fish emulsion
- **Application:** Follow soil test results, don't over-fertilize
- **Timing:** Apply before planting and during active growth
- **Tip:** Organic matter improves soil structure and nutrient retention"""
    
    # Organic farming
    if "organic" in message_lower:
        return """🌿 **Organic Farming Tips:**

- Use natural compost and manure
- Practice crop rotation (3-4 year cycles)
- Encourage beneficial insects
- Use natural pest deterrents (neem, garlic spray)
- Mulch to retain moisture and suppress weeds
- Avoid synthetic pesticides and fertilizers
- Maintain biodiversity on your farm"""
    
    # Disease
    if "disease" in message_lower or "blight" in message_lower:
        return """🔬 **Common Plant Diseases & Prevention:**

- **Fungal Diseases:** Improve air circulation, avoid overhead watering, use copper fungicides
- **Bacterial Issues:** Remove infected plants, practice crop rotation, use disease-resistant varieties
- **Viral Problems:** Control insect vectors, remove infected plants immediately
- **Prevention:** Proper spacing, clean tools, healthy soil, resistant varieties"""
    
    # Harvest
    if "harvest" in message_lower or "when to pick" in message_lower:
        return """🌾 **Harvest Tips:**

- Harvest in the morning after dew dries
- Use sharp, clean tools
- Handle produce gently to avoid bruising
- Check crop-specific maturity indicators
- Store properly immediately after harvest
- Most vegetables taste best when picked young and tender"""
    
    # Default responses
    general_responses = [
        "🌾 I'm here to help with farming advice! Ask me about crops, weather, market prices, pests, soil, or irrigation.",
        "🚜 I can assist with crop selection, pest control, weather updates, market prices, and sustainable farming practices. What would you like to know?",
        "🌱 Feel free to ask about specific crops, farming techniques, weather, or market prices in any city!",
        "👨‍🌾 I'm your agricultural assistant! Ask me about planting, harvesting, prices, weather forecasts, or farm management."
    ]
    
    return random.choice(general_responses)

# ---------------------- SIDEBAR INFO ----------------------
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    **Agri Sense AI** helps farmers with:
    - 🌤️ Weather updates for ANY city
    - 💰 Daily market prices (region-wise)
    - 🌾 Crop selection & care tips
    - 🐛 Pest & disease management
    - 💧 Irrigation advice
    - 🌱 Organic farming practices
    - 📅 Seasonal planning
    """)
    
    st.divider()
    
    # API Configuration Status
    st.header("⚙️ API Status")
    
    # Check if government API is working
    try:
        test_response = requests.get("https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit=1", timeout=3)
        if test_response.status_code == 200:
            st.success("✅ Live prices from Govt API")
            st.info("📡 Source: data.gov.in")
        else:
            st.warning("⚠️ Using sample data")
    except:
        st.warning("⚠️ Using sample data")
    
    with st.expander("📝 About Price Data"):
        st.write("""
        **Data Source:**
        
        🇮🇳 **Indian Government Open Data API**
        - Real mandi prices
        - Updated regularly
        - No API key needed!
        - FREE and open for all
        
        📊 **Note:** Prices shown are wholesale rates per quintal (100 kg) converted to per kg. Retail prices may vary.
        
        💡 **Fallback:** If API is unavailable, sample data is shown for reference.
        """)
    
    st.divider()
    
    st.header("🎯 Quick Topics")
    if st.button("📍 Prices in Delhi"):
        st.session_state.messages.append({"role": "user", "content": "Show prices in Delhi"})
        st.rerun()
    if st.button("🌤️ Weather in Mumbai"):
        st.session_state.messages.append({"role": "user", "content": "What's the weather in Mumbai?"})
        st.rerun()
    if st.button("🌾 Crop Tips"):
        st.session_state.messages.append({"role": "user", "content": "Tell me about wheat farming"})
        st.rerun()
    if st.button("🐛 Pest Control"):
        st.session_state.messages.append({"role": "user", "content": "How to control pests?"})
        st.rerun()
    
    st.divider()
    
    if st.session_state.user_location:
        st.info(f"📍 Default location: {st.session_state.user_location}")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------------- DISPLAY CHAT HISTORY ----------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------- CHAT INPUT ----------------------
if prompt := st.chat_input("Ask me anything about farming..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display bot response
    with st.chat_message("assistant"):
        with st.spinner("🌱 Thinking..."):
            response = get_bot_response(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# ---------------------- FOOTER ----------------------
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🌾 <b>Agri Sense AI</b> - Empowering Farmers with Technology</p>
    <p style='font-size: 0.9em;'>💡 Ask about weather, market prices, or farming tips for any location!</p>
</div>
""", unsafe_allow_html=True)
