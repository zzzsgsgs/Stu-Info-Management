<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import request from '../utils/request'
import * as echarts from 'echarts'

const stats = ref({
  total_students: 0,
  gender_ratio: { male: 0, female: 0 },
  average_gpa: 0,
  major_distribution: [] as { name: string, value: number }[]
})

const loading = ref(true)
let genderChart: echarts.ECharts | null = null
let majorChart: echarts.ECharts | null = null
const genderChartRef = ref<HTMLElement>()
const majorChartRef = ref<HTMLElement>()

const fetchData = async () => {
  try {
    const res: any = await request.get('/dashboard/')
    stats.value = res
    initCharts()
  } finally {
    loading.value = false
  }
}

const initCharts = () => {
  if (genderChartRef.value) {
    genderChart = echarts.init(genderChartRef.value)
    genderChart.setOption({
      title: { text: '性别比例', left: 'center' },
      tooltip: { trigger: 'item' },
      legend: { orient: 'vertical', left: 'left' },
      series: [
        {
          name: '性别',
          type: 'pie',
          radius: '50%',
          data: [
            { value: stats.value.gender_ratio.male, name: '男' },
            { value: stats.value.gender_ratio.female, name: '女' }
          ],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    })
  }

  if (majorChartRef.value) {
    majorChart = echarts.init(majorChartRef.value)
    majorChart.setOption({
      title: { text: '各专业人数分布', left: 'center' },
      tooltip: { trigger: 'axis' },
      xAxis: {
        type: 'category',
        data: stats.value.major_distribution.map(item => item.name),
        axisLabel: { interval: 0, rotate: 30 }
      },
      yAxis: { type: 'value' },
      series: [
        {
          data: stats.value.major_distribution.map(item => item.value),
          type: 'bar',
          itemStyle: { color: '#409EFF' }
        }
      ]
    })
  }
}

const handleResize = () => {
  genderChart?.resize()
  majorChart?.resize()
}

onMounted(() => {
  fetchData()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  genderChart?.dispose()
  majorChart?.dispose()
})
</script>

<template>
  <div v-loading="loading" class="h-full flex flex-col gap-6">
    <!-- Stat Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="bg-white dark:bg-[#1d1e1f] rounded-2xl p-6 border border-gray-100 dark:border-gray-800 card-shadow flex items-center justify-between">
        <div>
          <p class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">总学生人数</p>
          <h3 class="text-3xl font-bold text-gray-900 dark:text-gray-100">{{ stats.total_students }}</h3>
        </div>
        <div class="p-3 bg-blue-50 dark:bg-blue-900/30 rounded-xl text-blue-500">
          <el-icon class="text-2xl"><UserFilled /></el-icon>
        </div>
      </div>

      <div class="bg-white dark:bg-[#1d1e1f] rounded-2xl p-6 border border-gray-100 dark:border-gray-800 card-shadow flex items-center justify-between">
        <div>
          <p class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">平均 GPA</p>
          <div class="flex items-baseline gap-2">
            <h3 class="text-3xl font-bold text-gray-900 dark:text-gray-100">{{ stats.average_gpa }}</h3>
            <span class="text-xs font-medium text-green-500 bg-green-50 dark:bg-green-900/30 px-2 py-0.5 rounded-full flex items-center">
              <el-icon><TopRight /></el-icon> 稳定
            </span>
          </div>
        </div>
        <div class="p-3 bg-green-50 dark:bg-green-900/30 rounded-xl text-green-500">
          <el-icon class="text-2xl"><DataLine /></el-icon>
        </div>
      </div>

      <!-- Placeholder cards for balanced grid -->
      <div class="bg-white dark:bg-[#1d1e1f] rounded-2xl p-6 border border-gray-100 dark:border-gray-800 card-shadow flex items-center justify-between opacity-70">
        <div>
          <p class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">活跃课程</p>
          <h3 class="text-3xl font-bold text-gray-900 dark:text-gray-100">--</h3>
        </div>
        <div class="p-3 bg-purple-50 dark:bg-purple-900/30 rounded-xl text-purple-500">
          <el-icon class="text-2xl"><Reading /></el-icon>
        </div>
      </div>

      <div class="bg-white dark:bg-[#1d1e1f] rounded-2xl p-6 border border-gray-100 dark:border-gray-800 card-shadow flex items-center justify-between opacity-70">
        <div>
          <p class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">系统状态</p>
          <h3 class="text-3xl font-bold text-gray-900 dark:text-gray-100">正常</h3>
        </div>
        <div class="p-3 bg-orange-50 dark:bg-orange-900/30 rounded-xl text-orange-500">
          <el-icon class="text-2xl"><CircleCheckFilled /></el-icon>
        </div>
      </div>
    </div>

    <!-- Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1 min-h-[400px]">
      <div class="bg-white dark:bg-[#1d1e1f] rounded-2xl border border-gray-100 dark:border-gray-800 card-shadow p-6 col-span-1 flex flex-col">
        <h3 class="font-bold text-lg mb-4 text-gray-800 dark:text-gray-200">性别比例</h3>
        <div ref="genderChartRef" class="flex-1 w-full"></div>
      </div>
      <div class="bg-white dark:bg-[#1d1e1f] rounded-2xl border border-gray-100 dark:border-gray-800 card-shadow p-6 col-span-1 lg:col-span-2 flex flex-col">
        <h3 class="font-bold text-lg mb-4 text-gray-800 dark:text-gray-200">各专业人数分布</h3>
        <div ref="majorChartRef" class="flex-1 w-full"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Removed old styles, using Tailwind */
</style>
