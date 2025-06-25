<template>
  <div class="min-h-screen bg-gray-950 text-white flex flex-col">
    <!-- Header -->
    <header class="flex items-center justify-between px-6 py-4 bg-gray-900 border-b border-gray-800">
      <h1 class="text-xl font-bold">🧠AI</h1>
      <div class="flex items-center gap-4">
        <span class="bg-green-600 hover:bg-green-700 px-3 py-1.5 rounded text-sm">👤 Account: {{ username }}</span>
        <NuxtLink to="/home" class="bg-blue-600 hover:bg-blue-700 px-3 py-1.5 rounded text-sm">⬅️ Меню</NuxtLink>
        <button @click="logout" class="bg-red-600 hover:bg-red-700 px-3 py-1.5 rounded text-sm">🚪 Выйти</button>
      </div>
    </header>

    <!-- Chat Messages -->
    <div ref="chatContainer" class="flex-1 p-6 overflow-y-auto space-y-6">
      <div
        v-for="(msg, index) in chatHistory"
        :key="index"
        class="space-y-2"
      >
        <div class="bg-gray-800 p-3 rounded">
          <p class="text-sm text-blue-400">Вы:</p>
          <p>{{ msg.user }}</p>
        </div>
        <div class="bg-gray-700 p-3 rounded">
          <p class="text-sm text-green-400">Бот:</p>
          <p>{{ msg.response }}</p>
        </div>
      </div>
    </div>

    <!-- Input -->
    <form @submit.prevent="sendMessage" class="flex gap-2 p-4 border-t border-gray-800 bg-gray-900">
      <input
        v-model="userText"
        type="text"
        placeholder="Введите сообщение..."
        class="flex-1 bg-gray-800 px-4 py-2 rounded text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button type="submit" class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded">
        Отправить
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { apiFetch } from '@/utils/api'

const userText = ref('')
const chatHistory = ref<{ user: string; response: string }[]>([])
const username = ref('Гость')
const chatContainer = ref<HTMLElement | null>(null)

onMounted(() => {
  const token = localStorage.getItem('access_token')
  const storedUsername = localStorage.getItem('username')

  if (!token) {
    return navigateTo('/auth/login')
  }

  // Лог для отладки
  console.log('Username from localStorage:', storedUsername)

  if (storedUsername && storedUsername !== 'undefined' && storedUsername.trim() !== '') {
    username.value = storedUsername
  } else {
    username.value = 'Unknown User'
  }
})

// Прокрутка вниз после отправки
function scrollToBottom() {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

// Отправка запроса в чат
async function sendMessage() {
  if (!userText.value.trim()) return

  try {
    const token = localStorage.getItem('access_token')
    if (!token) return navigateTo('/auth/login')

    const res = await apiFetch('/chat/chat', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: userText.value })
    })

    chatHistory.value.push({
      user: userText.value,
      response: res?.response || '⚠️ Нет ответа от модели'
    })

    userText.value = ''
    scrollToBottom()
  } catch (err) {
    alert('🚫 Ошибка при отправке запроса')
    console.error(err)
  }
}

// Выход из чата
function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('username')
  navigateTo('/login')
}
</script>


