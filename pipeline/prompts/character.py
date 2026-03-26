"""성경 인물 해설 프롬프트 생성."""

from pipeline.prompts.base import SYSTEM_PROMPT_CHARACTER, build_request


def build_character_prompt(name: str) -> str:
    """성경 인물 해설용 사용자 프롬프트를 생성한다."""
    return f"""성경 인물 "{name}"에 대한 해설을 작성해주십시오.

## 요청 사항
다음 JSON 형식으로 응답해주십시오:
{{
  "name": "{name}",
  "biography": "인물의 생애 요약 (300~500자)",
  "key_events": [
    {{"event": "주요 사건 제목", "description": "사건 설명 (100~150자)", "reference": "관련 성경 구절"}}
  ],
  "character_traits": ["인물의 성품/특징 3~5개"],
  "lessons": "이 인물에게서 배울 수 있는 신앙적 교훈 (200~300자)",
  "key_references": ["관련 핵심 성경 구절 3~5개"],
  "prayer": "이 인물의 삶을 묵상하며 드리는 기도 (150~200자)"
}}"""


def build_character_request(name: str) -> dict:
    """성경 인물 해설 Batch API 요청을 생성한다."""
    safe_id = name.replace(" ", "-").replace("(", "").replace(")", "")
    custom_id = f"character-{safe_id}"
    user_prompt = build_character_prompt(name)
    return build_request(
        custom_id=custom_id,
        system_prompt=SYSTEM_PROMPT_CHARACTER,
        user_prompt=user_prompt,

    )
