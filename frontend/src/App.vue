<template>
  
  <div id="app" class="min-h-screen flex flex-col">
    <nav class="bg-[#5AB4C5] h-[10vh] relative z-20"></nav>
    <router-view :class="showFooter ? 'h-[80vh]' : 'h-[90vh]'" class="relative"/>
    <Footer 
      v-if="showFooter"
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
  }
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
    router.push('/ride')
  } else if (route.path === '/ride') {
    router.push('/ride/pause')
  }
}

const handleContinue = () => {
  router.push('/ride')
}

const handleFinish = () => {
  router.push('/ride/finish')
}
</script>
