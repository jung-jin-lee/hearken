#!/usr/bin/env python3
"""2권 신규 도서 분할 스크립트.

- The True Vine (Andrew Murray) — abide-in-christ 슬롯에 배치
- Institutes of the Christian Religion (John Calvin) — Books I~IV

소스 다운로드:
  True Vine: https://ccel.org/ccel/m/murray/true_vine/cache/true_vine.txt
  Institutes Vol.1: https://www.gutenberg.org/cache/epub/45001/pg45001.txt
  Institutes Vol.2: https://www.gutenberg.org/cache/epub/64392/pg64392.txt

사용법:
  python pipeline/scripts/split_books_batch7.py [--download]
"""

import json
import re
import sys
import urllib.request
from pathlib import Path

BOOKS_DIR = Path("pipeline/sources/data/books")

# ─────────────────────────────────────────────
# 공통 유틸리티
# ─────────────────────────────────────────────

def download(url: str, dest: Path) -> str:
    """URL에서 텍스트를 다운로드하여 파일에 저장하고 반환한다."""
    if dest.exists() and dest.stat().st_size > 10000:
        print(f"  [캐시] {dest.name}")
        return dest.read_text(encoding="utf-8")
    print(f"  [다운로드] {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        text = r.read().decode("utf-8")
    dest.write_text(text, encoding="utf-8")
    return text


def clean_text(text: str) -> str:
    """과도한 공백 및 구분선 정리."""
    text = re.sub(r"_{5,}", "", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip()


def save_chapter(out_dir: Path, num: int, title: str, body: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"ch{num:02d}.txt"
    path.write_text(f"{title}\n\n{body.strip()}\n", encoding="utf-8")
    words = len(body.split())
    print(f"  ch{num:02d}.txt: {title[:60]} ({words} words)")


def save_metadata(out_dir: Path, meta: dict) -> None:
    (out_dir / "metadata.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ─────────────────────────────────────────────
# 1. The True Vine — Andrew Murray
#    (abide-in-christ 슬롯에 배치, 29~31일 묵상)
# ─────────────────────────────────────────────

TRUE_VINE_METADATA = {
    "slug": "abide-in-christ",
    "title": "참된 포도나무",
    "title_original": "The True Vine: Meditations for a Month on John 15:1-16",
    "author": "앤드류 머레이 (Andrew Murray)",
    "author_original": "Andrew Murray",
    "year": "1897",
    "source": "https://ccel.org/ccel/m/murray/true_vine/cache/true_vine.txt",
    "license": "public_domain",
    "note": "요한복음 15장 포도나무 비유 기반 31일 묵상집. 그리스도 안에 거함(abiding in Christ) 주제.",
}

# 섹션 제목들 순서대로 (출현 순서 기반 — "THE VINE"이 두 번 나오므로 순서 목록 사용)
# 형식: (섹션 제목, 챕터 번호, 한국어 부제)
TRUE_VINE_SEQUENCE = [
    ("THE VINE",              1,  "포도나무 — 요한복음 15:1"),
    ("THE HUSBANDMAN",        2,  "농부 — 요한복음 15:1"),
    ("THE BRANCH",            3,  "가지 — 요한복음 15:2"),
    ("THE FRUIT",             4,  "열매 — 요한복음 15:2"),
    ("MORE FRUIT",            5,  "더 많은 열매 — 요한복음 15:2"),
    ("THE CLEANSING",         6,  "깨끗하게 하심 — 요한복음 15:3"),
    ("THE PRUNING KNIFE",     7,  "가지치기 — 요한복음 15:2"),
    ("ABIDE",                 8,  "거하라 — 요한복음 15:4"),
    ("EXCEPT YE ABIDE",       9,  "거하지 아니하면 — 요한복음 15:4"),
    ("THE VINE",              10, "참 포도나무 — 요한복음 15:5"),   # 두 번째 THE VINE
    ("YE THE BRANCHES",       11, "너희는 가지 — 요한복음 15:5"),
    ("MUCH FRUIT",            12, "많은 열매 — 요한복음 15:5"),
    ("YOU CAN DO NOTHING",    13, "아무것도 할 수 없다 — 요한복음 15:5"),
    ("WITHERED BRANCHES",     14, "마른 가지 — 요한복음 15:6"),
    ("WHATSOEVER YE WILL",    15, "무엇이든지 구하라 — 요한복음 15:7"),
    ("IF YE ABIDE",           16, "만일 내 말이 너희 안에 거하면 — 요한복음 15:7"),
    ("THE FATHER GLORIFIED",  17, "아버지께서 영광을 받으심 — 요한복음 15:8"),
    ("TRUE DISCIPLES",        18, "참 제자 — 요한복음 15:8"),
    ("THE WONDERFUL LOVE",    19, "놀라운 사랑 — 요한복음 15:9"),
    ("ABIDE IN MY LOVE",      20, "내 사랑 안에 거하라 — 요한복음 15:9"),
    ("OBEY AND ABIDE",        21, "순종과 거함 — 요한복음 15:10"),
    ("LOVE ONE ANOTHER",      22, "서로 사랑하라 — 요한복음 15:12"),
    ("EVEN AS I HAVE LOVED YOU", 23, "내가 너희를 사랑한 것같이 — 요한복음 15:12"),
    ("ELECTION",              24, "택하심 — 요한복음 15:16"),
    ("ABIDING FRUIT",         25, "영구한 열매 — 요한복음 15:16"),
    ("PREVAILING PRAYER",     26, "응답받는 기도 — 요한복음 15:16"),
]
# 빠른 조회용 set (제목들)
TRUE_VINE_TITLE_SET = {title for title, _, _ in TRUE_VINE_SEQUENCE}


def split_true_vine(raw_text: str) -> None:
    """The True Vine을 섹션별로 분할한다.

    TRUE_VINE_SEQUENCE를 순서대로 소비하면서 텍스트의 ALL-CAPS 제목들과 매핑한다.
    "THE VINE" 중복 등 동일 제목의 두 번째 출현도 올바르게 처리한다.
    """
    print("\n=== The True Vine (Andrew Murray) ===")
    text = clean_text(raw_text)
    out_dir = BOOKS_DIR / "abide-in-christ"

    # ALL-CAPS 제목 경계들 수집 (알려진 제목들만)
    pattern = re.compile(r"\n([A-Z][A-Z ]{2,45})\n", re.MULTILINE)
    all_matches = [(m, m.group(1).strip()) for m in pattern.finditer(text)
                   if m.group(1).strip() in TRUE_VINE_TITLE_SET]

    # sequence를 앞에서부터 소비하며 매핑
    seq_iter = iter(TRUE_VINE_SEQUENCE)
    seq_item = next(seq_iter, None)   # (title_key, ch_num, ch_title_kr)

    paired = []   # [(match, ch_num, full_title), ...]

    for match, key in all_matches:
        if seq_item is None:
            break
        exp_key, ch_num, ch_title_kr = seq_item
        if key == exp_key:
            full_title = f"{ch_num}일째: {key} — {ch_title_kr}"
            paired.append((match, ch_num, full_title))
            seq_item = next(seq_iter, None)

    chapters_meta = []
    for idx, (match, ch_num, full_title) in enumerate(paired):
        start = match.end()
        end = paired[idx + 1][0].start() if idx + 1 < len(paired) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)

        save_chapter(out_dir, ch_num, full_title, body)
        chapters_meta.append({
            "num": ch_num,
            "title": full_title,
            "file": f"ch{ch_num:02d}.txt",
        })

    chapters_meta.sort(key=lambda x: x["num"])
    meta = {**TRUE_VINE_METADATA, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw_text, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 2. Institutes of the Christian Religion — John Calvin
#    Book 단위로 분할 (Book I~IV = 4챕터)
#    Vol.1(pg45001): Book I, II, III ch.I~XIII
#    Vol.2(pg64392): Book III ch.XIV~XXV, Book IV
# ─────────────────────────────────────────────

INSTITUTES_METADATA = {
    "slug": "institutes-calvin",
    "title": "기독교 강요",
    "title_original": "Institutes of the Christian Religion",
    "author": "존 칼빈 (John Calvin)",
    "author_original": "John Calvin",
    "year": "1559",
    "source": "https://www.gutenberg.org/ebooks/45001 + 64392",
    "license": "public_domain",
    "note": "John Allen 번역 (1813). 4권 구성: 하나님의 지식, 그리스도, 은혜, 교회. Book 단위로 분할.",
    "translator": "John Allen",
}

INSTITUTES_BOOK_TITLES = {
    1: "제1권: 창조주 하나님을 아는 지식",
    2: "제2권: 구속주 하나님, 그리스도를 아는 지식",
    3: "제3권: 그리스도의 은혜를 받는 방법",
    4: "제4권: 하나님이 우리를 그리스도의 교제로 초청하시는 외적 수단",
}


def extract_gutenberg_content(text: str) -> str:
    """Gutenberg 헤더/푸터를 제거하고 본문만 반환한다."""
    start_marker = "*** START OF THE PROJECT GUTENBERG"
    end_marker = "*** END OF THE PROJECT GUTENBERG"
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start != -1:
        text = text[start:].split("\n", 1)[1] if "\n" in text[start:] else text[start:]
    if end != -1:
        text = text[:end]
    return text.strip()


def roman_to_int(r: str) -> int:
    vals = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7,
            "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12, "XIII": 13,
            "XIV": 14, "XV": 15, "XVI": 16, "XVII": 17, "XVIII": 18,
            "XIX": 19, "XX": 20, "XXI": 21, "XXII": 22, "XXIII": 23,
            "XXIV": 24, "XXV": 25}
    return vals.get(r.upper(), 0)


MAX_CHAPTER_WORDS = 8000  # 이보다 크면 반으로 분할


def split_text_at_paragraph(text: str, max_words: int) -> list[str]:
    """텍스트를 max_words 이하의 단락 경계에서 분할한다."""
    words = text.split()
    if len(words) <= max_words:
        return [text]

    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    chunks, current, current_words = [], [], 0
    for para in paragraphs:
        pw = len(para.split())
        if current_words + pw > max_words and current:
            chunks.append("\n\n".join(current))
            current, current_words = [], 0
        current.append(para)
        current_words += pw
    if current:
        chunks.append("\n\n".join(current))
    return chunks if chunks else [text]


def parse_chapters_from_text(text: str, vol_label: str) -> list[tuple[str, str, str]]:
    """텍스트에서 Book 번호, Chapter 번호, 본문을 파싱한다.

    반환: [(book_roman, chapter_roman, body), ...]
    """
    # Book 경계: 들여쓰기 허용
    book_pat = re.compile(r"^\s*BOOK (I{1,3}|IV)\b", re.MULTILINE)
    # Chapter 경계: Vol1 "   Chapter X.", Vol2 "   CHAPTER X." — 대소문자 무관
    ch_pat = re.compile(r"^\s+CHAPTER ([IVXLC]+)\.", re.MULTILINE | re.IGNORECASE)

    book_matches = list(book_pat.finditer(text))
    print(f"  {vol_label}: {len(book_matches)}개 Book, ", end="")

    chapters = []
    for b_idx, b_match in enumerate(book_matches):
        book_roman = b_match.group(1).upper()
        b_start = b_match.start()
        b_end = book_matches[b_idx + 1].start() if b_idx + 1 < len(book_matches) else len(text)
        book_text = text[b_start:b_end]

        ch_matches = list(ch_pat.finditer(book_text))
        for c_idx, c_match in enumerate(ch_matches):
            ch_roman = c_match.group(1).upper()
            c_start = c_match.end()
            c_end = ch_matches[c_idx + 1].start() if c_idx + 1 < len(ch_matches) else len(book_text)
            body = book_text[c_start:c_end].strip()
            body = re.sub(r"\n{4,}", "\n\n\n", body)
            chapters.append((book_roman, ch_roman, body))

    print(f"{len(chapters)}개 Chapter 파싱 완료")
    return chapters


def split_institutes(vol1_text: str, vol2_text: str) -> None:
    """Calvin Institutes를 챕터 단위로 분할한다.

    - Vol.1: Book I (ch.I~XVIII), Book II (ch.I~XVII), Book III (ch.I~XIII)
    - Vol.2: Book III (ch.XIV~XXV), Book IV (ch.I~XX)
    - 8,000 단어 초과 챕터는 단락 경계에서 분할 (A, B 파트)
    총 ~80개 챕터, 일부 대형 챕터는 2~3개 파일로 분할 → 최대 ~110 파일 예상.
    """
    print("\n=== Institutes of the Christian Religion (John Calvin) ===")
    out_dir = BOOKS_DIR / "institutes-calvin"
    out_dir.mkdir(parents=True, exist_ok=True)

    v1 = extract_gutenberg_content(vol1_text)
    v2 = extract_gutenberg_content(vol2_text)

    chapters_v1 = parse_chapters_from_text(v1, "Vol.1")
    chapters_v2 = parse_chapters_from_text(v2, "Vol.2")

    # Book III는 두 볼륨에 걸쳐 있으므로 합산
    # Vol.1의 Book III + Vol.2의 Book III → 하나의 Book III로 처리
    all_chapters = chapters_v1 + chapters_v2  # 중복 제거 불필요 (챕터 번호가 다름)

    # 파일 번호 순차 부여
    file_num = 0
    chapters_meta = []
    book_ch_counter: dict[str, int] = {}  # book_roman → 현재 챕터 순번

    for book_roman, ch_roman, body in all_chapters:
        book_num = roman_to_int(book_roman)
        ch_num = roman_to_int(ch_roman)
        book_ch_counter[book_roman] = book_ch_counter.get(book_roman, 0) + 1

        # 챕터 제목 구성
        ch_title = f"제{book_num}권 제{ch_num}장"

        parts = split_text_at_paragraph(body, MAX_CHAPTER_WORDS)
        suffix_labels = [""] if len(parts) == 1 else [f" (상)", f" (하)", f" (중)"]

        for part_idx, part_body in enumerate(parts):
            file_num += 1
            suffix = suffix_labels[part_idx] if part_idx < len(suffix_labels) else f" ({part_idx+1})"
            full_title = f"{ch_title}{suffix}"

            save_chapter(out_dir, file_num, full_title, part_body)
            chapters_meta.append({
                "num": file_num,
                "title": full_title,
                "file": f"ch{file_num:02d}.txt",
                "book": book_num,
                "chapter": ch_num,
            })

    meta = {**INSTITUTES_METADATA, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    print(f"  → 총 {file_num}개 파일 저장 완료 (원본 {len(all_chapters)}개 챕터)")


# ─────────────────────────────────────────────
# main
# ─────────────────────────────────────────────

def main():
    do_download = "--download" in sys.argv or len(sys.argv) == 1

    print("=== 도서 분할 시작 ===")

    # ── True Vine ──────────────────────────────
    true_vine_cache = Path("/tmp/true_vine_raw.txt")
    if do_download:
        raw = download(
            "https://ccel.org/ccel/m/murray/true_vine/cache/true_vine.txt",
            true_vine_cache,
        )
    else:
        if true_vine_cache.exists():
            raw = true_vine_cache.read_text(encoding="utf-8")
        else:
            raw = Path("/tmp/true_vine.txt").read_text(encoding="utf-8")
    split_true_vine(raw)

    # ── Calvin Institutes ──────────────────────
    vol1_cache = Path("/tmp/calvin_vol1.txt")
    vol2_cache = Path("/tmp/calvin_vol2.txt")

    if do_download:
        vol1 = download(
            "https://www.gutenberg.org/cache/epub/45001/pg45001.txt",
            vol1_cache,
        )
        vol2 = download(
            "https://www.gutenberg.org/cache/epub/64392/pg64392.txt",
            vol2_cache,
        )
    else:
        vol1 = vol1_cache.read_text(encoding="utf-8")
        vol2 = vol2_cache.read_text(encoding="utf-8")

    split_institutes(vol1, vol2)

    print("\n✓ 2권 분할 완료!")
    print("\n[건너뜀]")
    print("  my-utmost: 저작권 보호 중 (1963년 갱신, Oswald Chambers Publications)")
    print("  streams-in-desert: 접근 가능한 퍼블릭 도메인 텍스트 소스 없음")


if __name__ == "__main__":
    main()
