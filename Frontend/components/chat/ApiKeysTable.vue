<template>
  <main class="grid flex-1 items-start gap-4 p-4 sm:px-6 md:gap-8">
    <Tabs v-model="activeTab">
      <div class="flex flex-wrap items-center gap-4">
        <TabsList class="bg-gray-800/20 border border-indigo-700/50 rounded-lg">
          <TabsTrigger value="all" @click="changeTab('all')">All</TabsTrigger>
          <TabsTrigger value="Active" @click="changeTab('Active')">Active</TabsTrigger>
          <TabsTrigger value="Revoked" @click="changeTab('Revoked')">Revoked</TabsTrigger>
        </TabsList>

        <input
          v-model="searchQuery"
          placeholder="Search by key…"
          class="bg-gray-800/50 border border-indigo-700/50 text-white rounded-lg px-3 py-1 focus:ring-2 focus:ring-indigo-500"
        />

        <div class="ml-auto">
          <Button size="sm" @click="emit('createKey')">
            <PlusCircle class="h-4 w-4" /> Add API Key
          </Button>
        </div>
      </div>

      <Card class="bg-gray-900/30 border border-indigo-700/50 text-white shadow-xl rounded-xl backdrop-blur-lg">
        <CardHeader>
          <CardTitle>API Keys</CardTitle>
          <CardDescription>Manage your API keys.</CardDescription>
        </CardHeader>
        <CardContent>
          <div v-if="isLoading">
            <p class="animate-pulse">Loading…</p>
          </div>
          <div v-else-if="!filteredKeys.length">
            <p>No keys found.</p>
          </div>
          <Table v-else>
            <TableHeader>
              <TableRow>
                <TableHead>Key</TableHead>
                <TableHead>Status</TableHead>
                <TableHead class="hidden md:table-cell">Created at</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody class="max-h-[400px] overflow-y-auto">
              <TableRow v-for="k in paginatedKeys" :key="k.id">
                <TableCell>{{ k.key }}</TableCell>
                <TableCell>{{ k.status }}</TableCell>
                <TableCell class="hidden md:table-cell">{{ new Date(k.created_at).toLocaleString() }}</TableCell>
                <TableCell>
                  <Button size="icon" variant="ghost" @click="emit('deleteKey', k.id)">
                    <Trash2 class="h-4 w-4" />
                  </Button>
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </CardContent>
        <CardFooter class="flex justify-between items-center text-xs text-gray-400">
          <div v-if="filteredKeys.length">
            Showing
            {{ (currentPage-1)*itemsPerPage + 1 }}-
            {{ Math.min(currentPage*itemsPerPage, filteredKeys.length) }}
            of {{ filteredKeys.length }}
          </div>
          <div class="flex gap-2" v-if="totalPages>1">
            <Button size="sm" :disabled="currentPage===1" @click="goToPage(currentPage-1)">Prev</Button>
            <Button
              v-for="p in totalPages"
              :key="p"
              size="sm"
              :variant="p===currentPage?'default':'outline'"
              @click="goToPage(p)"
            >{{ p }}</Button>
            <Button size="sm" :disabled="currentPage===totalPages" @click="goToPage(currentPage+1)">Next</Button>
          </div>
        </CardFooter>
      </Card>
    </Tabs>
  </main>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { PlusCircle, Trash2 } from 'lucide-vue-next'

interface ApiKey {
  id: number
  key: string
  status: 'Active' | 'Revoked'
  created_at: string
}

const props = defineProps<{
  keys: ApiKey[]
  isLoading: boolean
}>()

const emit = defineEmits<{
  (e: 'createKey'): void
  (e: 'deleteKey', id: number): void
}>()

const activeTab = ref<'all' | 'Active' | 'Revoked'>('all')
const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = 4

const filteredKeys = computed(() =>
  props.keys.filter(k =>
    k.key.toLowerCase().includes(searchQuery.value.toLowerCase())
    && (activeTab.value === 'all' || k.status === activeTab.value)
  )
)

const totalPages = computed(() => Math.ceil(filteredKeys.value.length / itemsPerPage))

const paginatedKeys = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredKeys.value.slice(start, start + itemsPerPage)
})

function changeTab(tab: typeof activeTab.value) {
  activeTab.value = tab
  currentPage.value = 1
}

function goToPage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}
</script>
