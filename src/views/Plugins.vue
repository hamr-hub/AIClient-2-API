<template>
  <div class="plugins-page">
    <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
      <h2 class="text-xl font-bold text-slate-800 mb-6">插件管理</h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div 
          v-for="plugin in plugins" 
          :key="plugin.id"
          class="p-4 border rounded-xl transition-all"
          :class="plugin.enabled ? 'border-emerald-200 bg-emerald-50' : 'border-slate-200 bg-slate-50'"
        >
          <div class="flex items-start justify-between mb-3">
            <div class="flex items-center gap-3">
              <div 
                class="w-10 h-10 rounded-lg flex items-center justify-center"
                :class="plugin.enabled ? 'bg-emerald-100' : 'bg-slate-200'"
              >
                <i :class="['fas', plugin.icon, 'text-lg', plugin.enabled ? 'text-emerald-600' : 'text-slate-500']"></i>
              </div>
              <div>
                <p class="font-medium text-slate-800">{{ plugin.name }}</p>
                <p class="text-xs text-slate-500">v{{ plugin.version }}</p>
              </div>
            </div>
            <button 
              class="relative w-12 h-6 rounded-full transition-colors"
              :class="plugin.enabled ? 'bg-emerald-500' : 'bg-slate-300'"
              @click="togglePlugin(plugin)"
            >
              <span 
                class="absolute top-1 w-4 h-4 bg-white rounded-full transition-transform"
                :class="plugin.enabled ? 'translate-x-7' : 'translate-x-1'"
              ></span>
            </button>
          </div>
          <p class="text-sm text-slate-600 mb-3">{{ plugin.description }}</p>
          <div class="flex items-center gap-2 text-xs text-slate-500">
            <span 
              class="px-2 py-1 rounded-full"
              :class="plugin.type === 'auth' ? 'bg-blue-100 text-blue-700' : 'bg-purple-100 text-purple-700'"
            >
              {{ plugin.type === 'auth' ? '认证插件' : '中间件' }}
            </span>
          </div>
        </div>
      </div>
      
      <div class="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
        <div class="flex items-start gap-3">
          <i class="fas fa-info-circle text-amber-600 flex-shrink-0 mt-0.5"></i>
          <div>
            <p class="text-amber-800 font-medium">提示</p>
            <p class="text-sm text-amber-700 mt-1">启用或禁用插件后需要重启服务才能生效。</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const plugins = ref([
  { 
    id: 1, 
    name: 'default-auth', 
    icon: 'fa-lock',
    version: '1.0.0', 
    description: 'API Key 认证插件，提供基础的 API 密钥验证功能',
    type: 'auth',
    enabled: true 
  },
  { 
    id: 2, 
    name: 'ai-monitor', 
    icon: 'fa-eye',
    version: '1.1.0', 
    description: 'AI 接口监控插件，支持全链路抓包和请求日志',
    type: 'middleware',
    enabled: true 
  },
  { 
    id: 3, 
    name: 'api-potluck', 
    icon: 'fa-users',
    version: '2.0.0', 
    description: 'API 大锅饭插件，提供 Key 管理和用量统计功能',
    type: 'middleware',
    enabled: false 
  },
  { 
    id: 4, 
    name: 'model-usage-stats', 
    icon: 'fa-chart-bar',
    version: '1.0.5', 
    description: '模型用量统计插件，追踪各模型的使用情况',
    type: 'middleware',
    enabled: true 
  },
  { 
    id: 5, 
    name: 'rate-limiter', 
    icon: 'fa-gauge',
    version: '1.2.0', 
    description: '请求限流插件，防止 API 被滥用',
    type: 'middleware',
    enabled: false 
  },
  { 
    id: 6, 
    name: 'logging', 
    icon: 'fa-file-text',
    version: '1.0.0', 
    description: '日志记录插件，记录所有 API 请求和响应',
    type: 'middleware',
    enabled: false 
  }
])

const togglePlugin = (plugin) => {
  plugin.enabled = !plugin.enabled
}
</script>

<style scoped>
.plugins-page {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
