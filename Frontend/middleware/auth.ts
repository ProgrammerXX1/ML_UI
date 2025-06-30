export default defineNuxtRouteMiddleware((to, from) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token')

    // ❌ Если токена нет — редирект на login
    if (!token && to.path !== '/login') {
      return navigateTo('/login')
    }

    // ✅ Если вошёл и попал на /api_keys сразу после логина — редирект на /
    if (token && to.path === '/api_keys' && from.path === '/login') {
      return navigateTo('/')
    }
  }
})
