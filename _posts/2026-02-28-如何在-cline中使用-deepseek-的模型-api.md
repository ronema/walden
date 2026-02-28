---
title: 如何在 Cline中使用 deepseek 的模型 api
date: 2026-02-28
layout: post
banner:
  image: https://images.unsplash.com/photo-1709842362664-c112fffc1530?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2OTIwMzJ8MHwxfHJhbmRvbXx8fHx8fHx8fDE3NzIyNjA5NTR8&ixlib=rb-4.1.0&q=80&w=1080
  opacity: 0.618
  background: "#000"
  height: "100vh"
  min_height: "38vh"
  heading_style: "font-size: 4.25em; font-weight: bold; text-decoration: underline"
  subheading_style: "color: gold"
---

### DeepSeek 集成与 Cline 插件设置指南

### DeepSeek 平台设置

1. 注册 DeepSeek 开放平台
访问 DeepSeek Platform 并完成注册流程。

1. 创建 API KEY
注册完成后，前往 API Keys 页面 创建你的 API KEY。
请确保保存生成的 API KEY，以便后续使用。

### VSCode 插件设置

1. 安装 Cline 插件
打开 VSCode 插件面板，搜索 cline。
找到 Cline 插件后，点击安装。

1. 配置 Cline 插件
安装完成后，点击 VSCode 右上角的齿轮图标，进入 Cline 插件设置。

1. 填写配置信息
在 API Provider 下拉菜单中选择 OpenAI Compatible。
在 API地址 输入框中填写 DeepSeek 的 API 地址：https://api.deepseek.com/。
在 API 密钥 输入框中填写你在 DeepSeek 生成的 API KEY。
在 Model ID 输入框中填写：deepseek-coder。

1. 完成配置
检查所有信息无误后，点击 Done 完成配置。
现在你可以开始使用 Cline 插件调用 DeepSeek 的模型能力了。