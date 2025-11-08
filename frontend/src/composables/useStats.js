import { ref, computed } from 'vue'

export function useStats() {
  const rideHistory = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Total statistics
  const totalStats = computed(() => {
    return {
      totalRides: rideHistory.value.length,
      totalDistance: rideHistory.value.reduce((sum, ride) => sum + (ride.distance || 0), 0),
      totalTime: rideHistory.value.reduce((sum, ride) => sum + (ride.duration || 0), 0),
      totalCalories: rideHistory.value.reduce((sum, ride) => sum + (ride.calories || 0), 0),
      totalCost: rideHistory.value.reduce((sum, ride) => sum + (ride.cost || 0), 0),
      carbonSaved: rideHistory.value.reduce((sum, ride) => sum + (ride.distance || 0) * 0.12, 0) // 0.12kg CO2 per km
    }
  })

  // Monthly statistics
  const monthlyStats = computed(() => {
    const now = new Date()
    const currentMonth = now.getMonth()
    const currentYear = now.getFullYear()

    const monthlyRides = rideHistory.value.filter(ride => {
      const rideDate = new Date(ride.date)
      return rideDate.getMonth() === currentMonth && rideDate.getFullYear() === currentYear
    })

    return {
      totalRides: monthlyRides.length,
      totalDistance: monthlyRides.reduce((sum, ride) => sum + (ride.distance || 0), 0),
      totalTime: monthlyRides.reduce((sum, ride) => sum + (ride.duration || 0), 0),
      totalCalories: monthlyRides.reduce((sum, ride) => sum + (ride.calories || 0), 0),
      totalCost: monthlyRides.reduce((sum, ride) => sum + (ride.cost || 0), 0),
      carbonSaved: monthlyRides.reduce((sum, ride) => sum + (ride.distance || 0) * 0.12, 0)
    }
  })

  // Weekly statistics
  const weeklyStats = computed(() => {
    const now = new Date()
    const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)

    const weeklyRides = rideHistory.value.filter(ride => {
      const rideDate = new Date(ride.date)
      return rideDate >= weekAgo
    })

    return {
      totalRides: weeklyRides.length,
      totalDistance: weeklyRides.reduce((sum, ride) => sum + (ride.distance || 0), 0),
      totalTime: weeklyRides.reduce((sum, ride) => sum + (ride.duration || 0), 0),
      totalCalories: weeklyRides.reduce((sum, ride) => sum + (ride.calories || 0), 0),
      totalCost: weeklyRides.reduce((sum, ride) => sum + (ride.cost || 0), 0),
      carbonSaved: weeklyRides.reduce((sum, ride) => sum + (ride.distance || 0) * 0.12, 0)
    }
  })

  // Average statistics
  const averageStats = computed(() => {
    const count = rideHistory.value.length || 1
    return {
      avgDistance: totalStats.value.totalDistance / count,
      avgDuration: totalStats.value.totalTime / count,
      avgSpeed: totalStats.value.totalDistance / (totalStats.value.totalTime / 3600),
      avgCalories: totalStats.value.totalCalories / count,
      avgCost: totalStats.value.totalCost / count
    }
  })

  // Add a new ride to history
  const addRide = (ride) => {
    const rideWithDate = {
      ...ride,
      id: Date.now(),
      date: new Date().toISOString()
    }
    rideHistory.value.unshift(rideWithDate)
    saveToLocalStorage()
  }

  // Load rides from API or localStorage
  const loadRides = async () => {
    loading.value = true
    error.value = null

    try {
      // Try to load from API first
      // const response = await axios.get('/api/rides')
      // rideHistory.value = response.data

      // Fallback to localStorage
      const stored = localStorage.getItem('rideHistory')
      if (stored) {
        rideHistory.value = JSON.parse(stored)
      } else {
        // Initialize with empty array
        rideHistory.value = []
      }
    } catch (err) {
      console.error('Error loading ride history:', err)
      error.value = '無法載入騎乘記錄'
      
      // Try localStorage as fallback
      const stored = localStorage.getItem('rideHistory')
      if (stored) {
        rideHistory.value = JSON.parse(stored)
      }
    } finally {
      loading.value = false
    }
  }

  // Save to localStorage
  const saveToLocalStorage = () => {
    try {
      localStorage.setItem('rideHistory', JSON.stringify(rideHistory.value))
    } catch (err) {
      console.error('Error saving to localStorage:', err)
    }
  }

  // Delete a ride
  const deleteRide = (rideId) => {
    rideHistory.value = rideHistory.value.filter(ride => ride.id !== rideId)
    saveToLocalStorage()
  }

  // Clear all rides
  const clearHistory = () => {
    rideHistory.value = []
    saveToLocalStorage()
  }

  // Get rides by date range
  const getRidesByDateRange = (startDate, endDate) => {
    return rideHistory.value.filter(ride => {
      const rideDate = new Date(ride.date)
      return rideDate >= startDate && rideDate <= endDate
    })
  }

  return {
    rideHistory,
    loading,
    error,
    totalStats,
    monthlyStats,
    weeklyStats,
    averageStats,
    addRide,
    loadRides,
    deleteRide,
    clearHistory,
    getRidesByDateRange
  }
}
