<template>
  
</template>

<script setup>
import { onMounted } from 'vue'
import { useStats } from '../composables/useStats'
import { useWeather } from '../composables/useWeather'

const { rideHistory, monthlyStats, loadRides } = useStats()
const { weather, loading: weatherLoading, error: weatherError, fetchWeather } = useWeather()

onMounted(async () => {
  await loadRides()
  await fetchWeather()
})
</script>