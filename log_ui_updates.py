import sys
import os

# Ensure the backend is in path if necessary
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_notion_logger import create_log_subpage, create_code_block

log_title = "Update: Skeuomorphic Web UI Redesign (Physical Pedal)"
korean_desc = "웹 프론트엔드 UI를 실제 물리적인 기타 이펙터 페달(스톰프박스)과 완벽하게 동일한 외형과 조작감을 가지도록 전면 재디자인 및 로직 변경한 내용입니다."

blocks = []

blocks.append({
    "object": "block",
    "type": "heading_2",
    "heading_2": {
        "rich_text": [{"type": "text", "text": {"content": "1. 사실적인 질감 및 외형 (Skeuomorphic CSS 3D)"}}]
    }
})

blocks.append({
    "object": "block",
    "type": "paragraph",
    "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "- 밋밋한 모바일 웹 UI를 버리고, 오렌지색 파우더 코팅 메탈 케이싱 질감의 스톰프박스 외형을 CSS `radial-gradient`와 `box-shadow`의 다중 겹침으로 사실적으로 구현했습니다.\n- `index.css`에 `pedal-box` 클래스를 신설하여 빛 반사와 음영을 부여했습니다."}}]
    }
})

blocks.append({
    "object": "block",
    "type": "heading_2",
    "heading_2": {
        "rich_text": [{"type": "text", "text": {"content": "2. 다이내믹 3D 로터리 노브 (Rotary Potentiometers)"}}]
    }
})

blocks.append({
    "object": "block",
    "type": "paragraph",
    "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "- LEVEL, TONE, DIST (게인) 3개의 컨트롤 노브를 하드웨어와 동일한 홈 파인 외형으로 렌더링했습니다.\n- React의 상태값(0.0 ~ 1.0)에 따라 노브가 실제 각도(-135도 ~ +135도)로 회전(`transform: rotate`)하도록 `valToRotation` 함수를 구현하여 시각적 직관성을 극대화했습니다."}}]
    }
})

blocks.append({
    "object": "block",
    "type": "heading_2",
    "heading_2": {
        "rich_text": [{"type": "text", "text": {"content": "3. 금속 풋스위치 및 LED 리액션"}}]
    }
})

blocks.append({
    "object": "block",
    "type": "paragraph",
    "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "- 하단에 메탈 재질의 스위치를 만들어 유저의 클릭에 따라 물리적인 Z축 이동이 발생하게끔 애니메이션을 추가했습니다.\n- 상단의 상태 표시창(LED)은 AI가 톤을 생성할 때는 파란색으로 '숨쉬듯(Breathing)' 애니메이션이 들어가고, 적용된 상태에선 강렬한 빨간색으로 점등되어 하드웨어 조작의 피드백을 느끼게 합니다."}}]
    }
})

blocks.append({
    "object": "block",
    "type": "heading_2",
    "heading_2": {
        "rich_text": [{"type": "text", "text": {"content": "4. 향후 계획"}}]
    }
})

blocks.append({
    "object": "block",
    "type": "callout",
    "callout": {
        "rich_text": [{"type": "text", "text": {"content": "현재의 웹 UI 프로토타입은 향후 라즈베리 파이 + OLED 기반의 실제 하드웨어 페달로 이식될 때 동일한 조작 철학을 가지며 사용자 테스트에 사용될 예정입니다."}}],
        "icon": {"emoji": "🎸"},
        "color": "orange_background"
    }
})

create_log_subpage(log_title, korean_desc, blocks)
