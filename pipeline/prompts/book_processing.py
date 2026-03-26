"""퍼블릭 도메인 도서 가공 프롬프트 생성."""

from pipeline.prompts.base import SYSTEM_PROMPT_BOOK_PROCESSING, build_request


def build_book_processing_prompt(book_title: str, author: str,
                                 chapter_num: int,
                                 chapter_text: str) -> str:
    """도서 현대어 번역 및 요약용 사용자 프롬프트를 생성한다."""
    return f"""{author}의 《{book_title}》 {chapter_num}장을 가공해주십시오.

## 원문
{chapter_text}

## 요청 사항
다음 JSON 형식으로 응답해주십시오:
{{
  "modern_translation": "현대 한국어로 자연스럽게 풀어쓴 번역 (원문의 의미를 정확히 전달하되, 읽기 쉬운 문체로)",
  "summary": "이 장의 핵심 내용 요약 (200~300자)",
  "key_points": ["핵심 포인트 3~5개"],
  "difficult_terms": [
    {{"term": "어려운 용어", "explanation": "쉬운 설명"}}
  ],
  "reflection": "이 장을 읽고 묵상할 점 (100~200자)"
}}"""


def build_book_processing_request(book_slug: str, book_title: str,
                                  author: str, chapter_num: int,
                                  chapter_text: str) -> dict:
    """도서 가공 Batch API 요청을 생성한다."""
    custom_id = f"book-{book_slug}-ch{chapter_num:03d}"
    user_prompt = build_book_processing_prompt(
        book_title, author, chapter_num, chapter_text
    )
    return build_request(
        custom_id=custom_id,
        system_prompt=SYSTEM_PROMPT_BOOK_PROCESSING,
        user_prompt=user_prompt,

    )
