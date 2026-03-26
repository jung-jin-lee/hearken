#!/usr/bin/env python3
"""원본 성경 텍스트를 수집한다.

사용법:
  python -m pipeline.scripts.01_fetch_sources
  python -m pipeline.scripts.01_fetch_sources --from-file /path/to/bible.txt
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.config import BIBLE_BOOKS
from pipeline.sources.bible_kr import (
    fetch_chapter_text,
    get_all_chapters,
    load_bible_from_single_file,
    load_chapter_from_file,
)


def main():
    parser = argparse.ArgumentParser(description="성경 텍스트 수집")
    parser.add_argument(
        "--from-file",
        type=str,
        help="단일 텍스트 파일에서 전체 성경을 로드 (형식: '책이름 장:절 본문')",
    )
    args = parser.parse_args()

    if args.from_file:
        print(f"[수집] 파일에서 로드: {args.from_file}")
        bible = load_bible_from_single_file(Path(args.from_file))
        total_chapters = sum(len(chs) for chs in bible.values())
        print(f"[수집] {len(bible)}권, {total_chapters}장 로드 완료")
        return

    # API에서 수집
    chapters = get_all_chapters()
    print(f"[수집] 총 {len(chapters)}장 수집 시작...")

    cached = 0
    fetched = 0
    errors = 0

    for info in chapters:
        existing = load_chapter_from_file(info["book_id"], info["chapter"])
        if existing:
            cached += 1
            continue

        try:
            fetch_chapter_text(
                info["book_id"], info["book_kr"], info["chapter"]
            )
            fetched += 1
        except Exception as e:
            print(f"  [오류] {info['book_kr']} {info['chapter']}장: {e}")
            errors += 1

    print(f"[수집] 완료: 캐시 {cached}, 신규 {fetched}, 오류 {errors}")


if __name__ == "__main__":
    main()
