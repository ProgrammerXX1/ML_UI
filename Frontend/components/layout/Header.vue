<template>
  <header class="sticky top-0 z-30 flex h-14 items-center gap-4 border-b border-indigo-700/50 bg-gray-900/30 backdrop-blur-lg px-4 sm:px-6">
    <slot name="mobile-menu" />

    <!-- Dynamic Breadcrumb -->
    <Breadcrumb class="hidden md:flex text-gray-300 animate-glow-text">
      <BreadcrumbList>
        <BreadcrumbItem v-for="(crumb, index) in breadcrumbs" :key="index">
          <BreadcrumbLink v-if="crumb.to" as-child>
            <NuxtLink :to="crumb.to" class="hover:text-white transition-colors">
              {{ crumb.label }}
            </NuxtLink>
          </BreadcrumbLink>
          <BreadcrumbPage v-else>
            {{ crumb.label }}
          </BreadcrumbPage>
          <BreadcrumbSeparator v-if="index < breadcrumbs.length - 1" />
        </BreadcrumbItem>
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
        <DropdownMenuItem @click="colorMode.preference = 'light'" class="hover:bg-indigo-700/50">Light</DropdownMenuItem>
        <DropdownMenuItem @click="colorMode.preference = 'dark'" class="hover:bg-indigo-700/50">Dark</DropdownMenuItem>
        <DropdownMenuItem @click="colorMode.preference = 'system'" class="hover:bg-indigo-700/50">System</DropdownMenuItem>
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
        <DropdownMenuLabel>Role: {{ role }}</DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem @click="showUnderDevelopment" class="hover:bg-indigo-700/50">Settings</DropdownMenuItem>
        <DropdownMenuItem @click="showUnderDevelopment" class="hover:bg-indigo-700/50">Support</DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem @click="logout" class="hover:bg-indigo-700/50">Logout</DropdownMenuItem>
        <DropdownMenuItem v-if="role === 'user'" @click="setRole('admin')" class="hover:bg-indigo-700/50">Set Role to Admin (Debug)</DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useColorMode } from '@vueuse/core'
import { useUserStore } from '@/stores/user'
import { CircleUser, Search } from 'lucide-vue-next'
import { Icon } from '@iconify/vue'
import { navigateTo } from '#app'

defineProps<{
  breadcrumbs: { label: string; to?: string }[]
}>()

const userStore = useUserStore()
const role = computed(() => userStore.role)
const colorMode = useColorMode()
const searchQuery = ref('')

const logout = () => {
  userStore.reset()
  navigateTo('/login')
}

const showUnderDevelopment = () => {
  alert('Функция в разработке')
}

const setRole = (newRole: string) => {
  userStore.setRole(newRole)
}
</script>
