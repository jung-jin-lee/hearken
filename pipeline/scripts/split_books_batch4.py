#!/usr/bin/env python3
"""4차 도서 6권 분할 스크립트.

대상:
  1. Humility (앤드류 머레이) — 12장
  2. Orthodoxy (G.K. 체스터턴) — 9장
  3. The Ministry of Intercession (앤드류 머레이) — 15장
  4. Morning and Evening (스펄전) — 월별 12장
  5. Religious Affections (조나단 에드워즈) — 파트/섹션별 분할
  6. Dark Night of the Soul (십자가의 요한) — 2권 39장

사용법:
  python pipeline/scripts/split_books_batch4.py
"""

import json
import re
from pathlib import Path

BOOKS_DIR = Path("pipeline/sources/data/books")


def clean_text(text: str) -> str:
    """CCEL/Gutenberg 참조 번호 및 과도한 공백 정리."""
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def save_chapter(out_dir: Path, num: int, text: str, label: str = ""):
    """챕터 파일 저장."""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"ch{num:02d}.txt"
    path.write_text(clean_text(text) + "\n", encoding="utf-8")
    words = len(text.split())
    print(f"  ch{num:02d}.txt: {label} ({words} words)")


def save_metadata(out_dir: Path, meta: dict):
    """metadata.json 저장."""
    path = out_dir / "metadata.json"
    path.write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"  metadata.json 저장 완료 ({len(meta['chapters'])} chapters)")


# ──────────────────────────────────────────────
# 1. Humility — 12 Roman numeral sections
# ──────────────────────────────────────────────
def split_humility():
    print("\n=== 겸손 (Humility) ===")
    raw = (BOOKS_DIR / "humility" / "raw.txt").read_text(encoding="utf-8")
    lines = raw.split("\n")

    # 챕터 시작 라인 찾기 (1-indexed in grep → 0-indexed here)
    chapter_lines = []
    for i, line in enumerate(lines):
        if re.match(r"^(I|V|X)+\.\s*$", line.strip()):
            chapter_lines.append(i)

    titles = [
        "Humility: The Glory of the Creature",
        "Humility: The Secret of Redemption",
        "Humility: In the Life of Jesus",
        "Humility: In the Teaching of Jesus",
        "Humility: In the Disciples of Jesus",
        "Humility: In Daily Life",
        "Humility and Holiness",
        "Humility and Sin",
        "Humility and Faith",
        "Humility and Death to Self",
        "Humility and Happiness",
        "Humility and Exaltation",
    ]

    out_dir = BOOKS_DIR / "humility"
    chapters_meta = []

    for idx, start in enumerate(chapter_lines):
        end = chapter_lines[idx + 1] if idx + 1 < len(chapter_lines) else len(lines)
        # Notes 섹션 전에서 끝내기
        text_block = "\n".join(lines[start:end])
        if "NOTE A--" in text_block:
            text_block = text_block[: text_block.index("NOTE A--")]

        save_chapter(out_dir, idx + 1, text_block, titles[idx] if idx < len(titles) else "")
        chapters_meta.append({
            "num": idx + 1,
            "title": titles[idx] if idx < len(titles) else f"Chapter {idx + 1}",
            "file": f"ch{idx + 1:02d}.txt",
        })

    save_metadata(out_dir, {
        "slug": "humility",
        "title": "겸손",
        "title_original": "Humility: The Beauty of Holiness",
        "author": "앤드류 머레이 (Andrew Murray)",
        "author_original": "Andrew Murray",
        "year": "1895",
        "source": "https://www.gutenberg.org/ebooks/57121",
        "license": "public_domain",
        "chapters": chapters_meta,
    })


