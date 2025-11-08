# Backend Project Structure

```
backend/
├── app.py                          # Main Flask application
├── database.py                     # MongoDB connection & operations
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker configuration
├── README.md                       # Main documentation
├── QUICKSTART.md                   # Quick start guide
│
├── routes/                         # API route handlers
│   ├── ride_routes.py              # Ride session & history
│   ├── station_routes.py           # YouBike stations
│   ├── weather_routes.py           # Weather & AQI
│   └── stats_routes.py             # User statistics
│
├── docs/                           # Documentation
│   ├── API_DOCUMENTATION.md        # API reference
│   ├── RIDE_SCHEMA.md              # Schema documentation
│   ├── MONGODB_FINAL_SUMMARY.md    # MongoDB guide
│   └── MONGODB_CLOUDRUN_SETUP.md   # Deployment guide
│
├── tests/                          # Test files
│   ├── test_all_apis.py            # API tests
│   ├── test_mongodb.py             # MongoDB tests
│   ├── test_ride_schema.py         # Schema tests
│   └── test_ride_session.py        # Session tests
│
├── scripts/                        # Utility scripts
│   ├── fetch_aqi_data.py           # Fetch AQI data
│   ├── fetch_weather_data.py       # Fetch weather data
│   ├── fetch_youbike_data.py       # Fetch YouBike data
│   ├── fix_ssl_certificates.sh     # SSL fix
│   └── start_server.sh             # Server startup
│
└── examples/                       # Integration examples
    └── FRONTEND_INTEGRATION_EXAMPLES.js
```

## Quick Commands

### Run the server
```bash
python app.py
```

### Run tests
```bash
python tests/test_all_apis.py
python tests/test_mongodb.py
python tests/test_ride_schema.py
```

### Fetch data
```bash
python scripts/fetch_weather_data.py
python scripts/fetch_aqi_data.py
python scripts/fetch_youbike_data.py
```

### Start with script
```bash
./scripts/start_server.sh
```
