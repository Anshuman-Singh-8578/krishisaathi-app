# 🌾 Agri Sense AI Chatbot

An intelligent farming assistant built with Streamlit that provides real-time weather updates, market prices, and agricultural advice to farmers.

## ✨ Features

- 🌤️ **Real-time Weather Updates** - Get weather information for any city
- 💰 **Live Market Prices** - Daily commodity prices from Indian Government API
- 🌾 **Crop Advice** - Detailed farming tips for various crops
- 🐛 **Pest Management** - Organic pest control solutions
- 💧 **Irrigation Tips** - Best practices for water management
- 🌱 **Organic Farming** - Sustainable agriculture practices
- 📅 **Seasonal Planning** - Season-specific farming guidance

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/agri-sense-ai.git
cd agri-sense-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🔑 API Configuration

### Weather API (Required)
The app uses OpenWeatherMap API for weather data:
- API Key is included in the code for demonstration
- For production use, get your own key from [OpenWeatherMap](https://openweathermap.org/api)
- Replace the API_KEY in the `get_weather()` function

### Price Data APIs

**Primary:** Indian Government Open Data API
- ✅ No API key required
- ✅ Real mandi prices
- Source: [data.gov.in](https://data.gov.in)

**Secondary (Optional):** API-Ninjas
- Get free API key from [API-Ninjas](https://api-ninjas.com/)
- Replace `YOUR_API_NINJAS_KEY` in the code

## 📖 Usage

### Example Queries

**Weather:**
- "What's the weather in Delhi?"
- "Temperature in Mumbai"
- "Weather forecast for Bangalore"

**Market Prices:**
- "Show prices in Delhi"
- "Tomato price in Mumbai"
- "Market rates for Bangalore"
- "Vegetable prices in Chennai"

**Farming Advice:**
- "How to grow wheat?"
- "Tell me about tomato farming"
- "Pest control for aphids"
- "Irrigation best practices"

**Set Default Location:**
- "I'm in Delhi"
- "My location is Mumbai"

## 🛠️ Tech Stack

- **Framework:** Streamlit
- **APIs:** 
  - OpenWeatherMap (Weather data)
  - Government of India Open Data API (Price data)
  - API-Ninjas (Optional)
- **Language:** Python 3.8+

## 📁 Project Structure

```
agri-sense-ai/
│
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── .gitignore         # Git ignore file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Indian Government Open Data Platform for price data
- OpenWeatherMap for weather API
- Streamlit community for the amazing framework

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for Farmers**