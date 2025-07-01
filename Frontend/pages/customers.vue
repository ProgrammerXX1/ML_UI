
<template>
  <div class="flex min-h-screen w-full flex-col bg-gradient-to-br from-gray-950 via-indigo-950 to-purple-950 text-white relative overflow-hidden">
    <NeuralMesh />
    <NeuralVortex />
    <Sidebar />
    <div class="flex flex-col sm:gap-4 sm:py-4 sm:pl-64">
      <Header page-title="Customers">
        <template #mobileMenu>
          <Sidebar />
        </template>
      </Header>
      <main class="grid flex-1 items-start gap-4 p-4 sm:px-6 md:gap-8">
        <Card class="bg-gray-900/30 border border-indigo-700/50 text-white shadow-xl rounded-xl backdrop-blur-lg">
          <CardHeader>
            <CardTitle class="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent animate-flicker">Customers</CardTitle>
            <CardDescription class="text-gray-300 animate-glow-text">Manage your customers.</CardDescription>
          </CardHeader>
          <CardContent>
            <p class="text-gray-300">В разработке...</p>
          </CardContent>
        </Card>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

onMounted(async () => {
  userStore.init()
  userStore.loadFromLocalStorage()
  if (localStorage.getItem('access_token')) {
    await userStore.fetchUserData()
  }
})

definePageMeta({ middleware: ['auth', 'role-auth'] })
</script>
