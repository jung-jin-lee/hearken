#!/usr/bin/env python3
"""5차 도서 8권 분할 스크립트.

대상:
  1. Holiness (J.C. 라일) — 20장
  2. Heretics (체스터턴) — 20장
  3. Galatians Commentary (루터) — 6장
  4. Ascent of Mount Carmel (십자가의 요한) — 3권 다수 장
  5. 95 Theses (루터) — 단일 문서
  6. Absolute Surrender (앤드류 머레이) — 3개 강연
  7. Waiting on God (앤드류 머레이) — 31일 묵상
  8. Concerning Christian Liberty (루터) — 단일 논문

사용법:
  python pipeline/scripts/split_books_batch5.py
"""

import json
import re
from pathlib import Path

BOOKS_DIR = Path("pipeline/sources/data/books")


def clean_text(text: str) -> str:
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def save_chapter(out_dir: Path, num: int, text: str, label: str = ""):
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"ch{num:02d}.txt"
    path.write_text(clean_text(text) + "\n", encoding="utf-8")
    words = len(text.split())
    print(f"  ch{num:02d}.txt: {label} ({words} words)")


def save_metadata(out_dir: Path, meta: dict):
    path = out_dir / "metadata.json"
    path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  metadata.json ({len(meta['chapters'])} chapters)")


def split_by_word_limit(text, max_words=8000):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = []
    current_words = 0
    for para in paragraphs:
        pw = len(para.split())
        if current_words + pw > max_words and current:
            chunks.append("\n\n".join(current))
            current = [para]
            current_words = pw
        else:
            current.append(para)
            current_words += pw
    if current:
        chunks.append("\n\n".join(current))
    return chunks


# ─── 1. Holiness — J.C. Ryle ───
def split_holiness():
    print("\n=== 거룩 (Holiness) ===")
    raw = (BOOKS_DIR / "holiness-ryle" / "raw.txt").read_text(encoding="utf-8")
    lines = raw.split("\n")

    # 챕터는 "II.\nSANCTIFICATION" 형식 (Roman numeral 단독 줄 + 제목 줄)
    # 단, TOC의 "   I.           SIN                            1" 과 구분 필요
    chapter_lines = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        # "II." or "XIV." 등 단독 줄 (TOC 아님 — TOC는 같은 줄에 제목과 페이지 번호)
        if re.match(r"^[IVXLC]+\.\s*$", stripped) and i > 100:
            # 다음 줄이 대문자 제목인지 확인
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and next_line == next_line.upper() and len(next_line) > 2:
                    chapter_lines.append(i)

    out_dir = BOOKS_DIR / "holiness-ryle"
    chapters_meta = []
    ch_num = 0

    for idx, start in enumerate(chapter_lines):
        end = chapter_lines[idx + 1] if idx + 1 < len(chapter_lines) else len(lines)
        text_block = "\n".join(lines[start:end])
        title = lines[start + 1].strip() if start + 1 < len(lines) else ""

        chunks = split_by_word_limit(text_block, max_words=8000)
        for ci, chunk in enumerate(chunks):
            ch_num += 1
            if len(chunks) == 1:
                label = title
            else:
                label = f"{title} ({ci+1}/{len(chunks)})"
            save_chapter(out_dir, ch_num, chunk, label)
            chapters_meta.append({"num": ch_num, "title": label, "file": f"ch{ch_num:02d}.txt"})

    save_metadata(out_dir, {
        "slug": "holiness-ryle",
        "title": "거룩",
        "title_original": "Holiness: Its Nature, Hindrances, Difficulties, and Roots",
        "author": "J.C. 라일 (J.C. Ryle)",
        "author_original": "J.C. Ryle",
        "year": "1877",
        "source": "https://ccel.org/ccel/ryle/holiness",
        "license": "public_domain",
        "chapters": chapters_meta,
    })


