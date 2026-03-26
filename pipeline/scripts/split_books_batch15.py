#!/usr/bin/env python3
"""15차 도서 10권 분할 스크립트 — 확장 카탈로그 1순위 (CCEL 소스).

대상:
  1. All of Grace (Spurgeon) — CCEL grace
  2. The Cheque Book of the Bank of Faith (Spurgeon) — CCEL checkbook
  3. The Glory of Christ (John Owen) — CCEL glory
  4. On Temptation (John Owen) — CCEL temptation
  5. Indwelling Sin (John Owen) — CCEL indwellingsin
  6. Communion with God (John Owen) — CCEL communion
  7. Spiritual Mindedness (John Owen) — CCEL spirituallyminded
  8. Body of Divinity (Thomas Watson) — CCEL divinity
  9. The Ten Commandments (Thomas Watson) — CCEL commandments
  10. The Lord's Prayer (Thomas Watson) — CCEL prayer

사용법:
  python pipeline/scripts/split_books_batch15.py [--download]
"""

import json
import re
import sys
from pathlib import Path

BOOKS_DIR = Path("pipeline/sources/data/books")
CACHE_DIR = Path("/private/tmp/claude-501")
MAX_CHAPTER_WORDS = 8000

CCEL_BASE = "https://ccel.org/ccel"


# ─────────────────────────────────────────────
# 공통 유틸리티 (batch14와 동일)
# ─────────────────────────────────────────────

def _ccel_url(author: str, work: str) -> str:
    return f"{CCEL_BASE}/{author[0]}/{author}/{work}/cache/{work}.txt"


def download(url: str, dest: Path) -> str:
    import urllib.request
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


def _strip_ccel_header(text: str) -> str:
    """CCEL 텍스트 파일의 메타데이터/헤더를 제거."""
    # CCEL 텍스트는 보통 제목 + 저자 + 빈줄 후 본문
    # 또는 "Generated" 라인이 있음
    for marker in ["Generated on", "This document has been generated",
                     "This document is from", "This work is"]:
        idx = text.find(marker)
        if idx != -1 and idx < 2000:
            # 마커 이후의 다음 빈 줄부터 본문
            rest = text[idx:]
            nl = rest.find("\n\n")
            if nl != -1:
                text = rest[nl:].strip()
                break
    return text


def _split_ccel_by_chapter(text: str, chapter_pat: str = r"\n\s*CHAPTER\s+([IVXLC\d]+)\.?\s*\n",
                            min_words: int = 50) -> list[tuple]:
    """CCEL 텍스트를 챕터 마커로 분할. (num, title, body) 튜플 리스트 반환."""
    pat = re.compile(chapter_pat, re.IGNORECASE)
    matches = list(pat.finditer(text))
    if not matches:
        return []

    _ROMAN_MAP = {
        "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7,
        "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12, "XIII": 13,
        "XIV": 14, "XV": 15, "XVI": 16, "XVII": 17, "XVIII": 18,
        "XIX": 19, "XX": 20, "XXI": 21, "XXII": 22, "XXIII": 23,
        "XXIV": 24, "XXV": 25, "XXVI": 26, "XXVII": 27, "XXVIII": 28,
        "XXIX": 29, "XXX": 30,
    }

    chapters = []
    for i, m in enumerate(matches):
        raw_num = m.group(1).strip()
        num = _ROMAN_MAP.get(raw_num.upper(), 0)
        if num == 0:
            try:
                num = int(raw_num)
            except ValueError:
                num = i + 1
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()

        # 제목 추출
        lines = body.split("\n", 5)
        title_line = ""
        for line in lines[1:4]:
            stripped = line.strip()
            if stripped and len(stripped) > 3 and not re.match(r"(?:CHAPTER|BOOK)\s", stripped, re.IGNORECASE):
                title_line = stripped.rstrip(".")
                break

        if len(body.split()) >= min_words:
            chapters.append((num, title_line, body))

    return chapters


