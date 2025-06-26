<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useColorMode } from '@vueuse/core'
import { useAsyncData } from '#imports'
import { apiFetch } from '@/utils/api'
import {
  CircleUser, File, Home, LineChart, ListFilter, MoreHorizontal,
  Package, Package2, PanelLeft, PlusCircle, Search, Settings, ShoppingCart, Users2
} from 'lucide-vue-next'
import { Icon } from '@iconify/vue'

const router = useRouter()
const username = ref('Гость')
const colorMode = useColorMode()
const activeTab = ref<'all' | 'Active' | 'Draft' | 'Archived'>('all')
const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = 4
const isLoading = ref(false)

// Модалка для редактирования
const isEditModalOpen = ref(false)
const editingChat = ref<null | {
  id: number
  name: string
  status: 'Active' | 'Draft' | 'Archived'
  created_at: string
  image?: string
}>(null)

// Данные чатов с отслеживанием кликов
const chats = ref<any[]>([])
const clickCounts = ref<{ [key: number]: number }>({})
const lastClickTime = ref<{ [key: number]: number }>({})

// Загрузка данных
const { data: fetchedChats, pending: isInitialLoading, refresh } = await useAsyncData('chats', async () => {
  if (process.server) return []
  isLoading.value = true
  try {
    const token = localStorage.getItem('access_token')
    console.log(`[${new Date().toISOString()}] Токен:`, token)
    if (!token) {
      console.log(`[${new Date().toISOString()}] Токен отсутствует, редирект на /auth/login`)
      await navigateTo('/auth/login')
      return []
    }
    console.log(`[${new Date().toISOString()}] Отправляем запрос на /chat/list`)
    const res = await apiFetch('/chat/list', {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` }
    })
    console.log(`[${new Date().toISOString()}] Ответ от /chat/list:`, res)
    if (!Array.isArray(res)) {
      console.error(`[${new Date().toISOString()}] /chat/list вернул не массив:`, res)
      return []
    }
    return res.map(chat => {
      const id = Number(chat.id)
      if (isNaN(id)) {
        console.warn(`Некорректный id для чата:`, chat)
        return null
      }
      return {
        id,
        name: chat.title || 'Без названия',
        status: chat.status || 'Draft',
        created_at: chat.created_at || new Date().toISOString(),
        image: '/images/chat-2.png'
      }
    }).filter(chat => chat !== null)
  } catch (err) {
    console.error(`[${new Date().toISOString()}] Не удалось загрузить чаты:`, err)
    return []
  } finally {
    isLoading.value = false
  }
}, { server: false })

// Синхронизация данных
watch(fetchedChats, (newChats) => {
  chats.value = newChats || []
  clickCounts.value = {}
  lastClickTime.value = {}
})

const filteredChats = computed(() => {
  return chats.value.filter(c => {
    const matchesSearch = (c.name || '').toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesStatus = activeTab.value === 'all' || c.status === activeTab.value
    return matchesSearch && matchesStatus
  })
})

const paginatedChats = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredChats.value.slice(start, end)
})

const totalPages = computed(() => Math.ceil((filteredChats.value?.length || 0) / itemsPerPage))

function changeTab(tab: 'all' | 'Active' | 'Draft' | 'Archived') {
  activeTab.value = tab
  currentPage.value = 1
}

async function handleChatClick(chatId: number) {
  console.log('Получен chatId для клика:', chatId)
  const now = Date.now()
  const lastClick = lastClickTime.value[chatId] || 0
  const doubleClickThreshold = 300

  if (now - lastClick < doubleClickThreshold) {
    await goToChat(chatId)
    clickCounts.value[chatId] = 0
    lastClickTime.value[chatId] = 0
  } else {
    clickCounts.value[chatId] = 1
  }
  lastClickTime.value[chatId] = now
}

async function goToChat(chatId: number) {
  if (process.server || !Number.isInteger(chatId) || chatId <= 0) {
    console.error(`Некорректный chatId: ${chatId}`)
    alert('Некорректный идентификатор чата')
    return
  }
  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      await navigateTo('/auth/login')
      return
    }
    console.log(`[${new Date().toISOString()}] Запрос на /chat/${chatId}`)
    const res = await apiFetch(`/chat/${chatId}`, {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` }
    })
    if (!res || !res.id) {
      throw new Error('Чат не найден')
    }
    console.log(`[${new Date().toISOString()}] Переход на /chat/${chatId}`)
    await router.push(`/chat/${chatId}`)
  } catch (err) {
    console.error(`[${new Date().toISOString()}] Ошибка при переходе в чат ${chatId}:`, err)
    alert('Не удалось открыть чат: ' + (err.message || 'Чат не найден'))
  }
}

