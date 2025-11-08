<template>
  <div class="map-demo-view">
    <div class="demo-header">
      <h1>📍 地圖示範</h1>
      <p class="subtitle">使用 Google Maps 顯示多個地點標記</p>
    </div>

    <div class="map-controls">
      <button @click="showAllMarkers" class="control-btn">顯示所有標記</button>
      <button @click="centerOnTaipei" class="control-btn">回到台北市政府</button>
      <button @click="addCustomMarker" class="control-btn">新增自訂標記</button>
      <button @click="clearAllMarkers" class="control-btn danger">清除標記</button>
    </div>

    <div class="map-wrapper">
      <MapView
        ref="mapRef"
        :center="mapCenter"
        :zoom="mapZoom"
        :markers="customMarkers"
        :geojsonUrl="geojsonUrl"
        :apiKey="googleMapsApiKey"
        :mapTypeId="mapType"
        :showGpsButton="true"
        @marker-click="handleMarkerClick"
        @map-ready="handleMapReady"
        @location-found="handleLocationFound"
      />
    </div>

    <div v-if="selectedLocation" class="location-info">
      <h3>選取的地點</h3>
      <div class="info-grid">
        <div class="info-item">
          <strong>名稱:</strong> {{ selectedLocation.name }}
        </div>
        <div class="info-item">
          <strong>地址:</strong> {{ selectedLocation.site || selectedLocation.address }}
        </div>
        <div v-if="selectedLocation.distance" class="info-item">
          <strong>距離:</strong> {{ selectedLocation.distance }} 公里
        </div>
      </div>
    </div>

    <div class="demo-section">
      <h2>使用方式</h2>
      <div class="code-example">
        <h3>1. 基本使用</h3>
        <pre><code>&lt;MapView
  :center="{ lat: 25.0374865, lng: 121.5647688 }"
  :zoom="16"
  apiKey="YOUR_API_KEY"
/&gt;</code></pre>
      </div>

      <div class="code-example">
        <h3>2. 載入 GeoJSON 資料</h3>
        <pre><code>&lt;MapView
  geojsonUrl="/map.geojson"
  apiKey="YOUR_API_KEY"
  @marker-click="handleMarkerClick"
/&gt;</code></pre>
      </div>

      <div class="code-example">
        <h3>3. 自訂標記</h3>
        <pre><code>const markers = [
  {
    lat: 25.0374865,
    lng: 121.5647688,
    name: '台北市政府',
    address: '110台北市信義區市府路1號'
  }
]

&lt;MapView
  :markers="markers"
  apiKey="YOUR_API_KEY"
/&gt;</code></pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import MapView from '../components/MapView.vue'

// Map configuration
const mapRef = ref(null)
const mapCenter = ref({ lat: 25.0374865, lng: 121.5647688 })
const mapZoom = ref(16)
const mapType = ref('terrain') // roadmap, satellite, hybrid, terrain
const geojsonUrl = ref('/map.geojson')

// Replace with your actual API key
// load API key from .env
// Vite: VITE_GOOGLE_MAPS_API_KEY=your_key
const googleMapsApiKey = ref(import.meta.env.VITE_GOOGLE_MAPS_API_KEY || 'YOUR_API_KEY')

// Custom markers
const customMarkers = ref([])

// Selected location
const selectedLocation = ref(null)
const userLocation = ref(null)

const handleMarkerClick = (marker) => {
  selectedLocation.value = marker
  console.log('Marker clicked:', marker)
}

const handleMapReady = (map) => {
  console.log('Map is ready:', map)
}

const handleLocationFound = (location) => {
  userLocation.value = location
  console.log('User location found:', location)
}

const showAllMarkers = () => {
  // Reset to show all markers
  customMarkers.value = []
  mapRef.value?.getCurrentLocation()
}

const centerOnTaipei = () => {
  mapCenter.value = { lat: 25.0374865, lng: 121.5647688 }
  mapZoom.value = 16
}

const addCustomMarker = () => {
  const newMarker = {
    lat: 25.033 + Math.random() * 0.01,
    lng: 121.565 + Math.random() * 0.01,
    name: `自訂地點 ${customMarkers.value.length + 1}`,
    address: '台北市信義區',
    id: Date.now()
  }
  customMarkers.value.push(newMarker)
}

const clearAllMarkers = () => {
  customMarkers.value = []
  selectedLocation.value = null
}
</script>

<style scoped>
.map-demo-view {
  padding: 2rem 0;
}

.demo-header {
  text-align: center;
  margin-bottom: 2rem;
}

.demo-header h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.1rem;
  color: #666;
}

.map-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  justify-content: center;
}

.control-btn {
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 6px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.control-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.control-btn:active {
  transform: translateY(0);
}

.control-btn.danger {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.map-wrapper {
  width: 100%;
  height: 500px;
  margin-bottom: 2rem;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.location-info {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.location-info h3 {
  margin: 0 0 1rem 0;
  font-size: 1.3rem;
  color: #333;
}

.info-grid {
  display: grid;
  gap: 0.8rem;
}

.info-item {
  font-size: 1rem;
  color: #666;
}

.info-item strong {
  color: #333;
  margin-right: 0.5rem;
}

.demo-section {
  margin-top: 3rem;
}

.demo-section h2 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 1.5rem;
}

.code-example {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.code-example h3 {
  margin: 0 0 1rem 0;
  font-size: 1.2rem;
  color: #667eea;
}

.code-example pre {
  margin: 0;
  overflow-x: auto;
}

.code-example code {
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  line-height: 1.6;
  color: #333;
}

@media (max-width: 768px) {
  .demo-header h1 {
    font-size: 2rem;
  }
  
  .map-wrapper {
    height: 400px;
  }
  
  .map-controls {
    flex-direction: column;
  }
  
  .control-btn {
    width: 100%;
  }
  
  .code-example {
    padding: 1rem;
  }
  
  .code-example code {
    font-size: 0.8rem;
  }
}
</style>
