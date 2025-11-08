<template>
  <div class="map-container">
    <div ref="mapDiv" class="map"></div>
    <div v-if="loading" class="map-loading">載入地圖中...</div>
    
    <!-- GPS Location Button -->
    <div v-if="!loading && showGpsButton" class="gps-button" @click="getCurrentLocation">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <circle cx="12" cy="12" r="3"></circle>
      </svg>
    </div>

    <!-- Selected Marker Info Card -->
    <div v-if="selectedMarker" class="marker-info-card">
      <div class="info-content">
        <h3>{{ selectedMarker.name || selectedMarker.title }}</h3>
        <p v-if="selectedMarker.site || selectedMarker.address">
          📍 {{ selectedMarker.site || selectedMarker.address }}
        </p>
        <p v-if="selectedMarker.distance" class="distance">
          {{ selectedMarker.distance }} 公里
        </p>
      </div>
      <button class="close-btn" @click="selectedMarker = null">✕</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  center: {
    type: Object,
    default: () => ({ lat: 25.0374865, lng: 121.5647688 }) // Taipei default
  },
  zoom: {
    type: Number,
    default: 16
  },
  markers: {
    type: Array,
    default: () => []
  },
  apiKey: {
    type: String,
    required: false,
    default: ''
  },
  geojsonUrl: {
    type: String,
    default: ''
  },
  mapTypeId: {
    type: String,
    default: 'terrain' // roadmap, satellite, hybrid, terrain
  },
  showGpsButton: {
    type: Boolean,
    default: true
  },
  markerIcon: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['marker-click', 'map-ready', 'location-found'])

const mapDiv = ref(null)
const map = ref(null)
const loading = ref(true)
const googleMarkers = ref([])
const selectedMarker = ref(null)
const userLocationMarker = ref(null)
const currentLocation = ref(null)

