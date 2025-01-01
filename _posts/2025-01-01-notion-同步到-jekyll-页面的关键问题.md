---
title: notion 同步到 jekyll 页面的关键问题
date: 2025-01-01
layout: post
banner:
  image: https://images.unsplash.com/photo-1703596645625-6a11508f7e4c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2OTIwMzJ8MHwxfHJhbmRvbXx8fHx8fHx8fDE3MzU3MjE4MjR8&ixlib=rb-4.0.3&q=80&w=1080
  opacity: 0.618
  background: "#000"
  height: "100vh"
  min_height: "38vh"
  heading_style: "font-size: 4.25em; font-weight: bold; text-decoration: underline"
  subheading_style: "color: gold"
---

问题主要出在两个地方：

1. 页面类型的混淆：

1. API 调用方式的改进：

1. 内容获取逻辑：

1. Markdown 转换：

这就是为什么最新的代码能工作的原因。我们：

1. 正确识别了内容类型（页面而不是数据库）

1. 使用了正确的 API 调用方式

1. 正确处理了页面的块结构

1. 将 Notion 的格式正确转换为 Markdown