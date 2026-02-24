import urllib.request
import json
import os

TOKEN = os.environ.get("NOTION_TOKEN", "your_notion_token_here")
PAGE_ID = os.environ.get("NOTION_PAGE_ID", "your_page_id_here")

def append_to_notion(title, content):
    url = f"https://api.notion.com/v1/blocks/{PAGE_ID}/children"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    children = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": title}}]
            }
        }
    ]
    
    # Text in code block is limited to 2000 chars by Notion API
    chunk_size = 1950 
    current_block = ""
    lines = content.split('\n')
    
    for line in lines:
        if len(current_block) + len(line) + 1 > chunk_size:
            children.append({
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": [{"type": "text", "text": {"content": current_block.rstrip()}}],
                    "language": "markdown"
                }
            })
            current_block = line + '\n'
        else:
            current_block += line + '\n'
            
    if current_block.strip():
        children.append({
            "object": "block",
            "type": "code",
            "code": {
                "rich_text": [{"type": "text", "text": {"content": current_block.rstrip()}}],
                "language": "markdown"
            }
        })

    data = json.dumps({"children": children}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="PATCH")
    
    try:
        with urllib.request.urlopen(req) as response:
            res = response.read()
            print(f"✅ Successfully synced: {title}")
    except urllib.error.HTTPError as e:
        print(f"❌ Failed to sync {title}: {e.code} {e.read().decode('utf-8')}")

def main():
    print("🚀 Starting Notion Sync...")
    files_to_sync = {
        '마스터플랜 (Implementation Plan)': r'C:\Users\wontae\.gemini\antigravity\brain\a7dffb41-a79e-426c-87fb-fed640263c40\implementation_plan.md',
        '태스크 목록 (Task List)': r'C:\Users\wontae\.gemini\antigravity\brain\a7dffb41-a79e-426c-87fb-fed640263c40\task.md'
    }
    
    for title, filepath in files_to_sync.items():
        if os.path.exists(filepath):
            print(f"Reading: {filepath}")
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            append_to_notion(title, content)
        else:
            print(f"⚠️ File not found: {filepath}")

if __name__ == "__main__":
    main()
