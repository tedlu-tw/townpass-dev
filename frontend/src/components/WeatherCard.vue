<template>
  <div class="weather-card">
    <div class="weather-header">
      <h3>🌤️ 天氣資訊</h3>
      <span class="location">{{ weather?.location || '台北市' }}</span>
    </div>

    <div v-if="loading" class="loading">載入中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="weather-content">
      <div class="temperature">
        <span class="temp-value">{{ weather?.temperature || '--' }}°C</span>
        <span class="temp-feels">體感 {{ weather?.feelsLike || '--' }}°C</span>
      </div>

      <div class="weather-details">
        <div class="detail-item">
          <span class="icon">💧</span>
          <span class="label">濕度</span>
          <span class="value">{{ weather?.humidity || '--' }}%</span>
        </div>
        <div class="detail-item">
          <span class="icon">💨</span>
          <span class="label">風速</span>
          <span class="value">{{ weather?.windSpeed || '--' }} m/s</span>
        </div>
        <div class="detail-item">
          <span class="icon">🌡️</span>
          <span class="label">氣壓</span>
          <span class="value">{{ weather?.pressure || '--' }} hPa</span>
        </div>
      </div>

      <div class="weather-description">
        {{ weather?.description || '晴朗' }}
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  weather: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  }
})
</script>

<style scoped>
.weather-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.weather-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.weather-header h3 {
  margin: 0;
  font-size: 1.2rem;
}

.location {
  font-size: 0.9rem;
  opacity: 0.9;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
}

.temperature {
  text-align: center;
  margin-bottom: 1.5rem;
}

.temp-value {
  display: block;
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.temp-feels {
  font-size: 0.9rem;
  opacity: 0.9;
}

.weather-details {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.detail-item .icon {
  font-size: 1.5rem;
}

.detail-item .label {
  font-size: 0.8rem;
  opacity: 0.9;
}

.detail-item .value {
  font-size: 1rem;
  font-weight: 600;
}

.weather-description {
  text-align: center;
  font-size: 1.1rem;
  opacity: 0.95;
  text-transform: capitalize;
}
</style>
