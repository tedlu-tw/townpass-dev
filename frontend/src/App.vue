<template>
  <div id="app" class="min-h-screen flex flex-col">
    <Navbar />

    <main class="flex-1">
      <div class="w-full max-w-[1200px] mx-auto px-4 md:px-5">
        <router-view />
      </div>
    </main>

    <Footer class="py-[10%]"/>
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
</script>

<!-- Styles moved to global Tailwind setup (use `src/assets/main.css` with Tailwind directives) -->
