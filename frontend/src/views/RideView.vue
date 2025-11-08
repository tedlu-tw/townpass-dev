<template>
  <div class="ride-view">
    <div v-if="!isRiding" class="start-screen">
      <h2>🚴 開始騎乘</h2>
      
      <WeatherCard :weather="weather" :loading="weatherLoading" :error="weatherError" />

      <div class="station-selection">
        <h3>選擇起始站點</h3>
        <div class="search-box">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="搜尋站點..."
            class="search-input"
          >
        </div>

        <div class="map-section">
          <MapView 
            :center="mapCenter"
            :markers="stationMarkers"
            :apiKey="googleMapsApiKey"
            @marker-click="selectStation"
            ref="mapRef"
          />
        </div>

        <div class="nearby-stations">
          <h4>附近站點</h4>
          <div v-if="loadingStations" class="loading">載入中...</div>
          <div v-else class="stations-list">
            <Station 
              v-for="station in nearbyStations" 
              :key="station.id"
              :station="station"
              :showAction="true"
              @select-station="selectStation"
            />
          </div>
        </div>
      </div>

      <button 
        @click="handleStartRide" 
        class="start-button"
        :disabled="!selectedStation"
      >
        {{ selectedStation ? `從 ${selectedStation.name} 出發` : '請選擇站點' }}
      </button>
    </div>

    <div v-else class="riding-screen">
      <div class="ride-header">
        <h2>🚴 騎乘中</h2>
        <span class="status" :class="{ paused: isPaused }">
          {{ isPaused ? '⏸️ 已暫停' : '▶️ 進行中' }}
        </span>
      </div>

      <div class="ride-stats-live">
        <div class="stat-live">
          <span class="label">時間</span>
          <span class="value">{{ formattedDuration }}</span>
        </div>
        <div class="stat-live">
          <span class="label">距離</span>
          <span class="value">{{ rideData.distance.toFixed(2) }} km</span>
        </div>
        <div class="stat-live">
          <span class="label">速度</span>
          <span class="value">{{ rideData.avgSpeed.toFixed(1) }} km/h</span>
        </div>
        <div class="stat-live">
          <span class="label">熱量</span>
          <span class="value">{{ rideData.calories }} kcal</span>
        </div>
      </div>

      <div class="map-section-live">
        <MapView 
          :center="currentMapCenter"
          :markers="pathMarkers"
          :apiKey="googleMapsApiKey"
          ref="liveMapRef"
        />
      </div>

      <div class="ride-controls">
        <button @click="handlePause" class="control-button pause" v-if="!isPaused">
          ⏸️ 暫停
        </button>
        <button @click="handleResume" class="control-button resume" v-else>
          ▶️ 繼續
        </button>
        <button @click="showFinishDialog = true" class="control-button finish">
          🏁 結束騎乘
        </button>
      </div>
    </div>

    <!-- Finish Dialog -->
    <div v-if="showFinishDialog" class="modal-overlay" @click="showFinishDialog = false">
      <div class="modal-content" @click.stop>
        <h3>選擇結束站點</h3>
        <div class="stations-list-small">
          <Station 
            v-for="station in nearbyStations" 
            :key="station.id"
            :station="station"
            :showAction="true"
            @select-station="handleFinishRide"
          />
        </div>
        <button @click="showFinishDialog = false" class="cancel-button">取消</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import MapView from '../components/MapView.vue'
import Station from '../components/Station.vue'
import WeatherCard from '../components/WeatherCard.vue'
import { useRideSession } from '../composables/useRideSession'
import { useGeoLocation } from '../composables/useGeoLocation'
import { useWeather } from '../composables/useWeather'

const router = useRouter()

// Replace with your actual Google Maps API Key
const googleMapsApiKey = 'YOUR_GOOGLE_MAPS_API_KEY'

const {
  isRiding,
  isPaused,
  rideData,
  formattedDuration,
  startRide,
  pauseRide,
  resumeRide,
  finishRide,
  updateLocation
} = useRideSession()

const { location, loading: locationLoading } = useGeoLocation()
const { weather, loading: weatherLoading, error: weatherError, fetchWeather } = useWeather()

const searchQuery = ref('')
const selectedStation = ref(null)
const showFinishDialog = ref(false)
const loadingStations = ref(false)
const mapRef = ref(null)
const liveMapRef = ref(null)

