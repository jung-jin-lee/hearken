"""개역한글 성경 텍스트 로더.

퍼블릭 도메인인 개역한글판 성경 텍스트를 웹에서 가져오거나
로컬 파일에서 로드한다.
"""

import json
import re
from pathlib import Path

import httpx

from pipeline.config import BIBLE_BOOKS, SOURCES_DATA_DIR

BIBLE_DATA_DIR = SOURCES_DATA_DIR / "bible_kr"
BIBLE_DATA_DIR.mkdir(parents=True, exist_ok=True)

# 공개 성경 API 엔드포인트 (개역한글)
# 실제 사용 시 적절한 API로 교체 필요
BIBLE_API_BASE = "https://bible-api.deno.dev/api"


def fetch_chapter_text(book_id: str, book_kr: str, chapter: int) -> str:
    """API에서 성경 한 장의 텍스트를 가져온다.

    캐시 파일이 있으면 캐시에서 로드한다.
    """
    cache_dir = BIBLE_DATA_DIR / book_id
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"{chapter}.txt"

    if cache_path.exists():
        return cache_path.read_text(encoding="utf-8")

    # API 호출 (실제 구현 시 API에 맞게 조정)
    try:
        url = f"{BIBLE_API_BASE}/read/개역한글/{book_kr}/{chapter}"
        resp = httpx.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        # API 응답에서 절 텍스트 추출 (API 구조에 따라 조정 필요)
        verses = data.get("verses", [])
        lines = []
        for v in verses:
            verse_num = v.get("verse", "")
            text = v.get("text", "")
            lines.append(f"{verse_num} {text}")

        chapter_text = "\n".join(lines)
    except Exception as e:
        print(f"[경고] API 호출 실패 ({book_kr} {chapter}장): {e}")
        chapter_text = f"[{book_kr} {chapter}장 텍스트를 가져올 수 없습니다]"

    cache_path.write_text(chapter_text, encoding="utf-8")
    return chapter_text


def load_chapter_from_file(book_id: str, chapter: int) -> str | None:
    """로컬 캐시에서 성경 한 장의 텍스트를 로드한다."""
    cache_path = BIBLE_DATA_DIR / book_id / f"{chapter}.txt"
    if cache_path.exists():
        return cache_path.read_text(encoding="utf-8")
    return None


def save_chapter_text(book_id: str, chapter: int, text: str) -> None:
    """성경 한 장의 텍스트를 로컬에 저장한다."""
    cache_dir = BIBLE_DATA_DIR / book_id
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"{chapter}.txt"
    cache_path.write_text(text, encoding="utf-8")


def load_bible_from_single_file(file_path: Path) -> dict[str, dict[int, str]]:
    """단일 텍스트 파일에서 전체 성경을 로드한다.

    파일 형식: "책이름 장:절 본문" (한 줄에 한 절)

    Returns:
        {book_id: {chapter: chapter_text}} 형태의 딕셔너리
    """
    book_kr_to_id = {b["kr"]: b["id"] for b in BIBLE_BOOKS}
    bible = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # "창세기 1:1 태초에 하나님이..." 형태 파싱
            match = re.match(r"^(\S+)\s+(\d+):(\d+)\s+(.+)$", line)
            if not match:
                continue

            book_kr, ch_str, verse_str, text = match.groups()
            chapter = int(ch_str)
            verse = int(verse_str)

            book_id = book_kr_to_id.get(book_kr)
            if not book_id:
                continue

            if book_id not in bible:
                bible[book_id] = {}
            if chapter not in bible[book_id]:
                bible[book_id][chapter] = []

            bible[book_id][chapter].append(f"{verse} {text}")

    # 리스트를 텍스트로 합치고 캐시에 저장
    result = {}
    for book_id, chapters in bible.items():
        result[book_id] = {}
        for ch, verses in chapters.items():
            chapter_text = "\n".join(verses)
            result[book_id][ch] = chapter_text
            save_chapter_text(book_id, ch, chapter_text)

    return result


def get_all_chapters() -> list[dict]:
    """모든 성경 장의 메타데이터 리스트를 반환한다.

    Returns:
        [{"book_id": str, "book_kr": str, "chapter": int, "testament": str}, ...]
    """
    chapters = []
    for book in BIBLE_BOOKS:
        for ch in range(1, book["chapters"] + 1):
            chapters.append({
                "book_id": book["id"],
                "book_kr": book["kr"],
                "chapter": ch,
                "testament": book["testament"],
            })
    return chapters
