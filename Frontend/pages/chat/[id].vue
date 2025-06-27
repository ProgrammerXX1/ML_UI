```vue
<template>
  <div class="h-screen flex flex-col bg-gradient-to-br from-gray-950 via-indigo-900 to-purple-900 text-white relative overflow-hidden">
    <!-- Background Neural Mesh -->
    <canvas ref="neuralMeshCanvas" class="absolute inset-0 z-0 pointer-events-none"></canvas>
    <!-- Fixed Header -->
    <header class="sticky top-0 z-20 bg-gray-900/95 border-b border-indigo-800 px-6 py-4 backdrop-blur-sm">
      <div class="flex items-center justify-between relative">
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-2">
            <svg class="h-8 w-8 animate-neural-network" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
              <g class="nodes">
                <circle cx="50" cy="50" r="10" fill="none" stroke="#a5b4fc" stroke-width="2" class="node node-center" />
                <circle cx="30" cy="30" r="8" fill="none" stroke="#c084fc" stroke-width="2" class="node node-top-left" />
                <circle cx="70" cy="30" r="8" fill="none" stroke="#c084fc" stroke-width="2" class="node node-top-right" />
                <circle cx="30" cy="70" r="8" fill="none" stroke="#c084fc" stroke-width="2" class="node node-bottom-left" />
                <circle cx="70" cy="70" r="8" fill="none" stroke="#c084fc" stroke-width="2" class="node node-bottom-right" />
              </g>
              <g class="connections">
                <path d="M50 50 L30 30" stroke="#60a5fa" stroke-width="1" class="connection" />
                <path d="M50 50 L70 30" stroke="#60a5fa" stroke-width="1" class="connection" />
                <path d="M50 50 L30 70" stroke="#60a5fa" stroke-width="1" class="connection" />
                <path d="M50 50 L70 70" stroke="#60a5fa" stroke-width="1" class="connection" />
              </g>
            </svg>
            <span class="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text textijklmnopqrst animate-flicker">NeuralNet AI</span>
          </div>
          <div v-if="isGenerating" class="absolute left-0 top-0 w-full h-full flex items-center justify-center pointer-events-none">
            <div class="processing-animation" />
          </div>
          <div v-if="isEditingName">
            <input
              v-model="editableName"
              @keydown.enter="saveChatName"
              @blur="saveChatName"
              class="text-sm text-white bg-gray-800/50 border border-indigo-700 rounded px-2 py-1 focus:ring-2 focus:ring-purple-500 transition-all duration-300 shadow-glow"
              autofocus
            />
          </div>
          <p
            v-else
            class="text-sm text-gray-300 cursor-pointer hover:underline hover:text-white transition-all duration-200"
            @dblclick="startEditingName"
          >
            Чат: {{ currentChatName || 'не выбран' }}
          </p>
        </div>
        <div class="flex items-center gap-4">
          <span class="bg-gradient-to-r from-green-600 to-teal-600 hover:from-green-500 hover:to-teal-500 px-3 py-1.5 rounded text-sm transition-all duration-300 shadow-glow">
            👤 {{ username }}
          </span>
          <NuxtLink to="/" class="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 px-3 py-1.5 rounded text-sm transition-all duration-300 shadow-glow">⬅️ Меню</NuxtLink>
          <button @click="logout" class="bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-500 hover:to-pink-500 px-3 py-1.5 rounded text-sm transition-all duration-300 shadow-glow">🚪 Выйти</button>
        </div>
      </div>
    </header>
    <!-- Scrollable Messages -->
    <div ref="chatContainer" class="flex-1 overflow-y-auto px-6 py-4 space-y-6">
      <div v-if="isLoading" class="text-center text-gray-300 animate-pulse">
        <p>Загрузка сообщений...</p>
      </div>
      <div
        v-else-if="chatHistory.length === 0"
        class="text-center text-gray-400"
      >
        <p>Нет сообщений в этом чате.</p>
      </div>
      <div
        v-else
        v-for="(msg, index) in chatHistory"
        :key="index"
        class="space-y-2 animate-fade-in"
      >
        <div class="bg-gray-800/50 p-3 rounded border border-indigo-800 transform hover:scale-[1.02] transition-transform duration-200 shadow-glow">
          <p class="text-sm text-blue-400">Вы:</p>
          <p>{{ msg.request_text }}</p>
        </div>
        <div class="bg-gray-700/50 p-3 rounded border border-indigo-800 transform hover:scale-[1.02] transition-transform duration-200 shadow-glow">
          <p class="text-sm text-green-400">Бот:</p>
          <p>{{ msg.response_text }}</p>
        </div>
        <p class="text-xs text-gray-500">
          Время: {{ new Date(msg.timestamp).toLocaleString() }} (Задержка: {{ msg.latency_ms }}ms)
        </p>
      </div>
      <div v-if="isGenerating" class="text-center text-blue-400 animate-pulse">🤖 Генерация ответа...</div>
    </div>
    <!-- Fixed Input -->
    <form
      @submit.prevent="sendMessage"
      class="sticky bottom-0 z-10 flex gap-2 p-4 bg-gray-900/95 border-t border-indigo-800 backdrop-blur-sm"
    >
      <input
        v-model="userText"
        :disabled="isGenerating"
        type="text"
        placeholder="Введите сообщение..."
        class="flex-1 bg-gray-800/50 px-4 py-2 rounded text-white border border-indigo-700 focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all duration-300 shadow-glow disabled:opacity-50 disabled:cursor-not-allowed"
      />
      <button
        type="submit"
        :disabled="isGenerating"
        class="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 px-4 py-2 rounded disabled:opacity-50 transition-all duration-300 shadow-glow"
      >
        {{ isGenerating ? '...' : 'Отправить' }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiFetch } from '~/utils/api'

const userText = ref('')
const chatHistory = ref<any[]>([])
const username = ref('Гость')
const chatContainer = ref<HTMLElement | null>(null)
const currentChatName = ref<string | null>(null)
const isLoading = ref(false)
const isEditingName = ref(false)
const editableName = ref('')
const isGenerating = ref(false)

const route = useRoute()
const router = useRouter()

// Neural Mesh Background Animation
const neuralMeshCanvas = ref(null)

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  const storedUsername = localStorage.getItem('username')

  if (!token) return navigateTo('/auth/login')

  username.value = storedUsername && storedUsername.trim() !== 'undefined'
    ? storedUsername
    : 'Unknown User'

  if (route.params.id) {
    await fetchChatData(route.params.id as string)
  }

  // Initialize canvas animation
  const canvas = neuralMeshCanvas.value
  if (!canvas) return

  const ctx = canvas.getContext('2d')
  canvas.width = window.innerWidth
  canvas.height = window.innerHeight

  const nodes = Array.from({ length: 30 }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    vx: Math.random() * 0.5 - 0.25,
    vy: Math.random() * 0.5 - 0.25,
    radius: Math.random() * 2 + 1,
    isHub: Math.random() < 0.1, // 10% chance to be a hub
    pulseTime: Math.random() * 5000
  }))

  function animateMesh() {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    const time = Date.now()

    nodes.forEach(node => {
      node.x += node.vx
      node.y += node.vy

      if (node.x < 0 || node.x > canvas.width) node.vx *= -1
      if (node.y < 0 || node.y > canvas.height) node.vy *= -1

      // Draw node
      ctx.fillStyle = node.isHub && Math.sin(time * 0.001 + node.pulseTime) > 0.5 ? 'rgba(165, 180, 252, 0.8)' : 'rgba(165, 180, 252, 0.5)'
      ctx.beginPath()
      ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2)
      ctx.fill()

      // Draw signal wave for hubs
      if (node.isHub && Math.sin(time * 0.001 + node.pulseTime) > 0.5) {
        ctx.strokeStyle = 'rgba(96, 165, 250, 0.3)'
        ctx.lineWidth = 1
        ctx.beginPath()
        ctx.arc(node.x, node.y, node.radius + (time % 5000) * 0.01, 0, Math.PI * 2)
        ctx.stroke()
      }

      // Draw connections
      ctx.strokeStyle = 'rgba(96, 165, 250, 0.2)'
      ctx.lineWidth = 0.5
      nodes.forEach(other => {
        const dx = node.x - other.x
        const dy = node.y - other.y
        const distance = Math.sqrt(dx * dx + dy * dy)
        if (distance < 100) {
          ctx.beginPath()
          ctx.moveTo(node.x, node.y)
          ctx.lineTo(other.x, other.y)
          ctx.stroke()
        }
      })
    })

    requestAnimationFrame(animateMesh)
  }

  animateMesh()

  const resize = () => {
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
    nodes.forEach(node => {
      node.x = Math.random() * canvas.width
      node.y = Math.random() * canvas.height
    })
  }
  window.addEventListener('resize', resize)

  onBeforeUnmount(() => {
    window.removeEventListener('resize', resize)
  })
})

// Прокрутка вниз
function scrollToBottom() {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

// Загрузка чата
async function fetchChatData(chatId: string) {
  isLoading.value = true
  try {
    const token = localStorage.getItem('access_token')
    if (!token) return

    const messagesRes = await apiFetch(`/chat/${chatId}/messages`, {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` }
    })
    chatHistory.value = messagesRes || []

    const chatRes = await apiFetch(`/chat/${chatId}`, {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` }
    })
    currentChatName.value = chatRes.title || `Чат #${chatId}`
  } catch (err) {
    console.error('Не удалось загрузить чат:', err)
    chatHistory.value = []
    currentChatName.value = `Чат #${chatId}`
    alert('Не удалось загрузить чат')
  } finally {
    isLoading.value = false
  }
}

