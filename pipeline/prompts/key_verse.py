"""주요 구절 심층 해설 프롬프트 생성."""

from pipeline.prompts.base import SYSTEM_PROMPT_KEY_VERSE, build_request


def build_key_verse_prompt(reference: str, verse_text: str = "") -> str:
    """주요 구절 해설용 사용자 프롬프트를 생성한다."""
    text_section = f'\n## 본문\n"{verse_text}"\n' if verse_text else ""
    return f"""{reference}의 심층 해설을 작성해주십시오.
{text_section}
## 요청 사항
다음 JSON 형식으로 응답해주십시오:
{{
  "reference": "{reference}",
  "text": "구절 본문 (개역한글)",
  "context": "이 구절의 앞뒤 문맥과 배경 설명 (150~200자)",
  "meaning": "이 구절의 핵심 의미와 신학적 해설 (300~500자)",
  "application": "오늘날 우리 삶에 적용할 수 있는 점 (150~200자)",
  "cross_references": ["관련 성경 구절 3~5개"],
  "prayer": "이 구절을 묵상하며 드리는 기도 (100~150자)"
}}"""


def build_key_verse_request(reference: str, verse_text: str = "") -> dict:
    """주요 구절 해설 Batch API 요청을 생성한다."""
    safe_ref = reference.replace(" ", "-").replace(":", "-")
    custom_id = f"keyverse-{safe_ref}"
    user_prompt = build_key_verse_prompt(reference, verse_text)
    return build_request(
        custom_id=custom_id,
        system_prompt=SYSTEM_PROMPT_KEY_VERSE,
        user_prompt=user_prompt,

    )
