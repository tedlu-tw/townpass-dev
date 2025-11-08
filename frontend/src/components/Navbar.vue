<template>
  <nav class="navbar">
    <div class="container">
      <div class="navbar-brand">
        <h1>🏙️ TownPass</h1>
      </div>
      <div class="navbar-links">
        <router-link to="/home" class="nav-link">首頁</router-link>
        <router-link to="/stations" class="nav-link">站點地圖</router-link>
        <router-link to="/ride" class="nav-link">開始騎乘</router-link>
        <router-link to="/history" class="nav-link">騎乘紀錄</router-link>
        <router-link to="/map-demo" class="nav-link">地圖示範</router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
// Navbar component
</script>

<style scoped>
.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
}

.navbar-links {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.3s;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.2);
}

.nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.3);
}
</style>
