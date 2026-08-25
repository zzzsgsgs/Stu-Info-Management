import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '../stores/auth'
import router from '../router'

const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
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
  async error => {
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

    // Simple retry mechanism for 5xx errors or network errors
    const config = error.config;
    if (!config || !config.retry) {
       config.retry = 0;
    }

    if (config.retry < 2 && (!error.response || error.response.status >= 500)) {
        config.retry += 1;
        console.warn(`Retrying request... (${config.retry})`);
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(service(config));
            }, 1000 * config.retry); // exponential backoff
        });
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
