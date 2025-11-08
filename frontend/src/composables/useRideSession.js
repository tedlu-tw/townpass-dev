import { ref, computed } from 'vue'

export function useRideSession() {
  const isRiding = ref(false)
  const isPaused = ref(false)
  const startTime = ref(null)
  const pauseTime = ref(null)
  const totalPausedTime = ref(0)
  const currentLocation = ref(null)
  const rideData = ref({
    distance: 0,
    duration: 0,
    avgSpeed: 0,
    maxSpeed: 0,
    calories: 0,
    elevation: 0,
    path: [],
    startStation: null,
    endStation: null
  })

  const elapsedTime = computed(() => {
    if (!startTime.value) return 0
    const now = isPaused.value ? pauseTime.value : Date.now()
    return Math.floor((now - startTime.value - totalPausedTime.value) / 1000)
  })

  const formattedDuration = computed(() => {
    const seconds = elapsedTime.value
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    const secs = seconds % 60
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  })

  const startRide = (station) => {
    isRiding.value = true
    isPaused.value = false
    startTime.value = Date.now()
    totalPausedTime.value = 0
    rideData.value = {
      distance: 0,
      duration: 0,
      avgSpeed: 0,
      maxSpeed: 0,
      calories: 0,
      elevation: 0,
      path: [],
      startStation: station,
      endStation: null
    }
  }

  const pauseRide = () => {
    if (!isRiding.value || isPaused.value) return
    isPaused.value = true
    pauseTime.value = Date.now()
  }

  const resumeRide = () => {
    if (!isRiding.value || !isPaused.value) return
    const pauseDuration = Date.now() - pauseTime.value
    totalPausedTime.value += pauseDuration
    isPaused.value = false
  }

  const finishRide = (endStation) => {
    if (!isRiding.value) return null

    rideData.value.duration = elapsedTime.value
    rideData.value.endStation = endStation
    
    const summary = { ...rideData.value }
    
    // Reset state
    isRiding.value = false
    isPaused.value = false
    startTime.value = null
    pauseTime.value = null
    totalPausedTime.value = 0
    
    return summary
  }

  const updateLocation = (location) => {
    currentLocation.value = location
    
    if (!isRiding.value || isPaused.value) return
    
    // Add to path
    rideData.value.path.push({
      lat: location.latitude,
      lng: location.longitude,
      timestamp: Date.now(),
      altitude: location.altitude || 0
    })

    // Calculate distance and speed
    if (rideData.value.path.length > 1) {
      const lastPoint = rideData.value.path[rideData.value.path.length - 2]
      const distance = calculateDistance(
        lastPoint.lat, lastPoint.lng,
        location.latitude, location.longitude
      )
      rideData.value.distance += distance

      // Calculate speed
      const timeDiff = (Date.now() - lastPoint.timestamp) / 1000 / 3600 // hours
      const speed = distance / timeDiff
      rideData.value.maxSpeed = Math.max(rideData.value.maxSpeed, speed)
      rideData.value.avgSpeed = rideData.value.distance / (elapsedTime.value / 3600)

      // Calculate elevation gain
      const elevGain = Math.max(0, location.altitude - lastPoint.altitude)
      rideData.value.elevation += elevGain

      // Estimate calories (rough calculation)
      rideData.value.calories = Math.floor(rideData.value.distance * 40)
    }
  }

  const calculateDistance = (lat1, lng1, lat2, lng2) => {
    const R = 6371 // Earth's radius in km
    const dLat = toRad(lat2 - lat1)
    const dLng = toRad(lng2 - lng1)
    const a = 
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
      Math.sin(dLng / 2) * Math.sin(dLng / 2)
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
    return R * c
  }

  const toRad = (degrees) => degrees * Math.PI / 180

  return {
    isRiding,
    isPaused,
    rideData,
    currentLocation,
    elapsedTime,
    formattedDuration,
    startRide,
    pauseRide,
    resumeRide,
    finishRide,
    updateLocation
  }
}