async function createChat() {
  if (process.server) return
  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      await navigateTo('/auth/login')
      return
    }
    isLoading.value = true
    const res = await apiFetch('/chat/create', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: `Новый чат ${new Date().toISOString()}`, status: 'Draft' })
    })
    await refresh() // Обновляем данные через useAsyncData
    await router.push(`/chat/${res.id}`)
  } catch (err) {
    console.error(`[${new Date().toISOString()}] Не удалось создать чат:`, err)
    alert('Ошибка при создании чата')
  } finally {
    isLoading.value = false
  }
}

async function saveQuest() {
  if (process.server || !editingChat.value) return
  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      await navigateTo('/auth/login')
      return
    }
    isLoading.value = true
    const res = await apiFetch(`/chat/${editingChat.value.id}`, {
      method: 'PATCH',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: editingChat.value.name, status: editingChat.value.status })
    })
    await refresh() // Обновляем данные
  } catch (err) {
    console.error(`[${new Date().toISOString()}] Не удалось обновить чат ${editingChat.value?.id || 'unknown'}:`, err)
    alert('Ошибка при сохранении чата')
  } finally {
    isEditModalOpen.value = false
    editingChat.value = null
    isLoading.value = false
  }
}

async function deleteQuest(chatId: number) {
  if (process.server) return
  if (confirm('Вы точно хотите удалить этот чат?')) {
    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        await navigateTo('/auth/login')
        return
      }
      isLoading.value = true
      const res = await apiFetch(`/chat/${chatId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
      })
      if (res.status === 204 || res.ok) {
        await refresh() // Обновляем данные
        if (filteredChats.value.length === 0 && currentPage.value > 1) {
          currentPage.value = Math.max(1, currentPage.value - 1)
        }
      } else {
        const errorText = await res.text().catch(() => 'Неизвестная ошибка')
        throw new Error(`HTTP error! Status: ${res.status}, Detail: ${errorText}`)
      }
    } catch (err) {
      console.error(`[${new Date().toISOString()}] Ошибка при удалении чата ${chatId}:`, err)
      alert(`Ошибка при удалении чата: ${err.message || 'Неизвестная ошибка'}`)
    } finally {
      isLoading.value = false
    }
  }
}

async function sendMessage(chatId: number | null, message: string) {
  if (process.server || !message.trim()) return
  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      await navigateTo('/auth/login')
      return
    }
    isLoading.value = true
    const res = await apiFetch('/chat', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, title: chatId ? undefined : `Новый чат ${new Date().toISOString()}`, chat_id: chatId })
    })
    await refresh() // Обновляем данные
    if (!chatId) {
      await router.push(`/chat/${res.chat_id}`)
    }
  } catch (err) {
    console.error(`[${new Date().toISOString()}] Не удалось отправить сообщение:`, err)
    alert('Ошибка при отправке сообщения')
  } finally {
    isLoading.value = false
  }
}

function goToPage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

function showUnderDevelopment() {
  alert('Эти части еще находятся в разработке. Пожалуйста, вернитесь позже')
}

function logout() {
  if (process.server) return
  localStorage.removeItem('access_token')
  localStorage.removeItem('username')
  navigateTo('/auth/login')
}

function openEditModal(chat: typeof chats.value[0]) {
  editingChat.value = { ...chat }
  isEditModalOpen.value = true
}

onMounted(async () => {
  if (process.server) return
  const stored = localStorage.getItem('username')
  if (stored && stored.trim() && stored !== 'undefined') {
    username.value = stored
  }
  await refresh() // Выполняем начальную загрузку
})

definePageMeta({
  middleware: ['auth'],
})
</script>
<template>
  <div class="flex min-h-screen w-full flex-col bg-gray-900 text-white">
    <!-- Sidebar (десктоп) -->
    <aside class="fixed inset-y-0 left-0 z-10 w-64 flex-col border-r border-gray-800 bg-gray-900 hidden sm:flex">
      <nav class="flex flex-col gap-6 px-4 py-4 text-lg font-medium">
        <a href="#" class="group flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-white">
          <Package2 class="h-5 w-5 group-hover:scale-110 transition" />
          <span class="sr-only">Acme Inc</span>
        </a>
        <a href="#" class="flex items-center gap-4 px-2.5 text-gray-400 hover:text-white" @click="showUnderDevelopment">
          <Home class="h-5 w-5" /> Dashboard
        </a>
        <a href="#" class="flex items-center gap-4 px-2.5 text-gray-400 hover:text-white" @click="showUnderDevelopment">
          <ShoppingCart class="h-5 w-5" /> Orders
        </a>
        <a href="#" class="flex items-center gap-4 px-2.5 text-white">
          <Package class="h-5 w-5" /> Chats
        </a>
        <a href="#" class="flex items-center gap-4 px-2.5 text-gray-400 hover:text-white" @click="showUnderDevelopment">
          <Users2 class="h-5 w-5" /> Customers
        </a>
        <a href="#" class="flex items-center gap-4 px-2.5 text-gray-400 hover:text-white" @click="showUnderDevelopment">
          <LineChart class="h-5 w-5" /> Settings
        </a>
      </nav>
    </aside>
    <!-- Main layout -->
    <div class="flex flex-col sm:gap-4 sm:py-4 sm:pl-64">
      <header class="sticky top-0 z-30 flex h-14 items-center gap-4 border-b border-gray-800 bg-gray-900 px-4 sm:px-6">
        <Sheet>
          <SheetTrigger as-child>
            <Button size="icon" variant="outline" class="sm:hidden text-white border-gray-700 hover:bg-gray-800">
              <PanelLeft class="h-5 w-5" />
              <span class="sr-only">Toggle Menu</span>
            </Button>
          </SheetTrigger>
          <SheetContent side="left" class="sm:max-w-xs bg-gray-900 text-white border-gray-800">
            <nav class="grid gap-6 text-lg font-medium">
              <a href="#" class="group flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-white">
                <Package2 class="h-5 w-5 group-hover:scale-110 transition" />
              </a>
              <a href="#" class="flex items-center gap-4 px-2.5 text-gray-400 hover:text-white" @click="showUnderDevelopment">
                <Home class="h-5 w-5" /> Dashboard
              </a>
              <a href="#" class="flex items-center gap-4 px-2.5 text-gray-400 hover:text-white" @click="showUnderDevelopment">
                <ShoppingCart class="h-5 w-5" /> Orders
              </a>
              <a href="#" class="flex items-center gap-4 px-2.5 text-white">
                <Package class="h-5 w-5" /> Chats
              </a>
              <a href="#" class="flex items-center gap-4 px-2.5 text-gray-400 hover:text-white" @click="showUnderDevelopment">
                <Users2 class="h-5 w-5" /> Customers
              </a>
              <a href="#" class="flex items-center gap-4 px-2.5 text-gray-400 hover:text-white" @click="showUnderDevelopment">
                <LineChart class="h-5 w-5" /> Settings
              </a>
            </nav>
          </SheetContent>
        </Sheet>
        <!-- Breadcrumb -->
        <Breadcrumb class="hidden md:flex text-gray-400">
          <BreadcrumbList>
            <BreadcrumbItem>
              <BreadcrumbLink as-child><a href="#">Dashboard</a></BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem>
              <BreadcrumbLink as-child><a href="#">Chats</a></BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbPage>All Chats</BreadcrumbPage></BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>
        <!-- Search bar -->
        <div class="relative ml-auto flex-1 md:grow-0">
          <Search class="absolute left-2.5 top-2.5 h-4 w-4 text-gray-500" />
          <Input
            v-model="searchQuery"
            type="search"
            placeholder="Search..."
            class="w-full rounded-lg bg-gray-800 text-white placeholder-gray-500 pl-8 border border-gray-700 md:w-[200px] lg:w-[320px]"
          />
        </div>
        <!-- Theme switch -->
        <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <Button variant="outline" class="text-white border-gray-700 hover:bg-gray-800">
              <Icon icon="radix-icons:moon" class="h-5 w-5 dark:hidden" />
              <Icon icon="radix-icons:sun" class="h-5 w-5 hidden dark:block" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" class="bg-gray-800 text-white border border-gray-700">
            <DropdownMenuItem @click="colorMode.preference = 'light'">Light</DropdownMenuItem>
            <DropdownMenuItem @click="colorMode.preference = 'dark'">Dark</DropdownMenuItem>
            <DropdownMenuItem @click="colorMode.preference = 'system'">System</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
        <!-- Profile -->
        <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <Button variant="secondary" size="icon" class="rounded-full bg-gray-700 hover:bg-gray-600">
              <CircleUser class="h-5 w-5 text-white" />
              <span class="sr-only">Toggle user menu</span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" class="bg-gray-800 text-white border border-gray-700">
            <DropdownMenuLabel>Acc: {{ username }}</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="showUnderDevelopment">Settings</DropdownMenuItem>
            <DropdownMenuItem @click="showUnderDevelopment">Support</DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="logout">Logout</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </header>
      <main class="grid flex-1 items-start gap-4 p-4 sm:px-6 md:gap-8">
        <Tabs v-model="activeTab">
          <div class="flex items-center">
            <TabsList>
              <TabsTrigger value="all" @click="changeTab('all')">All</TabsTrigger>
              <TabsTrigger value="Active" @click="changeTab('Active')">Active</TabsTrigger>
              <TabsTrigger value="Draft" @click="changeTab('Draft')">Draft</TabsTrigger>
              <TabsTrigger value="Archived" @click="changeTab('Archived')" class="hidden sm:flex">Archived</TabsTrigger>
            </TabsList>
            <div class="ml-auto flex items-center gap-2">
              <DropdownMenu>
                <DropdownMenuTrigger as-child>
                  <Button variant="outline" size="sm" class="h-7 gap-1 text-white border-gray-700 hover:bg-gray-800">
                    <ListFilter class="h-4 w-4" />
                    <span class="sr-only sm:not-sr-only">Filter</span>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" class="bg-gray-800 text-white border border-gray-700">
                  <DropdownMenuLabel>Filter by</DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem @click="changeTab('Active')">Active</DropdownMenuItem>
                  <DropdownMenuItem @click="changeTab('Draft')">Draft</DropdownMenuItem>
                  <DropdownMenuItem @click="changeTab('Archived')">Archived</DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
              <Button size="sm" variant="outline" class="h-7 gap-1 text-white border-gray-700 hover:bg-gray-800">
                <File class="h-4 w-4" />
                <span class="sr-only sm:not-sr-only">Export</span>
              </Button>
              <Button size="sm" class="h-7 gap-1 bg-blue-600 hover:bg-blue-700 text-white" @click="createChat">
                <PlusCircle class="h-4 w-4" />
                <span class="sr-only sm:not-sr-only">Add Chat</span>
              </Button>
            </div>
          </div>
          <Card class="bg-gray-900 border border-gray-800 text-white shadow-lg rounded-lg">
            <CardHeader>
              <CardTitle>Chats</CardTitle>
              <CardDescription>Manage your chats.</CardDescription>
            </CardHeader>
            <CardContent>
              <div v-if="isLoading">
                <p>Загрузка...</p>
              </div>
              <div v-else-if="!chats.length">
                <p>Чаты не найдены. Попробуйте создать новый чат.</p>
              </div>
              <Table v-else>
                <TableHeader>
                  <TableRow>
                    <TableHead class="hidden w-[100px] sm:table-cell"><span class="sr-only">img</span></TableHead>
                    <TableHead>Name</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead class="hidden md:table-cell">Created at</TableHead>
                    <TableHead><span class="sr-only">Actions</span></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody class="max-h-[400px] overflow-y-auto">
                  <TableRow
                    v-for="chat in paginatedChats"
                    :key="chat.id"
                    @click="handleChatClick(chat.id)"
                    class="quest-row"
                  >
                    <TableCell class="hidden sm:table-cell">
                      <img
                        :src="chat.image"
                        alt="Chat"
                        class="rounded-md object-cover"
                        width="64"
                        height="64"
                        @error="chat.image = '/images/chat-2.png'"
                      />
                    </TableCell>
                    <TableCell class="font-medium">{{ chat.name }}</TableCell>
                    <TableCell><Badge variant="outline">{{ chat.status }}</Badge></TableCell>
                    <TableCell class="hidden md:table-cell">{{ new Date(chat.created_at).toLocaleString() }}</TableCell>
                    <TableCell @click.stop>
                      <DropdownMenu>
                        <DropdownMenuTrigger as-child>
                          <Button aria-haspopup="true" size="icon" variant="ghost" class="text-white">
                            <MoreHorizontal class="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end" class="bg-gray-800 text-white border border-gray-700">
                          <DropdownMenuLabel>Actions</DropdownMenuLabel>
                          <DropdownMenuItem @click="openEditModal(chat)">Edit</DropdownMenuItem>
                          <DropdownMenuItem @click="deleteQuest(chat.id)">Delete</DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </CardContent>
            <CardFooter class="flex justify-between items-center text-xs text-gray-400">
              <div v-if="filteredChats.length === 0">
                Showing 0-0 of 0 chats
              </div>
              <div v-else>
                Showing <strong>{{ (currentPage - 1) * itemsPerPage + 1 }}-{{ Math.min(currentPage * itemsPerPage, filteredChats.length) }}</strong> of <strong>{{ filteredChats.length }}</strong> chats
              </div>
              <div class="flex gap-2" v-if="totalPages > 1">
                <Button
                  size="sm"
                  variant="outline"
                  :disabled="currentPage === 1"
                  @click="goToPage(currentPage - 1)"
                  class="text-white border-gray-700"
                >
                  Previous
                </Button>
                <Button
                  v-for="page in totalPages"
                  :key="page"
                  size="sm"
                  :variant="page === currentPage ? 'default' : 'outline'"
                  @click="goToPage(page)"
                  class="text-white border-gray-700"
                >
                  {{ page }}
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  :disabled="currentPage === totalPages"
                  @click="goToPage(currentPage + 1)"
                  class="text-white border-gray-700"
                >
                  Next
                </Button>
              </div>
            </CardFooter>
          </Card>
        </Tabs>
        <!-- Модалка для редактирования -->
        <Sheet v-model:open="isEditModalOpen">
          <SheetContent class="bg-gray-900 text-white border-gray-800">
            <div class="grid gap-4 py-4" v-if="editingChat">
              <h2 class="text-lg font-semibold">Edit Chat</h2>
              <div class="grid gap-2">
                <label for="name">Name</label>
                <Input
                  id="name"
                  v-model="editingChat.name"
                  class="bg-gray-800 text-white border-gray-700"
                />
                <label for="status">Status</label>
                <select
                  id="status"
                  v-model="editingChat.status"
                  class="bg-gray-800 text-white border-gray-700 rounded-md p-2"
                >
                  <option value="Active">Active</option>
                  <option value="Draft">Draft</option>
                  <option value="Archived">Archived</option>
                </select>
              </div>
              <Button
                class="bg-blue-600 hover:bg-blue-700 text-white"
                @click="saveQuest"
              >
                Save
              </Button>
            </div>
            <div v-else>
              <p>Ошибка: данные чата недоступны</p>
            </div>
          </SheetContent>
        </Sheet>
      </main>
    </div>
  </div>
</template>

<style scoped>
.quest-row {
  cursor: pointer;
  transition: background-color 0.2s;
}
.quest-row:hover {
  background-color: #1f2937; /* Tailwind gray-700 */
}
</style>