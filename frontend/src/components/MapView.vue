<template>
  <div class="relative w-full h-full">
    <div ref="mapDiv" class="w-full h-full"></div>

    <!-- Center crosshair to indicate map center coordinate -->
    <div v-if="props.crosshair" class="absolute inset-0 flex items-center justify-center pointer-events-none">
      <div class="relative w-6 h-6">
        <!-- vertical line -->
        <div class="absolute left-1/2 top-0 transform -translate-x-1/2 h-6 w-[3px] bg-[#5AB4C5]"></div>
        <!-- horizontal line -->
        <div class="absolute top-1/2 left-0 transform -translate-y-1/2 w-6 h-[3px] bg-[#5AB4C5]"></div>
      </div>
    </div>

    <div v-if="loading" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white px-8 py-4 rounded-lg shadow-md font-medium z-50">
      載入地圖中...
    </div>

    <!-- GPS Location Button -->
    <button
      v-if="!loading && showGpsButton"
      @click="getCurrentLocation"
      class="absolute top-[15vh] right-5 bg-white w-10 h-10 rounded-full flex items-center justify-center shadow-md transition-colors hover:bg-gray-100 active:bg-gray-200"
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
      <div class="flex-1 flex-col justify-center items-center">
        <h3 class="m-0 mb-2 text-2xl font-semibold text-[#5AB4C5] text-center">{{ selectedMarker.name }}</h3>
        <p class="m-0 my-1 text-lg text-[#5AB4C5] text-center flex items-center justify-center gap-2">
          <!-- location icon -->
          <svg width="14" height="15" viewBox="0 0 14 15" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">
            <path d="M6.73828 1L6.73832 0H6.73828V1ZM12.4756 6.46582L13.4756 6.46586V6.46582H12.4756ZM7.12305 13.3105L7.57124 14.2045L7.57126 14.2045L7.12305 13.3105ZM6.35352 13.3105L5.90532 14.2045L5.90562 14.2046L6.35352 13.3105ZM1 6.46582H0V6.46586L1 6.46582ZM6.73828 4.12305L6.73838 3.12305H6.73828V4.12305ZM4.2793 6.46582H3.2793V6.4659L4.2793 6.46582ZM6.73828 8.80762V9.80762H6.73838L6.73828 8.80762ZM9.19727 6.46582L10.1973 6.4659V6.46582H9.19727ZM6.73828 1L6.73824 2C9.40102 2.00011 11.4756 4.04485 11.4756 6.46582H12.4756H13.4756C13.4756 2.85008 10.4132 0.000146687 6.73832 0L6.73828 1ZM12.4756 6.46582L11.4756 6.46578C11.4755 8.01896 10.6589 9.3271 9.58316 10.3765C8.51012 11.4234 7.274 12.1162 6.67484 12.4166L7.12305 13.3105L7.57126 14.2045C8.25799 13.8602 9.69806 13.0585 10.9798 11.8081C12.2588 10.5603 13.4755 8.76846 13.4756 6.46586L12.4756 6.46582ZM7.12305 13.3105L6.67485 12.4166C6.7137 12.3971 6.76322 12.3973 6.80141 12.4165L6.35352 13.3105L5.90562 14.2046C6.43076 14.4677 7.0455 14.4681 7.57124 14.2045L7.12305 13.3105ZM6.35352 13.3105L6.80171 12.4166C6.20255 12.1162 4.96618 11.4234 3.89288 10.3765C2.8169 9.32707 2.00006 8.01893 2 6.46578L1 6.46582L0 6.46586C9.17315e-05 8.76862 1.21713 10.5605 2.49643 11.8083C3.77841 13.0587 5.21872 13.8602 5.90532 14.2045L6.35352 13.3105ZM1 6.46582H2C2 4.04495 4.07524 2 6.73828 2V1V0C3.06345 0 0 2.84983 0 6.46582H1ZM6.73828 4.12305V3.12305C4.87396 3.12305 3.2793 4.57494 3.2793 6.46582H4.2793H5.2793C5.2793 5.76948 5.88637 5.12305 6.73828 5.12305V4.12305ZM4.2793 6.46582L3.2793 6.4659C3.27944 8.35709 4.8745 9.80762 6.73828 9.80762V8.80762V7.80762C5.88595 7.80762 5.27935 7.16161 5.2793 6.46574L4.2793 6.46582ZM6.73828 8.80762L6.73838 9.80762C8.60187 9.80744 10.1971 8.35711 10.1973 6.4659L9.19727 6.46582L8.19727 6.46574C8.19721 7.16144 7.59058 7.80754 6.73819 7.80762L6.73828 8.80762ZM9.19727 6.46582H10.1973C10.1973 4.57493 8.60241 3.12322 6.73838 3.12305L6.73828 4.12305L6.73819 5.12305C7.59016 5.12313 8.19727 5.76964 8.19727 6.46582H9.19727Z" fill="#5AB4C5"/>
          </svg>
          <span>{{ selectedMarker.site }}</span>
        </p>
        <h3 class="m-0 mb-2 text-[#91A0A8] text-center text-lg">可借：{{ selectedMarker.available_bikes }} / 可還：{{ selectedMarker.available_docks }}</h3>
      </div>
      <button @click="selectedMarker = null" class="fixed right-5 bg-transparent border-0 p-0 text-2xl text-[#5AB4C5] leading-none hover:text-gray-800 cursor-pointer" aria-label="關閉資訊卡">✕</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

