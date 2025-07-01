<template>
  <div class="flex min-h-screen w-full flex-col bg-gradient-to-br from-gray-950 via-indigo-950 to-purple-950 text-white relative overflow-hidden">
    <NeuralMesh />
    <NeuralVortex />
    <Sidebar />
    
    <div class="flex flex-col sm:gap-4 sm:py-4 sm:pl-64">
      <Header
  :breadcrumbs="[
    { label: 'Menu', to: '/chat' },
    { label: 'Admin-DashBoard' }
  ]"
>
        <template #mobileMenu>
          <Sidebar />
        </template>
      </Header>

      
    </div>
  </div>
</template>

<script setup lang="ts">
// 🔧 Компоненты
import Header from '@/components/layout/Header.vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import NeuralMesh from '@/components/layout/NeuralMesh.vue'
import NeuralVortex from '@/components/chat/NeuralVortex.vue'
</script>