```vue
<template>
  <div>
    <!-- Desktop Sidebar -->
    <aside class="fixed inset-y-0 left-0 z-20 w-64 flex-col border-r border-indigo-700/50 bg-gray-900/30 backdrop-blur-lg hidden sm:flex">
      <nav class="flex flex-col gap-6 px-4 py-6 text-lg font-medium">
        <NuxtLink
          to="/"
          class="group flex items-center justify-center h-12 w-full rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 text-white transition-all duration-300 hover:from-blue-500 hover:to-purple-500 shadow-glow"
        >
          <span class="ml-2 text-sm font-semibold animate-flicker">NeuralNet AI</span>
        </NuxtLink>
        <NuxtLink
          to="/chat"
          class="flex items-center gap-4 px-2.5 text-gray-300 hover:text-white hover:bg-indigo-800/50 rounded-lg py-2 transition-all duration-200 shadow-glow"
          :class="{ 'text-white bg-indigo-700/50': $route.path === '/chat' }"
        >
          <Package class="h-5 w-5" /> Chats
        </NuxtLink>
        <NuxtLink
          v-if="['coder', 'admin'].includes(role)"
          to="/generation"
          class="flex items-center gap-4 px-2.5 text-gray-300 hover:text-white hover:bg-indigo-800/50 rounded-lg py-2 transition-all duration-200 shadow-glow"
          :class="{ 'text-white bg-indigo-700/50': $route.path === '/generation' }"
        >
          <Key class="h-5 w-5" /> API Keys
        </NuxtLink>
        <NuxtLink
          v-if="role === 'admin'"
          to="/admin-dashboard"
          class="flex items-center gap-4 px-2.5 text-gray-300 hover:text-white hover:bg-indigo-800/50 rounded-lg py-2 transition-all duration-200 shadow-glow"
          :class="{ 'text-white bg-indigo-700/50': $route.path === '/admin-dashboard' }"
        >
          <LineChart class="h-5 w-5" /> Admin Dashboard
        </NuxtLink>
      </nav>
    </aside>
    <!-- Mobile Menu -->
    <Sheet>
      <SheetTrigger as-child>
        <Button size="icon" variant="outline" class="sm:hidden text-white border-indigo-700 hover:bg-indigo-800/50 shadow-glow">
          <PanelLeft class="h-5 w-5" />
          <span class="sr-only">Toggle Menu</span>
        </Button>
      </SheetTrigger>
      <SheetContent side="left" class="sm:max-w-xs bg-gray-900/30 text-white border-indigo-700/50 backdrop-blur-lg">
        <nav class="grid gap-6 text-lg font-medium">
          <NuxtLink
            to="/"
            class="group flex items-center justify-start h-12 rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 text-white transition-all duration-300 hover:from-blue-500 hover:to-purple-500 shadow-glow"
          >
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
          <NuxtLink
            to="/chat"
            class="flex items-center gap-4 px-2.5 text-gray-300 hover:text-white hover:bg-indigo-800/50 rounded-lg py-2 transition-all duration-200 shadow-glow"
            :class="{ 'text-white bg-indigo-700/50': $route.path === '/chat' }"
          >
            <Package class="h-5 w-5" /> Chats
          </NuxtLink>
          <NuxtLink
            v-if="['coder', 'admin'].includes(role)"
            to="/generation"
            class="flex items-center gap-4 px-2.5 text-gray-300 hover:text-white hover:bg-indigo-800/50 rounded-lg py-2 transition-all duration-200 shadow-glow"
            :class="{ 'text-white bg-indigo-700/50': $route.path === '/generation' }"
          >
            <Key class="h-5 w-5" /> API Keys
          </NuxtLink>
          <NuxtLink
            v-if="role === 'admin'"
            to="/admin-dashboard"
            class="flex items-center gap-4 px-2.5 text-gray-300 hover:text-white hover:bg-indigo-800/50 rounded-lg py-2 transition-all duration-200 shadow-glow"
            :class="{ 'text-white bg-indigo-700/50': $route.path === '/admin-dashboard' }"
          >
            <LineChart class="h-5 w-5" /> Admin Dashboard
          </NuxtLink>
        </nav>
      </SheetContent>
    </Sheet>
  </div>
</template>

<script setup lang="ts">
import { Package, Key, LineChart, PanelLeft } from 'lucide-vue-next'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const role = computed(() => userStore.role)
</script>
```