# ─── 2. Heretics — Chesterton ───
def split_heretics():
    print("\n=== 이단자들 (Heretics) ===")
    raw = (BOOKS_DIR / "heretics" / "raw.txt").read_text(encoding="utf-8")
    lines = raw.split("\n")

    chapter_pattern = re.compile(r"^[IVXLC]+\.\s+[A-Z]")
    chapter_lines = []
    chapter_titles = []

    for i, line in enumerate(lines):
        if chapter_pattern.match(line.strip()):
            chapter_lines.append(i)
            title = re.sub(r"^[IVXLC]+\.\s*", "", line.strip())
            chapter_titles.append(title)

    out_dir = BOOKS_DIR / "heretics"
    chapters_meta = []

    for idx, start in enumerate(chapter_lines):
        end = chapter_lines[idx + 1] if idx + 1 < len(chapter_lines) else None
        if end is None:
            for j in range(len(lines) - 1, start, -1):
                if "END OF THE PROJECT GUTENBERG" in lines[j]:
                    end = j
                    break
            if end is None:
                end = len(lines)
        text_block = "\n".join(lines[start:end])
        title = chapter_titles[idx]
        save_chapter(out_dir, idx + 1, text_block, title)
        chapters_meta.append({"num": idx + 1, "title": title, "file": f"ch{idx+1:02d}.txt"})

    save_metadata(out_dir, {
        "slug": "heretics",
        "title": "이단자들",
        "title_original": "Heretics",
        "author": "G.K. 체스터턴 (G.K. Chesterton)",
        "author_original": "G.K. Chesterton",
        "year": "1905",
        "source": "https://www.gutenberg.org/ebooks/470",
        "license": "public_domain",
        "chapters": chapters_meta,
    })


# ─── 3. Galatians Commentary — Luther ───
def split_galatians():
    print("\n=== 갈라디아서 주석 (Galatians Commentary) ===")
    raw = (BOOKS_DIR / "galatians-luther" / "raw.txt").read_text(encoding="utf-8")
    lines = raw.split("\n")

    chapter_pattern = re.compile(r"^CHAPTER\s+\d+")
    chapter_lines = []

    for i, line in enumerate(lines):
        if chapter_pattern.match(line.strip()):
            chapter_lines.append(i)

    out_dir = BOOKS_DIR / "galatians-luther"
    chapters_meta = []

    for idx, start in enumerate(chapter_lines):
        end = chapter_lines[idx + 1] if idx + 1 < len(chapter_lines) else None
        if end is None:
            for j in range(len(lines) - 1, start, -1):
                if "END OF THE PROJECT GUTENBERG" in lines[j]:
                    end = j
                    break
            if end is None:
                end = len(lines)

        text_block = "\n".join(lines[start:end])
        ch_num_match = re.search(r"CHAPTER\s+(\d+)", lines[start])
        ch_label = f"갈라디아서 {ch_num_match.group(1)}장 주석" if ch_num_match else f"Chapter {idx+1}"

        # Split long chapters
        chunks = split_by_word_limit(text_block, max_words=8000)
        for ci, chunk in enumerate(chunks):
            ch_global = sum(len(split_by_word_limit("\n".join(lines[chapter_lines[k]:chapter_lines[k+1] if k+1 < len(chapter_lines) else len(lines)]), 8000)) for k in range(idx)) + ci + 1
            if len(chunks) == 1:
                label = ch_label
            else:
                label = f"{ch_label} ({ci+1}/{len(chunks)})"
            save_chapter(out_dir, ch_global, chunk, label)
            chapters_meta.append({"num": ch_global, "title": label, "file": f"ch{ch_global:02d}.txt"})

    save_metadata(out_dir, {
        "slug": "galatians-luther",
        "title": "갈라디아서 주석",
        "title_original": "Commentary on the Epistle to the Galatians",
        "author": "마르틴 루터 (Martin Luther)",
        "author_original": "Martin Luther",
        "year": "1535",
        "source": "https://www.gutenberg.org/ebooks/1549",
        "license": "public_domain",
        "chapters": chapters_meta,
    })


