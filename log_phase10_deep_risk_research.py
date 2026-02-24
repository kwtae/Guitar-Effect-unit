import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_notion_logger import create_log_subpage, create_code_block

korean_detailed_docs = """
# ⚠️ Phase 10 보완 : 글로벌 클라우드 허브 스케일 아웃 시나리오에서의 딥 리스크(Deep Risk) 예상 및 방어 전략

수만 대의 라즈베리 파이(AI 기타 페달)가 하나의 클라우드 서버와 동기화되는 **Edge-to-Cloud(Federated Learning)** 환경에서는 치명적인 리스크들이 도사리고 있습니다. 이를 사전에 예측하고 방어하는 3대 아키텍처 전략을 수립했습니다.

---

## 🚫 1. 데이터 포이즈닝 (Data Poisoning from Crowdsourcing)
**[예상 리스크]**
* 전 세계 사용자가 자신의 RLHF(오답노트)를 클라우드에 공유하게 되면, 악의적인 유저(Troll)나 잘못된 귀를 가진 초보자가 "이게 마샬 톤이야!" 라며 쓰레기 파라미터를 수천 개 업로드할 수 있습니다.
* 무분별하게 이 데이터가 Global Vector DB(ChromaDB)에 섞여 들어가면, 전체 AI의 지능과 톤 추천 정확도가 순식간에 붕괴(Degradation)됩니다.

**[방어 아키텍처 (Poisoning Mitigation)]**
* **신뢰도 가중치 (Trust Score Mechanism):** 카르마(Karma) 시스템을 도입합니다. 특정 유저가 올린 커스텀 톤을 다른 사용자들이 "좋아요(Accept)" 액션으로 많이 다운로드할수록 해당 유저의 가중치가 상승합니다.
* **LLM 크로스 체킹 (Phase 3 알고리즘 재활용):** 클라우드에 업로드된 유저 데이터는 즉시 족보에 섞이지 않고 `Quarantine(격리소)` 상태로 대기합니다. 서버의 Gemini AI 백엔드가 코사인 유사도를 한 번 더 검사하여 "진짜 다수가 동의할 만한 수학적 파형인가?"를 검증한 뒤 합격선만 DB에 Merge 합니다.

---

## ⏳ 2. 엣지 디바이스 동기화 충돌 (Synchronization Conflicts & Latency)
**[예상 리스크]**
* 라즈베리 파이가 오프라인 기간(Gig Mode 등) 동안 수집한 방대한 튜닝 데이터와, 클라우드의 데이터가 충돌할 수 있습니다. (예: A유저와 B유저가 똑같은 "Fuzz 1번 프리셋"을 각자 다르게 수정해서 동시에 업로드하는 경우)
* 페달의 통신 환경(느린 와이파이, 끊김) 때문에 동기화 도중 데이터가 유실(Data Loss)될 수 있습니다.

**[방어 아키텍처 (Conflict Resolution)]**
* **Event Sourcing & UUID:** SQL의 단순 `UPDATE`가 아닌 `INSERT` 기반의 이벤트 소싱 기법을 씁니다. 유저가 노브를 돌린 모든 행동은 고유의 `uuid`를 가진 분리된 타임스탬프 이벤트로 로컬 DB에 차곡차곡 쌓입니다.
* 이후 서버에 연결되면 덮어쓰기(Overwrite)가 아니라 **Merge(병합)** 되며, 충돌 시에는 항상 **"가장 늦게 수정된 클라우드의 최종 반영본(Last-Write-Wins)"** 또는 "유저별 브랜치(Personal Branch) 분리" 정책을 따릅니다.

---

## 🔐 3. OAuth 보안 및 JWT 토큰 탈취 (IoT Security Breach)
**[예상 리스크]**
* 라즈베리 파이처럼 물리적으로 접근 가능한 IoT 기기 내부에 클라우드 관리자용 API Key가 하드코딩 되어있다면, 해커가 페달을 뜯어서 SD카드를 복사해 메인 서버를 해킹할 수 있습니다.

**[방어 아키텍처 (IoT Hardening)]**
* **Short-Lived JWT (단기 토큰):** 하드코딩된 API Key를 절대 쓰지 않습니다. 사용자가 모바일 앱(Phase 9) 로그인을 통해 페달에 Bluetooth로 `1시간짜리 임시 JWT 토큰`만 쏴줍니다. 
* 페달은 이 1시간짜리 토큰을 들고 클라우드 동기화를 수행하며, 페달을 도둑맞더라도 해커는 1시간 뒤 만료되는 키보드 조각만 얻게 되어 서버는 안전합니다. 
"""

log_title = "Phase 10 Deep Research: 대규모 Edge-Cloud 연동 시 데이터 포이즈닝(Data Poisoning) 및 동기화/보안 취약점 방어 전략"
korean_desc = "사용자가 요청한 '리스크 예상 및 딥 리서치' 에 대한 결과 보고서입니다. Federated Learning 환경에서 악성 유저의 쓰레기 데이터로 인해 전체 AI 지능이 붕괴되는 현상을 막기 위한 신뢰도 아키텍처, 엣지 디바이스 오프라인 동기화 충돌 방어, 하드웨어 탈취 시 클라우드를 보호하는 JWT 보안 토큰 전략을 수록했습니다."

blocks = []

blocks.append({
    "object": "block",
    "type": "callout",
    "callout": {
        "rich_text": [{"type": "text", "text": {"content": "엔터프라이즈급 확장 시 가장 위험한 '데이터 붕괴(포이즈닝)', '동기화 충돌', '기기 탈취 보안' 3대 취약점을 심층 분석하고 소프트웨어적으로 완벽히 방어한 설계도입니다."}}],
        "icon": {"emoji": "⚠️"},
        "color": "red_background"
    }
})

blocks.extend(create_code_block("markdown", korean_detailed_docs))
create_log_subpage(log_title, korean_desc, blocks)
