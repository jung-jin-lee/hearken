#!/usr/bin/env python3
"""13차 도서 4권 분할 스크립트.

대상:
  11. Selected Homilies of John Chrysostom (크리소스톰 설교선집) — CCEL
  12. The Beatitudes (토마스 왓슨 팔복 강해) — CCEL
  13. The Dialogue (시에나의 카타리나) — CCEL
  14. The Passion of Perpetua and Felicity (페르페투아 수난기) — NewAdvent

소스:
  11: https://ccel.org/ccel/s/schaff/npnf109/cache/npnf109.txt
  12: https://ccel.org/ccel/w/watson/beatitudes/cache/beatitudes.txt
  13: https://ccel.org/ccel/c/catherine/dialog/cache/dialog.txt
  14: https://www.newadvent.org/fathers/0324.htm

사용법:
  python pipeline/scripts/split_books_batch13.py [--download]
"""

import json
import re
import sys
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


# ─────────────────────────────────────────────
# HTML 파싱 유틸리티 (batch8과 동일)
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


def _strip_ccel_header(text: str, first_marker_pos: int) -> str:
    """CCEL 텍스트에서 첫 번째 챕터 마커 이전의 머리말/메타데이터를 제거."""
    if first_marker_pos > 0:
        return text[first_marker_pos:]
    return text


# ─────────────────────────────────────────────
# 11. Selected Homilies of John Chrysostom
#     — CCEL NPNF1-09 (선집: ~15-20편)
# ─────────────────────────────────────────────

CHRYSOSTOM_META = {
    "slug": "chrysostom-homilies",
    "title": "요한 크리소스톰 설교선집",
    "title_original": "Selected Homilies of John Chrysostom",
    "author": "요한 크리소스톰 (John Chrysostom)",
    "author_original": "John Chrysostom",
    "year": "~400",
    "source": "https://ccel.org/ccel/schaff/npnf109",
    "license": "public_domain",
    "translator": "Philip Schaff (ed.)",
    "note": "동방교회의 위대한 설교자 '황금의 입' 크리소스톰의 대표 설교 선집. NPNF1-09 수록작 중 선별.",
}

# 선별할 설교/저작 목록 (NPNF1-09 수록 내용 기반)
# On the Priesthood: Books 1-6
# Homilies on the Statues: 선별 (21편 중 대표작)
# Other select homilies from the volume
SELECTED_HOMILIES = {
    # On the Priesthood (사제직론) — 6 Books
    "priesthood_1": "사제직론 제1권 (On the Priesthood, Book I)",
    "priesthood_2": "사제직론 제2권 (On the Priesthood, Book II)",
    "priesthood_3": "사제직론 제3권 (On the Priesthood, Book III)",
    "priesthood_4": "사제직론 제4권 (On the Priesthood, Book IV)",
    "priesthood_5": "사제직론 제5권 (On the Priesthood, Book V)",
    "priesthood_6": "사제직론 제6권 (On the Priesthood, Book VI)",
    # Homilies on the Statues (석상 설교) — 대표 선별
    "statues_1": "석상 설교 제1편 (Homily I on the Statues)",
    "statues_2": "석상 설교 제2편 (Homily II on the Statues)",
    "statues_3": "석상 설교 제3편 (Homily III on the Statues)",
    "statues_6": "석상 설교 제6편 (Homily VI on the Statues)",
    "statues_11": "석상 설교 제11편 (Homily XI on the Statues)",
    "statues_17": "석상 설교 제17편 (Homily XVII on the Statues)",
    "statues_21": "석상 설교 제21편 (Homily XXI on the Statues)",
    # Other homilies
    "eutropius_1": "에우트로피우스의 몰락에 관하여 (On Eutropius, Homily I)",
    "eutropius_2": "에우트로피우스의 몰락 제2편 (On Eutropius, Homily II)",
}

# 석상 설교 선별 번호 목록
_STATUES_SELECTED = {1, 2, 3, 6, 11, 17, 21}


