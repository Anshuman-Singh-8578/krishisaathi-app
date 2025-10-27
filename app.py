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
        'check_disease': 'Check crop disease'
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
        'check_disease': 'फसल रोग जांचें'
    },
    'mr': {
        'app_title': 'कृषिसाथी एआय',
        'app_tagline': 'शेतकऱ्यांना जोडणे, वाढीस सक्षम करणे',
        'select_language': 'तुमची भाषा निवडा',
        'quick_actions': '🎯 जलद क्रिया',
        'disease_detection': '📷 रोग ओळख',
        'delhi_prices': '🏙️ दिल्ली किमती',
        'mumbai_weather': '🌤️ मुंबई हवामान',
        'crop_tips': '🌾 पीक सूचना',
        'clear_chat': '🗑️ चॅट साफ करा',
        'upload_image': '📸 पिकाचा फोटो अपलोड करा',
        'choose_image': 'एक प्रतिमा निवडा',
        'uploaded_image': 'अपलोड केलेली प्रतिमा',
        'analyzing': '🔬 विश्लेषण करत आहे...',
        'detection_complete': '✅ ओळख पूर्ण!',
        'disease': 'रोग',
        'confidence': 'विश्वास',
        'done': '✅ पूर्ण',
        'chat_placeholder': 'शेतीबद्दल विचारा...',
        'thinking': '🌱 विचार करत आहे...',
        'footer_title': '🌾 कृषिसाथी एआय',
        'footer_tagline': 'तंत्रज्ञानाद्वारे शेतकऱ्यांना सक्षम करणे',
        'footer_copyright': '© 2025 कृषिसाथी एआय. सर्व हक्क राखीव.',
        'smart_assistant': 'स्मार्ट शेती सहाय्यक',
        'show_prices': 'किमती दाखवा',
        'weather_in': 'हवामान',
        'tell_about': 'गव्हाबद्दल सांगा',
        'check_disease': 'पीक रोग तपासा'
    },
    'ta': {
        'app_title': 'கிருஷிசாத்தி AI',
        'app_tagline': 'விவசாயிகளை இணைத்தல், வளர்ச்சியை மேம்படுத்துதல்',
        'select_language': 'உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்',
        'quick_actions': '🎯 விரைவு செயல்கள்',
        'disease_detection': '📷 நோய் கண்டறிதல்',
        'delhi_prices': '🏙️ டெல்லி விலைகள்',
        'mumbai_weather': '🌤️ மும்பை வானிலை',
        'crop_tips': '🌾 பயிர் குறிப்புகள்',
        'clear_chat': '🗑️ அரட்டையை அழி',
        'upload_image': '📸 பயிர் படத்தை பதிவேற்றவும்',
        'choose_image': 'படத்தைத் தேர்ந்தெடுக்கவும்',
        'uploaded_image': 'பதிவேற்றப்பட்ட படம்',
        'analyzing': '🔬 பகுப்பாய்வு செய்கிறது...',
        'detection_complete': '✅ கண்டறிதல் முடிந்தது!',
        'disease': 'நோய்',
        'confidence': 'நம்பிக்கை',
        'done': '✅ முடிந்தது',
        'chat_placeholder': 'விவசாயம் பற்றி கேளுங்கள்...',
        'thinking': '🌱 சிந்திக்கிறது...',
        'footer_title': '🌾 கிருஷிசாத்தி AI',
        'footer_tagline': 'தொழில்நுட்பத்துடன் விவசாயிகளை மேம்படுத்துதல்',
        'footer_copyright': '© 2025 கிருஷிசாத்தி AI. அனைத்து உரிமைகளும் பாதுகாக்கப்பட்டவை.',
        'smart_assistant': 'ஸ்மார்ட் விவசாய உதவியாளர்',
        'show_prices': 'விலைகளைக் காட்டு',
        'weather_in': 'வானிலை',
        'tell_about': 'கோதுமை பற்றி சொல்லுங்கள்',
        'check_disease': 'பயிர் நோயைச் சரிபார்க்கவும்'
    },
    'te': {
        'app_title': 'కృషిసాథి AI',
        'app_tagline': 'రైతులను కలుపుతూ, వృద్ధిని శక్తివంతం చేయడం',
        'select_language': 'మీ భాషను ఎంచుకోండి',
        'quick_actions': '🎯 త్వరిత చర్యలు',
        'disease_detection': '📷 వ్యాధి గుర్తింపు',
        'delhi_prices': '🏙️ ఢిల్లీ ధరలు',
        'mumbai_weather': '🌤️ ముంబై వాతావరణం',
        'crop_tips': '🌾 పంట చిట్కాలు',
        'clear_chat': '🗑️ చాట్ క్లియర్ చేయండి',
        'upload_image': '📸 పంట చిత్రాన్ని అప్‌లోడ్ చేయండి',
        'choose_image': 'చిత్రాన్ని ఎంచుకోండి',
        'uploaded_image': 'అప్‌లోడ్ చేసిన చిత్రం',
        'analyzing': '🔬 విశ్లేషిస్తోంది...',
        'detection_complete': '✅ గుర్తింపు పూర్తయింది!',
        'disease': 'వ్యాధి',
        'confidence': 'విశ్వాసం',
        'done': '✅ పూర్తయింది',
        'chat_placeholder': 'వ్యవసాయం గురించి అడగండి...',
        'thinking': '🌱 ఆలోచిస్తోంది...',
        'footer_title': '🌾 కృషిసాథి AI',
        'footer_tagline': 'సాంకేతికతతో రైతులను శక్తివంతం చేయడం',
        'footer_copyright': '© 2025 కృషిసాథి AI. అన్ని హక్కులూ రక్షించబడ్డాయి.',
        'smart_assistant': 'స్మార్ట్ వ్యవసాయ సహాయకుడు',
        'show_prices': 'ధరలను చూపించు',
        'weather_in': 'వాతావరణం',
        'tell_about': 'గోధుమల గురించి చెప్పండి',
        'check_disease': 'పంట వ్యాధిని తనిఖీ చేయండి'
    },
    'bn': {
        'app_title': 'কৃষিসাথী AI',
        'app_tagline': 'কৃষকদের সংযোগ, বৃদ্ধিকে ক্ষমতায়ন',
        'select_language': 'আপনার ভাষা নির্বাচন করুন',
        'quick_actions': '🎯 দ্রুত ক্রিয়া',
        'disease_detection': '📷 রোগ সনাক্তকরণ',
        'delhi_prices': '🏙️ দিল্লির দাম',
        'mumbai_weather': '🌤️ মুম্বাই আবহাওয়া',
        'crop_tips': '🌾 ফসলের টিপস',
        'clear_chat': '🗑️ চ্যাট মুছুন',
        'upload_image': '📸 ফসলের ছবি আপলোড করুন',
        'choose_image': 'একটি ছবি নির্বাচন করুন',
        'uploaded_image': 'আপলোড করা ছবি',
        'analyzing': '🔬 বিশ্লেষণ করা হচ্ছে...',
        'detection_complete': '✅ সনাক্তকরণ সম্পূর্ণ!',
        'disease': 'রোগ',
        'confidence': 'আত্মবিশ্বাস',
        'done': '✅ সম্পন্ন',
        'chat_placeholder': 'কৃষি সম্পর্কে জিজ্ঞাসা করুন...',
        'thinking': '🌱 চিন্তা করছে...',
        'footer_title': '🌾 কৃষিসাথী AI',
        'footer_tagline': 'প্রযুক্তির সাথে কৃষকদের ক্ষমতায়ন',
        'footer_copyright': '© 2025 কৃষিসাথী AI. সমস্ত অধিকার সংরক্ষিত।',
        'smart_assistant': 'স্মার্ট কৃষি সহায়ক',
        'show_prices': 'দাম দেখান',
        'weather_in': 'আবহাওয়া',
        'tell_about': 'গম সম্পর্কে বলুন',
        'check_disease': 'ফসল রোগ পরীক্ষা করুন'
    },
    'gu': {
        'app_title': 'કૃષિસાથી AI',
        'app_tagline': 'ખેડૂતોને જોડવા, વૃદ્ધિને સશક્ત બનાવવી',
        'select_language': 'તમારી ભાષા પસંદ કરો',
        'quick_actions': '🎯 ઝડપી ક્રિયાઓ',
        'disease_detection': '📷 રોગ શોધ',
        'delhi_prices': '🏙️ દિલ્હી ભાવ',
        'mumbai_weather': '🌤️ મુંબઈ હવામાન',
        'crop_tips': '🌾 પાક ટીપ્સ',
        'clear_chat': '🗑️ ચેટ સાફ કરો',
        'upload_image': '📸 પાકનું ચિત્ર અપલોડ કરો',
        'choose_image': 'એક છબી પસંદ કરો',
        'uploaded_image': 'અપલોડ કરેલ છબી',
        'analyzing': '🔬 વિશ્લેષણ કરી રહ્યા છીએ...',
        'detection_complete': '✅ શોધ પૂર્ણ!',
        'disease': 'રોગ',
        'confidence': 'વિશ્વાસ',
        'done': '✅ પૂર્ણ',
        'chat_placeholder': 'ખેતી વિશે પૂછો...',
        'thinking': '🌱 વિચારી રહ્યા છીએ...',
        'footer_title': '🌾 કૃષિસાથી AI',
        'footer_tagline': 'ટેકનોલોજી સાથે ખેડૂતોને સશક્ત બનાવવા',
        'footer_copyright': '© 2025 કૃષિસાથી AI. બધા અધિકારો અનામત.',
        'smart_assistant': 'સ્માર્ટ ખેતી સહાયક',
        'show_prices': 'ભાવ બતાવો',
        'weather_in': 'હવામાન',
        'tell_about': 'ઘઉં વિશે કહો',
        'check_disease': 'પાક રોગ તપાસો'
    },
    'kn': {
        'app_title': 'ಕೃಷಿಸಾಥಿ AI',
        'app_tagline': 'ರೈತರನ್ನು ಸಂಪರ್ಕಿಸುವುದು, ಬೆಳವಣಿಗೆಯನ್ನು ಸಶಕ್ತಗೊಳಿಸುವುದು',
        'select_language': 'ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ',
        'quick_actions': '🎯 ತ್ವರಿತ ಕ್ರಿಯೆಗಳು',
        'disease_detection': '📷 ರೋಗ ಪತ್ತೆ',
        'delhi_prices': '🏙️ ದೆಹಲಿ ಬೆಲೆಗಳು',
        'mumbai_weather': '🌤️ ಮುಂಬೈ ಹವಾಮಾನ',
        'crop_tips': '🌾 ಬೆಳೆ ಸಲಹೆಗಳು',
        'clear_chat': '🗑️ ಚಾಟ್ ತೆರವುಗೊಳಿಸಿ',
        'upload_image': '📸 ಬೆಳೆ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ',
        'choose_image': 'ಚಿತ್ರವನ್ನು ಆಯ್ಕೆಮಾಡಿ',
        'uploaded_image': 'ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಚಿತ್ರ',
        'analyzing': '🔬 ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...',
        'detection_complete': '✅ ಪತ್ತೆ ಪೂರ್ಣಗೊಂಡಿದೆ!',
        'disease': 'ರೋಗ',
        'confidence': 'ವಿಶ್ವಾಸ',
        'done': '✅ ಪೂರ್ಣಗೊಂಡಿದೆ',
        'chat_placeholder': 'ಕೃಷಿ ಬಗ್ಗೆ ಕೇಳಿ...',
        'thinking': '🌱 ಯೋಚಿಸುತ್ತಿದೆ...',
        'footer_title': '🌾 ಕೃಷಿಸಾಥಿ AI',
        'footer_tagline': 'ತಂತ್ರಜ್ಞಾನದೊಂದಿಗೆ ರೈತರನ್ನು ಸಶಕ್ತಗೊಳಿಸುವುದು',
        'footer_copyright': '© 2025 ಕೃಷಿಸಾಥಿ AI. ಎಲ್ಲಾ ಹಕ್ಕುಗಳನ್ನು ಕಾಯ್ದಿರಿಸಲಾಗಿದೆ.',
        'smart_assistant': 'ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ಸಹಾಯಕ',
        'show_prices': 'ಬೆಲೆಗಳನ್ನು ತೋರಿಸಿ',
        'weather_in': 'ಹವಾಮಾನ',
        'tell_about': 'ಗೋಧಿ ಬಗ್ಗೆ ಹೇಳಿ',
        'check_disease': 'ಬೆಳೆ ರೋಗವನ್ನು ಪರಿಶೀಲಿಸಿ'
    },
    'ml': {
        'app_title': 'കൃഷിസാഥി AI',
        'app_tagline': 'കർഷകരെ ബന്ധിപ്പിക്കൽ, വളർച്ചയെ ശാക്തീകരിക്കൽ',
        'select_language': 'നിങ്ങളുടെ ഭാഷ തിരഞ്ഞെടുക്കുക',
        'quick_actions': '🎯 പെട്ടെന്നുള്ള പ്രവർത്തനങ്ങൾ',
        'disease_detection': '📷 രോഗം കണ്ടെത്തൽ',
        'delhi_prices': '🏙️ ഡൽഹി വിലകൾ',
        'mumbai_weather': '🌤️ മുംബൈ കാലാവസ്ഥ',
        'crop_tips': '🌾 വിള നുറുങ്ങുകൾ',
        'clear_chat': '🗑️ ചാറ്റ് മായ്ക്കുക',
        'upload_image': '📸 വിള ചിത്രം അപ്‌ലോഡ് ചെയ്യുക',
        'choose_image': 'ഒരു ചിത്രം തിരഞ്ഞെടുക്കുക',
        'uploaded_image': 'അപ്‌ലോഡ് ചെയ്ത ചിത്രം',
        'analyzing': '🔬 വിശകലനം നടത്തുന്നു...',
        'detection_complete': '✅ കണ്ടെത്തൽ പൂർത്തിയായി!',
        'disease': 'രോഗം',
        'confidence': 'വിശ്വാസം',
        'done': '✅ പൂർത്തിയായി',
        'chat_placeholder': 'കൃഷിയെക്കുറിച്ച് ചോദിക്കുക...',
        'thinking': '🌱 ചിന്തിക്കുന്നു...',
        'footer_title': '🌾 കൃഷിസാഥി AI',
        'footer_tagline': 'സാങ്കേതികവിദ്യയിലൂടെ കർഷകരെ ശാക്തീകരിക്കൽ',
        'footer_copyright': '© 2025 കൃഷിസാഥി AI. എല്ലാ അവകാശങ്ങളും സംരക്ഷിതം.',
        'smart_assistant': 'സ്മാർട്ട് കൃഷി സഹായി',
        'show_prices': 'വിലകൾ കാണിക്കുക',
        'weather_in': 'കാലാവസ്ഥ',
        'tell_about': 'ഗോതമ്പിനെക്കുറിച്ച് പറയുക',
        'check_disease': 'വിള രോഗം പരിശോധിക്കുക'
    },
    'pa': {
        'app_title': 'ਕ੍ਰਿਸ਼ੀਸਾਥੀ AI',
        'app_tagline': 'ਕਿਸਾਨਾਂ ਨੂੰ ਜੋੜਨਾ, ਵਿਕਾਸ ਨੂੰ ਸਸ਼ਕਤ ਬਣਾਉਣਾ',
        'select_language': 'ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ',
        'quick_actions': '🎯 ਤੇਜ਼ ਕਾਰਵਾਈਆਂ',
        'disease_detection': '📷 ਬਿਮਾਰੀ ਪਛਾਣ',
        'delhi_prices': '🏙️ ਦਿੱਲੀ ਕੀਮਤਾਂ',
        'mumbai_weather': '🌤️ ਮੁੰਬਈ ਮੌਸਮ',
        'crop_tips': '🌾 ਫਸਲ ਸੁਝਾਅ',
        'clear_chat': '🗑️ ਚੈਟ ਸਾਫ਼ ਕਰੋ',
        'upload_image': '📸 ਫਸਲ ਦੀ ਤਸਵੀਰ ਅੱਪਲੋਡ ਕਰੋ',
        'choose_image': 'ਇੱਕ ਤਸਵੀਰ ਚੁਣੋ',
        'uploaded_image': 'ਅੱਪਲੋਡ ਕੀਤੀ ਤਸਵੀਰ',
        'analyzing': '🔬 ਵਿਸ਼ਲੇਸ਼ਣ ਕਰ ਰਹੇ ਹਾਂ...',
        'detection_complete': '✅ ਪਛਾਣ ਪੂਰੀ!',
        'disease': 'ਬਿਮਾਰੀ',
        'confidence': 'ਵਿਸ਼ਵਾਸ',
        'done': '✅ ਪੂਰਾ',
        'chat_placeholder': 'ਖੇਤੀ ਬਾਰੇ ਪੁੱਛੋ...',
        'thinking': '🌱 ਸੋਚ ਰਹੇ ਹਾਂ...',
        'footer_title': '🌾 ਕ੍ਰਿਸ਼ੀਸਾਥੀ AI',
        'footer_tagline': 'ਤਕਨਾਲੋਜੀ ਨਾਲ ਕਿਸਾਨਾਂ ਨੂੰ ਸਸ਼ਕਤ ਬਣਾਉਣਾ',
        'footer_copyright': '© 2025 ਕ੍ਰਿਸ਼ੀਸਾਥੀ AI. ਸਾਰੇ ਅਧਿਕਾਰ ਰਾਖਵੇਂ.',
        'smart_assistant': 'ਸਮਾਰਟ ਖੇਤੀ ਸਹਾਇਕ',
        'show_prices': 'ਕੀਮਤਾਂ ਦਿਖਾਓ',
        'weather_in': 'ਮੌਸਮ',
        'tell_about': 'ਕਣਕ ਬਾਰੇ ਦੱਸੋ',
        'check_disease': 'ਫਸਲ ਬਿਮਾਰੀ ਜਾਂਚੋ'
    }
}

