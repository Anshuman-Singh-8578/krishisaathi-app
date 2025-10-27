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

# ---------------------- TRANSLATION SETUP ----------------------
try:
    from deep_translator import GoogleTranslator
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False
    st.warning("⚠️ Translation library not available. Install: pip install deep-translator")

# ---------------------- LANGUAGE CONFIGURATION ----------------------
SUPPORTED_LANGUAGES = {
    'en': {'name': 'English', 'flag': '🇬🇧'},
    'hi': {'name': 'हिन्दी', 'flag': '🇮🇳'},
    'mr': {'name': 'मराठी', 'flag': '🇮🇳'},
    'ta': {'name': 'தமிழ்', 'flag': '🇮🇳'},
    'te': {'name': 'తెలుగు', 'flag': '🇮🇳'},
    'bn': {'name': 'বাংলা', 'flag': '🇮🇳'},
    'gu': {'name': 'ગુજરાતી', 'flag': '🇮🇳'},
    'kn': {'name': 'ಕನ್ನಡ', 'flag': '🇮🇳'},
    'ml': {'name': 'മലയാളം', 'flag': '🇮🇳'},
    'pa': {'name': 'ਪੰਜਾਬੀ', 'flag': '🇮🇳'}
}

# ---------------------- UI TEXT TRANSLATIONS ----------------------
UI_TRANSLATIONS = {
    'en': {
        'app_title': 'KRISHISAATHI AI',
        'app_tagline': 'Connecting Farmers, Empowering Growth',
        'select_language': 'Select Your Language',
        'quick_actions': '🎯 Quick Actions',
        'disease_detection': '📷 Disease Detection',
        'delhi_prices': '🏙️ Delhi Prices',
        'mumbai_weather': '🌤️ Mumbai Weather',
        'crop_tips': '🌾 Crop Tips',
        'govt_schemes': '🏛️ Govt Schemes',
        'clear_chat': '🗑️ Clear Chat',
        'upload_image': '📸 Upload Crop Image',
        'choose_image': 'Choose an image',
        'uploaded_image': 'Uploaded Image',
        'analyzing': '🔬 Analyzing...',
        'detection_complete': '✅ Detection Complete!',
        'disease': 'Disease',
        'confidence': 'Confidence',
        'done': '✅ Done',
        'chat_placeholder': 'Ask about farming...',
        'thinking': '🌱 Thinking...',
        'footer_title': '🌾 Krishisaathi AI',
        'footer_tagline': 'Empowering Farmers with Technology',
        'footer_copyright': '© 2025 Krishisaathi AI. All rights reserved.',
        'smart_assistant': 'Smart Farming Assistant',
        'show_prices': 'Show prices in',
        'weather_in': 'Weather in',
        'tell_about': 'Tell me about wheat',
        'check_disease': 'Check crop disease',
        'govt_schemes_msg': 'Tell me about government schemes'
    },
    'hi': {
        'app_title': 'कृषिसाथी एआई',
        'app_tagline': 'किसानों को जोड़ना, विकास को सशक्त बनाना',
        'select_language': 'अपनी भाषा चुनें',
        'quick_actions': '🎯 त्वरित कार्य',
        'disease_detection': '📷 रोग पहचान',
        'delhi_prices': '🏙️ दिल्ली की कीमतें',
        'mumbai_weather': '🌤️ मुंबई का मौसम',
        'crop_tips': '🌾 फसल सुझाव',
        'govt_schemes': '🏛️ सरकारी योजनाएं',
        'clear_chat': '🗑️ चैट साफ करें',
        'upload_image': '📸 फसल की तस्वीर अपलोड करें',
        'choose_image': 'एक तस्वीर चुनें',
        'uploaded_image': 'अपलोड की गई तस्वीर',
        'analyzing': '🔬 विश्लेषण कर रहे हैं...',
        'detection_complete': '✅ पहचान पूर्ण!',
        'disease': 'रोग',
        'confidence': 'विश्वास',
        'done': '✅ पूर्ण',
        'chat_placeholder': 'खेती के बारे में पूछें...',
        'thinking': '🌱 सोच रहे हैं...',
        'footer_title': '🌾 कृषिसाथी एआई',
        'footer_tagline': 'प्रौद्योगिकी से किसानों को सशक्त बनाना',
        'footer_copyright': '© 2025 कृषिसाथी एआई। सर्वाधिकार सुरक्षित।',
        'smart_assistant': 'स्मार्ट खेती सहायक',
        'show_prices': 'कीमतें दिखाएं',
        'weather_in': 'मौसम',
        'tell_about': 'गेहूं के बारे में बताएं',
        'check_disease': 'फसल रोग जांचें',
        'govt_schemes_msg': 'सरकारी योजनाओं के बारे में बताएं'
    }
}

