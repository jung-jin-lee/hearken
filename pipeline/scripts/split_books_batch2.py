#!/usr/bin/env python3
"""2차 도서 3권의 Gutenberg 원문을 챕터별로 분할하는 스크립트.

사용법:
  python3 pipeline/scripts/split_books_batch2.py
"""

import re
from pathlib import Path

RAW_DIR = Path("/tmp")
BOOKS_DIR = Path("pipeline/sources/data/books")


def split_grace_abounding():
    """번연의 은혜가 넘치다 — 350 numbered paragraphs → ~15 chapters."""
    print("\n=== 은혜가 넘치다 (Grace Abounding) ===")
    with open(RAW_DIR / "grace_abounding_raw.txt", encoding="utf-8") as f:
        text = f.read()

    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    content = text[start:end].split("\n", 1)[1]

    # Find numbered paragraphs: "1. ", "2. ", etc.
    # Split on paragraph numbers at start of line
    parts = re.split(r"\n(\d+)\.\s+", content)

    # parts[0] is preface, then alternating [num, text, num, text, ...]
    paragraphs = {}
    for i in range(1, len(parts), 2):
        num = int(parts[i])
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        paragraphs[num] = body

    max_para = max(paragraphs.keys()) if paragraphs else 0
    print(f"  Found {len(paragraphs)} numbered paragraphs (max: {max_para})")

    # Also capture preface text
    preface = parts[0].strip()
    # Remove title/header lines at top
    preface_lines = preface.split("\n")
    # Find where actual prose begins
    prose_start = 0
    for idx, line in enumerate(preface_lines):
        if "A brief Account" in line or "GRACE ABOUNDING" in line:
            prose_start = idx
            break
    preface = "\n".join(preface_lines[prose_start:]).strip()

    out_dir = BOOKS_DIR / "grace-abounding"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Chapter groupings based on narrative arc
    chapter_ranges = [
        (0, 0, "서문과 헌사"),          # preface
        (1, 10, "유년기의 죄와 두려움"),
        (11, 25, "첫 번째 각성과 결혼"),
        (26, 45, "회심의 시작"),
        (46, 70, "성경과의 만남"),
        (71, 95, "믿음과 의심 사이에서"),
        (96, 120, "유혹과 영적 전쟁"),
        (121, 150, "예수를 팔겠느냐는 유혹"),
        (151, 180, "그리스도의 의를 발견함"),
        (181, 210, "은혜의 확신"),
        (211, 240, "설교자로 부름받다"),
        (241, 270, "사역의 시작"),
        (271, 300, "투옥과 시련"),
        (301, 325, "감옥에서의 믿음"),
        (326, 339, "결론과 고백"),
    ]

    saved = 0
    for ch_num, (start_p, end_p, title) in enumerate(chapter_ranges, 1):
        if start_p == 0 and end_p == 0:
            ch_text = preface
        else:
            sections = []
            for p in range(start_p, end_p + 1):
                if p in paragraphs:
                    sections.append(f"{p}. {paragraphs[p]}")
            ch_text = "\n\n".join(sections)

        if not ch_text.strip():
            continue

        ch_text = re.sub(r"\n{3,}", "\n\n", ch_text)
        outpath = out_dir / f"ch{ch_num:02d}.txt"
        outpath.write_text(ch_text + "\n", encoding="utf-8")
        words = len(ch_text.split())
        print(f"  ch{ch_num:02d}.txt: {title} ({words} words)")
        saved += 1

    print(f"  Total: {saved} chapters saved")


def split_edwards_sermons():
    """에드워즈 설교선집 — Introduction + 7 sermons."""
    print("\n=== 에드워즈 설교선집 (Selected Sermons) ===")
    with open(RAW_DIR / "edwards_sermons_raw.txt", encoding="utf-8") as f:
        text = f.read()

    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    content = text[start:end].split("\n", 1)[1]

    # Split by sermon headers
    # The sermons start with their titles in ALL CAPS
    sermon_markers = [
        ("INTRODUCTION", "서론: 조나단 에드워즈의 생애"),
        ("GOD GLORIFIED IN MAN'S DEPENDENCE", "제1설교: 사람의 의존 안에서 영광 받으시는 하나님 (1731)"),
        ("A DIVINE AND SUPERNATURAL LIGHT", "제2설교: 거룩하고 초자연적인 빛 (1733)"),
        ("RUTH'S RESOLUTION", "제3설교: 룻의 결심 (1735)"),
        ("THE MANY MANSIONS", "제4설교: 많은 거처 (1737)"),
        ("SINNERS IN THE HANDS OF AN ANGRY GOD", "제5설교: 노한 하나님의 손 안에 있는 죄인들 (1741)"),
        ("GOD'S AWFUL JUDGMENT IN THE BREAKING AND WITHERING", "제6설교: 강한 막대기를 꺾고 시들게 하시는 하나님의 심판 (1748)"),
        ("A FAREWELL SERMON", "제7설교: 고별 설교 (1750)"),
    ]

    out_dir = BOOKS_DIR / "edwards-sermons"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Find positions of each sermon
    positions = []
    for marker, title in sermon_markers:
        # Find the line position
        idx = content.find("\n" + marker)
        if idx == -1:
            idx = content.find(marker)
        if idx != -1:
            positions.append((idx, title))

    # Also find NOTES section to exclude
    notes_idx = content.find("\nNOTES\n")
    if notes_idx == -1:
        notes_idx = len(content)

    positions.sort(key=lambda x: x[0])

    saved = 0
    for i, (pos, title) in enumerate(positions):
        end_pos = positions[i + 1][0] if i + 1 < len(positions) else notes_idx
        ch_text = content[pos:end_pos].strip()
        ch_text = re.sub(r"\n{3,}", "\n\n", ch_text)

        ch_num = i + 1
        outpath = out_dir / f"ch{ch_num:02d}.txt"
        outpath.write_text(ch_text + "\n", encoding="utf-8")
        words = len(ch_text.split())
        print(f"  ch{ch_num:02d}.txt: {title} ({words} words)")
        saved += 1

    print(f"  Total: {saved} chapters saved")


def split_paradise_lost():
    """실낙원 (Paradise Lost) — 12 Books."""
    print("\n=== 실낙원 (Paradise Lost) ===")
    with open(RAW_DIR / "paradise_lost_raw.txt", encoding="utf-8") as f:
        text = f.read()

    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    content = text[start:end].split("\n", 1)[1]

    # Split by "Book I", "Book II", etc.
    books = re.split(r"\n(Book [IVXLC]+)\n", content)

    out_dir = BOOKS_DIR / "paradise-lost"
    out_dir.mkdir(parents=True, exist_ok=True)
    saved = 0

    for i in range(1, len(books), 2):
        header = books[i].strip()
        body = books[i + 1].strip() if i + 1 < len(books) else ""
        book_num = (i // 2) + 1
        body = re.sub(r"\n{3,}", "\n\n", body)

        outpath = out_dir / f"ch{book_num:02d}.txt"
        outpath.write_text(f"{header}\n\n{body}\n", encoding="utf-8")

        words = len(body.split())
        print(f"  ch{book_num:02d}.txt: {header} ({words} words)")
        saved += 1

    print(f"  Total: {saved} chapters saved")


if __name__ == "__main__":
    split_grace_abounding()
    split_edwards_sermons()
    split_paradise_lost()
