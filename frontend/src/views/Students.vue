<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import request from '../utils/request'

const tableData = ref([])
const total = ref(0)
const loading = ref(false)

const queryParams = reactive({
  skip: 0,
  limit: 10,
  search: '',
  sort_by: '',
  sort_desc: false
})

const dialogVisible = ref(false)
const dialogTitle = ref('新增学生')
const formRef = ref<FormInstance>()
const submitLoading = ref(false)

interface StudentForm {
  id?: number
  student_id: string
  name: string
  gender: string
  age: number | null
  grade: string
  major: string
  contact: string
  gpa: number | null
  enrollment_date: string
}

const formData = reactive<StudentForm>({
  student_id: '',
  name: '',
  gender: '男',
  age: null,
  grade: '大一',
  major: '',
  contact: '',
  gpa: null,
  enrollment_date: ''
})

const rules = reactive<FormRules>({
  student_id: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  grade: [{ required: true, message: '请选择年级', trigger: 'change' }],
  major: [{ required: true, message: '请输入专业', trigger: 'blur' }],
  enrollment_date: [{ required: true, message: '请选择入学日期', trigger: 'change' }],
  gpa: [
    { type: 'number', message: 'GPA必须为数字', trigger: 'blur', transform: (val) => Number(val) },
    { validator: (_rule, value, callback) => {
      if (value !== null && value !== '' && (value < 0 || value > 4)) {
        callback(new Error('GPA范围在 0.0 - 4.0 之间'))
      } else {
        callback()
      }
    }, trigger: 'blur'}
  ]
})

const fetchList = async () => {
  loading.value = true
  try {
    const res: any = await request.get('/students/', { params: queryParams })
    tableData.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  queryParams.skip = 0
  fetchList()
}

const handleSortChange = ({ prop, order }: any) => {
  queryParams.sort_by = prop
  queryParams.sort_desc = order === 'descending'
  fetchList()
}

const handleSizeChange = (val: number) => {
  queryParams.limit = val
  fetchList()
}

const handleCurrentChange = (val: number) => {
  queryParams.skip = (val - 1) * queryParams.limit
  fetchList()
}

const resetForm = () => {
  if (formRef.value) formRef.value.resetFields()
  Object.assign(formData, {
    id: undefined, student_id: '', name: '', gender: '男', age: null,
    grade: '大一', major: '', contact: '', gpa: null, enrollment_date: ''
  })
}

const handleAdd = () => {
  resetForm()
  dialogTitle.value = '新增学生'
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  resetForm()
  Object.assign(formData, row)
  dialogTitle.value = '编辑学生'
  dialogVisible.value = true
}

const handleDelete = (row: any) => {
  ElMessageBox.confirm(`确定删除学生 ${row.name} 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    await request.delete(`/students/${row.id}`)
    ElMessage.success('删除成功')
    fetchList()
  }).catch(() => {})
}

const selectedIds = ref<number[]>([])

const handleSelectionChange = (selection: any[]) => {
  selectedIds.value = selection.map(item => item.id)
}

const handleBatchDelete = () => {
  if (selectedIds.value.length === 0) return
  ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 名学生吗？`, '警告', {
    type: 'warning'
  }).then(async () => {
    // In a real app, you would have a bulk delete API. Here we just loop (or assuming backend adds bulk).
    // For simplicity, we loop.
    loading.value = true
    try {
      for (const id of selectedIds.value) {
        await request.delete(`/students/${id}`)
      }
      ElMessage.success('批量删除成功')
      fetchList()
    } finally {
      loading.value = false
    }
  }).catch(() => {})
}

const handleExport = () => {
  const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  window.open(`${baseURL}/students/export?token=${localStorage.getItem('token')}`)
}

const drawerVisible = ref(false)
const drawerData = ref<any>(null)

const handleViewProfile = (row: any) => {
  drawerData.value = row
  drawerVisible.value = true
}

const handleSubmit = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate(async (valid) => {
    if (valid) {
      submitLoading.value = true
      try {
        if (formData.id) {
          await request.put(`/students/${formData.id}`, formData)
          ElMessage.success('更新成功')
        } else {
          await request.post('/students/', formData)
          ElMessage.success('新增成功')
        }
        dialogVisible.value = false
        fetchList()
      } finally {
        submitLoading.value = false
      }
    }
  })
}

onMounted(() => {
  fetchList()
})
</script>

