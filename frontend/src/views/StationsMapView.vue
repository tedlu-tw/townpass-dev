<template>
  <div class="stations-map-view">
    <div class="header">
      <h1>🚲 YouBike 站點地圖</h1>
      <p class="subtitle">查找附近的 YouBike 站點</p>
    </div>

    <div class="filters">
      <button 
        @click="filterAvailable = !filterAvailable" 
        :class="{ active: filterAvailable }"
        class="filter-btn"
      >
        {{ filterAvailable ? '✓' : '' }} 僅顯示有車站點
      </button>
      <button @click="refreshStations" class="filter-btn">
        🔄 重新整理
      </button>
    </div>

    <div class="map-container">
      <MapView
        ref="mapRef"
        :center="mapCenter"
        :zoom="15"
        :markers="displayedStations"
        :apiKey="googleMapsApiKey"
        :showGpsButton="true"
        @marker-click="handleStationClick"
        @location-found="handleLocationFound"
      />
    </div>

    <!-- Station Detail Card -->
    <div v-if="selectedStation" class="station-detail">
      <div class="station-header">
        <h2>{{ selectedStation.name }}</h2>
        <button class="close-btn" @click="selectedStation = null">✕</button>
      </div>
      
      <div class="station-info">
        <div class="info-row">
          <span class="label">📍 位置</span>
          <span class="value">{{ selectedStation.address }}</span>
        </div>
        
        <div class="info-row" v-if="selectedStation.distance">
          <span class="label">📏 距離</span>
          <span class="value">{{ selectedStation.distance }} 公里</span>
        </div>
        
        <div class="availability">
          <div class="availability-item">
            <div class="number bikes">{{ selectedStation.availableBikes || 0 }}</div>
            <div class="text">可借車輛</div>
          </div>
          <div class="availability-item">
            <div class="number docks">{{ selectedStation.availableDocks || 0 }}</div>
            <div class="text">可還空位</div>
          </div>
        </div>
      </div>
      
      <div class="station-actions">
        <button class="action-btn primary" @click="navigateToStation">
          🧭 導航前往
        </button>
        <button class="action-btn" @click="startRide">
          🚴 開始騎乘
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MapView from '../components/MapView.vue'

const router = useRouter()
const mapRef = ref(null)
const googleMapsApiKey = ref(import.meta.env.VITE_GOOGLE_MAPS_API_KEY || 'YOUR_API_KEY')

// Map state
const mapCenter = ref({ lat: 25.0330, lng: 121.5654 })
const selectedStation = ref(null)
const userLocation = ref(null)
const filterAvailable = ref(false)

// Mock YouBike stations data - replace with actual API call
const stations = ref([
  {
    id: 1,
    name: 'YouBike 市政府站',
    address: '台北市信義區市府路1號',
    lat: 25.0374865,
    lng: 121.5647688,
    availableBikes: 5,
    availableDocks: 15,
    totalDocks: 20
  },
  {
    id: 2,
    name: 'YouBike 誠品信義站',
    address: '台北市信義區松高路11號',
    lat: 25.0397146,
    lng: 121.5653771,
    availableBikes: 0,
    availableDocks: 10,
    totalDocks: 10
  },
  {
    id: 3,
    name: 'YouBike 信義商圈站',
    address: '台北市信義區忠孝東路五段8號',
    lat: 25.0405919,
    lng: 121.5647644,
    availableBikes: 12,
    availableDocks: 8,
    totalDocks: 20
  }
])

const displayedStations = computed(() => {
  let filtered = stations.value

  // Filter by availability
  if (filterAvailable.value) {
    filtered = filtered.filter(s => s.availableBikes > 0)
  }

  // Convert to marker format
  return filtered.map(station => ({
    ...station,
    title: station.name,
    // You can add custom marker icons here
    icon: station.availableBikes > 0 
      ? null // Use default marker for available
      : {
          path: 'M 0,0 L -10,-20 L 10,-20 Z',
          fillColor: '#cccccc',
          fillOpacity: 1,
          strokeWeight: 0,
          scale: 1
        }
  }))
})

const handleStationClick = (station) => {
  selectedStation.value = station
}

const handleLocationFound = (location) => {
  userLocation.value = location
  mapCenter.value = location
}

const refreshStations = async () => {
  // TODO: Implement actual API call to fetch YouBike data
  console.log('Refreshing stations...')
  
  // Example: Load from backend
  // try {
  //   const response = await fetch('/api/youbike/stations')
  //   const data = await response.json()
  //   stations.value = data
  // } catch (error) {
  //   console.error('Error loading stations:', error)
  // }
}

const navigateToStation = () => {
  if (!selectedStation.value) return
  
  const { lat, lng } = selectedStation.value
  const url = `https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}`
  window.open(url, '_blank')
}

const startRide = () => {
  if (!selectedStation.value) return
  
  // Store selected station and navigate to ride view
  localStorage.setItem('startStation', JSON.stringify(selectedStation.value))
  router.push('/ride')
}

onMounted(() => {
  refreshStations()
})
</script>

<style scoped>
.stations-map-view {
  padding: 0;
  height: calc(100vh - 88px);
  display: flex;
  flex-direction: column;
}

.header {
  text-align: center;
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.header h1 {
  margin: 0 0 0.5rem 0;
  font-size: 1.8rem;
}

.subtitle {
  margin: 0;
  font-size: 1rem;
  opacity: 0.9;
}

.filters {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.filter-btn {
  padding: 0.5rem 1rem;
  border: 2px solid #667eea;
  border-radius: 20px;
  background: white;
  color: #667eea;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  background: #f0f0f0;
}

.filter-btn.active {
  background: #667eea;
  color: white;
}

.map-container {
  flex: 1;
  position: relative;
}

.station-detail {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-radius: 20px 20px 0 0;
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  max-height: 50vh;
  overflow-y: auto;
  z-index: 100;
}

.station-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.station-header h2 {
  margin: 0;
  font-size: 1.3rem;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #333;
}

.station-info {
  margin-bottom: 1.5rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-row .label {
  color: #666;
  font-weight: 500;
}

.info-row .value {
  color: #333;
}

.availability {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-top: 1rem;
}

.availability-item {
  text-align: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 12px;
}

.availability-item .number {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.3rem;
}

.availability-item .number.bikes {
  color: #4caf50;
}

.availability-item .number.docks {
  color: #2196f3;
}

.availability-item .text {
  font-size: 0.9rem;
  color: #666;
}

.station-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.action-btn {
  padding: 0.8rem;
  border: 2px solid #667eea;
  border-radius: 8px;
  background: white;
  color: #667eea;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
}

@media (max-width: 768px) {
  .stations-map-view {
    height: calc(100vh - 70px);
  }
  
  .header h1 {
    font-size: 1.5rem;
  }
  
  .station-detail {
    max-height: 60vh;
  }
  
  .station-actions {
    grid-template-columns: 1fr;
  }
}
</style>