const loadGoogleMapsScript = () => {
  return new Promise((resolve, reject) => {
    // Check if already loaded
    if (window.google && window.google.maps) {
      resolve()
      return
    }

    const script = document.createElement('script')
    const apiKey = props.apiKey || 'YOUR_API_KEY'
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&callback=initMap`
    script.async = true
    script.defer = true
    
    window.initMap = () => {
      resolve()
    }
    
    script.onerror = () => reject(new Error('Failed to load Google Maps'))
    document.head.appendChild(script)
  })
}

const initMap = async () => {
  try {
    // Check if API key is set
    if (!props.apiKey || props.apiKey === 'YOUR_API_KEY') {
      console.warn('⚠️ Google Maps API Key not set. Please add VITE_GOOGLE_MAPS_API_KEY to your .env file')
      console.info('📖 See MAPVIEW_SETUP.md for instructions')
    }
    
    await loadGoogleMapsScript()
    
    map.value = new google.maps.Map(mapDiv.value, {
      center: props.center,
      zoom: props.zoom,
      mapTypeId: props.mapTypeId,
      streetViewControl: false,
      mapTypeControl: false,
      fullscreenControl: false,
      zoomControl: false,
    })

    loading.value = false
    emit('map-ready', map.value)
    
    // Load markers from geojson if URL provided
    if (props.geojsonUrl) {
      await loadGeoJsonMarkers()
    } else if (props.markers.length > 0) {
      updateMarkers()
    }

    // Get user location
    if (props.showGpsButton) {
      getCurrentLocation()
    }
  } catch (error) {
    console.error('Error initializing map:', error)
    console.error('Make sure your Google Maps API key is valid and Maps JavaScript API is enabled')
    loading.value = false
  }
}

const loadGeoJsonMarkers = async () => {
  try {
    const response = await fetch(props.geojsonUrl)
    const data = await response.json()
    
    const markers = data.features.map(feature => ({
      lat: feature.geometry.coordinates[1], // GeoJSON uses [lng, lat]
      lng: feature.geometry.coordinates[0],
      name: feature.properties.name,
      site: feature.properties.site,
      address: feature.properties.site,
      id: feature.properties.id,
      ...feature.properties
    }))
    
    createMarkers(markers)
  } catch (error) {
    console.error('Error loading GeoJSON:', error)
  }
}

const createMarkers = (markersList) => {
  // Clear existing markers
  googleMarkers.value.forEach(marker => marker.setMap(null))
  googleMarkers.value = []

  // Add new markers
  markersList.forEach(markerData => {
    const marker = new google.maps.Marker({
      position: { lat: markerData.lat, lng: markerData.lng },
      map: map.value,
      title: markerData.name || markerData.title,
      icon: props.markerIcon || undefined,
    })

    // Add click listener
    marker.addListener('click', () => {
      // Calculate distance if user location is available
      if (currentLocation.value) {
        const distance = calculateDistance(
          currentLocation.value.lat,
          currentLocation.value.lng,
          markerData.lat,
          markerData.lng
        )
        markerData.distance = distance.toFixed(2)
      }
      
      selectedMarker.value = markerData
      emit('marker-click', markerData)
    })

    googleMarkers.value.push(marker)
  })
}

const updateMarkers = () => {
  createMarkers(props.markers)
}

const getCurrentLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        }
        
        currentLocation.value = pos
        
        // Remove existing user marker
        if (userLocationMarker.value) {
          userLocationMarker.value.setMap(null)
        }
        
        // Add user location marker
        userLocationMarker.value = new google.maps.Marker({
          position: pos,
          map: map.value,
          title: '您的位置',
          icon: {
            path: google.maps.SymbolPath.CIRCLE,
            fillColor: '#4285F4',
            fillOpacity: 1,
            scale: 8,
            strokeColor: 'white',
            strokeWeight: 2
          }
        })
        
        // Center map on user location
        map.value.setCenter(pos)
        
        emit('location-found', pos)
      },
      (error) => {
        console.error('Error getting location:', error)
      }
    )
  }
}

const calculateDistance = (lat1, lng1, lat2, lng2) => {
  const R = 6371 // Earth's radius in km
  const dLat = (lat2 - lat1) * Math.PI / 180
  const dLng = (lng2 - lng1) * Math.PI / 180
  const a = 
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLng / 2) * Math.sin(dLng / 2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c
}

const setCenter = (lat, lng) => {
  if (map.value) {
    map.value.setCenter({ lat, lng })
  }
}

const setZoom = (zoom) => {
  if (map.value) {
    map.value.setZoom(zoom)
  }
}

const addMarker = (markerData) => {
  if (!map.value) return
  
  const marker = new google.maps.Marker({
    position: { lat: markerData.lat, lng: markerData.lng },
    map: map.value,
    title: markerData.name || markerData.title,
    icon: markerData.icon || props.markerIcon || undefined,
  })

  marker.addListener('click', () => {
    selectedMarker.value = markerData
    emit('marker-click', markerData)
  })

  googleMarkers.value.push(marker)
  return marker
}

const clearMarkers = () => {
  googleMarkers.value.forEach(marker => marker.setMap(null))
  googleMarkers.value = []
}

// Watch for marker changes
watch(() => props.markers, () => {
  if (map.value) {
    updateMarkers()
  }
}, { deep: true })

// Watch for center changes
watch(() => props.center, (newCenter) => {
  if (map.value) {
    map.value.setCenter(newCenter)
  }
}, { deep: true })

onMounted(() => {
  initMap()
})

// Expose methods
defineExpose({
  setCenter,
  setZoom,
  addMarker,
  clearMarkers,
  getCurrentLocation,
  map
})
</script>

<style scoped>
.map-container {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 400px;
}

.map {
  width: 100%;
  height: 100%;
  border-radius: 8px;
}

.map-loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 1rem 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  font-weight: 500;
  z-index: 10;
}

.gps-button {
  position: absolute;
  right: 10px;
  top: 10px;
  background-color: white;
  width: 40px;
  height: 40px;
  border-radius: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: rgba(0, 0, 0, 0.3) 0px 1px 4px -1px;
  transition: background-color 0.2s;
  z-index: 5;
}

.gps-button:hover {
  background-color: #f5f5f5;
}

.gps-button:active {
  background-color: #e0e0e0;
}

.marker-info-card {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: rgba(0, 0, 0, 0.1) 0px -4px 10px;
  max-width: 90%;
  width: 400px;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.info-content {
  flex: 1;
}

.info-content h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.info-content p {
  margin: 0.3rem 0;
  font-size: 0.9rem;
  color: #666;
}

.info-content .distance {
  color: #667eea;
  font-weight: 500;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.5rem;
  color: #999;
  padding: 0;
  line-height: 1;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #333;
}

@media (max-width: 768px) {
  .marker-info-card {
    width: 85%;
    padding: 1rem;
  }
  
  .info-content h3 {
    font-size: 1rem;
  }
  
  .info-content p {
    font-size: 0.85rem;
  }
}
</style>
