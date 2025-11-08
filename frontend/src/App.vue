<template>
  <div id="app">
    <Navbar />

    <main class="app-main">
      <div class="container">
        <router-view />
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-main {
  flex: 1;
  padding: 80px 0 40px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  width: 100%;
}

@media (max-width: 768px) {
  .app-main {
    padding: 70px 0 30px;
  }
  
  .container {
    padding: 0 15px;
  }
}
</style>
