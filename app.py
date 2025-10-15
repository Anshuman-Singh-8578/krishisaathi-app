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
    """Weekly Updated Market Prices - 100+ Cities Pan India Coverage
    Last Updated: October 12, 2025"""
    
    sample_prices = {
        # ========== NORTH INDIA ==========
        # Delhi NCR Updated Dataset (October 2025)
{
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
    }
},

        # Punjab Updated Dataset (October 2025)
{
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
},

        
        # Haryana (October 2025)
{
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
},
        
        # Rajasthan (October 2025)
{
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
},
        
        # Uttar Pradesh (October 2025)
{
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
},
        
        # Uttarakhand (October 2025)
{
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
},
        
        # Himachal Pradesh (October 2025)
{
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
}
,
        
        # ========== WEST INDIA ==========
        # Maharashtra Updated Dataset (October 2025)
{
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
}

        
       # Gujarat (October 2025)
{
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
},
        
        # ========== SOUTH INDIA ==========
        # Karnataka (October 2025)
{
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
},
        
       # Tamil Nadu (October 2025)
{
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
},
        
        # Telangana (October 2025)
{
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
},
# Telangana (October 2025)
{
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
},
       # Kerala (October 2025)
{
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
},
        
        # ========== EAST INDIA ==========
        # West Bengal (October 2025)
{
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
},
        
       # Bihar (October 2025)
{
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
},
        
        # Jharkhand
        {
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
},
        
        # Odisha
        {
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
},
        
        # Assam & Northeast
        {
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
},
        
        # ========== CENTRAL INDIA ==========
        # Madhya Pradesh
        {
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
},
        
        # Chhattisgarh
        {
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
},
        
        # ========== UNION TERRITORIES ==========
        {"Chandigarh": {
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
},
    
    
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
            return """💰 **Market Prices Available For 100+ Cities!**

🌏 **NORTH INDIA (30+ cities):**
• **Delhi NCR:** Delhi, Noida, Gurgaon, Faridabad, Ghaziabad
• **Punjab:** Chandigarh, Ludhiana, Amritsar, Jalandhar, Patiala
• **Haryana:** Rohtak, Panipat, Karnal
• **Rajasthan:** Jaipur, Jodhpur, Udaipur, Kota
• **UP:** Lucknow, Kanpur, Agra, Varanasi, Meerut, Allahabad
• **Uttarakhand:** Dehradun
• **HP:** Shimla

🌏 **WEST INDIA (20+ cities):**
• **Maharashtra:** Mumbai, Pune, Nagpur, Nashik, Thane, Aurangabad
• **Gujarat:** Ahmedabad, Surat, Rajkot, Vadodara
• **Goa:** Goa/Panaji

🌏 **SOUTH INDIA (25+ cities):**
• **Karnataka:** Bangalore, Mysore, Mangalore, Hubli
• **Tamil Nadu:** Chennai, Coimbatore, Madurai, Tiruchirappalli, Salem
• **Telangana/AP:** Hyderabad, Vijayawada, Visakhapatnam, Warangal
• **Kerala:** Kochi, Thiruvananthapuram, Kozhikode

🌏 **EAST INDIA (15+ cities):**
• **West Bengal:** Kolkata, Siliguri, Durgapur, Asansol
• **Bihar:** Patna, Gaya, Bhagalpur
• **Jharkhand:** Ranchi, Jamshedpur, Dhanbad
• **Odisha:** Bhubaneswar, Cuttack, Rourkela
• **Northeast:** Guwahati, Shillong, Imphal, Agartala

🌏 **CENTRAL INDIA (10+ cities):**
• **MP:** Bhopal, Indore, Jabalpur, Gwalior
• **Chhattisgarh:** Raipur, Bhilai

🌏 **UNION TERRITORIES:**
• Puducherry, Jammu, Srinagar, Port Blair

**💬 Ask me like:**
- "Show prices in Mumbai"
- "Tomato price in Bangalore"
- "Market rates for your city"

**📍 Type your city name - We cover 100+ major cities!** 🌾"""
    
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
    **Krishisaathi** helps with:
    - 🌤️ Weather updates
    - 💰 Market prices (100+ cities)
    - 🌾 Crop tips
    - 🐛 Pest management
    - 💧 Irrigation advice
    """)
    
    st.divider()
    
    st.header("🎯 Quick Actions")
    if st.button("📍 Delhi Prices"):
        user_msg = "Show prices in Delhi"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        
        # Generate bot response
        bot_response = get_bot_response(user_msg)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
        
    if st.button("🌤️ Mumbai Weather"):
        user_msg = "Weather in Mumbai"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        
        # Generate bot response
        bot_response = get_bot_response(user_msg)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
        
    if st.button("🌾 Crop Tips"):
        user_msg = "Tell me about wheat"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        
        # Generate bot response
        bot_response = get_bot_response(user_msg)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
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
    <p>🌾 <b>Krishisaathi</b> - Empowering Farmers</p>
    <p style='font-size: 0.9em;'>💡 Weekly updated prices | Real-time weather</p>
</div>
""", unsafe_allow_html=True)
