# AI Controller - 本地 LLM 模型管理服务

基于 Python FastAPI 的控制层服务，用于管理本地大语言模型，提供 GPU 资源监控和自动模型调度功能。

---

## 📋 项目意图

### 背景
AIClient-2-API 是一个优秀的 API 代理服务，提供了完善的鉴权、用户管理和 UI 界面。但是它本身不包含大模型，也没有能力控制本地 GPU 资源。

### 核心目标
本项目旨在实现**"外壳解耦，内核驱动"**的架构方案：

1. **保留 AIClient-2-API 作为入口/UI**：不修改原有代码，通过 Git 持续更新
2. **新增 Python 控制层作为核心大脑**：实现智能调度、资源监控和队列管理
3. **无缝对接**：通过自定义渠道配置，原有用户分组、额度扣费、对话历史全部直接可用

### 解决的问题
- 🎯 **可靠性保障**：如果 vLLM 未启动，Python 后端会截断请求并报错，避免 Node.js 侧长时间挂起超时
- 🎯 **流量削峰**：利用并发控制保护 GPU，防止显存溢出
- 🎯 **自动管理**：根据请求自动启动/停止模型，节省资源

---

## 🏗️ 架构设计

```
┌──────────────────────────┐
│   AIClient-2-API        │  ← 入口层：鉴权、UI、协议转发
│     (Node.js)           │
└──────────┬──────────────┘
           │ OpenAI 协议
           ▼
┌──────────────────────────┐
│   AI Controller         │  ← 控制层：逻辑调度、资源监控、队列管理
│    (FastAPI/Python)     │
└──────────┬──────────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
┌──────────┐ ┌──────────┐
│ nvidia-smi│ │ systemctl│  ← 基础设施层：显存采集、模型启停
└──────────┘ └──────────┘
           │
           ▼
┌──────────────────────────┐
│     vLLM Instance       │  ← 推理层：实际模型推理
└──────────────────────────┘
```

---

## 🚀 快速开始

### 前置条件
- Python 3.10+
- NVIDIA GPU（支持 CUDA）
- vLLM 已安装 (`pip install vllm`)
- Systemd（用于模型服务管理，Linux 系统）

### 安装依赖

```bash
cd app-controller
pip install -r requirements.txt
```

### 配置模型

编辑 `config.yaml` 配置你的模型：

```yaml
models:
  gemma-2-9b:
    service: vllm-gemma    # systemd 服务名
    port: 8000             # vLLM 监听端口
    required_memory: 12GB  # 模型所需显存
  
  llama-3-8b:
    service: vllm-llama
    port: 8001
    required_memory: 10GB

settings:
  concurrency_limit: 4         # 并发请求限制
  min_available_memory: 2GB    # 最小可用显存阈值
```

### 启动服务

```bash
python main.py
```

服务将在 `http://localhost:5000` 启动

---

## 🔌 API 接口

### 核心接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/v1/chat/completions` | POST | OpenAI 协议兼容的聊天接口 |
| `/v1/models` | GET | 获取可用模型列表 |
| `/manage/gpu` | GET | 获取 GPU 状态（显存、温度、利用率） |
| `/manage/models` | GET | 获取所有模型运行状态 |
| `/manage/models/{name}/start` | POST | 启动指定模型 |
| `/manage/models/{name}/stop` | POST | 停止指定模型 |
| `/health` | GET | 健康检查 |

### 使用示例

**1. 获取 GPU 状态**
```bash
curl http://localhost:5000/manage/gpu
```

**2. 启动模型**
```bash
curl -X POST http://localhost:5000/manage/models/gemma-2-9b/start
```

**3. 聊天请求（OpenAI 格式）**
```bash
curl -X POST http://localhost:5000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma-2-9b",
    "messages": [{"role": "user", "content": "你好"}],
    "stream": true
  }'
```

---

## 📦 部署指南

### Systemd 服务部署

1. 复制服务配置文件：
```bash
sudo cp systemd/*.service /etc/systemd/system/
```

2. 重新加载 systemd：
```bash
sudo systemctl daemon-reload
```

3. 启用并启动服务：
```bash
sudo systemctl enable ai-controller
sudo systemctl start ai-controller
```

4. 查看服务状态：
```bash
sudo systemctl status ai-controller
```

### 与 AIClient-2-API 集成

1. 登录 AIClient-2-API 管理后台
2. 添加新的自定义渠道（Custom Provider）
3. 设置：
   - **类型**: Custom 或 OpenAI
   - **Base URL**: `http://localhost:5000`
   - **API Key**: 任意值（本地使用不验证）

---

## 📁 项目结构

```
app-controller/
├── main.py              # FastAPI 入口，定义 API 路由
├── config.yaml          # 模型配置文件（模型名→服务名→端口映射）
├── requirements.txt     # Python 依赖列表
├── README.md            # 项目说明文档
├── core/
│   ├── monitor.py       # GPU 显存监控模块（基于 nvidia-smi）
│   ├── scheduler.py     # 智能调度逻辑（显存检查、模型启停）
│   └── sys_ctl.py       # Systemd 进程控制模块
├── api/
│   └── proxy_vllm.py    # vLLM 请求代理模块
└── systemd/
    ├── ai-controller.service    # AI Controller 服务配置
    ├── vllm-gemma.service       # Gemma 模型服务配置
    └── vllm-llama.service       # Llama 模型服务配置
```

---

## ✨ 核心特性

1. **智能模型启动**：收到请求时自动检查并启动模型
2. **显存保护**：剩余显存不足时返回 503 错误，防止炸显存
3. **Systemd 集成**：通过 systemctl 可靠地管理模型生命周期
4. **流式响应支持**：完整支持 SSE 流式输出
5. **灵活配置**：通过 YAML 文件轻松配置多个模型
6. **实时监控**：提供 GPU 状态和模型状态 API

---

## 🛠️ 开发说明

### 核心模块职责

| 模块 | 职责 |
|------|------|
| `core/monitor.py` | 读取 nvidia-smi 获取 GPU 实时数据 |
| `core/sys_ctl.py` | 执行 systemctl 命令控制服务启停 |
| `core/scheduler.py` | 判断显存是否充足、模型是否运行 |
| `api/proxy_vllm.py` | 将请求转发给真正的 vLLM 端口 |

### 扩展建议

1. **模型热切换**：引入预加载/常驻策略，实现秒级切换
2. **显存碎片回收**：通过 vLLM API 参数动态调整显存利用率
3. **Redis 队列**：实现流量削峰的并发控制
4. **WebSocket 监控**：实时推送 GPU 状态到前端

---

## 📄 许可证

MIT License

---

## 📞 联系方式

如有问题或建议，欢迎提交 Issue 或 PR。