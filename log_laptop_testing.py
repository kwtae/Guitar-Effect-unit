import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_notion_logger import create_log_subpage, create_code_block

korean_detailed_docs = """
# 💻 Phase 5: 라즈베리 파이 없이 내 노트북에서 하드웨어 연동 테스트하기 (Emulator)

사용자께서 **"라즈베리 파이에 하드웨어를 꽂기 전에, 지금 사용 중인 일반 노트북(Windows/Mac)에서 전체 파이프라인(C++ OSC 통신 + FastAPI 학습)이 잘 도는지 먼저 테스트해 볼 수 없느냐"**고 질문해주신 점에 착안하여, 완벽한 해결책인 **가상 하드웨어 에뮬레이터(Emulator)** 스크립트를 작성했습니다.

기존에 작성했던 `hardware_daemon.py`는 `gpiozero` 모듈을 쓰기 때문에 리눅스(라즈베리 파이)에서만 구동되지만, 새로 개발된 **`laptop_hardware_emulator.py`**는 노트북의 "키보드"를 가짜 물리 노브 코드로 인식시킵니다.

---

## 🛠️ 키보드를 통한 기타 페달 완벽 시뮬레이션

별도의 회로 구성이나 납땜 없이, 터미널에서 `python laptop_hardware_emulator.py` 한 줄만 치면 내 키보드가 당장 기타 페달로 변신합니다!

### ⌨️ 시뮬레이터 조작법 매핑 (Key Bindings)
* **[Spacebar] 풋스위치 스톰프 (Bypass):** 물리적인 쇳덩이 스위치를 밟는 역할을 합니다 (이펙터 On/Off 전환).
* **[방향키 ⬆️ / ⬇️] Gain (게인) 노브:** 위로 누르면 게인이 돌려지고, 아래로 누르면 줄어듭니다.
* **[방향키 ➡️ / ⬅️] Tone (톤) 노브:** 우측 화살표가 시계방향 턴을 의미합니다.
* **[W / S 키보드] Level (볼륨) 노브:** 메인 볼륨을 조절합니다.

---

## 🚀 에뮬레이터가 백그라운드에서 진행하는 2가지 마법

내 노트북의 방향키를 한 번 누를 때, 스크립트 내부에서는 실제 라즈베리 파이에서 일어날 두 개의 완벽한 네트워크 이벤트가 동시에 발사됩니다.

1. **C++ 오디오 엔진 OSC 직결 (제로-레이턴시 제어):**
   - 위쪽 화살표를 누르는 순간, UDP 포트(9000번)를 통해 `/pedal/drive/gain 0.85` 라는 OSC 신호를 발사합니다. 
   - 사용자가 JUCE 플러그인(또는 C++ 스탠드얼론)을 켜두었다면 실시간으로 소리가 찌그러지는 것을 라이브로 모니터링할 수 있습니다.
2. **FastAPI RLHF (사용자 피드백) DB 자동 적재:**
   - 노브가 한 틱 돌아갈 때마다 백그라운드의 도커 컨테이너(FastAPI)로 냅다 `POST` 요청을 던집니다. 
   - *"지금 노트북 사용자가 게인 값을 맘에 안 들어해서 조금 올렸다!"* 라는 기록이 SQLite 데이터베이스 오답 노트에 실시간으로 차곡차곡 쌓이게 됩니다.

---

### 💡 테스트 스택 실행 순서 (노트북 유저용)
만약 오늘 퇴근 후 카페에서 테스트를 해보고 싶으시다면 다음 순서로 실행하시면 됩니다!

1. `docker-compose up -d` (백엔드 DB 컨테이너 기동)
2. C++ 오디오 엔진 켜기 (JUCE 로컬 빌드)
3. `pip install keyboard` (키보드 후킹 라이브러리 설치 - 관리자 권한 필요)
4. `python laptop_hardware_emulator.py` (에뮬레이터 구동)
5. **엔조이! 키보드 방향키를 누르면서 소리가 변하고 DB가 쌓이는 걸 확인하세요.**
"""

log_title = "Phase 5 Update: 물리 핀 없이 노트북 키보드로 페달 조작을 시뮬레이션 하는 가상 에뮬레이터(Emulator) 도입"
korean_desc = "사용자의 편의를 위해, 실제 라즈베리 파이 기기 세팅 전 윈도우/맥 환경의 키보드 방향키를 활용하여 OSC 소리 동기화 및 RLHF 백엔드 통신을 완벽히 모사해 내는 크로스-플랫폼 가상 하드웨어 테스트 환경 구축 가이드입니다."

blocks = []

blocks.append({
    "object": "block",
    "type": "callout",
    "callout": {
        "rich_text": [{"type": "text", "text": {"content": "라즈베리 파이가 수중에 없어도 걱정 마세요! 개발된 `laptop_hardware_emulator.py`를 통해 내 노트북 키보드로 완벽한 하드웨어 동작 통합 테스트가 가능합니다."}}],
        "icon": {"emoji": "💻"},
        "color": "blue_background"
    }
})

blocks.extend(create_code_block("markdown", korean_detailed_docs))
create_log_subpage(log_title, korean_desc, blocks)