# ─── 4. Ascent of Mount Carmel ───
def split_ascent():
    print("\n=== 갈멜산 등정 (Ascent of Mount Carmel) ===")
    raw = (BOOKS_DIR / "ascent-mount-carmel" / "raw.txt").read_text(encoding="utf-8")
    lines = raw.split("\n")

    chapter_pattern = re.compile(r"^CHAPTER\s+([IVXLC]+)\s*$")
    chapter_lines = []
    current_book = 0

    for i, line in enumerate(lines):
        m = chapter_pattern.match(line.strip())
        if m:
            roman = m.group(1)
            if roman == "I" and chapter_lines:
                current_book += 1
            if not chapter_lines:
                current_book = 1
            chapter_lines.append((i, roman, current_book))

    out_dir = BOOKS_DIR / "ascent-mount-carmel"
    chapters_meta = []
    ch_global = 0

    for idx, (start, roman, book) in enumerate(chapter_lines):
        end = chapter_lines[idx + 1][0] if idx + 1 < len(chapter_lines) else len(lines)
        text_block = "\n".join(lines[start:end])

        title = ""
        for k in range(start + 1, min(start + 15, len(lines))):
            stripped = lines[k].strip()
            if stripped and not stripped.startswith("CHAPTER"):
                title = stripped[:80]
                break

        ch_global += 1
        label = f"제{book}권 {roman}장: {title}"
        save_chapter(out_dir, ch_global, text_block, label)
        chapters_meta.append({"num": ch_global, "title": label, "file": f"ch{ch_global:02d}.txt"})

    save_metadata(out_dir, {
        "slug": "ascent-mount-carmel",
        "title": "갈멜산 등정",
        "title_original": "Ascent of Mount Carmel",
        "author": "십자가의 요한 (St. John of the Cross)",
        "author_original": "St. John of the Cross",
        "year": "1585",
        "source": "https://ccel.org/ccel/john_cross/ascent",
        "license": "public_domain",
        "note": "E. Allison Peers 영역본. 어둔 밤의 전편.",
        "chapters": chapters_meta,
    })


# ─── 5. 95 Theses ───
def split_theses():
    print("\n=== 95개 논제 (Ninety-Five Theses) ===")
    raw = (BOOKS_DIR / "ninety-five-theses" / "raw.txt").read_text(encoding="utf-8")
    lines = raw.split("\n")

    # Find the start of the theses (line with "1.")
    content_start = 0
    for i, line in enumerate(lines):
        if re.match(r"^\s*1\.\s+", line):
            content_start = i
            break

    # Find end - before Latin text or footnotes
    content_end = len(lines)
    for i in range(content_start + 1, len(lines)):
        if "DISPUTATIO PRO DECLARATIONE" in lines[i]:
            content_end = i
            break

    text = "\n".join(lines[content_start:content_end])
    out_dir = BOOKS_DIR / "ninety-five-theses"
    save_chapter(out_dir, 1, text, "95개 논제 전문")

    save_metadata(out_dir, {
        "slug": "ninety-five-theses",
        "title": "95개 논제",
        "title_original": "Disputation on the Power and Efficacy of Indulgences (Ninety-Five Theses)",
        "author": "마르틴 루터 (Martin Luther)",
        "author_original": "Martin Luther",
        "year": "1517",
        "source": "https://ccel.org/ccel/luther/theses",
        "license": "public_domain",
        "chapters": [{"num": 1, "title": "95개 논제 전문", "file": "ch01.txt"}],
    })


# ─── 6. Absolute Surrender ───
def split_surrender():
    print("\n=== 절대 항복 (Absolute Surrender) ===")
    raw = (BOOKS_DIR / "absolute-surrender" / "raw.txt").read_text(encoding="utf-8")
    lines = raw.split("\n")

    # Section headers are ALL-CAPS at start of line (no leading spaces)
    section_lines = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if (re.match(r"^[A-Z][A-Z ]{5,}[A-Z]$", stripped)
                and i > 20 and "CCEL" not in stripped):
            section_lines.append((i, stripped))

    out_dir = BOOKS_DIR / "absolute-surrender"
    chapters_meta = []

    for idx, (start, title) in enumerate(section_lines):
        end = section_lines[idx + 1][0] if idx + 1 < len(section_lines) else len(lines)
        text_block = "\n".join(lines[start:end])

        chunks = split_by_word_limit(text_block, max_words=8000)
        for ci, chunk in enumerate(chunks):
            ch_num = sum(len(split_by_word_limit("\n".join(lines[section_lines[k][0]:section_lines[k+1][0] if k+1 < len(section_lines) else len(lines)]), 8000)) for k in range(idx)) + ci + 1
            if len(chunks) == 1:
                label = title.title()
            else:
                label = f"{title.title()} ({ci+1}/{len(chunks)})"
            save_chapter(out_dir, ch_num, chunk, label)
            chapters_meta.append({"num": ch_num, "title": label, "file": f"ch{ch_num:02d}.txt"})

    save_metadata(out_dir, {
        "slug": "absolute-surrender",
        "title": "절대 항복",
        "title_original": "Absolute Surrender",
        "author": "앤드류 머레이 (Andrew Murray)",
        "author_original": "Andrew Murray",
        "year": "1895",
        "source": "https://ccel.org/ccel/murray/surrender",
        "license": "public_domain",
        "chapters": chapters_meta,
    })


