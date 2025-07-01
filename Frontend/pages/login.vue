```vue
<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br text-white relative overflow-hidden">
    <div class="w-full max-w-md bg-gray-900/30 rounded-xl shadow-2xl p-8 border border-indigo-700/50 backdrop-blur-lg relative animate-fade-in" :class="{ 'form-processing': loading }">
      <!-- Логотип и заголовок -->
      <div class="flex justify-center mb-6">
        <div class="flex items-center gap-2">
          <svg class="h-12 w-12 animate-neural-network" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <g class="nodes">
              <circle cx="50" cy="50" r="12" fill="none" stroke="#a5b4fc" stroke-width="3" class="node node-center" />
              <circle cx="30" cy="30" r="8" fill="none" stroke="#c084fc" stroke-width="2" class="node node-top-left" />
              <circle cx="70" cy="30" r="8" fill="none" stroke="#c084fc" stroke-width="2" class="node node-top-right" />
              <circle cx="30" cy="70" r="8" fill="none" stroke="#c084fc" stroke-width="2" class="node node-bottom-left" />
              <circle cx="70" cy="70" r="8" fill="none" stroke="#c084fc" stroke-width="2" class="node node-bottom-right" />
            </g>
            <g class="connections">
              <path d="M50 50 L30 30" stroke="#60a5fa" stroke-width="1.5" class="connection" />
              <path d="M50 50 L70 30" stroke="#60a5fa" stroke-width="1.5" class="connection" />
              <path d="M50 50 L30 70" stroke="#60a5fa" stroke-width="1.5" class="connection" />
              <path d="M50 50 L70 70" stroke="#60a5fa" stroke-width="1.5" class="connection" />
            </g>
          </svg>
          <h2 class="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent animate-flicker">NeuralNet AI</h2>
        </div>
      </div>
      <!-- Анимация загрузки -->
      <div v-if="loading" class="absolute inset-0 flex items-center justify-center pointer-events-none">
        <div class="processing-ring"></div>
      </div>
      <!-- Форма входа -->
      <form @submit.prevent="login" class="space-y-4">
        <div>
          <label class="block mb-1 text-sm font-medium text-gray-300 animate-glow-text">Имя пользователя</label>
          <input
            v-model="username"
            type="text"
            placeholder="your_username"
            required
            class="w-full px-4 py-2 rounded-md bg-gray-800/20 text-white border border-indigo-700/50 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all duration-300 hover:bg-gray-700/20 hover:scale-[1.02] shadow-glow"
            :disabled="loading"
          />
        </div>
        <div>
          <label class="block mb-1 text-sm font-medium text-gray-300 animate-glow-text">Пароль</label>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            required
            class="w-full px-4 py-2 rounded-md bg-gray-800/20 text-white border border-indigo-700/50 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all duration-300 hover:bg-gray-700/20 hover:scale-[1.02] shadow-glow"
            :disabled="loading"
          />
        </div>
        <p v-if="errorMessage" class="text-sm text-red-400 text-center animate-pulse">{{ errorMessage }}</p>
        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-semibold py-2 rounded-md disabled:opacity-50 shadow-lg hover:shadow-xl hover:scale-[1.05] transition-all duration-300"
        >
          {{ loading ? 'Вход...' : '🔐 Войти' }}
        </button>
        <p class="text-center text-sm text-gray-400 mt-4">
          Ещё нет аккаунта?
          <NuxtLink to="/register" class="text-blue-400 hover:text-purple-400 hover:underline animate-flicker transition-all duration-300">Зарегистрироваться</NuxtLink>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { navigateTo, useRuntimeConfig, useCookie } from '#app'
import { useUserStore } from '@/stores/user' // <- поправь путь!

const config = useRuntimeConfig()
const username = ref('')
const password = ref('')
const userStore = useUserStore()        // инициализируем стор
const cookieToken = useCookie('access_token') // вынесено вне login()

// При монтировании читаем из localStorage (если нужно, иначе стор сам должен читать)
onMounted(() => {
  const storedRole = localStorage.getItem('role')
  if (storedRole) userStore.role = storedRole  // обновляем стор
})

const login = async () => {
  try {
    const formData = new URLSearchParams()
    formData.append('username', username.value)
    formData.append('password', password.value)
    formData.append('grant_type', 'password')        // обязательно!
    formData.append('scope', '')                     // обязательно, даже если пусто
    formData.append('client_id', '')                 // обязательно, даже если пусто
    formData.append('client_secret', '')   

    const res = await fetch(`${config.public.apiUrl}/auth/login`, {
      method: 'POST',
      body: formData,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })

    const contentType = res.headers.get('content-type') || ''
    if (!res.ok) {
      if (!contentType.includes('application/json')) {
        throw new Error('Сервер вернул не JSON (возможно 404 или 500)')
      }
      const err = await res.json()
      throw new Error(err.detail || `Ошибка входа: ${res.status}`)
    }
    if (!contentType.includes('application/json')) {
      throw new Error('Некорректный формат ответа сервера')
    }

    const data = await res.json()
    const accessToken = data.access_token
    const returnedUsername = data.username
    const returnedRole = data.role  // ожидаем, что сервер возвращает роль

    if (accessToken) {
      localStorage.setItem('access_token', accessToken)
      localStorage.setItem('username', returnedUsername ?? 'Unknown')
      localStorage.setItem('role', returnedRole ?? 'user')  // сохраняем роль
      userStore.username = returnedUsername ?? 'Unknown'    // обновляем стор
      userStore.role = returnedRole ?? 'user'               // обновляем стор
      cookieToken.value = accessToken
      navigateTo('/chat')
    } else {
      alert('Ошибка: токен не получен')
    }
  } catch (err: any) {
    console.error('❌ Ошибка входа:', err)
    alert(err.message || 'Неверные данные для входа')
  }
}
</script>
```