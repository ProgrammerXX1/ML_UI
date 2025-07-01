<template>
  <div class="flex min-h-screen w-full flex-col bg-gradient-to-br from-gray-950 via-indigo-950 to-purple-950 text-white relative overflow-hidden">
    <NeuralMesh />
    <NeuralVortex />
    <Sidebar />
    <div class="flex flex-col sm:gap-4 sm:py-4 sm:pl-64">
      <Header
  :breadcrumbs="[
    { label: 'Menu', to: '/chat' },
    { label: 'Chats' }
  ]"
>
  <template #mobileMenu>
    <Sidebar />
  </template>
</Header>

      <ChatTable
        :chats="chats"
        :is-loading="isLoading"
        @chat-click="handleChatClick"
        @edit-chat="openEditModal"
        @delete-chat="deleteChat"
        @create-chat="createChat"
      />
      <EditModal
        :chat="editingChat"
        :is-open="isEditModalOpen"
        @save-chat="saveChat"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useRuntimeConfig } from '#app'
import { apiFetch } from '~/utils/api'
import { useUserStore } from '@/stores/user'

import Sidebar from '@/components/layout/Sidebar.vue'
import Header from '@/components/layout/Header.vue'
import ChatTable from '@/components/chat/ChatTable.vue'
import EditModal from '@/components/chat/EditModal.vue'
import NeuralMesh from '@/components/layout/NeuralMesh.vue'
import NeuralVortex from '@/components/chat/NeuralVortex.vue'

const userStore = useUserStore()
const router = useRouter()
const config = useRuntimeConfig()

type ChatStatus = 'Active' | 'Draft' | 'Archived'
type Chat = {
  id: number
  name: string
  status: ChatStatus
  created_at: string
  image?: string
}

const isLoading = ref(false)
const chats = ref<Chat[]>([])
const isEditModalOpen = ref(false)
const editingChat = ref<Chat | null>(null)
const clickCounts = ref<Record<number, number>>({})
const lastClickTime = ref<Record<number, number>>({})

onMounted(async () => {
  userStore.init()
  userStore.loadFromLocalStorage()
  if (localStorage.getItem('access_token')) {
    await userStore.fetchUserData()
  }
  await loadChats()
  window.addEventListener('storage', syncLocalStorage)
})

onUnmounted(() => {
  window.removeEventListener('storage', syncLocalStorage)
})

function syncLocalStorage() {
  userStore.loadFromLocalStorage()
}

function authCheck(): string {
  const token = localStorage.getItem('access_token')
  if (!token) {
    throw new Error('NO_TOKEN')
  }
  return token
}

async function fetchWithToken<T>(url: string, options: RequestInit = {}): Promise<T> {
  const token = authCheck()
  return await apiFetch(url, {
    ...options,
    headers: {
      Authorization: `Bearer ${token}`,
      ...(options.headers || {})
    }
  })
}

async function loadChats() {
  try {
    isLoading.value = true
    const res = await fetchWithToken<any[]>('/chat/list')
    chats.value = res.map(chat => ({
      id: Number(chat.id),
      name: chat.title || 'Без названия',
      status: chat.status || 'Draft',
      created_at: chat.created_at,
      image: '/images/chat-2.png'
    }))
  } catch (err) {
    console.error('loadChats: Ошибка при загрузке чатов:', err)
    chats.value = []
  } finally {
    isLoading.value = false
  }
}

async function handleChatClick(chatId: number) {
  const now = Date.now()
  const lastClick = lastClickTime.value[chatId] || 0
  if (now - lastClick < 300) {
    await goToChat(chatId)
    clickCounts.value[chatId] = 0
    lastClickTime.value[chatId] = 0
  } else {
    clickCounts.value[chatId] = 1
    lastClickTime.value[chatId] = now
  }
}

async function goToChat(chatId: number) {
  try {
    await fetchWithToken(`/chat/${chatId}`, { method: 'GET' })
    await router.push(`/chat/${chatId}`)
  } catch (err) {
    alert('Не удалось открыть чат')
  }
}

async function createChat() {
  try {
    const res = await fetchWithToken<Chat>('/chat/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: `Новый чат ${new Date().toISOString()}`, status: 'Draft' })
    })
    await loadChats()
    await router.push(`/chat/${res.id}`)
  } catch (err) {
    alert('Ошибка при создании чата')
  }
}

async function saveChat() {
  if (!editingChat.value) return
  try {
    await fetchWithToken(`/chat/${editingChat.value.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: editingChat.value.name, status: editingChat.value.status })
    })
    await fetchWithToken(`/chat/${editingChat.value.id}/save`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({})
    })
    await loadChats()
  } catch (err) {
    alert('Ошибка при сохранении')
  } finally {
    isEditModalOpen.value = false
    editingChat.value = null
  }
}

async function deleteChat(chatId: number) {
  if (!confirm('Удалить чат?')) return
  try {
    await fetchWithToken(`/chat/${chatId}`, { method: 'DELETE' })
    await loadChats()
  } catch (err) {
    alert('Ошибка при удалении чата')
  }
}

function openEditModal(chat: Chat) {
  editingChat.value = { ...chat }
  isEditModalOpen.value = true
}

definePageMeta({ middleware: ['auth', 'role-auth'] })
</script>