# ─── 7. Waiting on God ───
def split_waiting():
    print("\n=== 하나님을 기다리며 (Waiting on God) ===")
    raw = (BOOKS_DIR / "waiting-on-god" / "raw.txt").read_text(encoding="utf-8")
    lines = raw.split("\n")

    day_pattern = re.compile(r"^\s*(First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|Thirteenth|Fourteenth|Fifteenth|Sixteenth|Seventeenth|Eighteenth|Nineteenth|Twentieth|Twenty-First|Twenty-Second|Twenty-Third|Twenty-Fourth|Twenty-Fifth|Twenty-Sixth|Twenty-Seventh|Twenty-Eighth|Twenty-Ninth|Thirtieth|Thirtieth-First)\s+Day", re.IGNORECASE)
    day_lines = []

    for i, line in enumerate(lines):
        if day_pattern.match(line.strip()):
            day_lines.append(i)

    out_dir = BOOKS_DIR / "waiting-on-god"
    chapters_meta = []

    for idx, start in enumerate(day_lines):
        end = day_lines[idx + 1] if idx + 1 < len(day_lines) else len(lines)
        text_block = "\n".join(lines[start:end])

        title = lines[start].strip()
        ch_num = idx + 1
        save_chapter(out_dir, ch_num, text_block, title)
        chapters_meta.append({"num": ch_num, "title": f"{ch_num}일째: {title}", "file": f"ch{ch_num:02d}.txt"})

    save_metadata(out_dir, {
        "slug": "waiting-on-god",
        "title": "하나님을 기다리며",
        "title_original": "Waiting on God!",
        "author": "앤드류 머레이 (Andrew Murray)",
        "author_original": "Andrew Murray",
        "year": "1895",
        "source": "https://ccel.org/ccel/murray/waiting",
        "license": "public_domain",
        "note": "31일 묵상",
        "chapters": chapters_meta,
    })


# ─── 8. Concerning Christian Liberty ───
def split_liberty():
    print("\n=== 기독교인의 자유 (Concerning Christian Liberty) ===")
    raw = (BOOKS_DIR / "christian-liberty" / "raw.txt").read_text(encoding="utf-8")
    lines = raw.split("\n")

    # Find "LETTER" and main treatise as two sections
    sections = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("LETTER OF MARTIN LUTHER TO POPE LEO"):
            sections.append((i, "교황 레오 10세에게 보내는 편지"))
        elif stripped == "CONCERNING CHRISTIAN LIBERTY" and i > 100:
            sections.append((i, "기독교인의 자유에 관하여"))

    out_dir = BOOKS_DIR / "christian-liberty"
    chapters_meta = []

    for idx, (start, title) in enumerate(sections):
        end = sections[idx + 1][0] if idx + 1 < len(sections) else len(lines)
        text_block = "\n".join(lines[start:end])

        chunks = split_by_word_limit(text_block, max_words=8000)
        for ci, chunk in enumerate(chunks):
            ch_num = len(chapters_meta) + 1
            if len(chunks) == 1:
                label = title
            else:
                label = f"{title} ({ci+1}/{len(chunks)})"
            save_chapter(out_dir, ch_num, chunk, label)
            chapters_meta.append({"num": ch_num, "title": label, "file": f"ch{ch_num:02d}.txt"})

    save_metadata(out_dir, {
        "slug": "christian-liberty",
        "title": "기독교인의 자유",
        "title_original": "Concerning Christian Liberty",
        "author": "마르틴 루터 (Martin Luther)",
        "author_original": "Martin Luther",
        "year": "1520",
        "source": "https://ccel.org/ccel/luther/christianliberty",
        "license": "public_domain",
        "chapters": chapters_meta,
    })


if __name__ == "__main__":
    split_holiness()
    split_heretics()
    split_galatians()
    split_ascent()
    split_theses()
    split_surrender()
    split_waiting()
    split_liberty()
    print("\n✅ 8권 분할 완료!")
