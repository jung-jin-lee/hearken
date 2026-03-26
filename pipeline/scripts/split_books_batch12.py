#!/usr/bin/env python3
"""12차 도서 5권 분할 스크립트.

대상:
  6. On Keeping the Heart (존 플라벨) — CCEL
  7. Revelations of Divine Love (노리치의 줄리안) — CCEL
  8. George Müller of Bristol (조지 뮬러 자서전) — Gutenberg
  9. Selected Sermons of John Wesley (웨슬리 설교선집) — CCEL
  10. The Cloud of Unknowing (무지의 구름) — Wikisource

소스:
  6: https://ccel.org/ccel/f/flavel/keeping/cache/keeping.txt
  7: https://ccel.org/ccel/j/julian/revelations/cache/revelations.txt
  8: https://www.gutenberg.org/cache/epub/26522/pg26522.txt
  9: https://ccel.org/ccel/w/wesley/sermons/cache/sermons.txt
  10: https://en.wikisource.org/wiki/The_Cloud_of_Unknowing (75 chapter pages)

사용법:
  python pipeline/scripts/split_books_batch12.py [--download]
"""

import json
import re
import sys
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

BOOKS_DIR = Path("pipeline/sources/data/books")
CACHE_DIR = Path("/private/tmp/claude-501")
MAX_CHAPTER_WORDS = 8000


# ─────────────────────────────────────────────
# 공통 유틸리티 (batch8/10과 동일)
# ─────────────────────────────────────────────

