import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref(localStorage.getItem('vueuse-color-scheme') === 'dark')

  const toggleDark = () => {
    isDark.value = !isDark.value
    localStorage.setItem('vueuse-color-scheme', isDark.value ? 'dark' : 'light')

    if (isDark.value) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  // Initialize theme on load
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  }

  return { isDark, toggleDark }
})
