<template>
  <div class="config-page">
    <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-slate-800">系统配置</h2>
        <button 
          class="px-4 py-2 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 transition-colors flex items-center gap-2"
          @click="saveConfig"
        >
          <i class="fas fa-save"></i> 保存配置
        </button>
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h3 class="text-lg font-semibold text-slate-700 mb-4">服务器设置</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">服务器端口</label>
              <input 
                type="number" 
                v-model="config.serverPort"
                class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">API 密钥</label>
              <div class="relative">
                <input 
                  type="password" 
                  v-model="config.apiKey"
                  :type="showApiKey ? 'text' : 'password'"
                  class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                />
                <button 
                  type="button" 
                  class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                  @click="showApiKey = !showApiKey"
                >
                  <i :class="['fas', showApiKey ? 'fa-eye-slash' : 'fa-eye']"></i>
                </button>
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">默认提供商</label>
              <select 
                v-model="config.defaultProvider"
                class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              >
                <option value="gemini-cli-oauth">Gemini CLI OAuth</option>
                <option value="claude-custom">Claude Custom</option>
                <option value="openai-custom">OpenAI Custom</option>
                <option value="grok-custom">Grok Custom</option>
              </select>
            </div>
          </div>
        </div>
        
        <div>
          <h3 class="text-lg font-semibold text-slate-700 mb-4">健康检查设置</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">不健康阈值</label>
              <input 
                type="number" 
                v-model="config.maxErrorCount"
                class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">令牌刷新间隔（分钟）</label>
              <input 
                type="number" 
                v-model="config.tokenRefreshInterval"
                class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              />
            </div>
            <div class="flex items-center justify-between p-4 bg-slate-50 rounded-lg">
              <span class="text-slate-700">启用定时健康检查</span>
              <button 
                type="button"
                class="relative w-12 h-6 rounded-full transition-colors"
                :class="config.healthCheckEnabled ? 'bg-emerald-500' : 'bg-slate-300'"
                @click="config.healthCheckEnabled = !config.healthCheckEnabled"
              >
                <span 
                  class="absolute top-1 w-4 h-4 bg-white rounded-full transition-transform"
                  :class="config.healthCheckEnabled ? 'translate-x-7' : 'translate-x-1'"
                ></span>
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
        <div class="flex items-start gap-3">
          <i class="fas fa-info-circle text-amber-600 flex-shrink-0 mt-0.5"></i>
          <div>
            <p class="text-amber-800 font-medium">提示</p>
            <p class="text-sm text-amber-700 mt-1">修改配置后需要重启服务才能生效。</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const showApiKey = ref(false)

const config = reactive({
  serverPort: 3000,
  apiKey: '123456',
  defaultProvider: 'gemini-cli-oauth',
  maxErrorCount: 10,
  tokenRefreshInterval: 15,
  healthCheckEnabled: false
})

const saveConfig = () => {
  alert('配置已保存')
}
</script>

<style scoped>
.config-page {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
