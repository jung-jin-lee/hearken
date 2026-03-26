#!/usr/bin/env python3
"""9차 도서 4권 분할 스크립트 (Phase B).

대상:
  6. The Saints' Everlasting Rest (리처드 백스터) — 16장 → ~25 파일
  7. True Christianity (요한 아른트) — 제1-2권만 → ~40 파일
  8. The Interior Castle (아빌라의 테레사) — 7거처 → ~21 파일
  9. The Apostolic Fathers (다수) — 선별 문서 → ~25 파일

소스:
  6: https://www.gutenberg.org/cache/epub/58135/pg58135.txt
  7: https://www.gutenberg.org/cache/epub/34736/pg34736.txt
  8: https://ccel.org/ccel/t/teresa/castle2/cache/castle2.txt
  9: https://www.gutenberg.org/cache/epub/77576/pg77576.txt

사용법:
  python pipeline/scripts/split_books_batch9.py [--download]
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
# 공통 유틸리티 (batch8과 동일)
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
    "XXXIII": 33, "XXXIV": 34, "XXXV": 35, "XXXVI": 36,
    "XXXVII": 37, "XXXVIII": 38, "XXXIX": 39, "XL": 40,
    "XLI": 41, "XLII": 42, "XLIII": 43, "XLIV": 44, "XLV": 45,
    "XLVI": 46, "XLVII": 47, "XLVIII": 48, "XLIX": 49, "L": 50,
    "LI": 51, "LII": 52, "LIII": 53, "LIV": 54, "LV": 55,
    "LVI": 56, "LVII": 57,
}

def _roman(s: str) -> int:
    return _ROMAN_MAP.get(s.upper().strip(), 0)


# ─────────────────────────────────────────────
# 6. The Saints' Everlasting Rest — Richard Baxter
# ─────────────────────────────────────────────

SAINTS_REST_META = {
    "slug": "saints-everlasting-rest",
    "title": "성도의 영원한 안식",
    "title_original": "The Saints' Everlasting Rest",
    "author": "리처드 백스터 (Richard Baxter)",
    "author_original": "Richard Baxter",
    "year": "1650",
    "source": "https://www.gutenberg.org/ebooks/58135",
    "license": "public_domain",
    "note": "천상의 안식에 대한 묵상과 하늘을 향한 삶의 실천에 관한 청교도 경건 문학의 고전.",
}

SAINTS_REST_TITLES = {
    1: "서론: 성도의 안식의 본질",
    2: "성도의 안식을 위한 위대한 준비",
    3: "성도의 안식의 탁월함",
    4: "이 안식이 예비된 사람들의 성격",
    5: "성도의 안식을 잃는 자들의 비참",
    6: "안식을 잃고 지옥의 고통을 받는 자들의 비참",
    7: "성도의 안식을 부지런히 구해야 할 필요성",
    8: "성도의 안식에 대한 권리를 분별하는 방법",
    9: "다른 이들에게 이 안식을 구하도록 권면하는 의무",
    10: "성도의 안식은 이 땅에서 기대할 수 없음",
    11: "이 땅에서 천상의 삶을 사는 것의 중요성",
    12: "이 땅에서 천상의 삶을 사는 방법",
    13: "천상 묵상의 본질, 시간, 장소, 기질",
    14: "천상 묵상에서 숙고, 감정, 독백, 기도의 활용",
    15: "감각적 대상의 도움과 배신하는 마음의 경계",
    16: "천상 묵상의 실례와 전체 결론",
}


def split_saints_rest(raw: str) -> None:
    print("\n=== The Saints' Everlasting Rest (Richard Baxter) ===")
    text = extract_gutenberg(raw)
    text = clean_text(text)
    out_dir = BOOKS_DIR / "saints-everlasting-rest"

    # "CHAP. I." 패턴 — 열 0에서 시작하는 것만 (TOC는 들여쓰기됨)
    pat = re.compile(r"\nCHAP\.\s*([IVXLC]+)\.?\s*\n", re.MULTILINE)
    matches = list(pat.finditer(text))

    if not matches:
        pat = re.compile(r"\nChapter\s+([IVXLC]+)\b")
        matches = list(pat.finditer(text))

    chapters_meta = []
    for idx, m in enumerate(matches):
        ch_num = _roman(m.group(1))
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)

        kr_title = SAINTS_REST_TITLES.get(ch_num, f"제{ch_num}장")
        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            file_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            title = f"제{ch_num}장: {kr_title}{suffix}"
            save_chapter(out_dir, file_num, title, part)
            chapters_meta.append({
                "num": file_num, "title": title,
                "file": f"ch{file_num:02d}.txt",
            })

    meta = {**SAINTS_REST_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 7. True Christianity — Johann Arndt (제1-2권만)
# ─────────────────────────────────────────────

TRUE_CHRISTIANITY_META = {
    "slug": "true-christianity",
    "title": "참된 기독교",
    "title_original": "True Christianity",
    "author": "요한 아른트 (Johann Arndt)",
    "author_original": "Johann Arndt",
    "year": "1606",
    "source": "https://www.gutenberg.org/ebooks/34736",
    "license": "public_domain",
    "note": "경건주의 운동의 기초가 된 저서. 제1-2권만 수록 (가장 핵심적인 경건생활 부분).",
}


def split_true_christianity(raw: str) -> None:
    print("\n=== True Christianity (Johann Arndt) ===")
    text = extract_gutenberg(raw)
    text = clean_text(text)
    out_dir = BOOKS_DIR / "true-christianity"

    # Book III 시작 이전까지만 사용 (제1-2권)
    # 열 0에서 시작하는 BOOK만 매칭 (TOC 회피)
    book3_pat = re.compile(r"\nBOOK\s+(III|IV)\.", re.MULTILINE)
    book3_match = book3_pat.search(text)
    if book3_match:
        text = text[:book3_match.start()]

    # Chapter 패턴: 열 0의 "Chapter I." (TOC는 들여쓰기됨)
    ch_pat = re.compile(r"\nChapter\s+([IVXLC]+)\.\s*\n")
    matches = list(ch_pat.finditer(text))

    # Book 경계: 열 0의 "BOOK I."
    book_pat = re.compile(r"\nBOOK\s+(I{1,2})\.", re.MULTILINE)
    book_matches = list(book_pat.finditer(text))

    # 각 Chapter에 Book 번호 할당
    def get_book_num(ch_pos: int) -> int:
        book_num = 1
        for bm in book_matches:
            if bm.start() < ch_pos:
                grp = bm.group(1).upper()
                if grp in ("I", "THE FIRST"):
                    book_num = 1
                elif grp in ("II", "THE SECOND"):
                    book_num = 2
        return book_num

    chapters_meta = []
    ch_in_book: dict[int, int] = {}  # book_num → 카운터

    for idx, m in enumerate(matches):
        ch_roman_num = _roman(m.group(1))
        book_num = get_book_num(m.start())

        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()

        # Book 헤더가 본문에 섞여있으면 제거
        body = re.sub(r"^\s*BOOK\s+(I{1,2}|THE\s+\w+)\b.*?\n", "", body,
                       flags=re.IGNORECASE | re.MULTILINE)
        body = re.sub(r"\n{3,}", "\n\n", body)

        # 첫 줄에서 챕터 제목 추출
        first_line = body.split("\n")[0].strip() if body else ""
        if len(first_line) > 10 and len(first_line) < 200:
            ch_subtitle = first_line[:80]
        else:
            ch_subtitle = ""

        ch_in_book[book_num] = ch_in_book.get(book_num, 0) + 1
        ch_count = ch_in_book[book_num]

        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            file_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            if ch_subtitle:
                title = f"제{book_num}권 제{ch_count}장: {ch_subtitle}{suffix}"
            else:
                title = f"제{book_num}권 제{ch_count}장{suffix}"
            save_chapter(out_dir, file_num, title, part)
            chapters_meta.append({
                "num": file_num, "title": title,
                "file": f"ch{file_num:02d}.txt",
                "book": book_num,
            })

    meta = {**TRUE_CHRISTIANITY_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료 (제1-2권)")


# ─────────────────────────────────────────────
# 8. The Interior Castle — Teresa of Avila
# ─────────────────────────────────────────────

INTERIOR_CASTLE_META = {
    "slug": "interior-castle",
    "title": "영혼의 성",
    "title_original": "The Interior Castle (Las Moradas)",
    "author": "아빌라의 테레사 (St. Teresa of Avila)",
    "author_original": "St. Teresa of Avila",
    "year": "1577",
    "source": "https://ccel.org/ccel/t/teresa/castle2",
    "license": "public_domain",
    "translator": "The Benedictines of Stanbrook / E. Allison Peers",
    "note": "영혼을 보석 성에 비유하여 7개 거처를 통한 영적 성장의 여정을 묘사한 신비 신학의 걸작.",
}

MANSION_NAMES = {
    1: "첫째 거처: 자기 인식과 기도",
    2: "둘째 거처: 인내와 유혹의 싸움",
    3: "셋째 거처: 이 세상의 불안정함",
    4: "넷째 거처: 초자연적 기도의 시작",
    5: "다섯째 거처: 합일 기도",
    6: "여섯째 거처: 영적 약혼",
    7: "일곱째 거처: 영적 결혼",
}


def split_interior_castle(raw: str) -> None:
    print("\n=== The Interior Castle (Teresa of Avila) ===")
    text = clean_text(raw)
    out_dir = BOOKS_DIR / "interior-castle"

    # 거처(Mansion) 경계: "THE FIRST MANSIONS", "THE SECOND MANSIONS" 등
    mansion_pat = re.compile(
        r"\n\s*THE\s+(FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH)\s+MANSIONS?\s*\n",
        re.IGNORECASE,
    )
    mansion_matches = list(mansion_pat.finditer(text))

    ordinal_map = {
        "FIRST": 1, "SECOND": 2, "THIRD": 3, "FOURTH": 4,
        "FIFTH": 5, "SIXTH": 6, "SEVENTH": 7,
    }

    # 챕터 경계: "Chapter I" 또는 "CHAPTER I"
    ch_pat = re.compile(r"\n\s*Chapter\s+([IVXLC]+)\b", re.IGNORECASE)

    chapters_meta = []

    for m_idx, mm in enumerate(mansion_matches):
        mansion_num = ordinal_map[mm.group(1).upper()]
        m_start = mm.end()
        m_end = mansion_matches[m_idx + 1].start() if m_idx + 1 < len(mansion_matches) else len(text)
        mansion_text = "\n" + text[m_start:m_end]  # \n 추가: 첫 CHAPTER도 매칭되도록

        ch_matches = list(ch_pat.finditer(mansion_text))
        mansion_name = MANSION_NAMES.get(mansion_num, f"제{mansion_num}거처")

        if ch_matches:
            for c_idx, cm in enumerate(ch_matches):
                ch_num = _roman(cm.group(1))
                c_start = cm.end()
                c_end = ch_matches[c_idx + 1].start() if c_idx + 1 < len(ch_matches) else len(mansion_text)
                body = mansion_text[c_start:c_end].strip()
                body = re.sub(r"\n{3,}", "\n\n", body)

                parts = split_text_at_paragraph(body)
                for pi, part in enumerate(parts):
                    file_num = len(chapters_meta) + 1
                    suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
                    title = f"{mansion_name} — 제{ch_num}장{suffix}"
                    save_chapter(out_dir, file_num, title, part)
                    chapters_meta.append({
                        "num": file_num, "title": title,
                        "file": f"ch{file_num:02d}.txt",
                        "mansion": mansion_num,
                    })
        else:
            # 챕터 분할 없는 거처 — 전체를 하나로
            body = mansion_text.strip()
            body = re.sub(r"\n{3,}", "\n\n", body)
            parts = split_text_at_paragraph(body)
            for pi, part in enumerate(parts):
                file_num = len(chapters_meta) + 1
                suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
                title = f"{mansion_name}{suffix}"
                save_chapter(out_dir, file_num, title, part)
                chapters_meta.append({
                    "num": file_num, "title": title,
                    "file": f"ch{file_num:02d}.txt",
                    "mansion": mansion_num,
                })

    meta = {**INTERIOR_CASTLE_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 9. The Apostolic Fathers — 선별 문서
# ─────────────────────────────────────────────

APOSTOLIC_META = {
    "slug": "apostolic-fathers",
    "title": "사도교부 문헌집",
    "title_original": "The Writings of the Apostolic Fathers",
    "author": "클레멘트, 이그나티우스, 폴리카르프 외",
    "author_original": "Clement, Ignatius, Polycarp et al.",
    "year": "1-2세기",
    "source": "https://www.gutenberg.org/ebooks/77576",
    "license": "public_domain",
    "note": "초대교회 사도교부들의 서신과 문헌 모음. 1세기 말~2세기 초.",
}

# 선별할 문서들 (플랜 기준: 클레멘트 1서, 이그나티우스 서신, 폴리카르프, 디오그네투스)
APOSTOLIC_WORKS = [
    # (시작 패턴, 한국어 제목, 영어 제목)
    ("FIRST EPISTLE OF CLEMENT", "클레멘트의 첫째 서신", "First Epistle of Clement to the Corinthians"),
    ("SECOND EPISTLE OF CLEMENT", "클레멘트의 둘째 서신", "Second Epistle of Clement"),
    ("EPISTLE OF POLYCARP", "폴리카르프의 서신", "Epistle of Polycarp to the Philippians"),
    ("MARTYRDOM OF POLYCARP", "폴리카르프의 순교", "The Martyrdom of Polycarp"),
    ("EPISTLE OF BARNABAS", "바나바 서신", "The Epistle of Barnabas"),
    ("EPISTLE TO DIOGNETUS", "디오그네투스에게 보내는 편지", "The Epistle to Diognetus"),
    # 이그나티우스 서신들
    ("EPISTLE OF IGNATIUS TO THE EPHESIANS", "이그나티우스의 에베소 교회 서신", "Epistle of Ignatius to the Ephesians"),
    ("EPISTLE OF IGNATIUS TO THE MAGNESIANS", "이그나티우스의 마그네시아 교회 서신", "Epistle of Ignatius to the Magnesians"),
    ("EPISTLE OF IGNATIUS TO THE TRALLIANS", "이그나티우스의 트랄레스 교회 서신", "Epistle of Ignatius to the Trallians"),
    ("EPISTLE OF IGNATIUS TO THE ROMANS", "이그나티우스의 로마 교회 서신", "Epistle of Ignatius to the Romans"),
    ("EPISTLE OF IGNATIUS TO THE PHILADELPHIANS", "이그나티우스의 필라델피아 교회 서신", "Epistle of Ignatius to the Philadelphians"),
    ("EPISTLE OF IGNATIUS TO THE SMYRNAEANS", "이그나티우스의 서머나 교회 서신", "Epistle of Ignatius to the Smyrnaeans"),
    ("EPISTLE OF IGNATIUS TO POLYCARP", "이그나티우스가 폴리카르프에게", "Epistle of Ignatius to Polycarp"),
]


def split_apostolic_fathers(raw: str) -> None:
    print("\n=== The Apostolic Fathers ===")
    text = extract_gutenberg(raw)
    text = clean_text(text)
    out_dir = BOOKS_DIR / "apostolic-fathers"

    chapters_meta = []

    # 직접 문서 경계 찾기: (검색 문자열, 한국어 제목)
    # 각주 참조가 있는 전체 제목 사용 — 본문 제목과 정확히 매칭
    doc_markers = [
        ("FIRST EPISTLE OF CLEMENT TO THE CORINTHIANS", "클레멘트의 첫째 서신"),
        ("SECOND EPISTLE OF CLEMENT", "클레멘트의 둘째 서신"),
        ("EPISTLE OF POLYCARP TO THE PHILIPPIANS", "폴리카르프의 서신"),
        ("MARTYRDOM OF THE HOLY POLYCARP", "폴리카르프의 순교"),
        ("EPISTLE OF BARNABAS", "바나바 서신"),
        ("EPISTLE OF IGNATIUS TO THE EPHESIANS", "이그나티우스의 에베소 교회 서신"),
        ("EPISTLE OF IGNATIUS TO THE MAGNESIANS", "이그나티우스의 마그네시아 교회 서신"),
        ("EPISTLE OF IGNATIUS TO THE TRALLIANS", "이그나티우스의 트랄레스 교회 서신"),
        ("EPISTLE OF IGNATIUS TO THE ROMANS", "이그나티우스의 로마 교회 서신"),
        ("EPISTLE OF IGNATIUS TO THE PHILADELPHIANS", "이그나티우스의 필라델피아 교회 서신"),
        ("EPISTLE OF IGNATIUS TO THE SMYRN", "이그나티우스의 서머나 교회 서신"),
        ("EPISTLE OF IGNATIUS TO POLYCARP", "이그나티우스가 폴리카르프에게"),
        ("EPISTLE TO DIOGNETUS", "디오그네투스에게 보내는 편지"),
    ]

    upper = text.upper()

    # CHAP. 가 뒤따르는 출현을 찾아 (content_start, kr) 리스트 생성
    found: list[tuple[int, str]] = []
    for marker, kr in doc_markers:
        pos = 0
        while True:
            idx = upper.find(marker, pos)
            if idx < 0:
                break
            window = upper[idx:idx + 2000]
            chap_off = window.find("CHAP.")
            if chap_off >= 0:
                # 스퓨리어스 "SECOND EPISTLE OF IGNATIUS" 회피
                if "SECOND EPISTLE OF IGNATIUS" not in upper[idx:idx + 60]:
                    found.append((idx + chap_off, kr))
                    break
            pos = idx + 1

    found.sort(key=lambda x: x[0])

    # HERMAS 본문 위치 찾기 (TOC 회피 — 마지막 found 이후에서 검색)
    last_found_pos = found[-1][0] if found else 0
    hermas = upper.find("THE PASTOR OF HERMAS", last_found_pos)
    if hermas < 0:
        hermas = len(text)

    print(f"  [발견] {len(found)}개 문서")

    for i, (start, kr) in enumerate(found):
        if start >= hermas:
            continue
        end = found[i + 1][0] if i + 1 < len(found) else hermas

        body = text[start:end]
        # 뒤에 붙은 INTRODUCTORY NOTICE 제거
        intro = body.upper().rfind("INTRODUCTORY NOTICE")
        if intro > 0 and intro > len(body) * 0.7:
            body = body[:intro]

        body = re.sub(r"\n{3,}", "\n\n", body.strip())
        if len(body.split()) < 100:
            continue

        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            file_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            title = f"{kr}{suffix}"
            save_chapter(out_dir, file_num, title, part)
            chapters_meta.append({
                "num": file_num, "title": title,
                "file": f"ch{file_num:02d}.txt",
            })

    meta = {**APOSTOLIC_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# main
# ─────────────────────────────────────────────

URLS = {
    "saints_rest": "https://www.gutenberg.org/cache/epub/58135/pg58135.txt",
    "true_christianity": "https://www.gutenberg.org/cache/epub/34736/pg34736.txt",
    "interior_castle": "https://ccel.org/ccel/t/teresa/castle2/cache/castle2.txt",
    "apostolic_fathers": "https://www.gutenberg.org/cache/epub/77576/pg77576.txt",
}


def main():
    do_download = "--download" in sys.argv or len(sys.argv) == 1
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    print("=== Phase B: 4권 도서 분할 시작 ===\n")

    # ── 6. Saints' Everlasting Rest ──
    cache = CACHE_DIR / "saints_rest.txt"
    if do_download:
        raw = download(URLS["saints_rest"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_saints_rest(raw)

    # ── 7. True Christianity ──
    cache = CACHE_DIR / "true_christianity.txt"
    if do_download:
        raw = download(URLS["true_christianity"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_true_christianity(raw)

    # ── 8. Interior Castle ──
    cache = CACHE_DIR / "interior_castle.txt"
    if do_download:
        raw = download(URLS["interior_castle"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_interior_castle(raw)

    # ── 9. Apostolic Fathers ──
    cache = CACHE_DIR / "apostolic_fathers.txt"
    if do_download:
        raw = download(URLS["apostolic_fathers"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_apostolic_fathers(raw)

    print("\n✅ Phase B: 4권 분할 완료!")


if __name__ == "__main__":
    main()
