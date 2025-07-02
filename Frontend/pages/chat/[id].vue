<template>
  <div class="min-h-screen w-full bg-[rgb(24,24,27)] text-white flex flex-col">
    <Header
      :breadcrumbs="[
        { label: 'Menu', to: '/chat' },
        { label: 'Chat', to: `/chat/${chatId}` },
        { label: chat?.name || '...' }
      ]"
    >
      <template #actions>
        <button
          @click="handleBack"
          class="text-sm bg-gray-800 px-3 py-1.5 rounded-lg hover:bg-gray-700 transition"
        >
          Назад
        </button>
      </template>
    </Header>

    <main ref="scrollContainer" class="flex-1 overflow-y-auto p-4 sm:px-6 md:px-8">
      <div v-if="isLoading" class="text-center text-gray-400">Загрузка...</div>
      <div v-else>
        <div v-for="(msg, index) in allMessages" :key="index" class="mb-6">
          <div class="text-sm text-gray-400">Вы</div>
          <div class="bg-gray-800 p-3 rounded-lg mt-1 whitespace-pre-wrap">
            {{ msg.request_text || msg.content }}
          </div>

          <div class="mt-4 text-sm text-gray-400">Модель</div>
          <div class="bg-gray-800 p-3 rounded-lg mt-1 whitespace-pre-wrap">
            {{ msg.response_text || msg.content }}
          </div>
        </div>
      </div>
    </main>

    <form
      @submit.prevent="sendMessage"
      class="flex items-center gap-2 p-4 bg-gray-900 border-t border-gray-800"
    >
      <input
        v-model="newMessage"
        placeholder="Напишите сообщение..."
        class="flex-1 rounded-lg bg-gray-800 text-white p-2 outline-none border border-gray-700"
      />
      <button
        type="submit"
        class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg"
        :disabled="sending"
      >
        {{ sending ? '...' : 'Отправить' }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiFetch } from '~/utils/api'
import Header from '@/components/layout/Header.vue'

type Message = {
  request_text: string
  response_text: string
  timestamp: string
  latency_ms: number
  chat_id: number
}

type Chat = {
  id: number
  title: string
  status: string
}

const route = useRoute()
const router = useRouter()
const chatId = Number(route.params.id)

const chat = ref<Chat | null>(null)
const messages = ref<Message[]>([])
const newMessage = ref('')
const tempMessage = ref('')
const isLoading = ref(true)
const sending = ref(false)
const isTyping = ref(false)
const typedResponse = ref('')
const scrollContainer = ref<HTMLElement | null>(null)

const allMessages = computed(() => {
  if (isTyping.value) {
    return [
      ...messages.value,
      {
        request_text: tempMessage.value,
        response_text: typedResponse.value,
        timestamp: new Date().toISOString(),
        latency_ms: 0,
        chat_id: chatId
      }
    ]
  }
  return messages.value
})

async function authCheck(): Promise<string> {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('Требуется авторизация')
    await router.push('/login')
    throw new Error('NO_TOKEN')
  }
  return token
}

async function fetchWithToken<T>(url: string, options: RequestInit = {}): Promise<T> {
  const token = await authCheck()
  return apiFetch(url, {
    ...options,
    headers: {
      Authorization: `Bearer ${token}`,
      ...(options.headers || {})
    }
  })
}

async function loadChat() {
  try {
    const chatData = await fetchWithToken<Chat>(`/chat/${chatId}`)
    const msgData = await fetchWithToken<Message[]>(`/chat/${chatId}/messages`)
    chat.value = chatData
    messages.value = msgData
    await nextTick()
    scrollToBottom()
  } catch (err) {
    console.error('Ошибка загрузки чата:', err)
    alert('Не удалось загрузить чат')
    router.push('/chat')
  } finally {
    isLoading.value = false
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (scrollContainer.value) {
      scrollContainer.value.scrollTop = scrollContainer.value.scrollHeight
    }
  })
}

async function sendMessage() {
  const input = newMessage.value.trim()
  if (!input) return

  sending.value = true
  isTyping.value = true
  typedResponse.value = ''
  tempMessage.value = input
  newMessage.value = ''
  scrollToBottom()

  try {
    const res = await fetchWithToken<Message>(`/chat/${chatId}/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: input })
    })

    const fullText = res.response_text || ''
    let i = 0

    const interval = setInterval(() => {
      if (i < fullText.length) {
        typedResponse.value += fullText[i]
        i++
        scrollToBottom()
      } else {
        clearInterval(interval)

        messages.value.push({ ...res })

        typedResponse.value = ''
        tempMessage.value = ''
        isTyping.value = false
        scrollToBottom()
      }
    }, 15)
  } catch (err) {
    console.error('❌ Ошибка отправки:', err)
    alert('Ошибка при отправке сообщения')
    isTyping.value = false
    tempMessage.value = ''
  } finally {
    sending.value = false
  }
}

async function saveChat() {
  try {
    if (messages.value.length > 0) {
      const serialized = messages.value.map((m) => ({
        ...m,
        timestamp: typeof m.timestamp === 'string' ? m.timestamp : new Date(m.timestamp).toISOString()
      }))

      await fetchWithToken(`/chat/${chatId}/save`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(serialized)
      })
    }
  } catch (err) {
    console.warn('Ошибка сохранения чата:', err)
  }
}

async function handleBack() {
  await saveChat()
  await router.push('/chat')
}

onMounted(loadChat)
onBeforeUnmount(saveChat)
</script>
