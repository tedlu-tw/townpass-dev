<template>
  <div class="w-full flex flex-col items-center">
    <WeatherCard class="fixed z-10" :coordinates="mapCenter" />
    <MapView :zoom="16" :geojson-url="geojson" @center-changed="handleCenterChanged" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import MapView from '../components/MapView.vue'
import WeatherCard from '../components/WeatherCard.vue'

const geojson = ref("/map.geojson")
const mapCenter = ref(null)

function handleCenterChanged(center) {
  mapCenter.value = center
}
</script>