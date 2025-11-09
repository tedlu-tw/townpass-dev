<template>

  <div id="app" class="min-h-screen flex flex-col">
    <!-- <nav class="bg-[#5AB4C5] h-[10vh] relative z-20"></nav> -->
    <router-view :class="showFooter ? 'h-[90vh]' : 'h-[100vh]'" class="relative" />

    <!-- 歷史記錄按鈕 - 只在顯示「開始騎行」時顯示 -->
    <button v-if="footerButtonText === '開始騎行'" @click="goToHistory"
      class="fixed bottom-24 right-5 w-14 h-14 bg-[#5AB4C5] rounded-full shadow-lg flex items-center justify-center hover:bg-[#4a9fb0] transition-colors z-30">
      <svg width="34" height="34" viewBox="0 0 34 34" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M17 31.1667C13.3403 31.1667 10.1646 29.9507 7.47292 27.5188C4.78126 25.0868 3.25834 22.0528 2.90417 18.4167H5.77292C6.12709 21.2737 7.37258 23.6407 9.50938 25.5177C11.6462 27.3948 14.1431 28.3334 17 28.3334C20.1639 28.3334 22.8438 27.2355 25.0396 25.0396C27.2354 22.8438 28.3333 20.1639 28.3333 17C28.3333 13.8362 27.2354 11.1563 25.0396 8.96046C22.8438 6.76462 20.1639 5.66671 17 5.66671C14.9695 5.66671 13.0865 6.16844 11.351 7.17192C9.61563 8.17539 8.24029 9.56254 7.22501 11.3334H11.3333V14.1667H3.11667C3.8014 10.8612 5.44237 8.14587 8.03959 6.02087C10.6368 3.89587 13.6236 2.83337 17 2.83337C18.9597 2.83337 20.8014 3.20525 22.525 3.949C24.2486 4.69275 25.7479 5.70212 27.0229 6.97712C28.2979 8.25212 29.3073 9.75143 30.0511 11.475C30.7948 13.1987 31.1667 15.0403 31.1667 17C31.1667 18.9598 30.7948 20.8014 30.0511 22.525C29.3073 24.2487 28.2979 25.748 27.0229 27.023C25.7479 28.298 24.2486 29.3073 22.525 30.0511C20.8014 30.7948 18.9597 31.1667 17 31.1667ZM20.9667 22.95L15.5833 17.5667V9.91671H18.4167V16.4334L22.95 20.9667L20.9667 22.95Z"
          fill="white" />
      </svg>
    </button>

    <Footer v-if="showFooter" class="h-[10vh] relative z-20" :button-text="footerButtonText"
      :show-double-buttons="showDoubleButtons" @click="handleFooterClick" @continue="handleContinue"
      @finish="handleFinish" />
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Footer from './components/Footer.vue'

const route = useRoute()
const router = useRouter()

// Footer 配置映射表
const footerConfig = {
  '/home': {
    show: true,
    buttonText: '開始騎行',
    doubleButtons: false
  },
  '/': {
    show: true,
    buttonText: '開始騎行',
    doubleButtons: false
  },
  '/ride': {
    show: true,
    buttonText: '暫停騎行',
    doubleButtons: false
  },
  '/ride/pause': {
    show: true,
    buttonText: '',
    doubleButtons: true
  },
  '/ride/finish': {
    show: false,
    buttonText: '',
    doubleButtons: false
  },
  '/history': {
    show: false,
    buttonText: '',
    doubleButtons: false
  },
}

// 當前 Footer 配置
const currentConfig = ref(footerConfig['/home'])

// 使用 computed 來獲取配置值
const showFooter = computed(() => currentConfig.value.show)
const footerButtonText = computed(() => currentConfig.value.buttonText)
const showDoubleButtons = computed(() => currentConfig.value.doubleButtons)

// 監聽路由變化更新配置
watch(() => route.path, (newPath) => {
  currentConfig.value = footerConfig[newPath] || footerConfig['/home']
}, { immediate: true })

const handleFooterClick = () => {
  if (route.path === '/' || route.path === '/home') {
    router.push('/ride').then(() => {
      window.location.reload();
    })
  } else if (route.path === '/ride') {
    router.push('/ride/pause').then(() => {
      window.location.reload();
    })
  }
}

const handleContinue = () => {
  router.push('/ride').then(() => {
    window.location.reload();
  })
}

const handleFinish = () => {
  router.push('/ride/finish')
}

const goToHistory = () => {
  router.push('/history').then(() => {
    window.location.reload();
  })
}
</script>
