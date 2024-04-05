<script>
import axios from 'axios';

export default {
  data() {
    return {
      halls: [],
      hall: '1',
      operation: {
        id_book: 0,
        id_book_copy: 0,
        id_library_card: 0,
        id_hall: NaN,
        date_from: Date.now()
      }
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
    axios.get('http://127.0.0.1:8000/halls/', {
      headers: {
        Authorization: `Token ${accessToken}`,
      },
    })
        .then(response => {
          this.halls = response.data;
        })
        .catch(error => {
          console.error('Error fetching user information:', error);
        });
  },
  methods: {
      async make() {
        try {
          // Проверяем наличие токена перед загрузкой информации о пользователе
          const accessToken = localStorage.getItem('access_token');
          if (!accessToken) {
            // Если токен отсутствует, перенаправляем на страницу авторизации
            this.$router.push({name: 'Auth'});
            return;
          }
          // Отправляем запрос на регистрацию
          const response = await axios.post('http://127.0.0.1:8000/new_operation/', {
            username: this.newUsername,
            email: this.newEmail,
            password: this.newPassword,
          }, {
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
              Authorization: `Token ${accessToken}`,
            }
          });

          // Перенаправляем на страницу авторизации
          this.$router.push({ name: 'MainPage' }).catch(() => {}); // Обрабатываем возможные ошибки
        } catch (error) {
          // Выводим сообщение об ошибке (можно изменить)
          alert('Registration failed. Please try again.');
          console.error(error);
        }
      },
  }
};
</script>


<template>
  <div>
    {{ $route.params.id }}
  </div>
  <h2>Залы:</h2>
  <div v-if="halls.length">
    <div v-for="item of halls">
      <input type="radio" :id="'hall_' + item.id" :value="item.id" v-model="hall">
      <label :for="item.id">{{ item.name }}</label>
      <br>
    </div>
  </div>
  <h2>Registration</h2>
    <form @submit.prevent="make">
      <label for="newUsername">Username:</label>
      <input v-model="newUsername" type="text" id="newUsername" required />

      <input v-model="newPassword" type="password" id="newPassword" required />

      <button type="submit">Register</button>
    </form>
</template>

<style scoped>

</style>