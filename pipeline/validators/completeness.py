"""콘텐츠 완전성 체크 — 누락된 항목을 탐지한다."""

from pipeline.config import (
    BIBLE_BOOKS,
    BIBLE_CHARACTERS,
    BIBLE_TOPICS,
    TOTAL_CHAPTERS,
)


def check_commentary_completeness(results: dict[str, dict]) -> dict:
    """성경 해설의 완전성을 체크한다."""
    expected = set()
    for book in BIBLE_BOOKS:
        for ch in range(1, book["chapters"] + 1):
            expected.add(f"commentary-{book['id']}-{ch}")

    found = {k for k in results if k.startswith("commentary-") and "_error" not in results[k]}
    missing = expected - found

    return {
        "expected": len(expected),
        "found": len(found),
        "missing": sorted(missing),
        "complete": len(missing) == 0,
    }


def check_devotional_completeness(results: dict[str, dict]) -> dict:
    """365일 묵상의 완전성을 체크한다."""
    days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    expected = set()
    for m, days in enumerate(days_in_month, 1):
        for d in range(1, days + 1):
            expected.add(f"devotional-{m:02d}-{d:02d}")

    found = {k for k in results if k.startswith("devotional-") and "_error" not in results[k]}
    missing = expected - found

    return {
        "expected": len(expected),
        "found": len(found),
        "missing": sorted(missing),
        "complete": len(missing) == 0,
    }


def check_intro_completeness(results: dict[str, dict]) -> dict:
    """66권 개론의 완전성을 체크한다."""
    expected = {f"intro-{book['id']}" for book in BIBLE_BOOKS}
    found = {k for k in results if k.startswith("intro-") and "_error" not in results[k]}
    missing = expected - found

    return {
        "expected": len(expected),
        "found": len(found),
        "missing": sorted(missing),
        "complete": len(missing) == 0,
    }


def check_character_completeness(results: dict[str, dict]) -> dict:
    """인물 해설의 완전성을 체크한다."""
    found = {k for k in results if k.startswith("character-") and "_error" not in results[k]}
    return {
        "expected": len(BIBLE_CHARACTERS),
        "found": len(found),
        "complete": len(found) >= len(BIBLE_CHARACTERS),
    }


def check_topic_completeness(results: dict[str, dict]) -> dict:
    """주제별 가이드의 완전성을 체크한다."""
    expected = {f"topic-{t}" for t in BIBLE_TOPICS}
    found = {k for k in results if k.startswith("topic-") and "_error" not in results[k]}
    missing = expected - found

    return {
        "expected": len(expected),
        "found": len(found),
        "missing": sorted(missing),
        "complete": len(missing) == 0,
    }
