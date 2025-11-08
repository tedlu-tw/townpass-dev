// Frontend Integration Examples
// Example code for connecting Vue.js frontend to TownPass Backend API

// =============================================================================
// 1. API Service Configuration
// =============================================================================

// Create a file: src/services/api.js
const API_BASE_URL = 'http://127.0.0.1:5000/api';

export const api = {
  // Ride endpoints
  ride: {
    start: (data) => fetch(`${API_BASE_URL}/ride/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(res => res.json()),

    update: (data) => fetch(`${API_BASE_URL}/ride/update`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(res => res.json()),

    finish: (data) => fetch(`${API_BASE_URL}/ride/finish`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(res => res.json()),

    getActive: () => fetch(`${API_BASE_URL}/ride/active`)
      .then(res => res.json())
  },

  // History endpoints
  history: {
    getAll: (userId, limit = 10) => 
      fetch(`${API_BASE_URL}/history?user_id=${userId}&limit=${limit}`)
        .then(res => res.json()),

    getOne: (rideId) => fetch(`${API_BASE_URL}/history/${rideId}`)
      .then(res => res.json()),

    delete: (rideId) => fetch(`${API_BASE_URL}/history/${rideId}`, {
      method: 'DELETE'
    }).then(res => res.json())
  },

  // Station endpoints
  station: {
    getNearby: (lat, lng, radius = 1000, limit = 10) =>
      fetch(`${API_BASE_URL}/station/nearby?lat=${lat}&lng=${lng}&radius=${radius}&limit=${limit}`)
        .then(res => res.json()),

    getOne: (stationId) => fetch(`${API_BASE_URL}/station/${stationId}`)
      .then(res => res.json()),

    getAvailable: (minBikes = 1) =>
      fetch(`${API_BASE_URL}/station/available?min_bikes=${minBikes}`)
        .then(res => res.json())
  },

  // Weather endpoints
  weather: {
    getCurrent: (location = '臺北市') =>
      fetch(`${API_BASE_URL}/weather?location=${location}&include_aqi=true`)
        .then(res => res.json()),

    getAQI: (location) =>
      fetch(`${API_BASE_URL}/aqi${location ? '?location=' + location : ''}`)
        .then(res => res.json())
  },

  // Stats endpoints
  stats: {
    getUser: (userId) => fetch(`${API_BASE_URL}/stats?user_id=${userId}`)
      .then(res => res.json()),

    getLeaderboard: (metric = 'distance', limit = 10) =>
      fetch(`${API_BASE_URL}/stats/leaderboard?metric=${metric}&limit=${limit}`)
        .then(res => res.json()),

    getAchievements: (userId) =>
      fetch(`${API_BASE_URL}/stats/achievements?user_id=${userId}`)
        .then(res => res.json())
  }
};


// =============================================================================
// 2. Vue Composable Example (useRide.js)
// =============================================================================

// Create a file: src/composables/useRide.js
import { ref, computed } from 'vue';
import { api } from '@/services/api';

export function useRide() {
  const currentRide = ref(null);
  const isRiding = computed(() => currentRide.value !== null);
  const rideMetrics = ref({
    distance: 0,
    speed: 0,
    calories: 0,
    pausedTime: 0
  });

  async function startRide(userId, location) {
    try {
      const response = await api.ride.start({
        user_id: userId,
        start_location: location
      });
      
      currentRide.value = response;
      return response;
    } catch (error) {
      console.error('Failed to start ride:', error);
      throw error;
    }
  }

  async function updateRide(metrics) {
    if (!currentRide.value) return;

    try {
      const response = await api.ride.update({
        ride_id: currentRide.value.ride_id,
        ...metrics
      });
      
      rideMetrics.value = { ...rideMetrics.value, ...metrics };
      return response;
    } catch (error) {
      console.error('Failed to update ride:', error);
      throw error;
    }
  }

  async function finishRide(endLocation) {
    if (!currentRide.value) return;

    try {
      const response = await api.ride.finish({
        ride_id: currentRide.value.ride_id,
        end_location: endLocation
      });
      
      const summary = response.summary;
      currentRide.value = null;
      rideMetrics.value = {
        distance: 0,
        speed: 0,
        calories: 0,
        pausedTime: 0
      };
      
      return summary;
    } catch (error) {
      console.error('Failed to finish ride:', error);
      throw error;
    }
  }

  return {
    currentRide,
    isRiding,
    rideMetrics,
    startRide,
    updateRide,
    finishRide
  };
}


// =============================================================================
// 3. Vue Component Example (RideView.vue)
// =============================================================================

/*
<template>
  <div class="ride-view">
    <div v-if="!isRiding">
      <button @click="handleStartRide" class="btn-start">
        開始騎乘
      </button>
    </div>

    <div v-else class="ride-active">
      <div class="metrics">
        <div class="metric">
          <span class="label">距離</span>
          <span class="value">{{ (rideMetrics.distance / 1000).toFixed(2) }} km</span>
        </div>
        <div class="metric">
          <span class="label">速度</span>
          <span class="value">{{ rideMetrics.speed.toFixed(1) }} km/h</span>
        </div>
        <div class="metric">
          <span class="label">卡路里</span>
          <span class="value">{{ rideMetrics.calories.toFixed(0) }} kcal</span>
        </div>
      </div>

      <button @click="handleFinishRide" class="btn-finish">
        結束騎乘
      </button>
    </div>

    <div v-if="rideSummary" class="summary-modal">
      <h2>騎乘完成！</h2>
      <div class="summary">
        <p>距離: {{ rideSummary.distance_km }} km</p>
        <p>時間: {{ rideSummary.duration_minutes }} 分鐘</p>
        <p>平均速度: {{ rideSummary.avg_speed_kmh }} km/h</p>
        <p>減碳: {{ rideSummary.carbon_saved_kg }} kg</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRide } from '@/composables/useRide';
import { useGeoLocation } from '@/composables/useGeoLocation';

const { currentRide, isRiding, rideMetrics, startRide, updateRide, finishRide } = useRide();
const { getCurrentPosition } = useGeoLocation();
const rideSummary = ref(null);
const userId = 'user001'; // Replace with actual user ID

async function handleStartRide() {
  try {
    const position = await getCurrentPosition();
    const location = {
      lat: position.coords.latitude,
      lng: position.coords.longitude
    };
    
    await startRide(userId, location);
    startTrackingMetrics();
  } catch (error) {
    alert('無法開始騎乘: ' + error.message);
  }
}

async function handleFinishRide() {
  try {
    const position = await getCurrentPosition();
    const endLocation = {
      lat: position.coords.latitude,
      lng: position.coords.longitude
    };
    
    rideSummary.value = await finishRide(endLocation);
  } catch (error) {
    alert('無法結束騎乘: ' + error.message);
  }
}

let trackingInterval;
function startTrackingMetrics() {
  trackingInterval = setInterval(async () => {
    // Simulate metric updates
    const metrics = {
      distance: rideMetrics.value.distance + Math.random() * 100,
      speed: 12 + Math.random() * 8,
      calories: rideMetrics.value.calories + Math.random() * 5,
      paused_time: 0
    };
    
    await updateRide(metrics);
  }, 5000); // Update every 5 seconds
}
</script>
*/


// =============================================================================
// 4. Station Search Example
// =============================================================================

// In your component:
async function searchNearbyStations() {
  try {
    // Get current position
    const position = await navigator.geolocation.getCurrentPosition(
      (pos) => pos,
      (err) => { throw err; }
    );
    
    const lat = position.coords.latitude;
    const lng = position.coords.longitude;
    
    // Fetch nearby stations
    const result = await api.station.getNearby(lat, lng, 1000, 10);
    
    console.log(`Found ${result.count} nearby stations:`);
    result.stations.forEach(station => {
      console.log(`${station.sna}: ${station.available_rent_bikes} bikes, ${station.distance}m away`);
    });
    
    return result.stations;
  } catch (error) {
    console.error('Failed to get nearby stations:', error);
  }
}


// =============================================================================
// 5. Weather Display Example
// =============================================================================

async function displayWeather() {
  try {
    const weatherData = await api.weather.getCurrent('臺北市');
    
    console.log('Weather:', weatherData.weather);
    console.log('AQI:', weatherData.aqi);
    
    // Display in your UI
    return {
      temperature: weatherData.weather?.temperature || 'N/A',
      condition: weatherData.weather?.condition || 'N/A',
      aqi: weatherData.aqi?.aqi || 'N/A',
      aqiStatus: weatherData.aqi?.status || 'N/A'
    };
  } catch (error) {
    console.error('Failed to get weather:', error);
  }
}


// =============================================================================
// 6. Statistics Display Example
// =============================================================================

async function loadUserStats(userId) {
  try {
    const stats = await api.stats.getUser(userId);
    
    return {
      totalRides: stats.total_rides,
      totalDistance: stats.total_distance_km,
      totalCarbonSaved: stats.total_carbon_saved_kg,
      avgSpeed: stats.avg_speed_kmh,
      avgDistance: stats.avg_distance_km
    };
  } catch (error) {
    console.error('Failed to load stats:', error);
  }
}


// =============================================================================
// 7. History List Example
// =============================================================================

async function loadRideHistory(userId, limit = 10) {
  try {
    const result = await api.history.getAll(userId, limit);
    
    console.log(`Loaded ${result.count} rides`);
    
    return result.rides.map(ride => ({
      id: ride.ride_id,
      date: new Date(ride.start_time).toLocaleDateString(),
      distance: (ride.distance / 1000).toFixed(2) + ' km',
      duration: (ride.duration / 60).toFixed(0) + ' min',
      avgSpeed: ride.avg_speed.toFixed(1) + ' km/h',
      carbonSaved: ride.carbon_reduction.toFixed(2) + ' kg'
    }));
  } catch (error) {
    console.error('Failed to load history:', error);
  }
}


// =============================================================================
// 8. Error Handling Example
// =============================================================================

async function apiCallWithErrorHandling(apiFunction, errorMessage) {
  try {
    const result = await apiFunction();
    return { success: true, data: result };
  } catch (error) {
    console.error(errorMessage, error);
    
    // Handle different error types
    if (error.response) {
      // Server responded with error status
      return { 
        success: false, 
        error: error.response.data.error || 'Server error' 
      };
    } else if (error.request) {
      // Request made but no response
      return { 
        success: false, 
        error: 'No response from server. Please check your connection.' 
      };
    } else {
      // Something else went wrong
      return { 
        success: false, 
        error: error.message || 'Unknown error' 
      };
    }
  }
}

// Usage:
const result = await apiCallWithErrorHandling(
  () => api.ride.start({ user_id: 'user001' }),
  'Failed to start ride'
);

if (result.success) {
  console.log('Ride started:', result.data);
} else {
  alert('Error: ' + result.error);
}


// =============================================================================
// 9. Complete Example: RideTracker Component
// =============================================================================

export default {
  name: 'RideTracker',
  
  data() {
    return {
      userId: 'user001',
      currentRide: null,
      metrics: {
        distance: 0,
        speed: 0,
        calories: 0
      },
      nearbyStations: [],
      weather: null
    };
  },
  
  async mounted() {
    await this.loadInitialData();
  },
  
  methods: {
    async loadInitialData() {
      // Load weather
      this.weather = await api.weather.getCurrent('臺北市');
      
      // Load nearby stations
      const position = await this.getCurrentPosition();
      const stationsData = await api.station.getNearby(
        position.coords.latitude,
        position.coords.longitude,
        1000,
        5
      );
      this.nearbyStations = stationsData.stations;
    },
    
    async startRide() {
      const position = await this.getCurrentPosition();
      const response = await api.ride.start({
        user_id: this.userId,
        start_location: {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        }
      });
      
      this.currentRide = response;
      this.startMetricsTracking();
    },
    
    startMetricsTracking() {
      this.metricsInterval = setInterval(async () => {
        // Update metrics based on GPS or simulation
        this.metrics.distance += 50; // meters
        this.metrics.speed = 15 + Math.random() * 5;
        this.metrics.calories += 0.5;
        
        await api.ride.update({
          ride_id: this.currentRide.ride_id,
          ...this.metrics
        });
      }, 5000);
    },
    
    async finishRide() {
      clearInterval(this.metricsInterval);
      
      const position = await this.getCurrentPosition();
      const summary = await api.ride.finish({
        ride_id: this.currentRide.ride_id,
        end_location: {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        }
      });
      
      this.currentRide = null;
      this.showSummary(summary);
    },
    
    getCurrentPosition() {
      return new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject);
      });
    },
    
    showSummary(summary) {
      alert(`騎乘完成！\n距離: ${summary.distance_km} km\n時間: ${summary.duration_minutes} 分鐘\n減碳: ${summary.carbon_saved_kg} kg`);
    }
  }
};


// =============================================================================
// 10. Usage Notes
// =============================================================================

/*
INTEGRATION CHECKLIST:

1. ✅ Create API service file (src/services/api.js)
2. ✅ Update API_BASE_URL to match your backend
3. ✅ Add error handling for all API calls
4. ✅ Use async/await for cleaner code
5. ✅ Handle loading states in UI
6. ✅ Display error messages to users
7. ✅ Test each endpoint individually
8. ✅ Add proper TypeScript types if using TS

COMMON ISSUES:

- CORS errors: Make sure backend CORS is configured
- Network errors: Check if backend is running
- 404 errors: Verify endpoint URLs
- Data format: Ensure request body matches API expectations

BEST PRACTICES:

- Always handle errors gracefully
- Show loading indicators during API calls
- Cache frequently accessed data
- Debounce rapid API calls (e.g., search)
- Use environment variables for API URLs
*/
