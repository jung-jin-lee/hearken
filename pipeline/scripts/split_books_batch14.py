#!/usr/bin/env python3
"""14차 도서 9권 분할 스크립트 — 확장 카탈로그 1순위 (Gutenberg 소스).

대상:
  1. The Way to God (D.L. Moody) — Gutenberg #30449
  2. Secret Power (D.L. Moody) — Gutenberg #33341
  3. The Overcoming Life (D.L. Moody) — Gutenberg #33015
  4. Pleasure & Profit in Bible Study (D.L. Moody) — Gutenberg #36655
  5. Prevailing Prayer (D.L. Moody) — Gutenberg #61883
  6. Large Catechism (Martin Luther) — Gutenberg #1722
  7. Small Catechism (Martin Luther) — Gutenberg #1670
  8. Table Talk (Martin Luther) — Gutenberg #9841
  9. Corea: The Hermit Nation (W.E. Griffis) — Gutenberg #67141

사용법:
  python pipeline/scripts/split_books_batch14.py [--download]
"""

import json
import re
import sys
from pathlib import Path

BOOKS_DIR = Path("pipeline/sources/data/books")
CACHE_DIR = Path("/private/tmp/claude-501")
MAX_CHAPTER_WORDS = 8000

GUTENBERG_BASE = "https://www.gutenberg.org/cache/epub"


# ─────────────────────────────────────────────
# 공통 유틸리티
# ─────────────────────────────────────────────

def _gutenberg_url(ebook_id: int) -> str:
    return f"{GUTENBERG_BASE}/{ebook_id}/pg{ebook_id}.txt"


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
}


def _roman(s: str) -> int:
    return _ROMAN_MAP.get(s.upper().strip(), 0)


def _find_toc_end(text: str) -> int:
    """목차(CONTENTS/TABLE OF CONTENTS) 끝 위치를 찾는다.
    목차가 없으면 0을 반환."""
    toc_match = re.search(r"\n\s*(?:TABLE\s+OF\s+)?CONTENTS\.?\s*\n", text, re.IGNORECASE)
    if not toc_match:
        return 0
    # TOC 이후 빈 줄이 연속 2개 이상 나오면 본문 시작
    after_toc = text[toc_match.end():]
    body_start = re.search(r"\n\n\n", after_toc)
    if body_start:
        return toc_match.end() + body_start.end()
    # 폴백: TOC 시작 + 3000자
    return toc_match.start() + 3000


def _split_by_chapter_roman(text: str, pattern: str = r"\n\s*CHAPTER\s+([IVXLC]+)\.?\s*\n",
                             skip_toc: bool = True, min_words: int = 50):
    """범용: 로마 숫자 CHAPTER 마커로 분할.
    skip_toc=True면 CHAPTER I 중복으로 TOC를 감지하여 건너뜀.
    min_words: 이 단어 수 미만인 챕터는 필터링."""
    pat = re.compile(pattern, re.IGNORECASE)
    all_matches = list(pat.finditer(text))
    if not all_matches:
        return []

    if skip_toc and len(all_matches) > 1:
        # CHAPTER I이 2번 이상 나타나면 TOC와 본문이 중복된 것
        ch1_matches = [m for m in all_matches if _roman(m.group(1)) == 1]
        if len(ch1_matches) >= 2:
            # 두 번째 CHAPTER I부터가 본문
            body_start = ch1_matches[1].start()
            all_matches = [m for m in all_matches if m.start() >= body_start]
        else:
            # TOC 끝 위치 찾기
            toc_end = _find_toc_end(text)
            if toc_end > 0:
                all_matches = [m for m in all_matches if m.start() >= toc_end]

    chapters = []
    for i, m in enumerate(all_matches):
        num = _roman(m.group(1))
        start = m.start()
        end = all_matches[i + 1].start() if i + 1 < len(all_matches) else len(text)
        body = text[start:end].strip()
        # 제목 추출: CHAPTER 행 다음 줄
        lines = body.split("\n", 5)
        title_line = ""
        for line in lines[1:4]:
            stripped = line.strip()
            if stripped and not re.match(r"CHAPTER\s+[IVXLC]", stripped, re.IGNORECASE):
                title_line = stripped.rstrip(".")
                break
        chapters.append((num, title_line, body))

    # min_words 미만인 챕터 필터링 (TOC 잔여물 제거)
    if min_words > 0:
        chapters = [(n, t, b) for n, t, b in chapters if len(b.split()) >= min_words]

    return chapters


# ─────────────────────────────────────────────
# 1. The Way to God — D.L. Moody
#    Gutenberg #30449, 9 chapters
# ─────────────────────────────────────────────

