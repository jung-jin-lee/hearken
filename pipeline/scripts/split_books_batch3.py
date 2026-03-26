#!/usr/bin/env python3
"""3차 도서 3권의 Gutenberg 원문을 챕터별로 분할하는 스크립트.

- 스펄전의 좁은 문 (Around the Wicket Gate) — 뉴턴 편지 대체
- 복낙원 (Paradise Regained)
- 폭스의 순교자 열전 (Fox's Book of Martyrs)

사용법:
  python3 pipeline/scripts/split_books_batch3.py
"""

import re
from pathlib import Path

RAW_DIR = Path("/tmp")
BOOKS_DIR = Path("pipeline/sources/data/books")


def split_spurgeon_wicket():
    """스펄전의 좁은 문 — 11 sections."""
    print("\n=== 스펄전의 좁은 문 (Around the Wicket Gate) ===")
    with open(RAW_DIR / "spurgeon_wicket_raw.txt", encoding="utf-8") as f:
        text = f.read()

    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    content = text[start:end].split("\n", 1)[1]

    # Section headers from table of contents
    section_markers = [
        ("PREFACE.", "서문"),
        ("AWAKENING.", "각성"),
        ("JESUS ONLY.", "오직 예수"),
        ("FAITH IN THE PERSON OF THE LORD JESUS.", "주 예수의 인격을 믿는 믿음"),
        ("FAITH VERY SIMPLE.", "매우 단순한 믿음"),
        ("FEARING TO BELIEVE.", "믿기를 두려워함"),
        ("DIFFICULTY IN THE WAY OF BELIEVING.", "믿음의 길에 있는 어려움"),
        ("A HELPFUL SURVEY.", "그리스도의 사역을 살펴봄"),
        ("A REAL HINDRANCE.", "믿음에 대한 참된 방해물"),
        ("ON RAISING QUESTIONS.", "질문을 제기함에 대하여"),
        ("WITHOUT FAITH NO SALVATION.", "믿음 없이는 구원 없다"),
        ("TO THOSE WHO HAVE BELIEVED.", "믿는 자들에게"),
    ]

    out_dir = BOOKS_DIR / "around-the-wicket-gate"
    out_dir.mkdir(parents=True, exist_ok=True)

    positions = []
    for marker, title in section_markers:
        idx = content.find("\n" + marker)
        if idx == -1:
            idx = content.find(marker)
        if idx != -1:
            positions.append((idx, title, marker))

    positions.sort(key=lambda x: x[0])

    # Find end: "DAMAGE." or Transcriber's notes or end
    damage_idx = content.find("\nDAMAGE.")
    end_content = damage_idx if damage_idx != -1 else len(content)

    saved = 0
    for i, (pos, title, marker) in enumerate(positions):
        end_pos = positions[i + 1][0] if i + 1 < len(positions) else end_content
        ch_text = content[pos:end_pos].strip()
        ch_text = re.sub(r"\[Illustration.*?\]", "", ch_text)
        ch_text = re.sub(r"\n{3,}", "\n\n", ch_text)

        ch_num = i + 1
        outpath = out_dir / f"ch{ch_num:02d}.txt"
        outpath.write_text(ch_text + "\n", encoding="utf-8")
        words = len(ch_text.split())
        print(f"  ch{ch_num:02d}.txt: {title} ({words} words)")
        saved += 1

    print(f"  Total: {saved} chapters saved")


def split_paradise_regained():
    """복낙원 (Paradise Regained) — 4 Books."""
    print("\n=== 복낙원 (Paradise Regained) ===")
    with open(RAW_DIR / "paradise_regained_raw.txt", encoding="utf-8") as f:
        text = f.read()

    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    content = text[start:end].split("\n", 1)[1]

    books = re.split(r"\n(THE (?:FIRST|SECOND|THIRD|FOURTH) BOOK)\n", content)

    out_dir = BOOKS_DIR / "paradise-regained"
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


def split_foxe_martyrs():
    """폭스의 순교자 열전 — 챕터 기반 분할.

    원본은 전반부(초대교회~중세)와 후반부(종교개혁)로 나뉘며
    총 46개 CHAPTER가 있지만, 전반부 23장은 짧고 후반부 23장은 길다.
    전반부는 5~6장씩 묶고, 후반부는 개별 챕터로 유지.
    """
    print("\n=== 폭스의 순교자 열전 (Fox's Book of Martyrs) ===")
    with open(RAW_DIR / "foxe_martyrs_raw.txt", encoding="utf-8") as f:
        text = f.read()

    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    full_content = text[start:end].split("\n", 1)[1]

    # The first set of CHAPTERs (lines ~265-560) is the Table of Contents.
    # The actual content starts at the SECOND "CHAPTER I." (line ~579).
    # Find the second occurrence of "CHAPTER I."
    lines = full_content.split("\n")
    first_ch1 = -1
    second_ch1 = -1
    for idx, line in enumerate(lines):
        if line.strip() == "CHAPTER I.":
            if first_ch1 == -1:
                first_ch1 = idx
            else:
                second_ch1 = idx
                break

    if second_ch1 == -1:
        print("  [오류] 본문 시작점을 찾을 수 없습니다")
        return

    content = "\n".join(lines[second_ch1:])

    # Split by CHAPTER headers
    parts = re.split(r"\n(CHAPTER [IVXLC]+\.)\n", content)

    chapters_raw = []
    for i in range(1, len(parts), 2):
        header = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        body = re.sub(r"\n{3,}", "\n\n", body)
        chapters_raw.append((header, body))

    # Also include the first chapter (before the first split)
    first_body = parts[0].strip()
    first_body = re.sub(r"\n{3,}", "\n\n", first_body)
    if first_body and len(first_body.split()) > 100:
        chapters_raw.insert(0, ("CHAPTER I.", first_body))

    print(f"  Found {len(chapters_raw)} content chapters (after skipping TOC)")

    out_dir = BOOKS_DIR / "foxe-martyrs"
    out_dir.mkdir(parents=True, exist_ok=True)

    # The book has two parts:
    # Part 1 (chapters 1-23): Early church to pre-Reformation - shorter chapters
    # Part 2 (chapters 24-46): Reformation era - longer chapters
    # We'll keep all chapters individually since each covers distinct martyrs/periods

    saved = 0
    for i, (header, body) in enumerate(chapters_raw):
        ch_num = i + 1
        outpath = out_dir / f"ch{ch_num:02d}.txt"
        outpath.write_text(f"{header}\n\n{body}\n", encoding="utf-8")
        words = len(body.split())
        if ch_num <= 5 or ch_num % 10 == 0 or ch_num > 43:
            print(f"  ch{ch_num:02d}.txt: {header} ({words} words)")
        saved += 1

    print(f"  Total: {saved} chapters saved")


if __name__ == "__main__":
    split_spurgeon_wicket()
    split_paradise_regained()
    split_foxe_martyrs()
