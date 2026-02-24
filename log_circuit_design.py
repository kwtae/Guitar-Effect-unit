import sys
import os

# Ensure the backend is in path if necessary
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_notion_logger import create_log_subpage, create_code_block

# Read the generated markdown layout file
with open("C:/Users/wontae/.gemini/antigravity/scratch/ai_guitar_pedal/hardware_circuit_design.md", "r", encoding="utf-8") as f:
    circuit_docs = f.read()

log_title = "Update: Hardware Circuit & Wiring Guide (Physical Demo Prep)"
korean_desc = "실제 무대 시연(Demo) 및 배포를 위해, 라즈베리 파이(Raspberry Pi) 기반의 기타 이펙터 페달을 제작하기 위한 전자 회로 설계 및 부품(GPIO) 결선(Wiring) 가이드 문서입니다."

blocks = []

blocks.append({
    "object": "block",
    "type": "heading_2",
    "heading_2": {
        "rich_text": [{"type": "text", "text": {"content": "1. 회로 설계 및 부품 구성 기획안"}}]
    }
})

blocks.append({
    "object": "block",
    "type": "paragraph",
    "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "- 물리적인 AI 페달 프로토타입 시연을 위한 구체적인 H/W 컴포넌트(SBC, I2S DAC, 스위치, 로터리 인코더 등) 리스트업 및 포트 매핑을 확정했습니다.\n- 특히, 딜레이를 최소화해야 하는 악기인 기타 특성상, 파이프라인에서 ADC와 C++ DSP 간의 통신 병목을 줄이는 설계에 초점을 맞췄습니다."}}]
    }
})

blocks.append({
    "object": "block",
    "type": "heading_2",
    "heading_2": {
        "rich_text": [{"type": "text", "text": {"content": "2. 하드웨어 블록 다이어그램 & GPIO 결선표"}}]
    }
})

# Add the hardware documentation as code block for formatting safety in Notion
blocks.extend(create_code_block("markdown", circuit_docs))

# Add a closing
blocks.append({
    "object": "block",
    "type": "callout",
    "callout": {
        "rich_text": [{"type": "text", "text": {"content": "이 결선도(Wiring Diagram)를 바탕으로 만능 기판(Perfboard) 또는 PCB 주문을 통해 시연용 프로토타입 조립을 시작할 수 있습니다."}}],
        "icon": {"emoji": "🔌"},
        "color": "blue_background"
    }
})

create_log_subpage(log_title, korean_desc, blocks)
