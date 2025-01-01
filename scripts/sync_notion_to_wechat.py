import os
import requests
from notion_client import Client
from dotenv import load_dotenv
load_dotenv()

# Notion API 配置
NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
PAGE_ID = "16e96ee0-ac35-8078-9c9a-c743d0f3e841"

if not NOTION_API_TOKEN:
    raise ValueError("请设置 NOTION_API_TOKEN 环境变量")

# 初始化 Notion 客户端
notion = Client(auth=NOTION_API_TOKEN)

def get_access_token(app_id, app_secret):
    """获取公众号 Access Token"""
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    response = requests.get(url).json()
    return response.get("access_token")

def publish_to_wechat(access_token, title, content):
    """发布文章到微信公众号"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    data = {
        "articles": [
            {
                "title": title,
                "content": content,
                "author": "作者",
                "digest": "摘要内容",
                "show_cover_pic": 1
            }
        ]
    }
    response = requests.post(url, json=data).json()
    return response

def main():
    """主函数"""
    # 获取微信公众号 Access Token
    APP_ID = os.getenv("WECHAT_APP_ID")
    APP_SECRET = os.getenv("WECHAT_APP_SECRET")
    
    if not APP_ID or not APP_SECRET:
        raise ValueError("请设置 WECHAT_APP_ID 和 WECHAT_APP_SECRET 环境变量")
    
    access_token = get_access_token(APP_ID, APP_SECRET)
    
    # 从Notion获取内容并发布到微信公众号
    # 这里需要实现从Notion获取内容的逻辑
    # 然后调用publish_to_wechat函数发布内容

if __name__ == "__main__":
    main()
