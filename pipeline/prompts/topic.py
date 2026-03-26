"""주제별 성경 가이드 프롬프트 생성."""

from pipeline.prompts.base import SYSTEM_PROMPT_TOPIC, build_request


def build_topic_prompt(topic: str) -> str:
    """주제별 가이드용 사용자 프롬프트를 생성한다."""
    return f"""성경의 "{topic}"에 대한 주제별 가이드를 작성해주십시오.

## 요청 사항
다음 JSON 형식으로 응답해주십시오:
{{
  "topic": "{topic}",
  "introduction": "{topic}에 대한 성경의 가르침 개요 (200~300자)",
  "key_verses": [
    {{"reference": "성경 구절", "text": "구절 본문", "explanation": "해설 (100~150자)"}}
  ],
  "old_testament_perspective": "구약에서의 {topic} (150~200자)",
  "new_testament_perspective": "신약에서의 {topic} (150~200자)",
  "practical_application": "{topic}을 일상에서 실천하는 방법 (200~300자)",
  "prayer": "{topic}에 대해 묵상하며 드리는 기도 (150~200자)"
}}

key_verses는 가장 중요한 구절 10~15개를 선별해주십시오."""


def build_topic_request(topic: str) -> dict:
    """주제별 가이드 Batch API 요청을 생성한다."""
    custom_id = f"topic-{topic}"
    user_prompt = build_topic_prompt(topic)
    return build_request(
        custom_id=custom_id,
        system_prompt=SYSTEM_PROMPT_TOPIC,
        user_prompt=user_prompt,

    )
