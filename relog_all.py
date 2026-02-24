from enhanced_notion_logger import create_log_subpage, create_code_block
import json

def upload_tier2_log():
    # 1. Tier 2: MFCC Extraction
    description = """[모바일/앱 단 오디오 추출 실험] 
가상의 스마트폰 앱에서 무거운 WAV 스튜디오 품질의 기타 소리를 클라우드에 통째로 올리는 것은 딜레이와 용량 부족을 야기합니다.
따라서 앱 자체적으로 '음색의 지문'인 20차원 MFCC 벡터와 스펙트럼 무게중심 값만 가볍게 스캔하여 추출하는 파이썬 프로토타입입니다.
이 과정을 통해 130KB의 오디오 파일이 600 Byte 용량의 가벼운 JSON 텍스트로 약 200배 압축되었습니다."""
    
    with open("extract_audio_features.py", "r", encoding="utf-8") as f:
        code_content = f.read()
    
    blocks = [
        {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "💻 Python 추출 코드"}}]}}
    ]
    blocks.extend(create_code_block("python", code_content))
    
    create_log_subpage("🎸 [Tier 2] 오디오 특징 추출 (MFCC) 압축 실험", description, blocks)

def upload_tier3_log():
    # 2. Tier 3: LLM Prompt Engineering Data
    description = """[클라우드 AI 자연어 해석 실험]
사용자가 모바일 앱에 '기름진 랫 소리를 원해' 라고 쳤을 때, 서버단의 Gemini 기반 LLM이 어떻게 판단하는지 
프롬프트 엔지니어링 템플릿을 만들어 시뮬레이션한 결과입니다.
결과적으로 AI는 '기름진' 이라는 형용사를 해석해 비대칭 다이오드 클리핑(FET), 높은 바이어스, 슬류 레이트 지연 등 물리적인 파라미터 값으로 완벽하게 파싱(JSON) 해 내었습니다."""
    
    with open("llm_prompt_test.py", "r", encoding="utf-8") as f:
        code_content = f.read()

    blocks = [
        {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "🧠 LLM 프롬프트 및 가상 JSON 매핑 코드"}}]}}
    ]
    blocks.extend(create_code_block("python", code_content))
    
    create_log_subpage("🧠 [Tier 3] LLM 프롬프트 및 파라미터 매핑 실험", description, blocks)

def upload_tier1_log():
    # 3. Tier 1: Hardware & C++ DSP Design
    description = """[하드웨어 DSP 엔진 및 UI 설계]
서버가 내려준 JSON을 어떻게 딜레이(Latency) 0으로 만들어 스피커로 내보낼 것인가에 대한 실제 C++ 구현 뼈대입니다.
DSP 마이크로컨트롤러(Daisy Seed)에서 JUCE 프레임워크를 기반으로, 가상의 이펙터 객체 모듈을 만들고, 런타임에 배열 구조를 동적으로 꿰맞추어 오디오를 통과시킵니다.
또한, 라이브 시 직관적으로 개입할 수 있는 물리 노브(엔드리스 엔코더와 LED)의 작동 구조를 명시했습니다."""
    
    try:
        with open("physical_interface_design.md", "r", encoding="utf-8") as f:
            md_content = f.read()
            
        with open("dsp_engine/PluginProcessor.cpp", "r", encoding="utf-8") as f:
            cpp_content = f.read()
            
        blocks = [
            {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "🎛️ 하드웨어 물리 인터페이스 문서"}}]}}
        ]
        blocks.extend(create_code_block("markdown", md_content))
        
        blocks.append({"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "⚙️ C++ JUCE Dynamic Router 엔진 (핵심 코드)"}}]}})
        blocks.extend(create_code_block("c++", cpp_content))

        create_log_subpage("🎛️ [Tier 1] 하드웨어 설계 및 C++ DSP 매트릭스", description, blocks)

    except Exception as e:
        print("Missing files for Tier 1", e)

if __name__ == "__main__":
    upload_tier2_log()
    upload_tier3_log()
    upload_tier1_log()
