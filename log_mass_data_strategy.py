import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_notion_logger import create_log_subpage, create_code_block

korean_detailed_docs = """
# 🎸 Phase 5: 노트북 로컬 테스트를 위한 물리적 오디오 라우팅 (Audio Signal Chain)

라즈베리 파이 셋업 전, 개발하신 노트북 환경에서 에뮬레이터를 통해 가상 테스트를 진행하실 때 반드시 지켜야 할 **물리적 오디오 시그널 체인(Signal Chain)** 구성입니다.

1. **🎸 Input (입력부):** 
   - 기타 전용 55잭(TS 케이블)을 **오디오 인터페이스의 Input 1 (Hi-Z/Instrument 모드 활성화)** 에 직접 꽂습니다. (만약 제작 중인 하드웨어 페달 껍데기에 Input 잭과 True-bypass 배선이 되어있다면 페달을 거쳐서 오디오 인터페이스로 들어갑니다).
2. **💻 Processing (연산부 - 노트북):** 
   - 오디오 인터페이스가 노트북에 USB로 연결됩니다.
   - C++ JUCE 어플리케이션(Standalone 빌드)을 실행하고, 오디오 세팅에서 [입력: Input 1 / 출력: Output 1-2]를 및 **ASIO 드라이버(핵심)** 로 잡습니다.
   - 백그라운드에서는 `laptop_hardware_emulator.py` 가 켜져 방금 전 세팅한 키보드 입력(방향키, 스페이스바)을 대기합니다.
3. **🔊 Output (출력부):** 
   - 오디오 인터페이스의 Headphone 단자에 **헤드셋**을 꽂아 모니터링 하거나, 뒷면의 Line Out(L/R)을 실제 **기타 앰프(Return 단자) 혹은 스튜디오 모니터 스피커**에 연결하여 뿜어져 나오는 최종 사운드를 듣습니다.

---

# 🕸️ Phase 6: 초거대 데이터셋(Big Data) 크롤링 전략 

단순 오픈소스나 저희가 만든 5개의 더미 데이터로는 수만 가지 이펙터의 뉘앙스를 다 담을 수 없습니다. 세상에 존재하는 모든 기타 톤을 Vector DB에 욱여넣기 위한 **3가지 강력한 대규모 크롤링/수집 옵션**을 제안합니다. 이 중 원하시는 방향을 선택해 주시면 바로 수집 자동화 스크립트를 짜드리겠습니다.

## 🚀 Option 1: AI 기반 YouTube 무한 크롤링 (yt-dlp + Demucs)
**전 세계에서 가장 방대한 데이터 베이스, 유튜브(YouTube)를 빨아들이는 방법입니다.**
* **작동 원리:** "Marshall JCM800 Tone Demo" 등의 검색어로 유튜브 상위 1,000개 리뷰 영상의 오디오를 `yt-dlp` 스크립트로 일괄 다운로드합니다. 
* **AI 연계:** 영상 제목과 설명을 Gemini가 읽고 어떤 이펙터인지 태그(Tag)를 답니다.
* **정제:** 리뷰어가 말하는 목소리나 백킹 트랙을 걷어내기 위해 `Demucs` AI 음원 분리에 통과시켜 '순수 기타 솔로'만 발라낸 뒤, MFCC를 추출해 Vector DB에 넣습니다.
* **장점:** 데이터량이 무한에 가깝고, 세상에 존재하는 모든 희귀 부띠끄 페달의 소리까지 전부 채집 가능합니다.

## 🎛️ Option 2: ToneHunt / NAM 커뮤니티 스크래핑 (BeautifulSoup)
**초거대 앰프 시뮬 언어모델 커뮤니티(Neural Amp Modeler)의 유저 업로드 데이터를 가져옵니다.**
* **작동 원리:** `ToneHunt.org` 같은 앰프 톤 공유 사이트에 파이썬 크롤링 봇(Bot)을 파견합니다.
* **과정:** 유저들이 톤을 자랑하기 위해 올려둔 짧고 깨끗한 `.wav` 프리뷰 파일 수만 개를 자동 다운로드함과 동시에, 그들이 직접 텍스트로 써놓은 노브 세팅값 HTML(Gain 8, Bass 4)을 정확하게 긁어와 1:1 매칭 DB를 구성합니다.
* **장점:** 오디오 엔지니어 성향의 유저들이 올린 파일이라 이미 잡음이 없는 **초고음질의 순수 기타 시그널**이며, Demucs 분리가 필요 없이 라벨링 신뢰도가 매우 높습니다.

## 🤖 Option 3: HuggingFace Datasets API 직결 연동
**가장 엔지니어다운 스마트한 방법입니다.**
* **작동 원리:** 글로벌 AI 허브인 허깅페이스(HuggingFace)의 파이썬 API 모듈을 사용합니다.
* **과정:** 다운로드 없이 코드 몇 줄로 `GuitarSet` 이나 `EGDB` 같은 대규모 학술용 오디오 데이터셋의 스트림(Stream)을 바로 열어서 MFCC 벡터를 뽑아냅니다.
* **장점:** 크롤링 차단(CAPTCHA) 위험이 없고 데이터 구조가 가장 깨끗하게 정리되어 있어 즉각적인 대량 학습 테스트에 유리합니다.

이 세 가지 옵션(유튜브 / ToneHunt / HuggingFace) 중 어느 쪽이 사용자님의 초기 비전에 제일 잘 맞으실지, 혹은 3개를 동시에 섞는 하이브리드 파이프라인을 구축할지 지시해 주시면 즉각 크롤러 개발(Phase 6 코딩)에 착수하겠습니다!
"""

log_title = "Phase 5/6: 노트북 로컬 테스트 오디오 라우팅 환경 및 대규모 데이터셋 크롤링(Big Data) 3대 전략 기획안"
korean_desc = "사용자의 요청에 맞춰 (1) C++ JUCE와 에뮬레이터를 동시에 굴리기 위한 물리적 오디오 인터페이스 입출력 구조를 명시하고, (2) Vector DB를 꽉 채우기 위한 3대 데이터 수집 파이프라인(유튜브 영상 분리 / NAM 커뮤니티 크롤링 / 허깅페이스 API) 전략의 장단점을 한국어로 보고하는 문서입니다."

blocks = []

blocks.append({
    "object": "block",
    "type": "callout",
    "callout": {
        "rich_text": [{"type": "text", "text": {"content": "성공적인 에뮬레이터 테스트를 위한 Audio Interface 연결도와, 세상의 모든 기타 톤을 수집하기 위한 3가지 무한 크롤링(Crawling) 전략이 포함되어 있습니다."}}],
        "icon": {"emoji": "🕸️"},
        "color": "red_background"
    }
})

blocks.extend(create_code_block("markdown", korean_detailed_docs))
create_log_subpage(log_title, korean_desc, blocks)
