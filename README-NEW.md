# TownPass - Smart Bike Riding Platform 🚴

A Vue.js-based smart city bike riding platform with real-time tracking, statistics, and Google Maps integration.

## 🎯 Features

- **🚴 Ride Tracking**: Real-time GPS tracking of your bike rides
- **📊 Statistics**: Comprehensive ride statistics and personal records
- **🗺️ Map Integration**: Google Maps powered route visualization
- **🌤️ Weather Info**: Real-time weather information for ride planning
- **📈 Elevation Charts**: Visual elevation profile of your rides
- **📱 Responsive Design**: Works on desktop and mobile devices
- **💾 Local Storage**: Ride history saved locally in your browser

## 📁 Project Structure

```
├── Frontend Paths
│   ├── /home             → Dashboard with stats
│   ├── /ride             → Start/Active ride
│   ├── /ride/pause       → Paused ride view
│   ├── /ride/finish      → Ride completion
│   └── /history          → Ride history
|
├── Components (Shared)
│   ├── Navbar.vue           → Navigation bar
│   ├── Footer.vue           → Footer component
│   ├── Station.vue          → Station info display
│   ├── MapView.vue          → Google Maps rendering
│   ├── WeatherCard.vue      → Weather display
│   ├── RideSummaryCard.vue  → Ride summary
│   ├── SummaryCard.vue      → Personal stats
│   └── ElevationChart.vue   → Elevation chart
|
└── Composables (Hooks)
    ├── useRideSession.js    → Ride session management
    ├── useGeoLocation.js    → GPS tracking
    ├── useWeather.js        → Weather data
    └── useStats.js          → Statistics calculation
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+ (for backend scripts)
- Google Maps API Key ([Get one here](https://developers.google.com/maps/documentation/javascript/get-api-key))

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd townpass-dev
```

2. **Install frontend dependencies**
```bash
cd frontend
npm install
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your Google Maps API key
```

4. **Install backend dependencies**
```bash
cd ../backend
pip install -r requirements.txt
```

### Running the Application

**Frontend Development Server:**
```bash
cd frontend
npm run dev
```

Visit `http://localhost:5173`

**Backend Scripts** (optional - for real data):
```bash
cd backend
python fetch_youbike_data.py
python fetch_weather_data.py
python fetch_aqi_data.py
```

## 🗺️ Google Maps Setup

The application requires a Google Maps JavaScript API key for map functionality.

### Quick Setup:

1. Get your API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Enable **Maps JavaScript API**
3. Add to `.env` file:
```env
VITE_GOOGLE_MAPS_API_KEY=your_api_key_here
```

📖 See [GOOGLE_MAPS_SETUP.md](frontend/GOOGLE_MAPS_SETUP.md) for detailed instructions.

## 📖 Documentation

- [Frontend Structure Guide](frontend/STRUCTURE.md) - Detailed component and composable documentation
- [Google Maps Setup](frontend/GOOGLE_MAPS_SETUP.md) - Complete Maps API integration guide
- [Project Complete](PROJECT_COMPLETE.md) - Original project documentation

## 🏗️ Tech Stack

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Vue Router** - Official routing library
- **Pinia** - State management
- **Vite** - Build tool and dev server
- **Axios** - HTTP client
- **Google Maps JavaScript API** - Map rendering

### Backend (Data Scripts)
- **Python 3.8+**
- Government Open Data APIs
- JSON data storage

## 🎮 Usage

### Starting a Ride

1. Navigate to `/home` or `/ride`
2. Select a starting station from the map or list
3. Click "開始騎乘" (Start Ride)
4. GPS tracking begins automatically

### During a Ride

- View real-time stats: distance, time, speed, calories
- See your route on the map
- Pause anytime with the pause button
- Resume or end the ride

### After a Ride

- View complete ride summary
- See elevation profile
- Save to history
- Share on social media (coming soon)

### Viewing History

- Navigate to `/history`
- Filter by time period (week/month/year)
- View detailed statistics
- Export your data
- Delete individual rides

## 📊 Data Sources

- **YouBike**: Taipei Public Bike Open Data
- **Weather**: Central Weather Bureau Open Data
- **AQI**: Environmental Protection Agency Open Data

## 🔐 Privacy & Data

- All ride data is stored locally in your browser
- No personal data is sent to external servers
- Location data is only used during active rides
- You can delete your history anytime

## 🛠️ Development

### Project Scripts

```bash
# Frontend
npm run dev      # Start dev server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Lint code

# Backend
python fetch_youbike_data.py   # Fetch YouBike data
python fetch_weather_data.py   # Fetch weather data
python fetch_aqi_data.py        # Fetch AQI data
```

### Key Files

- `frontend/src/router/index.js` - Route definitions
- `frontend/src/App.vue` - Main app component
- `frontend/src/composables/` - Reusable logic
- `frontend/src/components/` - UI components
- `frontend/src/views/` - Page components

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Taiwan Government Open Data Platform
- Google Maps Platform
- Vue.js Community

## 📮 Contact

For questions or feedback, please open an issue on GitHub.

---

**Note**: This is a development version. For production deployment, ensure proper API key security, enable HTTPS for geolocation, and consider implementing a backend server for data persistence.
