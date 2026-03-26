"""생성된 콘텐츠의 JSON 스키마 검증."""

from pydantic import BaseModel, field_validator


class CommentarySchema(BaseModel):
    """장별 해설 스키마."""
    commentary: str
    key_themes: list[str]
    questions: list[str]
    prayer: str
    cross_references: list[str]

    @field_validator("commentary")
    @classmethod
    def commentary_not_empty(cls, v: str) -> str:
        if len(v.strip()) < 100:
            raise ValueError("해설이 100자 미만입니다")
        return v

    @field_validator("questions")
    @classmethod
    def three_questions(cls, v: list[str]) -> list[str]:
        if len(v) < 3:
            raise ValueError("묵상 질문이 3개 미만입니다")
        return v


class DevotionalSchema(BaseModel):
    """매일 묵상 스키마."""
    title: str
    reading: str
    question: str
    prayer: str

    @field_validator("reading")
    @classmethod
    def reading_not_empty(cls, v: str) -> str:
        if len(v.strip()) < 50:
            raise ValueError("묵상 글이 50자 미만입니다")
        return v


class BookIntroSchema(BaseModel):
    """성경 각 권 개론 스키마."""
    author: str
    date: str
    purpose: str
    summary: str
    key_themes: list[str]
    outline: list[dict]
    key_verses: list[str]
    message_for_today: str


class CharacterSchema(BaseModel):
    """성경 인물 해설 스키마."""
    name: str
    biography: str
    key_events: list[dict]
    character_traits: list[str]
    lessons: str
    key_references: list[str]
    prayer: str


class TopicSchema(BaseModel):
    """주제별 가이드 스키마."""
    topic: str
    introduction: str
    key_verses: list[dict]
    old_testament_perspective: str
    new_testament_perspective: str
    practical_application: str
    prayer: str


class KeyVerseSchema(BaseModel):
    """주요 구절 해설 스키마."""
    reference: str
    text: str
    context: str
    meaning: str
    application: str
    cross_references: list[str]
    prayer: str


class BookProcessingSchema(BaseModel):
    """도서 가공 스키마."""
    modern_translation: str
    summary: str
    key_points: list[str]
    difficult_terms: list[dict]
    reflection: str


# 스키마 매핑
SCHEMA_MAP = {
    "commentary": CommentarySchema,
    "devotional": DevotionalSchema,
    "intro": BookIntroSchema,
    "character": CharacterSchema,
    "topic": TopicSchema,
    "keyverse": KeyVerseSchema,
    "book": BookProcessingSchema,
}


def validate_item(custom_id: str, data: dict) -> tuple[bool, str]:
    """단일 항목을 스키마에 맞게 검증한다.

    Returns:
        (valid: bool, error_message: str)
    """
    if "_error" in data:
        return False, f"API 오류: {data['_error']}"

    # custom_id에서 콘텐츠 유형 추출
    content_type = custom_id.split("-")[0]
    schema_class = SCHEMA_MAP.get(content_type)

    if not schema_class:
        return False, f"알 수 없는 콘텐츠 유형: {content_type}"

    try:
        schema_class.model_validate(data)
        return True, ""
    except Exception as e:
        return False, str(e)


def validate_batch_results(results: dict[str, dict]) -> dict:
    """배치 결과 전체를 검증한다.

    Returns:
        {"total": int, "valid": int, "invalid": int,
         "errors": [{custom_id, error}]}
    """
    errors = []
    valid_count = 0

    for custom_id, data in results.items():
        is_valid, error = validate_item(custom_id, data)
        if is_valid:
            valid_count += 1
        else:
            errors.append({"custom_id": custom_id, "error": error})

    total = len(results)
    return {
        "total": total,
        "valid": valid_count,
        "invalid": total - valid_count,
        "errors": errors,
    }
