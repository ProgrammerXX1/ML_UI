<template>
  <header class="w-full bg-[#1e1e1e] h-12 px-6 flex items-center justify-between border-b border-neutral-800">
    <!-- Logo -->
    <div class="flex items-center font-semibold text-xl tracking-tight">
      <span class="text-white">Au</span><span class="text-red-700">rus</span>
    </div>

    <!-- Right side -->
    <div class="flex items-center space-x-8">
      <!-- Navigation -->
      <nav class="flex items-center space-x-10 text-sm text-neutral-300">
        <NuxtLink to="/playground" class="hover:text-red-500" :class="{ 'text-red-700': route.path === '/' }">
          Playground
        </NuxtLink>
        <NuxtLink to="/api-keys" class="hover:text-red-500" :class="{ 'text-white-500': route.path === '/' }">
          API Keys
        </NuxtLink>
        <NuxtLink to="/dashboard" class="hover:text-red-500" :class="{ 'text-white-500': route.path === '/' }">
          Dashboard
        </NuxtLink>
        <NuxtLink to="/docs" class="hover:text-red-500" :class="{ 'text-white-500': route.path === '/' }">
          Docs
        </NuxtLink>
      </nav>

      <!-- Settings icon -->
      <Icon icon="lucide:settings" class="text-neutral-400 hover:text-white text-lg" />


      <!-- Profile -->
      <div class="flex items-center space-x-4 px-6 py-2 border border-neutral-600 rounded-full bg-[#2c2c2c]">
        <div class="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-xs font-bold">
          Б
        </div>
        <span class="text-sm text-white font-medium">Personal</span>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue'
const route = useRoute()
</script>

<style scoped>
</style>
