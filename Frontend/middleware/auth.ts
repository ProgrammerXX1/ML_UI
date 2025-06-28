export default defineNuxtRouteMiddleware(() => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token')
    if (!token) {
      return navigateTo('/login')
    }
  }
})