<template>
  <div class="bg-white dark:bg-[#1d1e1f] rounded-2xl border border-gray-100 dark:border-gray-800 card-shadow p-6 h-full flex flex-col">
    <!-- Header Toolbar -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
      <div class="flex items-center">
        <el-input
          v-model="queryParams.search"
          placeholder="搜索姓名或专业..."
          class="w-64"
          clearable
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" class="ml-3" @click="handleSearch">
          查询
        </el-button>
      </div>

      <div class="flex items-center space-x-2">
        <el-button type="primary" icon="Plus" @click="handleAdd" class="hover:-translate-y-0.5 transition-transform duration-200">新增学生</el-button>
        <el-button type="success" plain icon="Download" @click="handleExport" class="hover:-translate-y-0.5 transition-transform duration-200">导出记录</el-button>
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="selectedIds.length === 0"
          @click="handleBatchDelete"
          class="hover:-translate-y-0.5 transition-transform duration-200"
        >
          批量删除 ({{ selectedIds.length }})
        </el-button>
      </div>
    </div>

    <!-- Data Table -->
    <el-table
      v-loading="loading"
      :data="tableData"
      stripe
      class="w-full flex-1"
      @sort-change="handleSortChange"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" />
      <el-table-column prop="student_id" label="学号" width="120" sortable="custom" />
      <el-table-column prop="name" label="姓名" width="120">
        <template #default="scope">
          <el-link type="primary" @click="handleViewProfile(scope.row)">{{ scope.row.name }}</el-link>
        </template>
      </el-table-column>
      <el-table-column prop="gender" label="性别" width="80" align="center">
        <template #default="scope">
          <el-tag :type="scope.row.gender === '男' ? '' : 'danger'">{{ scope.row.gender }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="age" label="年龄" width="80" />
      <el-table-column prop="grade" label="年级" width="100" />
      <el-table-column prop="major" label="专业" />
      <el-table-column prop="contact" label="联系方式" width="150" />
      <el-table-column prop="gpa" label="GPA" width="100" sortable="custom" />
      <el-table-column prop="enrollment_date" label="入学日期" width="120" />
      <el-table-column label="操作" width="120" fixed="right" align="center">
        <template #default="scope">
          <el-tooltip content="编辑详情" placement="top">
            <el-button type="primary" link icon="Edit" @click="handleEdit(scope.row)" />
          </el-tooltip>
          <el-tooltip content="删除记录" placement="top">
            <el-button type="danger" link icon="Delete" @click="handleDelete(scope.row)" />
          </el-tooltip>
        </template>
      </el-table-column>
    </el-table>

    <!-- Pagination -->
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

    <!-- 弹窗表单 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px" @close="resetForm">
      <el-form ref="formRef" :model="formData" :rules="rules" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="学号" prop="student_id">
              <el-input v-model="formData.student_id" :disabled="!!formData.id" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="formData.name" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="formData.gender" placeholder="请选择" style="width: 100%">
                <el-option label="男" value="男" />
                <el-option label="女" value="女" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="年龄" prop="age">
              <el-input-number v-model="formData.age" :min="1" :max="100" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="年级" prop="grade">
              <el-select v-model="formData.grade" placeholder="请选择" style="width: 100%">
                <el-option label="大一" value="大一" />
                <el-option label="大二" value="大二" />
                <el-option label="大三" value="大三" />
                <el-option label="大四" value="大四" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="专业" prop="major">
              <el-input v-model="formData.major" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="GPA" prop="gpa">
              <el-input v-model="formData.gpa" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系方式" prop="contact">
              <el-input v-model="formData.contact" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="入学日期" prop="enrollment_date">
              <el-date-picker v-model="formData.enrollment_date" type="date" value-format="YYYY-MM-DD" placeholder="选择日期" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="submitLoading" @click="handleSubmit(formRef)">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 档案抽屉 -->
    <el-drawer v-model="drawerVisible" :title="`${drawerData?.name || ''}的档案`" size="40%">
      <div v-if="drawerData">
        <el-descriptions title="基础信息" :column="2" border>
          <el-descriptions-item label="学号">{{ drawerData.student_id }}</el-descriptions-item>
          <el-descriptions-item label="姓名">{{ drawerData.name }}</el-descriptions-item>
          <el-descriptions-item label="性别">{{ drawerData.gender }}</el-descriptions-item>
          <el-descriptions-item label="年龄">{{ drawerData.age }}</el-descriptions-item>
          <el-descriptions-item label="专业">{{ drawerData.major }}</el-descriptions-item>
          <el-descriptions-item label="年级">{{ drawerData.grade }}</el-descriptions-item>
          <el-descriptions-item label="联系方式">{{ drawerData.contact }}</el-descriptions-item>
          <el-descriptions-item label="GPA">{{ drawerData.gpa }}</el-descriptions-item>
          <el-descriptions-item label="入学日期">{{ drawerData.enrollment_date }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-drawer>
  </div>
</template>

<style scoped>
/* Removed old styles, relying on Tailwind */
</style>
