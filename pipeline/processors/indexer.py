"""콘텐츠 매니페스트(인덱스) 생성."""

import json
from pathlib import Path

from pipeline.config import BIBLE_BOOKS, CONTENT_DIR


def build_manifest() -> dict:
    """전체 콘텐츠의 매니페스트를 생성한다."""
    manifest = {
        "version": "1.0.0",
        "language": "ko",
        "bible": {
            "books": [],
            "total_commentaries": 0,
            "total_introductions": 0,
            "characters": [],
            "topics": [],
            "key_verses_count": 0,
        },
        "devotional": {
            "total_days": 0,
        },
        "books": [],
    }

    # 성경 해설 카운트
    for book in BIBLE_BOOKS:
        book_dir = CONTENT_DIR / "bible" / "commentary" / book["id"]
        chapter_files = sorted(book_dir.glob("*.json")) if book_dir.exists() else []

        book_entry = {
            "id": book["id"],
            "kr": book["kr"],
            "testament": book["testament"],
            "total_chapters": book["chapters"],
            "available_commentaries": len(chapter_files),
        }
        manifest["bible"]["books"].append(book_entry)
        manifest["bible"]["total_commentaries"] += len(chapter_files)

    # 개론 카운트
    intro_dir = CONTENT_DIR / "bible" / "introductions"
    if intro_dir.exists():
        manifest["bible"]["total_introductions"] = len(list(intro_dir.glob("*.json")))

    # 인물 목록
    char_dir = CONTENT_DIR / "bible" / "characters"
    if char_dir.exists():
        for f in sorted(char_dir.glob("*.json")):
            with open(f, encoding="utf-8") as fh:
                data = json.load(fh)
                manifest["bible"]["characters"].append({
                    "slug": f.stem,
                    "name": data.get("name", f.stem),
                })

    # 주제 목록
    topic_dir = CONTENT_DIR / "bible" / "topics"
    if topic_dir.exists():
        for f in sorted(topic_dir.glob("*.json")):
            with open(f, encoding="utf-8") as fh:
                data = json.load(fh)
                manifest["bible"]["topics"].append({
                    "slug": f.stem,
                    "name": data.get("topic", f.stem),
                })

    # 주요 구절 카운트
    kv_path = CONTENT_DIR / "bible" / "key-verses" / "key-verses.json"
    if kv_path.exists():
        with open(kv_path, encoding="utf-8") as fh:
            data = json.load(fh)
            manifest["bible"]["key_verses_count"] = len(data.get("verses", []))

    # 묵상 카운트
    devotional_dir = CONTENT_DIR / "devotional"
    if devotional_dir.exists():
        for month_dir in devotional_dir.iterdir():
            if month_dir.is_dir():
                manifest["devotional"]["total_days"] += len(
                    list(month_dir.glob("*.json"))
                )

    # 도서 목록
    books_dir = CONTENT_DIR / "books"
    if books_dir.exists():
        for book_dir in sorted(books_dir.iterdir()):
            if book_dir.is_dir():
                chapters = len(list(book_dir.glob("*.json")))
                manifest["books"].append({
                    "slug": book_dir.name,
                    "chapters": chapters,
                })

    return manifest


def save_manifest() -> Path:
    """매니페스트를 생성하고 저장한다."""
    manifest = build_manifest()
    path = CONTENT_DIR / "manifest.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # 요약 출력
    bible = manifest["bible"]
    print(f"[매니페스트] 생성 완료:")
    print(f"  성경 해설: {bible['total_commentaries']}장")
    print(f"  성경 개론: {bible['total_introductions']}권")
    print(f"  인물: {len(bible['characters'])}명")
    print(f"  주제: {len(bible['topics'])}개")
    print(f"  주요 구절: {bible['key_verses_count']}개")
    print(f"  매일 묵상: {manifest['devotional']['total_days']}일")
    print(f"  도서: {len(manifest['books'])}권")

    return path
