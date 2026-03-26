"""성경 66권 개론 프롬프트 생성."""

from pipeline.prompts.base import SYSTEM_PROMPT_BOOK_INTRO, build_request


def build_book_intro_prompt(book_kr: str, chapters: int,
                            testament: str) -> str:
    """성경 각 권 개론용 사용자 프롬프트를 생성한다."""
    testament_kr = "구약" if testament == "old" else "신약"
    return f"""{testament_kr}성경 {book_kr} (총 {chapters}장)의 개론을 작성해주십시오.

## 요청 사항
다음 JSON 형식으로 응답해주십시오:
{{
  "author": "저자 또는 전통적으로 알려진 기록자",
  "date": "기록 추정 시기",
  "purpose": "기록 목적 (100~200자)",
  "summary": "전체 내용 요약 (300~500자)",
  "key_themes": ["핵심 주제 3~5개"],
  "outline": [
    {{"section": "1~10장", "title": "구간 제목", "description": "구간 설명 (50~100자)"}}
  ],
  "key_verses": ["이 책에서 가장 중요한 구절 3~5개"],
  "message_for_today": "오늘날 우리에게 주는 메시지 (200~300자)"
}}"""


def build_book_intro_request(book_id: str, book_kr: str, chapters: int,
                             testament: str) -> dict:
    """성경 각 권 개론 Batch API 요청을 생성한다."""
    custom_id = f"intro-{book_id}"
    user_prompt = build_book_intro_prompt(book_kr, chapters, testament)
    return build_request(
        custom_id=custom_id,
        system_prompt=SYSTEM_PROMPT_BOOK_INTRO,
        user_prompt=user_prompt,

    )
