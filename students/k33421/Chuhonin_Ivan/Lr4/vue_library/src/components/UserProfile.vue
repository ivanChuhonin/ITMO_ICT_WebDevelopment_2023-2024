<template>
    <div>
      <h1>User Information</h1>
      <div v-if="user">
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>ID:</strong> {{ user.id }}</p>
        <p><strong>Username:</strong> {{ user.username }}</p>
        <p><br><strong>Edit main profile:</strong> </p>
      </div>
      <div v-else>
        <p>Loading...</p>
      </div>
  
      <!-- Добавим кнопку для перехода на главную страницу -->
      <router-link to="/MainPage" class="back-button">
        Back to Main Page
      </router-link>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        user: null,
        reader: null
      };
    },
    mounted() {
      // Проверяем наличие токена перед загрузкой информации о пользователе
      const accessToken = localStorage.getItem('access_token');
      if (!accessToken) {
        // Если токен отсутствует, перенаправляем на страницу авторизации
        this.$router.push({ name: 'Auth' });
        return;
      }
  
      // Отправляем GET-запрос для получения информации о пользователе
      axios.get('http://127.0.0.1:8000/me/', {
        headers: {
          Authorization: `Token ${accessToken}`,
        },
      })
        .then(response => {
          this.user = response.data.user;
        })
        .catch(error => {
          console.error('Error fetching user information:', error);
        });
    },
  };
  </script>
  
  <style scoped>
  div {
  margin: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}
h1 {
  color: #333;
  font-size: 24px;
  margin-bottom: 10px;
}
p {
  margin-bottom: 10px;
}

strong {
  font-weight: bold;
}
.back-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  text-decoration: none;
  border-radius: 5px;
}

.back-button:hover {
  background-color: #0056b3;
}

  </style>
  