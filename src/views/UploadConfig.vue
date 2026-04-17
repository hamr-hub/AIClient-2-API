<template>
  <div class="upload-config-page">
    <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-slate-800">凭据文件管理</h2>
        <button 
          class="px-4 py-2 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 transition-colors flex items-center gap-2"
          @click="triggerUpload"
        >
          <i class="fas fa-upload"></i> 上传文件
        </button>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div 
          v-for="config in configFiles" 
          :key="config.id"
          class="p-4 border border-slate-200 rounded-xl hover:border-emerald-300 transition-colors"
        >
          <div class="flex items-start justify-between">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-slate-100 rounded-lg flex items-center justify-center">
                <i class="fas fa-file-json text-slate-500"></i>
              </div>
              <div>
                <p class="font-medium text-slate-800">{{ config.name }}</p>
                <p class="text-sm text-slate-500">{{ config.size }}</p>
              </div>
            </div>
            <div class="flex gap-2">
              <button 
                class="p-2 hover:bg-slate-100 rounded-lg transition-colors"
                @click="viewConfig(config)"
              >
                <i class="fas fa-eye text-slate-600"></i>
              </button>
              <button 
                class="p-2 hover:bg-slate-100 rounded-lg transition-colors"
                @click="downloadConfig(config)"
              >
                <i class="fas fa-download text-slate-600"></i>
              </button>
              <button 
                class="p-2 hover:bg-red-50 rounded-lg transition-colors"
                @click="deleteConfig(config.id)"
              >
                <i class="fas fa-trash text-red-500"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <input 
        type="file" 
        ref="fileInput" 
        class="hidden"
        accept=".json"
        @change="handleFileUpload"
      />
    </div>
    
    <div v-if="showViewModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-lg mx-4 max-h-[80vh] overflow-hidden flex flex-col">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-slate-800">查看配置</h3>
          <button 
            class="p-1 hover:bg-slate-100 rounded transition-colors"
            @click="showViewModal = false"
          >
            <i class="fas fa-x text-slate-500"></i>
          </button>
        </div>
        <div class="flex-1 overflow-auto">
          <pre class="text-sm text-slate-700 font-mono whitespace-pre-wrap">{{ viewContent }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const fileInput = ref(null)
const showViewModal = ref(false)
const viewContent = ref('')

const configFiles = ref([
  { id: 1, name: 'provider_pools.json', size: '2.3 KB' },
  { id: 2, name: 'config.json', size: '1.1 KB' },
  { id: 3, name: 'plugins.json', size: '512 B' },
  { id: 4, name: 'token-store.json', size: '3.2 KB' }
])

const triggerUpload = () => {
  fileInput.value?.click()
}

const handleFileUpload = (event) => {
  const file = event.target.files?.[0]
  if (file) {
    configFiles.value.push({
      id: Date.now(),
      name: file.name,
      size: formatFileSize(file.size)
    })
    event.target.value = ''
  }
}

const formatFileSize = (bytes) => {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

const viewConfig = (config) => {
  viewContent.value = JSON.stringify({ 
    providers: [],
    settings: {}
  }, null, 2)
  showViewModal.value = true
}

const downloadConfig = (config) => {
  alert(`下载: ${config.name}`)
}

const deleteConfig = (id) => {
  configFiles.value = configFiles.value.filter(c => c.id !== id)
}
</script>

<style scoped>
.upload-config-page {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