def get_ui_text(key, lang='en'):
    """Get translated UI text"""
    return UI_TRANSLATIONS.get(lang, UI_TRANSLATIONS['en']).get(key, UI_TRANSLATIONS['en'].get(key, key))

# ---------------------- TRANSLATION FUNCTIONS ----------------------
def translate_text(text, target_lang='en', source_lang='auto'):
    """Translate text to target language"""
    if not TRANSLATION_AVAILABLE or target_lang == 'en':
        return text
    
    try:
        translator = GoogleTranslator(source='auto', target=target_lang)
        return translator.translate(text)
    except Exception as e:
        return text

def get_greeting_by_language(lang_code):
    """Return appropriate greeting based on language"""
    greetings = {
        'en': 'Namaste! Welcome to Krishisaathi AI!',
        'hi': 'नमस्ते! कृषिसाथी एआई में आपका स्वागत है!',
        'mr': 'नमस्कार! कृषिसाथी एआय मध्ये आपले स्वागत आहे!',
        'ta': 'வணக்கம்! கிருஷிசாத்தி AI-க்கு வரவேற்கிறோம்!',
        'te': 'నమస్కారం! కృషిసాథి AI కి స్వాగతం!',
        'bn': 'নমস্কার! কৃষিসাথী AI তে স্বাগতম!',
        'gu': 'નમસ્તે! કૃષિસાથી AI માં તમારું સ્વાગત છે!',
        'kn': 'ನಮಸ್ಕಾರ! ಕೃಷಿಸಾಥಿ AI ಗೆ ಸ್ವಾಗತ!',
        'ml': 'നമസ്കാരം! കൃഷിസാഥി AI യിലേക്ക് സ്വാഗതം!',
        'pa': 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਕ੍ਰਿਸ਼ੀਸਾਥੀ AI ਵਿੱਚ ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ!'
    }
    return greetings.get(lang_code, greetings['en'])

