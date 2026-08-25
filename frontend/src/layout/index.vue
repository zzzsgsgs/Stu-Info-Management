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
  <el-container class="layout-container">
    <el-aside width="200px" class="aside">
      <div class="logo">学生信息管理系统</div>
      <el-menu
        :default-active="route.path"
        router
        class="el-menu-vertical"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
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
    <el-container>
      <el-header class="header">
        <div class="header-right">
          <el-switch
            v-model="themeStore.isDark"
            inline-prompt
            active-text="暗"
            inactive-text="亮"
            @change="themeStore.toggleDark"
            style="margin-right: 20px"
          />
          <el-dropdown trigger="click">
            <span class="el-dropdown-link userinfo">
              {{ authStore.username || 'Admin' }}
              <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="authStore.logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main>
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
.layout-container {
  height: 100vh;
}
.aside {
  background-color: var(--el-bg-color-overlay);
  border-right: 1px solid var(--el-border-color-light);
}
.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: var(--el-text-color-primary);
  font-size: 18px;
  font-weight: bold;
  border-bottom: 1px solid var(--el-border-color-light);
}
.el-menu-vertical {
  border-right: none;
}
.header {
  background-color: var(--el-bg-color);
  border-bottom: 1px solid var(--el-border-color-light);
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 20px;
}
.userinfo {
  cursor: pointer;
  display: flex;
  align-items: center;
  color: var(--el-text-color-regular);
}
/* transition */
.fade-transform-leave-active,
.fade-transform-enter-active {
  transition: all .3s;
}
.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}
.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
