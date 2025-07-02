<template>
  <div class="flex min-h-screen w-full flex-col bg-gradient-to-br from-gray-950 via-indigo-950 to-purple-950 text-white relative overflow-hidden">
    <NeuralMesh />
    <Sidebar />
    <div class="flex flex-col sm:gap-4 sm:py-4 sm:pl-64">
      <Header :breadcrumbs="[
        { label: 'Menu', to: '/chat' },
        { label: 'Admin Dashboard' }
      ]">
        <template #mobileMenu>
          <Sidebar />
        </template>
      </Header>
      <main class="grid flex-1 items-start gap-4 p-4 sm:px-6 md:gap-8">

        <!-- Метрики -->
        <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card class="bg-gray-900/30 border border-indigo-700/50 shadow-xl rounded-xl backdrop-blur-lg">
            <CardHeader class="flex flex-row items-center justify-between">
              <CardTitle class="text-lg font-bold text-white">Активные пользователи</CardTitle>
              <Users class="w-6 h-6 text-blue-400" />
            </CardHeader>
            <CardContent>
              <p class="text-2xl font-bold text-gray-200">{{ dashboard.users }}</p>
              <p class="text-sm text-gray-400">Всего зарегистрировано</p>
            </CardContent>
          </Card>

          <Card class="bg-gray-900/30 border border-indigo-700/50 shadow-xl rounded-xl backdrop-blur-lg">
            <CardHeader class="flex flex-row items-center justify-between">
              <CardTitle class="text-lg font-bold text-white">API запросы</CardTitle>
              <Code class="w-6 h-6 text-purple-400" />
            </CardHeader>
            <CardContent>
              <p class="text-2xl font-bold text-gray-200">{{ dashboard.logs }}</p>
              <p class="text-sm text-gray-400">Всего логов</p>
            </CardContent>
          </Card>

          <Card class="bg-gray-900/30 border border-indigo-700/50 shadow-xl rounded-xl backdrop-blur-lg">
            <CardHeader class="flex flex-row items-center justify-between">
              <CardTitle class="text-lg font-bold text-white">Средняя задержка</CardTitle>
              <DollarSign class="w-6 h-6 text-green-400" />
            </CardHeader>
            <CardContent>
              <p class="text-2xl font-bold text-gray-200">{{ dashboard.avg_latency }} мс</p>
              <p class="text-sm text-gray-400">Среднее время ответа</p>
            </CardContent>
          </Card>

          <Card class="bg-gray-900/30 border border-indigo-700/50 shadow-xl rounded-xl backdrop-blur-lg">
            <CardHeader class="flex flex-row items-center justify-between">
              <CardTitle class="text-lg font-bold text-white">CPU Usage</CardTitle>
              <Cpu class="w-6 h-6 text-red-400" />
            </CardHeader>
            <CardContent>
              <p class="text-2xl font-bold text-gray-200">{{ dashboard.system.cpu_percent }}%</p>
              <p class="text-sm text-gray-400">Текущая загрузка CPU</p>
            </CardContent>
          </Card>
        </div>

        <!-- GPU -->
<CardContent>
  <div v-if="dashboard.system.gpus.length > 0">
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>#</TableHead>
          <TableHead>Модель</TableHead>
          <TableHead>Объем памяти (GB)</TableHead>
          <TableHead>Выделено (GB)</TableHead>
          <TableHead>Резерв (GB)</TableHead>
          <TableHead>Загрузка (%)</TableHead>
          <TableHead>Температура (°C)</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow v-for="(gpu, index) in dashboard.system.gpus" :key="index">
          <TableCell>{{ index + 1 }}</TableCell>
          <TableCell>{{ gpu.name }}</TableCell>
          <TableCell>{{ gpu.memory_total }}</TableCell>
          <TableCell>{{ gpu.memory_allocated }}</TableCell>
          <TableCell>{{ gpu.memory_reserved }}</TableCell>
          <TableCell>{{ gpu.utilization }}%</TableCell>
          <TableCell>{{ gpu.temperature }}°C</TableCell>
        </TableRow>
      </TableBody>
    </Table>
  </div>
  <p v-else class="text-sm text-gray-400">Нет доступных GPU</p>
</CardContent>


        <!-- RAM и последний чат -->
        <div class="grid gap-4 md:grid-cols-2">
          <Card class="bg-gray-900/30 border border-indigo-700/50 shadow-xl rounded-xl backdrop-blur-lg">
            <CardHeader class="flex flex-row items-center justify-between">
              <CardTitle class="text-lg font-bold text-white">RAM Usage</CardTitle>
            </CardHeader>
            <CardContent>
              <p class="text-2xl font-bold text-gray-200">
                {{ dashboard.system.ram_used }} / {{ dashboard.system.ram_total }} GB
              </p>
              <p class="text-sm text-gray-400">Использовано памяти</p>
            </CardContent>
          </Card>

          <Card class="bg-gray-900/30 border border-indigo-700/50 shadow-xl rounded-xl backdrop-blur-lg">
            <CardHeader class="flex flex-row items-center justify-between">
              <CardTitle class="text-lg font-bold text-white">Последний чат</CardTitle>
            </CardHeader>
            <CardContent>
              <p class="text-lg text-gray-200">{{ dashboard.latest_chat_title }}</p>
              <p class="text-sm text-gray-400">Название последнего активного чата</p>
            </CardContent>
          </Card>
        </div>

      </main>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { Users, Code, DollarSign, Cpu } from 'lucide-vue-next'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from '@/components/ui/table'
import Header from '@/components/layout/Header.vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import NeuralMesh from '@/components/layout/NeuralMesh.vue'
import { apiFetch } from '@/utils/api'

const userStore = useUserStore()

// Проверка токена
function authCheck(): string {
  const token = localStorage.getItem('access_token')
  if (!token) throw new Error('NO_TOKEN')
  return token
}

// Запрос с токеном
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

// Типизация
interface GPUStat {
  name: string
  memory_total: number
  memory_allocated: number
  memory_reserved: number
  utilization: number       // %
  temperature: number       // °C
}

interface DashboardData {
  users: number
  chats: number
  logs: number
  api_keys: number
  avg_latency: number
  latest_chat_title: string
  system: {
    cpu_percent: number
    ram_total: number
    ram_used: number
    gpus: GPUStat[]
  }
}


// Данные дашборда
const dashboard = ref<DashboardData>({
  users: 0,
  chats: 0,
  logs: 0,
  api_keys: 0,
  avg_latency: 0,
  latest_chat_title: '',
  system: {
    cpu_percent: 0,
    ram_total: 0,
    ram_used: 0,
    gpus: []
  }
})

// Загрузка дашборда
async function fetchDashboard() {
  try {
    const res = await fetchWithToken<DashboardData>('/admin/dashboard')
    if (res && typeof res === 'object') {
      dashboard.value = res
    } else {
      console.warn('⚠️ Неверный ответ от сервера:', res)
    }
  } catch (e) {
    console.error('❌ Ошибка загрузки dashboard:', e)
  }
}

onMounted(async () => {
  userStore.init()
  if (process.client) {
    userStore.loadFromLocalStorage()

    if (localStorage.getItem('access_token')) {
      await userStore.fetchUserData()
    }

    await fetchDashboard()
    setInterval(fetchDashboard, 6000)
  }
})

definePageMeta({ middleware: ['auth', 'role-auth'] })
</script>
