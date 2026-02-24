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

def log_to_notion(log_title, log_body, code_language="json"):
    """
    Finds the 'Research & Data Logs' page and appends a beautifully formatted
    log entry with a timestamp, title, and code block for readability.
    """
    page_id = search_page("Research & Data Logs")
    if not page_id:
        print("❌ 'Research & Data Logs' page not found.")
        return
        
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Text block is limited to 2000 chars. We truncate if needed for the prototype logger.
    truncated_body = textwrap.shorten(log_body, width=1990, placeholder="...[Truncated]") if len(log_body) > 2000 else log_body

    children = [
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [
                    {"type": "text", "text": {"content": f"📅 {timestamp} | "}, "annotations": {"color": "gray"}},
                    {"type": "text", "text": {"content": log_title}, "annotations": {"bold": True, "color": "blue"}}
                ]
            }
        },
        {
            "object": "block",
            "type": "code",
            "code": {
                "rich_text": [{"type": "text", "text": {"content": truncated_body}}],
                "language": code_language
            }
        },
        {
            "object": "block",
            "type": "divider",
            "divider": {}
        }
    ]
    
    data = json.dumps({"children": children}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="PATCH")
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"✅ Successfully appended log to Notion: {log_title}")
    except urllib.error.HTTPError as e:
        print(f"❌ Failed to log: {e.code} - {e.read().decode('utf-8')}")

if __name__ == "__main__":
    # Test the logging system!
    test_message = '{"status": "System Online", "module": "Notion Logger", "message": "Ready to track AI Guitar Pedal progress!"}'
    log_to_notion("Logger Setup Complete", test_message, "json")
