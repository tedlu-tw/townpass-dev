<template>
  <div class="pause-view">
    <div class="pause-screen">
      <h2>⏸️ 騎乘已暫停</h2>
      <p class="pause-message">休息一下，準備好後繼續前進！</p>

      <div class="ride-stats">
        <div class="stat">
          <span class="label">已騎時間</span>
          <span class="value">{{ formattedDuration }}</span>
        </div>
        <div class="stat">
          <span class="label">已騎距離</span>
          <span class="value">{{ rideData.distance.toFixed(2) }} km</span>
        </div>
        <div class="stat">
          <span class="label">平均速度</span>
          <span class="value">{{ rideData.avgSpeed.toFixed(1) }} km/h</span>
        </div>
        <div class="stat">
          <span class="label">消耗熱量</span>
          <span class="value">{{ rideData.calories }} kcal</span>
        </div>
      </div>

      <WeatherCard :weather="weather" :loading="weatherLoading" :error="weatherError" />

      <div class="tips-section">
        <h3>💡 騎乘小提示</h3>
        <ul class="tips-list">
          <li>記得適時補充水分</li>
          <li>注意交通安全，遵守號誌</li>
          <li>保持適當車速，享受騎乘樂趣</li>
          <li>休息時可以伸展一下，放鬆肌肉</li>
        </ul>
      </div>

      <div class="pause-controls">
        <button @click="handleResume" class="resume-button">
          ▶️ 繼續騎乘
        </button>
        <button @click="confirmEnd = true" class="end-button">
          🏁 結束騎乘
        </button>
      </div>
    </div>

    <!-- Confirm End Dialog -->
    <div v-if="confirmEnd" class="modal-overlay" @click="confirmEnd = false">
      <div class="modal-content" @click.stop>
        <h3>確認結束騎乘？</h3>
        <p>騎乘將會結束，請選擇結束站點</p>
        <div class="modal-actions">
          <button @click="confirmEnd = false" class="cancel-btn">取消</button>
          <button @click="handleEnd" class="confirm-btn">確認結束</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import WeatherCard from '../components/WeatherCard.vue'
import { useRideSession } from '../composables/useRideSession'
import { useWeather } from '../composables/useWeather'

const router = useRouter()

const { rideData, formattedDuration, resumeRide } = useRideSession()
const { weather, loading: weatherLoading, error: weatherError, fetchWeather } = useWeather()

const confirmEnd = ref(false)

const handleResume = () => {
  resumeRide()
  router.push('/ride')
}

const handleEnd = () => {
  confirmEnd.value = false
  router.push('/ride') // Return to ride view to select end station
}

onMounted(() => {
  fetchWeather()
})
</script>

<style scoped>
.pause-view {
  padding: 2rem 0;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.pause-screen {
  max-width: 800px;
  width: 100%;
}

h2 {
  text-align: center;
  color: #333;
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.pause-message {
  text-align: center;
  color: #666;
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

.ride-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stat .label {
  display: block;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.stat .value {
  display: block;
  color: #667eea;
  font-size: 1.8rem;
  font-weight: bold;
}

.tips-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin: 2rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.tips-section h3 {
  color: #333;
  margin-bottom: 1rem;
}

.tips-list {
  list-style: none;
  padding: 0;
}

.tips-list li {
  padding: 0.75rem 0;
  color: #666;
  border-bottom: 1px solid #f0f0f0;
}

.tips-list li:last-child {
  border-bottom: none;
}

.tips-list li:before {
  content: "✓ ";
  color: #27ae60;
  font-weight: bold;
  margin-right: 0.5rem;
}

.pause-controls {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-top: 2rem;
}

.resume-button, .end-button {
  padding: 1rem;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.resume-button {
  background: #27ae60;
  color: white;
}

.end-button {
  background: #e74c3c;
  color: white;
}

.resume-button:hover, .end-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  max-width: 400px;
  text-align: center;
}

.modal-content h3 {
  margin-bottom: 1rem;
  color: #333;
}

.modal-content p {
  color: #666;
  margin-bottom: 2rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
}

.cancel-btn, .confirm-btn {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.cancel-btn {
  background: #95a5a6;
  color: white;
}

.confirm-btn {
  background: #e74c3c;
  color: white;
}
</style>
