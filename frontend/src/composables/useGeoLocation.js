import { ref, onMounted, onUnmounted } from 'vue'

export function useGeoLocation(options = {}) {
  const location = ref(null)
  const error = ref(null)
  const loading = ref(true)
  const watchId = ref(null)

  const defaultOptions = {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0,
    ...options
  }

  const updateLocation = (position) => {
    location.value = {
      latitude: position.coords.latitude,
      longitude: position.coords.longitude,
      altitude: position.coords.altitude,
      accuracy: position.coords.accuracy,
      altitudeAccuracy: position.coords.altitudeAccuracy,
      heading: position.coords.heading,
      speed: position.coords.speed,
      timestamp: position.timestamp
    }
    loading.value = false
    error.value = null
  }

  const handleError = (err) => {
    loading.value = false
    switch (err.code) {
      case err.PERMISSION_DENIED:
        error.value = '用戶拒絕了定位請求'
        break
      case err.POSITION_UNAVAILABLE:
        error.value = '位置信息不可用'
        break
      case err.TIMEOUT:
        error.value = '請求超時'
        break
      default:
        error.value = '發生未知錯誤'
    }
  }

  const startWatching = () => {
    if (!navigator.geolocation) {
      error.value = '您的瀏覽器不支持地理定位'
      loading.value = false
      return
    }

    // Get current position first
    navigator.geolocation.getCurrentPosition(
      updateLocation,
      handleError,
      defaultOptions
    )

    // Then watch for changes
    watchId.value = navigator.geolocation.watchPosition(
      updateLocation,
      handleError,
      defaultOptions
    )
  }

  const stopWatching = () => {
    if (watchId.value !== null) {
      navigator.geolocation.clearWatch(watchId.value)
      watchId.value = null
    }
  }

  const getCurrentPosition = () => {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error('您的瀏覽器不支持地理定位'))
        return
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          updateLocation(position)
          resolve(location.value)
        },
        (err) => {
          handleError(err)
          reject(error.value)
        },
        defaultOptions
      )
    })
  }

  const calculateDistance = (lat1, lng1, lat2, lng2) => {
    const R = 6371e3 // Earth's radius in meters
    const φ1 = toRad(lat1)
    const φ2 = toRad(lat2)
    const Δφ = toRad(lat2 - lat1)
    const Δλ = toRad(lng2 - lng1)

    const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
              Math.cos(φ1) * Math.cos(φ2) *
              Math.sin(Δλ / 2) * Math.sin(Δλ / 2)
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))

    return R * c // Distance in meters
  }

  const toRad = (degrees) => degrees * Math.PI / 180

  onMounted(() => {
    startWatching()
  })

  onUnmounted(() => {
    stopWatching()
  })

  return {
    location,
    error,
    loading,
    startWatching,
    stopWatching,
    getCurrentPosition,
    calculateDistance
  }
}
