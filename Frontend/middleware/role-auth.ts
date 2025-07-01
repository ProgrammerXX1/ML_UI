import { useUserStore } from '@/stores/user'
import { navigateTo } from '#app'

export default defineNuxtRouteMiddleware(async (to, from) => {
  // Пропускаем на сервере
  if (process.server) return

  const userStore = useUserStore()

  // // Если уже есть загружённый пользователь — сразу проверяем роль
  // if (userStore.username) {
  //   // Доступ к /generation только для coder/admin
  //   if (to.path === '/generation' && !['coder', 'admin'].includes(userStore.role)) {
  //     console.error('role-auth: доступ к /generation запрещён для', userStore.role)
  //     return navigateTo('/chat')
  //   }
  //   // Доступ к /admin-dashboard только для admin
  //   if (to.path === '/admin-dashboard' && userStore.role !== 'admin') {
  //     console.error('role-auth: доступ к /admin-dashboard запрещён для', userStore.role)
  //     return navigateTo('/chat')
  //   }
  //   return
  // }

  // Если пользователя ещё нет — подгружаем на клиенте
  if (import.meta.client) {
    userStore.loadFromLocalStorage()
    const token = localStorage.getItem('access_token')
    if (token) {
      try {
        await userStore.fetchUserData()
      } catch (err) {
        console.warn('role-auth: ошибка загрузки пользователя', err)
      }
    }
  }

  // После загрузки — ещё раз проверяем роль
  if (to.path === '/generation' && !['coder', 'admin'].includes(userStore.role)) {
    console.error('role-auth: доступ к /generation запрещён для', userStore.role)
    return navigateTo('/chat')
  }
  if (to.path === '/admin-dashboard' && userStore.role !== 'admin') {
    console.error('role-auth: доступ к /admin-dashboard запрещён для', userStore.role)
    return navigateTo('/chat')
  }
})