// ============================================================================
// Props & Emits
// ============================================================================

const props = defineProps({
  center: {
    type: Object,
    default: () => ({ lat: 25.0374865, lng: 121.5647688 })
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
    default: 'roadmap'
  },
  showGpsButton: {
    type: Boolean,
    default: true
  },
  markerIcon: {
    type: Object,
    default: null
  },
  crosshair: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['marker-click', 'map-ready', 'location-found', 'center-changed'])

// ============================================================================
// State
// ============================================================================

const mapDiv = ref(null)
const map = ref(null)
const loading = ref(true)
const googleMarkers = ref([])
const selectedMarker = ref(null)
const userLocationMarker = ref(null)
const currentLocation = ref(null)
const mapCenter = ref(null)

// ============================================================================
// Constants
// ============================================================================

// Map color keys to SVG asset URLs (resolved at build time via Vite)
const iconMap = {
  green: new URL('../assets/icons/ubike_green.svg', import.meta.url).href,
  red: new URL('../assets/icons/ubike_red.svg', import.meta.url).href,
  yellow: new URL('../assets/icons/ubike_yellow.svg', import.meta.url).href,
  grey: new URL('../assets/icons/ubike_grey.svg', import.meta.url).href,
}

// ============================================================================
// Google Maps Initialization
// ============================================================================

const loadGoogleMapsScript = () => {
  return new Promise((resolve, reject) => {
    if (window.google && window.google.maps) {
      resolve()
      return
    }

    const script = document.createElement('script')
    const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || 'YOUR_API_KEY'
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&callback=initMap`
    script.async = true
    script.defer = true
    
    window.initMap = () => resolve()
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
      clickableIcons: false,
      disableDefaultUI: true,
      streetViewControl: false,
      mapTypeControl: false,
      fullscreenControl: false,
      zoomControl: false,
    })

    loading.value = false
    emit('map-ready', map.value)
    
    // Listen for center changes
    map.value.addListener('center_changed', () => {
      const center = map.value.getCenter()
      if (center) {
        const centerCoords = {
          lat: center.lat(),
          lng: center.lng()
        }
        mapCenter.value = centerCoords
        emit('center-changed', centerCoords)
      }
    })
    
    // Emit initial center
    const initialCenter = map.value.getCenter()
    if (initialCenter) {
      const centerCoords = {
        lat: initialCenter.lat(),
        lng: initialCenter.lng()
      }
      mapCenter.value = centerCoords
      emit('center-changed', centerCoords)
    }
    
    if (props.geojsonUrl) {
      await loadGeoJsonMarkers()
    } else if (props.markers.length > 0) {
      updateMarkers()
    }

    if (props.showGpsButton) {
      getCurrentLocation()
    }
  } catch (error) {
    console.error('Error initializing map:', error)
    console.error('Make sure your Google Maps API key is valid and Maps JavaScript API is enabled')
    loading.value = false
  }
}

// ============================================================================
// GeoJSON Loading
// ============================================================================

const loadGeoJsonMarkers = async () => {
  try {
    const response = await fetch(props.geojsonUrl)
    const data = await response.json()
    
    const markers = data.features.map(feature => ({
      lat: feature.geometry.coordinates[1],
      lng: feature.geometry.coordinates[0],
      name: feature.properties.name,
      site: feature.properties.site,
      id: feature.properties.id,
      ...feature.properties
    }))
    
    createMarkers(markers)
  } catch (error) {
    console.error('Error loading GeoJSON:', error)
  }
}

// ============================================================================
// Marker Management
// ============================================================================

const resolveIconSource = (rawIcon) => {
  if (typeof rawIcon === 'string') {
    return iconMap[rawIcon] || rawIcon
  } else if (rawIcon && typeof rawIcon === 'object') {
    return rawIcon.url || null
  }
  return null
}

const createMarkerElement = (position, title, iconSource) => {
  const hasAdvancedMarker = window.google?.maps?.marker?.AdvancedMarkerElement

  if (hasAdvancedMarker) {
    try {
      if (iconSource) {
        const wrap = document.createElement('div')
        wrap.style.cssText = 'width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;'

        const img = document.createElement('img')
        img.src = iconSource
        img.style.cssText = 'max-width: 100%; max-height: 100%; object-fit: contain;'
        wrap.appendChild(img)

        return new google.maps.marker.AdvancedMarkerElement({
          map: map.value,
          position,
          title,
          content: wrap
        })
      } else {
        return new google.maps.marker.AdvancedMarkerElement({
          map: map.value,
          position,
          title
        })
      }
    } catch (err) {
      return new google.maps.Marker({
        position,
        map: map.value,
        title,
        icon: iconSource || undefined
      })
    }
  }

  return new google.maps.Marker({
    position,
    map: map.value,
    title,
    icon: iconSource || undefined
  })
}

const clearMarkers = () => {
  googleMarkers.value.forEach(marker => {
    if (!marker) return
    if (typeof marker.setMap === 'function') {
      marker.setMap(null)
    } else if ('map' in marker) {
      try { marker.map = null } catch (e) { /* ignore */ }
    }
  })
  googleMarkers.value = []
}

const createMarkers = (markersList) => {
  clearMarkers()

  markersList.forEach(markerData => {
    const position = { lat: markerData.lat, lng: markerData.lng }
    const rawIcon = markerData.icon || props.markerIcon || null
    const iconSource = resolveIconSource(rawIcon)
    
    const marker = createMarkerElement(position, markerData.name, iconSource)

    marker.addListener('click', () => {
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

const addMarker = (markerData) => {
  if (!map.value) return

  const position = { lat: markerData.lat, lng: markerData.lng }
  const rawIcon = markerData.icon || props.markerIcon || null
  const iconSource = resolveIconSource(rawIcon)
  
  const marker = createMarkerElement(position, markerData.name || markerData.title, iconSource)

  marker.addListener('click', () => {
    selectedMarker.value = markerData
    emit('marker-click', markerData)
  })

  googleMarkers.value.push(marker)
  return marker
}

// ============================================================================
// User Location
// ============================================================================

const createUserLocationMarker = (pos) => {
  const hasAdvancedMarker = window.google?.maps?.marker?.AdvancedMarkerElement

  if (hasAdvancedMarker) {
    const el = document.createElement('div')
    el.style.cssText = 'width: 16px; height: 16px; background: #4285F4; border: 2px solid white; border-radius: 50%; box-sizing: border-box;'

    try {
      return new window.google.maps.marker.AdvancedMarkerElement({
        map: map.value,
        position: pos,
        title: '您的位置',
        content: el,
      })
    } catch (e) {
      return new window.google.maps.Marker({
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
  }

  return new window.google.maps.Marker({
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

const getCurrentLocation = () => {
  if (!navigator.geolocation) return

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      }
      
      currentLocation.value = pos
      
      if (userLocationMarker.value) {
        userLocationMarker.value.setMap(null)
      }
      
      userLocationMarker.value = createUserLocationMarker(pos)
      map.value.setCenter(pos)
      
      emit('location-found', pos)
    },
    (error) => {
      console.error('Error getting location:', error)
    }
  )
}

// ============================================================================
// Utilities
// ============================================================================

const calculateDistance = (lat1, lng1, lat2, lng2) => {
  const R = 6371
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

// ============================================================================
// Watchers & Lifecycle
// ============================================================================

watch(() => props.markers, () => {
  if (map.value) {
    updateMarkers()
  }
}, { deep: true })

watch(() => props.center, (newCenter) => {
  if (map.value) {
    map.value.setCenter(newCenter)
  }
}, { deep: true })

onMounted(() => {
  initMap()
})

// ============================================================================
// Expose Public API
// ============================================================================

defineExpose({
  setCenter,
  setZoom,
  addMarker,
  clearMarkers,
  getCurrentLocation,
  map
})
</script>