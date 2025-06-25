<script setup lang="ts">
import { ref, computed } from 'vue'
const username = ref('Гость')
onMounted(() => {
  const stored = localStorage.getItem('username')
  if (stored && stored.trim() && stored !== 'undefined') {
    username.value = stored
  }
})
function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('username')
  navigateTo('/login')
}
definePageMeta({
  middleware: ['auth'],
})

const searchQuery = ref('')
const activeTab = ref<'all' | 'Active' | 'Draft' | 'Archived'>('all')
// import {
//   Badge, Button, Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle,
//   DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger,
//   Input, Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator,
//   Sheet, SheetContent, SheetTrigger, Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
//   Tabs, TabsContent, TabsList, TabsTrigger, Tooltip, TooltipContent, TooltipProvider, TooltipTrigger
// } from '@/components/ui'

import {
  CircleUser, File, Home, LineChart, ListFilter, MoreHorizontal,
  Package, Package2, PanelLeft, PlusCircle, Search, Settings, ShoppingCart, Users2
} from 'lucide-vue-next'

import { Icon } from '@iconify/vue'

const colorMode = useColorMode()
const quests = [
  {
    id: 1,
    image: '/images/1.png',
    name: 'CHAT 1',
    status: 'Draft',
    token: 150,
    corrects: 25,
    created_at: '2023-07-12 10:42 AM',
  },
  {
    id: 2,
    image: '/images/1.png',
    name: 'CHAT 2',
    status: 'Active',
    token: 130,
    corrects: 100,
    created_at: '2023-10-18 03:21 PM',
  },
  {
    id: 2,
    image: '/images/1.png',
    name: 'CHAT 3',
    status: 'Arhived',
    token: 100,
    corrects: 90,
    created_at: '2025-2-18 03:21 PM',
  },
]
// 🔍 Фильтрация по поиску и вкладке
const filteredQuests = computed(() => {
  return quests.value.filter(q => {
    const matchesSearch = q.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesStatus = activeTab.value === 'all' || q.status === activeTab.value
    return matchesSearch && matchesStatus
  })
})
</script>
<template>
  <div class="flex min-h-screen w-full flex-col bg-gray-950 text-white">
    <!-- Sidebar -->
    <aside class="fixed inset-y-0 left-0 z-10 hidden w-14 flex-col border-r border-gray-800 bg-gray-900 sm:flex">
      <nav class="flex flex-col items-center gap-4 px-2 py-4">
        <a
          href="#"
          class="group flex h-9 w-9 shrink-0 items-center justify-center gap-2 rounded-full bg-blue-600 text-lg font-semibold text-white hover:bg-blue-700"
        >
          <Package2 class="h-4 w-4 transition-transform group-hover:scale-110" />
          <span class="sr-only">Acme Inc</span>
        </a>
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger as-child>
              <a
                href="#"
                class="flex h-9 w-9 items-center justify-center rounded-lg text-gray-400 transition hover:text-white"
              >
                <Home class="h-5 w-5" />
                <span class="sr-only">Dashboard</span>
              </a>
            </TooltipTrigger>
            <TooltipContent side="right">Dashboard</TooltipContent>
          </Tooltip>
        </TooltipProvider>
      </nav>
    </aside>

    <!-- Main layout -->
    <div class="flex flex-col sm:gap-4 sm:py-4 sm:pl-14">
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
              <a href="#" class="flex items-center gap-4 px-2.5 text-gray-400 hover:text-white">
                <Home class="h-5 w-5" /> Dashboard
              </a>
              <a href="#" class="flex items-center gap-4 px-2.5 text-gray-400 hover:text-white">
                <ShoppingCart class="h-5 w-5" /> Orders
              </a>
              <a href="#" class="flex items-center gap-4 px-2.5 text-white">
                <Package class="h-5 w-5" /> Quests
              </a>
              <a href="#" class="flex items-center gap-4 px-2.5 text-gray-400 hover:text-white">
                <Users2 class="h-5 w-5" /> Customers
              </a>
              <a href="#" class="flex items-center gap-4 px-2.5 text-gray-400 hover:text-white">
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
            <DropdownMenuLabel>Acc :{{username}}</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem>Settings</DropdownMenuItem>
            <DropdownMenuItem>Support</DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="logout">Logout</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </header>

        <main class="grid flex-1 items-start gap-4 p-4 sm:px-6 md:gap-8">
          <Tabs default-value="all">
            <div class="flex items-center">
          <TabsList>
            <TabsTrigger value="all" @click="activeTab = 'all'">All</TabsTrigger>
            <TabsTrigger value="active" @click="activeTab = 'active'">Active</TabsTrigger>
            <TabsTrigger value="draft" @click="activeTab = 'draft'">Draft</TabsTrigger>
            <TabsTrigger value="archived" @click="activeTab = 'archived'" class="hidden sm:flex">Archived</TabsTrigger>
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
                  <DropdownMenuItem checked>Active</DropdownMenuItem>
                  <DropdownMenuItem>Draft</DropdownMenuItem>
                  <DropdownMenuItem>Archived</DropdownMenuItem>
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

          <TabsContent value="all">
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
                  <TableBody>
                    <TableRow v-for="quest in quests" :key="quest.id">
                      <TableCell class="hidden sm:table-cell">
                        <img :src="quest.image" alt="Quest" class="rounded-md object-cover" width="64" height="64" />
                      </TableCell>
                      <TableCell class="font-medium">{{ quest.name }}</TableCell>
                      <TableCell><Badge variant="outline">{{ quest.status }}</Badge></TableCell>
                      <TableCell class="hidden md:table-cell">{{ quest.token }}</TableCell>
                      <TableCell class="hidden md:table-cell">{{ quest.corrects }}</TableCell>
                      <TableCell class="hidden md:table-cell">{{ quest.created_at }}</TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger as-child>
                            <Button aria-haspopup="true" size="icon" variant="ghost" class="text-white">
                              <MoreHorizontal class="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end" class="bg-gray-800 text-white border border-gray-700">
                            <DropdownMenuLabel>Actions</DropdownMenuLabel>
                            <DropdownMenuItem>Edit</DropdownMenuItem>
                            <DropdownMenuItem>Delete</DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </CardContent>
              <CardFooter class="text-xs text-gray-400">
                Showing <strong>1–10</strong> of <strong>32</strong> quests
              </CardFooter>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  </div>
</template>