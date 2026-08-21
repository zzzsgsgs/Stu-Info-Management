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
  <div v-loading="loading" class="dashboard-container">
    <el-row :gutter="20" class="panel-group">
      <el-col :span="12">
        <el-card shadow="hover" class="data-panel">
          <div class="panel-title">总学生人数</div>
          <div class="panel-num text-primary">{{ stats.total_students }}</div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover" class="data-panel">
          <div class="panel-title">平均 GPA</div>
          <div class="panel-num text-success">{{ stats.average_gpa }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="chart-group">
      <el-col :span="8">
        <el-card shadow="hover">
          <div ref="genderChartRef" class="chart" style="height: 400px;"></div>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card shadow="hover">
          <div ref="majorChartRef" class="chart" style="height: 400px;"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.dashboard-container {
  padding: 20px;
}
.panel-group {
  margin-bottom: 20px;
}
.data-panel {
  text-align: center;
  padding: 20px 0;
}
.panel-title {
  color: #909399;
  font-size: 16px;
  margin-bottom: 10px;
}
.panel-num {
  font-size: 36px;
  font-weight: bold;
}
.text-primary {
  color: #409EFF;
}
.text-success {
  color: #67C23A;
}
.chart-group {
  margin-top: 20px;
}
</style>
