#!/usr/bin/env python3
"""일일 묵상집(My Utmost, Streams in the Desert)을 주 단위로 분할한다.

사용법:
  python -m pipeline.scripts.split_daily_devotional my-utmost /tmp/my-utmost-raw.txt
  python -m pipeline.scripts.split_daily_devotional streams-in-desert /tmp/streams-in-desert-raw.txt
"""

import json
import re
import sys
from pathlib import Path

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
MONTHS_KR = [
    "1월", "2월", "3월", "4월", "5월", "6월",
    "7월", "8월", "9월", "10월", "11월", "12월",
]
DAYS_IN_MONTH = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

BOOK_META = {
    "my-utmost": {
        "title": "지극히 높으신 분을 위한 나의 최선",
        "title_original": "My Utmost for His Highest",
        "author": "오스왈드 챔버스 (Oswald Chambers)",
        "author_original": "Oswald Chambers",
        "year": "1927",
        "source": "https://archive.org/details/my-utmost-for-his-highest-chambers",
        "license": "public_domain",
        "note": "챔버스의 대표적 일일 묵상집. 아내 비디가 그의 강의를 속기로 기록하여 사후 편집 출간. 365일 묵상을 주 단위로 분할.",
    },
    "streams-in-desert": {
        "title": "사막의 샘물",
        "title_original": "Streams in the Desert",
        "author": "카우만 부인 (Mrs. Charles E. Cowman)",
        "author_original": "L.B. Cowman",
        "year": "1925",
        "source": "https://archive.org/details/streamsindesert10000lett",
        "license": "public_domain",
        "note": "카우만 부인의 대표적 일일 묵상집. 남편의 투병과 선교 경험에서 우러난 366일 묵상을 주 단위로 분할.",
    },
}


def parse_daily_entries(text: str) -> dict[tuple[int, int], str]:
    """텍스트에서 일별 묵상을 추출한다.

    Returns:
        {(month_idx, day): entry_text} — month_idx는 0-based
    """
    entries = {}
    # 패턴: "January 1" 또는 "January 1\n" (줄의 시작)
    pattern = re.compile(
        r"^(" + "|".join(MONTHS) + r")\s+(\d{1,2})\s*$",
        re.MULTILINE,
    )

    matches = list(pattern.finditer(text))

    for i, match in enumerate(matches):
        month_name = match.group(1)
        day = int(match.group(2))
        month_idx = MONTHS.index(month_name)

        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        entry_text = text[start:end].strip()

        entries[(month_idx, day)] = entry_text

    return entries


def group_into_weeks(entries: dict[tuple[int, int], str]) -> list[dict]:
    """일별 묵상을 주 단위로 묶는다.

    Returns:
        [{"num": 1, "title": "1월 1-7일", "days": [(month, day, text), ...]}]
    """
    # 모든 날짜를 순서대로 정렬
    all_days = []
    for month_idx in range(12):
        max_day = DAYS_IN_MONTH[month_idx]
        for day in range(1, max_day + 1):
            if (month_idx, day) in entries:
                all_days.append((month_idx, day, entries[(month_idx, day)]))

    # 7일 단위로 묶기
    weeks = []
    for i in range(0, len(all_days), 7):
        chunk = all_days[i : i + 7]
        if not chunk:
            continue

        first_m, first_d, _ = chunk[0]
        last_m, last_d, _ = chunk[-1]

        if first_m == last_m:
            title = f"{MONTHS_KR[first_m]} {first_d}-{last_d}일"
        else:
            title = f"{MONTHS_KR[first_m]} {first_d}일 - {MONTHS_KR[last_m]} {last_d}일"

        weeks.append({
            "num": len(weeks) + 1,
            "title": title,
            "days": chunk,
        })

    return weeks


def save_book(slug: str, weeks: list[dict]) -> None:
    """분할된 도서를 파이프라인 형식으로 저장한다."""
    book_dir = Path(f"pipeline/sources/data/books/{slug}")
    book_dir.mkdir(parents=True, exist_ok=True)

    meta = BOOK_META[slug].copy()
    meta["slug"] = slug
    meta["chapters"] = []

    for week in weeks:
        filename = f"ch{week['num']:02d}.txt"
        meta["chapters"].append({
            "num": week["num"],
            "title": week["title"],
            "file": filename,
        })

        # 챕터 파일 생성
        lines = []
        for month_idx, day, text in week["days"]:
            lines.append(f"--- {MONTHS_KR[month_idx]} {day}일 ---\n")
            lines.append(text)
            lines.append("")

        (book_dir / filename).write_text("\n".join(lines), encoding="utf-8")

    # metadata.json 저장
    with open(book_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"[완료] {slug}: {len(weeks)}장, {sum(len(w['days']) for w in weeks)}일 저장")


def main():
    if len(sys.argv) < 3:
        print("사용법: python -m pipeline.scripts.split_daily_devotional <slug> <raw.txt>")
        sys.exit(1)

    slug = sys.argv[1]
    input_path = Path(sys.argv[2])

    if slug not in BOOK_META:
        print(f"[오류] 지원하지 않는 도서: {slug}")
        sys.exit(1)

    if not input_path.exists():
        print(f"[오류] 파일 없음: {input_path}")
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8")
    print(f"[파싱] {input_path.name} ({len(text):,}자)")

    entries = parse_daily_entries(text)
    print(f"[파싱] {len(entries)}개 일별 묵상 추출")

    weeks = group_into_weeks(entries)
    save_book(slug, weeks)


if __name__ == "__main__":
    main()
