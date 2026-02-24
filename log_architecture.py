import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_notion_logger import create_log_subpage, create_code_block

# Read the generated markdown layout file
with open("C:/Users/wontae/.gemini/antigravity/brain/93cd8ef8-d956-483b-b872-4bf35d0c9462/implementation_plan.md", "r", encoding="utf-8") as f:
    architecture_docs = f.read()

log_title = "Architecture Deep Dive: JUCE DSP Graph, Audio Extraction & ML Mapping"
korean_desc = "정해진 이펙터 순서를 강제하지 않는 C++ (JUCE) Graph Routing 동적 재조립 기술, Librosa를 활용한 레퍼런스 사운드 분석(MFCC) 파이프라인, 그리고 Gemini 프롬프트 매핑을 통한 프리셋 머신러닝(RLHF) 아키텍처 구현 상세 분석서입니다."

blocks = []

blocks.append({
    "object": "block",
    "type": "heading_2",
    "heading_2": {
        "rich_text": [{"type": "text", "text": {"content": "1. 핵심 기술 구조 (Core Technology)"}}]
    }
})

blocks.append({
    "object": "block",
    "type": "paragraph",
    "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "- C++(JUCE) 오디오 스레드 락(Lock)을 활용한 안전한 객체 배열(Vector) 동적 할당 및 라우팅 재조립 로직.\n- 무거운 Audio 파일을 200 Bytes의 가벼운 형태(JSON)로 줄이는 MFCC 및 Spectral Centroid 추출 기술.\n- Gemini LLM을 오디오 엔지니어로 롤플레이(Roleplay)시켜 0~1.0 사이의 float 파라미터 값으로 번역시키는 프롬프트 매핑."}}]
    }
})

blocks.append({
    "object": "block",
    "type": "heading_2",
    "heading_2": {
        "rich_text": [{"type": "text", "text": {"content": "2. Architecture Analysis (상세 문서)"}}]
    }
})

# Add the hardware documentation as code block for formatting safety in Notion
blocks.extend(create_code_block("markdown", architecture_docs))

# Add a closing
blocks.append({
    "object": "block",
    "type": "callout",
    "callout": {
        "rich_text": [{"type": "text", "text": {"content": "이 아키텍처는 유저의 피드백을 지속적으로 자가학습(RLHF)하여 점점 더 뛰어난 톤 메이킹 능력을 갖추는 '살아있는(Living)' 기타 페달을 설계하는 핵심 뼈대입니다."}}],
        "icon": {"emoji": "🧠"},
        "color": "purple_background"
    }
})

create_log_subpage(log_title, korean_desc, blocks)
