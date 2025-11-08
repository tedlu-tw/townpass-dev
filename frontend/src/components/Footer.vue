<template>
  <footer class="absolute bg-white w-full flex flex-col justify-center px-5 drop-shadow-[0px_0px_5px_rgba(0,0,0,0.2)]">
      <!-- 單按鈕模式 -->
      <button v-if="!showDoubleButtons" @click="handleClick" class="py-3 rounded-[8px] bg-[#5AB4C5] text-white relative z-30">
        {{ buttonText }}
      </button>
      
      <!-- 雙按鈕模式（暫停狀態） -->
      <div v-else class="flex gap-3">
        <button @click="handleFinish" class="flex-1 py-3 rounded-[8px] bg-white border-2 border-[#5AB4C5] text-black relative z-30">
          結束騎行
        </button>
        <button @click="handleContinue" class="flex-1 py-3 rounded-[8px] bg-[#5AB4C5] text-white relative z-30">
          繼續騎行
        </button>
      </div>
  </footer>
</template>

<script setup>
defineProps({
  buttonText: {
    type: String,
    default: '開始騎行'
  },
  showDoubleButtons: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click', 'continue', 'finish'])

const handleClick = () => {
  emit('click')
}

const handleContinue = () => {
  emit('continue')
}

const handleFinish = () => {
  emit('finish')
}
</script>