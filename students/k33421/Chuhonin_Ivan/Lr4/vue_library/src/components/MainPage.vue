<template>
  <div class="main-page">
    <h1 class="main-title">Добро пожаловать на главную страницу!</h1>
    <router-link :to="{ name: 'Auth' }">
      <button class="main-button">Выйти</button>
    </router-link>
  </div>
</template>

<script>
export default {
  // Компонент для главной страницы
};
</script>

<style scoped>
.main-page {
  text-align: center;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.main-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.main-button {
  padding: 15px 20px;
  margin-bottom: 10px;
  font-size: 20px;
  border-radius: 30px;
  background-color: transparent;
  text-decoration: none;
  cursor: pointer;
  color: #333;
  transition: background-color 0.3s;
  margin: 10;
  border: 1px solid #3498db;
  width: 400px; /* Фиксированная ширина кнопки */
}

.main-button:hover {
  background-color: #3498db;
  color: #fff;
}
</style>
