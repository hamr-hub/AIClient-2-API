<template>
  <div class="usage-page">
    <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-slate-800">用量查询</h2>
        <button 
          class="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 transition-colors flex items-center gap-2"
          @click="refreshData"
        >
          <i class="fas fa-refresh"></i> 刷新数据
        </button>
      </div>
      
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div class="p-4 bg-emerald-50 rounded-xl">
          <p class="text-sm text-emerald-700 mb-1">今日请求数</p>
          <h3 class="text-2xl font-bold text-emerald-800">{{ usageStats.todayRequests }}</h3>
        </div>
        <div class="p-4 bg-blue-50 rounded-xl">
          <p class="text-sm text-blue-700 mb-1">本周请求数</p>
          <h3 class="text-2xl font-bold text-blue-800">{{ usageStats.weekRequests }}</h3>
        </div>
        <div class="p-4 bg-purple-50 rounded-xl">
          <p class="text-sm text-purple-700 mb-1">本月请求数</p>
          <h3 class="text-2xl font-bold text-purple-800">{{ usageStats.monthRequests }}</h3>
        </div>
        <div class="p-4 bg-orange-50 rounded-xl">
          <p class="text-sm text-orange-700 mb-1">总请求数</p>
          <h3 class="text-2xl font-bold text-orange-800">{{ usageStats.totalRequests }}</h3>
        </div>
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="border border-slate-200 rounded-xl p-4">
          <h3 class="text-lg font-semibold text-slate-700 mb-4">按提供商统计</h3>
          <div class="space-y-3">
            <div v-for="item in providerStats" :key="item.name" class="flex items-center gap-4">
              <span class="text-sm text-slate-600 w-20">{{ item.name }}</span>
              <div class="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                <div 
                  class="h-full rounded-full"
                  :class="item.color"
                  :style="{ width: item.percentage + '%' }"
                ></div>
              </div>
              <span class="text-sm font-medium text-slate-700 w-16 text-right">{{ item.count }}</span>
            </div>
          </div>
        </div>
        
        <div class="border border-slate-200 rounded-xl p-4">
          <h3 class="text-lg font-semibold text-slate-700 mb-4">按模型统计</h3>
          <div class="space-y-3">
            <div v-for="item in modelStats" :key="item.name" class="flex items-center gap-4">
              <span class="text-sm text-slate-600 w-32 truncate">{{ item.name }}</span>
              <span class="text-sm font-medium text-slate-700">{{ item.count }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const usageStats = ref({
  todayRequests: 1250,
  weekRequests: 8920,
  monthRequests: 32500,
  totalRequests: 156000
})

const providerStats = ref([
  { name: 'Gemini', count: 8500, percentage: 45, color: 'bg-emerald-500' },
  { name: 'Claude', count: 6200, percentage: 33, color: 'bg-blue-500' },
  { name: 'OpenAI', count: 2800, percentage: 15, color: 'bg-purple-500' },
  { name: 'Grok', count: 1300, percentage: 7, color: 'bg-orange-500' }
])

const modelStats = ref([
  { name: 'gemini-2.5-flash', count: 4500 },
  { name: 'claude-3-5-sonnet', count: 3200 },
  { name: 'gpt-4o-mini', count: 2100 },
  { name: 'gemini-2.5-pro', count: 1800 },
  { name: 'claude-3-opus', count: 1200 }
])

const refreshData = () => {
  usageStats.value = {
    todayRequests: Math.floor(Math.random() * 2000) + 1000,
    weekRequests: Math.floor(Math.random() * 5000) + 7000,
    monthRequests: Math.floor(Math.random() * 10000) + 25000,
    totalRequests: Math.floor(Math.random() * 50000) + 130000
  }
}
</script>

<style scoped>
.usage-page {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