def download(url: str, dest: Path) -> str:
    if dest.exists() and dest.stat().st_size > 500:
        print(f"  [캐시] {dest.name}")
        return dest.read_text(encoding="utf-8")
    print(f"  [다운로드] {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = data.decode("latin-1")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    return text


def clean_text(text: str) -> str:
    text = re.sub(r"_{5,}", "", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip()


def extract_gutenberg(text: str) -> str:
    for start_m in ["*** START OF THE PROJECT GUTENBERG",
                     "*** START OF THIS PROJECT GUTENBERG"]:
        idx = text.find(start_m)
        if idx != -1:
            text = text[idx:].split("\n", 1)[1] if "\n" in text[idx:] else text[idx:]
            break
    for end_m in ["*** END OF THE PROJECT GUTENBERG",
                   "*** END OF THIS PROJECT GUTENBERG",
                   "End of the Project Gutenberg",
                   "End of Project Gutenberg"]:
        idx = text.find(end_m)
        if idx != -1:
            text = text[:idx]
            break
    return text.strip()


def save_chapter(out_dir: Path, num: int, title: str, body: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    fname = f"ch{num:02d}.txt"
    (out_dir / fname).write_text(f"{title}\n\n{body.strip()}\n", encoding="utf-8")
    words = len(body.split())
    print(f"  {fname}: {title[:60]} ({words} words)")


def save_metadata(out_dir: Path, meta: dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "metadata.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def split_text_at_paragraph(text: str, max_words: int = MAX_CHAPTER_WORDS) -> list[str]:
    if len(text.split()) <= max_words:
        return [text]
    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    chunks, current, cw = [], [], 0
    for para in paragraphs:
        pw = len(para.split())
        if cw + pw > max_words and current:
            chunks.append("\n\n".join(current))
            current, cw = [], 0
        current.append(para)
        cw += pw
    if current:
        chunks.append("\n\n".join(current))
    return chunks if chunks else [text]


_ROMAN_MAP = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7,
    "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12, "XIII": 13,
    "XIV": 14, "XV": 15, "XVI": 16, "XVII": 17, "XVIII": 18,
    "XIX": 19, "XX": 20, "XXI": 21, "XXII": 22, "XXIII": 23,
    "XXIV": 24, "XXV": 25, "XXVI": 26, "XXVII": 27, "XXVIII": 28,
    "XXIX": 29, "XXX": 30, "XXXI": 31, "XXXII": 32,
    "XXXIII": 33, "XXXIV": 34, "XXXV": 35,
}


def _roman(s: str) -> int:
    return _ROMAN_MAP.get(s.upper().strip(), 0)


def _parse_roman(s: str) -> int:
    """Parse a roman numeral string to integer, supporting values beyond _ROMAN_MAP."""
    val = _ROMAN_MAP.get(s.upper().strip(), 0)
    if val:
        return val
    # Fallback: algorithmic parsing for values beyond the map
    roman_vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    result = 0
    upper = s.upper().strip()
    for i, ch in enumerate(upper):
        if ch not in roman_vals:
            return 0
        v = roman_vals[ch]
        if i + 1 < len(upper) and roman_vals.get(upper[i + 1], 0) > v:
            result -= v
        else:
            result += v
    return result


# ─────────────────────────────────────────────
# HTML 유틸리티 (Wikisource 파싱용)
# ─────────────────────────────────────────────

class _HTMLText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts: list[str] = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "head"):
            self._skip = True
        if tag in ("p", "br", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li"):
            self.parts.append("\n\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "head"):
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)


def html_to_text(html: str) -> str:
    p = _HTMLText()
    p.feed(html)
    text = "".join(p.parts)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


# ─────────────────────────────────────────────
# CCEL 헤더/메타데이터 제거 유틸리티
# ─────────────────────────────────────────────

def strip_ccel_header(text: str) -> str:
    """Remove CCEL metadata/header from the beginning of a text file."""
    # CCEL files often start with metadata lines before actual content.
    # Look for common content-start markers.
    markers = [
        r"\n\s*CHAPTER\s",
        r"\n\s*Chapter\s",
        r"\n\s*INTRODUCTION",
        r"\n\s*Introduction",
        r"\n\s*PREFACE",
        r"\n\s*Preface",
        r"\n\s*PART\s",
        r"\n\s*TO THE READER",
        r"\n\s*THE EPISTLE",
        r"\n\s*SERMON\s",
        r"\n\s*Sermon\s",
        r"\n\s*CASE\s",
        r"\n\s*Case\s",
    ]
    for pat in markers:
        m = re.search(pat, text)
        if m:
            # Include some context before the match (look for previous blank line)
            pos = m.start()
            prev_blank = text.rfind("\n\n", 0, pos)
            if prev_blank > 0:
                return text[prev_blank:].strip()
            return text[pos:].strip()
    # If no marker found, try to skip first few metadata-like lines
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if i > 50 and line.strip():
            return "\n".join(lines[i:])
    return text


# ─────────────────────────────────────────────
# 6. On Keeping the Heart — John Flavel (CCEL)
# ─────────────────────────────────────────────

KEEPING_HEART_META = {
    "slug": "keeping-the-heart",
    "title": "마음 지키기",
    "title_original": "On Keeping the Heart",
    "author": "존 플라벨 (John Flavel)",
    "author_original": "John Flavel",
    "year": "1668",
    "source": "https://ccel.org/ccel/flavel/keeping",
    "license": "public_domain",
    "note": "잠언 4:23에 기초한 마음 지킴에 관한 청교도 고전. 12가지 상황에서의 마음 지킴의 실천.",
}


def split_keeping_heart(raw: str) -> None:
    print("\n=== On Keeping the Heart (John Flavel) ===")
    text = strip_ccel_header(raw)
    text = clean_text(text)
    out_dir = BOOKS_DIR / "keeping-the-heart"

    chapters_meta: list[dict] = []

    # Try section-based structure: "Case I", "Case II", "CASE 1", "Direction" etc.
    # Pattern 1: "Case I." / "CASE I." / "Case 1." etc.
    case_pat = re.compile(
        r"\n\s*(Case|CASE)\s+([IVXLC]+|\d+)\.?\s*[:\.\—\-]?\s*(.*?)\s*\n",
        re.IGNORECASE,
    )
    case_matches = list(case_pat.finditer(text))

    if len(case_matches) >= 5:
        # Section-based splitting on Case markers
        print(f"  Case 마커 {len(case_matches)}개 발견")
        for idx, m in enumerate(case_matches):
            grp = m.group(2)
            case_num = int(grp) if grp.isdigit() else _parse_roman(grp)
            case_title = m.group(3).strip() if m.group(3).strip() else ""

            start = m.start()
            end = case_matches[idx + 1].start() if idx + 1 < len(case_matches) else len(text)
            body = text[start:end].strip()
            body = re.sub(r"\n{3,}", "\n\n", body)

            title_str = f"제{case_num}장: 마음 지킴의 상황 {case_num}"
            if case_title:
                title_str = f"제{case_num}장: {case_title}"

            parts = split_text_at_paragraph(body)
            for pi, part in enumerate(parts):
                file_num = len(chapters_meta) + 1
                suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
                title = f"{title_str}{suffix}"
                save_chapter(out_dir, file_num, title, part)
                chapters_meta.append({
                    "num": file_num, "title": title,
                    "file": f"ch{file_num:02d}.txt",
                    "case": case_num,
                })
    else:
        # Try chapter markers
        ch_pat = re.compile(
            r"\n\s*(CHAPTER|Chapter)\s+([IVXLC]+|\d+)\.?\s*\n",
            re.IGNORECASE,
        )
        ch_matches = list(ch_pat.finditer(text))

        if len(ch_matches) >= 3:
            print(f"  Chapter 마커 {len(ch_matches)}개 발견")
            for idx, m in enumerate(ch_matches):
                grp = m.group(2)
                ch_num = int(grp) if grp.isdigit() else _parse_roman(grp)
                start = m.start()
                end = ch_matches[idx + 1].start() if idx + 1 < len(ch_matches) else len(text)
                body = text[start:end].strip()
                body = re.sub(r"\n{3,}", "\n\n", body)

                title_str = f"제{ch_num}장"

                parts = split_text_at_paragraph(body)
                for pi, part in enumerate(parts):
                    file_num = len(chapters_meta) + 1
                    suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
                    title = f"{title_str}{suffix}"
                    save_chapter(out_dir, file_num, title, part)
                    chapters_meta.append({
                        "num": file_num, "title": title,
                        "file": f"ch{file_num:02d}.txt",
                        "chapter": ch_num,
                    })
        else:
            # Fallback: paragraph-based splitting at 8K word chunks
            print("  구조 마커 없음 → 단락 기반 분할")
            # Try to split on section-like headers (ALL CAPS lines, "Direction" lines)
            sect_pat = re.compile(
                r"\n\s*(DIRECTION|Direction|SECT(?:ION)?\.?\s*[IVXLC\d]+|"
                r"[A-Z][A-Z\s]{15,})\s*\n"
            )
            sect_matches = list(sect_pat.finditer(text))

            if len(sect_matches) >= 5:
                print(f"  섹션 마커 {len(sect_matches)}개 발견")
                for idx, m in enumerate(sect_matches):
                    start = m.start()
                    end = (sect_matches[idx + 1].start()
                           if idx + 1 < len(sect_matches) else len(text))
                    body = text[start:end].strip()
                    body = re.sub(r"\n{3,}", "\n\n", body)

                    sect_title = m.group(1).strip()

                    parts = split_text_at_paragraph(body)
                    for pi, part in enumerate(parts):
                        file_num = len(chapters_meta) + 1
                        suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
                        title = f"섹션 {file_num}: {sect_title[:50]}{suffix}"
                        save_chapter(out_dir, file_num, title, part)
                        chapters_meta.append({
                            "num": file_num, "title": title,
                            "file": f"ch{file_num:02d}.txt",
                        })
            else:
                # Pure paragraph-based splitting
                print("  단락 경계 분할")
                parts = split_text_at_paragraph(text)
                for pi, part in enumerate(parts):
                    file_num = pi + 1
                    title = f"제{file_num}부"
                    save_chapter(out_dir, file_num, title, part)
                    chapters_meta.append({
                        "num": file_num, "title": title,
                        "file": f"ch{file_num:02d}.txt",
                    })

    meta = {**KEEPING_HEART_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 7. Revelations of Divine Love — Julian of Norwich (CCEL)
# ─────────────────────────────────────────────

REVELATIONS_META = {
    "slug": "revelations-divine-love",
    "title": "신적 사랑의 계시",
    "title_original": "Revelations of Divine Love",
    "author": "노리치의 줄리안 (Julian of Norwich)",
    "author_original": "Julian of Norwich",
    "year": "~1395",
    "source": "https://ccel.org/ccel/julian/revelations",
    "license": "public_domain",
    "translator": "Grace Warrack",
    "note": "영어로 기록된 최초의 여성 저술. 16가지 신적 현시(Showing)에 대한 깊은 묵상.",
}


def split_revelations(raw: str) -> None:
    print("\n=== Revelations of Divine Love (Julian of Norwich) ===")
    text = strip_ccel_header(raw)
    text = clean_text(text)
    out_dir = BOOKS_DIR / "revelations-divine-love"

    # Find CHAPTER markers: "CHAPTER I", "CHAPTER 1", etc.
    ch_pat = re.compile(
        r"\n\s*(CHAPTER|Chapter)\s+([IVXLC]+|\d+)\.?\s*\n",
        re.IGNORECASE,
    )
    ch_matches = list(ch_pat.finditer(text))
    print(f"  Chapter 마커 {len(ch_matches)}개 발견")

    if not ch_matches:
        # Try alternative markers
        ch_pat = re.compile(r"\n\s*(\d+)\.\s+", re.MULTILINE)
        ch_matches = list(ch_pat.finditer(text))
        print(f"  번호 마커 {len(ch_matches)}개 발견 (대안)")

    # Extract individual chapters with their numbers and texts
    raw_chapters: list[tuple[int, str]] = []
    for idx, m in enumerate(ch_matches):
        grp = m.group(2) if m.lastindex and m.lastindex >= 2 else m.group(1)
        ch_num = int(grp) if grp.isdigit() else _parse_roman(grp)
        start = m.end()
        end = ch_matches[idx + 1].start() if idx + 1 < len(ch_matches) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)
        raw_chapters.append((ch_num, body))

    # Group 3-4 adjacent chapters per file to avoid too many tiny files → ~25 files
    GROUP_SIZE = 4 if len(raw_chapters) > 80 else 3
    chapters_meta: list[dict] = []
    file_num = 0

    for i in range(0, len(raw_chapters), GROUP_SIZE):
        group = raw_chapters[i : i + GROUP_SIZE]
        if not group:
            break
        file_num += 1

        first_ch = group[0][0]
        last_ch = group[-1][0]

        # Combine the grouped chapters
        combined_parts = []
        for ch_num, ch_body in group:
            combined_parts.append(f"--- Chapter {ch_num} ---\n\n{ch_body}")
        combined = "\n\n".join(combined_parts)

        # Build title with range
        if first_ch == last_ch:
            title = f"제{first_ch}장 (Chapter {first_ch})"
        else:
            title = f"제{first_ch}-{last_ch}장 (Chapters {first_ch}-{last_ch})"

        # Split if combined exceeds max words
        parts = split_text_at_paragraph(combined)
        for pi, part in enumerate(parts):
            out_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            t = f"{title}{suffix}"
            save_chapter(out_dir, out_num, t, part)
            chapters_meta.append({
                "num": out_num, "title": t,
                "file": f"ch{out_num:02d}.txt",
                "chapters": list(range(first_ch, last_ch + 1)),
            })

    if not chapters_meta:
        # Fallback: paragraph-based splitting
        print("  Chapter 마커 파싱 실패 → 단락 기반 분할")
        parts = split_text_at_paragraph(text)
        for pi, part in enumerate(parts):
            file_num = pi + 1
            title = f"제{file_num}부"
            save_chapter(out_dir, file_num, title, part)
            chapters_meta.append({
                "num": file_num, "title": title,
                "file": f"ch{file_num:02d}.txt",
            })

    meta = {**REVELATIONS_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 8. George Müller of Bristol — Arthur T. Pierson (Gutenberg)
# ─────────────────────────────────────────────

MUELLER_META = {
    "slug": "mueller-autobiography",
    "title": "조지 뮬러 자서전",
    "title_original": "George Müller of Bristol, and His Witness to a Prayer-Hearing God",
    "author": "아서 T. 피어슨 (Arthur T. Pierson)",
    "author_original": "Arthur T. Pierson",
    "year": "1905",
    "source": "https://www.gutenberg.org/ebooks/26522",
    "license": "public_domain",
    "note": "기도의 사람 조지 뮬러의 삶과 사역. 신앙에 의한 고아원 운영과 기도 응답의 증거.",
}


def split_mueller(raw: str) -> None:
    print("\n=== George Müller of Bristol (Arthur T. Pierson) ===")
    text = extract_gutenberg(raw)
    text = clean_text(text)
    out_dir = BOOKS_DIR / "mueller-autobiography"

    # Look for CHAPTER markers (roman or arabic numerals)
    ch_pat = re.compile(
        r"\n\s*(CHAPTER|Chapter)\s+([IVXLC]+|\d+)\.?\s*\n",
        re.IGNORECASE,
    )
    ch_matches = list(ch_pat.finditer(text))
    print(f"  Chapter 마커 {len(ch_matches)}개 발견")

    if not ch_matches:
        # Try alternative: lines like "I.", "II." at start of line
        ch_pat = re.compile(r"\n\s*([IVXLC]+)\.\s*\n")
        ch_matches = list(ch_pat.finditer(text))
        print(f"  로마 숫자 마커 {len(ch_matches)}개 발견 (대안)")

    chapters_meta: list[dict] = []

    for idx, m in enumerate(ch_matches):
        grp = m.group(2) if m.lastindex and m.lastindex >= 2 else m.group(1)
        ch_num = int(grp) if grp.isdigit() else _parse_roman(grp)

        start = m.end()
        end = ch_matches[idx + 1].start() if idx + 1 < len(ch_matches) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)

        # Extract title: first non-empty line after CHAPTER marker
        first_lines = body.split("\n", 3)
        ch_title = ""
        for fl in first_lines[:3]:
            stripped = fl.strip()
            if stripped and len(stripped) > 3:
                ch_title = stripped.rstrip(".")
                break

        title_str = f"제{ch_num}장"
        if ch_title and len(ch_title) < 100:
            title_str = f"제{ch_num}장: {ch_title}"

        # Split long chapters at paragraph boundaries
        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            file_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            title = f"{title_str}{suffix}"
            save_chapter(out_dir, file_num, title, part)
            chapters_meta.append({
                "num": file_num, "title": title,
                "file": f"ch{file_num:02d}.txt",
                "chapter": ch_num,
            })

    if not chapters_meta:
        # Fallback: paragraph-based splitting
        print("  Chapter 마커 파싱 실패 → 단락 기반 분할")
        parts = split_text_at_paragraph(text)
        for pi, part in enumerate(parts):
            file_num = pi + 1
            title = f"제{file_num}부"
            save_chapter(out_dir, file_num, title, part)
            chapters_meta.append({
                "num": file_num, "title": title,
                "file": f"ch{file_num:02d}.txt",
            })

    meta = {**MUELLER_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 9. Selected Sermons of John Wesley (CCEL)
# ─────────────────────────────────────────────

WESLEY_META = {
    "slug": "wesley-sermons",
    "title": "존 웨슬리 설교선집",
    "title_original": "Selected Sermons of John Wesley",
    "author": "존 웨슬리 (John Wesley)",
    "author_original": "John Wesley",
    "year": "~1750",
    "source": "https://ccel.org/ccel/wesley/sermons",
    "license": "public_domain",
    "note": "감리교 창시자 존 웨슬리의 대표 설교 선집. 구원, 성화, 사랑의 완전 등 핵심 주제.",
}

WESLEY_TITLES = {
    1: "믿음으로 말미암는 구원 (Salvation by Faith)",
    5: "믿음으로 말미암는 칭의 (Justification by Faith)",
    7: "천국에 이르는 길 (The Way to the Kingdom)",
    9: "속박과 양자됨의 영 (The Spirit of Bondage and Adoption)",
    12: "성령의 증거 I (The Witness of the Spirit I)",
    17: "마음의 할례 (The Circumcision of the Heart)",
    18: "새 생명의 표지 (The Marks of the New Birth)",
    28: "산상수훈 강해 I (Upon Our Lord's Sermon on the Mount I)",
    33: "산상수훈 강해 VI (Upon Our Lord's Sermon on the Mount VI)",
    38: "원죄 (Original Sin)",
    40: "기독교적 완전 (Christian Perfection)",
    43: "성경적 구원의 길 (The Scripture Way of Salvation)",
    44: "원죄에 관하여 (On Original Sin)",
    45: "새로 남 (The New Birth)",
    54: "영원에 관하여 (On Eternity)",
    64: "새 창조 (The New Creation)",
    85: "구원을 이루라 (Working Out Our Own Salvation)",
    128: "자유 은총 (Free Grace)",
    141: "사랑에 관하여 (On Love)",
}
SELECTED_SERMONS = list(WESLEY_TITLES.keys())


def split_wesley_sermons(raw: str) -> None:
    print("\n=== Selected Sermons of John Wesley ===")
    text = strip_ccel_header(raw)
    text = clean_text(text)
    out_dir = BOOKS_DIR / "wesley-sermons"

    selected_set = set(SELECTED_SERMONS)

    # Find sermon boundaries: "Sermon 1", "SERMON I", "Sermon I", "SERMON 141" etc.
    # Try multiple patterns for robustness
    sermon_pat = re.compile(
        r"\n\s*(?:SERMON|Sermon)\s+(\d+|[IVXLC]+)\.?\s*\n",
        re.IGNORECASE,
    )
    sermon_matches = list(sermon_pat.finditer(text))
    print(f"  Sermon 마커 {len(sermon_matches)}개 발견")

    if len(sermon_matches) < 20:
        # Try alternative pattern with colon or dash
        sermon_pat2 = re.compile(
            r"\n\s*(?:SERMON|Sermon)\s+(\d+|[IVXLC]+)\s*[:\.\-—]",
            re.IGNORECASE,
        )
        alt_matches = list(sermon_pat2.finditer(text))
        if len(alt_matches) > len(sermon_matches):
            sermon_matches = alt_matches
            print(f"  대안 마커 {len(sermon_matches)}개 발견")

    if len(sermon_matches) < 20:
        # Try broader pattern
        sermon_pat3 = re.compile(
            r"\n\s*(?:SERMON|Sermon)\s+(\d+|[IVXLC]+)",
            re.IGNORECASE,
        )
        alt_matches = list(sermon_pat3.finditer(text))
        if len(alt_matches) > len(sermon_matches):
            sermon_matches = alt_matches
            print(f"  광범위 마커 {len(sermon_matches)}개 발견")

    # Build a map of sermon number → (start, end) in text
    sermon_ranges: dict[int, tuple[int, int]] = {}
    for idx, m in enumerate(sermon_matches):
        grp = m.group(1)
        s_num = int(grp) if grp.isdigit() else _parse_roman(grp)
        if s_num <= 0:
            continue
        start = m.start()
        end = sermon_matches[idx + 1].start() if idx + 1 < len(sermon_matches) else len(text)
        # Only keep first occurrence if duplicate
        if s_num not in sermon_ranges:
            sermon_ranges[s_num] = (start, end)

    print(f"  설교 범위 {len(sermon_ranges)}개 매핑 완료")

    chapters_meta: list[dict] = []

    for s_num in sorted(SELECTED_SERMONS):
        if s_num not in sermon_ranges:
            print(f"  ⚠ Sermon {s_num} 마커 없음 — 건너뜀")
            continue

        s_start, s_end = sermon_ranges[s_num]
        body = text[s_start:s_end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)

        kr_title = WESLEY_TITLES[s_num]
        title_base = f"설교 {s_num}: {kr_title}"

        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            file_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            title = f"{title_base}{suffix}"
            save_chapter(out_dir, file_num, title, part)
            chapters_meta.append({
                "num": file_num, "title": title,
                "file": f"ch{file_num:02d}.txt",
                "sermon": s_num,
            })

    meta = {**WESLEY_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료 "
          f"(선별 {len(SELECTED_SERMONS)}편 중 "
          f"{len({c['sermon'] for c in chapters_meta})}편 수록)")


# ─────────────────────────────────────────────
# 10. The Cloud of Unknowing — Anonymous (Wikisource)
# ─────────────────────────────────────────────

CLOUD_META = {
    "slug": "cloud-of-unknowing",
    "title": "무지의 구름",
    "title_original": "The Cloud of Unknowing",
    "author": "미상 (Anonymous, 14th century English mystic)",
    "author_original": "Anonymous",
    "year": "~1370",
    "source": "https://en.wikisource.org/wiki/The_Cloud_of_Unknowing",
    "license": "public_domain",
    "note": "14세기 영국 신비주의 걸작. 관상기도와 하나님과의 합일을 향한 75장의 영적 지침서.",
}

CLOUD_BASE_URL = "https://en.wikisource.org/wiki/The_Cloud_of_Unknowing"


def _download_cloud_pages(do_download: bool) -> list[tuple[str, str]]:
    """Download prologue + 75 chapter HTML pages from Wikisource.

    Returns list of (label, text) tuples.
    """
    pages: list[tuple[str, str]] = []

    # Prologue
    prologue_url = f"{CLOUD_BASE_URL}/Prologue"
    prologue_cache = CACHE_DIR / "cloud_prologue.html"
    if do_download:
        html = download(prologue_url, prologue_cache)
    else:
        html = prologue_cache.read_text(encoding="utf-8") if prologue_cache.exists() else ""
    if html:
        pages.append(("Prologue", html_to_text(html)))

    # Chapters 1-75
    for n in range(1, 76):
        ch_url = f"{CLOUD_BASE_URL}/Chapter_{n}"
        ch_cache = CACHE_DIR / f"cloud_ch{n:02d}.html"
        if do_download:
            html = download(ch_url, ch_cache)
            time.sleep(0.5)  # polite delay for Wikisource
        else:
            html = ch_cache.read_text(encoding="utf-8") if ch_cache.exists() else ""
        if html:
            pages.append((f"Chapter {n}", html_to_text(html)))

    return pages


def split_cloud_of_unknowing(pages: list[tuple[str, str]]) -> None:
    print("\n=== The Cloud of Unknowing (Anonymous) ===")
    out_dir = BOOKS_DIR / "cloud-of-unknowing"
    print(f"  다운로드된 페이지: {len(pages)}개")

    if not pages:
        print("  ⚠ 페이지 없음 — 건너뜀")
        return

    # Save combined raw text
    raw_combined = "\n\n".join(
        f"=== {label} ===\n\n{body}" for label, body in pages
    )

    # Group pages: Prologue first, then 3-4 chapters per file
    chapters_meta: list[dict] = []
    GROUP_SIZE = 4

    # Handle Prologue separately if present
    start_idx = 0
    if pages[0][0] == "Prologue":
        prologue_body = pages[0][1]
        file_num = 1
        title = "서문 (Prologue)"
        save_chapter(out_dir, file_num, title, prologue_body)
        chapters_meta.append({
            "num": file_num, "title": title,
            "file": "ch01.txt",
            "section": "prologue",
        })
        start_idx = 1

    # Group remaining chapters
    chapter_pages = pages[start_idx:]
    for i in range(0, len(chapter_pages), GROUP_SIZE):
        group = chapter_pages[i : i + GROUP_SIZE]
        if not group:
            break

        # Extract chapter numbers from labels
        ch_nums = []
        combined_parts = []
        for label, body in group:
            m = re.search(r"(\d+)", label)
            if m:
                ch_nums.append(int(m.group(1)))
            combined_parts.append(f"--- {label} ---\n\n{body}")
        combined = "\n\n".join(combined_parts)

        file_num = len(chapters_meta) + 1

        if ch_nums:
            first, last = ch_nums[0], ch_nums[-1]
            if first == last:
                title = f"제{first}장 (Chapter {first})"
            else:
                title = f"제{first}-{last}장 (Chapters {first}-{last})"
        else:
            title = f"제{file_num}부"

        # Split if combined exceeds max words
        parts = split_text_at_paragraph(combined)
        for pi, part in enumerate(parts):
            out_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            t = f"{title}{suffix}"
            save_chapter(out_dir, out_num, t, part)
            chapters_meta.append({
                "num": out_num, "title": t,
                "file": f"ch{out_num:02d}.txt",
                "chapters": ch_nums if ch_nums else [],
            })

    meta = {**CLOUD_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw_combined, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# main
# ─────────────────────────────────────────────

URLS = {
    "keeping_heart": "https://ccel.org/ccel/f/flavel/keeping/cache/keeping.txt",
    "revelations": "https://ccel.org/ccel/j/julian/revelations/cache/revelations.txt",
    "mueller": "https://www.gutenberg.org/cache/epub/26522/pg26522.txt",
    "wesley": "https://ccel.org/ccel/w/wesley/sermons/cache/sermons.txt",
    # cloud-of-unknowing uses per-chapter Wikisource URLs
}


def main():
    do_download = "--download" in sys.argv or len(sys.argv) == 1
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    print("=== 12차: 5권 도서 분할 시작 ===\n")

    # ── 6. On Keeping the Heart ──
    cache = CACHE_DIR / "keeping_heart.txt"
    if do_download:
        raw = download(URLS["keeping_heart"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_keeping_heart(raw)

    # ── 7. Revelations of Divine Love ──
    cache = CACHE_DIR / "revelations.txt"
    if do_download:
        raw = download(URLS["revelations"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_revelations(raw)

    # ── 8. George Müller of Bristol ──
    cache = CACHE_DIR / "mueller.txt"
    if do_download:
        raw = download(URLS["mueller"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_mueller(raw)

    # ── 9. Wesley Sermons (선집) ──
    cache = CACHE_DIR / "wesley_sermons.txt"
    if do_download:
        raw = download(URLS["wesley"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_wesley_sermons(raw)

    # ── 10. Cloud of Unknowing ──
    pages = _download_cloud_pages(do_download)
    split_cloud_of_unknowing(pages)

    print("\n✅ 12차: 5권 분할 완료!")


if __name__ == "__main__":
    main()
