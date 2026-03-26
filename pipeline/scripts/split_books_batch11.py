#!/usr/bin/env python3
"""11차 도서 5권 분할 스크립트.

대상:
  1. The Christian's Secret of a Happy Life (한나 위톨 스미스) — CCEL
  2. Power Through Prayer (E.M. 바운즈) — CCEL
  3. On Loving God (클레르보의 베르나르) — CCEL
  4. A Short Method of Prayer (마담 귀용) — Gutenberg
  5. Story of a Soul (소화 데레사) — Gutenberg

소스:
  1: https://ccel.org/ccel/s/smith_hw/secret/cache/secret.txt
  2: https://ccel.org/ccel/b/bounds/power/cache/power.txt
  3: https://ccel.org/ccel/b/bernard/loving_god/cache/loving_god.txt
  4: https://www.gutenberg.org/cache/epub/24989/pg24989.txt
  5: https://www.gutenberg.org/cache/epub/16772/pg16772.txt

사용법:
  python pipeline/scripts/split_books_batch11.py [--download]
"""

import json
import re
import sys
import urllib.request
from pathlib import Path

BOOKS_DIR = Path("pipeline/sources/data/books")
CACHE_DIR = Path("/private/tmp/claude-501")
MAX_CHAPTER_WORDS = 8000


# ─────────────────────────────────────────────
# 공통 유틸리티 (batch8/9/10과 동일)
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


def _strip_ccel_header(text: str, first_marker_pos: int) -> str:
    """CCEL 텍스트에서 첫 번째 챕터 마커 이전의 머리말/메타데이터를 제거."""
    if first_marker_pos > 0:
        return text[first_marker_pos:]
    return text


# ─────────────────────────────────────────────
# 1. The Christian's Secret of a Happy Life
#    — Hannah Whitall Smith (CCEL)
# ─────────────────────────────────────────────

CHRISTIAN_SECRET_META = {
    "slug": "christian-secret",
    "title": "그리스도인의 행복한 삶의 비결",
    "title_original": "The Christian's Secret of a Happy Life",
    "author": "한나 위톨 스미스 (Hannah Whitall Smith)",
    "author_original": "Hannah Whitall Smith",
    "year": "1875",
    "source": "https://ccel.org/ccel/smith_hw/secret",
    "license": "public_domain",
    "note": "신앙생활에서 기쁨과 평안을 누리는 실천적 비결. 성결운동의 대표적 여성 저자.",
}


