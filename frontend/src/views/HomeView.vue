<template>
  <div class="home-view">
    <section class="hero">
      <h1>🚴 開始你的騎乘之旅</h1>
      <p class="subtitle">智慧城市騎乘服務，讓每一次騎行都更美好</p>
      <router-link to="/ride" class="cta-button">立即開始騎乘</router-link>
    </section>

    <section class="quick-stats">
      <SummaryCard :stats="monthlyStats" period="本月統計" />
    </section>

    <section class="weather-section">
      <WeatherCard :weather="weather" :loading="weatherLoading" :error="weatherError" />
    </section>

    <section class="recent-rides">
      <h2>最近騎乘記錄</h2>
      <div v-if="rideHistory.length === 0" class="no-rides">
        <p>還沒有騎乘記錄，開始你的第一次騎行吧！</p>
      </div>
      <div v-else class="rides-list">
        <RideSummaryCard 
          v-for="ride in recentRides" 
          :key="ride.id" 
          :rideSummary="ride" 
        />
      </div>
      <router-link to="/history" class="view-all-link" v-if="rideHistory.length > 0">
        查看全部記錄 →
      </router-link>
    </section>

    <section class="features">
      <div class="feature-card">
        <div class="icon">📍</div>
        <h3>即時定位</h3>
        <p>精準記錄您的騎乘路線與距離</p>
      </div>
      <div class="feature-card">
        <div class="icon">📊</div>
        <h3>數據分析</h3>
        <p>詳細的騎乘統計與坡度分析</p>
      </div>
      <div class="feature-card">
        <div class="icon">🌤️</div>
        <h3>天氣資訊</h3>
        <p>即時天氣幫助您規劃行程</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import SummaryCard from '../components/SummaryCard.vue'
import WeatherCard from '../components/WeatherCard.vue'
import RideSummaryCard from '../components/RideSummaryCard.vue'
import { useStats } from '../composables/useStats'
import { useWeather } from '../composables/useWeather'

const { rideHistory, monthlyStats, loadRides } = useStats()
const { weather, loading: weatherLoading, error: weatherError, fetchWeather } = useWeather()

const recentRides = computed(() => rideHistory.value.slice(0, 3))

onMounted(async () => {
  await loadRides()
  await fetchWeather()
})
</script>

<style scoped>
.home-view {
  padding: 2rem 0;
}

.hero {
  text-align: center;
  padding: 3rem 0;
  margin-bottom: 3rem;
}

.hero h1 {
  font-size: 3rem;
  color: #333;
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.3rem;
  color: #666;
  margin-bottom: 2rem;
}

.cta-button {
  display: inline-block;
  padding: 1rem 3rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 50px;
  font-size: 1.2rem;
  font-weight: 600;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.quick-stats {
  margin-bottom: 3rem;
}

.weather-section {
  margin-bottom: 3rem;
}

.recent-rides {
  margin-bottom: 3rem;
}

.recent-rides h2 {
  color: #333;
  margin-bottom: 1.5rem;
}

.no-rides {
  background: white;
  border-radius: 12px;
  padding: 3rem;
  text-align: center;
  color: #666;
}

.rides-list {
  display: grid;
  gap: 1.5rem;
}

.view-all-link {
  display: block;
  text-align: center;
  margin-top: 1.5rem;
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.view-all-link:hover {
  color: #5568d3;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: all 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  color: #333;
  margin-bottom: 0.5rem;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}
</style>
