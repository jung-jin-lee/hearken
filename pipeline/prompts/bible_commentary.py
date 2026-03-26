"""성경 장별 해설 프롬프트 생성."""

from pipeline.prompts.base import SYSTEM_PROMPT_COMMENTARY, build_request


def build_commentary_prompt(book_kr: str, chapter: int, chapter_text: str) -> str:
    """장별 해설용 사용자 프롬프트를 생성한다."""
    return f"""{book_kr} {chapter}장의 해설을 작성해주십시오.

## 본문
{chapter_text}

## 요청 사항
다음 JSON 형식으로 응답해주십시오:
{{
  "commentary": "이 장의 핵심 메시지와 해설 (500~800자)",
  "key_themes": ["핵심 주제 3~5개"],
  "questions": [
    "묵상 질문 1",
    "묵상 질문 2",
    "묵상 질문 3"
  ],
  "prayer": "이 장의 내용을 바탕으로 한 기도문 (200~300자)",
  "cross_references": ["관련 성경 구절 3~5개 (예: 시편 19편 1절)"]
}}"""


def build_commentary_request(book_id: str, book_kr: str, chapter: int,
                             chapter_text: str) -> dict:
    """장별 해설 Batch API 요청을 생성한다."""
    custom_id = f"commentary-{book_id}-{chapter}"
    user_prompt = build_commentary_prompt(book_kr, chapter, chapter_text)
    return build_request(
        custom_id=custom_id,
        system_prompt=SYSTEM_PROMPT_COMMENTARY,
        user_prompt=user_prompt,

    )
