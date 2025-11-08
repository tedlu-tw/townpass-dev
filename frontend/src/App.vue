<template>
  
  <div id="app" class="min-h-screen flex flex-col">
    <nav class="bg-[#5AB4C5] h-[10vh]"></nav>
    <router-view class="h-[80vh]"/>
    <Footer class="h-[10vh]" />
  </div>
</template>

<script setup>
import Footer from './components/Footer.vue'
</script>

<!-- Styles moved to global Tailwind setup (use `src/assets/main.css` with Tailwind directives) -->