def get_ui_text(key, lang='en'):
    """Get translated UI text"""
    return UI_TRANSLATIONS.get(lang, UI_TRANSLATIONS['en']).get(key, UI_TRANSLATIONS['en'][key])

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
    
    .stTextInput input:focus, .stChatInput textarea:focus {
        border-color: #66bb6a !important;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2) !important;
    }
    
    .stChatInput {
        background: transparent !important;
    }
    
    .stChatInput > div {
        background: #2d2d2d !important;
        border: 2px solid #4caf50 !important;
        border-radius: 12px !important;
        padding: 0 !important;
    }
    
    .stChatInput textarea {
        padding: 1rem 1.5rem !important;
        min-height: 50px !important;
        font-size: 0.95rem !important;
    }
    
    .stChatInput button {
        background: linear-gradient(135deg, #4caf50 0%, #66bb6a 100%) !important;
        border: none !important;
        border-radius: 8px !important;
        margin: 4px !important;
        padding: 0.5rem 1rem !important;
    }
    
    .stChatInput button:hover {
        background: linear-gradient(135deg, #66bb6a 0%, #81c784 100%) !important;
        transform: scale(1.05);
    }
    
    [data-testid="stFileUploader"] {
        background: #2d2d2d !important;
        border: 2px dashed #4caf50 !important;
        border-radius: 12px !important;
        padding: 2rem !important;
    }
    
    [data-testid="stFileUploader"] * {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #2d2d2d 0%, #242424 100%) !important;
        border: 1px solid #4caf50 !important;
        border-radius: 10px !important;
        padding: 1rem !important;
    }
    
    [data-testid="stMetric"] * {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #81c784 !important;
    }
    
    .stSelectbox select {
        background: #2d2d2d !important;
        color: #e0e0e0 !important;
        border: 1px solid #4caf50 !important;
    }
    
    .stSpinner > div {
        border-top-color: #66bb6a !important;
    }
    
    hr {
        border-color: #4caf50 !important;
        opacity: 0.3;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------- INITIALIZE SESSION ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_location" not in st.session_state:
    st.session_state.user_location = None
if "expect_image" not in st.session_state:
    st.session_state.expect_image = False
if "selected_language" not in st.session_state:
    st.session_state.selected_language = 'en'

# Get current language
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

# ---------------------- PRICE FUNCTION (shortened for space) ----------------------
def get_produce_prices(state="all"):
    """Sample prices - using abbreviated version"""
    sample_prices = {
        "Delhi": {
            "Tomato": {"price": "₹22-36", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹14-24", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹15-23", "unit": "per kg", "trend": "↓"},
        },
        "Mumbai": {
            "Tomato": {"price": "₹26-40", "unit": "per kg", "trend": "↓"},
            "Potato": {"price": "₹18-28", "unit": "per kg", "trend": "→"},
            "Onion": {"price": "₹17-26", "unit": "per kg", "trend": "↓"},
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

# ---------------------- EXTRACT CITY ----------------------
def extract_city_and_vegetable_from_message(message):
    """Extracts both city name and vegetable name from user message"""
    message_lower = message.lower()
    
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
    
    vegetable = None
    produce_list = ["tomato", "potato", "onion", "cabbage"]
    
    for produce in produce_list:
        if produce in message_lower:
            vegetable = produce
            break
    
    return city, vegetable

# ---------------------- FORMAT PRICE RESPONSE ----------------------
def format_price_response(prices, city_name=None, vegetable_name=None):
    """Formats price data into readable response"""
    if not prices:
        return "❌ Sorry, no price data found. Try: Delhi or Mumbai."
    
    response = "💰 **Current Market Prices:**\n\n"
    
    for city, produce_data in prices.items():
        if city_name and city_name.lower() not in city.lower():
            continue
        
        response += f"📍 **{city}**\n\n"
        
        if vegetable_name:
            found = False
            for item, data in produce_data.items():
                if vegetable_name.lower() in item.lower():
                    response += f"• **{item}**: {data['price']} {data['unit']} {data['trend']}\n"
                    found = True
            
            if not found:
                response += f"❌ {vegetable_name.title()} price not available for {city}\n"
        else:
            for item, data in produce_data.items():
                response += f"• **{item}**: {data['price']} {data['unit']} {data['trend']}\n"
        
        response += "\n"
    
    response += "\n📊 **Legend:** → Rising | → Stable | ↓ Falling\n"
    
    return response

# ---------------------- MULTILINGUAL KEYWORD DETECTION ----------------------
def detect_intent_multilingual(user_message):
    """Detect user intent from multilingual input"""
    # Translate user message to English for intent detection
    if TRANSLATION_AVAILABLE:
        try:
            translator = GoogleTranslator(source='auto', target='en')
            message_en = translator.translate(user_message).lower()
        except:
            message_en = user_message.lower()
    else:
        message_en = user_message.lower()
    
    # Also check original message
    message_lower = user_message.lower()
    
    # Multilingual keywords for each intent
    disease_keywords = {
        'en': ['disease', 'sick', 'infected', 'diagnose', 'problem', 'leaf'],
        'hi': ['रोग', 'बीमार', 'संक्रमित', 'पत्ती', 'समस्या'],
        'mr': ['रोग', 'आजारी', 'संक्रमित', 'पान', 'समस्या'],
        'ta': ['நோய்', 'நோயுற்ற', 'தொற்று', 'இலை', 'பிரச்சனை'],
        'te': ['వ్యాధి', 'అనారోగ్యం', 'సోకిన', 'ఆకు', 'సమస్య'],
        'bn': ['রোগ', 'অসুস্থ', 'সংক্রমিত', 'পাতা', 'সমস্যা'],
        'gu': ['રોગ', 'બીમાર', 'ચેપગ્રસ્ત', 'પાન', 'સમસ્યા'],
        'kn': ['ರೋಗ', 'ಅನಾರೋಗ್ಯ', 'ಸೋಂಕು', 'ಎಲೆ', 'ಸಮಸ್ಯೆ'],
        'ml': ['രോഗം', 'അസുഖം', 'രോഗബാധ', 'ഇല', 'പ്രശ്നം'],
        'pa': ['ਬਿਮਾਰੀ', 'ਬੀਮਾਰ', 'ਸੰਕਰਮਿਤ', 'ਪੱਤਾ', 'ਸਮੱਸਿਆ']
    }
    
    price_keywords = {
        'en': ['price', 'cost', 'market', 'rate', 'mandi'],
        'hi': ['कीमत', 'दाम', 'बाजार', 'मंडी', 'भाव'],
        'mr': ['किंमत', 'दर', 'बाजार', 'मंडी'],
        'ta': ['விலை', 'சந்தை', 'வீதம்'],
        'te': ['ధర', 'మార్కెట్', 'మండి'],
        'bn': ['দাম', 'বাজার', 'মণ্ডি'],
        'gu': ['કિંમત', 'બજાર', 'મંડી'],
        'kn': ['ಬೆಲೆ', 'ಮಾರುಕಟ್ಟೆ', 'ಮಂಡಿ'],
        'ml': ['വില', 'മാർക്കറ്റ്', 'മണ്ഡി'],
        'pa': ['ਕੀਮਤ', 'ਬਾਜ਼ਾਰ', 'ਮੰਡੀ']
    }
    
    weather_keywords = {
        'en': ['weather', 'temperature', 'rain', 'climate'],
        'hi': ['मौसम', 'तापमान', 'बारिश', 'जलवायु'],
        'mr': ['हवामान', 'तापमान', 'पाऊस'],
        'ta': ['வானிலை', 'வெப்பநிலை', 'மழை'],
        'te': ['వాతావరణం', 'ఉష్ణోగ్రత', 'వర్షం'],
        'bn': ['আবহাওয়া', 'তাপমাত্রা', 'বৃষ্টি'],
        'gu': ['હવામાન', 'તાપમાન', 'વરસાદ'],
        'kn': ['ಹವಾಮಾನ', 'ತಾಪಮಾನ', 'ಮಳೆ'],
        'ml': ['കാലാവസ്ഥ', 'താപനില', 'മഴ'],
        'pa': ['ਮੌਸਮ', 'ਤਾਪਮਾਨ', 'ਮੀਂਹ']
    }
    
    crop_keywords = {
        'en': ['wheat', 'rice', 'crop', 'farming', 'cultivation', 'grow'],
        'hi': ['गेहूं', 'चावल', 'फसल', 'खेती', 'उगाना'],
        'mr': ['गहू', 'भात', 'पीक', 'शेती'],
        'ta': ['கோதுமை', 'அரிசி', 'பயிர்', 'விவசாயம்'],
        'te': ['గోధుమ', 'వరి', 'పంట', 'వ్యవసాయం'],
        'bn': ['গম', 'চাল', 'ফসল', 'চাষ'],
        'gu': ['ઘઉં', 'ચોખા', 'પાક', 'ખેતી'],
        'kn': ['ಗೋಧಿ', 'ಅಕ್ಕಿ', 'ಬೆಳೆ', 'ಕೃಷಿ'],
        'ml': ['ഗോതമ്പ്', 'അരി', 'വിള', 'കൃഷി'],
        'pa': ['ਕਣਕ', 'ਚੌਲ', 'ਫਸਲ', 'ਖੇਤੀ']
    }
    
    greeting_keywords = {
        'en': ['hello', 'hi', 'hey', 'namaste', 'start'],
        'hi': ['नमस्ते', 'हैलो', 'हाय', 'शुरू'],
        'mr': ['नमस्कार', 'हॅलो', 'सुरू'],
        'ta': ['வணக்கம்', 'ஹலோ', 'தொடங்கு'],
        'te': ['నమస్కారం', 'హలో', 'ప్రారంభం'],
        'bn': ['নমস্কার', 'হ্যালো', 'শুরু'],
        'gu': ['નમસ્તે', 'હેલો', 'શરૂ'],
        'kn': ['ನಮಸ್ಕಾರ', 'ಹಲೋ', 'ಪ್ರಾರಂಭ'],
        'ml': ['നമസ്കാരം', 'ഹലോ', 'ആരംഭിക്കുക'],
        'pa': ['ਸਤ ਸ੍ਰੀ ਅਕਾਲ', 'ਹੈਲੋ', 'ਸ਼ੁਰੂ']
    }
    
    # Check for disease intent
    for lang_keywords in disease_keywords.values():
        if any(keyword in message_lower for keyword in lang_keywords):
            return 'disease'
    if any(word in message_en for word in disease_keywords['en']):
        return 'disease'
    
    # Check for price intent
    for lang_keywords in price_keywords.values():
        if any(keyword in message_lower for keyword in lang_keywords):
            return 'price'
    if any(word in message_en for word in price_keywords['en']):
        return 'price'
    
    # Check for weather intent
    for lang_keywords in weather_keywords.values():
        if any(keyword in message_lower for keyword in lang_keywords):
            return 'weather'
    if any(word in message_en for word in weather_keywords['en']):
        return 'weather'
    
    # Check for crop tips intent
    for lang_keywords in crop_keywords.values():
        if any(keyword in message_lower for keyword in lang_keywords):
            return 'crop'
    if any(word in message_en for word in crop_keywords['en']):
        return 'crop'
    
    # Check for greeting intent
    for lang_keywords in greeting_keywords.values():
        if any(keyword in message_lower for keyword in lang_keywords):
            return 'greeting'
    if any(word in message_en for word in greeting_keywords['en']):
        return 'greeting'
    
    return 'default'

# ---------------------- CHATBOT RESPONSE LOGIC ----------------------
def get_bot_response(user_message, user_lang='en'):
    """Generates intelligent responses with multilingual understanding"""
    
    # Translate user message to English for processing
    message_en = user_message
    if TRANSLATION_AVAILABLE and user_lang != 'en':
        try:
            translator = GoogleTranslator(source='auto', target='en')
            message_en = translator.translate(user_message)
        except:
            pass
    
    # Detect intent from multilingual input
    intent = detect_intent_multilingual(user_message)
    response_en = ""
    
    if intent == 'disease':
        st.session_state.expect_image = True
        response_en = """🔬 **Crop Disease Detection**

📷 Please upload a clear photo of affected leaves or crops.

I'll analyze it and provide:
✅ Disease identification
✅ Treatment recommendations
✅ Prevention tips"""
    
    elif intent == 'price':
        city, vegetable = extract_city_and_vegetable_from_message(message_en)
        
        if city:
            prices = get_produce_prices(city)
            if prices:
                response_en = format_price_response(prices, city, vegetable)
            else:
                response_en = f"❌ Sorry, I don't have price data for '{city}'. Try: Delhi or Mumbai."
        else:
            response_en = """💰 **Market Prices Available!**

🏆 **Cities Covered:** Delhi, Mumbai, and more!

💬 **Ask me:** 
• "Tomato price in Mumbai"
• "Show onion prices in Delhi"

🔍 Type your city and vegetable name!"""
    
    elif intent == 'weather':
        city, _ = extract_city_and_vegetable_from_message(message_en)
        
        if not city:
            response_en = "🔍 Please specify a location!\nExample: 'Weather in Delhi'"
        else:
            weather = get_weather(city)
            if weather:
                response_en = f"""🌤️ **Weather in {weather['city']}:**
            
- Temperature: {weather['temperature']}°C (feels like {weather['feels_like']}°C)
- Conditions: {weather['description'].title()}
- Humidity: {weather['humidity']}%
- Wind: {weather['wind_speed']} m/s

**Advice:** {"Good for outdoor work! 🌞" if weather['temperature'] > 15 else "Indoor tasks recommended. 🧥"}"""
            else:
                response_en = f"❌ Couldn't fetch weather for '{city}'."
    
    elif intent == 'crop':
        response_en = """🌾 **Wheat Cultivation Guide**

**Climate:** 10-25°C, 50-75 cm rainfall
**Soil:** Well-drained loamy soil, pH 6.0-7.0
**Planting:** October-November, 100-125 kg/hectare
**Irrigation:** 4-6 times during critical stages
**Harvesting:** 120-150 days

💡 **Tips:** Use certified seeds, crop rotation, proper drainage"""
    
    elif intent == 'greeting':
        response_en = f"""{get_greeting_by_language(user_lang)}

I can help you with:
🌤️ Weather forecasts
💰 Market prices
🌾 Crop cultivation tips
🔬 Disease detection (upload photo)

**What would you like to know?** 🚜"""
    
    else:
        response_en = """🌾 **How can I help you today?**

Ask me about:
• 🔬 Crop disease (upload photo)
• 💰 Market prices
• 🌤️ Weather updates
• 🌱 Crop tips

**Type your question!** 🚜"""
    
    # Translate response back to user's language
    if user_lang != 'en':
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
