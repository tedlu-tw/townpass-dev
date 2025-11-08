<template>
  <div class="history-view">
    <div class="header">
      <h2>📊 騎乘歷史</h2>
      <div class="header-actions">
        <select v-model="filterPeriod" class="period-select">
          <option value="all">全部</option>
          <option value="week">本週</option>
          <option value="month">本月</option>
          <option value="year">今年</option>
        </select>
      </div>
    </div>

    <div class="stats-overview">
      <SummaryCard :stats="currentStats" :period="periodLabel" />
    </div>

    <div class="history-content">
      <div v-if="loading" class="loading">載入中...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="filteredRides.length === 0" class="no-data">
        <p>{{ filterPeriod === 'all' ? '尚無騎乘記錄' : '此期間沒有騎乘記錄' }}</p>
        <router-link to="/ride" class="start-riding-btn">開始騎乘</router-link>
      </div>
      <div v-else class="rides-timeline">
        <div v-for="(group, date) in groupedRides" :key="date" class="date-group">
          <h3 class="date-header">{{ formatDate(date) }}</h3>
          <div class="rides-in-date">
            <div v-for="ride in group" :key="ride.id" class="ride-item">
              <div class="ride-header">
                <span class="ride-time">{{ formatTime(ride.date) }}</span>
                <button @click="deleteRide(ride.id)" class="delete-btn">🗑️</button>
              </div>
              <RideSummaryCard :rideSummary="ride" :showWeather="false" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="export-section">
      <button @click="exportData" class="export-btn">
        📥 匯出記錄
      </button>
      <button @click="confirmClearAll = true" class="clear-btn">
        🗑️ 清除所有記錄
      </button>
    </div>

    <!-- Confirm Clear Dialog -->
    <div v-if="confirmClearAll" class="modal-overlay" @click="confirmClearAll = false">
      <div class="modal-content" @click.stop>
        <h3>⚠️ 確認清除？</h3>
        <p>這將永久刪除所有騎乘記錄，此操作無法復原。</p>
        <div class="modal-actions">
          <button @click="confirmClearAll = false" class="cancel-btn">取消</button>
          <button @click="handleClearAll" class="confirm-btn">確認清除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import SummaryCard from '../components/SummaryCard.vue'
import RideSummaryCard from '../components/RideSummaryCard.vue'
import { useStats } from '../composables/useStats'

const {
  rideHistory,
  loading,
  error,
  totalStats,
  weeklyStats,
  monthlyStats,
  loadRides,
  deleteRide: removeRide,
  clearHistory
} = useStats()

const filterPeriod = ref('all')
const confirmClearAll = ref(false)

const periodLabel = computed(() => {
  const labels = {
    all: '全部統計',
    week: '本週統計',
    month: '本月統計',
    year: '今年統計'
  }
  return labels[filterPeriod.value] || '統計'
})

const currentStats = computed(() => {
  switch (filterPeriod.value) {
    case 'week':
      return weeklyStats.value
    case 'month':
      return monthlyStats.value
    case 'all':
    default:
      return totalStats.value
  }
})

const filteredRides = computed(() => {
  const now = new Date()
  
  switch (filterPeriod.value) {
    case 'week': {
      const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
      return rideHistory.value.filter(ride => new Date(ride.date) >= weekAgo)
    }
    case 'month': {
      const currentMonth = now.getMonth()
      const currentYear = now.getFullYear()
      return rideHistory.value.filter(ride => {
        const rideDate = new Date(ride.date)
        return rideDate.getMonth() === currentMonth && rideDate.getFullYear() === currentYear
      })
    }
    case 'year': {
      const currentYear = now.getFullYear()
      return rideHistory.value.filter(ride => {
        return new Date(ride.date).getFullYear() === currentYear
      })
    }
    default:
      return rideHistory.value
  }
})

const groupedRides = computed(() => {
  const groups = {}
  filteredRides.value.forEach(ride => {
    const date = new Date(ride.date).toDateString()
    if (!groups[date]) {
      groups[date] = []
    }
    groups[date].push(ride)
  })
  return groups
})

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  const today = new Date()
  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)

  if (date.toDateString() === today.toDateString()) {
    return '今天'
  } else if (date.toDateString() === yesterday.toDateString()) {
    return '昨天'
  } else {
    return date.toLocaleDateString('zh-TW', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      weekday: 'short'
    })
  }
}

const formatTime = (dateStr) => {
  return new Date(dateStr).toLocaleTimeString('zh-TW', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

const handleClearAll = () => {
  clearHistory()
  confirmClearAll.value = false
}

const exportData = () => {
  const data = JSON.stringify(rideHistory.value, null, 2)
  const blob = new Blob([data], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `ride-history-${new Date().toISOString().split('T')[0]}.json`
  a.click()
  URL.revokeObjectURL(url)
}

onMounted(() => {
  loadRides()
})
</script>

<style scoped>
.history-view {
  padding: 2rem 0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header h2 {
  color: #333;
  margin: 0;
}

.period-select {
  padding: 0.5rem 1rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: border-color 0.3s;
}

.period-select:focus {
  outline: none;
  border-color: #667eea;
}

.stats-overview {
  margin-bottom: 3rem;
}

.loading, .error, .no-data {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 12px;
}

.error {
  color: #e74c3c;
}

.start-riding-btn {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.75rem 2rem;
  background: #667eea;
  color: white;
  text-decoration: none;
  border-radius: 25px;
  transition: all 0.3s;
}

.start-riding-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.rides-timeline {
  margin-bottom: 2rem;
}

.date-group {
  margin-bottom: 2rem;
}

.date-header {
  color: #667eea;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.rides-in-date {
  display: grid;
  gap: 1rem;
}

.ride-item {
  position: relative;
}

.ride-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.ride-time {
  color: #666;
  font-size: 0.9rem;
}

.delete-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.3s;
}

.delete-btn:hover {
  opacity: 1;
}

.export-section {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.export-btn, .clear-btn {
  flex: 1;
  padding: 1rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.export-btn {
  background: #667eea;
  color: white;
}

.clear-btn {
  background: #e74c3c;
  color: white;
}

.export-btn:hover, .clear-btn:hover {
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
