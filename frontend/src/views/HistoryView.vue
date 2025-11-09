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
        time: '18:23',
        duration: '00:28:15',
        distance: '7.82 KM'
    },
    {
        date: '2025/11/07',
        time: '07:45',
        duration: '00:35:42',
        distance: '9.15 KM'
    },
    {
        date: '2025/11/06',
        time: '19:10',
        duration: '00:22:30',
        distance: '5.64 KM'
    },
    {
        date: '2025/11/04',
        time: '08:20',
        duration: '00:41:18',
        distance: '11.23 KM'
    },
    {
        date: '2025/11/03',
        time: '17:55',
        duration: '00:19:47',
        distance: '4.92 KM'
    },
    {
        date: '2025/11/01',
        time: '14:30',
        duration: '00:31:25',
        distance: '8.47 KM'
    }
])

// 10 月的騎行記錄
const octoberRecords = ref([
    {
        date: '2025/10/31',
        time: '09:15',
        duration: '00:44:20',
        distance: '12.35 KM'
    },
    {
        date: '2025/10/29',
        time: '18:40',
        duration: '00:26:53',
        distance: '6.78 KM'
    },
    {
        date: '2025/10/28',
        time: '07:30',
        duration: '00:38:12',
        distance: '10.24 KM'
    },
    {
        date: '2025/10/27',
        time: '19:20',
        duration: '00:21:45',
        distance: '5.31 KM'
    },
    {
        date: '2025/10/25',
        time: '08:45',
        duration: '00:33:28',
        distance: '8.96 KM'
    },
    {
        date: '2025/10/24',
        time: '17:15',
        duration: '00:29:37',
        distance: '7.52 KM'
    },
    {
        date: '2025/10/22',
        time: '10:30',
        duration: '00:46:15',
        distance: '13.18 KM'
    },
    {
        date: '2025/10/21',
        time: '07:50',
        duration: '00:24:42',
        distance: '6.15 KM'
    },
    {
        date: '2025/10/19',
        time: '18:25',
        duration: '00:36:50',
        distance: '9.87 KM'
    },
    {
        date: '2025/10/18',
        time: '08:10',
        duration: '00:27:18',
        distance: '7.04 KM'
    },
    {
        date: '2025/10/16',
        time: '19:45',
        duration: '00:40:33',
        distance: '11.42 KM'
    },
    {
        date: '2025/10/15',
        time: '09:20',
        duration: '00:23:55',
        distance: '5.83 KM'
    },
    {
        date: '2025/10/13',
        time: '17:30',
        duration: '00:34:47',
        distance: '9.26 KM'
    },
    {
        date: '2025/10/12',
        time: '08:55',
        duration: '00:28:22',
        distance: '7.38 KM'
    },
    {
        date: '2025/10/10',
        time: '18:15',
        duration: '00:42:10',
        distance: '12.07 KM'
    },
    {
        date: '2025/10/09',
        time: '07:40',
        duration: '00:25:48',
        distance: '6.42 KM'
    },
    {
        date: '2025/10/07',
        time: '19:50',
        duration: '00:37:25',
        distance: '10.15 KM'
    },
    {
        date: '2025/10/06',
        time: '09:05',
        duration: '00:30:14',
        distance: '8.21 KM'
    },
    {
        date: '2025/10/04',
        time: '17:45',
        duration: '00:26:37',
        distance: '6.89 KM'
    },
    {
        date: '2025/10/03',
        time: '08:25',
        duration: '00:39:52',
        distance: '11.56 KM'
    },
    {
        date: '2025/10/01',
        time: '18:00',
        duration: '00:32:18',
        distance: '8.73 KM'
    }
])
</script>