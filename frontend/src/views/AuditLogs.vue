<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import request from '../utils/request'

const tableData = ref([])
const total = ref(0)
const loading = ref(false)
const queryParams = reactive({ skip: 0, limit: 20 })

const fetchList = async () => {
  loading.value = true
  try {
    const res: any = await request.get('/system/audit-logs', { params: queryParams })
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

const getTagType = (action: string) => {
  if (action === 'CREATE') return 'success'
  if (action === 'UPDATE') return 'warning'
  if (action === 'DELETE') return 'danger'
  return 'info'
}

onMounted(() => fetchList())
</script>

<template>
  <div class="bg-white dark:bg-[#1d1e1f] rounded-2xl border border-gray-100 dark:border-gray-800 card-shadow p-6 h-full flex flex-col">
    <div class="mb-6 border-b border-gray-100 dark:border-gray-800 pb-4">
      <h2 class="text-xl font-bold text-gray-800 dark:text-gray-200 m-0">安全审计日志</h2>
      <p class="text-sm text-gray-500 mt-1">追踪系统内所有核心的数据变更与越权行为。</p>
    </div>

    <el-table v-loading="loading" :data="tableData" stripe class="w-full flex-1">
      <el-table-column prop="timestamp" label="操作时间" width="220">
        <template #default="scope">
          <span class="font-mono text-xs">{{ new Date(scope.row.timestamp).toLocaleString() }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="username" label="操作人" width="120">
        <template #default="scope">
          <div class="flex items-center gap-2">
            <el-avatar :size="24">{{ scope.row.username.charAt(0).toUpperCase() }}</el-avatar>
            <span>{{ scope.row.username }}</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="action" label="动作" width="100" align="center">
        <template #default="scope">
          <el-tag :type="getTagType(scope.row.action)" effect="dark" size="small">{{ scope.row.action }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="entity_type" label="实体" width="120" />
      <el-table-column prop="entity_id" label="标识" width="150">
        <template #default="scope">
          <el-tag type="info" size="small">{{ scope.row.entity_id }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="details" label="详细描述" />
    </el-table>

    <div class="mt-6 flex justify-end">
      <el-pagination
        v-model:current-page="queryParams.skip"
        v-model:page-size="queryParams.limit"
        :page-sizes="[20, 50, 100]"
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
