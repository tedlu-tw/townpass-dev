<template>
    <MapView :center="{ lat: 25.0374865, lng: 121.5647688 }" :zoom="16"/>
</template>

<script setup>
import { onMounted } from 'vue'
import { useStats } from '../composables/useStats'
import { useWeather } from '../composables/useWeather'
import MapView from '../components/MapView.vue'

const { rideHistory, monthlyStats, loadRides } = useStats()
const { weather, loading: weatherLoading, error: weatherError, fetchWeather } = useWeather()

onMounted(async () => {
  await loadRides()
  await fetchWeather()
})
</script>