<template>
    <div class="w-full flex flex-col items-center">
        <MapView :zoom="16" :geojson-url="geojson" />
        <div class="absolute inset-0 bg-white bg-opacity-85 z-10 flex flex-col justify-center items-center">
            <div class="bg-[#5AB4C5] w-[90%] h-[80%] rounded-[8px] relative">
                <!-- 關閉按鈕 -->
                <button @click="goHome" class="absolute top-3 right-3 text-white hover:text-gray-200 text-3xl font-bold z-20">
                    ×
                </button>
                
                <div class="flex flex-col h-full items-center">
                    <h3 class="text-white font-semibold text-xl mt-5 ml-5 text-shadow self-start">{{ rideTitle }}
                    </h3>
                    
                    <!-- 大卡片 -->
                    <div class="w-[90%] mt-3 mb-3" style="height: 100%;">
                        <div class="bg-white rounded-[8px] overflow-hidden h-full flex flex-col">
                            <!-- 地圖區域 -->
                            <div class="h-full min-h-[120px]">
                                <MapView 
                                    :crosshair="false" 
                                    :show-gps-button="false" 
                                    :center="nearestStationCenter"
                                    :markers="nearestStationMarker ? [nearestStationMarker] : []"
                                    :zoom="17"
                                />
                            </div>
                            
                            <!-- 持續時間和騎行距離 -->
                            <div class="flex border-b border-gray-200">
                                <div class="flex-1 text-[#5AB4C5] text-center py-3 border-r border-gray-200">
                                    <p class="text-sm">持續時間</p>
                                    <p class="text-3xl font-bold mt-1">{{ formatted_time }}</p>
                                </div>
                                <div class="flex-1 text-[#5AB4C5] text-center py-3">
                                    <p class="text-sm">騎行距離</p>
                                    <p class="text-3xl font-bold mt-1">{{ distance }} <span class="text-lg">KM</span></p>
                                </div>
                            </div>
                            
                            <!-- 起始地址和還車點 -->
                            <div class="flex-1 p-4 flex flex-col justify-center">
                                <div>
                                    <h4 class="text-[#5AB4C5] text-base font-semibold mb-1">
                                        <svg class="inline-block w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                                        </svg>
                                        最近還車點
                                    </h4>
                                    <p class="text-gray-700 text-sm ml-5">{{ endStationName }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="ml-[10%] mb-5 self-start">
                        <p class="text-white font-semibold text-2xl">本次騎行你成功...</p>
                        <p class="text-white text-2xl">消耗 {{ calories }} kcal</p>
                        <p class="text-white text-2xl">減碳 {{ carbonSaved }} kgCO2e</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import MapView from '../components/MapView.vue'
import { useStationMarkers } from '../composables/useStationMarkers'
import { useGeoLocation } from '../composables/useGeoLocation'

const router = useRouter()
const geojson = ref("/map.geojson")
const calories = ref("0")
const distance = ref("0.00")
const formatted_time = ref("00:00:00")
const carbonSaved = ref("0.00")
const endStationName = ref("建國南路二段瑞安街264巷口")
const rideTitle = ref("騎行")
const nearestStationCenter = ref({ lat: 25.0374865, lng: 121.5647688 })
const nearestStationMarker = ref(null)

// API base URL (match other views)
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000'

// Get current location and nearby stations
const { location: userLocation, startWatching, stopWatching } = useGeoLocation()
const { stationMarkers, fetchStations } = useStationMarkers()

// Find nearest station from fetched stations (API already provides distance)
const findNearestStation = () => {
  if (!stationMarkers.value || stationMarkers.value.length === 0) {
    return null
  }

  // API returns stations sorted by distance, so first station is nearest
  // Or we can find the one with minimum distance property
  let nearest = null
  let minDistance = Infinity

  for (const station of stationMarkers.value) {
    const dist = station.distance || Infinity
    if (dist < minDistance) {
      minDistance = dist
      nearest = station
    }
  }

  return nearest
}

const goHome = () => {
  router.push('/home')
}

// Reverse geocode to get address from coordinates
const getAddressFromCoords = async (lat, lng) => {
    try {
        // Use Google Maps Geocoding API
        if (window.google && window.google.maps) {
            const geocoder = new window.google.maps.Geocoder()
            const latlng = { lat, lng }
            
            return new Promise((resolve, reject) => {
                geocoder.geocode({ location: latlng }, (results, status) => {
                    if (status === 'OK' && results && results[0]) {
                        // Get the formatted address
                        resolve(results[0].formatted_address)
                    } else {
                        reject(new Error('Geocoding failed: ' + status))
                    }
                })
            })
        } else {
            // Fallback: format coordinates as address
            return `${lat.toFixed(5)}, ${lng.toFixed(5)}`
        }
    } catch (err) {
        console.warn('Error geocoding:', err)
        return `${lat.toFixed(5)}, ${lng.toFixed(5)}`
    }
}

onMounted(() => {
    // When finishing, call backend finish API and then clear caches
    const rideId = sessionStorage.getItem('currentRideId')

    // helper to format minutes->HH:MM:SS
    const minutesToHms = (minutes) => {
        const secs = Math.round(minutes * 60)
        const h = Math.floor(secs / 3600)
        const m = Math.floor((secs % 3600) / 60)
        const s = secs % 60
        return `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`
    }

    // Try to get current browser geolocation (short timeout) to provide end_location
    const getCurrentPosition = (timeoutMs = 2000) => {
        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) return reject(new Error('Geolocation not available'))
            let resolved = false
            const timer = setTimeout(() => {
                if (!resolved) {
                    resolved = true
                    reject(new Error('Geolocation timeout'))
                }
            }, timeoutMs)

            navigator.geolocation.getCurrentPosition((pos) => {
                if (resolved) return
                resolved = true
                clearTimeout(timer)
                resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude })
            }, (err) => {
                if (resolved) return
                resolved = true
                clearTimeout(timer)
                reject(err)
            }, { enableHighAccuracy: false, maximumAge: 10000 })
        })
    }

    const callFinishApi = async () => {
        // Set ride title to current date and time
        const now = new Date()
        const year = now.getFullYear()
        const month = String(now.getMonth() + 1).padStart(2, '0')
        const day = String(now.getDate()).padStart(2, '0')
        const hours = String(now.getHours()).padStart(2, '0')
        const minutes = String(now.getMinutes()).padStart(2, '0')
        rideTitle.value = `${year}/${month}/${day} ${hours}:${minutes} 的騎行`
        
        if (!rideId) {
            // Load whatever cached values exist
            const savedDistance = sessionStorage.getItem('currentRideDistance')
            const savedCalories = sessionStorage.getItem('currentRideCalories')
            const savedTime = sessionStorage.getItem('currentRideFormattedTime')
            if (savedDistance) distance.value = savedDistance
            if (savedCalories) calories.value = savedCalories
            if (savedTime) formatted_time.value = savedTime
            return
        }

        // First, fetch start location BEFORE finishing (while session still exists)
        let startLocationData = null
        try {
            const statusRes = await fetch(`${apiUrl}/api/ride/status?ride_id=${rideId}`)
            if (!statusRes.ok) {
                // Fall back to cached values
                const savedDistance = sessionStorage.getItem('currentRideDistance')
                const savedCalories = sessionStorage.getItem('currentRideCalories')
                const savedTime = sessionStorage.getItem('currentRideFormattedTime')
                if (savedDistance) distance.value = savedDistance
                if (savedCalories) calories.value = savedCalories
                if (savedTime) formatted_time.value = savedTime
                return
            }
            const statusData = await statusRes.json()
            startLocationData = statusData.start_location
        } catch (err) {
            // Error checking session status
        }

        // Build request body
        const body = { ride_id: rideId }

        // Try to get current location for end_location and find nearest station
        let endLoc = null
        try {
            endLoc = await getCurrentPosition(2000).catch(() => null)
            if (endLoc) {
                body.end_location = endLoc
                
                // Fetch nearby stations and find the nearest one
                await fetchStations(endLoc.lat, endLoc.lng)
                const nearestStation = findNearestStation()
                if (nearestStation) {
                    endStationName.value = nearestStation.title || nearestStation.name || nearestStation.site || '還車點'
                    // Set map center to nearest station
                    nearestStationCenter.value = { lat: nearestStation.lat, lng: nearestStation.lng }
                    // Set marker for the station
                    nearestStationMarker.value = nearestStation
                }
            }
        } catch (e) {
            // ignore geolocation failure
        }

        try {
            const res = await fetch(`${apiUrl}/api/ride/finish`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            })

            const data = await res.json()
            
            if (res.ok && data.summary) {
                // Use backend summary to render final metrics
                const s = data.summary
                formatted_time.value = minutesToHms(s.duration_minutes)
                distance.value = (s.distance_km || 0).toFixed(2)
                calories.value = Math.round(s.calories || 0).toString()
                carbonSaved.value = (s.carbon_saved_kg || 0).toFixed(3)
                
                // Get start address from previously fetched start_location (before session was deleted)
                if (startLocationData) {
                    const address = await getAddressFromCoords(startLocationData.lat, startLocationData.lng)
                    startAddress.value = address
                } else {
                    startAddress.value = '起始地址'
                }
            } else {
                // fallback to cached values
                const savedDistance = sessionStorage.getItem('currentRideDistance')
                const savedCalories = sessionStorage.getItem('currentRideCalories')
                const savedTime = sessionStorage.getItem('currentRideFormattedTime')
                if (savedDistance) distance.value = savedDistance
                if (savedCalories) calories.value = savedCalories
                if (savedTime) formatted_time.value = savedTime
            }
        } catch (err) {
            // fallback to cached values
            const savedDistance = sessionStorage.getItem('currentRideDistance')
            const savedCalories = sessionStorage.getItem('currentRideCalories')
            const savedTime = sessionStorage.getItem('currentRideFormattedTime')
            if (savedDistance) distance.value = savedDistance
            if (savedCalories) calories.value = savedCalories
            if (savedTime) formatted_time.value = savedTime
        } finally {
            // Always clear ride-related sessionStorage after displaying results
            // This ensures the data is cleared whether API succeeds or fails
            const keysToClear = [
                'currentRideDistance', 'currentRideCalories', 'currentRideSpeed', 'currentRideFormattedTime',
                'currentRideId', 'currentRideStartTime', 'pauseStartTime', 'totalPausedSeconds'
            ]
            keysToClear.forEach(k => sessionStorage.removeItem(k))
        }
    }



    // Perform finish call immediately
    callFinishApi()
})
</script>