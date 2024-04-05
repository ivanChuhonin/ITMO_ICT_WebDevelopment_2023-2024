<template>
  <!-- Добавим кнопку для перехода на главную страницу -->
  <router-link to="/MainPage" class="back-button">
    Back to Main Page
  </router-link>
  <div>
    <h1>User Information</h1>
    <div v-if="user">
      <p><strong>Email:</strong> {{ user.email }}</p>
      <p><strong>ID:</strong> {{ user.id }}</p>
      <p><strong>Username:</strong> {{ user.username }}</p>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
  <div class="userprofile-container">
    <h2>Reader Information</h2>
    <form @submit.prevent="setUserprofile">
      <label for="full_name">Full name:</label>
      <input v-model="reader.full_name" type="text" id="full_name" required/>

      <label for="address">Address:</label>
      <input v-model="reader.address" type="text" id="address" required/>

      <label for="passport">Passport:</label>
      <input v-model="reader.passport" type="text" id="passport" required/>

      <label for="birthdate">birthday:</label>
      <input v-model="reader.birthdate" type="date" id="birthdate" required/>

      <label for="is_academic">Academic status:</label>
      <input v-model="reader.is_academic" type="checkbox" id="is_academic" required/>

      <button type="submit">Save</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      user: null,
      reader: {
        full_name: '',
        address: '',
        passport: '',
        birthdate: '',
        is_academic: false,
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
    axios.get('http://127.0.0.1:8000/me/', {
      headers: {
        Authorization: `Token ${accessToken}`,
      },
    })
        .then(response => {
          this.user = response.data.user;
          this.reader = response.data.reader;
        })
        .catch(error => {
          console.error('Error fetching user information:', error);
        });
  },
  methods: {
    async setUserprofile() {
      const accessToken = localStorage.getItem('access_token');
      if (!accessToken) {
        // Если токен отсутствует, перенаправляем на страницу авторизации
        this.$router.push({name: 'Auth'});
        return;
      }

      try {
        const response = await axios.post(
            'http://127.0.0.1:8000/saveme/',
            {
              full_name: this.reader.full_name,
              address: this.reader.address,
              passport: this.reader.passport,
              birthdate: this.reader.birthdate,
              is_academic: this.reader.is_academic
            },
            {
              headers: {
                Authorization: `Token ${accessToken}`,
                'Content-Type': 'application/json',
                Accept: 'application/json',
              },
            }
        );

        alert('Profile successfully saved!');

      } catch (error) {
        console.error(error);

        if (error.response && error.response.status === 401) {
          this.$router.push({name: 'ErrorPage'});
        }
      }
    },
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

form {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 5px;
}

input {
  margin-bottom: 15px;
  padding: 10px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.userprofile-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.userprofile-container h2 {
  color: #333;
  font-size: 24px;
  margin-bottom: 10px;
}

.userprofile-container form {
  margin-top: 20px;
}

.userprofile-container label {
  display: block;
  margin-bottom: 5px;
}

.userprofile-container input {
  padding: 5px;
  margin-bottom: 10px;
  width: 100%;
}

.userprofile-container button {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
}

.userprofile-container button:hover {
  background-color: #0056b3;
}
</style>
  