// Сохранить чат
async function saveChatData() {
  if (!route.params.id || chatHistory.value.length === 0) return
  try {
    const token = localStorage.getItem('access_token')
    if (!token) return

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
    console.log('Чат сохранён')
  } catch (err) {
    console.error('Ошибка при сохранении:', err)
  }
}

// Отправка сообщения
async function sendMessage() {
  if (!userText.value.trim()) return

  try {
    const token = localStorage.getItem('access_token')
    if (!token) return navigateTo('/auth/login')

    const chatId = route.params.id ? parseInt(route.params.id as string) : null
    if (!chatId) {
      alert('Невозможно отправить: чат не выбран')
      return
    }

    isGenerating.value = true // <-- показать лоадер

    const res = await fetch(`http://:8000/chat/${chatId}/send`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: userText.value }),
    })

    if (res.ok) {
      const responseData = await res.json()
      const newMessage = {
        request_text: responseData.request_text || userText.value,
        response_text: responseData.response_text || 'Нет ответа от сервера',
        timestamp: responseData.timestamp || new Date().toISOString(),
        latency_ms: responseData.latency_ms || 0,
        chat_id: responseData.chat_id
      }
      chatHistory.value.push(newMessage)
      userText.value = ''
      scrollToBottom()
    } else {
      const errorText = await res.text()
      throw new Error(`Ошибка: ${res.status}, ${errorText}`)
    }

  } catch (err: any) {
    console.error('Ошибка отправки:', err)
    alert(`🚫 ${err.message || 'Ошибка запроса'}`)
  } finally {
    isGenerating.value = false // <-- скрыть лоадер
  }
}

