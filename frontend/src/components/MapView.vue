<template>
  <div class="relative w-full h-full">
    <div ref="mapDiv" class="w-full h-full"></div>

    <div v-if="loading" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white px-8 py-4 rounded-lg shadow-md font-medium z-50">
      載入地圖中...
    </div>

    <!-- GPS Location Button -->
    <button
      v-if="!loading && showGpsButton"
      @click="getCurrentLocation"
      class="absolute top-5 right-2.5 bg-white w-10 h-10 rounded-full flex items-center justify-center shadow-md transition-colors z-20 hover:bg-gray-100 active:bg-gray-200"
      aria-label="取得目前位置"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-700">
        <circle cx="12" cy="12" r="10"></circle>
        <circle cx="12" cy="12" r="3"></circle>
      </svg>
    </button>

    <!-- Selected Marker Info Card -->
    <div
      v-if="selectedMarker"
      class="absolute bottom-5 left-1/2 transform -translate-x-1/2 bg-white p-4 rounded-xl shadow-lg max-w-[90%] w-[85%] md:w-[400px] md:p-6 z-40 flex justify-between items-start gap-4"
    >
      <div class="flex-1">
        <h3 class="m-0 mb-2 text-lg font-semibold text-gray-800">{{ selectedMarker.name || selectedMarker.title }}</h3>
        <p v-if="selectedMarker.site || selectedMarker.address" class="m-0 my-1 text-sm text-gray-500">
          📍 {{ selectedMarker.site || selectedMarker.address }}
        </p>
        <p v-if="selectedMarker.distance" class="m-0 my-1 text-sm text-indigo-500 font-medium">
          {{ selectedMarker.distance }} 公里
        </p>
      </div>
      <button @click="selectedMarker = null" class="bg-transparent border-0 p-0 text-2xl text-gray-400 leading-none hover:text-gray-800 cursor-pointer" aria-label="關閉資訊卡">✕</button>
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
    const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || 'YOUR_API_KEY'
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
    
    await loadGoogleMapsScript()
    
    map.value = new google.maps.Map(mapDiv.value, {
      center: props.center,
      zoom: props.zoom,
      mapTypeId: props.mapTypeId,
      disableDefaultUI: true,
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
  googleMarkers.value.forEach(marker => {
    if (!marker) return
    if (typeof marker.setMap === 'function') {
      marker.setMap(null)
    } else if ('map' in marker) {
      // AdvancedMarkerElement may use the `map` property
      try { marker.map = null } catch (e) { /* ignore */ }
    }
  })
  googleMarkers.value = []

  // Add new markers
  markersList.forEach(markerData => {
    let marker = null
    const position = { lat: markerData.lat, lng: markerData.lng }

    // Prefer AdvancedMarkerElement when available
    if (window.google && window.google.maps && window.google.maps.marker && window.google.maps.marker.AdvancedMarkerElement) {
      try {
        marker = new window.google.maps.marker.AdvancedMarkerElement({
          map: map.value,
          position,
          title: markerData.name || markerData.title,
        })
      } catch (e) {
        // fall back to classic Marker on error
        marker = new window.google.maps.Marker({
          position,
          map: map.value,
          title: markerData.name || markerData.title,
          icon: props.markerIcon || undefined,
        })
      }
    } else {
      marker = new window.google.maps.Marker({
        position,
        map: map.value,
        title: markerData.name || markerData.title,
        icon: props.markerIcon || undefined,
      })
    }

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
        
        // Add user location marker. Prefer AdvancedMarkerElement for newer API.
        if (window.google && window.google.maps && window.google.maps.marker && window.google.maps.marker.AdvancedMarkerElement) {
          // create a small styled element for the marker content
          const el = document.createElement('div')
          el.style.width = '16px'
          el.style.height = '16px'
          el.style.background = '#4285F4'
          el.style.border = '2px solid white'
          el.style.borderRadius = '50%'
          el.style.boxSizing = 'border-box'

          try {
            userLocationMarker.value = new window.google.maps.marker.AdvancedMarkerElement({
              map: map.value,
              position: pos,
              title: '您的位置',
              content: el,
            })
          } catch (e) {
            // fallback
            userLocationMarker.value = new window.google.maps.Marker({
              position: pos,
              map: map.value,
              title: '您的位置',
              icon: {
                path: window.google.maps.SymbolPath.CIRCLE,
                fillColor: '#4285F4',
                fillOpacity: 1,
                scale: 8,
                strokeColor: 'white',
                strokeWeight: 2
              }
            })
          }
        } else {
          userLocationMarker.value = new window.google.maps.Marker({
            position: pos,
            map: map.value,
            title: '您的位置',
            icon: {
              path: window.google.maps.SymbolPath.CIRCLE,
              fillColor: '#4285F4',
              fillOpacity: 1,
              scale: 8,
              strokeColor: 'white',
              strokeWeight: 2
            }
          })
        }
        
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
  let marker = null
  const position = { lat: markerData.lat, lng: markerData.lng }

  if (window.google && window.google.maps && window.google.maps.marker && window.google.maps.marker.AdvancedMarkerElement) {
    try {
      marker = new window.google.maps.marker.AdvancedMarkerElement({
        map: map.value,
        position,
        title: markerData.name || markerData.title,
      })
    } catch (e) {
      marker = new window.google.maps.Marker({
        position,
        map: map.value,
        title: markerData.name || markerData.title,
        icon: markerData.icon || props.markerIcon || undefined,
      })
    }
  } else {
    marker = new window.google.maps.Marker({
      position,
      map: map.value,
      title: markerData.name || markerData.title,
      icon: markerData.icon || props.markerIcon || undefined,
    })
  }

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