// Mock stations - replace with actual API call
const stations = ref([
  { id: 1, name: '台北車站', address: '台北市中正區北平西路3號', lat: 25.0478, lng: 121.5170, availableBikes: 10, availableSpaces: 5, totalSlots: 15 },
  { id: 2, name: '西門站', address: '台北市萬華區中華路一段', lat: 25.0420, lng: 121.5077, availableBikes: 8, availableSpaces: 7, totalSlots: 15 },
  { id: 3, name: '中正紀念堂站', address: '台北市中正區中山南路', lat: 25.0329, lng: 121.5200, availableBikes: 12, availableSpaces: 3, totalSlots: 15 }
])

const mapCenter = computed(() => {
  if (location.value) {
    return { lat: location.value.latitude, lng: location.value.longitude }
  }
  return { lat: 25.0330, lng: 121.5654 } // Taipei default
})

const currentMapCenter = computed(() => {
  if (location.value) {
    return { lat: location.value.latitude, lng: location.value.longitude }
  }
  return mapCenter.value
})

const stationMarkers = computed(() => {
  return stations.value.map(station => ({
    id: station.id,
    lat: station.lat,
    lng: station.lng,
    title: station.name,
    ...station
  }))
})

const pathMarkers = computed(() => {
  const markers = []
  if (rideData.path.length > 0) {
    markers.push({
      lat: rideData.path[0].lat,
      lng: rideData.path[0].lng,
      title: '起點',
      icon: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
    })
  }
  if (location.value) {
    markers.push({
      lat: location.value.latitude,
      lng: location.value.longitude,
      title: '當前位置',
      icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
    })
  }
  return markers
})

const nearbyStations = computed(() => {
  // Filter by search query if provided
  let filtered = stations.value
  if (searchQuery.value) {
    filtered = filtered.filter(s => 
      s.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }
  return filtered.slice(0, 6)
})

const selectStation = (station) => {
  selectedStation.value = station
}

const handleStartRide = () => {
  if (!selectedStation.value) return
  startRide(selectedStation.value)
}

const handlePause = () => {
  pauseRide()
  router.push('/ride/pause')
}

const handleResume = () => {
  resumeRide()
}

const handleFinishRide = (endStation) => {
  const summary = finishRide(endStation)
  showFinishDialog.value = false
  router.push({ name: 'ride-finish', params: { summary } })
}

// Watch location changes
watch(location, (newLocation) => {
  if (newLocation && isRiding.value) {
    updateLocation(newLocation)
    // Update map center
    if (liveMapRef.value) {
      liveMapRef.value.setCenter(newLocation.latitude, newLocation.longitude)
    }
  }
}, { deep: true })

onMounted(async () => {
  await fetchWeather()
  loadingStations.value = false
})
</script>

<style scoped>
.ride-view {
  padding: 2rem 0;
}

.start-screen h2, .riding-screen h2 {
  color: #333;
  margin-bottom: 2rem;
}

.station-selection {
  margin: 2rem 0;
}

.station-selection h3, .station-selection h4 {
  color: #333;
  margin-bottom: 1rem;
}

.search-box {
  margin-bottom: 1.5rem;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
}

.map-section, .map-section-live {
  height: 400px;
  margin-bottom: 2rem;
  border-radius: 8px;
  overflow: hidden;
}

.nearby-stations {
  margin-top: 2rem;
}

.stations-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.start-button {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.2rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.start-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.start-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.ride-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.status {
  padding: 0.5rem 1rem;
  background: #27ae60;
  color: white;
  border-radius: 20px;
  font-weight: 500;
}

.status.paused {
  background: #f39c12;
}

.ride-stats-live {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-live {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stat-live .label {
  display: block;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.stat-live .value {
  display: block;
  color: #667eea;
  font-size: 1.8rem;
  font-weight: bold;
}

.ride-controls {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.control-button {
  flex: 1;
  padding: 1rem;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.pause {
  background: #f39c12;
  color: white;
}

.resume {
  background: #27ae60;
  color: white;
}

.finish {
  background: #e74c3c;
  color: white;
}

.control-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-content h3 {
  margin-bottom: 1.5rem;
}

.stations-list-small {
  display: grid;
  gap: 1rem;
  margin-bottom: 1rem;
}

.cancel-button {
  width: 100%;
  padding: 0.75rem;
  background: #95a5a6;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>
