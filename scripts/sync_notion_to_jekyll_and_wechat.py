import os
import requests
from notion_client import Client
import json
from datetime import datetime

from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def translate_title(title):
    """将中文标题翻译为英文"""
    # 常见技术术语翻译字典
    translation_dict = {
        'notion': 'notion',
        '同步': 'sync',
        'jekyll': 'jekyll',
        '页面': 'page',
        '关键': 'key',
        '问题': 'issue',
        '网站': 'website',
        '互动': 'interaction',
        '设计': 'design',
        '疑问': 'question',
        '如何': 'how',
        '使用': 'use',
        '管理': 'manage',
        '博客': 'blog',
        '微信': 'wechat',
        '公众号': 'official account'
    }
    
    # 将标题按空格分割并翻译
    words = title.split()
    translated_words = [translation_dict.get(word, word) for word in words]
    return ' '.join(translated_words)

def get_unsplash_image(title, width=1200, height=800):
    """通过Unsplash API获取与标题相关的图片"""
    UNSPLASH_ACCESS_KEY = "nyqPuIzXl-mYVJruwXUGb4B4RFrMSe-1zqUKdp6vZZA"
    url = "https://api.unsplash.com/photos/random"
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }
    
    # 翻译标题为英文
    english_title = translate_title(title)
    params = {
        "query": title,
        "orientation": "landscape",
        "w": width,
        "h": height,
        "content_filter": "high",
        "order_by": "relevant"
    }
    
    # 配置重试机制
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    
    try:
        response = session.get(url, headers=headers, params=params, timeout=10, verify=False)
        response.raise_for_status()
        data = response.json()
        return data["urls"]["regular"]
    except requests.exceptions.RequestException as e:
        print(f"获取Unsplash图片失败: {str(e)}")
        return None

# Notion API 配置
NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
PAGE_ID = "16e96ee0-ac35-8078-9c9a-c743d0f3e841"

if not NOTION_API_TOKEN:
    raise ValueError("请设置 NOTION_API_TOKEN 环境变量")

# 初始化 Notion 客户端
notion = Client(auth=NOTION_API_TOKEN)

def test_connection():
    """测试 API 连接"""
    try:
        response = notion.users.me()
        print("API 连接测试结果：")
        print(f"用户信息: {response}")
        return True
    except Exception as e:
        print(f"API 连接失败: {str(e)}")
        return False

def process_block_content(block):
    """处理块内容"""
    block_type = block['type']
    
    if block_type == 'paragraph':
        text = block[block_type]['rich_text']
        if text:
            return ''.join([t['plain_text'] for t in text])
    elif block_type == 'heading_1':
        text = block[block_type]['rich_text']
        if text:
            return f"# {''.join([t['plain_text'] for t in text])}"
    elif block_type == 'heading_2':
        text = block[block_type]['rich_text']
        if text:
            return f"## {''.join([t['plain_text'] for t in text])}"
    elif block_type == 'heading_3':
        text = block[block_type]['rich_text']
        if text:
            return f"### {''.join([t['plain_text'] for t in text])}"
    elif block_type == 'bulleted_list_item':
        text = block[block_type]['rich_text']
        if text:
            return f"- {''.join([t['plain_text'] for t in text])}"
    elif block_type == 'numbered_list_item':
        text = block[block_type]['rich_text']
        if text:
            return f"1. {''.join([t['plain_text'] for t in text])}"
    elif block_type == 'code':
        text = block[block_type]['rich_text']
        if text:
            code_content = ''.join([t['plain_text'] for t in text])
            language = block[block_type]['language']
            return f"```{language}\n{code_content}\n```"
    elif block_type == 'image':
        try:
            image_url = block[block_type]['file']['url']
            return f"![image]({image_url})"
        except Exception as e:
            print(f"图片处理失败: {str(e)}")
            return ""
    elif block_type == 'quote':
        text = block[block_type]['rich_text']
        if text:
            return f"> {''.join([t['plain_text'] for t in text])}"
    elif block_type == 'callout':
        text = block[block_type]['rich_text']
        if text:
            return f"**{''.join([t['plain_text'] for t in text])}**"
    elif block_type == 'divider':
        return "---"
    elif block_type == 'child_page':
        return None  # 子页面需要单独处理
    
    return None

def get_page_content(page_id):
    """获取页面内容"""
    try:
        # 获取页面信息
        page = notion.pages.retrieve(page_id=page_id)
        title = page['properties']['title']['title'][0]['plain_text']
        print(f"\n页面标题：{title}")
        
        # 获取页面块内容
        blocks = notion.blocks.children.list(block_id=page_id)
        content = []
        child_pages = []
        
        for block in blocks["results"]:
            block_type = block['type']
            print(f"\n块类型：{block_type}")
            
            if block_type == 'child_page':
                child_page_id = block['id']
                child_page_title = block['child_page']['title']
                print(f"子页面：{child_page_title} ({child_page_id})")
                child_pages.append((child_page_id, child_page_title))
            else:
                block_content = process_block_content(block)
                if block_content:
                    content.append(block_content)
                    print(f"内容：{block_content}")
        
        # 保存当前页面内容
        if content:
            save_to_markdown(title, content)
        
        # 递归处理子页面
        for child_id, child_title in child_pages:
            get_page_content(child_id)
        
        return True
    except Exception as e:
        print(f"获取页面内容失败: {str(e)}")
        return False

def save_to_markdown(title, content):
    """保存为 Markdown 文件"""
    try:
        # 确保日期在文件名最前面，并按时间倒序排列
        date = datetime.now().strftime("%Y-%m-%d")
        filename = f"_posts/{date}-{title.replace(' ', '-').lower()}.md"
        
        # 确保 _posts 目录存在
        os.makedirs("_posts", exist_ok=True)
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(f"title: {title}\n")
            f.write(f"date: {date}\n")
            f.write("layout: post\n")
            f.write("banner:\n")
            image_url = get_unsplash_image(title)
            if image_url:
                f.write(f"  image: {image_url}\n")
            else:
                f.write("  image: https://source.unsplash.com/featured/1200x800/?technology,blog\n")
            f.write("  opacity: 0.618\n")
            f.write("  background: \"#000\"\n")
            f.write("  height: \"100vh\"\n")
            f.write("  min_height: \"38vh\"\n")
            f.write("  heading_style: \"font-size: 4.25em; font-weight: bold; text-decoration: underline\"\n")
            f.write("  subheading_style: \"color: gold\"\n")
            f.write("---\n\n")
            f.write("\n\n".join(content))
        
        print(f"\n已保存到文件：{filename}")
        return True
    except Exception as e:
        print(f"保存文件失败: {str(e)}")
        return False

def main():
    """主函数"""
    if not test_connection():
        return

    print("\n获取页面内容...")
    if get_page_content(PAGE_ID):
        print("\n成功获取并保存页面内容")
    else:
        print("\n获取页面内容失败")

if __name__ == "__main__":
    main()
