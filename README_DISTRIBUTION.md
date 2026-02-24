# 🎸 AI Guitar Pedal System - 배포 완결본 (Distribution)

본 프로젝트는 하드웨어(C++ DSP), 모바일 앱(React Native / Vite 뷰어), 클라우드 AI 서버(FastAPI + Python ML)를 혼합한 "자연어 기반 AI 멀티 이펙터"의 핵심 마스터 아키텍처 및 프로토타입 구현체를 담고 있습니다.

## 📦 파일 구조 개요

- **`backend/`**: 클라우드 API 및 AI 시스템 (FastAPI, SQLAlchemy DB ORM, Gemini API 연동 모듈)
- **`frontend/`**: 현장 라이브용 스마트폰 컨트롤 센터 앱 프로토타입 (React, Vite)
- **`dsp_engine/`**: 무지연 오디오를 출력할 하드웨어 마더보드(Daisy Seed 등)용 C++ / JUCE 기반 Routing Matrix 코어 클래스 프로토타입
- **`*.py` 루트 파일들**: 머신러닝 오디오 압축 로직, 테스트 스크립트, 노션 데이터 로깅 스크립트들.
- **`physical_interface_design.md`**: 터치스크린 없이 노브 3개만으로 AI 파라미터를 완전 제어하는 하드웨어 UI 기획 및 레이아웃 문서.

---

## 🚀 다른 컴퓨터에서 프로젝트 실행하는 방법

### 1단계: 백엔드 서버 구동 (Python 환경)
1. 시스템에 Python 3.10 이상이 설치되어 있어야 합니다.
2. 터미널을 열고 프로젝트 루트 경로에서 라이브러리를 설치합니다.
   ```bash
   pip install -r backend/requirements.txt
   ```
3. (선택: 오디오 스크립트 용 추가 라이브러리 설치)
   ```bash
   pip install librosa numpy soundfile
   ```
4. 서버를 실행합니다!
   ```bash
   uvicorn backend.main:app --host 127.0.0.1 --port 8000
   ```

### 2단계: 모바일 앱 구동 (Node.js 환경)
1. 시스템에 Node.js 가 설치되어 있어야 합니다.
2. 새로운 터미널 창을 열고 `frontend/` 폴더로 이동합니다.
   ```bash
   cd frontend
   npm install
   ```
3. 프론트엔드 모바일 뷰어(React UI)를 실행합니다.
   ```bash
   npm run dev
   ```
4. 브라우저에서 표시되는 주소(예: `http://localhost:5173`)로 접속하면 프리미엄 Glassmorphism UI 기반 AI 컨트롤 센터를 사용할 수 있습니다.

### 🧠 (선택) 3단계: Gemini AI 통신 및 RLHF 알고리즘 구동
실제 사용자가 무대에서 물리 노브를 꺾은 수치를 분석해 오차율(Error Delta)을 파악하고, Gemini API에게 이 오차를 상쇄시킬 새로운 "Prompt/가중치 세팅 값"을 짜오라고 명령하는 코어 스크립트입니다.

1. Gemini API 키를 터미널 환경 변수에 세팅합니다.
   ```powershell
   # Windows PowerShell
   $env:GEMINI_API_KEY="본인의_실제_API_키"
   ```
2. RLHF 학습 봇 스크립트를 실행합니다. (데이터베이스 내부에 생성된 오차를 자동으로 비교분석합니다.)
   ```bash
   # 프로젝트 루트 경로에서 실행
   python backend/rlhf_gemini_integration.py
   ```
3. 터미널의 출력 결과물 중앙에 `✨ --- GEMINI'S SELF-CORRECTED LOGIC ---` 란을 통해 AI가 스스로 "어떻게 게인 값을 수정할지"를 판단하는 결과를 감상합니다.
