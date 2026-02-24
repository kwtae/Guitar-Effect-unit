import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_notion_logger import create_log_subpage, create_code_block

korean_detailed_docs = """
# 📊 Phase 6 보완 전략: LLM 토큰 한계(Token Limits) 극복 및 쓰레기 데이터 판별(Filtering) 가이드라인

데이터의 양이 수십만 개 단위로 넘어가는 빅데이터 크롤링 모델에서는 **LLM의 토큰(Token) 통신 한계 비용**과 **오염된 데이터를 분류하는 정확한 기준점(Threshold)** 마련이 프로젝트의 성패를 가릅니다. 사용자의 날카로운 질문에 대한 아키텍처적 해답을 다음과 같이 설계했습니다.

---

## 💰 1. 수만 개 크롤링 시 LLM "토큰 한계(Token Limit)" 극복 전략

**결론부터 말씀드리면, 순수 데이터 크롤링 및 압축 과정에서는 LLM 토큰이 단 1개도 소모되지 않습니다!**

* **로컬 오프로딩 (Local Offloading):** `yt-dlp`로 수백 기가바이트의 유튜브 영상을 긁어오고, `Demucs`로 기타만 분리한 뒤, `librosa`로 MFCC 지문을 따내는 모든 무거운 작업은 오직 **사용자님의 로컬 CPU(노트북/서버)** 연산만 사용합니다. 
* **토큰이 소모되는 유일한 순간 (Token Usage):**
  1. **교차 검증 시:** 10만 개의 데이터 중, 수학적 대조(Cosine Similarity)를 돌렸더니 파형과 이름표가 불일치하는 "이상 데이터(Anomaly)"가 딱 1,000개 발견되었다고 가정합시다. 이때 오디오를 AI에게 보내는 게 아니라, 매우 짧은 텍스트 **"유튜브 이름: 메탈, 파형: 어쿠스틱. 어떻게 할까?" (약 30 Tokens)** 만 Gemini에게 보냅니다.
  2. **유저 톤 생성 시 (RAG 검색):** 유저가 기타를 쳤을 때, Vector DB가 가장 비슷한 과거 족보 JSON 3개만 추려냅니다. 이 텍스트 레시피 3개만 Gemini에 넣으므로 1회 요청 시 **약 200~300 Tokens** (거의 무료 수준)의 초경량 통신만 발생합니다.

*이처럼 무거운 '소리'는 벡터 수학(로컬 연산)으로 처리하고, 판단이 필요한 '가벼운 텍스트' 결론만 LLM에 넘기므로 크롤링 수집의 한계치(Limit)는 사실상 무한대입니다.*

---

## 🗑️ 2. 쓰레기 데이터 vs 사용 vs 재사용 3단계 판단 기준 (Filtering Thresholds)

유튜브나 커뮤니티에서 무작위로 수집된 수만 개의 데이터 중 무엇을 버리고 살릴 것인가? `layer3_cross_validation_filter.py` 모듈이 수행하는 엄격한 수학적 기준은 다음과 같습니다.

### 🟢 1단계: 맹목적 허용 (USE) - 유사도 85% ~ 100%
* **현상:** 리뷰어가 "Classic Tube Overdrive"라고 제목을 적어둔 영상의 주파수 지문이, 학술 논문 허깅페이스 베이스라인의 "Overdrive" 지문과 85% 이상 일치하는 경우.
* **조치:** **[즉시 사용]** 데이터가 매우 정직하고 순도 높음. 묻지도 따지지도 않고 ChromaDB (Vector DB)에 영구 보존.

### 🟡 2단계: 논리적 재사용 (RE-USE / Re-classify) - 유사도 50% ~ 84%
* **현상:** 유저가 "Insane Fuzz"라고 적어놨지만, 베이스라인과 대조해보니 퍼즈(Fuzz)라기보단 강한 디스토션(Distortion)에 가까운 애매한 60% 일치율이 나오는 경우.
* **조치:** **[재가공 후 사용]** 이 데이터를 즉시 버리는 것은 아깝습니다. 이 텍스트 쪼가리를 Gemini LLM에게 보냅니다. "이 데이터가 Fuzz라기엔 파형이 약해. 'Heavy Distortion'으로 태그를 바꿔서 저장할까?" ➡️ LLM이 적합하다고 판단하면 **라벨(이름표)을 강제로 수정(Re-classify)**하여 DB에 재사용 저장합니다.

### 🔴 3단계: 완전한 쓰레기 데이터 분리 (GARBAGE) - 유사도 0% ~ 49%
* **현상:** "완벽한 기타 톤 메이킹 강좌" 라면서 다운받아보니, 유튜버가 말하는 "목소리"가 곡 처음부터 끝까지 깔려있어 Demucs 분리조차 실패한 끔찍한 오디오 파형이 추출된 경우.
* **조치:** **[즉시 영구 폐기]** 베이스라인 유사도가 49% 미만으로 떨어지는 데이터는 기타 소리가 아니거나 음향학적 가치가 전혀 없는 "독(Poison)"입니다. 연산 자원 낭비를 막기 위해 LLM에게 묻지도 않고 파이썬 단에서 **즉시 쓰레기통(Drop)**으로 버립니다.

이러한 **[85% / 50% Threshold] 가이드라인**을 적용하면, 수십만 개의 유튜브 잡동사니 데이터를 빨아들이더라도 오직 빛나는 보석 같은 '순정 기타 톤' 데이터들만 Vector DB에 살아남게 됩니다! 
"""

log_title = "Phase 6 Update: LLM Token Limit 극복 방안 및 쓰레기 데이터 적격성(Garbage vs Reuse) 필터링 기준안"
korean_desc = "대규모 크롤링 시 발생하는 LLM 토큰 제한 우려에 대한 로컬 연산-오프로딩 해결책과, 코사인 유사도(Cosine Similarity)를 활용한 3단계(사용/가공 재사용/폐기) 데이터 필터링 임계점(Threshold) 메커니즘을 상세히 기록한 문서입니다."

blocks = []

blocks.append({
    "object": "block",
    "type": "callout",
    "callout": {
        "rich_text": [{"type": "text", "text": {"content": "질문하신 토큰 한계(Token Limits) 문제와 쓰레기 파형 분류(Refining Criteria)에 대한 명확한 수학적/아키텍처적 해답 매뉴얼입니다."}}],
        "icon": {"emoji": "🗑️"},
        "color": "gray_background"
    }
})

blocks.extend(create_code_block("markdown", korean_detailed_docs))
create_log_subpage(log_title, korean_desc, blocks)