# ──────────────────────────────────────────────
# 2. Orthodoxy — 9 chapters
# ──────────────────────────────────────────────
def split_orthodoxy():
    print("\n=== 정통 (Orthodoxy) ===")
    raw = (BOOKS_DIR / "orthodoxy" / "raw.txt").read_text(encoding="utf-8")
    lines = raw.split("\n")

    chapter_pattern = re.compile(r"^CHAPTER\s+[IVXLC]+")
    chapter_lines = []
    chapter_titles = []

    for i, line in enumerate(lines):
        if chapter_pattern.match(line.strip()):
            chapter_lines.append(i)
            # Extract title: "CHAPTER I.--_Introduction in Defence of Everything Else_"
            title = re.sub(r"^CHAPTER\s+[IVXLC]+\.?--?_?", "", line.strip())
            title = title.rstrip("_").strip()
            chapter_titles.append(title)

    out_dir = BOOKS_DIR / "orthodoxy"
    chapters_meta = []

    for idx, start in enumerate(chapter_lines):
        end = chapter_lines[idx + 1] if idx + 1 < len(chapter_lines) else None
        if end is None:
            # Find Gutenberg footer
            for j in range(len(lines) - 1, start, -1):
                if "END OF THE PROJECT GUTENBERG" in lines[j]:
                    end = j
                    break
            if end is None:
                end = len(lines)

        text_block = "\n".join(lines[start:end])
        title = chapter_titles[idx]
        save_chapter(out_dir, idx + 1, text_block, title)
        chapters_meta.append({
            "num": idx + 1,
            "title": title,
            "file": f"ch{idx + 1:02d}.txt",
        })

    save_metadata(out_dir, {
        "slug": "orthodoxy",
        "title": "정통",
        "title_original": "Orthodoxy",
        "author": "G.K. 체스터턴 (G.K. Chesterton)",
        "author_original": "G.K. Chesterton",
        "year": "1908",
        "source": "https://www.gutenberg.org/ebooks/16769",
        "license": "public_domain",
        "chapters": chapters_meta,
    })


# ──────────────────────────────────────────────
# 3. The Ministry of Intercession — 15 chapters
# ──────────────────────────────────────────────
def split_prayer():
    print("\n=== 중보기도의 사역 (The Ministry of Intercession) ===")
    raw = (BOOKS_DIR / "prayer-andrew-murray" / "raw.txt").read_text(encoding="utf-8")
    lines = raw.split("\n")

    chapter_pattern = re.compile(r"^CHAPTER\s+[IVXLC]+\s*$")
    chapter_lines = []

    for i, line in enumerate(lines):
        if chapter_pattern.match(line.strip()):
            chapter_lines.append(i)

    # 각 챕터의 제목은 CHAPTER 다음 줄들에 있음
    out_dir = BOOKS_DIR / "prayer-andrew-murray"
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

        # 제목 추출: CHAPTER 다음 비어있지 않은 줄
        title = ""
        for k in range(start + 1, min(start + 10, len(lines))):
            stripped = lines[k].strip()
            if stripped and not stripped.startswith("CHAPTER"):
                title = stripped.strip("_").strip()
                break

        save_chapter(out_dir, idx + 1, text_block, title)
        chapters_meta.append({
            "num": idx + 1,
            "title": title or f"Chapter {idx + 1}",
            "file": f"ch{idx + 1:02d}.txt",
        })

    save_metadata(out_dir, {
        "slug": "prayer-andrew-murray",
        "title": "중보기도의 사역",
        "title_original": "The Ministry of Intercession: A Plea for More Prayer",
        "author": "앤드류 머레이 (Andrew Murray)",
        "author_original": "Andrew Murray",
        "year": "1898",
        "source": "https://www.gutenberg.org/ebooks/29296",
        "license": "public_domain",
        "chapters": chapters_meta,
    })


