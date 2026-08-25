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
  <div class="app-container">
    <h2>课程管理</h2>
    <el-table v-loading="loading" :data="tableData" border style="width: 100%; margin-top: 20px;">
      <el-table-column prop="course_code" label="课程代码" width="150" />
      <el-table-column prop="name" label="课程名称" />
      <el-table-column prop="credits" label="学分" width="100" />
      <el-table-column prop="department" label="开课学院" />
      <el-table-column prop="teacher" label="授课教师" />
    </el-table>

    <div class="pagination-container" style="margin-top: 20px; text-align: right;">
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
.app-container {
  padding: 20px;
  background-color: var(--el-bg-color);
  border-radius: 4px;
}
</style>
