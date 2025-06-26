<template>
  <div class="min-h-screen bg-gray-950 text-white flex flex-col">
    <!-- Header -->
    <header class="flex items-center justify-between px-6 py-4 bg-gray-900 border-b border-gray-800">
      <div>
        <h1 class="text-xl font-bold">🧠AI</h1>
        <p v-if="currentChatName" class="text-sm text-gray-400">Чат: {{ currentChatName }}</p>
        <p v-else class="text-sm text-gray-400">Чат не выбран</p>
      </div>
      <div class="flex items-center gap-4">
        <span class="bg-green-600 hover:bg-green-700 px-3 py-1.5 rounded text-sm">👤 Account: {{ username }}</span>
        <NuxtLink to="/" class="bg-blue-600 hover:bg-blue-700 px-3 py-1.5 rounded text-sm">⬅️ Меню</NuxtLink>
        <button @click="logout" class="bg-red-600 hover:bg-red-700 px-3 py-1.5 rounded text-sm">🚪 Выйти</button>
      </div>
    </header>

    <!-- Chat Messages -->
    <div ref="chatContainer" class="flex-1 p-6 overflow-y-auto space-y-6">
      <div v-if="isLoading" class="text-center">
        <p>Загрузка сообщений...</p>
      </div>
      <div v-else-if="chatHistory.length === 0" class="text-center text-gray-400">
        <p>Нет сообщений в этом чате.</p>
      </div>
      <div v-else v-for="(msg, index) in chatHistory" :key="index" class="space-y-2">
        <div class="bg-gray-800 p-3 rounded">
          <p class="text-sm text-blue-400">Вы:</p>
          <p>{{ msg.request_text }}</p>
        </div>
        <div class="bg-gray-700 p-3 rounded">
          <p class="text-sm text-green-400">Бот:</p>
          <p>{{ msg.response_text }}</p>
        </div>
        <p class="text-xs text-gray-500">Время: {{ new Date(msg.timestamp).toLocaleString() }} (Задержка: {{ msg.latency_ms }}ms)</p>
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
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiFetch } from '@/utils/api'

const userText = ref('')
const chatHistory = ref<any[]>([])
const username = ref('Гость')
const chatContainer = ref<HTMLElement | null>(null)
const currentChatName = ref<string | null>(null)
const isLoading = ref(false)
const route = useRoute()
const router = useRouter()

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  const storedUsername = localStorage.getItem('username')

  if (!token) {
    return navigateTo('/auth/login')
  }

  console.log('Username from localStorage:', storedUsername)
  console.log('Token:', token)

  if (storedUsername && storedUsername !== 'undefined' && storedUsername.trim() !== '') {
    username.value = storedUsername
  } else {
    username.value = 'Unknown User'
  }

  // Загружаем данные чата только если есть chat_id
  if (route.params.id) {
    await fetchChatData(route.params.id as string)
  } else {
    currentChatName.value = null // Не создаем новый чат автоматически
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

// Загрузка данных чата (история сообщений и название)
async function fetchChatData(chatId: string) {
  isLoading.value = true
  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      await navigateTo('/auth/login')
      return
    }

    // Загружаем историю сообщений
    const messagesRes = await apiFetch(`/chat/${chatId}/messages`, {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` }
    })
    chatHistory.value = messagesRes || []

    // Загружаем название чата
    const chatRes = await apiFetch(`/chat/${chatId}`, {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` }
    })
    currentChatName.value = chatRes.title || `Чат #${chatId}`
  } catch (err) {
    console.error('Не удалось загрузить данные чата:', err)
    chatHistory.value = []
    currentChatName.value = `Чат #${chatId}`
    alert('Не удалось загрузить историю чата')
  } finally {
    isLoading.value = false
  }
}

// Сохранение данных чата перед выходом
async function saveChatData() {
  if (!route.params.id || chatHistory.value.length === 0) return
  try {
    const token = localStorage.getItem('access_token')
    if (!token) return

    // Отправляем историю на сервер
    await apiFetch(`/chat/${route.params.id}/save`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        messages: chatHistory.value
      })
    })
    console.log('Чат сохранен:', route.params.id)
  } catch (err) {
    console.error('Ошибка сохранения чата:', err)
  }
}

// Отправка запроса в чат
async function sendMessage() {
  if (!userText.value.trim()) return

  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      await navigateTo('/auth/login')
      return
    }

    console.log('Отправка запроса:', {
      message: userText.value,
      chat_id: route.params.id ? parseInt(route.params.id as string) : null
    })

    const res = await fetch('/chat', { // Изменен с /chat/chat на /chat
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: userText.value,
        chat_id: route.params.id ? parseInt(route.params.id as string) : null
      })
    })

    console.log('Ответ от сервера:', res.status, res.statusText)

    if (res.ok) {
      const contentType = res.headers.get('content-type')
      let responseData = null
      if (contentType && contentType.includes('application/json')) {
        responseData = await res.json()
      } else {
        console.warn('Ответ не содержит JSON или пустой:', await res.text())
        responseData = { chat_id: route.params.id ? parseInt(route.params.id as string) : null }
      }

      if (responseData) {
        // Проверка наличия всех полей
        const newMessage = {
          request_text: responseData.request_text || userText.value,
          response_text: responseData.response_text || 'Нет ответа от сервера',
          timestamp: responseData.timestamp || new Date().toISOString(),
          latency_ms: responseData.latency_ms || 0,
          chat_id: responseData.chat_id
        }
        chatHistory.value.push(newMessage)

        if (!route.params.id && responseData.chat_id) {
          currentChatName.value = `Чат #${responseData.chat_id}`
          await router.push(`/chat/${responseData.chat_id}`)
          await fetchChatData(responseData.chat_id.toString())
        }
      } else {
        if (route.params.id) {
          await fetchChatData(route.params.id as string)
        }
      }

      userText.value = ''
      scrollToBottom()
    } else {
      const errorText = await res.text().catch(() => 'Неизвестная ошибка')
      throw new Error(`HTTP error! Status: ${res.status}, Detail: ${errorText}`)
    }
  } catch (err) {
    console.error('Ошибка отправки сообщения:', err)
    alert(`🚫 Ошибка при отправке запроса: ${err.message || 'Неизвестная ошибка'}`)
    if (err.message.includes('401')) {
      await navigateTo('/auth/login')
    } else if (err.message.includes('404')) {
      alert('Эндпоинт не найден. Проверьте настройки сервера.')
    } else if (err.message.includes('500')) {
      alert('Ошибка на сервере. Попробуйте позже.')
    }
  }
}

// Выход из чата
function logout() {
  saveChatData()
  localStorage.removeItem('access_token')
  localStorage.removeItem('username')
  navigateTo('/login')
}

// Сохраняем данные перед выходом из компонента
onBeforeUnmount(() => {
  saveChatData()
})
</script>
