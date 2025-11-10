<template>
    <div class="w-full flex flex-col items-center">
        <div class="relative w-full h-full">
            <MapView :zoom="16" :center="mapCenter" />
            <div class="absolute inset-0 bg-white bg-opacity-85 z-10 flex flex-col">
                <WeatherCard class="relative z-20" :coordinates="weatherCoordinates" />
                <div class="flex-1 flex flex-col justify-center items-center">
                    <div class="text-[#5AB4C5] font-semibold text-center py-3">
                        <h2 class="text-2xl ">持續時間</h2>
                        <h3 class="text-6xl">{{ formatted_time }}</h3>
                    </div>
                    <div class="text-[#5AB4C5] font-semibold text-center py-3">
                        <h2 class="text-2xl text-[#5AB4C5] font-semibold">騎行距離</h2>
                        <h3 class="text-6xl">{{ distance }}<span class="text-4xl">KM</span></h3>
                    </div>
                    <div class="relative mt-10">
                        <svg width="200" height="200" viewBox="0 0 140 141" fill="none"
                            xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M70 117.5C95.7733 117.5 116.667 96.4574 116.667 70.5C116.667 44.5426 95.7733 23.5 70 23.5C44.2267 23.5 23.3333 44.5426 23.3333 70.5C23.3333 96.4574 44.2267 117.5 70 117.5Z"
                                fill="white" />
                            <path
                                d="M70 129.25C102.217 129.25 128.333 102.947 128.333 70.5C128.333 38.0533 102.217 11.75 70 11.75C37.7834 11.75 11.6667 38.0533 11.6667 70.5C11.6667 102.947 37.7834 129.25 70 129.25Z"
                                stroke="#2EB6C7" stroke-opacity="0.4" stroke-width="10" />
                        </svg>
                        <div class="absolute inset-0 flex flex-col items-center justify-center">
                            <div class="text-[#5AB4C5] font-bold text-6xl">{{ speed }}</div>
                            <div class="text-[#5AB4C5] font-semibold text-xl mt-1">KM/h</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="bg-[#E7A43C] w-full flex flex-col items-center">
            <span class="text-white text-m">本次騎行已經消耗了 {{calories}} kcal</span>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import MapView from '../components/MapView.vue'
import WeatherCard from '../components/WeatherCard.vue'
import { useGeoLocation } from '../composables/useGeoLocation'

const formatted_time = ref("00:00:00")
const distance = ref("0.00")
const speed = ref("0.0")
const calories = ref("0")

// Ride session
const rideId = ref(null)
const userId = ref("user_default") // Should come from auth system
const startTime = ref(null)
const isRideActive = ref(false)
const isStartingRide = ref(false) // Flag to prevent multiple simultaneous starts

// Map center - will be updated with user location
const mapCenter = ref(null)

// Geolocation and weather data
const { location: userLocation, startWatching, stopWatching } = useGeoLocation()
const weatherCoordinates = ref(null)
let weatherUpdateInterval = null
let rideUpdateInterval = null
let rideStatusInterval = null
let durationUpdateInterval = null
let lastWeatherUpdate = 0

// API base URL
const apiUrl = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://localhost:5000' : '')

// Format duration as HH:MM:SS
const formatDuration = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)
  return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
}

// Update duration display from startTime
const updateDuration = () => {
  if (startTime.value && isRideActive.value) {
    // Parse startTime as UTC by appending 'Z' if not present
    const startTimeStr = startTime.value.endsWith('Z') ? startTime.value : startTime.value + 'Z'
    const start = new Date(startTimeStr)
    const now = new Date()
    
    // Debug: Log times if duration seems wrong
    const totalElapsed = Math.floor((now - start) / 1000)
    if (totalElapsed > 28800) { // More than 8 hours
      console.error('⚠️ Duration calculation issue:', {
        startTime: startTime.value,
        startDate: start.toString(),
        now: now.toString(),
        elapsed: totalElapsed
      })
    }
    
    const realElapsed = totalElapsed
    
    // Subtract total paused time
    const totalPausedSeconds = parseInt(sessionStorage.getItem('totalPausedSeconds') || '0')
    const activeDuration = realElapsed - totalPausedSeconds
    
    formatted_time.value = formatDuration(Math.max(0, activeDuration))
    
    // Save state for other views
    saveRideState()
  }
}

