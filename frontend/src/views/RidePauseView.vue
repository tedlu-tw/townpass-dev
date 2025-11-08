<template>
  <div class="w-full flex flex-col items-center">
    <WeatherCard class="fixed z-10" :coordinates="mapCenter" />
    <MapView :zoom="16" :center="mapCenter" :markers="stationMarkers" @center-changed="onCenterChanged" />
    <div class="bg-[#E7A43C] w-full flex flex-col items-center">
      <span class="text-white text-m">本次騎行已經消耗了 {{ calories }} kcal</span>
    </div>
    <div class="bg-white w-full h-1/4 flex flex-col justify-center">
      <div class="text-[#5AB4C5] font-semibold text-center py-3">
        <h2 class="text-2xl ">持續時間 <span class="text-4xl">{{ formatted_time }}</span> </h2>
      </div>
      <div class="text-[#5AB4C5] font-semibold text-center py-3">
        <h2 class="text-2xl text-[#5AB4C5] font-semibold">騎行距離 <span class="text-4xl">{{ distance }}</span> KM</h2>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import MapView from '../components/MapView.vue'
import WeatherCard from '../components/WeatherCard.vue'
import { useStationMarkers } from '../composables/useStationMarkers'
import { useGeoLocation } from '../composables/useGeoLocation'

// Ride data
const calories = ref("0")
const distance = ref("0.00")
const formatted_time = ref("00:00:00")
const rideId = ref(null)
const startTime = ref(null)
const pausedAtSeconds = ref(null) // Snapshot of duration when paused

// Station markers
const mapCenter = ref(null)
const { stationMarkers, handleCenterChanged } = useStationMarkers()

// Geolocation
const { location: userLocation, startWatching, stopWatching } = useGeoLocation()

// API base URL
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000'
const router = useRouter()

// Format duration as HH:MM:SS
const formatDuration = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)
  return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
}

// Fetch ride status from backend
const fetchRideStatus = async () => {
  if (!rideId.value) {
    console.error('No ride ID available')
    return
  }
  
  try {
    const response = await fetch(`${apiUrl}/api/ride/status?ride_id=${rideId.value}`)
    const data = await response.json()
    
    if (response.ok) {
      // Update display values
      distance.value = data.distance_km.toFixed(2)
      calories.value = Math.round(data.calories).toString()
      
      // Snapshot the duration at pause time (frozen time)
      pausedAtSeconds.value = data.duration_seconds
      formatted_time.value = formatDuration(data.duration_seconds)
      
      // If we don't have startTime yet, calculate it from duration
      if (!startTime.value && data.duration_seconds) {
        const now = new Date()
        startTime.value = new Date(now.getTime() - (data.duration_seconds * 1000)).toISOString()
      }
      
      console.log('Ride status fetched (paused at):', data.duration_seconds, 'seconds')
    } else {
      console.error('Failed to fetch ride status:', data.error)
    }
  } catch (error) {
    console.error('Error fetching ride status:', error)
  }
}

// Map center changed handler (from user dragging map)
function onCenterChanged(center) {
  mapCenter.value = center
  handleCenterChanged(center)
}

// Watch for location changes and update map center
watch(userLocation, (newLocation) => {
  if (newLocation && !mapCenter.value) {
    // Only set initial center, don't override user's manual map movements
    mapCenter.value = {
      lat: newLocation.latitude,
      lng: newLocation.longitude
    }
  }
}, { deep: true, immediate: true })

onMounted(() => {
  // Start watching user location
  startWatching()
  
  // If location is already available, set it immediately
  if (userLocation.value) {
    mapCenter.value = {
      lat: userLocation.value.latitude,
      lng: userLocation.value.longitude
    }
  }
  
  // Get ride ID and start time from sessionStorage
  rideId.value = sessionStorage.getItem('currentRideId')
  startTime.value = sessionStorage.getItem('currentRideStartTime')
  
  // Load last known state immediately for instant display
  const savedDistance = sessionStorage.getItem('currentRideDistance')
  const savedCalories = sessionStorage.getItem('currentRideCalories')
  const savedTime = sessionStorage.getItem('currentRideFormattedTime')
  
  if (savedDistance) distance.value = savedDistance
  if (savedCalories) calories.value = savedCalories
  if (savedTime) formatted_time.value = savedTime
  
  if (rideId.value) {
    console.log('RidePauseView: Found ride ID:', rideId.value)
    
    // Record pause start time
    const pauseStartTime = new Date().toISOString()
    sessionStorage.setItem('pauseStartTime', pauseStartTime)
    
    // Fetch initial ride status (this will update with fresh data from API)
    fetchRideStatus()
    
    // DO NOT start duration update interval - time should be frozen when paused
    // The time displayed will be the snapshot from fetchRideStatus
  } else {
    console.warn('No ride ID found, cannot fetch ride status')
  }
})

onUnmounted(() => {
  stopWatching()
  
  // If leaving pause view (e.g., continuing ride), record pause duration
  if (router.currentRoute.value.path === '/ride') {
    const pauseStart = sessionStorage.getItem('pauseStartTime')
    if (pauseStart) {
      const pauseEnd = new Date()
      const pauseDuration = Math.floor((pauseEnd - new Date(pauseStart)) / 1000)
      
      // Add to total paused time
      const currentPausedTime = parseInt(sessionStorage.getItem('totalPausedSeconds') || '0')
      sessionStorage.setItem('totalPausedSeconds', (currentPausedTime + pauseDuration).toString())
      
      console.log(`Paused for ${pauseDuration} seconds, total paused: ${currentPausedTime + pauseDuration}`)
    }
  }
})
</script>