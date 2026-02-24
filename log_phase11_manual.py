import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_notion_logger import create_log_subpage, create_code_block

korean_detailed_docs = """
# 📖 AI Guitar Pedal - 공식 셋업(설치) 및 운용/유지보수 매뉴얼 (v1.0)

지금까지 기획/개발된 4,000여 개의 코드가 담긴 이 거대한 생태계를 사용자가 어떻게 실전에 투입하고 관리해야 하는지에 대한 **End-to-End 완벽 메뉴얼**입니다.

---

## 🛠️ 1. 설치 가이드 (Installation)

### 1-A. 하드웨어 플랫폼 이식 (Raspberry Pi 4 / 5 기준)
우리가 만든 `Release_v1.0.zip` 배포 파일을 빈 라즈베리 파이에 옮기는 것으로 시작됩니다.
1. 라즈베리 파이에 Ubuntu 또는 Raspberry Pi OS(64-bit)를 설치합니다.
2. 터미널(SSH)을 열고 **Docker**와 **Docker-Compose**를 설치합니다. (`sudo apt install docker.io docker-compose -y`)
3. 압축을 푼 프로젝트 폴더 전송 후, 오디오 인터페이스(또는 USB 사운드카드)를 라즈베리 파이에 꽂습니다.

### 1-B. 원클릭 소프트웨어 구동 (Software Kick-off)
프로젝트 디렉토리로 이동하여 마법의 명령어 한 줄을 입력합니다.
* **명령어:** `docker-compose up -d --build`
* **백그라운드 동작:** 스크립트가 실행됨과 동시에 `PostgreSQL`, `FastAPI(AI 백엔드)`, `ChromaDB`, `Watchtower` 4개의 코어 엔진이 스스로 격리된 컨테이너에 지어지며 1분 내로 가동됩니다.

---

## 🎸 2. 실전 운용 가이드 (Operation)

AI 페달은 환경에 따라 두 가지 폼팩터 모드로 완벽히 전환하여 사용합니다.

### 🏠 2-A. 홈 레코딩 모드 (Web Dashboard)
* **어떻게?** 같은 집안 와이파이에 연결된 노트북(맥북/윈도우) 크롬 브라우저를 켜고, `http://[라즈베리파이_IP주소]:8000` 에 접속하세요.
* **무엇을?** C-Panel이 뜹니다. 방구석에서 10만 개의 유튜브/톤헌트 데이터를 크롤링(Phase 2)하고, 타겟 MP3(예: 핑크플로이드 솔로곡)를 드래그&드롭 역분석하여 페달에 세팅값을 먹이는 딥러닝(RLHF) 훈련에 매진할 수 있습니다.

### 🏟️ 2-B. 무대 공연 모드 (Offline Gig Mobile App)
* **어떻게?** 내일이 당장 라이브 공연입니다! 스마트폰 커스텀 앱(React Native)을 켜고 페달과 **블루투스(BLE)** 로 페어링합니다.
* **무엇을?** 와이파이가 전혀 없는 클럽 지하실 무대라도 문제없습니다. 휴대폰 화면의 큼지막한 "Gig UI"를 탭하여 미리 훈련시켜둔 1번 프리셋(Clean), 2번 프리셋(Fuzz)을 딜레이 없이 휙휙 바꿉니다.

---

## 🩺 3. 유지보수 및 에러 방어 제어 (Maintenance)

스타트업을 차리시든, 혼자 평생 쓰시든 유지보수의 핵심은 "내가 신경 쓰지 않아도 되는 자동화"와 "문제가 터졌을 때 즉시 끄는 차단기"에 있습니다.

### 🔄 3-A. 평상시 신경 쓸 것? 🈚 (Zero Maintenance OTA)
사용자는 유지보수를 할 필요가 없습니다. GitHub에 파이썬 로직 개선 코드가 Push되면, 페달의 배 속에 있는 `Watchtower`가 **새벽 4시**마다 스스로 펌웨어(Docker Image)를 다운받고 갈아 끼웁니다. 백업 또한 도커 내부의 `PostgreSQL` 볼륨 마운팅(`pgdata`) 기능 덕에, 페달 전원 코드를 막 뽑아도 데이터는 절대 날아가지 않습니다.

### 🚨 3-B. 공연 당일 비상 차단 (The Kill-Switch)
"혹시나 모를 에러 방지"를 위한 확실한 브레이크. 공연 당일 아침, 스마트폰 앱이나 웹 대시보드를 열고 **[네트워크 및 자동 업데이트 보호 (Gig Mode)]** 스위치를 **[OFF]** 하세요. 외부 인터넷과 클라우드 허브 연결이 완전히 끊기며, 오직 로컬 C++ DSP의 신호 입출력(오프라인 연산)만 작동하게 되어 소프트웨어 업데이트로 인한 무대 위 돌발 셧다운을 100% 방지할 수 있습니다!
"""

log_title = "Final Manual: AI 인공지능 기타 페달 하드웨어 셋업, 실전 운용(Gig Mode), 유지보수 통합 매뉴얼"
korean_desc = "하드웨어를 라즈베리 파이에 이식하는 셋업 과정부터, 상황별(홈 레코딩 웹 vs 라이브 무대 모바일) 기기 체인징 운용, 그리고 무중단 도커(Docker) 업데이트 아키텍처를 통한 제로 유지보수 가이드라인을 최종 문서화했습니다."

blocks = []

blocks.append({
    "object": "block",
    "type": "callout",
    "callout": {
        "rich_text": [{"type": "text", "text": {"content": "질문하신 '설치, 운용, 유지보수' 에 대한 해답입니다. 사용자는 도커(Docker)를 통한 원클릭 설치 후, 집에서는 웹(Web) 훈련을, 공연장에서는 모바일(BLE) 조작을 통해 완전 무인(Automated) 유지보수 환경을 누리게 됩니다."}}],
        "icon": {"emoji": "📖"},
        "color": "orange_background"
    }
})

blocks.extend(create_code_block("markdown", korean_detailed_docs))
create_log_subpage(log_title, korean_desc, blocks)
