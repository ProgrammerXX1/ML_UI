<template>
  <div class="flex min-h-screen w-full flex-col bg-gradient-to-br from-gray-950 via-indigo-950 to-purple-950 text-white relative overflow-hidden">
    <NeuralMesh />
    <NeuralVortex />
    <Sidebar />

    <div class="flex flex-col sm:gap-4 sm:py-4 sm:pl-64">
      <Header
  :breadcrumbs="[
    { label: 'Menu', to: '/chat' },
    { label: 'API-Keys' }
  ]"
>     
        <template #mobileMenu>
          <Sidebar />
        </template>
      </Header>

      <div v-if="isLoading" class="p-4 text-center text-gray-400 animate-pulse">
        Загрузка ключей…
      </div>

      <ApiKeysTable
        v-else
        :keys="apiKeys"
        :is-loading="isLoading"
        @create-key="createApiKey"
        @delete-key="deleteApiKey"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useAsyncData } from '#app'
import { apiFetch } from '~/utils/api'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

import Header from '@/components/layout/Header.vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import NeuralMesh from '@/components/layout/NeuralMesh.vue'
import NeuralVortex from '@/components/chat/NeuralVortex.vue'
import ApiKeysTable from '@/components/chat/ApiKeysTable.vue'

type ApiKey = {
  id: number
  key: string
  status: 'Active' | 'Revoked'
  created_at: string
}

// подгружаем пользователя
const userStore = useUserStore()
userStore.init()
if (process.client) {
  userStore.loadFromLocalStorage()
  if (localStorage.getItem('access_token')) {
    userStore.fetchUserData().catch(() => {})
  }
}

// хелпер для запросов с токеном
async function fetchWithToken<T>(url: string, opts: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('access_token')
  if (!token) throw new Error('NO_TOKEN')
  return apiFetch<T>(url, {
    ...opts,
    headers: {
      Authorization: `Bearer ${token}`,
      ...(opts.headers || {})
    }
  })
}

// используем useAsyncData (БЕЗ await!)
const { data: fetchedKeys, pending, refresh } = useAsyncData<ApiKey[]>(
  'api-keys',
  async () => {
    const raw = await fetchWithToken<any[]>('/api/keys/list')
    return raw.map(k => ({
      id: Number(k.id),
      key: k.key,
      status: k.status ?? 'Active',
      created_at: k.created_at
    }))
  },
  { server: false }
)

// локальный стейт
const apiKeys = ref<ApiKey[]>([])
// флаг загрузки = pending
const isLoading = pending

// сразу заполняем apiKeys при первой загрузке
watch(
  fetchedKeys,
  (newKeys) => {
    apiKeys.value = newKeys ?? []
  },
  { immediate: true }
)

// создание нового ключа
async function createApiKey() {
  await fetchWithToken('/api/keys/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status: 'Active' })
  })
  await refresh()
}

// удаление
async function deleteApiKey(id: number) {
  if (!confirm('Удалить API-ключ?')) return
  await fetchWithToken(`/api/keys/${id}`, { method: 'DELETE' })
  await refresh()
}

// подключаем мидлвары
definePageMeta({ middleware: ['auth', 'role-auth'] })
</script>