def _process_chapters(chapters: list, out_dir: Path, meta_base: dict,
                       title_map: dict = None) -> None:
    """챕터 리스트를 처리하여 파일 저장 및 metadata.json 생성."""
    chapters_meta = []

    for num, title_line, body in chapters:
        if title_map and num in title_map:
            title = title_map[num]
        elif title_line:
            title = f"제{num}장: {title_line}"
        else:
            title = f"제{num}장"

        body = re.sub(r"\n{3,}", "\n\n", body)
        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            file_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            ch_title = f"{title}{suffix}"
            save_chapter(out_dir, file_num, ch_title, part)
            chapters_meta.append({
                "num": file_num, "title": ch_title, "file": f"ch{file_num:02d}.txt"
            })

    meta = {**meta_base, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    print(f"  총 {len(chapters_meta)}개 챕터 저장")
    return chapters_meta


# ─────────────────────────────────────────────
# 1. All of Grace — C.H. Spurgeon
# ─────────────────────────────────────────────

def split_spurgeon_grace(raw: str) -> None:
    print("\n=== All of Grace (C.H. Spurgeon) ===")
    text = clean_text(_strip_ccel_header(raw))
    out_dir = BOOKS_DIR / "spurgeon-all-of-grace"

    chapters = _split_ccel_by_chapter(text)
    if not chapters:
        # 대안 패턴: 숫자 챕터 또는 섹션
        chapters = _split_ccel_by_chapter(text, r"\n\s*(\d+)\.\s+[A-Z]")

    if not chapters:
        # 전체 분할
        parts = split_text_at_paragraph(text)
        chapters = [(i+1, "", part) for i, part in enumerate(parts)]

    _process_chapters(chapters, out_dir, {
        "slug": "spurgeon-all-of-grace",
        "title": "값없는 은혜",
        "title_original": "All of Grace",
        "author": "찰스 스펄전 (C.H. Spurgeon)",
        "author_original": "C.H. Spurgeon",
        "year": "1886",
        "source": "https://ccel.org/ccel/spurgeon/grace",
        "license": "public_domain",
        "note": "스펄전이 구원의 은혜를 쉽고 명쾌하게 풀어쓴 복음 입문서. 구원의 확신에 관한 가장 사랑받는 기독교 고전 중 하나.",
    })


# ─────────────────────────────────────────────
# 2. Cheque Book of the Bank of Faith — Spurgeon
# ─────────────────────────────────────────────

def split_spurgeon_checkbook(raw: str) -> None:
    print("\n=== Cheque Book of the Bank of Faith (Spurgeon) ===")
    text = clean_text(_strip_ccel_header(raw))
    out_dir = BOOKS_DIR / "spurgeon-checkbook-bank"

    # 365일 묵상으로 월별 또는 날짜별 분할
    # CCEL 버전의 구조를 확인하여 적절히 분할
    # 보통 "JANUARY 1", "JANUARY 2" 등의 날짜 마커 사용

    # 월별 마커로 분할
    month_pat = re.compile(r"\n\s*(JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|"
                           r"JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)\s*\n",
                           re.IGNORECASE)
    months = list(month_pat.finditer(text))

    month_kr = {
        "JANUARY": "1월", "FEBRUARY": "2월", "MARCH": "3월",
        "APRIL": "4월", "MAY": "5월", "JUNE": "6월",
        "JULY": "7월", "AUGUST": "8월", "SEPTEMBER": "9월",
        "OCTOBER": "10월", "NOVEMBER": "11월", "DECEMBER": "12월",
    }

    chapters_list = []
    if months:
        for i, m in enumerate(months):
            start = m.start()
            end = months[i + 1].start() if i + 1 < len(months) else len(text)
            body = text[start:end].strip()
            month_name = m.group(1).upper()
            kr = month_kr.get(month_name, month_name)
            chapters_list.append((i + 1, "", body))
    else:
        # 월별 마커 없으면 CHAPTER 또는 전체 분할
        chapters_list_raw = _split_ccel_by_chapter(text)
        if chapters_list_raw:
            chapters_list = chapters_list_raw
        else:
            parts = split_text_at_paragraph(text)
            chapters_list = [(i+1, "", p) for i, p in enumerate(parts)]

    title_map = {}
    if months:
        for i, m in enumerate(months):
            month_name = m.group(1).upper()
            kr = month_kr.get(month_name, month_name)
            title_map[i + 1] = f"{kr}: 신앙의 은행 수표책 ({month_name.title()})"

    _process_chapters(chapters_list, out_dir, {
        "slug": "spurgeon-checkbook-bank",
        "title": "신앙의 은행 수표책",
        "title_original": "The Cheque Book of the Bank of Faith",
        "author": "찰스 스펄전 (C.H. Spurgeon)",
        "author_original": "C.H. Spurgeon",
        "year": "1888",
        "source": "https://ccel.org/ccel/spurgeon/checkbook",
        "license": "public_domain",
        "note": "스펄전의 365일 약속 묵상집. 매일 성경 약속 말씀 하나를 선정하고 그에 대한 묵상을 제공.",
    }, title_map)


# ─────────────────────────────────────────────
# 3-7. John Owen 5권
# ─────────────────────────────────────────────

OWEN_BOOKS = [
    {
        "slug": "owen-glory-christ",
        "title": "그리스도의 영광",
        "title_original": "The Glory of Christ",
        "ccel_work": "glory",
        "year": "1684",
        "note": "오웬의 마지막 대작. 그리스도의 신적 영광과 중보자로서의 영광을 묵상하는 경건 서적.",
    },
    {
        "slug": "owen-temptation",
        "title": "유혹에 관하여",
        "title_original": "On Temptation",
        "ccel_work": "temptation",
        "year": "1658",
        "note": "유혹의 본질과 그에 대한 방어 전략을 다룬 청교도 영성의 핵심 저작.",
    },
    {
        "slug": "owen-indwelling-sin",
        "title": "내주하는 죄",
        "title_original": "Indwelling Sin in Believers",
        "ccel_work": "indwellingsin",
        "year": "1668",
        "note": "신자 안에 남아있는 죄의 본성과 작용 방식을 분석한 깊은 영적 탐구서.",
    },
    {
        "slug": "owen-communion-god",
        "title": "하나님과의 교제",
        "title_original": "Of Communion with God the Father, Son and Holy Ghost",
        "ccel_work": "communion",
        "year": "1657",
        "note": "성부, 성자, 성령 각 위격과의 독특한 교제의 본질을 탐구한 삼위일체 영성서.",
    },
    {
        "slug": "owen-spiritual-mindedness",
        "title": "영적인 마음",
        "title_original": "The Grace and Duty of Being Spiritually Minded",
        "ccel_work": "spirituallyminded",
        "year": "1681",
        "note": "로마서 8:6을 기반으로 영적 사고방식의 본질과 실천을 다룬 저작.",
    },
]


def split_owen_book(raw: str, book_info: dict) -> None:
    slug = book_info["slug"]
    print(f"\n=== {book_info['title_original']} (John Owen) ===")
    text = clean_text(_strip_ccel_header(raw))
    out_dir = BOOKS_DIR / slug

    chapters = _split_ccel_by_chapter(text)
    if not chapters:
        # BOOK 패턴 시도
        chapters = _split_ccel_by_chapter(text, r"\n\s*BOOK\s+([IVXLC]+)\.?\s*\n")
    if not chapters:
        # 전체 분할
        parts = split_text_at_paragraph(text)
        chapters = [(i+1, "", part) for i, part in enumerate(parts)]

    _process_chapters(chapters, out_dir, {
        "slug": slug,
        "title": book_info["title"],
        "title_original": book_info["title_original"],
        "author": "존 오웬 (John Owen)",
        "author_original": "John Owen",
        "year": book_info["year"],
        "source": f"https://ccel.org/ccel/owen/{book_info['ccel_work']}",
        "license": "public_domain",
        "note": book_info["note"],
    })


# ─────────────────────────────────────────────
# 8-10. Thomas Watson 3권
# ─────────────────────────────────────────────

WATSON_BOOKS = [
    {
        "slug": "watson-body-divinity-v1",
        "title": "조직신학 제1권",
        "title_original": "A Body of Divinity",
        "ccel_work": "divinity",
        "year": "1692",
        "note": "웨스트민스터 소교리문답을 기반으로 한 왓슨의 체계적인 신학 해설서. 개혁신학의 핵심을 담고 있다.",
    },
    {
        "slug": "watson-ten-commandments",
        "title": "십계명 강해",
        "title_original": "The Ten Commandments",
        "ccel_work": "commandments",
        "year": "1692",
        "note": "십계명 각 계명을 상세히 풀어 설명한 청교도 윤리의 보고.",
    },
    {
        "slug": "watson-lords-prayer",
        "title": "주기도문 강해",
        "title_original": "The Lord's Prayer",
        "ccel_work": "prayer",
        "year": "1692",
        "note": "주기도문의 각 구절을 깊이 있게 해설한 기도의 안내서.",
    },
]


def split_watson_book(raw: str, book_info: dict) -> None:
    slug = book_info["slug"]
    print(f"\n=== {book_info['title_original']} (Thomas Watson) ===")
    text = clean_text(_strip_ccel_header(raw))
    out_dir = BOOKS_DIR / slug

    # Watson의 CCEL 텍스트는 보통 챕터/질문 번호로 구분
    chapters = _split_ccel_by_chapter(text)
    if not chapters:
        # "Question" 패턴 시도 (소교리문답 기반)
        chapters = _split_ccel_by_chapter(text, r"\n\s*(?:Question|Q\.?)\s+(\d+)\.?\s*\n")
    if not chapters:
        # 전체 분할
        parts = split_text_at_paragraph(text)
        chapters = [(i+1, "", part) for i, part in enumerate(parts)]

    # Body of Divinity는 너무 크므로 앞/뒤 반으로 나눔
    if slug == "watson-body-divinity-v1" and len(chapters) > 20:
        # 전반부만 v1으로
        mid = len(chapters) // 2
        chapters = chapters[:mid]

    _process_chapters(chapters, out_dir, {
        "slug": slug,
        "title": book_info["title"],
        "title_original": book_info["title_original"],
        "author": "토마스 왓슨 (Thomas Watson)",
        "author_original": "Thomas Watson",
        "year": book_info["year"],
        "source": f"https://ccel.org/ccel/watson/{book_info['ccel_work']}",
        "license": "public_domain",
        "note": book_info["note"],
    })


# ─────────────────────────────────────────────
# 다운로드 설정
# ─────────────────────────────────────────────

DOWNLOADS = [
    # (author, work, cache_filename, split_function)
    ("spurgeon", "grace", "spurgeon-grace.txt", lambda r: split_spurgeon_grace(r)),
    ("spurgeon", "checkbook", "spurgeon-checkbook.txt", lambda r: split_spurgeon_checkbook(r)),
]

# Owen 5권 추가
for ob in OWEN_BOOKS:
    DOWNLOADS.append((
        "owen", ob["ccel_work"], f"owen-{ob['ccel_work']}.txt",
        lambda r, info=ob: split_owen_book(r, info),
    ))

# Watson 3권 추가
for wb in WATSON_BOOKS:
    DOWNLOADS.append((
        "watson", wb["ccel_work"], f"watson-{wb['ccel_work']}.txt",
        lambda r, info=wb: split_watson_book(r, info),
    ))


def main():
    do_download = "--download" in sys.argv

    for author, work, filename, split_fn in DOWNLOADS:
        cache_path = CACHE_DIR / filename
        url = _ccel_url(author, work)

        if do_download:
            raw = download(url, cache_path)
        elif cache_path.exists():
            raw = cache_path.read_text(encoding="utf-8")
        else:
            print(f"\n[건너뜀] {filename} — --download 플래그로 먼저 다운로드하세요")
            continue

        split_fn(raw)

    print("\n" + "=" * 60)
    print("15차 배치 처리 완료!")
    print("=" * 60)
    print("\n다음 단계:")
    for _, _, filename, _ in DOWNLOADS:
        slug = filename.replace(".txt", "").replace("spurgeon-", "spurgeon-").replace("owen-", "owen-").replace("watson-", "watson-")
        # slug 이름 추출
        print(f"  python -m pipeline.scripts.run_book build <slug>")


if __name__ == "__main__":
    main()