def split_chrysostom(raw: str) -> None:
    print("\n=== Selected Homilies of John Chrysostom (NPNF1-09) ===")
    text = clean_text(raw)
    out_dir = BOOKS_DIR / "chrysostom-homilies"
    chapters_meta = []

    # ── On the Priesthood (사제직론) ──
    # 패턴: "BOOK I." ~ "BOOK VI." within the On the Priesthood section
    priesthood_start = None
    priesthood_end = None

    # 사제직론 시작 찾기: "ON THE PRIESTHOOD" or "TREATISE ON THE PRIESTHOOD"
    ps_match = re.search(
        r"\n\s*(TREATISE\s+)?ON\s+THE\s+PRIESTHOOD",
        text, re.IGNORECASE,
    )
    if ps_match:
        priesthood_start = ps_match.start()

    # 사제직론 다음 주요 섹션 찾기 (Homilies on the Statues 또는 다른 섹션)
    if priesthood_start is not None:
        # 석상 설교 시작점 찾기
        statues_match = re.search(
            r"\n\s*(?:THE\s+)?HOMILIES?\s+ON\s+THE\s+STATUES",
            text[priesthood_start + 100:], re.IGNORECASE,
        )
        if statues_match:
            priesthood_end = priesthood_start + 100 + statues_match.start()
        else:
            priesthood_end = len(text)

        priest_text = text[priesthood_start:priesthood_end]

        # Book 경계 찾기: "BOOK I.", "BOOK II." 등
        book_pat = re.compile(
            r"\n\s*Book\s+([IVXLC]+)\.?\s*\n",
            re.IGNORECASE,
        )
        book_matches = list(book_pat.finditer(priest_text))

        for idx, bm in enumerate(book_matches):
            book_num = _roman(bm.group(1))
            if book_num < 1 or book_num > 6:
                continue

            b_start = bm.start()
            b_end = (book_matches[idx + 1].start()
                     if idx + 1 < len(book_matches)
                     else len(priest_text))
            body = priest_text[b_start:b_end].strip()
            body = re.sub(r"\n{3,}", "\n\n", body)

            key = f"priesthood_{book_num}"
            title = SELECTED_HOMILIES.get(key, f"사제직론 제{book_num}권")

            parts = split_text_at_paragraph(body)
            for pi, part in enumerate(parts):
                file_num = len(chapters_meta) + 1
                suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
                ch_title = f"{title}{suffix}"
                save_chapter(out_dir, file_num, ch_title, part)
                chapters_meta.append({
                    "num": file_num, "title": ch_title,
                    "file": f"ch{file_num:02d}.txt",
                    "section": "On the Priesthood",
                })

    # ── Homilies on the Statues (석상 설교) ──
    statues_start = None
    statues_end = None

    sm = re.search(
        r"\n\s*(?:THE\s+)?HOMILIES?\s+ON\s+THE\s+STATUES",
        text, re.IGNORECASE,
    )
    if sm:
        statues_start = sm.start()

    if statues_start is not None:
        # 다음 주요 섹션 경계 찾기
        next_section = re.search(
            r"\n\s*(?:CONCERNING|TWO\s+HOMILIES|HOMILY\s+ON\s+THE\s+PASSAGE|"
            r"ON\s+EUTROPIUS|TREATISE\s+ON|LETTERS?\s+OF|LETTER\s+TO)",
            text[statues_start + 100:], re.IGNORECASE,
        )
        if next_section:
            statues_end = statues_start + 100 + next_section.start()
        else:
            statues_end = len(text)

        statues_text = text[statues_start:statues_end]

        # 개별 Homily 마커: "HOMILY I.", "HOMILY II." 등
        hom_pat = re.compile(
            r"\n\s*Homily\s+([IVXLC]+)\.?\s*\n",
            re.IGNORECASE,
        )
        hom_matches = list(hom_pat.finditer(statues_text))

        for idx, hm in enumerate(hom_matches):
            hom_num = _roman(hm.group(1))
            if hom_num not in _STATUES_SELECTED:
                continue

            h_start = hm.start()
            h_end = (hom_matches[idx + 1].start()
                     if idx + 1 < len(hom_matches)
                     else len(statues_text))
            body = statues_text[h_start:h_end].strip()
            body = re.sub(r"\n{3,}", "\n\n", body)

            key = f"statues_{hom_num}"
            title = SELECTED_HOMILIES.get(key, f"석상 설교 제{hom_num}편")

            parts = split_text_at_paragraph(body)
            for pi, part in enumerate(parts):
                file_num = len(chapters_meta) + 1
                suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
                ch_title = f"{title}{suffix}"
                save_chapter(out_dir, file_num, ch_title, part)
                chapters_meta.append({
                    "num": file_num, "title": ch_title,
                    "file": f"ch{file_num:02d}.txt",
                    "section": "Homilies on the Statues",
                })

    # ── On Eutropius (에우트로피우스) ──
    eut_match = re.search(
        r"\n\s*(?:HOMILY\s+)?ON\s+EUTROPIUS",
        text, re.IGNORECASE,
    )
    if eut_match:
        eut_start = eut_match.start()
        eut_text_after = text[eut_start:]

        # Eutropius 내 Homily 마커 찾기
        eut_hom_pat = re.compile(
            r"\n\s*Homily\s+([IVXLC]+)\.?\s*\n",
            re.IGNORECASE,
        )
        eut_hom_matches = list(eut_hom_pat.finditer(eut_text_after))

        if eut_hom_matches:
            for idx, em in enumerate(eut_hom_matches[:2]):  # 최대 2편
                hom_num = _roman(em.group(1))
                h_start = em.start()
                h_end = (eut_hom_matches[idx + 1].start()
                         if idx + 1 < len(eut_hom_matches)
                         else min(len(eut_text_after), em.start() + 80000))
                body = eut_text_after[h_start:h_end].strip()
                body = re.sub(r"\n{3,}", "\n\n", body)

                key = f"eutropius_{hom_num}"
                title = SELECTED_HOMILIES.get(
                    key, f"에우트로피우스 제{hom_num}편 (On Eutropius)",
                )

                parts = split_text_at_paragraph(body)
                for pi, part in enumerate(parts):
                    file_num = len(chapters_meta) + 1
                    suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
                    ch_title = f"{title}{suffix}"
                    save_chapter(out_dir, file_num, ch_title, part)
                    chapters_meta.append({
                        "num": file_num, "title": ch_title,
                        "file": f"ch{file_num:02d}.txt",
                        "section": "On Eutropius",
                    })
        else:
            # Homily 마커 없이 전체를 하나로 처리
            # 다음 주요 섹션까지만 추출
            next_sec = re.search(
                r"\n\s*(?:LETTERS?\s+OF|LETTER\s+TO|INDEXES|INDEX)",
                eut_text_after[200:], re.IGNORECASE,
            )
            end_pos = 200 + next_sec.start() if next_sec else min(len(eut_text_after), 80000)
            body = eut_text_after[:end_pos].strip()
            body = re.sub(r"\n{3,}", "\n\n", body)

            title = SELECTED_HOMILIES["eutropius_1"]
            parts = split_text_at_paragraph(body)
            for pi, part in enumerate(parts):
                file_num = len(chapters_meta) + 1
                suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
                ch_title = f"{title}{suffix}"
                save_chapter(out_dir, file_num, ch_title, part)
                chapters_meta.append({
                    "num": file_num, "title": ch_title,
                    "file": f"ch{file_num:02d}.txt",
                    "section": "On Eutropius",
                })

    # 폴백: 아무것도 찾지 못한 경우 전체 텍스트에서 HOMILY 마커로 시도
    if not chapters_meta:
        print("  [주의] 섹션별 추출 실패, 전체 HOMILY 마커로 시도")
        hom_pat = re.compile(r"\n\s*Homily\s+([IVXLC]+)\.?\s*\n", re.IGNORECASE)
        all_matches = list(hom_pat.finditer(text))

        # 최대 20개 선별
        selected_indices = list(range(min(20, len(all_matches))))
        for sel_idx in selected_indices:
            m = all_matches[sel_idx]
            hom_num = _roman(m.group(1))
            start = m.start()
            end = (all_matches[sel_idx + 1].start()
                   if sel_idx + 1 < len(all_matches)
                   else len(text))
            body = text[start:end].strip()
            body = re.sub(r"\n{3,}", "\n\n", body)

            title = f"설교 제{hom_num}편 (Homily {m.group(1)})"
            parts = split_text_at_paragraph(body)
            for pi, part in enumerate(parts):
                file_num = len(chapters_meta) + 1
                suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
                ch_title = f"{title}{suffix}"
                save_chapter(out_dir, file_num, ch_title, part)
                chapters_meta.append({
                    "num": file_num, "title": ch_title,
                    "file": f"ch{file_num:02d}.txt",
                })

    meta = {**CHRYSOSTOM_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 12. The Beatitudes — Thomas Watson (CCEL)
# ─────────────────────────────────────────────

WATSON_META = {
    "slug": "watson-beatitudes",
    "title": "팔복 강해",
    "title_original": "The Beatitudes: An Exposition of Matthew 5:1-12",
    "author": "토마스 왓슨 (Thomas Watson)",
    "author_original": "Thomas Watson",
    "year": "1660",
    "source": "https://ccel.org/ccel/watson/beatitudes",
    "license": "public_domain",
    "note": "마태복음 5:1-12 산상수훈 팔복에 대한 청교도식 심층 강해.",
}

# 8 Beatitudes 한국어 제목
BEATITUDE_TITLES = {
    1: "심령이 가난한 자 (Blessed Are the Poor in Spirit)",
    2: "애통하는 자 (Blessed Are They That Mourn)",
    3: "온유한 자 (Blessed Are the Meek)",
    4: "의에 주리고 목마른 자 (Blessed Are They Which Do Hunger and Thirst)",
    5: "긍휼히 여기는 자 (Blessed Are the Merciful)",
    6: "마음이 청결한 자 (Blessed Are the Pure in Heart)",
    7: "화평하게 하는 자 (Blessed Are the Peacemakers)",
    8: "의를 위하여 박해를 받는 자 (Blessed Are They Which Are Persecuted)",
}


def split_watson_beatitudes(raw: str) -> None:
    print("\n=== The Beatitudes (Thomas Watson) ===")
    text = clean_text(raw)
    out_dir = BOOKS_DIR / "watson-beatitudes"

    chapters_meta = []

    # 여러 패턴으로 섹션 경계 탐색
    # 패턴 1: "BLESSED ARE THE..." (팔복 구문)
    blessed_pat = re.compile(
        r"\n\s*((?:THE\s+)?BEATITUDES?[:\.]?\s*(?:AN\s+EXPOSITION)?|"
        r"BLESSED\s+ARE\s+(?:THE\s+)?[A-Z][A-Z\s,;']+)",
        re.MULTILINE,
    )
    blessed_matches = list(blessed_pat.finditer(text))

    # 패턴 2: "Chapter" or "CHAPTER" 마커
    ch_pat = re.compile(
        r"\n\s*(?:CHAPTER|Chapter)\s+([IVXLC]+|\d+)\.?\s*\n",
        re.MULTILINE,
    )
    ch_matches = list(ch_pat.finditer(text))

    # 패턴 3: 섹션 번호 패턴 (CCEL 텍스트에서 자주 사용)
    sec_pat = re.compile(
        r"\n\s*(?:SECTION|Section)\s+([IVXLC]+|\d+)\.?\s*\n",
        re.MULTILINE,
    )
    sec_matches = list(sec_pat.finditer(text))

    # 패턴 4: 숫자+점+제목 ("I. ", "II. " 등 — 메인 분할)
    num_pat = re.compile(
        r"\n\s*([IVXLC]+)\.\s+([A-Z][A-Za-z\s,;'\-]+)\n",
    )
    num_matches = list(num_pat.finditer(text))

    # 가장 많은 매치를 사용 (우선순위: chapter > section > blessed > num)
    if len(ch_matches) >= 5:
        print(f"  패턴: CHAPTER 마커 {len(ch_matches)}개")
        # 첫 마커 이전 CCEL 헤더 제거
        text = _strip_ccel_header(text, ch_matches[0].start())
        ch_matches = list(ch_pat.finditer(text))

        for idx, m in enumerate(ch_matches):
            grp = m.group(1)
            ch_num = int(grp) if grp.isdigit() else _roman(grp)
            start = m.start()
            end = (ch_matches[idx + 1].start()
                   if idx + 1 < len(ch_matches)
                   else len(text))
            body = text[start:end].strip()
            body = re.sub(r"\n{3,}", "\n\n", body)

            # 팔복 번호와 매칭 시도 (대략적)
            beat_num = ch_num if ch_num <= 8 else None
            title = BEATITUDE_TITLES.get(beat_num, f"제{ch_num}장 (Chapter {grp})")

            parts = split_text_at_paragraph(body)
            for pi, part in enumerate(parts):
                file_num = len(chapters_meta) + 1
                suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
                ch_title = f"{title}{suffix}"
                save_chapter(out_dir, file_num, ch_title, part)
                chapters_meta.append({
                    "num": file_num, "title": ch_title,
                    "file": f"ch{file_num:02d}.txt",
                })

    elif len(sec_matches) >= 5:
        print(f"  패턴: SECTION 마커 {len(sec_matches)}개")
        text = _strip_ccel_header(text, sec_matches[0].start())
        sec_matches = list(sec_pat.finditer(text))

        for idx, m in enumerate(sec_matches):
            grp = m.group(1)
            sec_num = int(grp) if grp.isdigit() else _roman(grp)
            start = m.start()
            end = (sec_matches[idx + 1].start()
                   if idx + 1 < len(sec_matches)
                   else len(text))
            body = text[start:end].strip()
            body = re.sub(r"\n{3,}", "\n\n", body)

            title = f"제{sec_num}절 (Section {grp})"

            parts = split_text_at_paragraph(body)
            for pi, part in enumerate(parts):
                file_num = len(chapters_meta) + 1
                suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
                ch_title = f"{title}{suffix}"
                save_chapter(out_dir, file_num, ch_title, part)
                chapters_meta.append({
                    "num": file_num, "title": ch_title,
                    "file": f"ch{file_num:02d}.txt",
                })

    else:
        # 폴백: "Blessed" 키워드나 큰 빈 줄 경계로 분할
        print("  [폴백] 마커 부족, BLESSED 키워드 + 단락 기반 분할")
        # CCEL 헤더 휴리스틱 제거: 본문 시작 추정
        # "blessed" 첫 등장 또는 상위 2000자 이후
        first_blessed = re.search(
            r"(?:BLESSED|Blessed)\s+(?:are|is)\s+",
            text, re.IGNORECASE,
        )
        if first_blessed and first_blessed.start() > 200:
            text = text[max(0, first_blessed.start() - 200):]

        # BLESSED 구문으로 분할 시도
        bless_split = re.compile(
            r"\n\s*(?:\")?(?:BLESSED|Blessed)\s+(?:are|is)\s+",
            re.IGNORECASE,
        )
        bless_positions = list(bless_split.finditer(text))

        if len(bless_positions) >= 4:
            print(f"  BLESSED 키워드 {len(bless_positions)}개 발견")
            for idx, bp in enumerate(bless_positions):
                start = bp.start()
                end = (bless_positions[idx + 1].start()
                       if idx + 1 < len(bless_positions)
                       else len(text))
                body = text[start:end].strip()
                body = re.sub(r"\n{3,}", "\n\n", body)

                beat_num = idx + 1
                title = BEATITUDE_TITLES.get(
                    beat_num,
                    f"제{beat_num}복 강해 (Beatitude {beat_num})",
                )

                parts = split_text_at_paragraph(body)
                for pi, part in enumerate(parts):
                    file_num = len(chapters_meta) + 1
                    suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
                    ch_title = f"{title}{suffix}"
                    save_chapter(out_dir, file_num, ch_title, part)
                    chapters_meta.append({
                        "num": file_num, "title": ch_title,
                        "file": f"ch{file_num:02d}.txt",
                    })
        else:
            # 최종 폴백: 단락 기반 분할
            print("  [최종 폴백] 단락 기반 분할 수행")
            parts = split_text_at_paragraph(text)
            for pi, part in enumerate(parts):
                file_num = pi + 1
                title = f"Part {file_num}"
                save_chapter(out_dir, file_num, title, part)
                chapters_meta.append({
                    "num": file_num, "title": title,
                    "file": f"ch{file_num:02d}.txt",
                })

    meta = {**WATSON_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 13. The Dialogue — Catherine of Siena (CCEL)
# ─────────────────────────────────────────────

DIALOGUE_META = {
    "slug": "dialogue-catherine",
    "title": "대화",
    "title_original": "The Dialogue of St. Catherine of Siena",
    "author": "시에나의 카타리나 (Catherine of Siena)",
    "author_original": "Catherine of Siena",
    "year": "1370",
    "source": "https://ccel.org/ccel/catherine/dialog",
    "license": "public_domain",
    "note": "하나님과의 대화 형식으로 쓴 네 논고: 신적 섭리, 분별, 기도, 순종.",
}

# 4대 논고 한국어 제목
TREATISE_TITLES = {
    "DIVINE PROVIDENCE": "신적 섭리에 관한 논고 (A Treatise of Divine Providence)",
    "DISCRETION": "분별에 관한 논고 (A Treatise of Discretion)",
    "PRAYER": "기도에 관한 논고 (A Treatise of Prayer)",
    "OBEDIENCE": "순종에 관한 논고 (A Treatise of Obedience)",
}


def split_dialogue_catherine(raw: str) -> None:
    print("\n=== The Dialogue of St. Catherine of Siena ===")
    text = clean_text(raw)
    out_dir = BOOKS_DIR / "dialogue-catherine"

    chapters_meta = []

    # 1차: TREATISE 마커로 분할 (이 텍스트에는 CHAPTER 마커가 없음)
    treatise_pat = re.compile(
        r"\n(A\s+TREATISE\s+OF\s+\w[\w\s]+?)\.?\s*\n",
        re.IGNORECASE,
    )
    treatise_matches = list(treatise_pat.finditer(text))

    if treatise_matches:
        # CCEL 헤더 제거
        text = _strip_ccel_header(text, treatise_matches[0].start())
        treatise_matches = list(treatise_pat.finditer(text))

        print(f"  TREATISE 마커 {len(treatise_matches)}개 발견")
        for idx, tm in enumerate(treatise_matches):
            t_name = tm.group(1).strip().upper()
            t_start = tm.end()
            t_end = (treatise_matches[idx + 1].start()
                     if idx + 1 < len(treatise_matches)
                     else len(text))
            body = text[t_start:t_end].strip()
            body = re.sub(r"\n{3,}", "\n\n", body)

            # 한국어 논고 제목 매핑
            kr_title = t_name.title()
            for key, val in TREATISE_TITLES.items():
                if key in t_name:
                    kr_title = val
                    break

            parts = split_text_at_paragraph(body)
            for pi, part in enumerate(parts):
                file_num = len(chapters_meta) + 1
                suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
                ch_title = f"{kr_title}{suffix}"
                save_chapter(out_dir, file_num, ch_title, part)
                chapters_meta.append({
                    "num": file_num, "title": ch_title,
                    "file": f"ch{file_num:02d}.txt",
                    "treatise": t_name,
                })
    else:
        # 폴백: 단락 기반 분할
        print("  [주의] TREATISE 마커를 찾을 수 없어 단락 기반 분할 수행")
        parts = split_text_at_paragraph(text)
        for pi, part in enumerate(parts):
            file_num = pi + 1
            title = f"Part {file_num}"
            save_chapter(out_dir, file_num, title, part)
            chapters_meta.append({
                "num": file_num, "title": title,
                "file": f"ch{file_num:02d}.txt",
            })

    meta = {**DIALOGUE_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 14. The Passion of Perpetua and Felicity
#     — NewAdvent HTML
# ─────────────────────────────────────────────

PERPETUA_META = {
    "slug": "passion-of-perpetua",
    "title": "성녀 페르페투아와 펠리시타스의 수난기",
    "title_original": "The Passion of the Holy Martyrs Perpetua and Felicity",
    "author": "페르페투아 외 (Perpetua et al.)",
    "author_original": "Perpetua et al.",
    "year": "~203",
    "source": "https://www.newadvent.org/fathers/0324.htm",
    "license": "public_domain",
    "note": "초대교회 여성 순교자 페르페투아의 옥중 일기. 가장 오래된 기독교 여성 저술 중 하나.",
}


def split_perpetua(raw_html: str) -> None:
    print("\n=== The Passion of Perpetua and Felicity ===")
    text = html_to_text(raw_html)
    text = clean_text(text)
    out_dir = BOOKS_DIR / "passion-of-perpetua"

    chapters_meta = []

    # NewAdvent HTML → 변환 후 "Chapter N." 또는 "Preface." 형식
    # 패턴 1: "Chapter N." (h2 태그가 변환된 결과)
    sec_pat = re.compile(
        r"\n\s*((?:Preface|Chapter\s+\d+))\.\s+[A-Z]",
    )
    raw_matches = list(sec_pat.finditer(text))

    # 매칭된 섹션 정리
    valid_matches = []
    for m in raw_matches:
        label = m.group(1).strip()
        if label == "Preface":
            num = 0
        else:
            num_str = re.search(r"\d+", label)
            num = int(num_str.group()) if num_str else -1
        if num >= 0:
            valid_matches.append((num, m))

    # 중복 번호 제거 (첫 번째만 유지)
    seen = set()
    unique_matches = []
    for num, m in valid_matches:
        if num not in seen:
            seen.add(num)
            unique_matches.append((num, m))
    unique_matches.sort(key=lambda x: x[1].start())

    if len(unique_matches) >= 5:
        print(f"  섹션 마커 {len(unique_matches)}개 발견")

        # 인접 섹션들을 2-3개씩 그룹핑 → ~8-10개 파일
        group_size = max(2, len(unique_matches) // 8)  # 8-10개 파일 목표
        groups = []
        i = 0
        while i < len(unique_matches):
            group = unique_matches[i:i + group_size]
            groups.append(group)
            i += group_size

        for gidx, group in enumerate(groups):
            first_num = group[0][0]
            last_num = group[-1][0]
            first_match = group[0][1]

            # 그룹 본문 범위 설정
            g_start = first_match.start()
            # 다음 그룹의 시작이나 텍스트 끝까지
            if gidx + 1 < len(groups):
                g_end = groups[gidx + 1][0][1].start()
            else:
                g_end = len(text)

            body = text[g_start:g_end].strip()
            body = re.sub(r"\n{3,}", "\n\n", body)

            if len(body.split()) < 30:
                continue

            # 제목 생성
            if first_num == last_num:
                title = f"제{first_num}절 (Section {_to_roman(first_num)})"
            else:
                title = (
                    f"제{first_num}-{last_num}절"
                    f" (Sections {_to_roman(first_num)}-{_to_roman(last_num)})"
                )

            file_num = len(chapters_meta) + 1
            save_chapter(out_dir, file_num, title, body)
            chapters_meta.append({
                "num": file_num, "title": title,
                "file": f"ch{file_num:02d}.txt",
                "sections": list(range(first_num, last_num + 1)),
            })

    else:
        # 폴백: 단락 기반 분할 (짧은 텍스트이므로 적은 수의 파일)
        print("  [폴백] 섹션 마커 부족, 단락 기반 분할")
        parts = split_text_at_paragraph(text, max_words=3000)
        for pi, part in enumerate(parts):
            file_num = pi + 1
            title = f"Part {file_num}"
            save_chapter(out_dir, file_num, title, part)
            chapters_meta.append({
                "num": file_num, "title": title,
                "file": f"ch{file_num:02d}.txt",
            })

    meta = {**PERPETUA_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw_html, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


def _to_roman(n: int) -> str:
    """정수를 로마 숫자 문자열로 변환."""
    result = []
    for value, numeral in [
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    ]:
        while n >= value:
            result.append(numeral)
            n -= value
    return "".join(result)


# ─────────────────────────────────────────────
# main
# ─────────────────────────────────────────────

URLS = {
    "chrysostom": "https://ccel.org/ccel/s/schaff/npnf109/cache/npnf109.txt",
    "watson": "https://ccel.org/ccel/w/watson/beatitudes/cache/beatitudes.txt",
    "catherine": "https://ccel.org/ccel/c/catherine/dialog/cache/dialog.txt",
    "perpetua": "https://www.newadvent.org/fathers/0324.htm",
}


def main():
    do_download = "--download" in sys.argv or len(sys.argv) == 1
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    print("=== 13차: 4권 도서 분할 시작 ===\n")

    # ── 11. Selected Homilies of John Chrysostom ──
    cache = CACHE_DIR / "chrysostom_npnf109.txt"
    if do_download:
        raw = download(URLS["chrysostom"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_chrysostom(raw)

    # ── 12. The Beatitudes (Thomas Watson) ──
    cache = CACHE_DIR / "watson_beatitudes.txt"
    if do_download:
        raw = download(URLS["watson"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_watson_beatitudes(raw)

    # ── 13. The Dialogue (Catherine of Siena) ──
    cache = CACHE_DIR / "catherine_dialog.txt"
    if do_download:
        raw = download(URLS["catherine"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_dialogue_catherine(raw)

    # ── 14. The Passion of Perpetua and Felicity ──
    cache = CACHE_DIR / "perpetua.htm"
    if do_download:
        raw = download(URLS["perpetua"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_perpetua(raw)

    print("\n✅ 13차: 4권 분할 완료!")


if __name__ == "__main__":
    main()
