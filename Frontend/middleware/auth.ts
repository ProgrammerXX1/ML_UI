import { apiFetch } from '~/utils/api'
import { navigateTo } from '#app'

export default defineNuxtRouteMiddleware(async (to, from) => {
  // Если выполняемся на сервере — ничего не делаем
  if (process.server) return

  const token = localStorage.getItem('access_token')
  if (!token) {
    console.error('auth middleware: токен отсутствует')
    return navigateTo('/login')
  }

  try {
    // Проверяем, что токен валиден
    await apiFetch('/jwt-protected', {
      headers: { Authorization: `Bearer ${token}` }
    })

    // Дополнительно для всех /chat* проверяем доступ
    if (to.path.startsWith('/chat')) {
      await apiFetch('/chat', {
        headers: { Authorization: `Bearer ${token}` }
      })
    }
  } catch (err) {
    console.error('auth middleware: ошибка проверки токена', err)
    return navigateTo('/login')
  }
})