MOODY_WAY_META = {
    "slug": "moody-way-to-god",
    "title": "하나님께 가는 길",
    "title_original": "The Way to God and How to Find It",
    "author": "드와이트 무디 (D.L. Moody)",
    "author_original": "D.L. Moody",
    "year": "1884",
    "source": "https://www.gutenberg.org/ebooks/30449",
    "license": "public_domain",
    "note": "19세기 대부흥운동가 무디의 복음 입문서. 하나님의 사랑, 회개, 구원의 확신을 9장에 걸쳐 설명.",
}

MOODY_WAY_CHAPTERS = {
    1: "제1장: 지식을 초월하는 사랑 (Love that Passeth Knowledge)",
    2: "제2장: 천국으로 들어가는 관문 (The Gateway into the Kingdom)",
    3: "제3장: 두 부류의 사람 (The Two Classes)",
    4: "제4장: 권면의 말씀 (Words of Counsel)",
    5: "제5장: 신성한 구세주 (A Divine Saviour)",
    6: "제6장: 회개와 보상 (Repentance and Restitution)",
    7: "제7장: 구원의 확신 (Assurance of Salvation)",
    8: "제8장: 만유의 그리스도 (Christ All and in All)",
    9: "제9장: 배교 (Backsliding)",
}


def split_moody_way(raw: str) -> None:
    print("\n=== The Way to God (D.L. Moody) ===")
    text = clean_text(extract_gutenberg(raw))
    out_dir = BOOKS_DIR / "moody-way-to-god"
    chapters_meta = []

    chapters = _split_by_chapter_roman(text)
    if not chapters:
        print("  [경고] 챕터 마커를 찾을 수 없음. 전체 텍스트를 분할합니다.")
        parts = split_text_at_paragraph(text)
        for i, part in enumerate(parts, 1):
            title = f"제{i}장"
            save_chapter(out_dir, i, title, part)
            chapters_meta.append({"num": i, "title": title, "file": f"ch{i:02d}.txt"})
    else:
        for num, _title_line, body in chapters:
            title = MOODY_WAY_CHAPTERS.get(num, f"제{num}장")
            parts = split_text_at_paragraph(body)
            for pi, part in enumerate(parts):
                file_num = len(chapters_meta) + 1
                suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
                ch_title = f"{title}{suffix}"
                save_chapter(out_dir, file_num, ch_title, part)
                chapters_meta.append({
                    "num": file_num, "title": ch_title, "file": f"ch{file_num:02d}.txt"
                })

    meta = {**MOODY_WAY_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    print(f"  총 {len(chapters_meta)}개 챕터 저장")


# ─────────────────────────────────────────────
# 2. Secret Power — D.L. Moody
#    Gutenberg #33341
# ─────────────────────────────────────────────

MOODY_SECRET_META = {
    "slug": "moody-secret-power",
    "title": "비밀의 능력",
    "title_original": "Secret Power; or, The Secret of Success in Christian Life and Work",
    "author": "드와이트 무디 (D.L. Moody)",
    "author_original": "D.L. Moody",
    "year": "1881",
    "source": "https://www.gutenberg.org/ebooks/33341",
    "license": "public_domain",
    "note": "무디가 성령의 인격과 사역에 관해 기술한 대표작. 성령의 능력의 원천과 증거에 대해 다룬다.",
}

MOODY_SECRET_CHAPTERS = {
    1: "제1장: 능력 — 그 원천 (Power: Its Source)",
    2: "제2장: '안에' 그리고 '위에' 있는 능력 (Power 'In' and 'Upon')",
    3: "제3장: 능력으로 증거하기 (Witnessing in Power)",
    4: "제4장: 능력으로 가르치기 (Teaching in Power)",
    5: "제5장: 능력으로 기도하기 (Praying in Power)",
    6: "제6장: 죽음을 주는 편지와 생명을 주는 영 (The Letter and the Spirit)",
    7: "제7장: 성령의 열매 (The Fruit of the Spirit)",
}


def split_moody_secret(raw: str) -> None:
    print("\n=== Secret Power (D.L. Moody) ===")
    text = clean_text(extract_gutenberg(raw))
    out_dir = BOOKS_DIR / "moody-secret-power"
    chapters_meta = []

    chapters = _split_by_chapter_roman(text)
    for num, _title_line, body in chapters:
        title = MOODY_SECRET_CHAPTERS.get(num, f"제{num}장")
        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            file_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            ch_title = f"{title}{suffix}"
            save_chapter(out_dir, file_num, ch_title, part)
            chapters_meta.append({
                "num": file_num, "title": ch_title, "file": f"ch{file_num:02d}.txt"
            })

    if not chapters_meta:
        # 챕터 마커가 없으면 전체 분할
        parts = split_text_at_paragraph(text)
        for i, part in enumerate(parts, 1):
            save_chapter(out_dir, i, f"제{i}장", part)
            chapters_meta.append({"num": i, "title": f"제{i}장", "file": f"ch{i:02d}.txt"})

    meta = {**MOODY_SECRET_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    print(f"  총 {len(chapters_meta)}개 챕터 저장")


# ─────────────────────────────────────────────
# 3. The Overcoming Life — D.L. Moody
#    Gutenberg #33015, 7 sermons
# ─────────────────────────────────────────────

MOODY_OVERCOMING_META = {
    "slug": "moody-overcoming-life",
    "title": "승리하는 삶",
    "title_original": "The Overcoming Life, and Other Sermons",
    "author": "드와이트 무디 (D.L. Moody)",
    "author_original": "D.L. Moody",
    "year": "1896",
    "source": "https://www.gutenberg.org/ebooks/33015",
    "license": "public_domain",
    "note": "무디의 대표 설교 모음집. 승리하는 삶, 참된 회개, 지혜, 겸손, 안식 등을 주제로 한 설교들.",
}

# 설교 제목 (ALL CAPS로 나타남)
OVERCOMING_SERMONS = [
    "THE OVERCOMING LIFE",
    "RESULTS OF TRUE REPENTANCE",
    "TRUE WISDOM",
    '"COME THOU AND ALL THY HOUSE INTO THE ARK"',
    "HUMILITY",
    "REST",
    'SEVEN "I WILLS" OF CHRIST',
    "WHAT THINK YE OF CHRIST?",
    "TO THE WORK",
]

OVERCOMING_KR = {
    "THE OVERCOMING LIFE": "승리하는 삶 (The Overcoming Life)",
    "RESULTS OF TRUE REPENTANCE": "참된 회개의 결과 (Results of True Repentance)",
    "TRUE WISDOM": "참된 지혜 (True Wisdom)",
    '"COME THOU AND ALL THY HOUSE INTO THE ARK"': "방주로 오라 (Come Thou into the Ark)",
    "HUMILITY": "겸손 (Humility)",
    "REST": "안식 (Rest)",
    'SEVEN "I WILLS" OF CHRIST': "그리스도의 일곱 '내가 하리라' (Seven 'I Wills' of Christ)",
    "WHAT THINK YE OF CHRIST?": "그리스도를 어떻게 생각하느냐 (What Think Ye of Christ?)",
    "TO THE WORK": "사역을 향하여 (To the Work)",
}


def split_moody_overcoming(raw: str) -> None:
    print("\n=== The Overcoming Life (D.L. Moody) ===")
    text = clean_text(extract_gutenberg(raw))
    out_dir = BOOKS_DIR / "moody-overcoming-life"
    chapters_meta = []

    # 설교 본문 제목은 마침표로 끝남 (예: "THE OVERCOMING LIFE.")
    # TOC 항목은 마침표 없음 (예: "THE OVERCOMING LIFE")
    # 마침표가 있는 매치를 우선, 없으면 내용이 충분한 매치 사용

    sermon_positions = []
    for title in OVERCOMING_SERMONS:
        escaped = re.escape(title)
        # 마침표가 있는 본문 제목 먼저 찾기
        pat_with_dot = re.compile(r"\n\s*" + escaped + r"\.\s*\n", re.IGNORECASE)
        pat_without_dot = re.compile(r"\n\s*" + escaped + r"\s*\n", re.IGNORECASE)

        matches_dot = list(pat_with_dot.finditer(text))
        if matches_dot:
            sermon_positions.append((matches_dot[0].start(), title))
        else:
            # 마침표 없는 매치 중, 내용이 충분한 것 선택
            matches_all = list(pat_without_dot.finditer(text))
            for j, m in enumerate(matches_all):
                next_m = matches_all[j + 1].start() if j + 1 < len(matches_all) else len(text)
                if len(text[m.start():next_m].split()) > 200:
                    sermon_positions.append((m.start(), title))
                    break

    sermon_positions.sort(key=lambda x: x[0])

    # 내용이 너무 짧은 항목 제거 (< 100 words)
    filtered = []
    for i, (pos, title) in enumerate(sermon_positions):
        next_pos = sermon_positions[i + 1][0] if i + 1 < len(sermon_positions) else len(text)
        body = text[pos:next_pos]
        if len(body.split()) > 100:
            filtered.append((pos, title))
    sermon_positions = filtered

    for i, (pos, title) in enumerate(sermon_positions):
        end = sermon_positions[i + 1][0] if i + 1 < len(sermon_positions) else len(text)
        body = text[pos:end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)

        kr_title = OVERCOMING_KR.get(title, title)
        ch_title = f"제{i+1}장: {kr_title}"

        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            file_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            ct = f"{ch_title}{suffix}"
            save_chapter(out_dir, file_num, ct, part)
            chapters_meta.append({"num": file_num, "title": ct, "file": f"ch{file_num:02d}.txt"})

    meta = {**MOODY_OVERCOMING_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    print(f"  총 {len(chapters_meta)}개 챕터 저장")


# ─────────────────────────────────────────────
# 4. Pleasure & Profit in Bible Study — D.L. Moody
#    Gutenberg #36655, 9 chapters
# ─────────────────────────────────────────────

MOODY_PLEASURE_META = {
    "slug": "moody-pleasure-profit",
    "title": "성경 공부의 기쁨과 유익",
    "title_original": "Pleasure & Profit in Bible Study",
    "author": "드와이트 무디 (D.L. Moody)",
    "author_original": "D.L. Moody",
    "year": "1895",
    "source": "https://www.gutenberg.org/ebooks/36655",
    "license": "public_domain",
    "note": "무디가 성경 공부의 방법과 기쁨에 관해 기술한 실용적인 안내서.",
}

MOODY_PLEASURE_CHAPTERS = {
    1: "제1장: 하나님의 말씀과의 긴밀한 접촉",
    2: "제2장: 의심과 탐구 — 증명과 영감",
    3: "제3장: 구약과 신약",
    4: "제4장: 내 말은 사라지지 않으리라",
    5: "제5장: 성취된 예언",
    6: "제6장: 본문 설교와 강해 설교",
    7: "제7장: 읽기와 연구하기",
    8: "제8장: 성경 공부법",
    9: "제9장: 망원경적 방법과 현미경적 방법",
}


def split_moody_pleasure(raw: str) -> None:
    print("\n=== Pleasure & Profit in Bible Study (D.L. Moody) ===")
    text = clean_text(extract_gutenberg(raw))
    out_dir = BOOKS_DIR / "moody-pleasure-profit"
    chapters_meta = []

    chapters = _split_by_chapter_roman(text)
    for num, _title_line, body in chapters:
        title = MOODY_PLEASURE_CHAPTERS.get(num, f"제{num}장")
        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            file_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            ch_title = f"{title}{suffix}"
            save_chapter(out_dir, file_num, ch_title, part)
            chapters_meta.append({
                "num": file_num, "title": ch_title, "file": f"ch{file_num:02d}.txt"
            })

    meta = {**MOODY_PLEASURE_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    print(f"  총 {len(chapters_meta)}개 챕터 저장")


# ─────────────────────────────────────────────
# 5. Prevailing Prayer — D.L. Moody
#    Gutenberg #61883, 11 chapters
# ─────────────────────────────────────────────

MOODY_PRAYER_META = {
    "slug": "moody-prevailing-prayer",
    "title": "승리하는 기도",
    "title_original": "Prevailing Prayer: What Hinders It?",
    "author": "드와이트 무디 (D.L. Moody)",
    "author_original": "D.L. Moody",
    "year": "1884",
    "source": "https://www.gutenberg.org/ebooks/61883",
    "license": "public_domain",
    "note": "기도의 9가지 필수 요소를 다루는 무디의 기도 안내서. 찬양, 고백, 감사, 용서, 믿음 등을 다룬다.",
}

MOODY_PRAYER_CHAPTERS = {
    1: "제1장: 성경의 기도들 (The Prayers of the Bible)",
    2: "제2장: 찬양 (Adoration)",
    3: "제3장: 고백 (Confession)",
    4: "제4장: 보상 (Restitution)",
    5: "제5장: 감사 (Thanksgiving)",
    6: "제6장: 용서 (Forgiveness)",
    7: "제7장: 하나됨 (Unity)",
    8: "제8장: 믿음 (Faith)",
    9: "제9장: 간구 (Petition)",
    10: "제10장: 복종 (Submission)",
    11: "제11장: 응답받은 기도들 (Answered Prayers)",
}


def split_moody_prayer(raw: str) -> None:
    print("\n=== Prevailing Prayer (D.L. Moody) ===")
    text = clean_text(extract_gutenberg(raw))
    out_dir = BOOKS_DIR / "moody-prevailing-prayer"
    chapters_meta = []

    chapters = _split_by_chapter_roman(text)
    for num, _title_line, body in chapters:
        title = MOODY_PRAYER_CHAPTERS.get(num, f"제{num}장")
        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            file_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            ch_title = f"{title}{suffix}"
            save_chapter(out_dir, file_num, ch_title, part)
            chapters_meta.append({
                "num": file_num, "title": ch_title, "file": f"ch{file_num:02d}.txt"
            })

    meta = {**MOODY_PRAYER_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    print(f"  총 {len(chapters_meta)}개 챕터 저장")


# ─────────────────────────────────────────────
# 6. Large Catechism — Martin Luther
#    Gutenberg #1722
# ─────────────────────────────────────────────

LUTHER_LARGE_META = {
    "slug": "luther-large-catechism",
    "title": "대교리문답",
    "title_original": "Martin Luther's Large Catechism",
    "author": "마르틴 루터 (Martin Luther)",
    "author_original": "Martin Luther",
    "year": "1529",
    "source": "https://www.gutenberg.org/ebooks/1722",
    "license": "public_domain",
    "translator": "Bente and Dau",
    "note": "루터의 교리교육 대작. 십계명, 사도신경, 주기도문, 세례, 성만찬을 체계적으로 해설한 교리문답서.",
}

# 대교리문답의 주요 섹션
LUTHER_LARGE_SECTIONS = [
    ("서문: 기독교인에게 유익한 서문", "PREFACE"),
    ("짧은 서문", "SHORT PREFACE"),
    ("제1부: 십계명 — 제1계명", "The First Commandment"),
    ("제1부: 십계명 — 제2계명", "The Second Commandment"),
    ("제1부: 십계명 — 제3계명", "The Third Commandment"),
    ("제1부: 십계명 — 제4계명", "The Fourth Commandment"),
    ("제1부: 십계명 — 제5계명", "The Fifth Commandment"),
    ("제1부: 십계명 — 제6계명", "The Sixth Commandment"),
    ("제1부: 십계명 — 제7계명", "The Seventh Commandment"),
    ("제1부: 십계명 — 제8계명", "The Eighth Commandment"),
    ("제1부: 십계명 — 제9-10계명", "The Ninth and Tenth Commandments"),
    ("제1부: 십계명 — 결론", "Conclusion of the Ten Commandments"),
    ("제2부: 사도신경 — 제1조항 (창조)", "The First Article"),
    ("제2부: 사도신경 — 제2조항 (구속)", "The Second Article"),
    ("제2부: 사도신경 — 제3조항 (성화)", "The Third Article"),
    ("제3부: 주기도문", "THE PRAYER"),
    ("제4부: 세례에 관하여", "OF BAPTISM"),
    ("제5부: 성만찬에 관하여", "OF THE SACRAMENT"),
]


def split_luther_large(raw: str) -> None:
    print("\n=== Large Catechism (Martin Luther) ===")
    text = clean_text(extract_gutenberg(raw))
    out_dir = BOOKS_DIR / "luther-large-catechism"
    chapters_meta = []

    # 대교리문답 구조 (Gutenberg #1722):
    #   서문 → 제1부(십계명, 개별 계명) → 제2부(사도신경, 3조항)
    #   → 제3부(주기도문) → 제4부(세례) → 제5부(성만찬) → 결론

    # 주요 마커 패턴들 (줄 시작에서 매칭)
    markers = [
        (r"^A Christian,\s+Profitable", "서문 (Preface)"),
        (r"^The First Commandment\.", "제1부: 십계명 — 제1계명"),
        (r"^The Second Commandment\.", "제1부: 십계명 — 제2계명"),
        (r"^The Third Commandment\.", "제1부: 십계명 — 제3계명"),
        (r"^The Fourth Commandment\.", "제1부: 십계명 — 제4계명"),
        (r"^The Fifth Commandment\.", "제1부: 십계명 — 제5계명"),
        (r"^The Sixth Commandment\.", "제1부: 십계명 — 제6계명"),
        (r"^The Seventh Commandment\.", "제1부: 십계명 — 제7계명"),
        (r"^The Eighth Commandment\.", "제1부: 십계명 — 제8계명"),
        (r"^The Ninth and Tenth Commandment", "제1부: 십계명 — 제9-10계명"),
        (r"^Part Second\.", "제2부: 사도신경 (The Creed)"),
        (r"^Part Third\.", "제3부: 주기도문 (The Lord's Prayer)"),
        (r"^Part Fourth\.", "제4부: 세례에 관하여 (Of Baptism)"),
        (r"^OF THE SACRAMENT OF THE ALTAR", "제5부: 성만찬에 관하여 (Of the Sacrament)"),
        (r"^Conclusion", "결론 (Conclusion)"),
    ]

    section_positions = []
    for pattern, title in markers:
        m = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
        if m:
            section_positions.append((m.start(), title))

    section_positions.sort(key=lambda x: x[0])

    # 서문과 본문 사이의 요약 섹션 건너뛰기
    # "The First Commandment."이 두 번 나타날 수 있음 (요약 + 상세)
    # 상세 버전은 더 뒤에 있고 내용이 더 김
    # 중복 제거: 같은 제목이 두 번 나오면 내용이 더 긴 것만 유지
    deduped = {}
    for pos, title in section_positions:
        if title in deduped:
            # 이미 있으면 더 늦은 위치(상세 버전)로 대체
            deduped[title] = max(deduped[title], pos)
        else:
            deduped[title] = pos
    section_positions = sorted(deduped.items(), key=lambda x: x[1])
    # (title, pos) → (pos, title)
    section_positions = [(pos, title) for title, pos in section_positions]

    for i, (pos, title) in enumerate(section_positions):
        end = section_positions[i + 1][0] if i + 1 < len(section_positions) else len(text)
        body = text[pos:end].strip()
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

    meta = {**LUTHER_LARGE_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    print(f"  총 {len(chapters_meta)}개 챕터 저장")


# ─────────────────────────────────────────────
# 7. Small Catechism — Martin Luther
#    Gutenberg #1670
# ─────────────────────────────────────────────

LUTHER_SMALL_META = {
    "slug": "luther-small-catechism",
    "title": "소교리문답",
    "title_original": "Luther's Little Instruction Book: The Small Catechism of Martin Luther",
    "author": "마르틴 루터 (Martin Luther)",
    "author_original": "Martin Luther",
    "year": "1529",
    "source": "https://www.gutenberg.org/ebooks/1670",
    "license": "public_domain",
    "note": "루터의 소교리문답. 가정과 교회에서의 교리교육을 위한 간결한 안내서. 십계명, 사도신경, 주기도문, 성례에 대한 핵심 교리.",
}

def split_luther_small(raw: str) -> None:
    print("\n=== Small Catechism (Martin Luther) ===")
    text = clean_text(extract_gutenberg(raw))
    out_dir = BOOKS_DIR / "luther-small-catechism"
    chapters_meta = []

    # 소교리문답은 "I. The Ten Commandments", "II. The Creed" 등으로 구분
    section_pat = re.compile(
        r"\n\s*(I{1,3}V?I{0,3})\.\s+(The\s+[A-Z].*?)$",
        re.MULTILINE,
    )
    matches = list(section_pat.finditer(text))

    if not matches:
        # 폴백: "The Xth Commandment" / "The Creed" 등의 대제목 패턴
        alt_pat = re.compile(
            r"\n\s*((?:I|II|III|IV|V|VI|VII)\.\s+.*?)$",
            re.MULTILINE,
        )
        matches = list(alt_pat.finditer(text))

    section_names = {
        "I": "제1부: 십계명 (The Ten Commandments)",
        "II": "제2부: 사도신경 (The Creed)",
        "III": "제3부: 주기도문 (The Lord's Prayer)",
        "IV": "제4부: 세례 성례 (The Sacrament of Holy Baptism)",
        "V": "제5부: 고백 (Confession)",
        "VI": "제6부: 성만찬 성례 (The Sacrament of the Altar)",
        "VII": "부록: 조석 기도와 의무의 표 (Daily Prayers & Table of Duties)",
    }

    if matches:
        for i, m in enumerate(matches):
            start = m.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            body = text[start:end].strip()
            body = re.sub(r"\n{3,}", "\n\n", body)

            roman = m.group(1) if m.lastindex and m.lastindex >= 1 else str(i + 1)
            title = section_names.get(roman, f"제{i+1}부: {m.group(0).strip()}")

            parts = split_text_at_paragraph(body)
            for pi, part in enumerate(parts):
                file_num = len(chapters_meta) + 1
                suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
                ch_title = f"{title}{suffix}"
                save_chapter(out_dir, file_num, ch_title, part)
                chapters_meta.append({
                    "num": file_num, "title": ch_title, "file": f"ch{file_num:02d}.txt"
                })
    else:
        # 최종 폴백: 전체를 분할
        parts = split_text_at_paragraph(text)
        for i, part in enumerate(parts, 1):
            save_chapter(out_dir, i, f"제{i}부", part)
            chapters_meta.append({"num": i, "title": f"제{i}부", "file": f"ch{i:02d}.txt"})

    meta = {**LUTHER_SMALL_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    print(f"  총 {len(chapters_meta)}개 챕터 저장")


# ─────────────────────────────────────────────
# 8. Table Talk — Martin Luther
#    Gutenberg #9841, selections
# ─────────────────────────────────────────────

LUTHER_TABLE_META = {
    "slug": "luther-table-talk",
    "title": "탁상담화 (선집)",
    "title_original": "Selections from the Table Talk of Martin Luther",
    "author": "마르틴 루터 (Martin Luther)",
    "author_original": "Martin Luther",
    "year": "~1566",
    "source": "https://www.gutenberg.org/ebooks/9841",
    "license": "public_domain",
    "note": "루터의 식탁에서 나눈 대화를 제자들이 기록한 것. 신학, 삶, 교회에 대한 루터의 생생한 견해를 담고 있다.",
}

# Table Talk는 주제별로 구분됨 — 로마 숫자 또는 제목
TABLE_TALK_TOPICS = {
    "OF GOD": "하나님에 관하여",
    "OF GOD'S WORD": "하나님의 말씀에 관하여",
    "OF GOD\u2019S WORD": "하나님의 말씀에 관하여",
    "OF GOD'S WORKS": "하나님의 역사에 관하여",
    "OF GOD\u2019S WORKS": "하나님의 역사에 관하여",
    "OF JESUS CHRIST": "예수 그리스도에 관하여",
    "OF THE HOLY GHOST": "성령에 관하여",
    "OF THE CREATION": "창조에 관하여",
    "OF ANGELS": "천사에 관하여",
    "OF DEVILS": "마귀에 관하여",
    "OF THE LAW": "율법에 관하여",
    "OF THE GOSPEL": "복음에 관하여",
    "OF BAPTISM": "세례에 관하여",
    "OF THE LORD'S SUPPER": "성만찬에 관하여",
    "OF THE LORD\u2019S SUPPER": "성만찬에 관하여",
    "OF THE CHURCH": "교회에 관하여",
    "OF PREACHERS AND PREACHING": "설교자와 설교에 관하여",
    "OF PRAYER": "기도에 관하여",
    "OF FAITH": "믿음에 관하여",
    "OF REPENTANCE": "회개에 관하여",
    "OF SIN": "죄에 관하여",
    "OF SINS AND OF FREE-WILL": "죄와 자유의지에 관하여",
    "OF THE NATURE OF THE WORLD": "세상의 본성에 관하여",
    "OF THE LORD CHRIST": "주 그리스도에 관하여",
    "OF THE CATECHISM": "교리문답에 관하여",
    "OF THE LAW AND THE GOSPEL": "율법과 복음에 관하여",
    "OF THE CONFESSION AND CONSTANCY OF THE DOCTRINE": "교리의 고백과 견고함에 관하여",
    "OF IMPERIAL DIETS": "제국 의회에 관하여",
    "OF DEATH": "죽음에 관하여",
    "OF MARRIAGE": "결혼에 관하여",
    "OF MUSIC": "음악에 관하여",
}


def split_luther_table(raw: str) -> None:
    print("\n=== Table Talk (Martin Luther) ===")
    text = clean_text(extract_gutenberg(raw))
    out_dir = BOOKS_DIR / "luther-table-talk"
    chapters_meta = []

    # Table Talk는 줄 시작에 "OF GOD'S WORD." 등의 주제별 마커 사용
    # 패턴: 줄 시작에 "OF " + ALL CAPS 제목 + 마침표
    # 유니코드 아포스트로피(\u2019) 포함
    of_pat = re.compile(r"^(OF\s+[A-Z][A-Z\s'.\u2018\u2019-]+?)\.?\s*$", re.MULTILINE)
    matches = list(of_pat.finditer(text))

    # INTRODUCTION 섹션도 포함
    intro_match = re.search(r"^INTRODUCTION\.?\s*$", text, re.MULTILINE)
    if intro_match:
        # 소개글을 첫 섹션으로
        first_of = matches[0].start() if matches else len(text)
        intro_body = text[intro_match.start():first_of].strip()
        if len(intro_body.split()) > 50:
            file_num = len(chapters_meta) + 1
            save_chapter(out_dir, file_num, "서문 (Introduction)", intro_body)
            chapters_meta.append({
                "num": file_num, "title": "서문 (Introduction)", "file": f"ch{file_num:02d}.txt"
            })

    for i, m in enumerate(matches):
        topic = m.group(1).strip()
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)

        kr = TABLE_TALK_TOPICS.get(topic, topic.title())
        file_num = len(chapters_meta) + 1
        title = f"제{file_num}장: {kr}"

        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            fn = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            ct = f"{title}{suffix}"
            save_chapter(out_dir, fn, ct, part)
            chapters_meta.append({
                "num": fn, "title": ct, "file": f"ch{fn:02d}.txt"
            })

    if not chapters_meta:
        # 최종 폴백: 문단 분할
        parts = split_text_at_paragraph(text)
        for i, part in enumerate(parts, 1):
            save_chapter(out_dir, i, f"제{i}장", part)
            chapters_meta.append({"num": i, "title": f"제{i}장", "file": f"ch{i:02d}.txt"})

    meta = {**LUTHER_TABLE_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    print(f"  총 {len(chapters_meta)}개 챕터 저장")


# ─────────────────────────────────────────────
# 9. Corea: The Hermit Nation — W.E. Griffis
#    Gutenberg #67141
# ─────────────────────────────────────────────

GRIFFIS_META = {
    "slug": "griffis-hermit-nation",
    "title": "코리아: 은둔의 나라",
    "title_original": "Corea: The Hermit Nation",
    "author": "윌리엄 그리피스 (W.E. Griffis)",
    "author_original": "William Elliot Griffis",
    "year": "1882",
    "source": "https://www.gutenberg.org/ebooks/67141",
    "license": "public_domain",
    "note": "19세기 미국인이 본 한국의 역사와 문화. 한국 기독교 역사의 배경을 이해하는 데 중요한 자료.",
}


def split_griffis(raw: str) -> None:
    print("\n=== Corea: The Hermit Nation (W.E. Griffis) ===")
    text = clean_text(extract_gutenberg(raw))
    out_dir = BOOKS_DIR / "griffis-hermit-nation"
    chapters_meta = []

    # 로마숫자 40 이상 확장 (54챕터까지 — LIV)
    extra_roman = {
        "XLI": 41, "XLII": 42, "XLIII": 43, "XLIV": 44, "XLV": 45,
        "XLVI": 46, "XLVII": 47, "XLVIII": 48, "XLIX": 49, "L": 50,
        "LI": 51, "LII": 52, "LIII": 53, "LIV": 54,
    }
    _ROMAN_MAP.update(extra_roman)

    # Griffis는 "^CHAPTER I." + 다음줄에 제목 패턴
    # TOC 중복 방지를 위해 skip_toc=True 사용 + min_words 필터
    chapters = _split_by_chapter_roman(text, skip_toc=True, min_words=200)

    if not chapters:
        # skip_toc이 너무 공격적이었을 수 있음 — 재시도
        chapters = _split_by_chapter_roman(text, skip_toc=False)
        # 본문 챕터만 필터 (내용 100단어 이상)
        chapters = [(n, t, b) for n, t, b in chapters if len(b.split()) > 100]

    for num, title_line, body in chapters:
        title = f"제{num}장: {title_line}" if title_line else f"제{num}장"
        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            file_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            ch_title = f"{title}{suffix}"
            save_chapter(out_dir, file_num, ch_title, part)
            chapters_meta.append({
                "num": file_num, "title": ch_title, "file": f"ch{file_num:02d}.txt"
            })

    meta = {**GRIFFIS_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    print(f"  총 {len(chapters_meta)}개 챕터 저장")


# ─────────────────────────────────────────────
# 다운로드 설정
# ─────────────────────────────────────────────

DOWNLOADS = [
    (30449, "moody-way-to-god.txt", split_moody_way),
    (33341, "moody-secret-power.txt", split_moody_secret),
    (33015, "moody-overcoming-life.txt", split_moody_overcoming),
    (36655, "moody-pleasure-profit.txt", split_moody_pleasure),
    (61883, "moody-prevailing-prayer.txt", split_moody_prayer),
    (1722, "luther-large-catechism.txt", split_luther_large),
    (1670, "luther-small-catechism.txt", split_luther_small),
    (9841, "luther-table-talk.txt", split_luther_table),
    (67141, "griffis-hermit-nation.txt", split_griffis),
]


def main():
    do_download = "--download" in sys.argv

    for ebook_id, filename, split_fn in DOWNLOADS:
        cache_path = CACHE_DIR / filename
        url = _gutenberg_url(ebook_id)

        if do_download:
            raw = download(url, cache_path)
        elif cache_path.exists():
            raw = cache_path.read_text(encoding="utf-8")
        else:
            print(f"\n[건너뜀] {filename} — --download 플래그로 먼저 다운로드하세요")
            continue

        split_fn(raw)

    print("\n" + "=" * 60)
    print("14차 배치 처리 완료!")
    print("=" * 60)
    print("\n다음 단계:")
    for _, filename, _ in DOWNLOADS:
        slug = filename.replace(".txt", "")
        print(f"  python -m pipeline.scripts.run_book build {slug}")


if __name__ == "__main__":
    main()
