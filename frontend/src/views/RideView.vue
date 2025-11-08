<template>
    <div class="w-full flex flex-col items-center">
        <WeatherCard class="fixed z-20" />
        <div class="relative w-full h-full">
            <MapView :zoom="16" :geojson-url="geojson" />
            <div class="absolute inset-0 bg-white bg-opacity-60 z-10"></div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import MapView from '../components/MapView.vue'
import WeatherCard from '../components/WeatherCard.vue'

const geojson = ref("/map.geojson")
</script>