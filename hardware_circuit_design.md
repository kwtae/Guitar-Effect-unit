# AI Guitar Pedal: Hardware Circuit & Wiring Guide (시연 및 배포용 회로 설계)

이 문서는 라즈베리 파이(Raspberry Pi)를 두뇌로 사용하여 물리적인 AI 기타 이펙터 페달을 제작하기 위한 **전자 회로 설계 및 부품 결선 가이드**입니다. 무대 시연(Demo) 및 프로토타입 배포를 위해 반드시 필요한 하드웨어 세팅을 다룹니다.

---

## 1. 필요 부품 (Bill of Materials)

*   **SBC (메인 보드):** Raspberry Pi 5 (또는 Pi 4 Model B)
*   **Audio Interface:** HiFiBerry DAC+ ADC Pro (고음질 I2S 연결용) 혹은 USB 오디오 인터페이스
*   **입력 장치 (물리 노브):** 로터리 인코더 (Rotary Encoder with Push Button) x 3개 (Level, Tone, Dist 조절)
*   **스위치:** 3PDT 풋스위치 (물리적 바이패스 및 AI 제네레이트 킥 용도)
*   **표시 장치:** 5mm LED (레드/블루 듀얼 컬러 또는 개별 LED 2개) + 220옴 저항
*   **디스플레이 (선택):** 0.96인치 I2C OLED 디스플레이 (프리셋 이름 표시용)
*   **케이스:** 알루미늄 다이캐스트 인클로저 (1590BB 또는 1590XX 사이즈 권장)

---

## 2. GPIO 핀 배열 및 회로 결선 (Raspberry Pi 기반)

라즈베리 파이의 40핀 GPIO 헤더를 기준으로 부품들을 연결합니다. (참고: Audio HAT 장착 시 충돌하지 않는 남는 GPIO 핀을 사용해야 합니다.)

### A. 로터리 인코더 (Rotary Encoders) 3개 배선
로터리 인코더는 3개의 핀(A, B, GND)을 가집니다. 회전에 인터럽트를 걸어 Python 데몬이 감지합니다.
*   **Encoder 1 (Level):**
    *   Pin A → GPIO 17
    *   Pin B → GPIO 27
    *   GND → 공통 GND
*   **Encoder 2 (Tone):**
    *   Pin A → GPIO 22
    *   Pin B → GPIO 23
    *   GND → 공통 GND
*   **Encoder 3 (Dist/Gain):**
    *   Pin A → GPIO 24
    *   Pin B → GPIO 25
    *   GND → 공통 GND
> *소프트웨어 처리:* `pigpio` 라이브러리를 사용하여 디바운싱(Debouncing) 처리를 해야 노브가 튀지 않습니다.

### B. 풋스위치 (Stomp Switch) 
페달을 밟아 톤 생성을 발동시키거나 활성화하는 스위치입니다.
*   **스위치 핀 1:** GPIO 5 (내부 Pull-up 저항 설정 필요)
*   **스위치 핀 2:** 공통 GND
> *소프트웨어 처리:* Falling Edge 감지로 스위치가 눌렸을 때 FastAPI(백엔드)로 트리거 신호(`/generate`)를 전송합니다.

### C. 상태 표시 LED (리액션)
AI가 분석 중일 때 파란색 점멸, 켜져 있을 때 빨간색 점등.
*   **Red LED (Active):** GPIO 6 → 220Ω 저항 → LED (+)극 / GND → LED (-)극
*   **Blue LED (Thinking):** GPIO 13 → 220Ω 저항 → LED (+)극 / GND → LED (-)극

### D. I2C OLED 디스플레이 (기기 상태창)
*   **VCC:** 라즈베리 파이 3.3V 핀
*   **GND:** 공통 GND
*   **SDA (Data):** GPIO 2 (I2C1 SDA)
*   **SCL (Clock):** GPIO 3 (I2C1 SCL)

---

## 3. 내부 연결 라우팅 블록 다이어그램

```text
[ 물리적 조작부 ]               [ 두뇌부 (Raspberry Pi + HAT) ]              [ 오디오/네트워크 입출력 ]
                                ________________________________
 1. 로터리 인코더 ──(GPIO)──▶  | Hardware Daemon (Python)      |
 2. 풋스위치      ──(GPIO)──▶  |  - I/O Polling & Event Emitter|
 3. I2C OLED      ◀──(I2C)──   |_______________________________|             [ 무선 통신망 ]
 4. 상태 LED      ◀──(GPIO)──           | (웹 소켓 / REST API)        ========▶ Wi-Fi (Gemini API 통신 / RLHF 전송)
                                 _______▼_______________________
                                | Local FastAPI Server          |
                                |  - DB 읽기/쓰기 (SQLite)      |
                                |  - AI 프롬프트 분석 & 라우팅  |
                                |_______________________________|
                                        | (OSC/MIDI 로컬 제어 신호)
                                 _______▼_______________________         [ 아날로그 오디오 연결 ]
                                | JUCE C++ DSP Engine           |       ┌──▶ [ 1/4" 모노 잭 (Out) ] ──▶ 기타 앰프
                                |  (Fast Audio Processing)      |───────┤ (Audio HAT I2S)
         일렉트릭 기타 ──▶ [ 1/4" 모노 잭 (In) ] ───────────────────────▶ (Audio HAT I2S)
                                |_______________________________|
```

---

## 4. 소프트웨어 실행 순서 (Systemd 서비스 구동)
이펙터의 전원(9V 또는 5V 3A)이 켜지면 OS 부팅 후 자동으로 다음 과정이 백그라운드에서 실행되어야 합니다.

1.  `jackd` (또는 ALSA) 오디오 드라이버 실행 (지연 시간 5ms 이하 타겟).
2.  `juce-pedal-dsp` (C++ 오디오 처리 엔진) 스탠드얼론 모드 실행.
3.  `uvicorn backend.main:app` (AI 두뇌 FastAPI 서버) 실행.
4.  `hardware_daemon.py` (GPIO 감지 및 LED, 디스플레이 제어 스크립트) 실행.

위 4가지 컴포넌트가 모두 로드되면 비로소 LED가 빛나며 시연(Demo)이 가능한 상태가 됩니다!
