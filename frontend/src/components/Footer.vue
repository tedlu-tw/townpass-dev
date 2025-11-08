<template>
  <footer class="footer">
    <div class="container">
      <p>© 2025 TownPass - 智慧城市騎乘服務平台</p>
      <div class="footer-links">
        <a href="#">關於我們</a>
        <a href="#">服務條款</a>
        <a href="#">隱私政策</a>
      </div>
    </div>
  </footer>
</template>

<script setup>
// Footer component
</script>

<style scoped>
.footer {
  background: #2c3e50;
  color: white;
  padding: 2rem 0;
  margin-top: auto;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  text-align: center;
}

.container p {
  margin: 0 0 1rem 0;
}

.footer-links {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
}

.footer-links a {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s;
}

.footer-links a:hover {
  color: white;
}
</style>
