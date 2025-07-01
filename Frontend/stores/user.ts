import { defineStore } from 'pinia'
import { ref } from 'vue'
import { apiFetch } from '~/utils/api'

export const useUserStore = defineStore('user', () => {
  const username = ref<string>('Гость')
  const role = ref<string>('user')

  // Загрузка данных из localStorage
  function loadFromLocalStorage() {
    const storedUsername = localStorage.getItem('username')
    const storedRole = localStorage.getItem('role')
    console.log('loadFromLocalStorage: username:', storedUsername, 'role:', storedRole)
    if (storedUsername && storedUsername !== 'undefined') {
      username.value = storedUsername
    }
    if (storedRole && ['user', 'coder', 'admin'].includes(storedRole)) {
      role.value = storedRole
    }
  }

  // Запрос актуальных данных с сервера
  async function fetchUserData() {
    try {
      const token = localStorage.getItem('access_token')
      if (!token) {
        console.error('fetchUserData: Токен отсутствует')
        throw new Error('NO_TOKEN')
      }
      console.log('fetchUserData: Запрашиваем /user/profile с токеном:', token)
      const userData = await apiFetch('/jwt-protected', {
        headers: { Authorization: `Bearer ${token}` }
      })
      console.log('fetchUserData: Ответ сервера:', userData)
      username.value = userData.username || 'Гость'
      role.value = userData.role || 'user'
      localStorage.setItem('username', username.value)
      localStorage.setItem('role', role.value)
      console.log('fetchUserData: Установлены username:', username.value, 'role:', role.value)
    } catch (err) {
      console.error('fetchUserData: Ошибка:', err)
    }
  }

  // Сброс состояния
  function reset() {
    username.value = 'Гость'
    role.value = 'user'
    localStorage.removeItem('username')
    localStorage.removeItem('role')
    localStorage.removeItem('access_token')
    console.log('reset: Сброшено состояние пользователя')
  }

  // Ручная установка роли (для отладки)
  function setRole(newRole: string) {
    if (['user', 'coder', 'admin'].includes(newRole)) {
      role.value = newRole
      localStorage.setItem('role', newRole)
      console.log('setRole: Установлена роль:', newRole)
    } else {
      console.error('setRole: Неверная роль:', newRole)
    }
  }

  // Инициализация: при создании стора загрузить из localStorage и обновить с сервера
  async function init() {
    loadFromLocalStorage()
    if (localStorage.getItem('access_token')) {
      await fetchUserData()
    }
  }

  // Вызови init() где-то в точке входа приложения (например, в app.vue или layout)

  return { username, role, fetchUserData, loadFromLocalStorage, reset, setRole, init }
})