# ──────────────────────────────────────────────
# 4. Morning and Evening — 주별 53장
# ──────────────────────────────────────────────
def split_morning_evening():
    print("\n=== 아침저녁 (Morning and Evening) ===")
    raw = (BOOKS_DIR / "morning-evening" / "raw.txt").read_text(encoding="utf-8")
    lines = raw.split("\n")

    months_kr = {
        "January": "1월", "February": "2월", "March": "3월",
        "April": "4월", "May": "5월", "June": "6월",
        "July": "7월", "August": "8월", "September": "9월",
        "October": "10월", "November": "11월", "December": "12월",
    }

    # 모든 Morning 엔트리의 시작 라인 찾기
    morning_pattern = re.compile(r"^Morning, (\w+) (\d+)$")
    day_starts = []
    for i, line in enumerate(lines):
        m = morning_pattern.match(line.strip())
        if m:
            day_starts.append((i, m.group(1), int(m.group(2))))

    # 7일씩 묶어서 주별 챕터 생성
    out_dir = BOOKS_DIR / "morning-evening"
    chapters_meta = []
    week_size = 7
    ch_num = 0

    for w in range(0, len(day_starts), week_size):
        week_days = day_starts[w:w + week_size]
        start = week_days[0][0]
        if w + week_size < len(day_starts):
            end = day_starts[w + week_size][0]
        else:
            end = len(lines)

        text_block = "\n".join(lines[start:end])
        first_month = week_days[0][1]
        first_day = week_days[0][2]
        last_month = week_days[-1][1]
        last_day = week_days[-1][2]

        if first_month == last_month:
            label = f"{months_kr[first_month]} {first_day}-{last_day}일"
        else:
            label = f"{months_kr[first_month]} {first_day}일 - {months_kr[last_month]} {last_day}일"

        ch_num += 1
        save_chapter(out_dir, ch_num, text_block, label)
        chapters_meta.append({
            "num": ch_num,
            "title": label,
            "file": f"ch{ch_num:02d}.txt",
        })

    save_metadata(out_dir, {
        "slug": "morning-evening",
        "title": "아침저녁",
        "title_original": "Morning and Evening: Daily Readings",
        "author": "C.H. 스펄전 (C.H. Spurgeon)",
        "author_original": "C.H. Spurgeon",
        "year": "1866",
        "source": "https://ccel.org/ccel/spurgeon/morneve",
        "license": "public_domain",
        "note": "365일 매일 묵상 (아침/저녁), 주별로 분할",
        "chapters": chapters_meta,
    })


# ──────────────────────────────────────────────
# 5. Religious Affections — 3파트, 섹션별 분할
# ──────────────────────────────────────────────
def split_religious_affections():
    print("\n=== 종교적 정서론 (Religious Affections) ===")
    raw = (BOOKS_DIR / "religious-affections" / "raw.txt").read_text(encoding="utf-8")
    lines = raw.split("\n")

    # CCEL 헤더 제거: "INTRODUCTION." 이후부터 시작
    content_start = 0
    for i, line in enumerate(lines):
        if line.strip() == "INTRODUCTION.":
            content_start = i
            break

    # PART 경계 찾기
    part_lines = [content_start]
    for i, line in enumerate(lines):
        if re.match(r"\s*PART\s+(II|III)\.\s*$", line.strip()):
            part_lines.append(i)

    # Part 2와 Part 3의 Roman numeral 섹션 경계 찾기
    def find_sections(start_line, end_line):
        """파트 내의 Roman numeral 섹션 경계를 찾는다."""
        candidates = []
        for i in range(start_line, end_line):
            line = lines[i]
            m = re.match(r"^\s+(I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII)\.\s+\w", line)
            if m:
                roman = m.group(1)
                if len(line.strip()) > 30:
                    candidates.append((i, roman))

        # 너무 가까운 연속 후보 필터링 (서론 목록 항목 제거)
        # 실제 섹션은 100줄 이상 간격, 서론 항목은 10줄 이내
        sections = []
        for idx, (line_num, roman) in enumerate(candidates):
            next_line = candidates[idx + 1][0] if idx + 1 < len(candidates) else end_line
            gap = next_line - line_num
            if gap > 50:  # 50줄 이상이면 실제 섹션
                sections.append((line_num, roman))
        return sections

    part2_start = part_lines[1]
    part3_start = part_lines[2]

    # Part 2 섹션들 (Signs I-XII that are NOT signs)
    part2_sections = find_sections(part2_start, part3_start)
    # Part 3 섹션들 (Signs I-XII of true affections)
    part3_sections = find_sections(part3_start, len(lines))

    out_dir = BOOKS_DIR / "religious-affections"
    chapters_meta = []
    ch_num = 0

    # 각 섹션을 개별 챕터로 분할 (Part 1은 단락 기반 분할)
    def split_by_word_limit(text_lines, max_words=8000):
        """긴 텍스트를 max_words 단위로 단락 경계에서 분할."""
        full_text = "\n".join(text_lines)
        paragraphs = [p.strip() for p in full_text.split("\n\n") if p.strip()]
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

    # Part 1: 서론 + 정서의 본질 (단락 기반 분할)
    part1_text = lines[content_start:part2_start]
    part1_chunks = split_by_word_limit(part1_text, max_words=8000)
    for ci, chunk in enumerate(part1_chunks):
        ch_num += 1
        label = f"제1부: 정서의 본질 ({ci + 1}/{len(part1_chunks)})"
        save_chapter(out_dir, ch_num, chunk, label)
        chapters_meta.append({
            "num": ch_num,
            "title": label,
            "file": f"ch{ch_num:02d}.txt",
        })

    # Part 2, Part 3: 각 Roman numeral 섹션을 개별 챕터로
    def split_sections_individually(sections, part_end, part_name):
        nonlocal ch_num
        for s_idx, (start, roman) in enumerate(sections):
            if s_idx + 1 < len(sections):
                end = sections[s_idx + 1][0]
            else:
                end = part_end

            section_lines = lines[start:end]
            section_chunks = split_by_word_limit(section_lines, max_words=8000)

            for ci, chunk in enumerate(section_chunks):
                ch_num += 1
                if len(section_chunks) == 1:
                    label = f"{part_name} 표지 {roman}"
                else:
                    label = f"{part_name} 표지 {roman} ({ci + 1}/{len(section_chunks)})"
                save_chapter(out_dir, ch_num, chunk, label)
                chapters_meta.append({
                    "num": ch_num,
                    "title": label,
                    "file": f"ch{ch_num:02d}.txt",
                })

    split_sections_individually(part2_sections, part3_start, "제2부: 불확실한")
    split_sections_individually(part3_sections, len(lines), "제3부: 참된 정서의")

    save_metadata(out_dir, {
        "slug": "religious-affections",
        "title": "종교적 정서론",
        "title_original": "A Treatise Concerning Religious Affections",
        "author": "조나단 에드워즈 (Jonathan Edwards)",
        "author_original": "Jonathan Edwards",
        "year": "1746",
        "source": "https://ccel.org/ccel/edwards/affections",
        "license": "public_domain",
        "chapters": chapters_meta,
    })


