<template>
  <div class="logs-page">
    <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-slate-800">实时日志</h2>
        <div class="flex items-center gap-3">
          <select 
            v-model="filterLevel"
            class="px-3 py-2 border border-slate-300 rounded-lg text-sm"
          >
            <option value="all">全部级别</option>
            <option value="info">INFO</option>
            <option value="warn">WARN</option>
            <option value="error">ERROR</option>
          </select>
          <button 
            class="px-3 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 transition-colors flex items-center gap-2"
            @click="clearLogs"
          >
            <i class="fas fa-trash"></i> 清空
          </button>
        </div>
      </div>
      
      <div class="h-96 overflow-auto bg-slate-900 rounded-xl p-4 font-mono text-sm">
        <div 
          v-for="(log, index) in filteredLogs" 
          :key="index"
          class="mb-1 flex"
        >
          <span class="text-slate-500 w-32 shrink-0">{{ log.time }}</span>
          <span 
            class="px-1.5 py-0.5 rounded text-xs font-medium mx-2 shrink-0"
            :class="[
              log.level === 'INFO' ? 'bg-blue-500 text-white' :
              log.level === 'WARN' ? 'bg-yellow-500 text-white' :
              'bg-red-500 text-white'
            ]"
          >
            {{ log.level }}
          </span>
          <span :class="[
            log.level === 'ERROR' ? 'text-red-400' :
            log.level === 'WARN' ? 'text-yellow-400' :
            'text-slate-300'
          ]">
            {{ log.message }}
          </span>
        </div>
        <div v-if="logs.length === 0" class="text-slate-500 text-center py-8">
          暂无日志
        </div>
      </div>
      
      <div class="mt-4 flex items-center justify-between">
        <div class="flex items-center gap-4 text-sm text-slate-500">
          <span>日志数量: {{ logs.length }}</span>
          <span>INFO: {{ infoCount }}</span>
          <span>WARN: {{ warnCount }}</span>
          <span>ERROR: {{ errorCount }}</span>
        </div>
        <button 
          class="px-3 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 transition-colors flex items-center gap-2"
          @click="toggleAutoScroll"
        >
          <i :class="['fas', autoScroll ? 'fa-check' : 'fa-times']"></i>
          {{ autoScroll ? '自动滚动' : '停止滚动' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const logs = ref([])
const filterLevel = ref('all')
const autoScroll = ref(true)

let logInterval = null

const logMessages = [
  { level: 'INFO', message: 'API server started on port 3000' },
  { level: 'INFO', message: 'Loaded 5 provider configurations' },
  { level: 'INFO', message: 'Plugin default-auth loaded successfully' },
  { level: 'INFO', message: 'Plugin ai-monitor loaded successfully' },
  { level: 'WARN', message: 'Provider OpenAI-Backup has 0 healthy accounts' },
  { level: 'INFO', message: 'Health check completed for all providers' },
  { level: 'INFO', message: 'API request received: /api/v1/chat/completions' },
  { level: 'INFO', message: 'Request completed successfully in 125ms' },
  { level: 'ERROR', message: 'Failed to refresh token for provider Gemini-Primary' },
  { level: 'INFO', message: 'Token refreshed successfully after retry' },
  { level: 'INFO', message: 'New provider added: Claude-Enterprise' },
  { level: 'WARN', message: 'High memory usage detected: 78%' },
  { level: 'INFO', message: 'Config file saved successfully' },
  { level: 'INFO', message: 'Plugin model-usage-stats loaded successfully' },
  { level: 'INFO', message: 'API request received: /api/v1/models' },
  { level: 'INFO', message: 'Model list retrieved successfully' },
  { level: 'ERROR', message: 'Provider Qwen-Cloud connection timeout' },
  { level: 'INFO', message: 'Provider fallback to secondary node' },
  { level: 'INFO', message: 'System health check passed' },
  { level: 'INFO', message: 'Server time synchronized' }
]

const filteredLogs = computed(() => {
  if (filterLevel.value === 'all') return logs.value
  return logs.value.filter(log => log.level === filterLevel.value.toUpperCase())
})

const infoCount = computed(() => logs.value.filter(l => l.level === 'INFO').length)
const warnCount = computed(() => logs.value.filter(l => l.level === 'WARN').length)
const errorCount = computed(() => logs.value.filter(l => l.level === 'ERROR').length)

const addLog = () => {
  const randomLog = logMessages[Math.floor(Math.random() * logMessages.length)]
  const now = new Date()
  const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`
  
  logs.value.push({
    time: timeStr,
    level: randomLog.level,
    message: randomLog.message
  })
  
  if (logs.value.length > 100) {
    logs.value.shift()
  }
  
  if (autoScroll.value) {
    setTimeout(() => {
      const container = document.querySelector('.h-96')
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    }, 100)
  }
}

const clearLogs = () => {
  logs.value = []
}

const toggleAutoScroll = () => {
  autoScroll.value = !autoScroll.value
}

onMounted(() => {
  logs.value = [
    { time: '10:00:00', level: 'INFO', message: 'AIClient2API service started' },
    { time: '10:00:01', level: 'INFO', message: 'Loading configuration...' },
    { time: '10:00:02', level: 'INFO', message: 'Configuration loaded successfully' },
    { time: '10:00:03', level: 'INFO', message: 'Initializing providers...' },
    { time: '10:00:04', level: 'INFO', message: 'All providers initialized' },
    { time: '10:00:05', level: 'INFO', message: 'Server ready on http://localhost:3000' }
  ]
  
  logInterval = setInterval(addLog, 3000)
})

onUnmounted(() => {
  if (logInterval) {
    clearInterval(logInterval)
  }
})
</script>

<style scoped>
.logs-page {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
