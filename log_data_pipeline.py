import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_notion_logger import create_log_subpage, create_code_block

korean_detailed_docs = """
# 📊 AI Guitar Pedal: 머신러닝 데이터 확보 및 튜닝 파이프라인 (Data Pipeline)

이 프로젝트의 머신러닝(Gemini 프롬프트 튜닝)을 위해 수집되어 사용되는 **"학습 데이터(Training Data)"**는 외부 인터넷이나 거대한 기존 오디오 데이터셋에서 가져오는 것이 아닙니다. **100% 사용자의 물리적 조작(Human Feedback)과 오디오 분석 경험치에서 자생적으로 확보**되는 매우 효율적인 구조를 가지고 있습니다.

---

## 📥 1. 핵심 데이터 원천: 사용자의 물리적 조작 (Manual Overrides / RLHF)

AI 톤 생성의 가장 강력한 학습 데이터는 "오답 노트"에서 옵니다. 사용자가 이펙터를 튜닝하며 남긴 아쉬움 그 자체가 완벽한 학습 데이터 파이프라인이 됩니다.

*   **상황 인지:** 유저가 페달에게 "두터운 메탈 톤"을 요구했고, AI(Gemini)가 `Gain을 0.6`으로 맞춰 주었습니다.
*   **데이터 발생 (인간의 개입):** 유저가 앰프 소리를 들어보고 "쯧, 이건 너무 약해"라며 페달에 달린 진짜 **물리적 Gain 노브를 돌려서 0.85로 강제 수정(Override)** 합니다.
*   **수집 로직 (하드웨어 데몬):** 라즈베리 파이 안의 파이썬 프로그램(`hardware_daemon.py`)이 이 노브가 돌아간 각도를 감지합니다. 즉시 백엔드(FastAPI)로 신호를 보내, `[원본 AI 추론값: 0.6]` vs `[유저가 확정한 정답값: 0.85]` 사이의 **오차(Delta: +0.25)**를 계산합니다.
*   **저장 및 축적:** 이 오차 데이터와 어떤 텍스트 프롬프트("두터운 메탈 톤")에서 이 오차가 났는지가 로컬 **SQLite 데이터베이스(`RLHFFeedback` 테이블)에 차곡차곡 쌓입니다.** 마치 유저가 남긴 보완 리뷰처럼 동작합니다.

---

## 📥 2. 교보재 데이터: 레퍼런스 사운드 지문 (Reference Audio Fingerprints)

사용자가 단순히 말(Text)로만 톤을 요구하지 않고, 롤모델이 되는 기타리스트의 음원 파일(MP3/WAV)을 "이 소리랑 똑같이 내줘!"라며 앱에 업로드할 때 발생하는 데이터입니다.

*   **데이터 파이프라인 압축:** 무거운 음원 파일 전체를 통째로 서버로 보내 학습 데이터로 쓰지 않습니다. Python의 `librosa` 라이브러리(`extract_audio_features.py`)가 음원의 주파수를 분해하여, 가장 핵심적인 음색 특성 20개(`MFCC 벡터`)와 밝기(`Spectral Centroid`)를 도출해냅니다.
*   **경량화 된 정답지 축적:** 이 "시그니처 사운드 지문" 데이터는 용량이 `200 Bytes`도 안 되지만, 이 오디오 지문을 통해 궁극적으로 완성된 노브 셋팅값(`Preset` 세이브 데이터) 조합 연관관계 자체가 훌륭한 **"오디오-투-파라미터(Audio-to-Parameter)"의 지도 학습(Supervised Learning) 데이터 쌍(Pair)**이 됩니다.

---

## 📥 3. 커뮤니티 군집 데이터 (Cloud Preset Sync - Phase 2 이후 확장)

현재 시스템은 라즈베리 파이 내부의 1인 로컬 기기처럼 굴러가지만, Vercel/AWS 등으로 클라우드망에 API(`backend/main.py`)가 연결되면 데이터 수집량이 폭발적으로 늘어납니다.

*   **크라우드 소싱(Crowdsourcing):** 전 세계 100명의 연주자가 똑같은 AI 페달을 쓰면, 매일 100명분의 노브 수동 수정 데이터(오차 델타값)가 클라우드로 쏟아져 들어옵니다.
*   **페르소나 그룹핑 연산:** "블루스 연주자들은 펜더 앰프를 쓰기 때문에 기본적으로 Treble(고음)을 낮게 잡는구나", "메탈 젠트 연주자들에겐 게인 마진을 10% 더 주자" 같은 군집화(Clustering)된 빅데이터가 모입니다.
*   **공유 풀 생태계:** 유저들이 스스로 깎고 다듬어 최고의 톤으로 저장한 완성된 튜닝값(`Preset` 데이터)을 다른 연주자 디바이스끼리 블루투스나 Wi-Fi로 덮어쓰기 공유할 때마다, AI는 이 "명작(Masterpiece)" 톤들의 가이드라인 가중치를 한 번 더 강하게 업데이트하게 됩니다.

---

### 💡 결론 요약
우리의 AI는 따로 거대한 비용을 들여 수만 시간의 기타 소리 데이터를 Pre-training(사전 학습) 시키기 위해 GPU 자원을 낭비할 필요가 없습니다. 

**가장 완벽하고 순도 높은 정답 데이터인 "실제 연주자의 귀와 손가락 조작 이벤트" 자체**를 실시간으로 데이터베이스에 끊임없이 수집(`RLHF`)하여, 다음 날 아침 조금 더 똑똑한 프롬프트(LLM) 가이드라인으로 돌려쓰기 때문에 오직 **자기 객관화와 강화학습만 무한히 반복**하는 매우 효율적인 지능 생태계입니다.
"""

log_title = "Data Pipeline Deep Dive: AI 학습 데이터 수집 및 RLHF 구조"
korean_desc = "AI 기타 페달이 방대한 오디오 데이터 사전 학습 없이도 어떻게 연주자의 물리적 노브 조작(Human Feedback)과 가벼운 오디오 지문(MFCC)만을 이용해 스스로를 튜닝하고 똑똑해지는지, 3가지 핵심 데이터 파이프라인을 한국어로 상세히 풀어쓴 문서입니다."

blocks = []

blocks.append({
    "object": "block",
    "type": "callout",
    "callout": {
        "rich_text": [{"type": "text", "text": {"content": "본 문서는 사용자의 질의(모델 학습 데이터 확보 로직에 대한 궁금증)에 대해 상세히 답변한 기술 문서이며, Phase 2 개발에 앞선 인프라 정리 내용입니다."}}],
        "icon": {"emoji": "📊"},
        "color": "blue_background"
    }
})

# Add the detailed docs as code block for formatting safety in Notion
blocks.extend(create_code_block("markdown", korean_detailed_docs))

create_log_subpage(log_title, korean_desc, blocks)
