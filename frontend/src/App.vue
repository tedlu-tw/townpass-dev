<template>
  
  <div id="app" class="min-h-screen flex flex-col">
    <nav class="bg-[#5AB4C5] h-[10vh] relative z-20"></nav>
    <router-view class="h-[80vh] relative"/>
    <Footer 
      class="h-[10vh] relative z-20" 
      :button-text="footerButtonText" 
      :show-double-buttons="showDoubleButtons"
      @click="handleFooterClick" 
      @continue="handleContinue"
      @finish="handleFinish"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Footer from './components/Footer.vue'

const route = useRoute()
const router = useRouter()
const footerButtonText = ref('開始騎行')
const showDoubleButtons = ref(false)

watch(() => route.path, (newPath) => {
  if (newPath === '/ride') {
    footerButtonText.value = '暫停騎行'
    showDoubleButtons.value = false
  } else if (newPath === '/ride/pause') {
    showDoubleButtons.value = true
  } else {
    footerButtonText.value = '開始騎行'
    showDoubleButtons.value = false
  }
}, { immediate: true })

const handleFooterClick = () => {
  if (route.path === '/' || route.path === '/home') {
    // HomeView: 開始騎行 -> 切換到 RideView
    router.push('/ride')
  } else if (route.path === '/ride') {
    // RideView: 暫停騎行 -> 切換到 RidePauseView
    router.push('/ride/pause')
  }
}

const handleContinue = () => {
  // 繼續騎行 -> 返回 RideView
  router.push('/ride')
}

const handleFinish = () => {
  // 結束騎行 -> 切換到 RideFinishView
  router.push('/ride/finish')
}
</script>
