```vue
<template>
  <main class="grid flex-1 items-start gap-4 p-4 sm:px-6 md:gap-8">
    <Tabs v-model="activeTab">
      <div class="flex items-center">
        <TabsList class="bg-gray-800/20 border border-indigo-700/50 rounded-lg">
          <TabsTrigger value="all" @click="changeTab('all')" class="hover:bg-indigo-700/50 transition-all duration-300">All</TabsTrigger>
          <TabsTrigger value="Active" @click="changeTab('Active')" class="hover:bg-indigo-700/50 transition-all duration-300">Active</TabsTrigger>
          <TabsTrigger value="Draft" @click="changeTab('Draft')" class="hover:bg-indigo-700/50 transition-all duration-300">Draft</TabsTrigger>
          <TabsTrigger value="Archived" @click="changeTab('Archived')" class="hidden sm:flex hover:bg-indigo-700/50 transition-all duration-300">Archived</TabsTrigger>
        </TabsList>
        <div class="ml-auto flex items-center gap-2">
          <DropdownMenu>
            <DropdownMenuTrigger as-child>
              <Button variant="outline" size="sm" class="h-7 gap-1 text-white border-indigo-700/50 hover:bg-indigo-800/50 transition-all duration-300 shadow-glow">
                <ListFilter class="h-4 w-4" />
                <span class="sr-only sm:not-sr-only">Filter</span>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" class="bg-gray-800/30 text-white border border-indigo-700/50 backdrop-blur-lg">
              <DropdownMenuLabel>Filter by</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem @click="changeTab('Active')" class="hover:bg-indigo-700/50">Active</DropdownMenuItem>
              <DropdownMenuItem @click="changeTab('Draft')" class="hover:bg-indigo-700/50">Draft</DropdownMenuItem>
              <DropdownMenuItem @click="changeTab('Archived')" class="hover:bg-indigo-700/50">Archived</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
          <Button size="sm" variant="outline" class="h-7 gap-1 text-white border-indigo-700/50 hover:bg-indigo-800/50 transition-all duration-300 shadow-glow">
            <File class="h-4 w-4" />
            <span class="sr-only sm:not-sr-only">Export</span>
          </Button>
          <Button
            size="sm"
            class="h-7 gap-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white transition-all duration-300 shadow-glow"
            @click="emit('createChat')"
          >
            <PlusCircle class="h-4 w-4" />
            <span class="sr-only sm:not-sr-only">Add Chat</span>
          </Button>
        </div>
      </div>
      <Card class="bg-gray-900/30 border border-indigo-700/50 text-white shadow-xl rounded-xl backdrop-blur-lg">
        <CardHeader>
          <CardTitle class="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent animate-flicker">Chats</CardTitle>
          <CardDescription class="text-gray-300 animate-glow-text">Manage your AI-driven conversations.</CardDescription>
        </CardHeader>
        <CardContent>
          <div v-if="isLoading">
            <p class="text-gray-300 animate-pulse">Загрузка...</p>
          </div>
          <div v-else-if="!chats.length">
            <p class="text-gray-300">Чаты не найдены. Попробуйте создать новый чат.</p>
          </div>
          <Table v-else>
            <TableHeader>
              <TableRow class="border-b border-indigo-700/50">
                <TableHead class="hidden w-[100px] sm:table-cell"><span class="sr-only">img</span></TableHead>
                <TableHead class="text-gray-300 animate-glow-text">Name</TableHead>
                <TableHead class="text-gray-300 animate-glow-text">Status</TableHead>
                <TableHead class="hidden md:table-cell text-gray-300 animate-glow-text">Created at</TableHead>
                <TableHead><span class="sr-only">Actions</span></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody class="max-h-[400px] overflow-y-auto">
              <TableRow
                v-for="chat in paginatedChats"
                :key="chat.id"
                @click="emit('chatClick', chat.id)"
                class="quest-row"
              >
                <TableCell class="hidden sm:table-cell">
                  <img
                    :src="chat.image"
                    alt="Chat"
                    class="rounded-md object-cover transform hover:scale-105 transition-transform duration-200"
                    width="64"
                    height="64"
                    @error="chat.image = '/images/chat-2.png'"
                  />
                </TableCell>
                <TableCell class="font-medium text-gray-200">{{ chat.name }}</TableCell>
                <TableCell><Badge variant="outline" class="border-indigo-700/50 text-gray-200 shadow-glow">{{ chat.status }}</Badge></TableCell>
                <TableCell class="hidden md:table-cell text-gray-300">{{ new Date(chat.created_at).toLocaleString() }}</TableCell>
                <TableCell @click.stop>
                  <DropdownMenu>
                    <DropdownMenuTrigger as-child>
                      <Button aria-haspopup="true" size="icon" variant="ghost" class="text-white hover:bg-indigo-800/50 shadow-glow">
                        <MoreHorizontal class="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end" class="bg-gray-800/30 text-white border border-indigo-700/50 backdrop-blur-lg">
                      <DropdownMenuLabel>Actions</DropdownMenuLabel>
                      <DropdownMenuItem @click="emit('editChat', chat); menuOpen = false" class="hover:bg-indigo-700/50">Edit</DropdownMenuItem>
                      <DropdownMenuItem @click="emit('deleteChat', chat.id); menuOpen = false" class="hover:bg-indigo-700/50">Delete</DropdownMenuItem>
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
</template>
<script setup lang="ts">
import { ref, computed } from 'vue'
import { File, ListFilter, MoreHorizontal, PlusCircle } from 'lucide-vue-next'

const props = defineProps<{
  chats: Chat[]
  isLoading: boolean
}>()
const menuOpen = ref(false)
const emit = defineEmits<{
  (e: 'chatClick', id: number): void
  (e: 'editChat', chat: Chat): void
  (e: 'deleteChat', id: number): void
  (e: 'createChat'): void
}>()

type ChatStatus = 'Active' | 'Draft' | 'Archived'
type Chat = {
  id: number
  name: string
  status: ChatStatus
  created_at: string
  image?: string
}

const activeTab = ref<ChatStatus | 'all'>('all')
const currentPage = ref(1)
const itemsPerPage = 4
const searchQuery = ref('')

// ✅ chats используется через props.chats
const filteredChats = computed(() =>
  props.chats.filter(c =>
    c.name.toLowerCase().includes(searchQuery.value.toLowerCase()) &&
    (activeTab.value === 'all' || c.status === activeTab.value)
  )
)

const paginatedChats = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredChats.value.slice(start, start + itemsPerPage)
})

const totalPages = computed(() => Math.ceil(filteredChats.value.length / itemsPerPage))

const changeTab = (tab: ChatStatus | 'all') => {
  activeTab.value = tab
  currentPage.value = 1
}

const goToPage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) currentPage.value = page
}
</script>
