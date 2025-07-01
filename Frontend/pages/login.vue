
<template>
  <div class="flex min-h-screen w-full flex-col bg-gradient-to-br from-gray-950 via-indigo-950 to-purple-950 text-white relative overflow-hidden">
    <NeuralMesh />
    <div class="flex flex-1 items-center justify-center p-4">
      <Card class="w-full max-w-md bg-gray-900/30 border border-indigo-700/50 shadow-xl rounded-xl backdrop-blur-lg">
        <CardHeader>
          <CardTitle class="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent animate-flicker">Login to NeuralNet AI</CardTitle>
          <CardDescription class="text-gray-300 animate-glow-text">Enter your credentials to access your account.</CardDescription>
        </CardHeader>
        <CardContent>
          <div class="grid gap-4">
            <div class="grid gap-2">
              <label for="username" class="text-gray-300 animate-glow-text">Username</label>
              <Input
                id="username"
                v-model="username"
                placeholder="Enter your username"
                class="bg-gray-800/20 text-white border-indigo-700/50 focus:border-purple-500 transition-all duration-300 shadow-glow"
              />
            </div>
            <div class="grid gap-2">
              <label for="password" class="text-gray-300 animate-glow-text">Password</label>
              <Input
                id="password"
                v-model="password"
                type="password"
                placeholder="Enter your password"
                class="bg-gray-800/20 text-white border-indigo-700/50 focus:border-purple-500 transition-all duration-300 shadow-glow"
              />
            </div>
            <Button
              :disabled="isLoading"
              class="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white transition-all duration-300 shadow-glow"
              @click="login"
            >
              <span v-if="isLoading" class="animate-pulse">Logging in...</span>
              <span v-else>Login</span>
            </Button>
            <div class="text-center text-sm text-gray-300">
              Don't have an account? <NuxtLink to="/register" class="text-blue-400 hover:text-blue-300 transition-colors">Register</NuxtLink>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { navigateTo } from '#app'
import { useUserStore } from '@/stores/user'
import { apiFetch } from '~/utils/api'

const userStore = useUserStore()
const username = ref('')
const password = ref('')
const isLoading = ref(false)

async function login() {
  if (!username.value || !password.value) {
    alert('Пожалуйста, заполните все поля')
    return
  }

  isLoading.value = true
  try {
    const params = new URLSearchParams()
    params.append('username', username.value)
    params.append('password', password.value)

    const response = await apiFetch('/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: params
    })

    localStorage.setItem('access_token', response.access_token)
    await userStore.fetchUserData()
    navigateTo('/chat')
  } catch (err) {
    console.error('login: Ошибка авторизации:', err)
    alert('Ошибка авторизации')
  } finally {
    isLoading.value = false
  }
}


</script>
