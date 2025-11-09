import { ref } from 'vue'

export function useStationMarkers() {
  const stationMarkers = ref([])
  const isLoading = ref(false)
  const fetchError = ref(null)
  const lastFetchedCenter = ref(null)
  const fetchTimeout = ref(null)

  // 計算兩點之間的距離（公尺）
  function calculateDistance(lat1, lng1, lat2, lng2) {
    const R = 6371e3 // 地球半徑（公尺）
    const φ1 = lat1 * Math.PI / 180
    const φ2 = lat2 * Math.PI / 180
    const Δφ = (lat2 - lat1) * Math.PI / 180
    const Δλ = (lng2 - lng1) * Math.PI / 180

    const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
      Math.cos(φ1) * Math.cos(φ2) *
      Math.sin(Δλ / 2) * Math.sin(Δλ / 2)
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))

    return R * c
  }

  async function fetchStations(lat, lng) {
    if (!lat || !lng) return
    
    // 如果已有上次的位置，檢查距離
    if (lastFetchedCenter.value) {
      const distance = calculateDistance(
        lastFetchedCenter.value.lat,
        lastFetchedCenter.value.lng,
        lat,
        lng
      )
      // 如果移動距離小於 200 公尺，不重新獲取
      if (distance < 200) {
        return
      }
    }
    
    // 如果正在載入中，不重新獲取
    if (isLoading.value) {
      return
    }
    
    isLoading.value = true
    fetchError.value = null
    
    try {
      const apiUrl = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://localhost:5000' : '')
      const response = await fetch(`${apiUrl}/api/station/nearby?lat=${lat}&lng=${lng}&radius=2000`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      // 將 API 資料轉換為 markers 格式
      if (data.features && Array.isArray(data.features)) {
        const validMarkers = []
        
        for (const feature of data.features) {
          // 檢查基本結構
          if (!feature.geometry || !feature.geometry.coordinates || !Array.isArray(feature.geometry.coordinates)) {
            console.warn('Missing geometry or coordinates:', feature)
            continue
          }
          
          const coords = feature.geometry.coordinates
          if (coords.length < 2) {
            console.warn('Insufficient coordinates:', coords)
            continue
          }
          
          // 轉換為數字
          const lat = Number(coords[1])
          const lng = Number(coords[0])
          
          // 嚴格驗證
          if (!Number.isFinite(lat) || !Number.isFinite(lng)) {
            console.warn('Invalid coordinates after conversion:', { lat, lng, original: coords })
            continue
          }
          
          // 合理範圍檢查（台灣範圍）
          if (lat < 21 || lat > 26 || lng < 119 || lng > 122) {
            console.warn('Coordinates out of Taiwan range:', { lat, lng })
            continue
          }
          
          // 創建 marker 對象，MapView 期望 lat/lng 在頂層
          const marker = {
            ...feature.properties,
            lat,
            lng,
            title: feature.properties?.name || feature.properties?.site || '站點'
          }
          
          validMarkers.push(marker)
        }
        
        console.log(`Loaded ${validMarkers.length} valid markers out of ${data.features.length} total`)
        stationMarkers.value = validMarkers
        
        // 記錄最後獲取的位置
        lastFetchedCenter.value = { lat, lng }
      }
    } catch (error) {
      console.error('Error fetching station data:', error)
      fetchError.value = error.message
      stationMarkers.value = []
    } finally {
      isLoading.value = false
    }
  }

  function handleCenterChanged(center) {
    // 清除之前的計時器
    if (fetchTimeout.value) {
      clearTimeout(fetchTimeout.value)
    }
    
    // 設置防抖：地圖停止移動 500ms 後才獲取資料
    fetchTimeout.value = setTimeout(() => {
      if (center && center.lat && center.lng) {
        fetchStations(center.lat, center.lng)
      }
    }, 500)
  }

  return {
    stationMarkers,
    isLoading,
    fetchError,
    fetchStations,
    handleCenterChanged
  }
}
