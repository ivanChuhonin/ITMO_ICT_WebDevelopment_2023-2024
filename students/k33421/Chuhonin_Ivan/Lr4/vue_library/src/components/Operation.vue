<script>
import axios from 'axios';
import {useRoute} from "vue-router";

export default {
  data() {
    return {
      book_name: '',
      halls: [],
      operation: {
        id_book: 0,
        id_hall: '1',
        date_from: null
      }
    };
  },
  mounted() {
    var date = new Date()
    var year = date.getFullYear()
    var month = date.getMonth() + 1
    month = month > 9 ? '' + month : '0' + month
    var day = date.getDate()
    day = day > 9 ? '' + day : '0' + day
    this.operation.date_from = year + '-' + month + '-' + day

    const route = useRoute()
    this.operation.id_book = route.params.id
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
    axios.get('http://127.0.0.1:8000/books/' + route.params.id + '/', {
      headers: {
        Authorization: `Token ${accessToken}`,
      },
    })
        .then(response => {
          this.book_name = response.data.book_name + ', ' + response.data.author;
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
          id_book: parseInt(this.operation.id_book),
          id_hall: parseInt(this.operation.id_hall),
          date_from: this.operation.date_from
        }, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            Authorization: `Token ${accessToken}`,
          }
        });

        // Перенаправляем на страницу авторизации
        this.$router.push({name: 'MainPage'}).catch(() => {
        });
      } catch (error) {
        // Выводим сообщение об ошибке
        alert('Operation failed. Please try again.');
        console.error(error);
      }
    },
  }
};
</script>


<template>
  <div class="operation-container">
  <h2>Getting of the book</h2>

  <h3>{{ this.book_name }}</h3>

  <h3>Halls:</h3>
  <div v-if="halls.length">
    <div v-for="item of halls">
      <input type="radio" :id="'hall_' + item.id" :value="item.id" v-model="operation.id_hall">
      <label :for="item.id">{{ item.name }}</label>
      <br>
    </div>
  </div>
  <form @submit.prevent="make">

    <label for="date_from">Date:</label><br>
    <input v-model="operation.date_from" type="date" id="date_from" required/><br>

    <button type="submit">Take book</button>
  </form>
  </div>
</template>

<style scoped>
.operation-container {
  width: 400%;
  max-width: 400px;
  margin: 0 auto;
  text-align: center;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 10px;
}

h3 {
  font-size: 18px;
  color: #555;
  margin-bottom: 5px;
}

label {
  font-weight: bold;
  color: #777;
}

input[type="radio"] {
  margin-right: 5px;
}

button {
  background-color: #007bff;
  color: #fff;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 30px;
}

button:hover {
  background-color: #0056b3;
}

form {
  margin-top: 20px;
}

input[type="text"],
input[type="email"],
input[type="password"],
textarea {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
  margin-bottom: 10px;
  box-sizing: border-box;
}

input[type="text"]:focus,
input[type="email"]:focus,
input[type="password"]:focus,
textarea:focus {
  border-color: #007bff;
  outline: none;
}
</style>