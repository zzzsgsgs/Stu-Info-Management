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
  <div class="app-container">
    <h2>系统审计日志</h2>
    <el-table v-loading="loading" :data="tableData" border style="width: 100%; margin-top: 20px;">
      <el-table-column prop="timestamp" label="操作时间" width="200" />
      <el-table-column prop="username" label="操作人" width="120" />
      <el-table-column prop="action" label="操作类型" width="120" align="center">
        <template #default="scope">
          <el-tag :type="getTagType(scope.row.action)">{{ scope.row.action }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="entity_type" label="实体类型" width="120" />
      <el-table-column prop="entity_id" label="实体ID" width="150" />
      <el-table-column prop="details" label="详细信息" />
    </el-table>

    <div class="pagination-container" style="margin-top: 20px; text-align: right;">
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
.app-container {
  padding: 20px;
  background-color: var(--el-bg-color);
  border-radius: 4px;
}
</style>
