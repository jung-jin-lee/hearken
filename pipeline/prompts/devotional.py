"""365일 매일 묵상 프롬프트 생성."""

from pipeline.prompts.base import SYSTEM_PROMPT_DEVOTIONAL, build_request


def build_devotional_prompt(month: int, day: int, reference: str,
                            verse_text: str) -> str:
    """매일 묵상용 사용자 프롬프트를 생성한다."""
    return f"""{month}월 {day}일 매일 묵상을 작성해주십시오.

## 오늘의 본문
{reference}
"{verse_text}"

## 요청 사항
다음 JSON 형식으로 응답해주십시오:
{{
  "title": "오늘의 묵상 제목 (10~20자)",
  "reading": "본문 해설과 묵상 (300~500자). 오늘 하루를 시작하며 이 말씀이 주는 의미를 나누어 주십시오.",
  "question": "자기 성찰을 위한 묵상 질문 1개",
  "prayer": "오늘의 기도문 (150~250자)"
}}"""


def build_devotional_request(month: int, day: int, reference: str,
                             verse_text: str) -> dict:
    """매일 묵상 Batch API 요청을 생성한다."""
    custom_id = f"devotional-{month:02d}-{day:02d}"
    user_prompt = build_devotional_prompt(month, day, reference, verse_text)
    return build_request(
        custom_id=custom_id,
        system_prompt=SYSTEM_PROMPT_DEVOTIONAL,
        user_prompt=user_prompt,

    )
