import urllib.request
import json
from datetime import datetime
import textwrap

import os
TOKEN = os.environ.get("NOTION_TOKEN", "your_notion_token_here")

def search_page(title):
    url = "https://api.notion.com/v1/search"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    data = json.dumps({
        "query": title,
        "filter": {
            "value": "page",
            "property": "object"
        }
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read())
            if res["results"]:
                return res["results"][0]["id"]
    except Exception as e:
        print("Search error:", e)
    return None

def create_log_subpage(log_title, korean_description, content_blocks):
    """
    Finds the 'Research & Data Logs' page and creates a NEW SUB-PAGE inside it.
    This vastly improves readability instead of cluttering one single page.
    """
    parent_page_id = search_page("Research & Data Logs")
    if not parent_page_id:
        print("❌ 'Research & Data Logs' page not found.")
        return
        
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_title = f"{log_title} ({timestamp})"
    
    children = [
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": korean_description}}],
                "icon": {"emoji": "💡"},
                "color": "blue_background"
            }
        },
        {
            "object": "block",
            "type": "divider",
            "divider": {}
        }
    ]
    
    # Add the provided content blocks
    children.extend(content_blocks)
    
    data = json.dumps({
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "icon": {"type": "emoji", "emoji": "📝"},
        "properties": {
            "title": [{"type": "text", "text": {"content": full_title}}]
        },
        "children": children
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"✅ Successfully created sub-page: {full_title}")
    except urllib.error.HTTPError as e:
        print(f"❌ Failed to create sub-page: {e.code} - {e.read().decode('utf-8')}")

def create_code_block(language, code_text):
    """Utility to split long text into multiple code blocks if it exceeds Notion API limits"""
    blocks = []
    chunk_size = 1950
    lines = code_text.split('\n')
    current_block = ""
    
    for line in lines:
        if len(current_block) + len(line) + 1 > chunk_size:
            blocks.append({
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": [{"type": "text", "text": {"content": current_block.rstrip()}}],
                    "language": language
                }
            })
            current_block = line + '\n'
        else:
            current_block += line + '\n'
            
    if current_block.strip():
        blocks.append({
            "object": "block",
            "type": "code",
            "code": {
                "rich_text": [{"type": "text", "text": {"content": current_block.rstrip()}}],
                "language": language
            }
        })
    return blocks
