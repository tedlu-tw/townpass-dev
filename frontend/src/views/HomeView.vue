<template>
  <div class="w-full flex flex-col items-center">
    <WeatherCard class="fixed z-10"/>
    <MapView :zoom="16" :geojson-url="geojson" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import MapView from '../components/MapView.vue'
import WeatherCard from '../components/WeatherCard.vue'

const geojson = ref("/map.geojson")
</script>