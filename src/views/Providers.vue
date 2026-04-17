<template>
  <div class="providers-page">
    <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-slate-800">提供商池管理</h2>
        <button 
          class="px-4 py-2 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 transition-colors flex items-center gap-2"
          @click="showAddModal = true"
        >
          <i class="fas fa-plus"></i> 添加提供商
        </button>
      </div>
      
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <div 
          v-for="provider in providers" 
          :key="provider.id"
          class="p-4 border rounded-xl transition-all"
          :class="[
            provider.status === 'healthy' ? 'border-emerald-200 bg-emerald-50' :
            provider.status === 'warning' ? 'border-amber-200 bg-amber-50' :
            'border-red-200 bg-red-50'
          ]"
        >
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2">
              <span 
                class="w-2 h-2 rounded-full"
                :class="[
                  provider.status === 'healthy' ? 'bg-emerald-500' :
                  provider.status === 'warning' ? 'bg-amber-500' :
                  'bg-red-500'
                ]"
              ></span>
              <span class="font-medium text-slate-800">{{ provider.name }}</span>
            </div>
            <div class="flex gap-1">
              <button class="p-1 hover:bg-white/50 rounded transition-colors">
                <i class="fas fa-edit text-slate-600"></i>
              </button>
              <button class="p-1 hover:bg-white/50 rounded transition-colors">
                <i class="fas fa-trash text-red-500"></i>
              </button>
            </div>
          </div>
          <p class="text-sm text-slate-600 mb-2">{{ provider.type }}</p>
          <div class="flex items-center gap-4 text-xs text-slate-500">
            <span>{{ provider.accounts }} 账户</span>
            <span>{{ provider.requests }} 请求</span>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="showAddModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-md mx-4">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-slate-800">添加提供商</h3>
          <button 
            class="p-1 hover:bg-slate-100 rounded transition-colors"
            @click="showAddModal = false"
          >
            <i class="fas fa-x text-slate-500"></i>
          </button>
        </div>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">提供商名称</label>
            <input 
              type="text" 
              v-model="newProvider.name"
              class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              placeholder="输入提供商名称"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">提供商类型</label>
            <select 
              v-model="newProvider.type"
              class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            >
              <option value="gemini-cli-oauth">Gemini CLI OAuth</option>
              <option value="claude-custom">Claude Custom</option>
              <option value="openai-custom">OpenAI Custom</option>
              <option value="grok-custom">Grok Custom</option>
              <option value="qwen-custom">Qwen Custom</option>
            </select>
          </div>
          <div class="flex gap-3 pt-4">
            <button 
              class="flex-1 px-4 py-2 border border-slate-300 text-slate-700 rounded-lg hover:bg-slate-50 transition-colors"
              @click="showAddModal = false"
            >
              取消
            </button>
            <button 
              class="flex-1 px-4 py-2 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 transition-colors"
              @click="addProvider"
            >
              添加
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const showAddModal = ref(false)

const providers = ref([
  { id: 1, name: 'Gemini Primary', type: 'Gemini CLI OAuth', status: 'healthy', accounts: 3, requests: 1250 },
  { id: 2, name: 'Claude Enterprise', type: 'Claude Custom', status: 'healthy', accounts: 2, requests: 890 },
  { id: 3, name: 'OpenAI Backup', type: 'OpenAI Custom', status: 'warning', accounts: 1, requests: 450 },
  { id: 4, name: 'Grok Beta', type: 'Grok Custom', status: 'healthy', accounts: 2, requests: 230 },
  { id: 5, name: 'Qwen Cloud', type: 'Qwen Custom', status: 'error', accounts: 0, requests: 0 }
])

const newProvider = reactive({
  name: '',
  type: 'gemini-cli-oauth'
})

const addProvider = () => {
  if (!newProvider.name) return
  
  providers.value.push({
    id: Date.now(),
    name: newProvider.name,
    type: newProvider.type,
    status: 'healthy',
    accounts: 0,
    requests: 0
  })
  
  newProvider.name = ''
  newProvider.type = 'gemini-cli-oauth'
  showAddModal.value = false
}
</script>

<style scoped>
.providers-page {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
