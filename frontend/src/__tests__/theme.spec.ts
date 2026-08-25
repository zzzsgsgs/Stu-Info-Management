import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useThemeStore } from '../stores/theme'

describe('Theme Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    document.documentElement.className = ''
  })

  it('initializes dark mode from localStorage', () => {
    localStorage.setItem('vueuse-color-scheme', 'dark')
    const themeStore = useThemeStore()
    expect(themeStore.isDark).toBe(true)
    expect(document.documentElement.classList.contains('dark')).toBe(true)
  })

  it('toggles dark mode', () => {
    const themeStore = useThemeStore()
    expect(themeStore.isDark).toBe(false)

    themeStore.toggleDark()

    expect(themeStore.isDark).toBe(true)
    expect(localStorage.getItem('vueuse-color-scheme')).toBe('dark')
    expect(document.documentElement.classList.contains('dark')).toBe(true)

    themeStore.toggleDark()

    expect(themeStore.isDark).toBe(false)
    expect(localStorage.getItem('vueuse-color-scheme')).toBe('light')
    expect(document.documentElement.classList.contains('dark')).toBe(false)
  })
})
