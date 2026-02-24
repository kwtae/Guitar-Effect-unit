import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_notion_logger import create_log_subpage, create_code_block

korean_detailed_docs = """
# 🎸 AI Guitar Pedal: 핵심 아키텍처 가이드 (DSP, 사분석 및 AI 매핑 기술)

이 문서는 고정된 이펙터 연결에 얽매이지 않고, **AI 스스로 소리의 흐름을 설계하는 "지능형 기타 페달"**의 내부 기술 원리를 쉽게 풀어쓴 문서입니다.

---

## 1. 정해진 순서를 파괴하는 동적 라우팅 알고리즘 (JUCE C++ Graph Routing)

대부분의 기존 디지털 이펙터(멀티이펙터)는 `컴프레서 → 오버드라이브 → EQ → 공간계`라는 "정해진 파이프라인(순서)"을 강제합니다. 하지만 본 시스템의 C++ DSP 엔진은 이러한 틀을 깨고, AI의 판단에 따라 이펙터의 종류와 순서를 실시간으로 완전히 뜯어고치는 **다이내믹 객체 지향 렌더링(Dynamic Object-Oriented Rendering)** 방식을 사용합니다.

### 💡 작동 원리
1. **모듈의 추상화 (`EffectNode`)**: 드라이브, EQ 등 모든 이펙터 기능은 공통된 뼈대(`EffectNode`)를 상속받은 블록 장난감 같은 '객체'로 존재합니다.
2. **배열 체인 (`std::vector`)**: 메인 오디오 프로세서(`AIPedalAudioProcessor`)는 텅 빈 배열(Vector)을 쥐고 있습니다. 오디오 신호는 이 배열 속에 담긴 블록들을 1번부터 차례대로 통과할 뿐입니다.
3. **AI의 실시간 재조립 (`applyAIPreset`)**: 
   - 프론트엔드 앱에서 사용자가 새로운 톤 생성을 요청하면, 백엔드 AI가 `["eq_module", "drive_module"]` 형태의 JSON 설계도를 C++ 엔진으로 전송합니다.
   - C++ 엔진은 지직거리는 소리(팝 노이즈)를 방지하기 위해 0.001초 단위로 오디오 처리 스레드의 문을 걸어 잠급니다(**Thread Lock**).
   - 기존 배열(Vector)을 싹 비우고, AI가 보낸 순서대로 `EQ 모듈 생성` → `Drive 모듈 생성`을 하여 배열상에 꽂아 넣습니다. 
   - 동시에 AI가 골라준 수치(게인량 0.8 등)를 각 모듈에 붓고 스레드 잠금을 해제합니다.
   
**결과적으로 사용자는 오디오 끊김을 거의 느끼지 못한 채, 완전히 새로운 회로 회로도를 가진 이펙터 시스템으로 탈바꿈하게 됩니다.**

---

## 2. 깃털처럼 가벼운 레퍼런스 사운드 분석 파이프라인 (Audio Feature Extraction)

"존 메이어의 이 기타 톤이랑 똑같이 만들어줘"라며 5MB짜리 오디오(MP3/WAV) 리프를 서버(AI)로 바로 전송하면 통신 비용, 처리 시간, 해킹 위협 등 모든 면에서 최악의 효율을 낳습니다.

이 문제를 해결하기 위해, 우리는 엣지 디바이스(라즈베리 파이나 모바일 앱) 단에서 **Python Librosa 라이브러리를 활용해 소리의 "지문(Fingerprint)"만을 추출**하는 방식을 채택했습니다. (`extract_audio_features.py`)

### 🔍 추출하는 2가지 핵심 지문
1. **MFCC (Mel-Frequency Cepstral Coefficients)**: 사람이 소리의 음색을 인지하는 방식을 수학적으로 모델링하여, 20개의 숫자 차원으로 소리의 전체적인 '질감(Texture)'이나 '드라이브의 거친 정도'를 요약해 냅니다.
2. **Spectral Centroid (주파수 무게중심)**: 소리의 가장 뼈대가 되는 주파수가 어디 쏠려있는지를 찾아, 소리가 얼마나 찌르는지(밝은지) 반대로 먹먹하고 어두운지를 단 1개의 수치로 도출합니다.

**혁신 포인트:** 이 과정을 통해 5MB의 묵직한 오디오 덩어리는, **단 200 Bytes 용량의 아주 가벼운 텍스트(JSON) 조합**으로 극강의 압축이 이루어집니다. 서버는 이 숫자 배열만 받아도 원본 소리의 뉘앙스를 완벽에 가깝게 추론할 수 있습니다.

---

## 3. 오디오 엔지니어를 빙의한 프롬프트 매핑 & 머신러닝 자가 발전 (RLHF)

전통적인 NAM(Neural Amp Modeler)이나 딥러닝 톤 매칭은 한 가지 톤을 복제할 때마다 그래픽카드(GPU)를 혹사시켜 수 시간동안 가중치를 훈련해야 합니다. 이 시스템은 GPU 훈련(Training) 대신 거대언어모델(Gemini 1.5 Pro)의 추론 능력과 **강화학습 알고리즘(RLHF)**을 영리하게 믹스했습니다.

### 🧠 동작 매커니즘
1. **통역사 (Zero-Shot Mapping)**: 
   - 유저의 막연한 텍스트("빈티지하고 끈적한 솔로 톤")나, 위에서 온 오디오 지문(MFCC 수치)이 백엔드에 도착합니다.
   - 우리의 시스템 프롬프트(System Prompt)가 Gemini LLM에게 명령합니다. *"너는 세계 최고의 기타 톤 엔지니어다. 이 유저의 의도를 분석해서, 우리 C++ 이펙터가 알아들을 수 있는 0부터 1까지의 실수값 노브 세팅(Gain 0.6, Tone 0.45 등)으로 번역해라."*
   
2. **강화학습(RLHF) 기반의 자가 수정**:
   - AI가 톤을 짜줬는데, 실제 연주자가 쳐보고 "너무 답답해!"라며 실제 페달의 물리적인 톤(Tone) 노브를 손으로 확 올려버렸습니다.
   - 라즈베리 파이 데몬은 이 "AI 예측 실패와 유저의 직접 수정 기록(Delta)"을 조용히 SQLite 데이터베이스에 기록해 둡니다.
   - **이상치 제거 (IQR)**: 악의적인 유저가 노브를 극단적으로 트롤링한 데이터는 K-Means 및 사분위수(IQR) 알고리즘을 통해 깨끗하게 걸러냅니다.
   - **지수 이동 평균 (EMA) 반영**: 밤이 되면 봇이 깨어나, 정상적인 "유저 보정 평균치(예: 평균적으로 15% 더 밝은 톤을 선호함)"를 도출합니다. 그리고 모델이 급격히 바보가 되는 것을 막기 위해 기존의 AI 성향과 최신 트렌드를 8:2 (EMA)로 부드럽게 섞습니다.
   
3. **진화 (Evolution)**:
   - 다음 번에 유저가 "빈티지 솔로 톤"을 요구하면, Gemini는 어제 배운 새로운 가이드라인("사람들은 내 생각보다 조금 더 밝은 톤을 좋아해")을 스스로의 시스템 프롬프트에 더해 한층 더 정교해진 톤 수치를 뽑아냅니다.

결론적으로, 이 이펙터는 **수만 명의 연주자가 사용할수록 수백만 개의 수동 노브 수정 데이터가 축적되며, AI의 귀가 점점 더 프로듀서처럼 정확하게 진화하는 유기적인 시스템**입니다.
"""

log_title = "Architecture Deep Dive: JUCE DSP & ML Mapping (Korean Detailed Ver.)"
korean_desc = "이전 영어 병기 문서를 보다 더 가독성을 높이고, 비개발자나 프로젝트 기획자도 이해하기 쉽도록 구조화시킨 한국어 상세 아키텍처 해석본 문서입니다."

blocks = []

blocks.append({
    "object": "block",
    "type": "callout",
    "callout": {
        "rich_text": [{"type": "text", "text": {"content": "본 문서는 C++ 오디오 프로그래밍, 파이썬 데이터 추출, 그리고 프롬프트 엔지니어링이 어떻게 융합되어 AI 페달 생태계를 구성하는지 상세히 기술합니다."}}],
        "icon": {"emoji": "📖"},
        "color": "gray_background"
    }
})

# Add the hardware documentation as code block for formatting safety in Notion
blocks.extend(create_code_block("markdown", korean_detailed_docs))

create_log_subpage(log_title, korean_desc, blocks)
