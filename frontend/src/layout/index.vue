<script setup lang="ts">
import { useAuthStore } from '../stores/auth'
import { useThemeStore } from '../stores/theme'
import { useRoute } from 'vue-router'
import { onMounted } from 'vue'

const authStore = useAuthStore()
const themeStore = useThemeStore()
const route = useRoute()

onMounted(() => {
  authStore.fetchUserInfo()
})
</script>

<template>
  <el-container class="layout-container bg-gray-50 dark:bg-[#141414]">
    <el-aside width="220px" class="aside relative shadow-xl z-20 backdrop-blur-md bg-white/90 dark:bg-gray-900/90 border-r border-gray-200 dark:border-gray-800 transition-all duration-300">
      <div class="logo flex items-center justify-center h-16 border-b border-gray-100 dark:border-gray-800">
        <el-icon class="text-primary text-2xl mr-2"><Monitor /></el-icon>
        <span class="font-bold text-gray-800 dark:text-gray-200 text-lg tracking-wide">Stu-Info Sys</span>
      </div>
      <el-menu
        :default-active="route.path"
        router
        class="el-menu-vertical border-none bg-transparent mt-4"
      >
        <el-menu-item index="/">
          <el-icon><DataLine /></el-icon>
          <span>Dashboard</span>
        </el-menu-item>
        <el-menu-item index="/students">
          <el-icon><User /></el-icon>
          <span>学生管理</span>
        </el-menu-item>
        <el-menu-item index="/courses">
          <el-icon><Reading /></el-icon>
          <span>课程管理</span>
        </el-menu-item>
        <el-menu-item index="/audit-logs">
          <el-icon><List /></el-icon>
          <span>审计日志</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container class="flex flex-col h-full overflow-hidden">
      <el-header class="header h-16 flex items-center justify-between px-6 bg-white dark:bg-[#1d1e1f] border-b border-gray-200 dark:border-gray-800 shadow-sm z-10">
        <!-- Breadcrumb -->
        <div class="breadcrumb flex items-center text-sm text-gray-500 dark:text-gray-400">
          <el-icon class="mr-2 text-lg"><Guide /></el-icon>
          <span class="font-medium tracking-wide">
            {{ route.name ? route.name.toString().charAt(0).toUpperCase() + route.name.toString().slice(1) : 'Dashboard' }}
          </span>
        </div>

        <div class="header-right flex items-center space-x-6">
          <el-switch
            v-model="themeStore.isDark"
            inline-prompt
            active-text="暗"
            inactive-text="亮"
            @change="themeStore.toggleDark"
            style="margin-right: 20px"
          />
          <el-dropdown trigger="click" class="cursor-pointer">
            <div class="flex items-center space-x-2 group hover:bg-gray-100 dark:hover:bg-gray-800 py-1 px-3 rounded-full transition-colors duration-200">
              <el-avatar :size="32" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" />
              <span class="font-medium text-gray-700 dark:text-gray-300 group-hover:text-primary transition-colors">
                {{ authStore.username || 'Admin' }}
              </span>
              <el-icon class="text-gray-400"><arrow-down /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu class="w-32">
                <el-dropdown-item icon="SwitchButton" @click="authStore.logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="bg-gray-50 dark:bg-[#141414] p-6 overflow-y-auto">
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
/* Scoped styles kept minimal due to Tailwind usage */
.el-menu-item {
  margin: 0 8px;
  border-radius: 8px;
  margin-bottom: 4px;
  transition: all 0.2s;
}
.el-menu-item.is-active {
  background-color: rgba(64, 158, 255, 0.1);
  font-weight: bold;
}
</style>