// Start ride session
const startRide = async () => {
  if (!userLocation.value) {
    console.error('Waiting for location...')
    return
  }
  
  // Prevent multiple simultaneous starts
  if (isStartingRide.value || isRideActive.value || rideId.value) {
    console.log('Ride already starting or active, skipping start request')
    return
  }
  
  isStartingRide.value = true
  
  try {
    const response = await fetch(`${apiUrl}/api/ride/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userId.value,
        start_location: {
          lat: userLocation.value.latitude,
          lng: userLocation.value.longitude
        }
      })
    })
    
    const data = await response.json()
    
    if (response.ok) {
      rideId.value = data.ride_id
      // Normalize startTime: ensure it has 'Z' suffix for UTC
      const normalizedStartTime = data.start_time.endsWith('Z') ? data.start_time : data.start_time + 'Z'
      startTime.value = normalizedStartTime
      isRideActive.value = true
      
      // Store ride info in sessionStorage for other views to access
      sessionStorage.setItem('currentRideId', data.ride_id)
      sessionStorage.setItem('currentRideStartTime', normalizedStartTime)
      
      // Initialize total paused time (reset on new ride)
      sessionStorage.setItem('totalPausedSeconds', '0')
      
      console.log('Ride started:', data)
      
      // Start duration update interval (every second)
      if (durationUpdateInterval) {
        clearInterval(durationUpdateInterval)
      }
      durationUpdateInterval = setInterval(updateDuration, 1000)
      updateDuration() // Update immediately
      
      // Start status polling for new ride
      if (rideStatusInterval) {
        clearInterval(rideStatusInterval)
      }
      rideStatusInterval = setInterval(() => {
        if (isRideActive.value && rideId.value) {
          fetchRideStatus()
        }
      }, 3000)
    } else {
      console.error('Failed to start ride:', data.error)
    }
  } catch (error) {
    console.error('Error starting ride:', error)
  } finally {
    isStartingRide.value = false
  }
}

// Send ride update with current location
const sendRideUpdate = async () => {
  if (!rideId.value || !userLocation.value) return
  
  try {
    const response = await fetch(`${apiUrl}/api/ride/update`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ride_id: rideId.value,
        current_location: {
          lat: userLocation.value.latitude,
          lng: userLocation.value.longitude
        },
        speed: userLocation.value.speed ? userLocation.value.speed * 3.6 : 0 // m/s to km/h
      })
    })
    
    if (!response.ok) {
      console.error('Failed to send ride update')
    }
  } catch (error) {
    console.error('Error sending ride update:', error)
  }
}

// Fetch current ride status from backend to update distance, speed, calories
const fetchRideStatus = async () => {
  if (!rideId.value) return
  
  try {
    const response = await fetch(`${apiUrl}/api/ride/status?ride_id=${rideId.value}`)
    const data = await response.json()
    
    if (response.ok) {
      // Update display values with backend calculations
      distance.value = data.distance_km.toFixed(2)
      speed.value = data.avg_speed_kmh.toFixed(1)
      calories.value = Math.round(data.calories).toString()
      
      console.log('📊 Ride status updated:', {
        distance: data.distance_km,
        speed: data.avg_speed_kmh,
        calories: data.calories
      })
    } else {
      console.error('Failed to fetch ride status:', data.error)
    }
  } catch (error) {
    console.error('Error fetching ride status:', error)
  }
}

// Save current ride state to sessionStorage
const saveRideState = () => {
  sessionStorage.setItem('currentRideDistance', distance.value)
  sessionStorage.setItem('currentRideCalories', calories.value)
  sessionStorage.setItem('currentRideSpeed', speed.value)
  sessionStorage.setItem('currentRideFormattedTime', formatted_time.value)
}

// Update weather coordinates from user location (throttled to 20 seconds)
const updateWeatherCoordinates = () => {
  const now = Date.now()
  
  if (userLocation.value && (now - lastWeatherUpdate >= 20000)) {
    weatherCoordinates.value = {
      lat: userLocation.value.latitude,
      lng: userLocation.value.longitude
    }
    lastWeatherUpdate = now
  }
}

// Watch for location changes and update map center + weather coordinates
watch(userLocation, (newLocation) => {
  if (newLocation) {
    // Update map center to current location for auto-tracking
    mapCenter.value = {
      lat: newLocation.latitude,
      lng: newLocation.longitude
    }
    
    updateWeatherCoordinates()
    
    // Note: Do NOT auto-start here - location updates frequently!
    // Auto-start is handled once in onMounted() after first location fix
  }
}, { deep: true })

onMounted(() => {
  // Start watching user location
  startWatching()
  
  // Check if returning from pause - restore ride state
  const existingRideId = sessionStorage.getItem('currentRideId')
  const existingStartTime = sessionStorage.getItem('currentRideStartTime')
  
  if (existingRideId && existingStartTime) {
    // Check if session is too old (more than 24 hours)
    const start = new Date(existingStartTime)
    const now = new Date()
    const hoursSinceStart = (now - start) / 1000 / 3600
    
    if (hoursSinceStart > 24) {
      console.warn('⚠️ Clearing old ride session (>24 hours old)')
      sessionStorage.clear()
      // Will start a new ride instead
    } else {
      // Restore ride session
      rideId.value = existingRideId
      startTime.value = existingStartTime
      isRideActive.value = true
      
      // Restore display values from sessionStorage
      const savedDistance = sessionStorage.getItem('currentRideDistance')
      const savedCalories = sessionStorage.getItem('currentRideCalories')
      const savedSpeed = sessionStorage.getItem('currentRideSpeed')
      const savedTime = sessionStorage.getItem('currentRideFormattedTime')
      
      if (savedDistance) distance.value = savedDistance
      if (savedCalories) calories.value = savedCalories
      if (savedSpeed) speed.value = savedSpeed
      if (savedTime) formatted_time.value = savedTime
      
      console.log('Restored ride session:', existingRideId)
      
      // Start duration update interval
      if (durationUpdateInterval) {
        clearInterval(durationUpdateInterval)
      }
      durationUpdateInterval = setInterval(updateDuration, 1000)
      updateDuration() // Update immediately
      
      // Start status polling for restored session
      if (rideStatusInterval) {
        clearInterval(rideStatusInterval)
      }
      rideStatusInterval = setInterval(() => {
        if (isRideActive.value && rideId.value) {
          fetchRideStatus()
        }
      }, 3000)
      fetchRideStatus() // Fetch immediately to get current values
    }
  }
  
  // Start a new ride if no valid session exists
  if (!rideId.value) {
    // Wait for first location update, then auto-start ride
    const unwatch = watch(userLocation, (newLocation) => {
      if (newLocation && !isRideActive.value && !rideId.value && !isStartingRide.value) {
        console.log('First location received, auto-starting ride...')
        // Update map center
        mapCenter.value = {
          lat: newLocation.latitude,
          lng: newLocation.longitude
        }
        // Update weather coordinates
        weatherCoordinates.value = {
          lat: newLocation.latitude,
          lng: newLocation.longitude
        }
        // Start ride once
        startRide()
        // Stop watching after first start
        unwatch()
      }
    })
  }
  
  // Set interval for weather updates (every 20 seconds)
  weatherUpdateInterval = setInterval(() => {
    if (userLocation.value) {
      weatherCoordinates.value = {
        lat: userLocation.value.latitude,
        lng: userLocation.value.longitude
      }
    }
  }, 20000)
  
  // Set interval for ride updates (every 5 seconds)
  rideUpdateInterval = setInterval(() => {
    if (isRideActive.value && rideId.value) {
      sendRideUpdate()
    }
  }, 5000)
  
  // Set interval for ride status updates (every 3 seconds) - fetch distance, speed, calories
  rideStatusInterval = setInterval(() => {
    if (isRideActive.value && rideId.value) {
      fetchRideStatus()
    }
  }, 3000)
})

onUnmounted(() => {
  stopWatching()
  
  if (weatherUpdateInterval) {
    clearInterval(weatherUpdateInterval)
  }
  
  if (rideUpdateInterval) {
    clearInterval(rideUpdateInterval)
  }
  
  if (rideStatusInterval) {
    clearInterval(rideStatusInterval)
  }
  
  if (durationUpdateInterval) {
    clearInterval(durationUpdateInterval)
  }
})

</script>