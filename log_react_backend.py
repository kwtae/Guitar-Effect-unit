from enhanced_notion_logger import create_log_subpage, create_code_block
import json

def upload_tier2_react_ui_log():
    description = """[Tier 2 모바일 앱 - React Native 스타일 컨트롤 센터 구현]
하드웨어가 아닌 사용자의 스마트폰 뷰에서 구동될 'AI Tone Studio' 모바일 앱의 프론트엔드 프로토타입입니다.
React(Vite)를 활용하여 자연어 입력(Prompt), 오디오 시뮬레이션 추출 로직, 결과로 반환된 JSON을 직관적인 UI 노브(Knob)와 체인(Chain)으로 매핑하여 표시하는 뷰를 구현하였습니다.
백엔드 로컬 서버(FastAPI)와 CORS로 완벽히 연동되어, 앱에서 '기름진 랫'을 요청하면 DB에 저장되고 즉시 모바일 UI에 렌더링 됩니다."""
    
    with open("frontend/src/App.jsx", "r", encoding="utf-8") as f:
        code_content = f.read()

    blocks = [
        {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "📱 React App (모바일 UI 컨트롤러) 코드"}}]}}
    ]
    blocks.extend(create_code_block("javascript", code_content))
    
    create_log_subpage("📱 [Tier 2] 모바일 앱 컨트롤 센터 UI 프로토타입 (React)", description, blocks)

def upload_tier3_backend_expansion_log():
    description = """[Tier 3 클라우드 API - 백엔드 기능 확장]
단순히 데이터를 넣고 읽는 수준을 넘어, 스마트폰(Frontend)과 원활한 통신을 위해 FastAPI의 CORS 미들웨어를 개방하고,
글로벌 톤 공유 공간인 'Preset Cloud'를 위해 "저장된 모든 커뮤니티 프리셋을 불러오는(GET /presets/)" 기능들을 추가 확장 완료했습니다."""
    
    with open("backend/main.py", "r", encoding="utf-8") as f:
        code_content = f.read()

    blocks = [
        {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "☁️ FastAPI 라우터 및 CORS 설정 코드"}}]}}
    ]
    blocks.extend(create_code_block("python", code_content))
    
    create_log_subpage("☁️ [Tier 3] 클라우드 API CORS 및 엔드포인트 확장", description, blocks)

if __name__ == "__main__":
    upload_tier2_react_ui_log()
    upload_tier3_backend_expansion_log()
