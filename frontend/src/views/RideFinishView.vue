<template>
    <div class="w-full flex flex-col items-center">
        <MapView :zoom="16" :geojson-url="geojson" />
        <div class="absolute inset-0 bg-white bg-opacity-85 z-10 flex flex-col justify-center items-center">
            <div class="bg-[#5AB4C5] w-[90%] h-[95%] rounded-[8px] relative">
                <!-- 關閉按鈕 -->
                <button @click="goHome" class="absolute top-3 right-3 text-white hover:text-gray-200 text-3xl font-bold z-20">
                    ×
                </button>
                
                <div class="flex flex-col h-full items-center">
                    <h3 class="text-white font-semibold text-xl mt-5 ml-5 text-shadow self-start"> 2025/11/08 09:41 的騎行
                    </h3>
                    
                    <!-- 大卡片 -->
                    <div class="w-[90%] mt-3 mb-3" style="height: 55%;">
                        <div class="bg-white rounded-[8px] overflow-hidden h-full flex flex-col">
                            <!-- 地圖區域 -->
                            <div class="h-[50%] min-h-[120px]">
                                <MapView :crosshair="false" :show-gps-button="false" />
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
                            
                            <!-- 借車點和還車點 -->
                            <div class="flex-1 p-4 flex flex-col justify-center">
                                <div class="mb-3">
                                    <h4 class="text-[#5AB4C5] text-base font-semibold mb-1">
                                        <svg class="inline-block w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                                        </svg>
                                        最近借車點
                                    </h4>
                                    <p class="text-gray-700 text-sm ml-5">和平新生路口西南側</p>
                                </div>
                                <div>
                                    <h4 class="text-[#5AB4C5] text-base font-semibold mb-1">
                                        <svg class="inline-block w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                                        </svg>
                                        還車點
                                    </h4>
                                    <p class="text-gray-700 text-sm ml-5">建國南路二段瑞安街264巷口</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="ml-[10%] mb-5 self-start">
                        <p class="text-white font-semibold text-2xl">本次騎行你成功...</p>
                        <p class="text-white text-2xl">消耗 80 kcal</p>
                        <p class="text-white text-2xl">減碳 3.54 kgCO2e</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import MapView from '../components/MapView.vue'

const router = useRouter()
const geojson = ref("/map.geojson")
const calories = ref("123")
const distance = ref("123")
const formatted_time = ref("123")

const goHome = () => {
  router.push('/home')
}
</script>