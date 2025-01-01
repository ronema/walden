# 如何使用 Notion 来同步管理你的博客和微信公众号

### **Notion + Jekyll + 公众号的详细实现**

使用 **Notion** 写作，可以享受它优秀的排版和协作功能；然后通过 API 将文章同步到 Jekyll 和微信公众号，实现一站式写作和多平台发布。以下是详细步骤：

---

### **1. 准备工作**

### **1.1 配置 Notion API**

1. 登录你的 Notion 账号，访问 [Notion Developers](https://www.notion.so/my-integrations)。
2. 创建一个新的 Integration：
    - 点击 **"New Integration"**。
    - 填写名称，比如 "Jekyll Publisher"。
    - 保存后，获得 **Integration Token**（类似 `secret_xxx`）。
3. 在 Notion 的数据库页面，点击右上角「共享 (Share)」，将你的 Integration 添加到该页面。

### **1.2 准备 Jekyll 环境**

1. 确保你的 Jekyll 环境正常运行（包括本地或托管在 GitHub Pages）。
2. 文章存储路径一般在 `_posts` 文件夹中，格式为 Markdown (`.md`) 文件。

### **1.3 微信公众号开发接口**

1. 登录你的微信公众号后台，获取 `AppID` 和 `AppSecret`。
2. 配置微信公众号接口，确保可以调用 API（如发布文章接口）。

---

### **2. 实现流程**

### **2.1 从 Notion 获取文章**

通过 Notion API，提取你在 Notion 数据库中的文章内容，转化为 Markdown 文件。

示例代码（Python）：

```python
import requests
import json

NOTION_API_TOKEN = "your_notion_integration_token"
DATABASE_ID = "your_notion_database_id"

headers = {
    "Authorization": f"Bearer {NOTION_API_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# 获取 Notion 数据库中的页面
def fetch_notion_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers)
    pages = response.json().get("results", [])
    return pages

# 获取单个页面的详细内容
def fetch_page_content(page_id):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.get(url, headers=headers)
    content = response.json()
    return content

# 示例调用
pages = fetch_notion_pages()
for page in pages:
    print(page["properties"]["Name"]["title"][0]["text"]["content"])

```

### **2.2 同步到 Jekyll**

将提取到的文章内容转化为 Markdown 文件，并存储到 Jekyll 的 `_posts` 文件夹中。

示例代码（继续 Python）：

```python
import os
from datetime import datetime

# 将文章内容转为 Markdown 文件
def save_to_jekyll(title, content):
    date = datetime.now().strftime("%Y-%m-%d")
    filename = f"./_posts/{date}-{title.replace(' ', '-').lower()}.md"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"---\n")
        file.write(f"title: {title}\n")
        file.write(f"date: {date}\n")
        file.write(f"layout: post\n")
        file.write(f"---\n\n")
        file.write(content)
    print(f"Saved to Jekyll: {filename}")

# 示例调用
for page in pages:
    title = page["properties"]["Name"]["title"][0]["text"]["content"]
    content = "文章内容（根据 fetch_page_content 提取具体段落）"
    save_to_jekyll(title, content)

```

运行后，你的文章会自动存储到 Jekyll 的 `_posts` 文件夹中。使用 `jekyll serve` 预览效果，或者推送到 GitHub Pages。

---

### **2.3 同步到微信公众号**

将文章内容通过微信公众号 API 发布到公众号平台。

示例代码（微信公众号）：

```python
# 获取公众号 Access Token
def get_access_token(app_id, app_secret):
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    response = requests.get(url).json()
    return response.get("access_token")

# 发布文章
def publish_to_wechat(access_token, title, content):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    data = {
        "articles": [
            {
                "title": title,
                "content": content,
                "author": "作者",
                "digest": "摘要内容",
                "show_cover_pic": 1,
            }
        ]
    }
    response = requests.post(url, json=data).json()
    print(response)

# 示例调用
APP_ID = "your_wechat_app_id"
APP_SECRET = "your_wechat_app_secret"
access_token = get_access_token(APP_ID, APP_SECRET)

# 发布内容
for page in pages:
    title = page["properties"]["Name"]["title"][0]["text"]["content"]
    content = "文章内容（根据 fetch_page_content 提取具体段落）"
    publish_to_wechat(access_token, title, content)

```

---

### **3. 自动化整合**

你可以将以上流程整合为一个自动化脚本，实现全流程自动运行：

1. **获取 Notion 数据库内容** → 提取标题和正文。
2. **保存为 Markdown 文件** → 同步到 Jekyll 博客。
3. **发布到微信公众号** → 调用公众号 API。

### **定时自动化**

- 使用 `crontab` 或 Windows Task Scheduler 定时运行脚本，实现每天定时同步。
- 结合 Git Hooks 或 CI/CD 工具（如 GitHub Actions），在提交文章后自动同步到 Jekyll 和公众号。