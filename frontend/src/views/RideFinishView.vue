<template>
  <div class="finish-view">
    <div class="finish-screen">
      <div class="success-header">
        <h1>🎉 騎乘完成！</h1>
        <p class="congratulations">恭喜您完成這次騎乘</p>
      </div>

      <RideSummaryCard :rideSummary="rideSummary" :showWeather="true" />

      <div class="elevation-section" v-if="elevationData.length > 0">
        <ElevationChart :data="elevationData" />
      </div>

      <div class="achievements-section">
        <h3>🏆 本次成就</h3>
        <div class="achievements-list">
          <div class="achievement" v-for="achievement in achievements" :key="achievement">
            {{ achievement }}
          </div>
        </div>
      </div>

      <div class="sharing-section">
        <h3>📤 分享您的成就</h3>
        <div class="share-buttons">
          <button class="share-btn facebook">
            <span>Facebook</span>
          </button>
          <button class="share-btn twitter">
            <span>Twitter</span>
          </button>
          <button class="share-btn line">
            <span>LINE</span>
          </button>
        </div>
      </div>

      <div class="action-buttons">
        <button @click="saveRide" class="save-btn">
          💾 儲存記錄
        </button>
        <router-link to="/ride" class="new-ride-btn">
          🚴 開始新騎乘
        </router-link>
        <router-link to="/history" class="history-btn">
          📊 查看歷史
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import RideSummaryCard from '../components/RideSummaryCard.vue'
import ElevationChart from '../components/ElevationChart.vue'
import { useStats } from '../composables/useStats'
import { useWeather } from '../composables/useWeather'

const router = useRouter()
const route = useRoute()

const { addRide } = useStats()
const { weather, fetchWeather } = useWeather()

// Get ride summary from route params or use mock data
const rideSummary = ref(route.params.summary || {
  date: new Date().toISOString(),
  duration: 1800, // 30 minutes
  distance: 5.2,
  avgSpeed: 15.5,
  maxSpeed: 25.3,
  calories: 208,
  elevation: 45,
  cost: 10,
  startStation: '台北車站',
  endStation: '西門站',
  weather: null
})

const elevationData = ref([
  { distance: 0, elevation: 10 },
  { distance: 1, elevation: 15 },
  { distance: 2, elevation: 25 },
  { distance: 3, elevation: 35 },
  { distance: 4, elevation: 40 },
  { distance: 5, elevation: 45 }
])

const achievements = computed(() => {
  const list = []
  if (rideSummary.value.distance >= 5) list.push('🎯 距離達成 5km+')
  if (rideSummary.value.duration >= 1800) list.push('⏱️ 騎乘時間 30分鐘+')
  if (rideSummary.value.avgSpeed >= 15) list.push('⚡ 平均速度 15km/h+')
  if (rideSummary.value.elevation >= 30) list.push('⛰️ 爬升高度 30m+')
  if (list.length === 0) list.push('💪 完成騎乘挑戰')
  return list
})

const saveRide = () => {
  // Add weather info if available
  if (weather.value) {
    rideSummary.value.weather = {
      temperature: weather.value.temperature,
      condition: weather.value.description
    }
  }
  
  addRide(rideSummary.value)
  alert('騎乘記錄已儲存！')
  router.push('/history')
}

onMounted(async () => {
  await fetchWeather()
  // Add weather to summary if available
  if (weather.value) {
    rideSummary.value.weather = {
      temperature: weather.value.temperature,
      condition: weather.value.description
    }
  }
})
</script>

<style scoped>
.finish-view {
  padding: 2rem 0;
}

.finish-screen {
  max-width: 900px;
  margin: 0 auto;
}

.success-header {
  text-align: center;
  margin-bottom: 3rem;
}

.success-header h1 {
  font-size: 3rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.congratulations {
  font-size: 1.2rem;
  color: #666;
}

.elevation-section {
  margin: 2rem 0;
}

.achievements-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin: 2rem 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.achievements-section h3 {
  color: #333;
  margin-bottom: 1rem;
}

.achievements-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.achievement {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  font-weight: 500;
}

.sharing-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin: 2rem 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.sharing-section h3 {
  color: #333;
  margin-bottom: 1rem;
}

.share-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.share-btn {
  flex: 1;
  min-width: 150px;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  color: white;
}

.facebook {
  background: #1877f2;
}

.twitter {
  background: #1da1f2;
}

.line {
  background: #00b900;
}

.share-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.action-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 2rem;
}

.save-btn, .new-ride-btn, .history-btn {
  padding: 1rem;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  text-align: center;
  text-decoration: none;
  display: block;
  transition: all 0.3s;
}

.save-btn {
  background: #27ae60;
  color: white;
}

.new-ride-btn {
  background: #667eea;
  color: white;
}

.history-btn {
  background: #95a5a6;
  color: white;
}

.save-btn:hover, .new-ride-btn:hover, .history-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
</style>
