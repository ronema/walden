import os
from notion_client import Client
import json
from datetime import datetime

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
            return text[0]['plain_text']
    elif block_type == 'heading_1':
        text = block[block_type]['rich_text']
        if text:
            return f"# {text[0]['plain_text']}"
    elif block_type == 'heading_2':
        text = block[block_type]['rich_text']
        if text:
            return f"## {text[0]['plain_text']}"
    elif block_type == 'heading_3':
        text = block[block_type]['rich_text']
        if text:
            return f"### {text[0]['plain_text']}"
    elif block_type == 'bulleted_list_item':
        text = block[block_type]['rich_text']
        if text:
            return f"- {text[0]['plain_text']}"
    elif block_type == 'numbered_list_item':
        text = block[block_type]['rich_text']
        if text:
            return f"1. {text[0]['plain_text']}"
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
            f.write("  image: https://source.unsplash.com/1200x800/?" + title.replace(" ", ",") + "\n")
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
