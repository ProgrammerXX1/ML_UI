<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-black to-gray-950 text-white">
    <div class="w-full max-w-md bg-gray-900 rounded-xl shadow-2xl p-8 border border-gray-800">
      <h2 class="text-3xl font-bold text-center text-white mb-6">Вход в систему 👤</h2>

      <form @submit.prevent="login" class="space-y-4">
        <!-- Username -->
        <div>
          <label class="block mb-1 text-sm font-medium text-gray-300">Имя пользователя</label>
          <input
            v-model="username"
            type="text"
            placeholder="your_username"
            required
            class="w-full px-4 py-2 rounded-md bg-gray-800 text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-600"
          />
        </div>

        <!-- Password -->
        <div>
          <label class="block mb-1 text-sm font-medium text-gray-300">Пароль</label>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            required
            class="w-full px-4 py-2 rounded-md bg-gray-800 text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-600"
          />
        </div>

        <!-- Submit -->
        <button
          type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 transition text-white font-semibold py-2 rounded-md"
        >
          🔐 Войти
        </button>

        <!-- Link to register -->
        <p class="text-center text-sm text-gray-400 mt-4">
          Ещё нет аккаунта?
          <NuxtLink to="/register" class="text-blue-400 hover:underline">Зарегистрироваться</NuxtLink>
        </p>
      </form>
    </div>
  </div>
</template>


<script setup lang="ts">

import { ref } from 'vue'


const username = ref('')
const password = ref('')

const login = async () => {
  try {
    const formData = new URLSearchParams()
    formData.append('username', username.value)
    formData.append('password', password.value)

    const res = await fetch('http://127.0.0.1:8000/auth/login', {
      method: 'POST',
      body: formData,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })

    if (!res.ok) {
      throw new Error(`Ошибка входа: ${res.status}`)
    }

    const data = await res.json()

    const accessToken = data.access_token
    const returnedUsername = data.username

    if (accessToken) {
      localStorage.setItem('access_token', accessToken)
      localStorage.setItem('username', returnedUsername ?? 'Unknown')
      navigateTo('/')
    } else {
      alert('Ошибка: токен не получен')
    }
  } catch (err) {
    console.error('Ошибка входа:', err)
    alert('Неверные данные для входа')
  }
}


</script>