def split_christian_secret(raw: str) -> None:
    print("\n=== The Christian's Secret of a Happy Life (H.W. Smith) ===")
    text = clean_text(raw)
    out_dir = BOOKS_DIR / "christian-secret"

    # CCEL 텍스트: "Chapter" 마커 탐색 (여러 패턴 시도)
    # 패턴 1: "Chapter 1" / "Chapter I" / "Chapter One" 등
    ch_pat = re.compile(
        r"\n\s*Chapter\s+(\w+)\b[.\s]*\n",
        re.IGNORECASE,
    )
    matches = list(ch_pat.finditer(text))

    # 패턴 2: 로마 숫자만 (CHAPTER IV. 형태)
    if len(matches) < 3:
        ch_pat = re.compile(
            r"\n\s*CHAPTER\s+([IVXLC]+)\.?\s*\n",
            re.MULTILINE,
        )
        matches = list(ch_pat.finditer(text))

    # 패턴 3: 숫자.제목 형태 ("1. Is It Scriptural?")
    if len(matches) < 3:
        ch_pat = re.compile(
            r"\n\s*(\d+)\.\s+([A-Z][A-Za-z\s,\-'?!]+)\n",
        )
        matches = list(ch_pat.finditer(text))

    if not matches:
        # 최종 폴백: 단락 기반 분할
        print("  [주의] 챕터 마커를 찾을 수 없어 단락 기반 분할 수행")
        parts = split_text_at_paragraph(text)
        chapters_meta = []
        for pi, part in enumerate(parts):
            file_num = pi + 1
            title = f"Part {file_num}"
            save_chapter(out_dir, file_num, title, part)
            chapters_meta.append({
                "num": file_num, "title": title,
                "file": f"ch{file_num:02d}.txt",
            })
        meta = {**CHRISTIAN_SECRET_META, "chapters": chapters_meta}
        save_metadata(out_dir, meta)
        (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
        print(f"  → {len(chapters_meta)}개 챕터 저장 완료")
        return

    # 첫 번째 챕터 이전의 CCEL 헤더 제거 (메타정보)
    text = _strip_ccel_header(text, matches[0].start())
    # 다시 매칭 (텍스트가 변경되었으므로)
    matches = list(ch_pat.finditer(text))

    chapters_meta = []
    for idx, m in enumerate(matches):
        grp = m.group(1)
        # 챕터 번호 결정
        if grp.isdigit():
            ch_num = int(grp)
        else:
            roman_val = _roman(grp)
            ch_num = roman_val if roman_val > 0 else idx + 1

        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)

        if len(body.split()) < 50:
            continue

        # 제목 추출: 챕터 마커 바로 뒤의 첫 줄
        lines = body.split("\n", 1)
        ch_title_line = lines[0].strip() if lines else ""
        # 제목이 너무 길거나 소문자로 시작하면 제목 아님
        if ch_title_line and len(ch_title_line) < 120 and not ch_title_line[0].islower():
            title = f"Chapter {ch_num}: {ch_title_line}"
            body = lines[1].strip() if len(lines) > 1 else ""
        else:
            title = f"Chapter {ch_num}"

        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            file_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            save_chapter(out_dir, file_num, f"{title}{suffix}", part)
            chapters_meta.append({
                "num": file_num, "title": f"{title}{suffix}",
                "file": f"ch{file_num:02d}.txt",
            })

    meta = {**CHRISTIAN_SECRET_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 2. Power Through Prayer — E.M. Bounds (CCEL)
# ─────────────────────────────────────────────

POWER_PRAYER_META = {
    "slug": "power-through-prayer",
    "title": "기도의 능력",
    "title_original": "Power Through Prayer",
    "author": "E.M. 바운즈 (E.M. Bounds)",
    "author_original": "E.M. Bounds",
    "year": "1907",
    "source": "https://ccel.org/ccel/bounds/power",
    "license": "public_domain",
    "note": "기도하는 사역자의 필요성과 기도의 능력에 관한 짧은 에세이 모음.",
}


def split_power_prayer(raw: str) -> None:
    print("\n=== Power Through Prayer (E.M. Bounds) ===")
    text = clean_text(raw)
    out_dir = BOOKS_DIR / "power-through-prayer"

    # 패턴 1: "Chapter 1" / "Chapter I" 등
    ch_pat = re.compile(
        r"\n\s*Chapter\s+(\w+)\b[.\s]*\n",
        re.IGNORECASE,
    )
    matches = list(ch_pat.finditer(text))

    # 패턴 2: 로마 숫자 CHAPTER
    if len(matches) < 3:
        ch_pat = re.compile(
            r"\n\s*CHAPTER\s+([IVXLC]+)\.?\s*\n",
            re.MULTILINE,
        )
        matches = list(ch_pat.finditer(text))

    # 패턴 3: 숫자+제목 같은 줄 ("1 Men of Prayer Needed")
    if len(matches) < 3:
        ch_pat = re.compile(
            r"\n\s{0,5}(\d{1,2})\s+([A-Z][A-Za-z\s,\-']+)\n",
        )
        raw_matches = list(ch_pat.finditer(text))
        # 숫자가 1부터 연속이고 3개 이상인지 확인
        filtered = [m for m in raw_matches if int(m.group(1)) <= 25]
        if len(filtered) >= 3:
            matches = filtered

    # 패턴 3b: 숫자와 대문자 제목이 별도 줄 ("1\nMEN OF PRAYER NEEDED")
    if len(matches) < 3:
        ch_pat = re.compile(
            r"\n\s*(\d{1,2})\s*\n\s*([A-Z][A-Z\s,\-']+)\n",
        )
        matches = list(ch_pat.finditer(text))

    # 패턴 4: ALL-CAPS 줄 (설교 제목 패턴)
    if len(matches) < 3:
        ch_pat = re.compile(
            r"\n\s*([A-Z][A-Z\s,\-']{10,80})\s*\n",
        )
        raw_matches = list(ch_pat.finditer(text))
        # 중복 및 메타데이터 제외
        skip = {"POWER THROUGH PRAYER", "CONTENTS", "TABLE OF CONTENTS",
                "THE END", "FOOTNOTES", "INDEX", "PREFACE", "INTRODUCTION"}
        filtered = []
        for m in raw_matches:
            t = m.group(1).strip()
            if t in skip or len(t) < 10:
                continue
            filtered.append(m)
        if len(filtered) >= 3:
            matches = filtered

    if not matches:
        print("  [주의] 챕터 마커를 찾을 수 없어 단락 기반 분할 수행")
        parts = split_text_at_paragraph(text)
        chapters_meta = []
        for pi, part in enumerate(parts):
            file_num = pi + 1
            title = f"Part {file_num}"
            save_chapter(out_dir, file_num, title, part)
            chapters_meta.append({
                "num": file_num, "title": title,
                "file": f"ch{file_num:02d}.txt",
            })
        meta = {**POWER_PRAYER_META, "chapters": chapters_meta}
        save_metadata(out_dir, meta)
        (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
        print(f"  → {len(chapters_meta)}개 챕터 저장 완료")
        return

    # CCEL 헤더 제거
    text = _strip_ccel_header(text, matches[0].start())
    matches = list(ch_pat.finditer(text))

    chapters_meta = []
    for idx, m in enumerate(matches):
        grp = m.group(1)
        if grp.isdigit():
            ch_num = int(grp)
        else:
            roman_val = _roman(grp)
            ch_num = roman_val if roman_val > 0 else idx + 1

        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)

        if len(body.split()) < 50:
            continue

        # 제목 추출
        lines = body.split("\n", 1)
        ch_title_line = lines[0].strip() if lines else ""
        if ch_title_line and len(ch_title_line) < 120 and not ch_title_line[0].islower():
            title = f"Chapter {ch_num}: {ch_title_line}"
            body = lines[1].strip() if len(lines) > 1 else ""
        else:
            title = f"Chapter {ch_num}"

        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            file_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            save_chapter(out_dir, file_num, f"{title}{suffix}", part)
            chapters_meta.append({
                "num": file_num, "title": f"{title}{suffix}",
                "file": f"ch{file_num:02d}.txt",
            })

    meta = {**POWER_PRAYER_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 3. On Loving God — Bernard of Clairvaux (CCEL)
# ─────────────────────────────────────────────

ON_LOVING_GOD_META = {
    "slug": "on-loving-god",
    "title": "하나님 사랑에 관하여",
    "title_original": "On Loving God",
    "author": "클레르보의 베르나르 (Bernard of Clairvaux)",
    "author_original": "Bernard of Clairvaux",
    "year": "~1130",
    "source": "https://ccel.org/ccel/bernard/loving_god",
    "license": "public_domain",
    "note": "하나님을 사랑해야 하는 이유와 그 사랑의 네 단계를 논하는 시토회 수도원장의 고전.",
}


def split_on_loving_god(raw: str) -> None:
    print("\n=== On Loving God (Bernard of Clairvaux) ===")
    text = clean_text(raw)
    out_dir = BOOKS_DIR / "on-loving-god"

    # 패턴 1: "Chapter I." / "Chapter 1." 등
    ch_pat = re.compile(
        r"\n\s*Chapter\s+(\w+)\.?\s*\n",
        re.IGNORECASE,
    )
    matches = list(ch_pat.finditer(text))

    # 패턴 2: 로마 숫자 CHAPTER
    if len(matches) < 3:
        ch_pat = re.compile(
            r"\n\s*CHAPTER\s+([IVXLC]+)\.?\s*\n",
            re.MULTILINE,
        )
        matches = list(ch_pat.finditer(text))

    # 패턴 3: 로마 숫자만 줄에 단독 ("I.", "II.", ...)
    if len(matches) < 3:
        ch_pat = re.compile(
            r"\n\s*([IVXLC]+)\.\s*\n",
        )
        raw_matches = list(ch_pat.finditer(text))
        # 유효한 로마 숫자만 필터
        filtered = [m for m in raw_matches if _roman(m.group(1)) > 0]
        if len(filtered) >= 3:
            matches = filtered
            ch_pat = re.compile(r"\n\s*([IVXLC]+)\.\s*\n")

    # 패턴 4: 숫자.제목
    if len(matches) < 3:
        ch_pat = re.compile(
            r"\n\s*(\d{1,2})\.\s+([A-Z][A-Za-z\s,\-']+)\n",
        )
        matches = list(ch_pat.finditer(text))

    if not matches:
        print("  [주의] 챕터 마커를 찾을 수 없어 단락 기반 분할 수행")
        parts = split_text_at_paragraph(text)
        chapters_meta = []
        for pi, part in enumerate(parts):
            file_num = pi + 1
            title = f"Part {file_num}"
            save_chapter(out_dir, file_num, title, part)
            chapters_meta.append({
                "num": file_num, "title": title,
                "file": f"ch{file_num:02d}.txt",
            })
        meta = {**ON_LOVING_GOD_META, "chapters": chapters_meta}
        save_metadata(out_dir, meta)
        (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
        print(f"  → {len(chapters_meta)}개 챕터 저장 완료")
        return

    # CCEL 헤더 제거
    text = _strip_ccel_header(text, matches[0].start())
    matches = list(ch_pat.finditer(text))

    chapters_meta = []
    for idx, m in enumerate(matches):
        grp = m.group(1)
        if grp.isdigit():
            ch_num = int(grp)
        else:
            roman_val = _roman(grp)
            ch_num = roman_val if roman_val > 0 else idx + 1

        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)

        if len(body.split()) < 50:
            continue

        # 제목 추출
        lines = body.split("\n", 1)
        ch_title_line = lines[0].strip() if lines else ""
        if ch_title_line and len(ch_title_line) < 120 and not ch_title_line[0].islower():
            title = f"Chapter {ch_num}: {ch_title_line}"
            body = lines[1].strip() if len(lines) > 1 else ""
        else:
            title = f"Chapter {ch_num}"

        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            file_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            save_chapter(out_dir, file_num, f"{title}{suffix}", part)
            chapters_meta.append({
                "num": file_num, "title": f"{title}{suffix}",
                "file": f"ch{file_num:02d}.txt",
            })

    meta = {**ON_LOVING_GOD_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 4. A Short Method of Prayer — Madame Guyon
#    (Gutenberg)
# ─────────────────────────────────────────────

SHORT_METHOD_META = {
    "slug": "short-method-prayer",
    "title": "간결한 기도법",
    "title_original": "A Short Method of Prayer",
    "author": "마담 귀용 (Madame Guyon)",
    "author_original": "Jeanne Marie Bouvier de la Motte Guyon",
    "year": "1685",
    "source": "https://www.gutenberg.org/ebooks/24989",
    "license": "public_domain",
    "note": "내면기도와 묵상의 단순하고 실천적인 방법을 안내하는 프랑스 신비주의 저작.",
}


def split_short_method(raw: str) -> None:
    print("\n=== A Short Method of Prayer (Madame Guyon) ===")
    text = extract_gutenberg(raw)
    text = clean_text(text)
    out_dir = BOOKS_DIR / "short-method-prayer"

    # 패턴 1: "CHAPTER I." / "CHAPTER 1." 등
    ch_pat = re.compile(
        r"\n\s*CHAPTER\s+([IVXLC]+|\d+)\.?\s*\n",
        re.IGNORECASE,
    )
    matches = list(ch_pat.finditer(text))

    # 패턴 2: "Chapter I" (대소문자 혼합)
    if len(matches) < 3:
        ch_pat = re.compile(
            r"\n\s*Chapter\s+(\w+)\.?\s*\n",
            re.IGNORECASE,
        )
        matches = list(ch_pat.finditer(text))

    # 패턴 3: 로마 숫자 단독 줄
    if len(matches) < 3:
        ch_pat = re.compile(
            r"\n\s*([IVXLC]+)\.\s*\n",
        )
        raw_matches = list(ch_pat.finditer(text))
        filtered = [m for m in raw_matches if _roman(m.group(1)) > 0]
        if len(filtered) >= 3:
            matches = filtered
            ch_pat = re.compile(r"\n\s*([IVXLC]+)\.\s*\n")

    # 패턴 4: 숫자.제목
    if len(matches) < 3:
        ch_pat = re.compile(
            r"\n\s*(\d{1,2})\.\s+([A-Z][A-Za-z\s,\-']+)\n",
        )
        matches = list(ch_pat.finditer(text))

    if not matches:
        print("  [주의] 챕터 마커를 찾을 수 없어 단락 기반 분할 수행")
        parts = split_text_at_paragraph(text)
        chapters_meta = []
        for pi, part in enumerate(parts):
            file_num = pi + 1
            title = f"Part {file_num}"
            save_chapter(out_dir, file_num, title, part)
            chapters_meta.append({
                "num": file_num, "title": title,
                "file": f"ch{file_num:02d}.txt",
            })
        meta = {**SHORT_METHOD_META, "chapters": chapters_meta}
        save_metadata(out_dir, meta)
        (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
        print(f"  → {len(chapters_meta)}개 챕터 저장 완료")
        return

    chapters_meta = []
    for idx, m in enumerate(matches):
        grp = m.group(1)
        if grp.isdigit():
            ch_num = int(grp)
        else:
            roman_val = _roman(grp)
            ch_num = roman_val if roman_val > 0 else idx + 1

        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)

        if len(body.split()) < 50:
            continue

        # 제목 추출
        lines = body.split("\n", 1)
        ch_title_line = lines[0].strip() if lines else ""
        if ch_title_line and len(ch_title_line) < 120 and not ch_title_line[0].islower():
            title = f"Chapter {ch_num}: {ch_title_line}"
            body = lines[1].strip() if len(lines) > 1 else ""
        else:
            title = f"Chapter {ch_num}"

        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            file_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            save_chapter(out_dir, file_num, f"{title}{suffix}", part)
            chapters_meta.append({
                "num": file_num, "title": f"{title}{suffix}",
                "file": f"ch{file_num:02d}.txt",
            })

    meta = {**SHORT_METHOD_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 5. Story of a Soul — St. Thérèse of Lisieux
#    (Gutenberg)
# ─────────────────────────────────────────────

STORY_SOUL_META = {
    "slug": "story-of-a-soul",
    "title": "영혼의 이야기",
    "title_original": "The Story of a Soul (L'Histoire d'une Âme)",
    "author": "소화 데레사 (St. Thérèse of Lisieux)",
    "author_original": "St. Thérèse of Lisieux",
    "year": "1898",
    "source": "https://www.gutenberg.org/ebooks/16772",
    "license": "public_domain",
    "note": "'작은 길'의 영성을 제시한 소화 데레사의 자서전. 세 원고(A, B, C)로 구성.",
}


def split_story_soul(raw: str) -> None:
    print("\n=== Story of a Soul (St. Thérèse of Lisieux) ===")
    text = extract_gutenberg(raw)
    text = clean_text(text)
    out_dir = BOOKS_DIR / "story-of-a-soul"

    # 패턴 1: "CHAPTER I" / "CHAPTER V VOCATION..." (제목이 같은 줄에 올 수 있음)
    ch_pat = re.compile(
        r"\nCHAPTER\s+([IVXLC]+|\d+)\b\s*(.*?)\s*\n",
    )
    matches = list(ch_pat.finditer(text))

    # 패턴 2: "Chapter I" (대소문자 혼합)
    if len(matches) < 3:
        ch_pat = re.compile(
            r"\n\s*Chapter\s+(\w+)\b[^\n]*\n",
            re.IGNORECASE,
        )
        matches = list(ch_pat.finditer(text))

    # 패턴 3: 로마 숫자 단독 줄
    if len(matches) < 3:
        ch_pat = re.compile(
            r"\n\s*([IVXLC]+)\.\s*\n",
        )
        raw_matches = list(ch_pat.finditer(text))
        filtered = [m for m in raw_matches if _roman(m.group(1)) > 0]
        if len(filtered) >= 3:
            matches = filtered
            ch_pat = re.compile(r"\n\s*([IVXLC]+)\.\s*\n")

    # 패턴 4: 숫자.제목
    if len(matches) < 3:
        ch_pat = re.compile(
            r"\n\s*(\d{1,2})\.\s+([A-Z][A-Za-z\s,\-']+)\n",
        )
        matches = list(ch_pat.finditer(text))

    if not matches:
        print("  [주의] 챕터 마커를 찾을 수 없어 단락 기반 분할 수행")
        parts = split_text_at_paragraph(text)
        chapters_meta = []
        for pi, part in enumerate(parts):
            file_num = pi + 1
            title = f"Part {file_num}"
            save_chapter(out_dir, file_num, title, part)
            chapters_meta.append({
                "num": file_num, "title": title,
                "file": f"ch{file_num:02d}.txt",
            })
        meta = {**STORY_SOUL_META, "chapters": chapters_meta}
        save_metadata(out_dir, meta)
        (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
        print(f"  → {len(chapters_meta)}개 챕터 저장 완료")
        return

    chapters_meta = []
    for idx, m in enumerate(matches):
        grp = m.group(1)
        if grp.isdigit():
            ch_num = int(grp)
        else:
            roman_val = _roman(grp)
            ch_num = roman_val if roman_val > 0 else idx + 1

        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)

        if len(body.split()) < 50:
            continue

        # 제목 추출: 먼저 regex match에서 inline 제목 확인
        inline_title = m.group(2).strip() if m.lastindex >= 2 and m.group(2).strip() else ""
        if inline_title:
            title = f"Chapter {ch_num}: {inline_title}"
        else:
            lines = body.split("\n", 1)
            ch_title_line = lines[0].strip() if lines else ""
            if ch_title_line and len(ch_title_line) < 120 and not ch_title_line[0].islower():
                title = f"Chapter {ch_num}: {ch_title_line}"
                body = lines[1].strip() if len(lines) > 1 else ""
            else:
                title = f"Chapter {ch_num}"

        # Story of a Soul 챕터가 매우 길 수 있음 → 8K 단어 단위로 분할
        # 단일 개행만 있는 경우 이중 개행으로 변환
        if "\n\n" not in body and "\n" in body:
            body = re.sub(r"\n(?=[A-Z])", "\n\n", body)
        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            file_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            save_chapter(out_dir, file_num, f"{title}{suffix}", part)
            chapters_meta.append({
                "num": file_num, "title": f"{title}{suffix}",
                "file": f"ch{file_num:02d}.txt",
            })

    meta = {**STORY_SOUL_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# main
# ─────────────────────────────────────────────

URLS = {
    "christian_secret": "https://ccel.org/ccel/s/smith_hw/secret/cache/secret.txt",
    "power_prayer": "https://ccel.org/ccel/b/bounds/power/cache/power.txt",
    "on_loving_god": "https://ccel.org/ccel/b/bernard/loving_god/cache/loving_god.txt",
    "short_method": "https://www.gutenberg.org/cache/epub/24989/pg24989.txt",
    "story_soul": "https://www.gutenberg.org/cache/epub/16772/pg16772.txt",
}


def main():
    do_download = "--download" in sys.argv or len(sys.argv) == 1
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    print("=== 11차: 5권 도서 분할 시작 ===\n")

    # ── 1. The Christian's Secret of a Happy Life ──
    cache = CACHE_DIR / "christian_secret.txt"
    if do_download:
        raw = download(URLS["christian_secret"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_christian_secret(raw)

    # ── 2. Power Through Prayer ──
    cache = CACHE_DIR / "power_prayer.txt"
    if do_download:
        raw = download(URLS["power_prayer"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_power_prayer(raw)

    # ── 3. On Loving God ──
    cache = CACHE_DIR / "on_loving_god.txt"
    if do_download:
        raw = download(URLS["on_loving_god"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_on_loving_god(raw)

    # ── 4. A Short Method of Prayer ──
    cache = CACHE_DIR / "short_method_prayer.txt"
    if do_download:
        raw = download(URLS["short_method"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_short_method(raw)

    # ── 5. Story of a Soul ──
    cache = CACHE_DIR / "story_soul.txt"
    if do_download:
        raw = download(URLS["story_soul"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_story_soul(raw)

    print("\n✅ 11차: 5권 분할 완료!")


if __name__ == "__main__":
    main()
