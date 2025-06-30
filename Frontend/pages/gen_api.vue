```vue
<template>
  <div class="flex min-h-screen w-full flex-col bg-gradient-to-br from-gray-950 via-indigo-950 to-purple-950 text-white relative overflow-hidden">
    <!-- Background Neural Mesh -->
    <canvas ref="neuralMeshCanvas" class="absolute inset-0 z-0 pointer-events-none"></canvas>
    <!-- Bottom-Left Neural Vortex -->
    <div class="fixed bottom-4 left-4 z-10 hidden sm:block">
      <svg class="h-16 w-16 animate-neural-vortex" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <g class="nodes">
          <circle cx="50" cy="50" r="8" fill="none" stroke="#c084fc" stroke-width="2" class="node node-main" />
          <circle cx="40" cy="40" r="6" fill="none" stroke="#60a5fa" stroke-width="1.5" class="node node-1" />
          <circle cx="60" cy="40" r="6" fill="none" stroke="#60a5fa" stroke-width="1.5" class="node node-2" />
          <circle cx="50" cy="60" r="6" fill="none" stroke="#60a5fa" stroke-width="1.5" class="node node-3" />
          <circle cx="50" cy="50" r="10" fill="none" stroke="#a5b4fc" stroke-width="1" class="signal-pulse" />
        </g>
        <g class="connections">
          <path d="M50 50 L40 40" stroke="#a5b4fc" stroke-width="1" class="connection" />
          <path d="M50 50 L60 40" stroke="#a5b4fc" stroke-width="1" class="connection" />
          <path d="M50 50 L50 60" stroke="#a5b4fc" stroke-width="1" class="connection" />
        </g>
      </svg>
    </div>
    <!-- Sidebar (Desktop) -->
    <aside class="fixed inset-y-0 left-0 z-20 w-64 flex-col border-r border-indigo-700/50 bg-gray-900/30 backdrop-blur-lg hidden sm:flex">
  <nav class="flex flex-col gap-6 px-4 py-6 text-lg font-medium">

    <NuxtLink to="/" class="group flex items-center justify-center h-12 w-full rounded-lg bg-gradient-to-r from-red-600 to-purple-600 text-black transition-all duration-300 hover:from-blue-500 hover:to-purple-500 shadow-glow">
      <svg class="h-8 w-8 animate-neural-network" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <g class="nodes">
          <circle cx="50" cy="50" r="10" fill="none" stroke="#a5b4fc" stroke-width="2" class="node node-center" />
          <circle cx="30" cy="30" r="8" fill="none" stroke="#c084fc" stroke-width="2" class="node node-top-left" />
          <circle cx="70" cy="30" r="8" fill="none" stroke="#c084fc" stroke-width="2" class="node-coffee" />
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
      <span class="ml-2 text-sm font-semibold animate-flicker">NeuralNet AI</span>
    </NuxtLink>

    <NuxtLink to="/" class="flex items-center gap-4 px-2.5 text-gray-300 hover:text-white hover:bg-indigo-800/50 rounded-lg py-2 transition-all duration-200 shadow-glow">
      <Home class="h-5 w-5" /> Tester
    </NuxtLink>

    <NuxtLink to="/orders" class="flex items-center gap-4 px-2.5 text-gray-300 hover:text-white hover:bg-indigo-800/50 rounded-lg py-2 transition-all duration-200 shadow-glow">
      <ShoppingCart class="h-5 w-5" /> Orders
    </NuxtLink>

    <NuxtLink to="/" class="flex items-center gap-4 px-2.5 text-gray-300 hover:text-white hover:bg-indigo-800/50 rounded-lg py-2 transition-all duration-200 shadow-glow">
      <Package class="h-5 w-5" /> Chats
    </NuxtLink>

    <NuxtLink to="/customers" class="flex items-center gap-4 px-2.5 text-gray-300 hover:text-white hover:bg-indigo-800/50 rounded-lg py-2 transition-all duration-200 shadow-glow">
      <Users2 class="h-5 w-5" /> Customers
    </NuxtLink>

    <NuxtLink to="/api-keys" class="flex items-center gap-4 px-2.5 text-white bg-indigo-700/50 rounded-lg py-2 shadow-glow">
      <Key class="h-5 w-5" /> API Keys
    </NuxtLink>

    <NuxtLink to="/settings" class="flex items-center gap-4 px-2.5 text-gray-300 hover:text-white hover:bg-indigo-800/50 rounded-lg py-2 transition-all duration-200 shadow-glow">
      <LineChart class="h-5 w-5" /> Settings
    </NuxtLink>

  </nav>
</aside>

    <!-- Main Layout -->
    <div class="flex flex-col sm:gap-4 sm:py-4 sm:pl-64">
      <header class="sticky top-0 z-30 flex h-14 items-center gap-4 border-b border-indigo-700/50 bg-gray-900/30 backdrop-blur-lg px-4 sm:px-6">
        <Sheet>
  <SheetTrigger as-child>
    <Button size="icon" variant="outline" class="sm:hidden text-white border-indigo-700 hover:bg-indigo-800/50 shadow-glow">
      <PanelLeft class="h-5 w-5" />
      <span class="sr-only">Toggle Menu</span>
    </Button>
  </SheetTrigger>

  <SheetContent side="left" class="sm:max-w-xs bg-gray-900/30 text-white border-indigo-700/50 backdrop-blur-lg">
    <nav class="grid gap-6 text-lg font-medium">

      <NuxtLink to="/" class="group flex items-center justify-start h-12 rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 text-white transition-all duration-300 hover:from-blue-500 hover:to-purple-500 shadow-glow">
        <svg class="h-8 w-8 ml-2 animate-neural-network" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
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
        <span class="ml-2 text-sm font-semibold animate-flicker">NeuralNet AI</span>
      </NuxtLink>

      <NuxtLink to="/" class="flex items-center gap-4 px-2.5 text-gray-300 hover:text-white hover:bg-indigo-800/50 rounded-lg py-2 transition-all duration-200 shadow-glow">
        <Home class="h-5 w-5" /> Tester
      </NuxtLink>

      <NuxtLink to="/orders" class="flex items-center gap-4 px-2.5 text-gray-300 hover:text-white hover:bg-indigo-800/50 rounded-lg py-2 transition-all duration-200 shadow-glow">
        <ShoppingCart class="h-5 w-5" /> Orders
      </NuxtLink>

      <NuxtLink to="/" class="flex items-center gap-4 px-2.5 text-gray-300 hover:text-white hover:bg-indigo-800/50 rounded-lg py-2 transition-all duration-200 shadow-glow">
        <Package class="h-5 w-5" /> Chats
      </NuxtLink>

      <NuxtLink to="/customers" class="flex items-center gap-4 px-2.5 text-gray-300 hover:text-white hover:bg-indigo-800/50 rounded-lg py-2 transition-all duration-200 shadow-glow">
        <Users2 class="h-5 w-5" /> Customers
      </NuxtLink>

      <NuxtLink to="/api-keys" class="flex items-center gap-4 px-2.5 text-white bg-indigo-700/50 rounded-lg py-2 shadow-glow">
        <Key class="h-5 w-5" /> API Keys
      </NuxtLink>

      <NuxtLink to="/settings" class="flex items-center gap-4 px-2.5 text-gray-300 hover:text-white hover:bg-indigo-800/50 rounded-lg py-2 transition-all duration-200 shadow-glow">
        <LineChart class="h-5 w-5" /> Settings
      </NuxtLink>

    </nav>
  </SheetContent>
</Sheet>

        <!-- Breadcrumb -->
        <Breadcrumb class="hidden md:flex text-gray-300 animate-glow-text">
          <BreadcrumbList>
            <BreadcrumbItem>
              <BreadcrumbLink as-child><a href="/" class="hover:text-white transition-colors">Dashboard</a></BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbPage>API Keys</BreadcrumbPage></BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>
        <!-- Search Bar -->
        <div class="relative ml-auto flex-1 md:grow-0">
          <Search class="absolute left-2.5 top-2.5 h-4 w-4 text-gray-400" />
          <Input
            v-model="searchQuery"
            type="search"
            placeholder="Search..."
            class="w-full rounded-lg bg-gray-800/20 text-white placeholder-gray-400 pl-8 border border-indigo-700/50 focus:border-purple-500 transition-all duration-300 hover:scale-[1.02] shadow-glow md:w-[200px] lg:w-[320px]"
          />
        </div>
        <!-- Theme Switch -->
        <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <Button variant="outline" class="text-white border-indigo-700/50 hover:bg-indigo-800/50 transition-all duration-300 shadow-glow">
              <Icon icon="radix-icons:moon" class="h-5 w-5 dark:hidden" />
              <Icon icon="radix-icons:sun" class="h-5 w-5 hidden dark:block" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" class="bg-gray-800/30 text-white border border-indigo-700/50 backdrop-blur-lg">
            <DropdownMenuItem @click="colorMode = 'light'" class="hover:bg-indigo-700/50">Light</DropdownMenuItem>
            <DropdownMenuItem @click="colorMode = 'dark'" class="hover:bg-indigo-700/50">Dark</DropdownMenuItem>
            <DropdownMenuItem @click="colorMode = 'system'" class="hover:bg-indigo-700/50">System</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
        <!-- Profile -->
        <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <Button variant="secondary" size="icon" class="rounded-full bg-indigo-700 hover:bg-indigo-600 transition-all duration-300 shadow-glow">
              <CircleUser class="h-5 w-5 text-white" />
              <span class="sr-only">Toggle user menu</span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" class="bg-gray-800/30 text-white border border-indigo-700/50 backdrop-blur-lg">
            <DropdownMenuLabel>Acc: {{ username }}</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="showUnderDevelopment" class="hover:bg-indigo-700/50">Settings</DropdownMenuItem>
            <DropdownMenuItem @click="showUnderDevelopment" class="hover:bg-indigo-700/50">Support</DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="logout" class="hover:bg-indigo-700/50">Logout</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </header>
      <main class="grid flex-1 items-start gap-4 p-4 sm:px-6 md:gap-8">
        <Tabs v-model="activeTab">
          <div class="flex items-center">
            <TabsList class="bg-gray-800/20 border border-indigo-700/50 rounded-lg">
              <TabsTrigger value="all" @click="changeTab('all')" class="hover:bg-indigo-700/50 transition-all duration-300">All</TabsTrigger>
              <TabsTrigger value="Active" @click="changeTab('Active')" class="hover:bg-indigo-700/50 transition-all duration-300">Active</TabsTrigger>
              <TabsTrigger value="Inactive" @click="changeTab('Inactive')" class="hover:bg-indigo-700/50 transition-all duration-300">Inactive</TabsTrigger>
            </TabsList>
            <div class="ml-auto flex items-center gap-2">
              <Button size="sm" class="h-7 gap-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white transition-all duration-300 shadow-glow" @click="generateApiKey">
                <PlusCircle class="h-4 w-4" />
                <span class="sr-only sm:not-sr-only">Generate API Key</span>
              </Button>
            </div>
          </div>
          <Card class="bg-gray-900/30 border border-indigo-700/50 text-white shadow-xl rounded-xl backdrop-blur-lg">
            <CardHeader>
              <CardTitle class="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent animate-flicker">API Keys</CardTitle>
              <CardDescription class="text-gray-300 animate-glow-text">Manage your API keys for secure access.</CardDescription>
            </CardHeader>
            <CardContent>
              <div v-if="isLoading">
                <p class="text-gray-300 animate-pulse">Загрузка...</p>
              </div>
              <div v-else-if="!apiKeys.length">
                <p class="text-gray-300">API ключи не найдены. Попробуйте сгенерировать новый ключ.</p>
              </div>
              <Table v-else>
                <TableHeader>
                  <TableRow class="border-b border-indigo-700/50">
                    <TableHead class="text-gray-300 animate-glow-text">Key</TableHead>
                    <TableHead class="text-gray-300 animate-glow-text">Status</TableHead>
                    <TableHead class="hidden md:table-cell text-gray-300 animate-glow-text">Created at</TableHead>
                    <TableHead><span class="sr-only">Actions</span></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody class="max-h-[400px] overflow-y-auto">
                  <TableRow
                    v-for="key in paginatedKeys"
                    :key="key.id"
                    class="quest-row"
                  >
                    <TableCell class="font-medium text-gray-200">
                      {{ key.key.substring(0, 8) + '...' + key.key.substring(key.key.length - 8) }}
                      <Button size="icon" variant="ghost" class="ml-2 text-white hover:bg-indigo-800/50 shadow-glow" @click="copyKey(key.key)">
                        <Copy class="h-4 w-4" />
                      </Button>
                    </TableCell>
                    <TableCell><Badge variant="outline" class="border-indigo-700/50 text-gray-200 shadow-glow">{{ key.status }}</Badge></TableCell>
                    <TableCell class="hidden md:table-cell text-gray-300">{{ new Date(key.created_at).toLocaleString() }}</TableCell>
                    <TableCell @click.stop>
                      <DropdownMenu>
                        <DropdownMenuTrigger as-child>
                          <Button aria-haspopup="true" size="icon" variant="ghost" class="text-white hover:bg-indigo-800/50 shadow-glow">
                            <MoreHorizontal class="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end" class="bg-gray-800/30 text-white border border-indigo-700/50 backdrop-blur-lg">
                          <DropdownMenuLabel>Actions</DropdownMenuLabel>
                          <DropdownMenuItem @click="deleteKey(key.id)" class="hover:bg-indigo-700/50">Delete</DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </CardContent>
            <CardFooter class="flex justify-between items-center text-xs text-gray-400">
              <div v-if="filteredKeys.length === 0">
                Showing 0-0 of 0 keys
              </div>
              <div v-else>
                Showing <strong>{{ (currentPage - 1) * itemsPerPage + 1 }}-{{ Math.min(currentPage * itemsPerPage, filteredKeys.length) }}</strong> of <strong>{{ filteredKeys.length }}</strong> keys
              </div>
              <div class="flex gap-2" v-if="totalPages > 1">
                <Button
                  size="sm"
                  variant="outline"
                  :disabled="currentPage === 1"
                  @click="goToPage(currentPage - 1)"
                  class="text-white border-indigo-700/50 hover:bg-indigo-800/50 transition-all duration-300 shadow-glow"
                >
                  Previous
                </Button>
                <Button
                  v-for="page in totalPages"
                  :key="page"
                  size="sm"
                  :variant="page === currentPage ? 'default' : 'outline'"
                  @click="goToPage(page)"
                  class="text-white border-indigo-700/50 hover:bg-indigo-800/50 transition-all duration-300 shadow-glow"
                >
                  {{ page }}
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  :disabled="currentPage === totalPages"
                  @click="goToPage(currentPage + 1)"
                  class="text-white border-indigo-700/50 hover:bg-indigo-800/50 transition-all duration-300 shadow-glow"
                >
                  Next
                </Button>
              </div>
            </CardFooter>
          </Card>
        </Tabs>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useAsyncData, useRuntimeConfig } from '#app'
import { apiFetch } from '~/utils/api'
import { CircleUser, Copy, Home, LineChart, MoreHorizontal, Package, PanelLeft, PlusCircle, Search, ShoppingCart, Users2, Key } from 'lucide-vue-next'
import { Icon } from '@iconify/vue'

const username = ref('Гость')
const activeTab = ref<'all' | 'Active' | 'Inactive'>('all')
const searchQuery = ref('')
const colorMode = ref('dark')
const currentPage = ref(1)
const itemsPerPage = 4
const isLoading = ref(false)
const config = useRuntimeConfig()
const API_BASE = config.public.NUXT_PUBLIC_API_URL

type KeyStatus = 'Active' | 'Inactive'

type ApiKey = {
  id: number
  key: string
  status: KeyStatus
  created_at: string
}

const apiKeys = ref<ApiKey[]>([])
const neuralMeshCanvas = ref(null)

function authCheck(): string {
  const token = localStorage.getItem('access_token')
  if (!token) throw new Error('NO_TOKEN')
  return token
}

async function fetchWithToken<T>(url: string, options: RequestInit = {}): Promise<T> {
  const token = authCheck()
  const res = await apiFetch(url, {
    ...options,
    headers: {
      Authorization: `Bearer ${token}`,
      ...(options.headers || {})
    }
  })
  return res
}

const { data: fetchedKeys, refresh } = await useAsyncData('api-keys', async () => {
  try {
    isLoading.value = true
    const res = await fetchWithToken<any[]>(`${API_BASE}/api/keys/list`)
    return res.map(key => ({
      id: Number(key.id),
      key: key.key || 'Unknown',
      status: key.status || 'Active',
      created_at: key.created_at
    }))
  } catch (err) {
    console.error('Ошибка при загрузке API ключей', err)
    return []
  } finally {
    isLoading.value = false
  }
}, { server: false })

watch(fetchedKeys, (newKeys) => {
  apiKeys.value = newKeys || []
})

const filteredKeys = computed(() =>
  apiKeys.value.filter(k =>
    k.key.toLowerCase().includes(searchQuery.value.toLowerCase()) &&
    (activeTab.value === 'all' || k.status === activeTab.value)
  )
)

const paginatedKeys = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredKeys.value.slice(start, start + itemsPerPage)
})

const totalPages = computed(() => Math.ceil(filteredKeys.value.length / itemsPerPage))

function changeTab(tab: typeof activeTab.value) {
  activeTab.value = tab
  currentPage.value = 1
}

function goToPage(page: number) {
  if (page >= 1 && page <= totalPages.value) currentPage.value = page
}

async function generateApiKey() {
  try {
    isLoading.value = true
    const res = await fetchWithToken<ApiKey>(`${API_BASE}/api/keys/create`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: 'Active' })
    })
    await refresh()
  } catch (err) {
    console.error('Ошибка при создании API ключа', err)
    alert('Ошибка при создании API ключа')
  } finally {
    isLoading.value = false
  }
}

async function deleteKey(keyId: number) {
  if (!confirm('Удалить API ключ?')) return
  try {
    isLoading.value = true
    await fetchWithToken(`${API_BASE}/api/keys/${keyId}`, { method: 'DELETE' })
    await refresh()
  } catch (err) {
    console.error('Ошибка при удалении API ключа', err)
    alert('Ошибка при удалении API ключа')
  } finally {
    isLoading.value = false
  }
}

async function copyKey(key: string) {
  try {
    await navigator.clipboard.writeText(key)
    alert('API ключ скопирован в буфер обмена')
  } catch (err) {
    console.error('Ошибка при копировании ключа', err)
    alert('Ошибка при копировании ключа')
  }
}

function showUnderDevelopment() {
  alert('Функция в разработке')
}

function logout() {
  showUnderDevelopment()
}

onMounted(() => {
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
    isHub: Math.random() < 0.1,
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

      ctx.fillStyle = node.isHub && Math.sin(time * 0.001 + node.pulseTime) > 0.5 ? 'rgba(192, 132, 252, 0.8)' : 'rgba(192, 132, 252, 0.5)'
      ctx.beginPath()
      ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2)
      ctx.fill()

      if (node.isHub && Math.sin(time * 0.001 + node.pulseTime) > 0.5) {
        ctx.strokeStyle = 'rgba(96, 165, 250, 0.3)'
        ctx.lineWidth = 1
        ctx.beginPath()
        ctx.arc(node.x, node.y, node.radius + (time % 5000) * 0.01, 0, Math.PI * 2)
        ctx.stroke()
      }

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

  onUnmounted(() => {
    window.removeEventListener('resize', resize)
  })

  const stored = localStorage.getItem('username')
  if (stored && stored !== 'undefined') username.value = stored
})

definePageMeta({ middleware: ['auth'] })
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

/* Bottom-left neural vortex animation */
.animate-neural-vortex .nodes {
  animation: spiral 10s linear infinite;
}
.animate-neural-vortex .node {
  animation: pulse 2s infinite ease-in-out;
}
.animate-neural-vortex .node-1 { animation-delay: 0s; }
.animate-neural-vortex .node-2 { animation-delay: 0.3s; }
.animate-neural-vortex .node-3 { animation-delay: 0.6s; }
.animate-neural-vortex .node-main { animation-delay: 0.9s; }
.animate-neural-vortex .connection {
  animation: connect 2s infinite ease-in-out;
}
.animate-neural-vortex .signal-pulse {
  animation: signal-pulse 5s infinite ease-in-out;
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

@keyframes spiral {
  0% { transform: rotate(0deg) translate(10px, 10px); }
  100% { transform: rotate(360deg) translate(10px, 10px); }
}

@keyframes signal-pulse {
  0%, 100% { transform: scale(1); opacity: 0.3; }
  50% { transform: scale(2); opacity: 0; }
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

/* Smooth transitions for interactive elements */
button, a, input, select {
  transition: all 0.3s ease;
}

/* Glow effect for interactive elements */
.shadow-glow {
  box-shadow: 0 0 10px rgba(79, 70, 229, 0.3);
}

/* Hover effects for table rows */
.quest-row {
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}
.quest-row:hover {
  background-color: #1e1b4b; /* Indigo-900 */
  transform: translateY(-2px);
}
</style>
```