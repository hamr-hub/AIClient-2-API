<div align="center">

<img src="src/img/logo-mid.webp" alt="logo"  style="width: 128px; height: 128px;margin-bottom: 3px;">

# AIClient-2-API 🚀

**一个能将多种仅客户端内使用的大模型 API（Gemini CLI, Antigravity, Codex, Grok, Kiro ...），模拟请求，统一封装为本地 OpenAI 兼容接口的强大代理。**

<a href="https://trendshift.io/repositories/15832" target="_blank"><img src="https://trendshift.io/api/badge/repositories/15832" alt="justlovemaki%2FAIClient-2-API | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
</div>

<div align="center">

<a href="https://deepwiki.com/justlikemaki/AIClient-2-API"><img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki"  style="width: 134px; height: 23px;margin-bottom: 3px;"></a>

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Node.js](https://img.shields.io/badge/Node.js-≥20.0.0-green.svg)](https://nodejs.org/)
[![Docker](https://img.shields.io/badge/docker-≥20.0.0-blue.svg)](https://hub.docker.com/r/justlikemaki/aiclient-2-api)
[![GitHub stars](https://img.shields.io/github/stars/justlovemaki/AIClient-2-API.svg?style=flat&label=Star)](https://github.com/justlovemaki/AIClient-2-API/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/justlovemaki/AIClient-2-API.svg)](https://github.com/justlovemaki/AIClient-2-API/issues)

[**🔧 OpenClaw 配置**](./docs/OPENCLAW_CONFIG_GUIDE-ZH.md) | [**👉 中文**](./README-ZH.md) | [English](./README.md) | [日本語](./README-JA.md) | [**📚 完整文档**](https://aiproxy.justlikemaki.vip/zh/)

</div>

## 💎 赞助商

<table width="100%">
  <tr>
    <td width="25%" align="center" valign="middle">
      <a href="https://www.packyapi.com/register?aff=AIClient2API">
        <img src="static/packycode.png" alt="PackyCode Sponsor" width="180">
      </a>
    </td>
    <td width="75%" align="left" valign="middle">
      PackyCode 是一家可靠且高效的 API 中转服务商，提供 Claude Code、Codex、Gemini 等模型的中转服务。PackyCode 为本软件用户提供特别优惠：<a href="https://www.packyapi.com/register?aff=AIClient2API">通过此链接注册</a>并在充值时输入 <strong>AIClient2API</strong> 优惠码，即可享受 <strong>10% 的折扣</strong>。
    </td>
  </tr>
  <tr>
    <td width="25%" align="center" valign="middle">
      <a href="https://www.aicodemirror.com/register?invitecode=5BUE62">
        <img src="static/aicodemirror.jpg" alt="AICodeMirror Sponsor" width="180">
      </a>
    </td>
    <td width="75%" align="left" valign="middle">
      感谢 AICodeMirror 赞助本项目！AICodeMirror 为 Claude Code / Codex / Gemini CLI 提供官方高稳定性中转服务，具备企业级并发能力、快速开票和 7/24 专属技术支持。Claude Code / Codex / Gemini 官方渠道价格仅为原价的 38% / 2% / 9%，充值还有额外优惠！AICodeMirror 为 AIClient-2-API 用户提供专属福利：<a href="https://www.aicodemirror.com/register?invitecode=5BUE62">通过此链接注册</a>即可享受首充 <strong>8折（20% off）</strong> 优惠，企业客户最高可享 75折（25% off）！
    </td>
  </tr>
  <tr>
    <td width="25%" align="center" valign="middle">
      <a href="https://www.lingtrue.com/register?aff=MP34">
        <img src="static/lingtrueapi.png" alt="LingtrueAPI Sponsor" width="180">
      </a>
    </td>
    <td width="75%" align="left" valign="middle">
      感谢 LingtrueAPI 对本项目的赞助！LingtrueAPI 是一家全球大模型API中转服务平台，提供Claude opus 4.6、GPT 5.4、Gemini 3.1 pro等多种模型API调用服务，致力于让用户以低成本、高稳定性链接全球AI能力,最大化生产效率。LingtrueAPI为本软件用户提供了特别优惠：<a href="https://www.lingtrue.com/register?aff=MP34">通过此链接注册</a>并在首次充值时输入 <strong>LingtrueAPI</strong> 优惠码即可享受 <strong>9折优惠</strong>。
    </td>
  </tr>
  <tr>
    <td width="25%" align="center" valign="middle">
      <a href="https://poixe.com/i/ebmvga">
        <img src="static/poixeai.png" alt="Poixe AI Sponsor" width="180">
      </a>
    </td>
    <td width="75%" align="left" valign="middle">
      Poixe AI 提供可靠的 AI 模型接口服务，您可以使用平台提供的 LLM API 接口轻松构建 AI 产品，同时也可以成为供应商，为平台提供大模型资源以赚取收益。<a href="https://poixe.com/i/ebmvga">通过 AIClient-2-API 专属链接注册</a>，充值额外赠送 <strong>$5 美金</strong>。
    </td>
  </tr>
  <tr>
    <td width="25%" align="center" valign="middle">
      <img src="static/wechat.png" alt="Sponsor Contact" width="150">
    </td>
    <td width="75%" align="left" valign="middle">
      <strong>成为赞助商</strong><br>
      如果您有意赞助本项目，请扫描左侧微信二维码（添加时请注明来意：<strong>赞助</strong>）。
    </td>
  </tr>
</table>

---

## 🚀 项目概览

`AIClient2API` 是一个突破客户端限制的 API 代理服务，将 Gemini、Antigravity、Codex, Grok、Kiro 等原本仅限客户端内使用的免费大模型，转换为可供任何应用调用的标准 OpenAI 兼容接口。基于 Node.js 构建，支持 OpenAI、Claude、Gemini 三大协议的智能互转，让 Cherry-Studio、NextChat、Cline 等工具能够免费大量使用 Claude Opus 4.5、Gemini 3.0 Pro 等高级模型。项目采用策略模式和适配器模式的模块化架构，内置账号池管理、智能轮询、自动故障转移和健康检查机制，确保 99.9% 的服务可用性。

> [!NOTE]
> **🎉 重要里程碑**
>
> - 感谢阮一峰老师在 [周刊 359 期](https://www.ruanyifeng.com/blog/2025/08/weekly-issue-359.html) 的推荐

> **📅 版本更新日志**
> 
> <details>
> <summary>点击展开查看详细版本历史</summary>
> 
> - **2026.03.02** - 新增 Grok 协议支持，支持通过 Cookie/SSO 方式访问 xAI Grok 系列模型（Grok 3/4），支持多模态输入、图片/视频生成、自动 token 刷新及流式输出
> - **2026.01.26** - 新增 Codex 协议支持：支持 OpenAI Codex OAuth 授权接入
> - **2026.01.25** - 增强 AI 监控插件：支持监控 AI 协议转换前后的请求参数和响应。优化日志管理：统一日志格式，可视化配置
> - **2026.01.15** - 优化提供商池管理器：新增异步刷新队列机制、缓冲队列去重、全局并发控制，支持节点预热和自动过期检测
> > - **2026.01.03** - 新增主题切换功能并优化提供商池初始化，移除使用提供商默认配置的降级策略
> - **2025.12.30** - 添加主进程管理和自动更新功能
> - **2025.12.25** - 配置文件统一管理：所有配置集中到 `configs/` 目录，Docker 用户需更新挂载路径为 `-v "本地路径:/app/configs"`
> - **2025.12.11** - Docker 镜像自动构建并发布到 Docker Hub: [justlikemaki/aiclient-2-api](https://hub.docker.com/r/justlikemaki/aiclient-2-api)
> - **2025.11.30** - 新增 Antigravity 协议支持，支持通过 Google 内部接口访问 Gemini 3 Pro、Claude Sonnet 4.5 等模型
> - **2025.11.11** - 新增 Web UI 管理控制台，支持实时配置管理和健康状态监控
> - **2025.11.06** - 新增对 Gemini 3 预览版的支持，增强模型兼容性和性能优化
> - **2025.10.18** - Kiro 开放注册，新用户赠送 500 额度，已完整支持 Claude Sonnet 4.5
> - **2025.08.29** - 发布账号池管理功能，支持多账号轮询、智能故障转移和自动降级策略
>   - 配置方式：在 `configs/config.json` 中添加 `PROVIDER_POOLS_FILE_PATH` 参数
>   - 参考配置：[provider_pools.json](./configs/provider_pools.json.example)
> - **历史已开发**
>   - 支持 Gemini CLI、Kiro 等客户端2API
>   - OpenAI ,Claude ,Gemini 三协议互转，自动智能切换
> </details>

---

## 💡 核心优势

### 🎯 统一接入，一站式管理
*   **多模型统一接口**：通过标准 OpenAI 兼容协议，一次配置即可接入 Gemini、Claude、Grok、Codex、Kimi K2、MiniMax M2 等主流大模型
*   **灵活切换机制**：Path 路由、支持通过启动参数、环境变量三种方式动态切换模型，满足不同场景需求
*   **零成本迁移**：完全兼容 OpenAI API 规范，Cherry-Studio、NextChat、Cline 等工具无需修改即可使用
*   **多协议智能转换**：支持 OpenAI、Claude、Gemini 三大协议间的智能转换，实现跨协议模型调用

### 🚀 突破限制，提升效率
*   **绕过官方限制**：利用 OAuth 授权机制，有效突破 Gemini, Antigravity 等服务的免费 API 速率和配额限制
*   **TLS 指纹绕过**：内置 TLS Sidecar (Go uTLS) 模拟浏览器特征，有效绕过 Grok 等服务的 Cloudflare 403 封锁
*   **免费高级模型**：通过 Kiro API 模式免费使用 Claude Opus 4.5，降低使用成本
*   **账号池智能调度**：支持多账号轮询、自动故障转移和配置降级，确保 99.9% 服务可用性

### 🛡️ 安全可控，数据透明
*   **全链路日志记录**：捕获所有请求和响应数据，支持审计、调试
*   **私有数据集构建**：基于日志数据快速构建专属训练数据集
*   **系统提示词管理**：支持覆盖和追加两种模式，实现统一基础指令与个性化扩展的完美结合

### 🔧 开发友好，易于扩展
*   **Web UI 管理控制台**：实时配置管理、健康状态监控、API 测试和日志查看
*   **模块化架构**：基于策略模式和适配器模式，新增模型提供商仅需 3 步
*   **完整测试保障**：集成测试和单元测试覆盖率 90%+，确保代码质量
*   **容器化部署**：提供 Docker 支持，一键部署，跨平台运行

---

## 📑 快速导航

- [💡 核心优势](#-核心优势)
- [🚀 快速启动](#-快速启动)
  - [🐳 Docker 部署](#-docker-部署)
  - [⚙️ 本地部署](#-本地部署)
  - [🔧 前端工程说明](#-前端工程说明)
  - [🤝 与 app-controller 集成](#-与-app-controller-集成)
- [📋 核心功能](#-核心功能)
- [🔐 授权配置指南](#-授权配置指南)
- [📁 授权文件存储路径](#-授权文件存储路径)
- [⚙️ 高级配置](#高级配置)
- [❓ 常见问题](#-常见问题)
- [📄 开源许可](#-开源许可)
- [🙏 致谢](#-致谢)
- [⚠️ 免责声明](#️-免责声明)

---

## 🔧 使用说明

### 🚀 快速启动

使用 AIClient-2-API 最推荐的方式是通过自动化脚本启动，并直接在 **Web UI 控制台** 进行可视化配置。

