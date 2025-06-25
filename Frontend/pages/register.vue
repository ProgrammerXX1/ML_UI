<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-black to-gray-950 text-white">
    <div class="w-full max-w-md bg-gray-900 rounded-xl shadow-2xl p-8 border border-gray-800">
      <h2 class="text-3xl font-bold text-center text-white mb-6">Создать аккаунт 🚀</h2>

      <form @submit.prevent="register" class="space-y-4">
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
          📩 Зарегистрироваться
        </button>

        <!-- Link to login -->
        <p class="text-center text-sm text-gray-400 mt-4">
          Уже есть аккаунт?
          <NuxtLink to="/login" class="text-blue-400 hover:underline">Войти</NuxtLink>
        </p>
      </form>
    </div>
  </div>
</template>


<script setup lang="ts">
const username = ref('')
const password = ref('')

async function register() {
  try {
    const res = await fetch('http://127.0.0.1:8000/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
        is_api_user: false,
      }),
    })

    if (!res.ok) {
      throw new Error('Registration failed')
    }

    const data = await res.json()
    localStorage.setItem('access_token', data.access_token)
    navigateTo('/home')
  } catch (err) {
    alert('Registration failed')
    console.error(err)
  }
}
</script>
