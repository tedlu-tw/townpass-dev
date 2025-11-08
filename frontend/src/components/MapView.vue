<template>
  <div class="map-container">
    <div ref="mapDiv" class="map"></div>
    <div v-if="loading" class="map-loading">載入地圖中...</div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  center: {
    type: Object,
    default: () => ({ lat: 25.0330, lng: 121.5654 }) // Taipei default
  },
  zoom: {
    type: Number,
    default: 15
  },
  markers: {
    type: Array,
    default: () => []
  },
  apiKey: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['marker-click', 'map-ready'])

const mapDiv = ref(null)
const map = ref(null)
const loading = ref(true)
const googleMarkers = ref([])

const loadGoogleMapsScript = () => {
  return new Promise((resolve, reject) => {
    // Check if already loaded
    if (window.google && window.google.maps) {
      resolve()
      return
    }

    const script = document.createElement('script')
    script.src = `https://maps.googleapis.com/maps/api/js?key=${props.apiKey}&callback=initMap`
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
    await loadGoogleMapsScript()
    
    map.value = new google.maps.Map(mapDiv.value, {
      center: props.center,
      zoom: props.zoom,
      mapTypeControl: true,
      streetViewControl: true,
      fullscreenControl: true,
    })

    loading.value = false
    emit('map-ready', map.value)
    
    // Add markers if provided
    if (props.markers.length > 0) {
      updateMarkers()
    }
  } catch (error) {
    console.error('Error initializing map:', error)
    loading.value = false
  }
}

const updateMarkers = () => {
  // Clear existing markers
  googleMarkers.value.forEach(marker => marker.setMap(null))
  googleMarkers.value = []

  // Add new markers
  props.markers.forEach(markerData => {
    const marker = new google.maps.Marker({
      position: { lat: markerData.lat, lng: markerData.lng },
      map: map.value,
      title: markerData.title,
      icon: markerData.icon || undefined,
    })

    marker.addListener('click', () => {
      emit('marker-click', markerData)
    })

    googleMarkers.value.push(marker)
  })
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
}
</style>
