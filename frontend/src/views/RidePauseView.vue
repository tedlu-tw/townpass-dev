<template>
  <div class="w-full flex flex-col items-center">
    <WeatherCard class="fixed z-10" />
    <MapView :zoom="16" :geojson-url="geojson" />
    <div class="bg-[#E7A43C] w-full flex flex-col items-center">
      <span class="text-white text-m">本次騎行已經消耗了 {{ calories }} kcal</span>
    </div>
    <div class="bg-white w-full h-1/4 flex flex-col justify-center">
      <div class="text-[#5AB4C5] font-semibold text-center py-3">
        <h2 class="text-2xl ">持續時間 <span class="text-4xl">{{ formatted_time }}</span> </h2>
      </div>
      <div class="text-[#5AB4C5] font-semibold text-center py-3">
        <h2 class="text-2xl text-[#5AB4C5] font-semibold">騎行距離 <span class="text-2xl">{{ distance }}</span> KM</h2>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import MapView from '../components/MapView.vue'
import WeatherCard from '../components/WeatherCard.vue'

const geojson = ref("/map.geojson")
const calories = ref("123")
const distance = ref("123")
const formatted_time = ref("123")
</script>