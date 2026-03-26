#!/usr/bin/env python3
"""1순위 도서 3권의 Gutenberg 원문을 챕터별로 분할하는 스크립트.

사용법:
  python pipeline/scripts/split_books.py
"""

import re
from pathlib import Path

RAW_DIR = Path("/tmp")
BOOKS_DIR = Path("pipeline/sources/data/books")


def split_confessions():
    """고백록 (Confessions) — 13 Books."""
    print("\n=== 고백록 (Confessions) ===")
    with open(RAW_DIR / "confessions_raw.txt", encoding="utf-8") as f:
        text = f.read()

    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    content = text[start:end].split("\n", 1)[1]

    books = re.split(r"\n(BOOK [IVXLC]+)\n", content)

    out_dir = BOOKS_DIR / "confessions"
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


def split_imitation():
    """그리스도를 본받아 (Imitation of Christ) — 4 Books, 114 Chapters.

    Book 3이 59장으로 너무 크므로, 4개 Book 단위로 분할합니다.
    각 Book 내 챕터는 하나의 파일로 합칩니다.
    """
    print("\n=== 그리스도를 본받아 (Imitation of Christ) ===")
    with open(RAW_DIR / "imitation_raw.txt", encoding="utf-8") as f:
        text = f.read()

    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    content = text[start:end].split("\n", 1)[1]

    # Split into 4 books
    book_splits = re.split(
        r"\n(THE (?:FIRST|SECOND|THIRD|FOURTH) BOOK)\n", content
    )

    out_dir = BOOKS_DIR / "imitation-of-christ"
    out_dir.mkdir(parents=True, exist_ok=True)

    book_names = {
        "THE FIRST BOOK": ("제1권: 영적 생활에 유익한 권고", 25),
        "THE SECOND BOOK": ("제2권: 내적 생활에 관한 권고", 12),
        "THE THIRD BOOK": ("제3권: 내적 위로에 관하여", 59),
        "THE FOURTH BOOK": ("제4권: 성체에 관하여", 18),
    }

    # Now split each book into individual chapters
    saved = 0
    chapter_global = 0

    for i in range(1, len(book_splits), 2):
        book_header = book_splits[i].strip()
        book_body = book_splits[i + 1] if i + 1 < len(book_splits) else ""
        book_num = (i // 2) + 1

        # Split chapters within this book
        chapters = re.split(r"\n(CHAPTER [IVXLC]+)\n", book_body)

        for j in range(1, len(chapters), 2):
            ch_header = chapters[j].strip()
            ch_body = chapters[j + 1].strip() if j + 1 < len(chapters) else ""
            ch_body = re.sub(r"\n{3,}", "\n\n", ch_body)
            chapter_global += 1

            outpath = out_dir / f"ch{chapter_global:03d}.txt"
            outpath.write_text(
                f"Book {book_num} — {ch_header}\n\n{ch_body}\n",
                encoding="utf-8",
            )

            words = len(ch_body.split())
            if chapter_global <= 5 or chapter_global % 20 == 0:
                print(f"  ch{chapter_global:03d}.txt: Book {book_num} {ch_header} ({words} words)")
            saved += 1

    print(f"  Total: {saved} chapters saved")


def split_holy_war():
    """거룩한 전쟁 (The Holy War) — 챕터 없는 연속 서사, 단락 기반 ~20장 분할."""
    print("\n=== 거룩한 전쟁 (The Holy War) ===")
    with open(RAW_DIR / "holywar_raw.txt", encoding="utf-8") as f:
        text = f.read()

    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    content = text[start:end].split("\n", 1)[1]

    # Remove title block and front matter (find first paragraph)
    # Skip until we find the actual story beginning
    lines = content.split("\n")

    # Find the start of actual prose (after title block)
    prose_start = 0
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("In my travels,") or stripped.startswith("IN my travels"):
            prose_start = idx
            break
        # Also check for common opening
        if "I have used similitudes" in stripped:
            continue
        if len(stripped) > 80 and idx > 50:
            prose_start = idx
            break

    prose_text = "\n".join(lines[prose_start:]).strip()
    # Clean up picture/illustration markers
    prose_text = re.sub(r"\[Picture:.*?\]", "", prose_text)
    prose_text = re.sub(r"\{[0-9]+\}", "", prose_text)
    prose_text = re.sub(r"\n{3,}", "\n\n", prose_text)

    # Split into paragraphs
    paragraphs = [p.strip() for p in prose_text.split("\n\n") if p.strip()]
    total_words = sum(len(p.split()) for p in paragraphs)
    target_chapters = 20
    words_per_chapter = total_words // target_chapters

    print(f"  Total words: {total_words}, target ~{words_per_chapter} words/chapter")

    out_dir = BOOKS_DIR / "holy-war"
    out_dir.mkdir(parents=True, exist_ok=True)

    chapters = []
    current_chapter = []
    current_words = 0

    for para in paragraphs:
        para_words = len(para.split())
        current_chapter.append(para)
        current_words += para_words

        if current_words >= words_per_chapter and len(chapters) < target_chapters - 1:
            chapters.append("\n\n".join(current_chapter))
            current_chapter = []
            current_words = 0

    # Remaining goes to last chapter
    if current_chapter:
        chapters.append("\n\n".join(current_chapter))

    for idx, ch_text in enumerate(chapters, 1):
        outpath = out_dir / f"ch{idx:02d}.txt"
        outpath.write_text(ch_text + "\n", encoding="utf-8")
        words = len(ch_text.split())
        print(f"  ch{idx:02d}.txt: ({words} words)")

    print(f"  Total: {len(chapters)} chapters saved")


if __name__ == "__main__":
    split_confessions()
    split_imitation()
    split_holy_war()
