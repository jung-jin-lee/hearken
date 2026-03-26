"""배치 결과를 최종 콘텐츠 JSON 파일로 구조화한다."""

import json
from pathlib import Path

from pipeline.config import BIBLE_BOOKS, CONTENT_DIR


def save_json(data: dict, path: Path) -> None:
    """JSON 파일을 저장한다."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def structure_commentary(results: dict[str, dict]) -> int:
    """장별 해설 결과를 개별 JSON 파일로 저장한다.

    Returns:
        저장된 파일 수
    """
    book_map = {b["id"]: b for b in BIBLE_BOOKS}
    count = 0

    for custom_id, data in results.items():
        if not custom_id.startswith("commentary-") or "_error" in data:
            continue

        parts = custom_id.split("-")
        book_id = parts[1]
        chapter = int(parts[2])
        book_info = book_map.get(book_id, {})

        output = {
            "book": book_id,
            "book_kr": book_info.get("kr", ""),
            "chapter": chapter,
            **data,
        }

        path = CONTENT_DIR / "bible" / "commentary" / book_id / f"{chapter}.json"
        save_json(output, path)
        count += 1

    print(f"[구조화] 장별 해설: {count}개 파일 저장")
    return count


def structure_devotional(results: dict[str, dict]) -> int:
    """매일 묵상 결과를 개별 JSON 파일로 저장한다."""
    count = 0

    for custom_id, data in results.items():
        if not custom_id.startswith("devotional-") or "_error" in data:
            continue

        parts = custom_id.split("-")
        month = int(parts[1])
        day = int(parts[2])

        output = {"month": month, "day": day, **data}

        path = CONTENT_DIR / "devotional" / f"{month:02d}" / f"{day:02d}.json"
        save_json(output, path)
        count += 1

    print(f"[구조화] 매일 묵상: {count}개 파일 저장")
    return count


def structure_book_intros(results: dict[str, dict]) -> int:
    """66권 개론 결과를 개별 JSON 파일로 저장한다."""
    book_map = {b["id"]: b for b in BIBLE_BOOKS}
    count = 0

    for custom_id, data in results.items():
        if not custom_id.startswith("intro-") or "_error" in data:
            continue

        book_id = custom_id.replace("intro-", "")
        book_info = book_map.get(book_id, {})

        output = {
            "book": book_id,
            "book_kr": book_info.get("kr", ""),
            "chapters": book_info.get("chapters", 0),
            "testament": book_info.get("testament", ""),
            **data,
        }

        path = CONTENT_DIR / "bible" / "introductions" / f"{book_id}.json"
        save_json(output, path)
        count += 1

    print(f"[구조화] 성경 개론: {count}개 파일 저장")
    return count


def structure_characters(results: dict[str, dict]) -> int:
    """인물 해설 결과를 개별 JSON 파일로 저장한다."""
    count = 0

    for custom_id, data in results.items():
        if not custom_id.startswith("character-") or "_error" in data:
            continue

        char_slug = custom_id.replace("character-", "")
        path = CONTENT_DIR / "bible" / "characters" / f"{char_slug}.json"
        save_json(data, path)
        count += 1

    print(f"[구조화] 인물 해설: {count}개 파일 저장")
    return count


def structure_topics(results: dict[str, dict]) -> int:
    """주제별 가이드 결과를 개별 JSON 파일로 저장한다."""
    count = 0

    for custom_id, data in results.items():
        if not custom_id.startswith("topic-") or "_error" in data:
            continue

        topic_name = custom_id.replace("topic-", "")
        path = CONTENT_DIR / "bible" / "topics" / f"{topic_name}.json"
        save_json(data, path)
        count += 1

    print(f"[구조화] 주제별 가이드: {count}개 파일 저장")
    return count


def structure_key_verses(results: dict[str, dict]) -> int:
    """주요 구절 해설 결과를 단일 JSON 파일로 저장한다."""
    verses = []

    for custom_id, data in results.items():
        if not custom_id.startswith("keyverse-") or "_error" in data:
            continue
        verses.append(data)

    if verses:
        path = CONTENT_DIR / "bible" / "key-verses" / "key-verses.json"
        save_json({"verses": verses}, path)

    print(f"[구조화] 주요 구절: {len(verses)}개 저장")
    return len(verses)