# ---------------------- GOVERNMENT SCHEMES DATA ----------------------
GOVERNMENT_SCHEMES = {
    "PM-KISAN": {
        "full_name": "Pradhan Mantri Kisan Samman Nidhi",
        "objective": "Direct income support to small and marginal farmers",
        "benefits": "₹6,000 per year in 3 installments directly into farmer's bank account",
        "eligibility": "Small and marginal farmers with landholding up to 2 hectares",
        "how_to_apply": "Apply online at pmkisan.gov.in or through Common Service Centers",
        "contact": "Call 155261 or 011-24300606"
    },
    "PMFBY": {
        "full_name": "Pradhan Mantri Fasal Bima Yojana",
        "objective": "Crop insurance covering losses from natural calamities, pests, and diseases",
        "benefits": "Low premiums (2% Kharif, 1.5% Rabi); coverage for yield loss, post-harvest loss, and localized calamities",
        "eligibility": "All farmers including sharecroppers and tenant farmers",
        "how_to_apply": "Through banks, insurance companies, or pmfby.gov.in",
        "contact": "Toll-free: 18001801551"
    },
    "KCC": {
        "full_name": "Kisan Credit Card Scheme",
        "objective": "Easy access to short-term credit for farming needs",
        "benefits": "Loans up to ₹3 lakh at 7% interest, flexible repayment options, 3% interest subvention",
        "eligibility": "All farmers owning cultivable land",
        "how_to_apply": "Visit nearest bank branch with land documents and Aadhaar card",
        "contact": "Contact your nearest bank branch"
    },
    "PMKSY": {
        "full_name": "Pradhan Mantri Krishi Sinchai Yojana",
        "objective": "Water-use efficiency and irrigation improvement - 'Har Khet Ko Pani'",
        "benefits": "Subsidies for drip & sprinkler systems (up to 55%); promotes 'More Crop Per Drop'",
        "eligibility": "All categories of farmers",
        "how_to_apply": "Through State Agriculture Department offices or online portal",
        "contact": "Visit nearest Krishi Vigyan Kendra (KVK)"
    },
    "AIF": {
        "full_name": "Agriculture Infrastructure Fund",
        "objective": "Financing post-harvest infrastructure and agri supply chains",
        "benefits": "Loans with 3% interest subvention and credit guarantee; ₹1 lakh crore scheme",
        "eligibility": "Farmers, FPOs, agri-entrepreneurs, startups, cooperatives",
        "how_to_apply": "Apply through banks or online at agriinfra.dac.gov.in",
        "contact": "Contact NABARD or participating banks"
    },
    "PKVY": {
        "full_name": "Paramparagat Krishi Vikas Yojana",
        "objective": "Promotion of organic and sustainable farming practices",
        "benefits": "₹50,000 per hectare for 3 years; support for organic clusters, certification, and marketing",
        "eligibility": "Groups of farmers (minimum 50) practicing organic farming",
        "how_to_apply": "Through State Agriculture Department under RKVY",
        "contact": "Contact State Organic Certification Agency"
    },
    "PM-KUSUM": {
        "full_name": "PM Kisan Urja Suraksha evam Utthaan Mahabhiyan",
        "objective": "Solar energy for farmers - reduce diesel dependency",
        "benefits": "30% subsidy by central govt, 30% by state; income through sale of surplus electricity to grid",
        "eligibility": "All farmers",
        "how_to_apply": "Through State Nodal Agency or online at kusum.mnre.gov.in",
        "contact": "Ministry of New and Renewable Energy helpline"
    },
    "SMAM": {
        "full_name": "Sub-Mission on Agricultural Mechanization",
        "objective": "Promoting farm mechanization to increase productivity",
        "benefits": "40-50% subsidy on tractors, harvesters, and machinery (priority to SC/ST/Women farmers)",
        "eligibility": "All farmers, with special focus on SC/ST/Women/Small farmers",
        "how_to_apply": "Through State Agriculture Department or online DBT portal",
        "contact": "Visit District Agriculture Office"
    },
    "PENSION": {
        "full_name": "PM Kisan Maan Dhan Yojana (PM-KMY)",
        "objective": "Old age pension scheme for small and marginal farmers",
        "benefits": "₹3,000 monthly pension after 60 years of age; contribution-based scheme",
        "eligibility": "Farmers aged 18-40 years with up to 2 hectares land",
        "how_to_apply": "Through Common Service Centers with Aadhaar and bank account",
        "contact": "CSC helpline: 1800-3000-3468"
    },
    "RKVY": {
        "full_name": "Rashtriya Krishi Vikas Yojana - RAFTAAR",
        "objective": "Boosting agri-development and innovation at state level",
        "benefits": "Grants for startups, infrastructure, innovation; flexible state-specific programs",
        "eligibility": "States, farmers, agri-entrepreneurs, startups",
        "how_to_apply": "Through State Agriculture Department",
        "contact": "Contact State Agriculture Mission"
    },
    "PMMSY": {
        "full_name": "Pradhan Mantri Matsya Sampada Yojana",
        "objective": "Development of fisheries and aqua-based livelihoods",
        "benefits": "40-60% subsidy for hatcheries, ponds, cold storage, and processing units",
        "eligibility": "Fish farmers, SHGs, FPOs, entrepreneurs",
        "how_to_apply": "Through Department of Fisheries or online portal",
        "contact": "Department of Fisheries helpline"
    }
}

