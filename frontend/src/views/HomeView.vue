<template>
  <div class="w-full flex flex-col items-center">
    <WeatherCard class="fixed z-10" :coordinates="mapCenter" />
    <MapView :zoom="16" :markers="stationMarkers" @center-changed="onCenterChanged" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import MapView from '../components/MapView.vue'
import WeatherCard from '../components/WeatherCard.vue'
import { useStationMarkers } from '../composables/useStationMarkers'

const mapCenter = ref(null)
const { stationMarkers, handleCenterChanged } = useStationMarkers()

function onCenterChanged(center) {
	mapCenter.value = center
	handleCenterChanged(center)
}

</script>