import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../stores/auth'
import router from '../router'

const service = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 5000
})

service.interceptors.request.use(
  config => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers['Authorization'] = `Bearer ${authStore.token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

service.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    let message = '请求失败'
    if (error.response) {
      if (error.response.status === 401) {
        message = '认证失败，请重新登录'
        const authStore = useAuthStore()
        authStore.logout()
        router.push('/login')
      } else {
        message = error.response.data?.detail || `Error code: ${error.response.status}`
      }
    }
    ElMessage({
      message: message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
