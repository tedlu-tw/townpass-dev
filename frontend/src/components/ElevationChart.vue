<template>
  <div class="elevation-chart">
    <div class="chart-header">
      <h3>⛰️ 坡度變化圖</h3>
      <div class="chart-stats">
        <span>最高: {{ maxElevation }}m</span>
        <span>最低: {{ minElevation }}m</span>
        <span>總爬升: {{ totalClimb }}m</span>
      </div>
    </div>
    <div ref="chartContainer" class="chart-container">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  }
})

const chartCanvas = ref(null)
const chartContainer = ref(null)

const maxElevation = computed(() => {
  if (!props.data.length) return 0
  return Math.max(...props.data.map(d => d.elevation)).toFixed(0)
})

const minElevation = computed(() => {
  if (!props.data.length) return 0
  return Math.min(...props.data.map(d => d.elevation)).toFixed(0)
})

const totalClimb = computed(() => {
  if (!props.data.length) return 0
  let climb = 0
  for (let i = 1; i < props.data.length; i++) {
    const diff = props.data[i].elevation - props.data[i - 1].elevation
    if (diff > 0) climb += diff
  }
  return climb.toFixed(0)
})

const drawChart = () => {
  if (!chartCanvas.value || !props.data.length) return

  const canvas = chartCanvas.value
  const ctx = canvas.getContext('2d')
  const container = chartContainer.value

  // Set canvas size
  canvas.width = container.clientWidth
  canvas.height = container.clientHeight

  const padding = 40
  const width = canvas.width - padding * 2
  const height = canvas.height - padding * 2

  // Clear canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  // Calculate scales
  const maxElev = Math.max(...props.data.map(d => d.elevation))
  const minElev = Math.min(...props.data.map(d => d.elevation))
  const elevRange = maxElev - minElev || 1

  // Draw grid
  ctx.strokeStyle = '#e0e0e0'
  ctx.lineWidth = 1
  for (let i = 0; i <= 5; i++) {
    const y = padding + (height / 5) * i
    ctx.beginPath()
    ctx.moveTo(padding, y)
    ctx.lineTo(padding + width, y)
    ctx.stroke()
  }

  // Draw elevation line
  ctx.strokeStyle = '#667eea'
  ctx.lineWidth = 3
  ctx.beginPath()

  props.data.forEach((point, index) => {
    const x = padding + (width / (props.data.length - 1)) * index
    const y = padding + height - ((point.elevation - minElev) / elevRange) * height

    if (index === 0) {
      ctx.moveTo(x, y)
    } else {
      ctx.lineTo(x, y)
    }
  })

  ctx.stroke()

  // Fill area under curve
  ctx.lineTo(padding + width, padding + height)
  ctx.lineTo(padding, padding + height)
  ctx.closePath()
  ctx.fillStyle = 'rgba(102, 126, 234, 0.1)'
  ctx.fill()

  // Draw axes labels
  ctx.fillStyle = '#666'
  ctx.font = '12px sans-serif'
  ctx.textAlign = 'right'

  // Y-axis labels
  for (let i = 0; i <= 5; i++) {
    const y = padding + (height / 5) * i
    const value = (maxElev - (elevRange / 5) * i).toFixed(0)
    ctx.fillText(value + 'm', padding - 10, y + 4)
  }
}

watch(() => props.data, () => {
  drawChart()
}, { deep: true })

onMounted(() => {
  drawChart()
  window.addEventListener('resize', drawChart)
})
</script>

<style scoped>
.elevation-chart {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.chart-header h3 {
  margin: 0;
  color: #333;
}

.chart-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: #666;
}

.chart-container {
  width: 100%;
  height: 300px;
  position: relative;
}

canvas {
  width: 100%;
  height: 100%;
}
</style>
