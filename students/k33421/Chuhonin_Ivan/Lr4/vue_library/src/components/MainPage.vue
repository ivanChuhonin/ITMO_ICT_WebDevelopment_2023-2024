<template>
  <div class="main-page">
    <h2 class="main-title">Выберите книгу для чтения!</h2>
    <ul>
      <li v-for="{ id, book_name, author, area, publishing_house } in books">
        <router-link :to="'operation/' + id">{{ book_name }}</router-link><br>
        <span class="author">{{ author }}</span><br>
        <span class="message">{{ area }}</span><br>
        <span class="message">{{ publishing_house }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      books: []
    };
  },
  mounted() {
    // Проверяем наличие токена перед загрузкой информации о пользователе
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      // Если токен отсутствует, перенаправляем на страницу авторизации
      this.$router.push({name: 'Auth'});
      return;
    }

    // Отправляем GET-запрос для получения информации о пользователе
    axios.get('http://127.0.0.1:8000/books/', {
      headers: {
        Authorization: `Token ${accessToken}`,
      },
    })
        .then(response => {
          this.books = response.data;
        })
        .catch(error => {
          console.error('Error fetching user information:', error);
        });
  }
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
