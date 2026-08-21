import { defineStore } from 'pinia'
import { ref } from 'vue'
import request from '../utils/request'
import router from '../router'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const username = ref(localStorage.getItem('username') || '')

  const setToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const setUsername = (newUsername: string) => {
    username.value = newUsername
    localStorage.setItem('username', newUsername)
  }

  const logout = () => {
    token.value = ''
    username.value = ''
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    router.push('/login')
  }

  const fetchUserInfo = async () => {
    if (token.value) {
      try {
        const res: any = await request.get('/users/me/')
        setUsername(res.username)
      } catch (error) {
        logout()
      }
    }
  }

  return { token, username, setToken, setUsername, logout, fetchUserInfo }
})
