import sys
import os

# Ensure the backend is in path if necessary (though the logger is in the root directory)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_notion_logger import create_log_subpage, create_code_block

# Read the generated markdown layout file
with open("C:/Users/wontae/.gemini/antigravity/brain/93cd8ef8-d956-483b-b872-4bf35d0c9462/hardware_integration.md", "r", encoding="utf-8") as f:
    hardware_docs = f.read()

log_title = "Update: Hardware Integration, Security & ML Tuning"
korean_desc = "하드웨어 통합 가이드(라즈베리 파이 단독 실행), 백엔드 보안 강화(CORS & SlowAPI Rate Limiting), 그리고 머신러닝 이상치 제거(IQR) 및 지수이동평균(EMA) 튜닝 결과 문서입니다."

blocks = []

# Add some intro text
blocks.append({
    "object": "block",
    "type": "heading_2",
    "heading_2": {
        "rich_text": [{"type": "text", "text": {"content": "1. 서비스 인프라 및 보안 업데이트"}}]
    }
})

blocks.append({
    "object": "block",
    "type": "paragraph",
    "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "- FastAPI 백엔드에 SlowAPI 적용 (Rate Limiting) 및 엄격한 CORS 적용하여 프로토타입에서 운영환경 수준으로 보안성을 강화했습니다.\n- SQLite에서 PostgreSQL로 스위칭할 수 있도록 SQLAlchemy 셋팅을 추가하여 동시성 문제를 대비했습니다."}}]
    }
})

blocks.append({
    "object": "block",
    "type": "heading_2",
    "heading_2": {
        "rich_text": [{"type": "text", "text": {"content": "2. ML 가중치 산출 로직(RLHF) 고도화"}}]
    }
})

blocks.append({
    "object": "block",
    "type": "paragraph",
    "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "- 단순히 유저들이 수정한 노브 값의 평균을 내어 다음 프롬프트를 조율하던 기존 방식에서, IQR 알고리즘 기반 극단적 이상치(Outlier) 제거 로직을 Numpy로 구현했습니다.\n- 모델 성향이 너무 빨리 뒤집히지 않도록 데이터 트렌드를 8:2 비율로 섞는 EMA(지수이동평균) 방식을 제안 및 코드화했습니다."}}]
    }
})

blocks.append({
    "object": "block",
    "type": "heading_2",
    "heading_2": {
        "rich_text": [{"type": "text", "text": {"content": "3. Hardware Integration & Edge AI Blueprint"}}]
    }
})

# Add the hardware documentation as code block for formatting safety in Notion
blocks.extend(create_code_block("markdown", hardware_docs))

# Add a closing
blocks.append({
    "object": "block",
    "type": "callout",
    "callout": {
        "rich_text": [{"type": "text", "text": {"content": "이 사항들은 다음 페이즈 개발을 위한 아키텍처 토대가 됩니다."}}],
        "icon": {"emoji": "🚀"},
        "color": "green_background"
    }
})

create_log_subpage(log_title, korean_desc, blocks)