// Начать редактирование имени
function startEditingName() {
  if (currentChatName.value) {
    editableName.value = currentChatName.value
    isEditingName.value = true
  }
}

// Сохранить новое имя чата
async function saveChatName() {
  isEditingName.value = false
  if (!route.params.id || !editableName.value.trim()) return

  try {
    const token = localStorage.getItem('access_token')
    const response = await apiFetch(`/chat/${route.params.id}`, {
      method: 'PATCH',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ title: editableName.value }),
    })

    if (response && response.title) {
      currentChatName.value = response.title
    }
  } catch (err) {
    console.error('Ошибка переименования чата:', err)
    alert('🚫 Не удалось обновить название.')
  }
}

// Выход
function logout() {
  saveChatData()
  localStorage.removeItem('access_token')
  localStorage.removeItem('username')
  navigateTo('/login')
}
</script>

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

/* Server processing animation */
.processing-animation {
  width: 100px;
  height: 4px;
  background: linear-gradient(90deg, transparent, #60a5fa, transparent);
  animation: wave 7s linear infinite;
  border-radius: 2px;
  box-shadow: 0 0 10px rgba(96, 165, 250, 0.5);
}

@keyframes wave {
  0% { background-position: -100px; }
  100% { background-position: 100px; }
}

/* Fade-in animation for messages */
.animate-fade-in {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Smooth transitions for interactive elements */
button, a, input {
  transition: all 0.3s ease;
}

/* Glow effect for interactive elements */
.shadow-glow {
  box-shadow: 0 0 10px rgba(79, 70, 229, 0.3);
}

/* Apply glow to existing gradient elements */
.bg-gradient-to-r.from-blue-600.to-purple-600,
.bg-gradient-to-r.from-green-600.to-teal-600,
.bg-gradient-to-r.from-red-600.to-pink-600 {
  box-shadow: 0 0 10px rgba(79, 70, 229, 0.3);
}
</style>
```