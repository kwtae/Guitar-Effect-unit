import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_notion_logger import create_log_subpage, create_code_block

korean_detailed_docs = """
# 📡 Phase 8: OTA (Over-The-Air) 자동 업데이트 및 네트워크 안정화 UI 구현 완료

사용자님의 훌륭한 피드백을 수용하여, 단순한 자동 업데이트를 넘어선 "기가바이트급 안정성 확보 및 사용자 제어권 부여" 기능을 성공적으로 구현했습니다.

---

## 🛠️ 1. GitHub Actions CI/CD 기반 Multi-Arch 빌드
`backend/Dockerfile`을 기반으로 코드가 업데이트될 때마다 자동으로 Docker Image를 생성하는 `.github/workflows/docker-publish.yml` 파이프라인을 구축했습니다.
* **x86 (노트북/데스크탑)** 및 **ARM64 (라즈베리 파이 엣지 기기)** 플랫폼용 이미지를 동시에 빌드하여 GitHub Registry(GHCR)에 푸시(Push)합니다.

## 🔄 2. Watchtower를 통한 백그라운드 무선 업데이트 (OTA)
라즈베리 파이에 접속할 필요 없이, `docker-compose.yml` 리스트에 `containrr/watchtower` 컨테이너를 추가했습니다.
* 매일 새벽, 클라우드 레지스트리를 찔러보고 새로운 버전의 코드가 발견되면 사용자의 개입 없이 오래된 컨테이너를 부수고 최신 버전으로 자동 재부팅시킵니다.

## 🛡️ 3. 오프라인 공연 모드 및 롤백 (Web GUI Toggles)
가장 우려하셨던 **"업데이트 도중 에러가 나서 당장 내일 있을 공연을 망치면 어떡하는가?"** 에 대한 완벽한 방어책을 Web Dashboard UI (`index.html`)에 심어두었습니다.

* **📡 오프라인 긱 모드 (Offline Gig Mode):** 
  가장 안전한 토글 버튼입니다. 이 버튼을 켜면 페달 내부의 모든 외부 인터넷 접속(클라우드 핑, Watchtower 업데이트, 통계 전송)이 블록(Block)됩니다. 오직 로컬 CPU를 이용한 파형 연산 로직만 동작하여, 무대 위에서 발생할 수 있는 1%의 네트워크 지연이나 크래시 변수를 완전히 차단합니다.
* **🔄 무선 업데이트(OTA) 개별 차단:** 
  Watchtower의 `.env` 환경 변수(WATCHTOWER_POLL_INTERVAL=0)와 연동되어 업데이트 기능만 선별적으로 끕니다.
* **↩️ 펌웨어 롤백 (Rollback):**
  도커(Docker)의 강력한 장점입니다. 새 버전에서 소리가 이상하다면, 클릭 한 번으로 과거 해시(Hash)값을 가진 안정적인 구버전 이미지로 즉시 되돌릴 수 있습니다.

이제 무대 위에서 완벽하게 통제되는 가장 스마트한 인공지능 기타 페달 생태계의 뼈대가 갖춰졌습니다!
"""

log_title = "Phase 8 Release: OTA 도커 CI/CD 무선 업데이트 파이프라인 및 무대 공연용(Gig Mode) 오프라인 롤백 방어 시스템 구축"
korean_desc = "사용자의 피드백을 반영하여 GitHub Actions를 통한 엣지 디바이스 자동 배포(Watchtower)를 구현하고, 공연 중 돌발적인 업데이트로 인한 사고를 100% 차단하기 위한 'Offline Gig Mode' 및 '퍼웨어 롤백' UI를 웹 대시보드에 탑재했습니다."

blocks = []

blocks.append({
    "object": "block",
    "type": "callout",
    "callout": {
        "rich_text": [{"type": "text", "text": {"content": "자동 업데이트의 늪(고장)에 빠지지 않도록 뮤지션에게 완벽한 네트워크 제어권(오프라인 모드, 롤백 버튼)을 돌려주는 Phase 8 인프라 구축 완료 보고서입니다."}}],
        "icon": {"emoji": "🛡️"},
        "color": "yellow_background"
    }
})

blocks.extend(create_code_block("markdown", korean_detailed_docs))
create_log_subpage(log_title, korean_desc, blocks)
