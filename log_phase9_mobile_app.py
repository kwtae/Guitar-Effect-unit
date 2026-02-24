import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_notion_logger import create_log_subpage, create_code_block

korean_detailed_docs = """
# 📱 Phase 9: 모바일 네이티브 앱 (React Native) UI 및 BLE 제어 연동 완료

공연장 등 와이파이가 끊기는 현장(Offline)에서도 스마트폰을 꺼내 페달을 완벽하게 제어할 수 있는 **크로스 플랫폼 모바일 레이어** 구축을 완료했습니다. 프로젝트 폴더 내 `mobile_app_prototype` 디렉토리에 핵심 코드가 작성되었습니다.

---

## 🎸 1. Stage Gig Mode (무대용 UI) - `App.js`
무대 위, 어둡고 긴박한 상황에서 뮤지션이 발가락이나 엄지손가락 하나로 직관적으로 조작할 수 있는 **거대하고 명암비가 높은 다크 모드 뷰(View)** 를 설계했습니다.
* **BLE vs WiFi 토글 스위치:** 공연장 지하에서 와이파이가 터지지 않을 때, `Bluetooth Low Energy(BLE)` 무선 프로토콜로 전환하여 페달(라즈베리 파이)과 스마트폰을 직결시키는 핫스왑 기능을 구현했습니다.
* **Live Tweak 가상 노브:** 화면의 `+`, `-` 버튼을 누르면 그 즉시 `FastAPI(또는 BLE)` 소켓을 통해 C++ DSP 엔진으로 신호가 날아가 실시간 볼륨/게인 조율이 가능합니다.

## 👉 2. Tinder 스타일 AI 튜닝 카드 (RLHF) - `RLHFSwipeCard.js`
가장 획기적인 기능입니다. 집에서 기타를 치며 AI 파라미터를 교정(RLHF)할 때, 복잡하게 타이핑할 필요가 없습니다. 
AI가 제시한 소리를 기타로 직접 쳐보고 들어본 뒤:
* **스와이프 오른쪽 (Swipe Right 🟢):** "완벽해! 이 톤을 내 족보에 저장해 줘." -> (Vector DB 바로 이식)
* **스와이프 왼쪽 (Swipe Left 🔴):** "별로야! 소리가 너무 먹먹해, AI야 다시 만들어 봐." -> (거절 피드백과 함께 FastAPI로 오답노트 전송 후 재연산 지시)

이 두 가지 컴포넌트(`App.js`, `RLHFSwipeCard.js`)는 Expo / React Native 스택으로 작성되었으므로 안드로이드와 아이폰 양쪽에서 단일 코드로 완벽하게 구동됩니다.
이로써 우리는 단순히 "프로그램"이 아닌, 하드웨어-클라우드-모바일 앱이 삼위일체를 이루는 진짜 물리적인 "IoT 프로덕트"로 도약했습니다!
"""

log_title = "Phase 9 Release: React Native 모바일 연동, BLE 오프라인 접속 및 틴더형(Tinder) 스와이프 AI 톤 평가 UI 구축"
korean_desc = "하드웨어를 무선으로 컨트롤하고 실전 공연(Gig)에서 직관적으로 사용할 수 있도록 설계된 React Native/Expo 기반의 모바일 네이티브 앱 아키텍처 및 무선(BLE) 통신 프로토콜 구현 기록입니다."

blocks = []

blocks.append({
    "object": "block",
    "type": "callout",
    "callout": {
        "rich_text": [{"type": "text", "text": {"content": "집 안의 PC를 벗어나, 주머니 속 스마트폰으로 AI 기타 페달을 완벽히 지휘하는 모바일 연동(Phase 9) 개발 내역입니다."}}],
        "icon": {"emoji": "📱"},
        "color": "purple_background"
    }
})

blocks.extend(create_code_block("markdown", korean_detailed_docs))
create_log_subpage(log_title, korean_desc, blocks)
