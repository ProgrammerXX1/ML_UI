import { useUserStore } from '@/stores/user'

export default defineNuxtRouteMiddleware((to) => {
  const userStore = useUserStore()
  const role = userStore.role

  if (to.path === '/api-keys' && !['coder', 'admin'].includes(role)) {
    return navigateTo('/chat')
  }
  if (to.path === '/admin-dashboard' && role !== 'admin') {
    return navigateTo('/chat')
  }
})