# ──────────────────────────────────────────────
# 6. Dark Night of the Soul — 2권 39장
# ──────────────────────────────────────────────
def split_dark_night():
    print("\n=== 어둔 밤 (Dark Night of the Soul) ===")
    raw = (BOOKS_DIR / "dark-night-of-soul" / "raw.txt").read_text(encoding="utf-8")
    lines = raw.split("\n")

    # 챕터 경계 찾기
    chapter_pattern = re.compile(r"^CHAPTER\s+([IVXLC]+)\s*$")
    chapter_lines = []
    current_book = 0

    # Book 경계: Book 1은 첫 번째 CHAPTER I, Book 2는 14장 이후 다시 CHAPTER I
    for i, line in enumerate(lines):
        m = chapter_pattern.match(line.strip())
        if m:
            roman = m.group(1)
            if roman == "I" and chapter_lines:
                current_book = 2
            if not chapter_lines:
                current_book = 1
            chapter_lines.append((i, roman, current_book))

    out_dir = BOOKS_DIR / "dark-night-of-soul"
    chapters_meta = []
    ch_global = 0

    for idx, (start, roman, book) in enumerate(chapter_lines):
        end = chapter_lines[idx + 1][0] if idx + 1 < len(chapter_lines) else len(lines)
        text_block = "\n".join(lines[start:end])

        # 제목 추출: CHAPTER 다음 비어있지 않은 줄
        title = ""
        for k in range(start + 1, min(start + 15, len(lines))):
            stripped = lines[k].strip()
            if stripped and not stripped.startswith("CHAPTER"):
                title = stripped.strip()
                break

        ch_global += 1
        label = f"제{book}권 {roman}장: {title[:60]}"
        save_chapter(out_dir, ch_global, text_block, label)
        chapters_meta.append({
            "num": ch_global,
            "title": label,
            "file": f"ch{ch_global:02d}.txt",
        })

    save_metadata(out_dir, {
        "slug": "dark-night-of-soul",
        "title": "어둔 밤",
        "title_original": "Dark Night of the Soul",
        "author": "십자가의 요한 (St. John of the Cross)",
        "author_original": "St. John of the Cross",
        "year": "1585",
        "source": "https://ccel.org/ccel/john_cross/dark_night",
        "license": "public_domain",
        "note": "E. Allison Peers 영역본. 제1권 감각의 밤(14장), 제2권 영혼의 밤(25장).",
        "chapters": chapters_meta,
    })


if __name__ == "__main__":
    split_humility()
    split_orthodoxy()
    split_prayer()
    split_morning_evening()
    split_religious_affections()
    split_dark_night()
    print("\n✅ 6권 분할 완료!")
