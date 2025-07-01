<template>
  <div class="flex min-h-screen w-full flex-col bg-gradient-to-br from-gray-950 via-indigo-950 to-purple-950 text-white">
    <Sidebar />
    <div class="flex flex-col sm:gap-4 sm:py-4 sm:pl-64">
      <Header :page-title="route.meta.pageTitle ?? 'NeuralNet Platform'">
        <template #mobileMenu>
          <Sidebar />
        </template>
      </Header>
      <main class="grid flex-1 items-start gap-4 p-4 sm:px-6 md:gap-8">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import Sidebar from '@/components/layout/Sidebar.vue'
import Header from '@/components/layout/Header.vue'
const route = useRoute()
</script>
