import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_notion_logger import create_log_subpage, create_code_block

korean_detailed_docs = """
# 📚 AI Guitar Pedal Phase 3: 대규모 사전 학습(Pre-training) 데이터 구축 파이프라인

지금까지 구축한 RLHF(유저의 직접 노브 조작 피드백) 방식은 페달이 '스스로 진화'하게 만드는데 필수적입니다. 하지만 제품을 **최초로 켰을 때 발생하는 거대한 오차(Initial Large Error)**를 줄이려면, 깡통 상태의 AI에게 **"베이스라인 기본기(Baseline Knowledge)"**를 주입하는 방대한 사전 학습(Pre-training) 과정이 선행되어야 합니다.

외부 인터넷과 기존 거대 데이터셋을 긁어와 이 기초 체력을 다지는 파이프라인(Phase 3)을 다음과 같이 설계했습니다.

---

## 🔍 1. 방대한 외부 오디오 소스(Dataset) 크롤링 및 확보 전략

기타 이펙터 및 앰프 시뮬레이션 연구를 위해 이미 학계와 오픈소스 커뮤니티에 공개된 신뢰도 높은 방대한 데이터셋들을 타겟으로 삼습니다.

1.  **오픈소스 학술 데이터셋 긁어오기 (Scraping & Download)**
    *   **IDMT-SMT-Guitar:** 다양한 픽업 종류, 주법, 수백 가지의 이펙터가 먹여진 수만 개의 기타 `.wav` 파일 오디오 클립 데이터베이스.
    *   **GuitarSet / EGDB:** 깨끗한 DI(다이렉트) 시그널과 앰프 마이킹 시그널이 쌍(Pair)으로 구성된 정교한 데이터셋.
2.  **커뮤니티 메타데이터 크롤링 (ToneHunt & NAM Community)**
    *   초거대 앰프 시뮬 언어모델인 Neural Amp Modeler(NAM) 유저 커뮤니티(ToneHunt 등)에서 사용자들이 직접 업로드한 앰프/페달 프리셋 셋팅값(게인 8, 트레블 4 등) 텍스트와, 그에 매칭되는 샘플 프리뷰 오디오 구동 파일을 봇(Bot)으로 수만 건 크롤링(Crawling)하여 수집합니다.

---

## ⚙️ 2. 대용량 일괄 추출 (Bulk Feature Extraction) 파이프라인

수집한 수백 기가바이트(GB)의 오디오 음원들을そのまま LLM에 넣을 수는 없습니다. 이를 기계가 읽기 쉬운 정답지로 압축하는 과정이 학습 DB 구축의 핵심입니다.

*   **배치 프로세싱 스크립트 구축:** 
    우리가 앞서 개발한 `extract_audio_features.py` 스크립트를 Multi-processing(다중 코어) 환경으로 개조합니다. 
*   **MFCC 지문화 (Fingerprinting):** 
    수만 개의 WAV 파일을 순회하며, 각각의 오디오를 20바이트 크기의 **음색 지문(MFCC Vector)과 밝기(Spectral Centroid)** JSON으로 순식간에 압축 변환시킵니다.
*   **Labeling (학습 쌍 맞추기):**
    이렇게 압축된 오디오 지문(MFCC) 데이터 옆에, 크롤링 때 함께 얻어온 **"텍스트 설명(ex. 60년대 영국 진공관 앰프 크런치 톤)"** 또는 **"실제 노브 셋팅값(Gain 0.7)"**을 1:1로 매칭시켜 거대한 `[Input: Audio 지문 + 텍스트] -> [Output: 정답 노브 값]` 학습용 CSV/JSON DB 테이블을 완성합니다.

---

## 🧠 3. 학습 DB를 LLM에 주입하는 2가지 마스터플랜

구축된 이 거대한 Mapped DB를 통해 Gemini(또는 오픈소스 LLM)의 기본 오답률을 제로에 가깝게 낮추는 두 가지 기술적 접근법입니다.

### 🚀 전략 A: 벡터 데이터베이스 검색 증강 생성 (RAG - 빠르고 경제적)
*   위에서 만든 수만 개의 (텍스트+MFCC) 데이터를 Pinecone, ChromaDB 같은 **Vector Database(벡터 DB)** 에 꽂아 넣습니다.
*   실제 사용자가 "웽웽거리는 퍼즈 톤"이라고 치거나 기타를 쳤을 때, Vector DB에서 **수학적으로 가장 비슷한 과거의 오디오 지문 정답 세트를 0.01초 만에 3개 정도 검색**해 옵니다.
*   이 검색된 3개의 정답지를 AI(Gemini) 프롬프트에 "컨닝 페이퍼(Few-shot)"로 끼워 넣고 질문하면, AI는 환각(Hallucination) 없이 놀라울 정도로 정확한 초기 노브 세팅값을 도출해냅니다.

### 🚀 전략 B: 모델 가중치 파인튜닝 (Supervised Fine-Tuning - 무겁고 완벽함)
*   만들어진 데이터셋 전체를 Google Cloud Vertex AI 모델 학습소에 던져 넣고, Gemini 모델 자체의 가중치(Synapse Weight)를 영구적으로 개조합니다.
*   이 과정이 끝나면 모델은 범용 챗봇이 아닌, 파라미터 매핑만을 위해 태어난 **"초정밀 기타 톤 전용 LLM"**으로 재탄생합니다. 초기 개발 비용(GPU 렌탈)이 들지만, 이후 추론 속도가 가볍고 매우 고도화됩니다.

---

이 Phase 3의 대규모 사전 학습(Pre-training) 데이터 주입이 선행된 후, 우리가 앞서 구축한 Phase 1 & 2의 **"사용자 실시간 노브 오버라이드(RLHF)"** 가 결합된다면, **구입 즉시 완벽한 소리를 내면서도 쓸수록 내 손에 맞게 진화하는 세계 유일의 마스터피스 페달**이 완성될 것입니다!
"""

log_title = "Phase 3 Blueprint: 초기 오차 최소화를 위한 대규모 사전 학습(Pre-training) 데이터 파이프라인 기획안"
korean_desc = "사용자의 추가 질문에 따라, AI 이펙터의 초기 추론 오류를 획기적으로 줄이기 위해 외부 인터넷과 오픈소스 데이터셋을 어떻게 크롤링하고(Data Scraping), 압축하여 벡터 기반 RAG 및 파인튜닝 학습 DB로 이식시킬 수 있는지에 대한 핵심 아키텍처 방법론을 자세한 한국어로 기술한 기록입니다."

blocks = []

blocks.append({
    "object": "block",
    "type": "callout",
    "callout": {
        "rich_text": [{"type": "text", "text": {"content": "초기 모델의 베이스라인 정확도를 완성하기 위한 Phase 3 사전 학습 가이드라인입니다. (Crawling ➔ Bulk MFCC Extraction ➔ Vector DB RAG/Fine-Tuning 전개도 포함)"}}],
        "icon": {"emoji": "📚"},
        "color": "pink_background"
    }
})

blocks.extend(create_code_block("markdown", korean_detailed_docs))
create_log_subpage(log_title, korean_desc, blocks)
