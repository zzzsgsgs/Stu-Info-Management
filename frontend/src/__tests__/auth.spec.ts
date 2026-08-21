import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '../stores/auth'

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('sets token and saves to localStorage', () => {
    const authStore = useAuthStore()
    expect(authStore.token).toBe('')

    authStore.setToken('test-token')
    expect(authStore.token).toBe('test-token')
    expect(localStorage.getItem('token')).toBe('test-token')
  })

  it('sets username and saves to localStorage', () => {
    const authStore = useAuthStore()
    expect(authStore.username).toBe('')

    authStore.setUsername('testuser')
    expect(authStore.username).toBe('testuser')
    expect(localStorage.getItem('username')).toBe('testuser')
  })
})
