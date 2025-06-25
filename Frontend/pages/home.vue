<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useColorMode } from '@vueuse/core'
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

// Модалка для редактирования
const isEditModalOpen = ref(false)
const editingQuest = ref<null | {
  id: number
  image: string
  name: string
  status: 'Active' | 'Draft' | 'Archived'
  token: number
  corrects: number
  created_at: string
}>(null)

// Данные квестов
const quests = ref([
  { id: 1, image: '/images/1.png', name: 'CHAT 1', status: 'Draft', token: 150, corrects: 25, created_at: '2023-07-12 10:42 AM' },
  { id: 2, image: '/images/1.png', name: 'CHAT 2', status: 'Active', token: 130, corrects: 100, created_at: '2023-10-18 03:21 PM' },
  { id: 3, image: '/images/1.png', name: 'CHAT 3', status: 'Archived', token: 100, corrects: 90, created_at: '2025-02-18 03:21 PM' },
  { id: 4, image: '/images/1.png', name: 'CHAT 4', status: 'Draft', token: 170, corrects: 40, created_at: '2024-01-10 11:00 AM' },
  { id: 5, image: '/images/1.png', name: 'CHAT 5', status: 'Active', token: 190, corrects: 130, created_at: '2024-03-02 01:30 PM' },
  { id: 6, image: '/images/1.png', name: 'CHAT 6', status: 'Archived', token: 110, corrects: 55, created_at: '2022-11-22 04:10 PM' },
  { id: 7, image: '/images/1.png', name: 'CHAT 7', status: 'Draft', token: 140, corrects: 10, created_at: '2023-05-06 08:20 AM' },
  { id: 8, image: '/images/1.png', name: 'CHAT 8', status: 'Active', token: 200, corrects: 145, created_at: '2024-07-15 06:45 PM' },
  { id: 9, image: '/images/1.png', name: 'CHAT 9', status: 'Archived', token: 120, corrects: 60, created_at: '2021-09-30 12:00 PM' },
  { id: 10, image: '/images/1.png', name: 'CHAT 10', status: 'Draft', token: 155, corrects: 35, created_at: '2023-08-12 09:50 AM' },
  { id: 11, image: '/images/1.png', name: 'CHAT 11', status: 'Active', token: 160, corrects: 120, created_at: '2024-10-05 03:40 PM' },
  { id: 12, image: '/images/1.png', name: 'CHAT 12', status: 'Archived', token: 95, corrects: 80, created_at: '2023-03-25 05:15 PM' },
  { id: 13, image: '/images/1.png', name: 'CHAT 13', status: 'Draft', token: 135, corrects: 15, created_at: '2024-12-11 10:10 AM' },
  { id: 14, image: '/images/1.png', name: 'CHAT 14', status: 'Active', token: 180, corrects: 110, created_at: '2025-01-21 02:25 PM' },
  { id: 15, image: '/images/1.png', name: 'CHAT 15', status: 'Archived', token: 105, corrects: 70, created_at: '2022-06-18 11:35 AM' },
])
const filteredQuests = computed(() => {
  return quests.value.filter((q) => {
    const matchesSearch = q.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesStatus = activeTab.value === 'all' || q.status === activeTab.value
    return matchesSearch && matchesStatus
  })
})
const paginatedQuests = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredQuests.value.slice(start, end)
})
const totalPages = computed(() => {
  return Math.ceil(filteredQuests.value.length / itemsPerPage)
})
function changeTab(tab: 'all' | 'Active' | 'Draft' | 'Archived') {
  activeTab.value = tab
  currentPage.value = 1
}
function goToQuest(questId: number) {
  router.push({ name: 'QuestDetails', params: { id: questId } })
}
function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('username')
  navigateTo('/login')
}
function openEditModal(quest: typeof quests.value[0]) {
  editingQuest.value = { ...quest }
  isEditModalOpen.value = true
}
function saveQuest() {
  if (editingQuest.value) {
    const index = quests.value.findIndex((q) => q.id === editingQuest.value!.id)
    if (index !== -1) {
      quests.value[index] = { ...editingQuest.value }
    }
    isEditModalOpen.value = false
    editingQuest.value = null
  }
}
function deleteQuest(questId: number) {
  if (confirm('Are you sure you want to delete this quest?')) {
    quests.value = quests.value.filter((q) => q.id !== questId)
  }
}
function goToPage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}
// Уведомление "Ещё в разработке"
function showUnderDevelopment() {
  alert('This feature is still under development.')
}
onMounted(() => {
  const stored = localStorage.getItem('username')
  if (stored && stored.trim() && stored !== 'undefined') {
    username.value = stored
  }
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
          <Package class="h-5 w-5" /> Quests
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
                <Package class="h-5 w-5" /> Quests
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
              <BreadcrumbLink as-child><a href="#">Quests</a></BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem><BreadcrumbPage>All Quests</BreadcrumbPage></BreadcrumbItem>
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
              <NuxtLink to="/chat">
                <Button size="sm" class="h-7 gap-1 bg-blue-600 hover:bg-blue-700 text-white">
                  <PlusCircle class="h-4 w-4" />
                  <span class="sr-only sm:not-sr-only">Chat/Add Quest</span>
                </Button>
              </NuxtLink>
            </div>
          </div>
          <Card class="bg-gray-900 border border-gray-800 text-white shadow-lg rounded-lg">
            <CardHeader>
              <CardTitle>Quests</CardTitle>
              <CardDescription>Manage your quests and view their performance optimization.</CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead class="hidden w-[100px] sm:table-cell"><span class="sr-only">img</span></TableHead>
                    <TableHead>Name</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead class="hidden md:table-cell">Token</TableHead>
                    <TableHead class="hidden md:table-cell">Corrects</TableHead>
                    <TableHead class="hidden md:table-cell">Created at</TableHead>
                    <TableHead><span class="sr-only">Actions</span></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody class="max-h-[400px] overflow-y-auto">
                  <TableRow
                    v-for="quest in paginatedQuests"
                    :key="quest.id"
                    @click="goToQuest(quest.id)"
                    class="quest-row"
                  >
                    <TableCell class="hidden sm:table-cell">
                      <img
                        :src="quest.image"
                        alt="Quest"
                        class="rounded-md object-cover"
                        width="64"
                        height="64"
                      />
                    </TableCell>
                    <TableCell class="font-medium">{{ quest.name }}</TableCell>
                    <TableCell><Badge variant="outline">{{ quest.status }}</Badge></TableCell>
                    <TableCell class="hidden md:table-cell">{{ quest.token }}</TableCell>
                    <TableCell class="hidden md:table-cell">{{ quest.corrects }}</TableCell>
                    <TableCell class="hidden md:table-cell">{{ quest.created_at }}</TableCell>
                    <TableCell @click.stop>
                      <DropdownMenu>
                        <DropdownMenuTrigger as-child>
                          <Button aria-haspopup="true" size="icon" variant="ghost" class="text-white">
                            <MoreHorizontal class="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end" class="bg-gray-800 text-white border border-gray-700">
                          <DropdownMenuLabel>Actions</DropdownMenuLabel>
                          <DropdownMenuItem @click="openEditModal(quest)">Edit</DropdownMenuItem>
                          <DropdownMenuItem @click="deleteQuest(quest.id)">Delete</DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </CardContent>
            <CardFooter class="flex justify-between items-center text-xs text-gray-400">
              <div>
                Showing <strong>{{ (currentPage - 1) * itemsPerPage + 1 }}-{{ Math.min(currentPage * itemsPerPage, filteredQuests.length) }}</strong> of <strong>{{ filteredQuests.length }}</strong> quests
              </div>
              <div class="flex gap-2">
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
            <div class="grid gap-4 py-4">
              <h2 class="text-lg font-semibold">Edit Quest</h2>
              <div class="grid gap-2">
                <label for="name">Name</label>
                <Input
                  id="name"
                  v-model="editingQuest.name"
                  class="bg-gray-800 text-white border-gray-700"
                />
              </div>
              <div class="grid gap-2">
                <label for="status">Status</label>
                <select
                  id="status"
                  v-model="editingQuest.status"
                  class="bg-gray-800 text-white border-gray-700 rounded-lg p-2"
                >
                  <option value="Active">Active</option>
                  <option value="Draft">Draft</option>
                  <option value="Archived">Archived</option>
                </select>
              </div>
              <div class="grid gap-2">
                <label for="token">Token</label>
                <Input
                  id="token"
                  type="number"
                  v-model.number="editingQuest.token"
                  class="bg-gray-800 text-white border-gray-700"
                />
              </div>
              <div class="grid gap-2">
                <label for="corrects">Corrects</label>
                <Input
                  id="corrects"
                  type="number"
                  v-model.number="editingQuest.corrects"
                  class="bg-gray-800 text-white border-gray-700"
                />
              </div>
              <Button
                class="bg-blue-600 hover:bg-blue-700 text-white"
                @click="saveQuest"
              >
                Save
              </Button>
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