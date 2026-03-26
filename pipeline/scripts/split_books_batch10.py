#!/usr/bin/env python3
"""10차 도서 3권 분할 스크립트 (Phase C).

대상:
  10. City of God — 선집 (아우구스티누스) — 핵심 7권 → ~30 파일
  11. Talks to Farmers (C.H. 스펄전) — 19편 설교
  12. Summa Theologica — 선집 (토마스 아퀴나스) — 제1부 핵심 20개 문제

소스:
  10: https://www.gutenberg.org/cache/epub/45304/pg45304.txt (Vol.1: Books 1-13)
      https://www.gutenberg.org/cache/epub/45305/pg45305.txt (Vol.2: Books 14-22)
  11: https://www.gutenberg.org/cache/epub/42518/pg42518.txt
  12: https://www.gutenberg.org/cache/epub/17611/pg17611.txt (Part I)

사용법:
  python pipeline/scripts/split_books_batch10.py [--download]
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
# 공통 유틸리티 (batch8/9와 동일)
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


# ─────────────────────────────────────────────
# 10. City of God — Augustine (선집: 7권)
# ─────────────────────────────────────────────

CITY_OF_GOD_META = {
    "slug": "city-of-god",
    "title": "신국론 (선집)",
    "title_original": "The City of God (Selected Books)",
    "author": "아우구스티누스 (Saint Augustine)",
    "author_original": "Saint Augustine of Hippo",
    "year": "426",
    "source": "https://www.gutenberg.org/ebooks/45304",
    "license": "public_domain",
    "translator": "Marcus Dods",
    "note": "22권 중 핵심 7권 선별 (제1,5,8,11,14,19,22권). 두 도성의 기원, 전개, 목적지.",
}

# 선별 Book 번호와 한국어 제목
SELECTED_BOOKS = {
    1: "제1권: 로마의 약탈 — 이교 신들의 무력함",
    5: "제5권: 로마의 운명과 하나님의 섭리",
    8: "제8권: 플라톤주의와 기독교 신학",
    11: "제11권: 두 도성의 기원 — 천사와 창조",
    14: "제14권: 두 사랑, 두 도성 — 원죄와 정욕",
    19: "제19권: 두 도성의 목적 — 평화와 정의",
    22: "제22권: 성도의 영원한 행복 — 부활의 몸",
}


_ORDINALS = {
    "FIRST": 1, "SECOND": 2, "THIRD": 3, "FOURTH": 4, "FIFTH": 5,
    "SIXTH": 6, "SEVENTH": 7, "EIGHTH": 8, "NINTH": 9, "TENTH": 10,
    "ELEVENTH": 11, "TWELFTH": 12, "THIRTEENTH": 13, "FOURTEENTH": 14,
    "FIFTEENTH": 15, "SIXTEENTH": 16, "SEVENTEENTH": 17, "EIGHTEENTH": 18,
    "NINETEENTH": 19, "TWENTIETH": 20, "TWENTY-FIRST": 21, "TWENTY-SECOND": 22,
}


def split_city_of_god(vol1_raw: str, vol2_raw: str) -> None:
    print("\n=== City of God (Augustine) — 선집 ===")
    v1 = extract_gutenberg(vol1_raw)
    v2 = extract_gutenberg(vol2_raw)
    text = v1 + "\n\n" + v2
    text = clean_text(text)
    out_dir = BOOKS_DIR / "city-of-god"

    # 본문에서 Book 경계: "BOOK FIRST.", "BOOK FOURTEENTH.[1]" 등 (서수 단어)
    book_pat = re.compile(
        r"\n\s*BOOK\s+([A-Z-]+)\.?\s*(?:\[\d+\])?\s*\n",
        re.MULTILINE,
    )
    book_matches = list(book_pat.finditer(text))

    chapters_meta = []

    for idx, bm in enumerate(book_matches):
        ordinal = bm.group(1).strip().upper()
        book_num = _ORDINALS.get(ordinal, 0)

        if book_num not in SELECTED_BOOKS:
            continue

        b_start = bm.end()
        b_end = book_matches[idx + 1].start() if idx + 1 < len(book_matches) else len(text)
        book_text = text[b_start:b_end].strip()
        book_text = re.sub(r"\n{3,}", "\n\n", book_text)

        book_title = SELECTED_BOOKS[book_num]

        # Chapter 마커 없음 → 단락 경계에서 8K 단위로 분할
        parts = split_text_at_paragraph(book_text)
        for pi, part in enumerate(parts):
            file_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            title = f"{book_title}{suffix}"
            save_chapter(out_dir, file_num, title, part)
            chapters_meta.append({
                "num": file_num, "title": title,
                "file": f"ch{file_num:02d}.txt",
                "book": book_num,
            })

    meta = {**CITY_OF_GOD_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    combined_raw = vol1_raw + "\n\n===== VOLUME 2 =====\n\n" + vol2_raw
    (out_dir / "raw.txt").write_text(combined_raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 11. Talks to Farmers — C.H. Spurgeon
# ─────────────────────────────────────────────

TALKS_META = {
    "slug": "talks-to-farmers",
    "title": "농부들에게 전하는 말씀",
    "title_original": "Talks to Farmers",
    "author": "C.H. 스펄전 (C.H. Spurgeon)",
    "author_original": "C.H. Spurgeon",
    "year": "1882",
    "source": "https://www.gutenberg.org/ebooks/42518",
    "license": "public_domain",
    "note": "농사 비유를 통한 19편의 영적 설교. 스펄전의 대중적 설교 스타일.",
}

TALKS_TITLES = {
    1: "게으른 자의 밭 (The Sluggard's Farm)",
    2: "무너진 울타리 (The Broken Fence)",
    3: "서리와 해빙 (Frost and Thaw)",
    4: "죽어야 열매 맺는 밀알 (The Corn of Wheat Dying to Bring Forth Fruit)",
    5: "밭가는 자 (The Ploughman)",
    6: "바위를 가는 것 (Ploughing the Rock)",
    7: "씨 뿌리는 자의 비유 (The Parable of the Sower)",
    8: "으뜸가는 밀 (The Principal Wheat)",
    9: "마음의 봄 (Spring in the Heart)",
    10: "농장 일꾼들 (Farm Laborers)",
    11: "일꾼들이 할 수 있는 것과 없는 것 (What the Farm Laborers Can Do)",
    12: "털 깎는 자 앞의 양 (The Sheep Before the Shearers)",
    13: "건초밭에서 (In the Hay-Field)",
    14: "추수의 기쁨 (The Joy of Harvest)",
    15: "영적 이삭줍기 (Spiritual Gleaning)",
    16: "곡식 밭의 식사 시간 (Meal-Time in the Cornfields)",
    17: "짐 실은 수레 (The Loaded Wagon)",
    18: "타작 (Threshing)",
    19: "곳간의 밀 (Wheat in the Barn)",
}


def split_talks_to_farmers(raw: str) -> None:
    print("\n=== Talks to Farmers (C.H. Spurgeon) ===")
    text = extract_gutenberg(raw)
    text = clean_text(text)
    out_dir = BOOKS_DIR / "talks-to-farmers"

    # 설교 제목: 열 0에서 시작하는 ALL-CAPS 줄 + 마침표 (TOC는 들여쓰기+쉼표)
    # 예: "THE SLUGGARD'S FARM." (열 0, 마침표) vs "  THE SLUGGARD'S FARM,  1" (TOC)
    title_pat = re.compile(r"\n([A-Z][A-Z\',\- ]{4,80})\.\s*\n")
    matches = list(title_pat.finditer(text))

    # 메타데이터 제외
    filtered = []
    skip = {"CONTENTS", "THE END", "FOOTNOTES", "INDEX", "TABLE OF CONTENTS",
            "TALKS TO FARMERS"}
    for m in matches:
        t = m.group(1).strip()
        if t in skip or len(t) < 8:
            continue
        filtered.append(m)

    chapters_meta = []
    for idx, m in enumerate(filtered):
        title_en = m.group(1).strip()
        start = m.end()
        end = filtered[idx + 1].start() if idx + 1 < len(filtered) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)

        if len(body.split()) < 200:
            continue

        ch_num = len(chapters_meta) + 1
        kr_title = TALKS_TITLES.get(ch_num, title_en.title())

        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            file_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            title = f"{kr_title}{suffix}"
            save_chapter(out_dir, file_num, title, part)
            chapters_meta.append({
                "num": file_num, "title": title,
                "file": f"ch{file_num:02d}.txt",
            })

    meta = {**TALKS_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 12. Summa Theologica — Thomas Aquinas (선집)
#     제1부(Prima Pars)에서 핵심 20개 문제 선별
# ─────────────────────────────────────────────

SUMMA_META = {
    "slug": "summa-selections",
    "title": "신학대전 (선집)",
    "title_original": "Summa Theologica (Selected Questions from Part I)",
    "author": "토마스 아퀴나스 (Thomas Aquinas)",
    "author_original": "Thomas Aquinas",
    "year": "1274",
    "source": "https://www.gutenberg.org/ebooks/17611",
    "license": "public_domain",
    "translator": "Fathers of the English Dominican Province",
    "note": "제1부(Prima Pars)에서 핵심 문제(Quaestio) 선별. 하나님의 존재, 본질, 삼위일체, 창조 등.",
}

# 선별할 핵심 문제(Question) 번호들
# Q2: 하나님의 존재, Q3: 하나님의 단순성, Q4: 하나님의 완전성,
# Q5: 선(善), Q11: 하나님의 단일성, Q12: 하나님을 아는 방법,
# Q13: 하나님의 이름들, Q14: 하나님의 지식, Q19: 하나님의 의지,
# Q22: 하나님의 섭리, Q25: 하나님의 능력, Q27: 성삼위의 발출,
# Q29: 위격(Person), Q44: 만물의 제1원인, Q45: 창조의 양식,
# Q47: 사물의 다양성, Q75: 인간의 영혼, Q76: 영혼과 육체의 결합,
# Q82: 의지, Q83: 자유의지
SELECTED_QUESTIONS = [2, 3, 4, 5, 11, 12, 13, 14, 19, 22,
                       25, 27, 29, 44, 45, 47, 75, 76, 82, 83]

QUESTION_TITLES = {
    2: "하나님의 존재 (The Existence of God)",
    3: "하나님의 단순성 (The Simplicity of God)",
    4: "하나님의 완전성 (The Perfection of God)",
    5: "선(善)에 관하여 (Of Goodness in General)",
    11: "하나님의 단일성 (The Unity of God)",
    12: "하나님을 아는 방법 (How God is Known by Us)",
    13: "하나님의 이름들 (The Names of God)",
    14: "하나님의 지식 (Of God's Knowledge)",
    19: "하나님의 의지 (The Will of God)",
    22: "하나님의 섭리 (The Providence of God)",
    25: "하나님의 능력 (The Power of God)",
    27: "성삼위의 발출 (The Procession of the Divine Persons)",
    29: "신적 위격 (The Divine Persons)",
    44: "만물의 제1원인으로서의 하나님 (God as First Cause)",
    45: "창조의 양식 (The Mode of Emanation of Things)",
    47: "사물의 다양성 (Of the Distinction of Things)",
    75: "인간의 영혼 (Of Man — the Soul)",
    76: "영혼과 육체의 결합 (The Union of Body and Soul)",
    82: "의지 (The Will)",
    83: "자유의지 (Free-Will)",
}


def split_summa(raw: str) -> None:
    print("\n=== Summa Theologica — Part I (Selected Questions) ===")
    text = extract_gutenberg(raw)
    text = clean_text(text)
    out_dir = BOOKS_DIR / "summa-selections"

    # Question 경계 찾기: "QUESTION 2" or "QUESTION II" 등
    q_pat = re.compile(
        r"\n\s*QUESTION\s+(\d+|[IVXLC]+)\.?\s*\n",
        re.IGNORECASE,
    )
    matches = list(q_pat.finditer(text))

    chapters_meta = []
    selected_set = set(SELECTED_QUESTIONS)

    for idx, m in enumerate(matches):
        grp = m.group(1)
        q_num = int(grp) if grp.isdigit() else _roman(grp)

        if q_num not in selected_set:
            continue

        start = m.start()  # Question 헤더부터 포함
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)

        kr_title = QUESTION_TITLES.get(q_num, f"문제 {q_num}")

        # Article 단위로 더 분할할 수 있지만 Question 단위로 유지
        # 8K 초과시 Article 경계에서 분할
        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            file_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            title = f"문제 {q_num}: {kr_title}{suffix}"
            save_chapter(out_dir, file_num, title, part)
            chapters_meta.append({
                "num": file_num, "title": title,
                "file": f"ch{file_num:02d}.txt",
                "question": q_num,
            })

    meta = {**SUMMA_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# main
# ─────────────────────────────────────────────

URLS = {
    "city_v1": "https://www.gutenberg.org/cache/epub/45304/pg45304.txt",
    "city_v2": "https://www.gutenberg.org/cache/epub/45305/pg45305.txt",
    "talks": "https://www.gutenberg.org/cache/epub/42518/pg42518.txt",
    "summa": "https://www.gutenberg.org/cache/epub/17611/pg17611.txt",
}


def main():
    do_download = "--download" in sys.argv or len(sys.argv) == 1
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    print("=== Phase C: 3권 도서 분할 시작 ===\n")

    # ── 10. City of God ──
    c1 = CACHE_DIR / "city_of_god_v1.txt"
    c2 = CACHE_DIR / "city_of_god_v2.txt"
    if do_download:
        v1 = download(URLS["city_v1"], c1)
        v2 = download(URLS["city_v2"], c2)
    else:
        v1 = c1.read_text(encoding="utf-8")
        v2 = c2.read_text(encoding="utf-8")
    split_city_of_god(v1, v2)

    # ── 11. Talks to Farmers ──
    cache = CACHE_DIR / "talks_to_farmers.txt"
    if do_download:
        raw = download(URLS["talks"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_talks_to_farmers(raw)

    # ── 12. Summa Theologica ──
    cache = CACHE_DIR / "summa_part1.txt"
    if do_download:
        raw = download(URLS["summa"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_summa(raw)

    print("\n✅ Phase C: 3권 분할 완료!")


if __name__ == "__main__":
    main()
