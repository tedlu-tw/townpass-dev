<template>
  <div class="summary-card">
    <div class="card-header">
      <h3>📊 個人統計</h3>
      <span class="period">{{ period }}</span>
    </div>

    <div class="stats-grid">
      <div class="stat-item">
        <span class="icon">🚴</span>
        <span class="label">總騎乘次數</span>
        <span class="value">{{ stats?.totalRides || 0 }}</span>
      </div>

      <div class="stat-item">
        <span class="icon">📍</span>
        <span class="label">總騎乘距離</span>
        <span class="value">{{ (stats?.totalDistance || 0).toFixed(1) }} km</span>
      </div>

      <div class="stat-item">
        <span class="icon">⏱️</span>
        <span class="label">總騎乘時間</span>
        <span class="value">{{ formatTotalTime(stats?.totalTime) }}</span>
      </div>

      <div class="stat-item">
        <span class="icon">🔥</span>
        <span class="label">總消耗熱量</span>
        <span class="value">{{ (stats?.totalCalories || 0).toLocaleString() }} kcal</span>
      </div>

      <div class="stat-item">
        <span class="icon">💰</span>
        <span class="label">總花費</span>
        <span class="value">${{ stats?.totalCost || 0 }}</span>
      </div>

      <div class="stat-item">
        <span class="icon">🌍</span>
        <span class="label">減碳量</span>
        <span class="value">{{ (stats?.carbonSaved || 0).toFixed(2) }} kg</span>
      </div>
    </div>

    <div class="achievements">
      <h4>🏆 成就</h4>
      <div class="achievement-list">
        <span v-for="achievement in achievements" :key="achievement" class="badge">
          {{ achievement }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  stats: {
    type: Object,
    default: null
  },
  period: {
    type: String,
    default: '本月統計'
  }
})

const achievements = computed(() => {
  const list = []
  if (props.stats?.totalRides >= 10) list.push('🚴 騎士新手')
  if (props.stats?.totalRides >= 50) list.push('🏅 資深騎士')
  if (props.stats?.totalDistance >= 100) list.push('📍 百里騎士')
  if (props.stats?.totalDistance >= 500) list.push('⭐ 千里騎士')
  return list.length > 0 ? list : ['開始你的騎乘之旅！']
})

const formatTotalTime = (seconds) => {
  if (!seconds) return '0小時'
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  return `${hours}小時 ${minutes}分`
}
</script>

<style scoped>
.summary-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f0f0f0;
}

.card-header h3 {
  margin: 0;
  color: #333;
}

.period {
  color: #667eea;
  font-weight: 500;
  font-size: 0.9rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.5rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.stat-item .icon {
  font-size: 2rem;
}

.stat-item .label {
  font-size: 0.85rem;
  color: #666;
}

.stat-item .value {
  font-size: 1.3rem;
  font-weight: bold;
  color: #667eea;
}

.achievements {
  padding-top: 1rem;
  border-top: 2px solid #f0f0f0;
}

.achievements h4 {
  margin: 0 0 1rem 0;
  color: #333;
}

.achievement-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.badge {
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}
</style>
