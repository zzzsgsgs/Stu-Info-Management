<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import request from '../utils/request'

const tableData = ref([])
const total = ref(0)
const loading = ref(false)
const queryParams = reactive({ skip: 0, limit: 10 })

const fetchList = async () => {
  loading.value = true
  try {
    const res: any = await request.get('/courses/', { params: queryParams })
    tableData.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

const handleSizeChange = (val: number) => {
  queryParams.limit = val
  fetchList()
}

const handleCurrentChange = (val: number) => {
  queryParams.skip = (val - 1) * queryParams.limit
  fetchList()
}

onMounted(() => fetchList())
</script>

<template>
  <div class="bg-white dark:bg-[#1d1e1f] rounded-2xl border border-gray-100 dark:border-gray-800 card-shadow p-6 h-full flex flex-col">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold text-gray-800 dark:text-gray-200 m-0">课程大纲</h2>
      <el-button type="primary" icon="Plus">排课</el-button>
    </div>

    <el-table v-loading="loading" :data="tableData" stripe class="w-full flex-1">
      <el-table-column prop="course_code" label="课程代码" width="150" />
      <el-table-column prop="name" label="课程名称" />
      <el-table-column prop="credits" label="学分" width="100">
        <template #default="scope">
          <el-tag type="info" effect="plain">{{ scope.row.credits }} 学分</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="department" label="开课学院" />
      <el-table-column prop="teacher" label="授课教师" />
    </el-table>

    <div class="mt-6 flex justify-end">
      <el-pagination
        v-model:current-page="queryParams.skip"
        v-model:page-size="queryParams.limit"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<style scoped>
</style>
