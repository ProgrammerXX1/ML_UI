```vue
<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-950 via-indigo-950 to-purple-950 text-white relative overflow-hidden">
    <div class="w-full max-w-md bg-gray-900/30 rounded-xl shadow-2xl p-8 border border-indigo-700/50 backdrop-blur-lg relative animate-fade-in" :class="{ 'form-processing': loading }">
      <!-- Animated Logo -->
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
      <!-- Processing Animation -->
      <div v-if="loading" class="absolute inset-0 flex items-center justify-center pointer-events-none">
        <div class="processing-ring" />
      </div>
      <form @submit.prevent="login" class="space-y-4">
        <!-- Username -->
        <div>
          <label class="block mb-1 text-sm font-medium text-gray-300 animate-glow-text">Имя пользователя</label>
          <input
            v-model="username"
            type="text"
            placeholder="your_username"
            required
            class="w-full px-4 py-2 rounded-md bg-gray-800/20 text-white border border-indigo-700/50 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all duration-300 hover:bg-gray-700/20 hover:scale-[1.02] shadow-glow"
          />
        </div>
        <!-- Password -->
        <div>
          <label class="block mb-1 text-sm font-medium text-gray-300 animate-glow-text">Пароль</label>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            required
            class="w-full px-4 py-2 rounded-md bg-gray-800/20 text-white border border-indigo-700/50 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all duration-300 hover:bg-gray-700/20 hover:scale-[1.02] shadow-glow"
          />
        </div>
        <!-- Error message -->
        <p v-if="errorMessage" class="text-sm text-red-400 text-center animate-pulse">{{ errorMessage }}</p>
        <!-- Submit -->
        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 transition-all duration-300 text-white font-semibold py-2 rounded-md disabled:opacity-50 shadow-lg hover:shadow-xl hover:scale-[1.05]"
        >
          {{ loading ? 'Вход...' : '🔐 Войти' }}
        </button>
        <!-- Link to register -->
        <p class="text-center text-sm text-gray-400 mt-4">
          Ещё нет аккаунта?
          <NuxtLink to="/register" class="text-blue-400 hover:text-purple-400 hover:underline animate-flicker transition-all duration-300">Зарегистрироваться</NuxtLink>
        </p>
      </form>
    </div>
  </div>
</template>

<style scoped>
/* Neural network logo animation */
.animate-neural-network .nodes {
  animation: rotate 20s linear infinite;
}
.animate-neural-network .node {
  animation: pulse 2s infinite ease-in-out;
}
.animate-neural-network .node-top-left { animation-delay: 0s; }
.animate-neural-network .node-top-right { animation-delay: 0.2s; }
.animate-neural-network .node-bottom-left { animation-delay: 0.4s; }
.animate-neural-network .node-bottom-right { animation-delay: 0.6s; }
.animate-neural-network .node-center { animation-delay: 0.8s; }
.animate-neural-network .connection {
  animation: connect 2s infinite ease-in-out;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.7; }
  50% { transform: scale(1.2); opacity: 1; }
}

@keyframes connect {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Processing animation for form submission */
.processing-ring {
  width: 100%;
  height: 100%;
  border: 3px solid transparent;
  border-top-color: #60a5fa;
  border-right-color: #c084fc;
  border-radius: 50%;
  animation: spin 7s linear infinite; /* Matches 5-10s server response time */
  box-shadow: 0 0 15px rgba(96, 165, 250, 0.5);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Flicker animation for text */
.animate-flicker {
  animation: flicker 3s infinite ease-in-out;
}

@keyframes flicker {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}

/* Glow text animation for labels */
.animate-glow-text {
  animation: glow-text 2s infinite ease-in-out;
}

@keyframes glow-text {
  0%, 100% { text-shadow: 0 0 5px rgba(165, 180, 252, 0.5); }
  50% { text-shadow: 0 0 10px rgba(165, 180, 252, 0.8); }
}

/* Fade-in animation for form */
.animate-fade-in {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Glow effect for inputs and buttons */
.shadow-glow {
  box-shadow: 0 0 10px rgba(79, 70, 229, 0.3);
}

/* Form processing glow */
.form-processing {
  box-shadow: 0 0 20px rgba(96, 165, 250, 0.5);
}

/* Smooth transitions for interactive elements */
button, a, input {
  transition: all 0.3s ease;
}
</style>
```
<script setup lang="ts">
import { ref } from 'vue'
import { navigateTo, useRuntimeConfig, useCookie } from '#app'

const config = useRuntimeConfig()

const username = ref('')
const password = ref('')

const login = async () => {
  try {
    const formData = new URLSearchParams()
    formData.append('username', username.value)
    formData.append('password', password.value)

    const res = await fetch(`${config.public.apiUrl}/auth/login`, {
      method: 'POST',
      body: formData,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })

    if (!res.ok) throw new Error(`Ошибка входа: ${res.status}`)

    const data = await res.json()
    const accessToken = data.access_token
    const returnedUsername = data.username

    if (accessToken) {
      localStorage.setItem('access_token', accessToken)
      localStorage.setItem('username', returnedUsername ?? 'Unknown')
      useCookie('access_token').value = accessToken
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

