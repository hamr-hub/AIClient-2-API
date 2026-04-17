<template>
  <div class="custom-models-page">
    <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-slate-800">自定义模型管理</h2>
        <button 
          class="px-4 py-2 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 transition-colors flex items-center gap-2"
          @click="showAddModal = true"
        >
          <i class="fas fa-plus"></i> 添加模型
        </button>
      </div>
      
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="bg-slate-50">
              <th class="px-4 py-3 text-left text-sm font-semibold text-slate-700">模型名称</th>
              <th class="px-4 py-3 text-left text-sm font-semibold text-slate-700">目标提供商</th>
              <th class="px-4 py-3 text-left text-sm font-semibold text-slate-700">目标模型</th>
              <th class="px-4 py-3 text-left text-sm font-semibold text-slate-700">状态</th>
              <th class="px-4 py-3 text-left text-sm font-semibold text-slate-700">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="model in customModels" :key="model.id" class="border-b border-slate-100">
              <td class="px-4 py-3">
                <span class="font-medium text-slate-800">{{ model.name }}</span>
              </td>
              <td class="px-4 py-3 text-slate-600">{{ model.provider }}</td>
              <td class="px-4 py-3 text-slate-600">{{ model.targetModel }}</td>
              <td class="px-4 py-3">
                <span 
                  class="px-2 py-1 text-xs rounded-full"
                  :class="model.enabled ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-500'"
                >
                  {{ model.enabled ? '启用' : '禁用' }}
                </span>
              </td>
              <td class="px-4 py-3">
                <button 
                  class="p-1 hover:bg-slate-100 rounded transition-colors"
                  @click="toggleModel(model)"
                >
                  <i :class="['fas', model.enabled ? 'fa-toggle-on text-emerald-500' : 'fa-toggle-off text-slate-400']"></i>
                </button>
                <button 
                  class="p-1 hover:bg-slate-100 rounded transition-colors ml-2"
                  @click="deleteModel(model.id)"
                >
                  <i class="fas fa-trash text-red-500"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <div v-if="showAddModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-md mx-4">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-slate-800">添加自定义模型</h3>
          <button 
            class="p-1 hover:bg-slate-100 rounded transition-colors"
            @click="showAddModal = false"
          >
            <i class="fas fa-x text-slate-500"></i>
          </button>
        </div>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">模型名称</label>
            <input 
              type="text" 
              v-model="newModel.name"
              class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              placeholder="自定义模型名称"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">目标提供商</label>
            <select 
              v-model="newModel.provider"
              class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            >
              <option value="gemini-cli-oauth">Gemini CLI OAuth</option>
              <option value="claude-custom">Claude Custom</option>
              <option value="openai-custom">OpenAI Custom</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">目标模型</label>
            <input 
              type="text" 
              v-model="newModel.targetModel"
              class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              placeholder="目标模型名称"
            />
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
              @click="addModel"
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

const customModels = ref([
  { id: 1, name: 'my-gpt-4o', provider: 'OpenAI Custom', targetModel: 'gpt-4o', enabled: true },
  { id: 2, name: 'my-gemini-pro', provider: 'Gemini CLI OAuth', targetModel: 'gemini-2.5-pro', enabled: true },
  { id: 3, name: 'my-claude-sonnet', provider: 'Claude Custom', targetModel: 'claude-3-5-sonnet-20241022', enabled: false }
])

const newModel = reactive({
  name: '',
  provider: 'gemini-cli-oauth',
  targetModel: ''
})

const addModel = () => {
  if (!newModel.name || !newModel.targetModel) return
  
  customModels.value.push({
    id: Date.now(),
    name: newModel.name,
    provider: newModel.provider,
    targetModel: newModel.targetModel,
    enabled: true
  })
  
  newModel.name = ''
  newModel.provider = 'gemini-cli-oauth'
  newModel.targetModel = ''
  showAddModal.value = false
}

const toggleModel = (model) => {
  model.enabled = !model.enabled
}

const deleteModel = (id) => {
  customModels.value = customModels.value.filter(m => m.id !== id)
}
</script>

<style scoped>
.custom-models-page {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
