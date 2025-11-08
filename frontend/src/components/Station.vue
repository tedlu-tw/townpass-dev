<template>
  <div class="station-card">
    <h3 class="station-name">{{ station?.name || '載入中...' }}</h3>
    <p class="station-address">{{ station?.address }}</p>
    
    <div class="station-stats">
      <div class="stat">
        <span class="label">可租</span>
        <span class="value bikes">{{ station?.availableBikes || 0 }}</span>
      </div>
      <div class="stat">
        <span class="label">可還</span>
        <span class="value spaces">{{ station?.availableSpaces || 0 }}</span>
      </div>
      <div class="stat">
        <span class="label">總數</span>
        <span class="value">{{ station?.totalSlots || 0 }}</span>
      </div>
    </div>

    <div class="station-distance" v-if="station?.distance">
      <span>📍 距離: {{ station.distance }} 公尺</span>
    </div>

    <button v-if="showAction" @click="$emit('select-station', station)" class="action-btn">
      選擇此站點
    </button>
  </div>
</template>

<script setup>
defineProps({
  station: {
    type: Object,
    default: null
  },
  showAction: {
    type: Boolean,
    default: false
  }
})

defineEmits(['select-station'])
</script>

<style scoped>
.station-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: all 0.3s;
}

.station-card:hover {
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.station-name {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 1.1rem;
}

.station-address {
  color: #666;
  font-size: 0.9rem;
  margin: 0 0 1rem 0;
}

.station-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.stat {
  flex: 1;
  text-align: center;
}

.stat .label {
  display: block;
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.stat .value {
  display: block;
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.stat .value.bikes {
  color: #27ae60;
}

.stat .value.spaces {
  color: #3498db;
}

.station-distance {
  text-align: center;
  color: #667eea;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.action-btn {
  width: 100%;
  padding: 0.75rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

.action-btn:hover {
  background: #5568d3;
}
</style>
