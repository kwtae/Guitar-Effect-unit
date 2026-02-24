from enhanced_notion_logger import create_log_subpage, create_code_block
import json

def upload_rlhf_algorithm_log():
    description = """[핵심 알고리즘] 사용자 피드백 기반 AI 자가 학습 보정 (RLHF)
무대 위 라이브 상황에서 AI가 세팅한 값이 마음에 들지 않아, 연주자가 하드웨어 물리 노브(예: Gain)를 돌려 파라미터를 강제 수정(Override)하면 발생하는 프로세스입니다.
수정값(Delta)이 스마트폰 앱을 거쳐 클라우드의 PostgreSQL 'RLHFFeedback' 테이블에 저장됩니다.
이후 크론잡이나 머신러닝 파이프라인이 이 오차값(Error Rate)의 평균을 계산하여, "AI가 '기름진 랫'을 만들 때 게인을 너무 낮게 잡는 경향이 있다"는 것을 스스로 깨닫고, 다음 번 프롬프트 추론 시 가중치(Weight)를 보정(Fine-Tuning)하여 점점 완벽에 가까운 톤 메이커로 진화합니다."""
    
    with open("backend/rlhf_training_job.py", "r", encoding="utf-8") as f:
        code_content = f.read()

    blocks = [
        {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "📈 주기적 RLHF 오차 가중치 업데이트 알고리즘 (Python/SQLAlchemy)"}}]}}
    ]
    blocks.extend(create_code_block("python", code_content))
    
    create_log_subpage("📈 [Core Engine] RLHF 사용자 피드백 자가 학습 모델 (오차 보정)", description, blocks)

if __name__ == "__main__":
    upload_rlhf_algorithm_log()