def get_scheme_info(message):
    """Returns information about government schemes"""
    message_lower = message.lower()
    
    # Check if asking about specific scheme
    scheme_keywords = {
        'PM-KISAN': ['pm kisan', 'pmkisan', 'income support', '6000', 'direct benefit', 'samman nidhi'],
        'PMFBY': ['fasal bima', 'crop insurance', 'pmfby', 'insurance', 'bima yojana'],
        'KCC': ['kisan credit', 'kcc', 'credit card', 'loan', 'ऋण'],
        'PMKSY': ['sinchai', 'irrigation', 'pmksy', 'drip', 'sprinkler', 'सिंचाई'],
        'AIF': ['infrastructure', 'aif', 'storage', 'cold storage', 'warehouse'],
        'PKVY': ['organic', 'pkvy', 'natural farming', 'paramparagat'],
        'PM-KUSUM': ['solar', 'kusum', 'solar pump', 'renewable', 'सौर'],
        'SMAM': ['mechanization', 'tractor', 'machinery', 'equipment', 'यंत्रीकरण'],
        'PENSION': ['pension', 'maan dhan', 'retirement', 'पेंशन'],
        'RKVY': ['rkvy', 'raftaar', 'rashtriya krishi'],
        'PMMSY': ['fisheries', 'matsya', 'fish farming', 'मत्स्य']
    }
    
    # Find matching scheme
    for scheme_key, keywords in scheme_keywords.items():
        if any(keyword in message_lower for keyword in keywords):
            scheme = GOVERNMENT_SCHEMES[scheme_key]
            return f"""📋 **{scheme['full_name']}**

🎯 **Objective:**
{scheme['objective']}

💰 **Key Benefits:**
{scheme['benefits']}

✅ **Eligibility:**
{scheme['eligibility']}

📝 **How to Apply:**
{scheme['how_to_apply']}

📞 **Contact:**
{scheme['contact']}

💡 **Pro Tip:** Keep your Aadhaar, bank account, and land documents ready for smooth application process!"""
    
    # General schemes overview
    return """🏛️ **Major Government Schemes for Farmers (2025)**

**💵 Income Support & Financial Aid:**
• **PM-KISAN**: ₹6,000/year direct benefit (3 installments)
• **PM Kisan Pension**: ₹3,000/month after 60 years
• **Kisan Credit Card**: Easy loans up to ₹3 lakh at 7% interest

**🛡️ Risk Management:**
• **PM Fasal Bima Yojana**: Crop insurance with low premiums
  - 2% premium for Kharif crops
  - 1.5% premium for Rabi crops
  - Coverage for natural calamities, pests, diseases

**💧 Irrigation & Water Management:**
• **PM Krishi Sinchai Yojana**: Up to 55% subsidy on drip/sprinkler
• 'Har Khet Ko Pani' - Every farm gets water
• 'More Crop Per Drop' - Water efficiency

**☀️ Energy & Technology:**
• **PM-KUSUM**: 60% subsidy on solar pumps
  - Earn by selling surplus electricity
  - Reduce diesel costs
• **SMAM**: 40-50% subsidy on farm machinery
  - Tractors, harvesters, equipment
  - Priority for women farmers

**🏭 Infrastructure & Marketing:**
• **Agriculture Infrastructure Fund**: ₹1 lakh crore scheme
  - 3% interest subvention
  - Cold storage, warehouses, processing units
• **RKVY-RAFTAAR**: Support for innovation and startups

**🌱 Sustainable Farming:**
• **PKVY**: Organic farming support - ₹50,000/hectare for 3 years
• **Natural Farming Mission**: Chemical-free agriculture

**🐟 Fisheries:**
• **PM Matsya Sampada Yojana**: 40-60% subsidy for fish farming

**🆕 New Initiatives (October 2025):**
• ₹35,440 crore outlay for FPOs and PACS modernization
• Expansion of Farmer Producer Organizations
• Multi-service Primary Agricultural Credit Societies

**📞 Important Helplines:**
• Agriculture: **1800-180-1551** (Toll-free)
• PM-KISAN: **155261** / **011-24300606**
• Crop Insurance: **18001801551**
• CSC: **1800-3000-3468**

**🌐 Online Portals:**
• farmer.gov.in - Central portal
• pmkisan.gov.in - PM-KISAN
• pmfby.gov.in - Crop Insurance
• agriinfra.dac.gov.in - Infrastructure Fund

💬 **Ask me about specific schemes!**
Examples:
• "Tell me about PM-KISAN"
• "How to get crop insurance?"
• "What is Kisan Credit Card?"
• "Solar pump subsidy details"

📍 **Visit your nearest:**
• Krishi Vigyan Kendra (KVK)
• Common Service Center (CSC)
• District Agriculture Office
"""

