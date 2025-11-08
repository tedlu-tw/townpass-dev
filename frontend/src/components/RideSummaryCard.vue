<template>
  <div class="ride-summary-card">
    <div class="card-header">
      <h3>🚴 騎乘總結</h3>
      <span class="ride-date">{{ formatDate(rideSummary?.date) }}</span>
    </div>

    <div class="summary-grid">
      <div class="summary-item">
        <span class="icon">⏱️</span>
        <span class="label">騎乘時間</span>
        <span class="value">{{ formatDuration(rideSummary?.duration) }}</span>
      </div>

      <div class="summary-item">
        <span class="icon">📍</span>
        <span class="label">騎乘距離</span>
        <span class="value">{{ (rideSummary?.distance || 0).toFixed(2) }} km</span>
      </div>

      <div class="summary-item">
        <span class="icon">⚡</span>
        <span class="label">平均速度</span>
        <span class="value">{{ (rideSummary?.avgSpeed || 0).toFixed(1) }} km/h</span>
      </div>

      <div class="summary-item">
        <span class="icon">🔥</span>
        <span class="label">消耗熱量</span>
        <span class="value">{{ rideSummary?.calories || 0 }} kcal</span>
      </div>

      <div class="summary-item">
        <span class="icon">⛰️</span>
        <span class="label">爬升高度</span>
        <span class="value">{{ (rideSummary?.elevation || 0).toFixed(0) }} m</span>
      </div>

      <div class="summary-item">
        <span class="icon">💰</span>
        <span class="label">費用</span>
        <span class="value">${{ rideSummary?.cost || 0 }}</span>
      </div>
    </div>

    <div class="route-info">
      <div class="route-item">
        <span class="route-label">起點:</span>
        <span class="route-value">{{ rideSummary?.startStation || '未知' }}</span>
      </div>
      <div class="route-item">
        <span class="route-label">終點:</span>
        <span class="route-value">{{ rideSummary?.endStation || '未知' }}</span>
      </div>
    </div>

    <div v-if="showWeather && rideSummary?.weather" class="weather-info">
      <span>🌤️ {{ rideSummary.weather.temperature }}°C, {{ rideSummary.weather.condition }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  rideSummary: {
    type: Object,
    default: null
  },
  showWeather: {
    type: Boolean,
    default: true
  }
})

const formatDate = (date) => {
  if (!date) return '今天'
  return new Date(date).toLocaleDateString('zh-TW', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatDuration = (seconds) => {
  if (!seconds) return '0分'
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  return hours > 0 ? `${hours}小時 ${minutes}分` : `${minutes}分`
}
</script>

<style scoped>
.ride-summary-card {
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

.ride-date {
  color: #666;
  font-size: 0.9rem;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.summary-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.5rem;
}

.summary-item .icon {
  font-size: 2rem;
}

.summary-item .label {
  font-size: 0.85rem;
  color: #666;
}

.summary-item .value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #667eea;
}

.route-info {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.route-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
}

.route-label {
  font-weight: 600;
  color: #666;
}

.route-value {
  color: #333;
}

.weather-info {
  text-align: center;
  padding: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 8px;
  font-size: 0.95rem;
}
</style>
