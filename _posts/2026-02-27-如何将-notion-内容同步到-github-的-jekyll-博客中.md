---
title: 如何将 notion 内容同步到 GitHub 的 jekyll 博客中
date: 2026-02-27
layout: post
banner:
  image: https://images.unsplash.com/photo-1649451844931-57e22fc82de3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2OTIwMzJ8MHwxfHJhbmRvbXx8fHx8fHx8fDE3NzIxODg4NTl8&ixlib=rb-4.1.0&q=80&w=1080
  opacity: 0.618
  background: "#000"
  height: "100vh"
  min_height: "38vh"
  heading_style: "font-size: 4.25em; font-weight: bold; text-decoration: underline"
  subheading_style: "color: gold"
---

# Notion 同步到 Jekyll 博客的实现方式

## 简要步骤

### 1. 获取 Notion API Token 和页面 ID

1. 登录 Notion，访问 Notion Developers。

1. 创建一个新的 Integration，获取 API Token。

1. 在 Notion 页面中，点击右上角的「Share」按钮，将 Integration 添加到页面。

1. 获取 Notion 页面 ID：

- 打开要同步的 Notion 页面。

- 在浏览器地址栏中，复制页面 URL 中 https://www.notion.so/ 后面的部分。

- 如果 URL 中包含 -，请将其删除，保留 32 位字符的页面 ID。

### 2. 配置环境变量

1. 在项目根目录创建 .env 文件。

1. 添加以下内容：

```javascript
NOTION_API_TOKEN=your_notion_integration_token
```

### 3. 配置 GitHub Actions 自动化工作流

1. 在 .github/workflows/ 目录下创建 sync_notion.yml 文件。

1. 添加以下内容：

```yaml
name: Sync Notion to Jekyll
on:
  schedule:
    - cron: '0 0 * * *' # 每天 UTC 时间 00:00（北京时间 08:00）运行
  workflow_dispatch: # 支持手动触发
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run sync script
        env:
          NOTION_API_TOKEN: ${{ secrets.NOTION_API_TOKEN }}
        run: python scripts/sync_notion_to_jekyll.py
      - name: Commit and push changes
        run: |
          git config --global user.name "GitHub Actions"
          git config --global user.email "actions@github.com"
          git add .
          git commit -m "Sync Notion content"
          git push
```

### 4. 实现同步

1. 运行脚本：python3 scripts/sync_notion_to_jekyll.py。

1. 脚本会自动将 Notion 内容同步到 Jekyll 博客的 _posts 目录。

1. GitHub Actions 会按照设定的时间自动运行同步任务。

## 功能概述

本脚本用于将 Notion 中的内容同步到 Jekyll 博客。它通过 Notion API 获取页面内容，将其转换为 Markdown 格式，并保存到 Jekyll 的 _posts 目录中。支持处理多种 Notion 块类型，如段落、标题、列表、代码块、图片等。

## 详细实现过程

### 1. 环境配置

- 使用 dotenv 加载环境变量，包括 Notion API Token。

- 初始化 Notion 客户端。

### 2. 获取 Notion 页面内容

- 通过 get_page_content 函数获取指定页面的内容。

- 递归处理子页面。

- 使用 process_block_content 函数处理不同类型的 Notion 块。

### 3. 内容处理

- 将 Notion 块转换为 Markdown 格式。

- 支持处理以下块类型：

- 段落 (paragraph)

- 标题 (heading_1, heading_2, heading_3)

- 列表 (bulleted_list_item, numbered_list_item)

- 代码块 (code)

- 图片 (image)

- 引用 (quote)

- 分隔线 (divider)

- 子页面 (child_page)

### 4. 保存为 Markdown 文件

- 使用 save_to_markdown 函数将处理后的内容保存到 _posts 目录。

- 文件名格式为 YYYY-MM-DD-title.md。

- 自动生成文章元数据，包括标题、日期和布局。

### 5. 图片处理

- 通过 Unsplash API 获取与文章标题相关的图片作为横幅。

- 支持处理 Notion 中的图片块，直接使用图片 URL。

## 关键代码

### 初始化 Notion 客户端

```python
NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
notion = Client(auth=NOTION_API_TOKEN)
```

### 获取页面内容

```python
def get_page_content(page_id):
    page = notion.pages.retrieve(page_id=page_id)
    title = page['properties']['title']['title'][0]['plain_text']
    blocks = notion.blocks.children.list(block_id=page_id)
    # 处理块内容
```

### 处理块内容

```python
def process_block_content(block):
    block_type = block['type']
    if block_type == 'paragraph':
        text = block[block_type]['rich_text']
        return ''.join([t['plain_text'] for t in text])
    # 处理其他块类型
```

### 保存为 Markdown

```python
def save_to_markdown(title, content):
    date = datetime.now().strftime("%Y-%m-%d")
    filename = f"_posts/{date}-{title.replace(' ', '-').lower()}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f"title: {title}\n")
        f.write(f"date: {date}\n")
        f.write("layout: post\n")
        f.write("---\n\n")
        f.write("\n\n".join(content))
```

## 使用说明

1. 配置 Notion API Token 和环境变量。

1. 运行脚本：python3 scripts/sync_notion_to_jekyll.py。

1. 脚本会自动将 Notion 内容同步到 Jekyll 博客的 _posts 目录。

## 注意事项

- 确保 Notion 页面已与集成共享。

- 根据需要调整 Markdown 文件的元数据和格式。

## 常见问题与解决方案

### 1. GitHub Actions 推送失败（403 错误）

### 原因分析

- GitHub Actions 默认没有仓库的写权限

- 需要配置正确的权限才能推送更改

### 解决方案

1. 配置仓库 Actions 权限：

- 打开 GitHub 仓库页面

- 点击 Settings -> Actions -> General

- 找到 "Workflow permissions"

- 选择 "Read and write permissions"

- 保存更改

1. 配置 Personal Access Token（PAT）：

- 登录 GitHub 账户

- 点击右上角头像 -> Settings -> Developer settings -> Personal access tokens -> Tokens (classic)

- 点击 "Generate new token" -> "Generate new token (classic)"

- 选择以下权限：

- 生成并复制 token

1. 在仓库中配置 PAT：

- 打开仓库页面

- 点击 Settings -> Secrets and variables -> Actions

- 点击 "New repository secret"

- 名称输入 GH_PAT

- 值粘贴刚才复制的 token

- 点击 Add secret

1. 修改工作流配置：

```yaml
- name: Commit and push changes
  env:
    GH_PAT: ${{ secrets.GH_PAT }}
  run: |
    git config --global user.name "GitHub Actions"
    git config --global user.email "actions@github.com"
    git remote set-url origin https://x-access-token:$GH_PAT@github.com/$GITHUB_REPOSITORY.git
    git add _posts/
    git commit -m "Automated sync from Notion" || echo "No changes to commit"
    git push origin main
```

## 2. 其他常见错误

### ModuleNotFoundError: No module named 'dotenv'

- 解决方案：在 requirements.txt 中添加 python-dotenv 依赖

- 修改 GitHub Actions 工作流：

```yaml
- name: Install dependencies
  run: pip install notion-client requests python-dotenv
```

### Notion API 认证失败

- 检查 .env 文件中的 NOTION_API_TOKEN 是否正确