# ---------------------- CSS ----------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {display: none;}
    
    .main {
        background: #1a1a1a;
        padding: 0;
    }
    
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1400px !important;
        margin: 0 auto;
    }
    
    .language-selector {
        background: linear-gradient(135deg, #2d2d2d 0%, #1f1f1f 100%);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        border: 1px solid #4caf50;
    }
    
    .stChatMessage {
        background: linear-gradient(135deg, #2d2d2d 0%, #242424 100%) !important;
        border-radius: 12px !important;
        border: 1px solid #4caf50 !important;
        margin-bottom: 1rem !important;
        padding: 1.25rem !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stChatMessage p, .stChatMessage div {
        color: #e0e0e0 !important;
    }
    
    .stChatMessage strong {
        color: #66bb6a !important;
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
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1f1f1f 0%, #2d2d2d 100%) !important;
        border-right: 2px solid #4caf50 !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #66bb6a !important;
    }
    
    .app-title {
        font-size: 2rem;
        font-weight: 800;
        color: #2e7d32;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .app-tagline {
        color: #81c784;
        font-size: 0.95rem;
        font-weight: 500;
        margin: 0.25rem 0 0 0;
    }
    
    .stTextInput input, .stChatInput textarea {
        background: #2d2d2d !important;
        color: #e0e0e0 !important;
        border: 1px solid #4caf50 !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------- INITIALIZE SESSION ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "expect_image" not in st.session_state:
    st.session_state.expect_image = False
if "selected_language" not in st.session_state:
    st.session_state.selected_language = 'en'

current_lang = st.session_state.selected_language

# ---------------------- HEADER ----------------------
header_col1, header_col2 = st.columns([1, 5])

with header_col1:
    st.markdown('<div style="font-size: 4rem; text-align: center;">🌾</div>', unsafe_allow_html=True)

with header_col2:
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; justify-content: center; height: 100%;">
        <h1 class="app-title">{get_ui_text('app_title', current_lang)}</h1>
        <p class="app-tagline">{get_ui_text('app_tagline', current_lang)}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr>', unsafe_allow_html=True)

# ---------------------- LANGUAGE SELECTOR ----------------------
st.markdown('<div class="language-selector">', unsafe_allow_html=True)
col_lang1, col_lang2 = st.columns([3, 1])

with col_lang1:
    st.markdown(f"**🌍 {get_ui_text('select_language', current_lang)}**")

with col_lang2:
    selected_lang = st.selectbox(
        "Language",
        options=list(SUPPORTED_LANGUAGES.keys()),
        format_func=lambda x: f"{SUPPORTED_LANGUAGES[x]['flag']} {SUPPORTED_LANGUAGES[x]['name']}",
        index=list(SUPPORTED_LANGUAGES.keys()).index(st.session_state.selected_language),
        label_visibility="collapsed"
    )
    
    if selected_lang != st.session_state.selected_language:
        st.session_state.selected_language = selected_lang
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- WEATHER & PRICE FUNCTIONS ----------------------
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

def get_produce_prices(state="all"):
    """Sample prices - abbreviated"""
    sample_prices = {
        "Delhi": {
            "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹14-24", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"}
        },
        "Mumbai": {
            "Tomato": {"price": "₹26-40", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹18-28", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹17-26", "unit": "per kg", "trend": "↓"}
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

def format_price_response(prices, city_name=None, vegetable_name=None):
    """Formats price data into readable response"""
    if not prices:
        return "❌ Sorry, no price data found. Try: Delhi or Mumbai."
    
    response = "💰 **Current Market Prices:**\n\n"
    
    for city, produce_data in prices.items():
        if city_name and city_name.lower() not in city.lower():
            continue
        
        response += f"📍 **{city}**\n\n"
        
        for item, data in produce_data.items():
            response += f"• **{item}**: {data['price']} {data['unit']} {data['trend']}\n"
        
        response += "\n"
    
    response += "\n📊 **Legend:** ↑ Rising | → Stable | ↓ Falling\n"
    return response

# ---------------------- DISEASE DETECTION ----------------------
def ai_predict_disease(image_file):
    """Placeholder for ML model"""
    diseases = {
        "Tomato - Late Blight": {
            "symptoms": "Dark brown spots on leaves, white mold on undersides",
            "treatment": "Remove infected leaves, apply copper-based fungicide",
            "prevention": "Avoid overhead watering, use resistant varieties"
        }
    }
    
    disease_name = random.choice(list(diseases.keys()))
    disease_info = diseases[disease_name]
    
    return {
        "name": disease_name,
        "confidence": random.randint(75, 98),
        **disease_info
    }

# ---------------------- INTENT DETECTION ----------------------
def detect_intent_multilingual(user_message):
    """Detect user intent from multilingual input"""
    message_lower = user_message.lower()
    
    # Scheme keywords
    scheme_keywords = ['scheme', 'subsidy', 'government', 'yojana', 'benefit', 'pm kisan', 
                      'insurance', 'loan', 'credit', 'pension', 'योजना', 'सब्सिडी', 'बीमा',
                      'rkvy', 'kusum', 'solar', 'fasal bima', 'kisan credit', 'organic']
    
    disease_keywords = ['disease', 'sick', 'infected', 'problem', 'leaf', 'रोग', 'बीमारी']
    price_keywords = ['price', 'cost', 'market', 'rate', 'mandi', 'कीमत', 'दाम', 'बाजार']
    weather_keywords = ['weather', 'temperature', 'rain', 'climate', 'मौसम', 'तापमान']
    crop_keywords = ['wheat', 'rice', 'crop', 'farming', 'cultivation', 'grow', 'गेहूं', 'चावल', 'फसल']
    greeting_keywords = ['hello', 'hi', 'hey', 'namaste', 'start', 'नमस्ते', 'हैलो']
    
    # Check intents
    if any(keyword in message_lower for keyword in scheme_keywords):
        return 'scheme'
    if any(keyword in message_lower for keyword in disease_keywords):
        return 'disease'
    if any(keyword in message_lower for keyword in price_keywords):
        return 'price'
    if any(keyword in message_lower for keyword in weather_keywords):
        return 'weather'
    if any(keyword in message_lower for keyword in crop_keywords):
        return 'crop'
    if any(keyword in message_lower for keyword in greeting_keywords):
        return 'greeting'
    
    return 'default'

# ---------------------- CHATBOT RESPONSE LOGIC ----------------------
def get_bot_response(user_message, user_lang='en'):
    """Generates intelligent responses"""
    
    message_en = user_message
    if TRANSLATION_AVAILABLE and user_lang != 'en':
        try:
            translator = GoogleTranslator(source='auto', target='en')
            message_en = translator.translate(user_message)
        except:
            pass
    
    intent = detect_intent_multilingual(user_message)
    response_en = ""
    
    if intent == 'scheme':
        scheme_info = get_scheme_info(message_en)
        response_en = scheme_info
    
    elif intent == 'disease':
        st.session_state.expect_image = True
        response_en = """🔬 **Crop Disease Detection**

📷 Please upload a clear photo of affected leaves or crops.

I'll analyze it and provide:
✅ Disease identification
✅ Treatment recommendations
✅ Prevention tips"""
    
    elif intent == 'price':
        city = "Delhi"  # Default
        prices = get_produce_prices(city)
        response_en = format_price_response(prices, city)
    
    elif intent == 'weather':
        weather = get_weather("Mumbai")
        if weather:
            response_en = f"""🌤️ **Weather in {weather['city']}:**
            
- Temperature: {weather['temperature']}°C (feels like {weather['feels_like']}°C)
- Conditions: {weather['description'].title()}
- Humidity: {weather['humidity']}%
- Wind: {weather['wind_speed']} m/s"""
        else:
            response_en = "❌ Couldn't fetch weather data."
    
    elif intent == 'crop':
        response_en = """🌾 **Crop Cultivation Tips**

I can help with:
• 🌾 Wheat - Rabi crop
• 🍚 Rice - Kharif crop
• 🍅 Tomato - Vegetable crop
• 🥔 Potato - Tuber crop

**Ask me:** "Tell me about wheat cultivation" """
    
    elif intent == 'greeting':
        response_en = f"""{get_greeting_by_language(user_lang)}

I can help you with:
🌤️ Weather forecasts
💰 Market prices
🌾 Crop cultivation tips
🔬 Disease detection (upload photo)
🏛️ Government schemes & subsidies

**What would you like to know?** 🚜"""
    
    else:
        response_en = """🌾 **How can I help you today?**

Ask me about:
• 🔬 Crop disease (upload photo)
• 💰 Market prices
• 🌤️ Weather updates
• 🌱 Crop tips
• 🏛️ Government schemes

**Type your question!** 🚜"""
    
    # Translate response back to user's language
    if user_lang != 'en' and TRANSLATION_AVAILABLE:
        return translate_text(response_en, target_lang=user_lang)
    
    return response_en

# ---------------------- SIDEBAR ----------------------
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 1.5rem 0 1.5rem 0; border-bottom: 1px solid rgba(76, 175, 80, 0.2);">
        <h2 style="font-size: 1.3rem; font-weight: 800; color: #66bb6a; margin: 0;">🌾 {get_ui_text('app_title', current_lang)}</h2>
        <p style="font-size: 0.8rem; color: #81c784; margin: 0.4rem 0 0 0;">{get_ui_text('smart_assistant', current_lang)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"### {get_ui_text('quick_actions', current_lang)}")
    
    if st.button(get_ui_text('disease_detection', current_lang)):
        user_msg = get_ui_text('check_disease', current_lang)
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg, st.session_state.selected_language)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
    
    if st.button(get_ui_text('delhi_prices', current_lang)):
        user_msg = f"{get_ui_text('show_prices', current_lang)} Delhi"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg, st.session_state.selected_language)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
        
    if st.button(get_ui_text('mumbai_weather', current_lang)):
        user_msg = f"{get_ui_text('weather_in', current_lang)} Mumbai"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg, st.session_state.selected_language)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
        
    if st.button(get_ui_text('crop_tips', current_lang)):
        user_msg = get_ui_text('tell_about', current_lang)
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg, st.session_state.selected_language)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
    
    if st.button(get_ui_text('govt_schemes', current_lang)):
        user_msg = get_ui_text('govt_schemes_msg', current_lang)
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_response = get_bot_response(user_msg, st.session_state.selected_language)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.rerun()
    
    st.divider()
    
    if st.button(get_ui_text('clear_chat', current_lang)):
        st.session_state.messages = []
        st.session_state.expect_image = False
        st.rerun()

# ---------------------- CHAT INTERFACE ----------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------- IMAGE UPLOAD ----------------------
if st.session_state.expect_image:
    st.subheader(get_ui_text('upload_image', current_lang))
    
    uploaded_file = st.file_uploader(
        get_ui_text('choose_image', current_lang), 
        type=["jpg", "png", "jpeg"]
    )
    
    if uploaded_file:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(uploaded_file, caption=get_ui_text('uploaded_image', current_lang), use_container_width=True)
        
        with col2:
            with st.spinner(get_ui_text('analyzing', current_lang)):
                prediction = ai_predict_disease(uploaded_file)
                
                st.success(get_ui_text('detection_complete', current_lang))
                st.metric(get_ui_text('disease', current_lang), prediction['name'])
                st.metric(get_ui_text('confidence', current_lang), f"{prediction['confidence']}%")
        
        if st.button(get_ui_text('done', current_lang)):
            st.session_state.expect_image = False
            result_msg = f"""✅ **Disease Detection Complete**

**Identified:** {prediction['name']} ({prediction['confidence']}% confidence)

**Symptoms:** {prediction['symptoms']}

**Treatment:** {prediction['treatment']}"""
            
            if st.session_state.selected_language != 'en':
                result_msg = translate_text(result_msg, target_lang=st.session_state.selected_language)
            
            st.session_state.messages.append({"role": "assistant", "content": result_msg})
            st.rerun()

# ---------------------- CHAT INPUT ----------------------
if prompt := st.chat_input(get_ui_text('chat_placeholder', current_lang)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner(get_ui_text('thinking', current_lang)):
            response = get_bot_response(prompt, st.session_state.selected_language)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# ---------------------- FOOTER ----------------------
st.markdown(f"""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); border-radius: 12px; margin-top: 3rem; border: 1px solid #4caf50;">
    <p style="color: #66bb6a; font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem;">{get_ui_text('footer_title', current_lang)}</p>
    <p style="color: #81c784; font-size: 0.9rem; margin-bottom: 0;">{get_ui_text('footer_tagline', current_lang)}</p>
    <p style="color: #a5d6a7; font-size: 0.8rem; margin-top: 1rem;">{get_ui_text('footer_copyright', current_lang)}</p>
</div>
""", unsafe_allow_html=True)
