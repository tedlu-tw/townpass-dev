<template>
    <div class="w-full flex flex-col items-center">
        <MapView :zoom="16" :geojson-url="geojson" />
        <div class="absolute inset-0 bg-white bg-opacity-85 z-10">
            <!-- 標題 -->
            <div class="px-5 pt-5 pb-3">
                <h1 class="text-3xl font-bold text-[#5AB4C5]">歷史紀錄</h1>
            </div>

            <!-- 可滾動內容區域 -->
            <div class="flex-1 overflow-y-auto px-5">
                <!-- 2025 年 11 月 -->
                <div class="mb-6">
                    <h2 class="text-gray-400 text-base mb-3">2025 年 11 月</h2>

                    <div v-for="(record, index) in novemberRecords" :key="`nov-${index}`"
                        class="bg-white rounded-lg shadow-md p-4 mb-3 flex">
                        <!-- 左側日期時間 -->
                        <div class="w-32 flex-shrink-0 text-center pr-4 border-r border-gray-200">
                            <p class="text-gray-700 text-sm">{{ record.date }}</p>
                            <p class="text-gray-700 text-sm">{{ record.time }}</p>
                        </div>

                        <!-- 右側資訊 -->
                        <div class="flex-1 pl-4">
                            <p class="text-gray-700 text-sm mb-1">騎行 {{ record.duration }}</p>
                            <p class="text-gray-700 text-sm">距離 {{ record.distance }}</p>
                        </div>
                    </div>
                </div>

                <!-- 2025 年 10 月 -->
                <div class="mb-6">
                    <h2 class="text-gray-400 text-base mb-3">2025 年 10 月</h2>

                    <div v-for="(record, index) in octoberRecords" :key="`oct-${index}`"
                        class="bg-white rounded-lg shadow-md p-4 mb-3 flex">
                        <!-- 左側日期時間 -->
                        <div class="w-32 flex-shrink-0 text-center pr-4 border-r border-gray-200">
                            <p class="text-gray-700 text-sm">{{ record.date }}</p>
                            <p class="text-gray-700 text-sm">{{ record.time }}</p>
                        </div>

                        <!-- 右側資訊 -->
                        <div class="flex-1 pl-4">
                            <p class="text-gray-700 text-sm mb-1">騎行 {{ record.duration }}</p>
                            <p class="text-gray-700 text-sm">距離 {{ record.distance }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import MapView from '../components/MapView.vue'

// 11 月的騎行記錄
const novemberRecords = ref([
    {
        date: '2025/11/08',
        time: '09:41',
        duration: '00:09:41',
        distance: '10.32 KM'
    },
    {
        date: '2025/11/08',
        time: '09:41',
        duration: '00:09:41',
        distance: '10.32 KM'
    },
    {
        date: '2025/11/08',
        time: '09:41',
        duration: '00:09:41',
        distance: '10.32 KM'
    }
])

// 10 月的騎行記錄
const octoberRecords = ref([
    {
        date: '2025/11/08',
        time: '09:41',
        duration: '00:09:41',
        distance: '10.32 KM'
    },
    {
        date: '2025/11/08',
        time: '09:41',
        duration: '00:09:41',
        distance: '10.32 KM'
    },
    {
        date: '2025/11/08',
        time: '09:41',
        duration: '00:09:41',
        distance: '10.32 KM'
    }
])
</script>