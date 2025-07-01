```vue
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
        <!-- Карточки с общими метриками -->
        <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card class="bg-gray-900/30 border border-indigo-700/50 shadow-xl rounded-xl backdrop-blur-lg">
            <CardHeader class="flex flex-row items-center justify-between">
              <CardTitle class="text-lg font-bold text-white">
                Активные пользователи
              </CardTitle>
              <Users class="w-6 h-6 text-blue-400" />
            </CardHeader>
            <CardContent>
              <p class="text-2xl font-bold text-gray-200">42</p>
              <p class="text-sm text-gray-400">За последние 24 часа</p>
            </CardContent>
          </Card>
          <Card class="bg-gray-900/30 border border-indigo-700/50 shadow-xl rounded-xl backdrop-blur-lg">
            <CardHeader class="flex flex-row items-center justify-between">
              <CardTitle class="text-lg font-bold text-white">
                API запросы
              </CardTitle>
              <Code class="w-6 h-6 text-purple-400" />
            </CardHeader>
            <CardContent>
              <p class="text-2xl font-bold text-gray-200">127</p>
              <p class="text-sm text-gray-400">За последние 24 часа</p>
            </CardContent>
          </Card>
          <Card class="bg-gray-900/30 border border-indigo-700/50 shadow-xl rounded-xl backdrop-blur-lg">
            <CardHeader class="flex flex-row items-center justify-between">
              <CardTitle class="text-lg font-bold text-white">
                Использовано токенов
              </CardTitle>
              <DollarSign class="w-6 h-6 text-green-400" />
            </CardHeader>
            <CardContent>
              <p class="text-2xl font-bold text-gray-200">15,320</p>
              <p class="text-sm text-gray-400">За текущий месяц</p>
            </CardContent>
          </Card>
          <Card class="bg-gray-900/30 border border-indigo-700/50 shadow-xl rounded-xl backdrop-blur-lg">
            <CardHeader class="flex flex-row items-center justify-between">
              <CardTitle class="text-lg font-bold text-white">
                GPU Usage
              </CardTitle>
              <Cpu class="w-6 h-6 text-red-400" />
            </CardHeader>
            <CardContent>
              <p class="text-2xl font-bold text-gray-200">78%</p>
              <p class="text-sm text-gray-400">Текущее использование</p>
            </CardContent>
          </Card>
        </div>

        <!-- Таблица активности пользователей -->
        <Card class="bg-gray-900/30 border border-indigo-700/50 shadow-xl rounded-xl backdrop-blur-lg">
          <CardHeader>
            <CardTitle class="text-2xl font-bold text-white">
              Активность пользователей
            </CardTitle>
            <CardDescription class="text-gray-300">
              Запросы обычных пользователей
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID</TableHead>
                  <TableHead>Имя</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Запросы</TableHead>
                  <TableHead>Последнее действие</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableRow v-for="user in users" :key="user.id">
                  <TableCell>{{ user.id }}</TableCell>
                  <TableCell>{{ user.name }}</TableCell>
                  <TableCell>{{ user.email }}</TableCell>
                  <TableCell>{{ user.requests }}</TableCell>
                  <TableCell>{{ new Date(user.lastAction).toLocaleString() }}</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        <!-- Таблица API-запросов -->
        <Card class="bg-gray-900/30 border border-indigo-700/50 shadow-xl rounded-xl backdrop-blur-lg">
          <CardHeader>
            <CardTitle class="text-2xl font-bold text-white">
              API запросы
            </CardTitle>
            <CardDescription class="text-gray-300">
              Запросы кодеров через API
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID ключа</TableHead>
                  <TableHead>Пользователь</TableHead>
                  <TableHead>Токены</TableHead>
                  <TableHead>Эндпоинт</TableHead>
                  <TableHead>Статус</TableHead>
                  <TableHead>Время</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableRow v-for="apiRequest in apiRequests" :key="apiRequest.id">
                  <TableCell>{{ apiRequest.keyId }}</TableCell>
                  <TableCell>{{ apiRequest.user }}</TableCell>
                  <TableCell>{{ apiRequest.tokens }}</TableCell>
                  <TableCell>{{ apiRequest.endpoint }}</TableCell>
                  <TableCell :class="[apiRequest.status === 'Success' ? 'text-green-400' : 'text-red-400']">
                    {{ apiRequest.status }}
                  </TableCell>
                  <TableCell>{{ new Date(apiRequest.time).toLocaleString() }}</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        <!-- Графики использования ресурсов -->
        <Card class="bg-gray-900/30 border border-indigo-700/50 shadow-xl rounded-xl backdrop-blur-lg">
          <CardHeader>
            <CardTitle class="text-2xl font-bold text-white">
              Использование ресурсов
            </CardTitle>
            <CardDescription class="text-gray-300">
              Токены и GPU за последние 7 дней
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div class="grid gap-4 md:grid-cols-2">
              <!-- График токенов -->
              <div>
                <h3 class="text-lg font-semibold text-gray-200 mb-2">Использование токенов</h3>
                <canvas ref="tokensChart" class="w-full h-64"></canvas>
              </div>
              <!-- График GPU -->
              <div>
                <h3 class="text-lg font-semibold text-gray-200 mb-2">Использование GPU (%)</h3>
                <canvas ref="gpuChart" class="w-full h-64"></canvas>
              </div>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import Chart from 'chart.js/auto'
import { Users, Code, DollarSign, Cpu } from 'lucide-vue-next'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from '@/components/ui/table'

// Компоненты
import Header from '@/components/layout/Header.vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import NeuralMesh from '@/components/layout/NeuralMesh.vue'

const userStore = useUserStore()

// Статичные данные для пользователей
const users = ref([
  { id: 1, name: 'Иван Иванов', email: 'ivan@example.com', requests: 45, lastAction: '2025-07-01T10:00:00Z' },
  { id: 2, name: 'Мария Петрова', email: 'maria@example.com', requests: 32, lastAction: '2025-07-01T09:30:00Z' },
  { id: 3, name: 'Алексей Сидоров', email: 'alexey@example.com', requests: 67, lastAction: '2025-06-30T15:45:00Z' },
])

// Статичные данные для API-запросов
const apiRequests = ref([
  { id: 1, keyId: 'API123', user: 'coder1@example.com', tokens: 500, endpoint: '/api/generate', status: 'Success', time: '2025-07-01T08:00:00Z' },
  { id: 2, keyId: 'API456', user: 'coder2@example.com', tokens: 750, endpoint: '/api/analyze', status: 'Failed', time: '2025-07-01T07:30:00Z' },
  { id: 3, keyId: 'API789', user: 'coder3@example.com', tokens: 300, endpoint: '/api/predict', status: 'Success', time: '2025-06-30T22:15:00Z' },
])

// Ссылки на canvas для графиков
const tokensChart = ref<HTMLCanvasElement | null>(null)
const gpuChart = ref<HTMLCanvasElement | null>(null)

// Статичные данные для графиков
const chartData = {
  labels: ['2025-06-25', '2025-06-26', '2025-06-27', '2025-06-28', '2025-06-29', '2025-06-30', '2025-07-01'],
  tokens: [1200, 1500, 1800, 1300, 2000, 1700, 15320],
  gpu: [65, 70, 68, 75, 80, 72, 78],
}

onMounted(async () => {
  userStore.init()
  if (process.client) {
    userStore.loadFromLocalStorage()
    if (localStorage.getItem('access_token')) {
      await userStore.fetchUserData()
    }

    // Инициализация графика токенов
    if (tokensChart.value) {
      new Chart(tokensChart.value, {
        type: 'line',
        data: {
          labels: chartData.labels,
          datasets: [{
            label: 'Токены',
            data: chartData.tokens,
            borderColor: 'rgba(59, 130, 246, 0.8)',
            backgroundColor: 'rgba(59, 130, 246, 0.2)',
            tension: 0.4,
            fill: true,
          }],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              title: { display: true, text: 'Токены', color: '#d1d5db' },
              grid: { color: 'rgba(255, 255, 255, 0.1)' },
              ticks: { color: '#d1d5db' },
            },
            x: {
              title: { display: true, text: 'Дата', color: '#d1d5db' },
              grid: { color: 'rgba(255, 255, 255, 0.1)' },
              ticks: { color: '#d1d5db' },
            },
          },
          plugins: {
            legend: { labels: { color: '#d1d5db' } },
          },
        },
      })
    }

    // Инициализация графика GPU
    if (gpuChart.value) {
      new Chart(gpuChart.value, {
        type: 'line',
        data: {
          labels: chartData.labels,
          datasets: [{
            label: 'GPU Usage (%)',
            data: chartData.gpu,
            borderColor: 'rgba(239, 68, 68, 0.8)',
            backgroundColor: 'rgba(239, 68, 68, 0.2)',
            tension: 0.4,
            fill: true,
          }],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              title: { display: true, text: 'GPU Usage (%)', color: '#d1d5db' },
              grid: { color: 'rgba(255, 255, 255, 0.1)' },
              ticks: { color: '#d1d5db' },
            },
            x: {
              title: { display: true, text: 'Дата', color: '#d1d5db' },
              grid: { color: 'rgba(255, 255, 255, 0.1)' },
              ticks: { color: '#d1d5db' },
            },
          },
          plugins: {
            legend: { labels: { color: '#d1d5db' } },
          },
        },
      })
    }
  }
})

definePageMeta({ middleware: ['auth', 'role-auth'] })
</script>
```