import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_notion_logger import create_log_subpage, create_code_block

korean_detailed_docs = """
# 🎸 Phase 2 완료 보고서: 하드웨어 직접 제어(GPIO) 및 초저지연 OSC 통신망 구축 

단순한 클라우드 API를 넘어, 이 프로젝트를 **"진짜 발로 밟고 손으로 돌리는 물리적인 기타 페달"**로 격상시키기 위한 **Phase 2 (Edge 디바이스 하드웨어 통합)** 작업이 모두 성공적으로 완료되었습니다.

본 단계에서 어떤 코드들이 어떻게 작성되었고, 전체 구조상 어떤 점이 보완되었는지 상세히 정리합니다.

---

## 🛠️ 1. 하드웨어 데몬 스크립트 작성 (`hardware_daemon.py`)
라즈베리 파이(Raspberry Pi) OS 백그라운드에서 24시간 쉬지 않고 돌아가며, 사용자의 물리적 조작을 감지하는 파이썬 데몬(Daemon)을 완성했습니다.

*   **물리적 조작 감지 (`gpiozero` 적용):** 
    - 3개의 로터리 인코더(Level, Tone, Gain)가 돌아가는 방향과 틱(Tick)을 감지합니다.
    - 3PDT 금속 풋스위치가 밟히는 순간(Falling-edge)을 0.1초 디바운싱(Bounce time) 처리하여 정확히 캐치합니다.
*   **LED 피드백 제어 (`PWMLED`):** 페달이 켜지면 붉은색 LED가 켜지고(Engaged), AI가 톤을 생성할 때는 푸른색 LED가 애플 로고처럼 부드럽게 숨쉬는 애니메이션(Pulsing)을 넣었습니다.
*   **머신러닝(RLHF) 연동:** 유저가 돌아간 노브 값(Delta)을 그냥 넘기지 않고, 로컬 FastAPI 서버로 `POST /rlhf-feedback/` 요청을 날려 오늘의 AI가 얼마나 톤을 못 맞췄는지(오답 노트)를 DB에 차곡차곡 쌓아줍니다.

---

## ⚡ 2. 초저지연 OSC 분산 통신 브릿지 구축 (Python ↔ C++)
단순히 노브를 돌려서 DB에만 기록하면 소용이 없겠죠? 소리를 직접 일그러뜨리는 **C++(JUCE) 오디오 엔진으로 "즉시명령"을 내리기 위해 OSC(Open Sound Control) 프로토콜을 백엔드에 통합**했습니다.

*   **Python FastAPI (`main.py` 수정):** 클라우드에서 AI가 새로운 프리셋 맵핑을 내려주면, 곧바로 `python-osc` 라이브러리를 통해 UDP 레이어로 쏜살같이 C++ 포트(9000번)로 JSON 지시사항을 발사합니다.
*   **JUCE C++ 엔진 (`PluginProcessor.cpp` 수정):** 
    - JUCE 엔진 코드에 `OSCReceiver` 상속 객체를 추가하여 항상 9000번 포트에 귀를 열고 있도록 설계했습니다.
    - 파이썬 데몬이 `/pedal/drive/gain 0.85` 라고 외치는 순간, 오디오 스레드 중단 없이 실시간으로 DriveModule의 게인 값을 동기화합니다. 기존 미디(MIDI CC) 방식이 128단계의 해상도밖에 지원하지 못하는 반면, 이 OSC 방식은 **무한한 해상도의 Float(소수점) 값을 제로-레이턴시로 C++로 전송**합니다!

---

## 🐳 3. 전체 구조 컴팩트화 및 Docker 배포 자동화
"개발자 PC에서는 잘 되는데, 공연용 라즈베리 파이에서는 안 되는데요?" 같은 문제를 원천 차단하기 위해, 이 복잡한 생태계를 도커(Docker) 컨테이너 안에 캡슐화했습니다.

*   **Dockerfile 작성:** 최소한의 파이썬 리눅스 환경(`python:3.12-slim`)을 베이스로, `uvicorn`, `fastapi`, `python-osc` 등을 한 번에 굽도록 구성했습니다.
*   **Docker Compose (`docker-compose.yml`):**
    - `ai-pedal-backend` 컨테이너 스크립트를 작성하여, 공연장에 던져진 텅 빈 라즈베리 파이라도 터미널에서 `docker-compose up -d` 한 줄만 치면 모든 백엔드 프로세스가 바로 일어납니다.
    - 특히 Sqlite 데이터베이스는 컨테이너 외부에 **볼륨(Volume) 마운트** 시켰기 때문에, 페달의 전원을 뽑았다가 내일 다시 켜도 여태껏 유저들이 노브를 돌리며 AI를 가르쳤던(RLHF) 피드백 데이터가 휘발되지 않고 영구 보존됩니다.

---

## 💡 4. 전체 구조 검토 및 Phase 3(차후 보완) 제안 사항
현재까지 물리적인 연결과 통신망이 완벽히 연동(Phase 2)되었지만, 앞으로 시스템이 스케일업(Scale-up) 하기 위해서는 다음 부분들이 보안되면 더욱 훌륭할 것입니다.

1.  **SQLite에서 PostgreSQL로의 전환:** 페달을 혼자 쓸 때는 가벼운 파일DB인 SQLite가 좋지만, 만약 100명의 연주자가 동시에 이 페달을 동기화하여 글로벌 톤 클라우드를 만든다면 `Write-Lock` 에러가 납니다. 추후 도커 컴포즈에 PostgreDB 컨테이너를 하나 더 붙이는 방향을 고려해야 합니다.
2.  **클라우드 페르소나 (Cloud Persona) 독립:** 현재는 모든 피드백 데이터를 하나로 뭉쳐서 AI의 평균 톤을 학습시킵니다. 앞으로는 앱에 '로그인' 기능을 붙여서 **"내 페달 AI는 펑크록 성향(Persona A)", "네 페달 AI는 데스메탈 성향(Persona B)"** 으로 분리 조교할 수 있게 해야 합니다.
3.  **UI 컨트롤 웹소켓 (WebSockets):** 현재 OSC는 폰트엔드(React/기기)에서 파라미터가 변경된 걸 C++로만 쏴줍니다. 반대로 누군가 물리 노브를 잡고 돌릴 때, 모바일 폰에 켜둔 React 앱 메뉴의 노브 그래픽들도 마법처럼 같이 휙휙 돌아가게 연동시키려면 FastAPI 내부에 WebSocket 방송국(Broadcaster)을 세워야 합니다.
"""

log_title = "Phase 2 Deploy: 하드웨어 데몬 스크립트 작성 및 OSC 통신망 연동 완료"
korean_desc = "사용자의 요청에 따라, Raspberry Pi용 GPIO 하드웨어 제어 데몬 작성, Python-C++ 간의 초저지연 OSC 통신 연동, 도커(Docker) 배포 캡슐화 결과와 차후 보완사항(Phase 3 제안)을 한국어로 상세히 보고하는 문서입니다."

blocks = []

blocks.append({
    "object": "block",
    "type": "callout",
    "callout": {
        "rich_text": [{"type": "text", "text": {"content": "Phase 2 코딩이 모두 완료되었습니다. 실제 라즈베리 파이 단말기에서 구동 가능한 H/W 데몬 및 OSC 통신 브릿지의 작동 원리를 정리했습니다."}}],
        "icon": {"emoji": "🚀"},
        "color": "green_background"
    }
})

blocks.extend(create_code_block("markdown", korean_detailed_docs))
create_log_subpage(log_title, korean_desc, blocks)
