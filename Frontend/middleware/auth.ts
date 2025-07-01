import { defineNuxtRouteMiddleware } from '#app'
import { useUserStore } from '@/stores/user'

export default defineNuxtRouteMiddleware((to) => {
  const userStore = useUserStore()
  const role = userStore.role
  console.log('role-auth: Проверка роли:', role, 'для пути:', to.path)

  if (to.path === '/api-keys' && !['coder', 'admin'].includes(role)) {
    console.log('role-auth: Доступ к /api-keys запрещен, перенаправление на /chat')
    return navigateTo('/chat')
  }
  if (to.path === '/admin-dashboard' && role !== 'admin') {
    console.log('role-auth: Доступ к /admin-dashboard запрещен, перенаправление на /chat')
    return navigateTo('/chat')
  }
})