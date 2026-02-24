import urllib.request
import json

import os
TOKEN = os.environ.get("NOTION_TOKEN", "your_notion_token_here")
PAGE_ID = os.environ.get("NOTION_PAGE_ID", "your_page_id_here")
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def create_database(parent_page_id, title):
    url = "https://api.notion.com/v1/databases"
    data = json.dumps({
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": title}}],
        "properties": {
            "Task Name": {"title": {}},
            "Status": {"select": {
                "options": [
                    {"name": "To Do", "color": "red"},
                    {"name": "In Progress", "color": "blue"},
                    {"name": "Done", "color": "green"}
                ]
            }},
            "Component": {"select": {
                "options": [
                    {"name": "Tier 1 (HW/DSP)", "color": "orange"},
                    {"name": "Tier 2 (Mobile App)", "color": "purple"},
                    {"name": "Tier 3 (Cloud/AI)", "color": "pink"}
                ]
            }}
        }
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read())
            print(f"✅ Created Task Database: {title}")
            return res['id']
    except urllib.error.HTTPError as e:
        print(f"❌ Failed to create DB: {e.read().decode()}")
        return None

def create_page(parent_page_id, title, icon="📄"):
    url = "https://api.notion.com/v1/pages"
    data = json.dumps({
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "icon": {"type": "emoji", "emoji": icon},
        "properties": {
            "title": [{"type": "text", "text": {"content": title}}]
        }
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read())
            print(f"✅ Created Page: {title}")
            return res['id']
    except urllib.error.HTTPError as e:
        print(f"❌ Failed to create page: {e.read().decode()}")
        return None

def main():
    print("🚀 Setting up Notion Workspace...")
    create_database(PAGE_ID, "🛠️ Project Tasks & Backlog")
    create_page(PAGE_ID, "📝 Master Architecture & Documentation", "🏛️")
    create_page(PAGE_ID, "📊 Research & Data Logs", "📈")
    print("✅ Workspace structured successfully. You can drag and drop existing content into these pages.")

if __name__ == "__main__":
    main()
