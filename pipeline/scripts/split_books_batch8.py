#!/usr/bin/env python3
"""8차 도서 5권 분할 스크립트 (Phase A).

대상:
  1. The Pursuit of God (A.W. 토저) — 10장
  2. Pensées (블레즈 파스칼) — 주제별 섹션
  3. The Everlasting Man (G.K. 체스터턴) — ~16장
  4. St. Francis of Assisi (G.K. 체스터턴) — 10장
  5. The Didache (미상) — 16장

소스:
  1: https://www.gutenberg.org/cache/epub/25141/pg25141.txt
  2: https://www.gutenberg.org/cache/epub/46921/pg46921.txt
  3: https://www.gutenberg.org/cache/epub/65688/pg65688.txt
  4: https://www.gutenberg.org/cache/epub/63084/pg63084.txt
  5: https://www.newadvent.org/fathers/0714.htm

사용법:
  python pipeline/scripts/split_books_batch8.py [--download]
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
# 공통 유틸리티
# ─────────────────────────────────────────────

def download(url: str, dest: Path) -> str:
    if dest.exists() and dest.stat().st_size > 500:
        print(f"  [캐시] {dest.name}")
        return dest.read_text(encoding="utf-8")
    print(f"  [다운로드] {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    # Try UTF-8, fallback to latin-1
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
# 1. The Pursuit of God — A.W. Tozer
# ─────────────────────────────────────────────

PURSUIT_META = {
    "slug": "pursuit-of-god",
    "title": "하나님을 추구함",
    "title_original": "The Pursuit of God",
    "author": "A.W. 토저 (A.W. Tozer)",
    "author_original": "A.W. Tozer",
    "year": "1948",
    "source": "https://www.gutenberg.org/ebooks/25141",
    "license": "public_domain",
    "note": "그리스도인의 내면적 삶과 하나님의 임재를 추구하는 영적 고전. 10장.",
}

PURSUIT_TITLES = {
    1: ("Following Hard after God", "하나님을 열렬히 추구함"),
    2: ("The Blessedness of Possessing Nothing", "아무것도 소유하지 않는 복"),
    3: ("Removing the Veil", "휘장을 벗김"),
    4: ("Apprehending God", "하나님을 깨달음"),
    5: ("The Universal Presence", "편재하시는 하나님"),
    6: ("The Speaking Voice", "말씀하시는 음성"),
    7: ("The Gaze of the Soul", "영혼의 응시"),
    8: ("Restoring the Creator-creature Relation", "창조주와 피조물의 관계 회복"),
    9: ("Meekness and Rest", "온유와 안식"),
    10: ("The Sacrament of Living", "삶의 성례"),
}


def split_pursuit(raw: str) -> None:
    print("\n=== The Pursuit of God (A.W. Tozer) ===")
    text = extract_gutenberg(raw)
    text = clean_text(text)
    out_dir = BOOKS_DIR / "pursuit-of-god"

    # 이 판본에서 챕터 제목은 _이탤릭_ 형식: "_Following Hard after God_"
    chapters_meta = []
    title_positions = []
    for ch_num in sorted(PURSUIT_TITLES.keys()):
        en, kr = PURSUIT_TITLES[ch_num]
        escaped = re.escape(en)
        pat = re.compile(r"\n\s*_?" + escaped + r"_?\s*\n", re.IGNORECASE)
        m = pat.search(text)
        if m:
            title_positions.append((m.start(), m.end(), ch_num, en, kr))

    title_positions.sort(key=lambda x: x[0])

    for idx, (pos, end_pos, ch_num, en, kr) in enumerate(title_positions):
        start = end_pos
        end = title_positions[idx + 1][0] if idx + 1 < len(title_positions) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)

        title = f"{kr} ({en})"
        save_chapter(out_dir, ch_num, title, body)
        chapters_meta.append({"num": ch_num, "title": title, "file": f"ch{ch_num:02d}.txt"})

    meta = {**PURSUIT_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 2. Pensées — Blaise Pascal
# ─────────────────────────────────────────────

PENSEES_META = {
    "slug": "pensees-pascal",
    "title": "팡세",
    "title_original": "The Thoughts of Blaise Pascal",
    "author": "블레즈 파스칼 (Blaise Pascal)",
    "author_original": "Blaise Pascal",
    "year": "1670",
    "source": "https://www.gutenberg.org/ebooks/46921",
    "license": "public_domain",
    "translator": "C. Kegan Paul",
    "note": "인간 조건과 기독교 변증에 관한 단편적 사색 모음. 사후 출판.",
}

# 주제별 섹션 키워드 (Gutenberg 46921 기준, ALL-CAPS/italic 제목들)
PENSEES_SECTIONS = [
    "GENERAL INTRODUCTION",
    "THE MISERY OF MAN WITHOUT GOD",
    "THE HAPPINESS OF MAN WITH GOD",
    "NOTES",
]


def split_pensees(raw: str) -> None:
    print("\n=== Pensées (Blaise Pascal) ===")
    text = extract_gutenberg(raw)
    text = clean_text(text)
    out_dir = BOOKS_DIR / "pensees-pascal"

    # 이 판본(C. Kegan Paul 번역)의 구조:
    # 대섹션: _THE MISERY OF MAN WITHOUT GOD_;  (이탤릭+세미콜론)
    # 소섹션: _MAN'S DISPROPORTION._  _DIVERSION._  등 (이탤릭+마침표, ALL-CAPS)
    # 전략: ALL-CAPS 소섹션 제목을 경계로 분할

    # 대섹션 경계 (이탤릭 마커 + 세미콜론으로 본문 구분, TOC 회피)
    main_sections = [
        ("_THE MISERY OF MAN WITHOUT GOD_;", "하나님 없는 인간의 비참"),
        ("_THE HAPPINESS OF MAN WITH GOD_;", "하나님과 함께하는 인간의 행복"),
    ]

    # 대섹션 시작/끝 위치 찾기 (세미콜론 포함으로 TOC와 구분)
    section_ranges: list[tuple[int, int, str]] = []
    for pattern, kr_name in main_sections:
        idx = text.find(pattern)
        if idx == -1:
            # 세미콜론 없이 재시도
            pattern_no_semi = pattern.rstrip(";")
            idx = text.rfind(pattern_no_semi)  # 마지막 출현 사용 (TOC 회피)
        if idx != -1:
            end_pos = idx + len(pattern)
            # 해당 줄 끝까지 건너뜀
            nl = text.find("\n", end_pos)
            if nl != -1:
                end_pos = nl + 1
            section_ranges.append((end_pos, 0, kr_name))

    # 끝 위치 할당
    for i in range(len(section_ranges)):
        if i + 1 < len(section_ranges):
            section_ranges[i] = (section_ranges[i][0], section_ranges[i + 1][0] - 200,
                                  section_ranges[i][2])
        else:
            section_ranges[i] = (section_ranges[i][0], len(text), section_ranges[i][2])

    # 소섹션 패턴: _ALL-CAPS TITLE._ 또는 _ALL-CAPS TITLE_ (단독 줄)
    sub_pat = re.compile(r"\n_([A-Z][A-Z\' ]{3,60})[\._]\s*_?\s*\n")

    chapters_meta = []
    ch_num = 0

    for sec_start, sec_end, kr_section in section_ranges:
        sec_body = text[sec_start:sec_end]
        sub_matches = list(sub_pat.finditer(sec_body))

        # 메타 헤더들 제외
        sub_matches = [
            s for s in sub_matches
            if s.group(1).strip() not in {
                "OR", "PREFACE", "PREFACE TO THE FIRST PART",
                "PREFACE TO THE SECOND PART", "NOTES",
                "THAT NATURE IS NATURALLY CORRUPT",
            }
            and len(s.group(1).strip()) > 5
        ]

        if sub_matches:
            for si, sub_m in enumerate(sub_matches):
                sub_title_raw = sub_m.group(1).strip()
                sub_title = sub_title_raw.title()
                s_start = sub_m.end()
                s_end = sub_matches[si + 1].start() if si + 1 < len(sub_matches) else len(sec_body)
                body = sec_body[s_start:s_end].strip()
                if len(body.split()) < 80:
                    continue

                parts = split_text_at_paragraph(body)
                for pi, part in enumerate(parts):
                    ch_num += 1
                    suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
                    title = f"{kr_section} — {sub_title}{suffix}"
                    save_chapter(out_dir, ch_num, title, part)
                    chapters_meta.append({
                        "num": ch_num, "title": title,
                        "file": f"ch{ch_num:02d}.txt",
                    })
        else:
            # 소제목 없으면 8K 단위로 분할
            parts = split_text_at_paragraph(sec_body)
            for pi, part in enumerate(parts):
                ch_num += 1
                suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
                title = f"{kr_section}{suffix}"
                save_chapter(out_dir, ch_num, title, part)
                chapters_meta.append({
                    "num": ch_num, "title": title,
                    "file": f"ch{ch_num:02d}.txt",
                })

    meta = {**PENSEES_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 3. The Everlasting Man — G.K. Chesterton
# ─────────────────────────────────────────────

EVERLASTING_META = {
    "slug": "everlasting-man",
    "title": "영원한 인간",
    "title_original": "The Everlasting Man",
    "author": "G.K. 체스터턴 (G.K. Chesterton)",
    "author_original": "G.K. Chesterton",
    "year": "1925",
    "source": "https://www.gutenberg.org/ebooks/65688",
    "license": "public_domain",
    "note": "인류 역사와 그리스도교 신앙에 대한 변증서. H.G. 웰스의 '세계사 대계'에 대한 응답.",
}

# Part I 8장 + Part II 6장 + 서론 + 결론 + 부록2
EVERLASTING_CHAPTERS = {
    "INTRODUCTION": ("서론: 이 책의 계획", "Introduction: The Plan of This Book"),
    # Part I
    "THE MAN IN THE CAVE": ("제1부 1장: 동굴 속의 인간", "Part I Ch.1"),
    "PROFESSORS AND PREHISTORIC MEN": ("제1부 2장: 교수들과 선사시대 인간", "Part I Ch.2"),
    "THE ANTIQUITY OF CIVILISATION": ("제1부 3장: 문명의 고대성", "Part I Ch.3"),
    "GOD AND COMPARATIVE RELIGION": ("제1부 4장: 하나님과 비교종교", "Part I Ch.4"),
    "MAN AND MYTHOLOGIES": ("제1부 5장: 인간과 신화", "Part I Ch.5"),
    "THE DEMONS AND THE PHILOSOPHERS": ("제1부 6장: 악마들과 철학자들", "Part I Ch.6"),
    "THE WAR OF THE GODS AND DEMONS": ("제1부 7장: 신들과 악마들의 전쟁", "Part I Ch.7"),
    "THE END OF THE WORLD": ("제1부 8장: 세상의 끝", "Part I Ch.8"),
    # Part II
    "THE GOD IN THE CAVE": ("제2부 1장: 동굴 속의 하나님", "Part II Ch.1"),
    "THE RIDDLES OF THE GOSPEL": ("제2부 2장: 복음의 수수께끼", "Part II Ch.2"),
    "THE STRANGEST STORY IN THE WORLD": ("제2부 3장: 세상에서 가장 놀라운 이야기", "Part II Ch.3"),
    "THE WITNESS OF THE HERETICS": ("제2부 4장: 이단자들의 증언", "Part II Ch.4"),
    "THE ESCAPE FROM PAGANISM": ("제2부 5장: 이교로부터의 탈출", "Part II Ch.5"),
    "THE FIVE DEATHS OF THE FAITH": ("제2부 6장: 신앙의 다섯 번의 죽음", "Part II Ch.6"),
    "CONCLUSION": ("결론: 이 책의 요약", "Conclusion: The Summary of This Book"),
}


def split_everlasting(raw: str) -> None:
    print("\n=== The Everlasting Man (G.K. Chesterton) ===")
    text = extract_gutenberg(raw)
    text = clean_text(text)
    out_dir = BOOKS_DIR / "everlasting-man"

    # 이 판본 구조: "CHAPTER I\n\nTHE MAN IN THE CAVE\n\n본문..."
    # INTRODUCTION과 CONCLUSION은 "CHAPTER" 없이 바로 제목

    # 챕터 경계: "CHAPTER" + 로마숫자 줄 다음에 제목 줄
    ch_pat = re.compile(r"\nCHAPTER\s+([IVXLC]+)\s*\n", re.MULTILINE)
    ch_matches = list(ch_pat.finditer(text))

    # INTRODUCTION, CONCLUSION 별도 탐색
    intro_pat = re.compile(r"\nINTRODUCTION\s*\n", re.MULTILINE)
    concl_pat = re.compile(r"\nCONCLUSION\s*\n", re.MULTILINE)

    # 모든 경계 수집: (position, title_key_or_none)
    boundaries: list[tuple[int, int, str]] = []  # (start_of_heading, start_of_body, kr_title)

    # INTRODUCTION 찾기 (TOC가 아닌 본문)
    for m in intro_pat.finditer(text):
        # TOC 판별: 근처에 숫자가 있으면 TOC
        context = text[m.start():m.start()+200]
        if re.search(r"\d{2,}", context) and "PART" not in context[:50]:
            continue  # TOC 항목
        boundaries.append((m.start(), m.end(), "서론: 이 책의 계획"))
        break  # 첫 본문 INTRODUCTION만

    # PART I / PART II 경계 추적
    current_part = 0
    part_boundaries = []
    for m in re.finditer(r"\nPART\s+(I{1,2})\s*\n", text):
        part_num = 1 if m.group(1) == "I" else 2
        part_boundaries.append((m.start(), part_num))

    def get_part(pos: int) -> int:
        p = 0
        for bp, bn in part_boundaries:
            if bp < pos:
                p = bn
        return p

    # CHAPTER 경계
    ch_title_map_p1 = {
        1: "동굴 속의 인간", 2: "교수들과 선사시대 인간",
        3: "문명의 고대성", 4: "하나님과 비교종교",
        5: "인간과 신화", 6: "악마들과 철학자들",
        7: "신들과 악마들의 전쟁", 8: "세상의 끝",
    }
    ch_title_map_p2 = {
        1: "동굴 속의 하나님", 2: "복음의 수수께끼",
        3: "세상에서 가장 놀라운 이야기", 4: "이단자들의 증언",
        5: "이교로부터의 탈출", 6: "신앙의 다섯 번의 죽음",
    }

    for m in ch_matches:
        ch_num = _roman(m.group(1))
        part = get_part(m.start())
        if part == 1:
            kr = ch_title_map_p1.get(ch_num, f"제{ch_num}장")
            kr_title = f"제1부 {ch_num}장: {kr}"
        elif part == 2:
            kr = ch_title_map_p2.get(ch_num, f"제{ch_num}장")
            kr_title = f"제2부 {ch_num}장: {kr}"
        else:
            kr_title = f"제{ch_num}장"
        # 본문 시작: CHAPTER 줄 이후의 제목 줄 이후
        after = text[m.end():m.end()+200]
        # 다음 비어있지 않은 줄 (제목)을 건너뜀
        title_end = m.end()
        for line in after.split("\n"):
            title_end += len(line) + 1
            if line.strip() and line.strip().isupper():
                break  # 제목 줄 건너뜀
        boundaries.append((m.start(), title_end, kr_title))

    # CONCLUSION 찾기
    for m in concl_pat.finditer(text):
        if m.start() > len(text) * 0.8:  # 파일 후반부의 것만
            boundaries.append((m.start(), m.end(), "결론: 이 책의 요약"))
            break

    boundaries.sort(key=lambda x: x[0])

    chapters_meta = []
    for idx, (heading_start, body_start, kr_title) in enumerate(boundaries):
        end = boundaries[idx + 1][0] if idx + 1 < len(boundaries) else len(text)
        body = text[body_start:end].strip()
        # Part 헤더, 부록 정리
        body = re.sub(r"^PART\s+(I{1,3}|IV|V)\b.*?\n", "", body, flags=re.MULTILINE)
        body = re.sub(r"^ON THE CREATURE.*?\n", "", body, flags=re.MULTILINE)
        body = re.sub(r"^ON THE MAN.*?\n", "", body, flags=re.MULTILINE)
        body = re.sub(r"\n{3,}", "\n\n", body)

        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            ch_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            title = f"{kr_title}{suffix}"
            save_chapter(out_dir, ch_num, title, part)
            chapters_meta.append({
                "num": ch_num, "title": title,
                "file": f"ch{ch_num:02d}.txt",
            })

    meta = {**EVERLASTING_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 4. St. Francis of Assisi — G.K. Chesterton
# ─────────────────────────────────────────────

FRANCIS_META = {
    "slug": "st-francis-assisi",
    "title": "아시시의 성 프란체스코",
    "title_original": "St. Francis of Assisi",
    "author": "G.K. 체스터턴 (G.K. Chesterton)",
    "author_original": "G.K. Chesterton",
    "year": "1923",
    "source": "https://www.gutenberg.org/ebooks/63084",
    "license": "public_domain",
    "note": "아시시의 성 프란체스코의 생애와 영성에 대한 체스터턴의 전기적 해석.",
}

FRANCIS_TITLES = {
    1: "성 프란체스코의 문제 (The Problem of St. Francis)",
    2: "성 프란체스코가 만난 세상 (The World St. Francis Found)",
    3: "전사 프란체스코 (Francis the Fighter)",
    4: "건축가 프란체스코 (Francis the Builder)",
    5: "하나님의 음유시인 (Le Jongleur de Dieu)",
    6: "작은 가난뱅이 (The Little Poor Man)",
    7: "세 수도회 (The Three Orders)",
    8: "그리스도의 거울 (The Mirror of Christ)",
    9: "기적과 죽음 (Miracles and Death)",
    10: "성 프란체스코의 유언 (The Testament of St. Francis)",
}


def split_francis(raw: str) -> None:
    print("\n=== St. Francis of Assisi (G.K. Chesterton) ===")
    text = extract_gutenberg(raw)
    text = clean_text(text)
    out_dir = BOOKS_DIR / "st-francis-assisi"

    # 이 판본: 본문 챕터는 "_Chapter I_" 형식 (이탤릭 마커)
    # TOC의 "CHAPTER I"(ALL-CAPS, 들여쓰기)와 구분
    pat = re.compile(r"\n\s*_Chapter\s+([IVXLC]+)_\s*\n", re.MULTILINE)
    matches = list(pat.finditer(text))

    chapters_meta = []
    for idx, m in enumerate(matches):
        ch_num = _roman(m.group(1))
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        # 이탤릭 부제목 줄 제거 (예: "_The Problem of St. Francis_")
        body = re.sub(r"^_[^_]+_\s*\n", "", body)
        body = re.sub(r"\n{3,}", "\n\n", body)

        title = FRANCIS_TITLES.get(ch_num, f"제{ch_num}장")
        parts = split_text_at_paragraph(body)
        for pi, part in enumerate(parts):
            file_num = len(chapters_meta) + 1
            suffix = f" ({pi+1}/{len(parts)})" if len(parts) > 1 else ""
            full_title = f"{title}{suffix}"
            save_chapter(out_dir, file_num, full_title, part)
            chapters_meta.append({
                "num": file_num, "title": full_title,
                "file": f"ch{file_num:02d}.txt",
            })

    meta = {**FRANCIS_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 5. The Didache — 초대교회 문서
# ─────────────────────────────────────────────

DIDACHE_META = {
    "slug": "didache",
    "title": "디다케",
    "title_original": "The Didache: The Teaching of the Twelve Apostles",
    "author": "미상",
    "author_original": "Unknown",
    "year": "c.100",
    "source": "https://www.newadvent.org/fathers/0714.htm",
    "license": "public_domain",
    "translator": "M.B. Riddle (Ante-Nicene Fathers)",
    "note": "초대교회 가장 오래된 교회 질서서 중 하나. 두 가지 길, 세례, 성찬, 예언자 등.",
}

DIDACHE_TITLES = {
    1: "두 가지 길: 첫째 계명 (The Two Ways; The First Commandment)",
    2: "둘째 계명: 중죄의 금지 (The Second Commandment: Gross Sin Forbidden)",
    3: "다른 죄들의 금지 (Other Sins Forbidden)",
    4: "여러 가지 계율 (Various Precepts)",
    5: "죽음의 길 (The Way of Death)",
    6: "거짓 교사와 우상 제물 (Against False Teachers, and Food Offered to Idols)",
    7: "세례에 관하여 (Concerning Baptism)",
    8: "금식과 기도에 관하여 (Concerning Fasting and Prayer)",
    9: "감사 — 성찬 (The Thanksgiving / Eucharist)",
    10: "영성체 후 기도 (Prayer After Communion)",
    11: "교사, 사도, 예언자에 관하여 (Concerning Teachers, Apostles, and Prophets)",
    12: "그리스도인의 접대 (Reception of Christians)",
    13: "예언자 부양 (Support of Prophets)",
    14: "주일 예배 (Christian Assembly on the Lord's Day)",
    15: "감독과 집사: 훈계 (Bishops and Deacons; Christian Reproof)",
    16: "깨어 있으라: 주의 오심 (Watchfulness; The Coming of the Lord)",
}


def split_didache(raw_html: str) -> None:
    print("\n=== The Didache ===")
    text = html_to_text(raw_html)
    text = clean_text(text)
    out_dir = BOOKS_DIR / "didache"

    # Chapter 패턴: "Chapter 1." or "Chapter I." 등
    pat = re.compile(r"\n\s*Chapter\s+(\d+|[IVXLC]+)\.?\s", re.IGNORECASE)
    matches = list(pat.finditer(text))

    chapters_meta = []
    for idx, m in enumerate(matches):
        grp = m.group(1)
        ch_num = int(grp) if grp.isdigit() else _roman(grp)
        start = m.start()  # 챕터 헤더부터 포함
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)

        title = DIDACHE_TITLES.get(ch_num, f"제{ch_num}장")
        save_chapter(out_dir, ch_num, title, body)
        chapters_meta.append({
            "num": ch_num, "title": title,
            "file": f"ch{ch_num:02d}.txt",
        })

    if not chapters_meta:
        # Fallback: "Chapter" 패턴이 없으면 전체를 하나로
        print("  [경고] 챕터 패턴 미발견, 전체를 하나의 파일로 저장")
        save_chapter(out_dir, 1, "디다케 전문", text)
        chapters_meta.append({"num": 1, "title": "디다케 전문", "file": "ch01.txt"})

    meta = {**DIDACHE_META, "chapters": chapters_meta}
    save_metadata(out_dir, meta)
    (out_dir / "raw.txt").write_text(raw_html, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 로마숫자 변환
# ─────────────────────────────────────────────

_ROMAN_MAP = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7,
    "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12, "XIII": 13,
    "XIV": 14, "XV": 15, "XVI": 16, "XVII": 17, "XVIII": 18,
    "XIX": 19, "XX": 20, "XXI": 21, "XXII": 22, "XXIII": 23,
    "XXIV": 24, "XXV": 25, "XXVI": 26, "XXVII": 27, "XXVIII": 28,
    "XXIX": 29, "XXX": 30, "XXXI": 31,
}


def _roman(s: str) -> int:
    return _ROMAN_MAP.get(s.upper().strip(), 0)


# ─────────────────────────────────────────────
# main
# ─────────────────────────────────────────────

URLS = {
    "pursuit": "https://www.gutenberg.org/cache/epub/25141/pg25141.txt",
    "pensees": "https://www.gutenberg.org/cache/epub/46921/pg46921.txt",
    "everlasting": "https://www.gutenberg.org/cache/epub/65688/pg65688.txt",
    "francis": "https://www.gutenberg.org/cache/epub/63084/pg63084.txt",
    "didache": "https://www.newadvent.org/fathers/0714.htm",
}


def main():
    do_download = "--download" in sys.argv or len(sys.argv) == 1
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    print("=== Phase A: 5권 도서 분할 시작 ===\n")

    # ── 1. Pursuit of God ──
    cache = CACHE_DIR / "pursuit_of_god.txt"
    if do_download:
        raw = download(URLS["pursuit"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_pursuit(raw)

    # ── 2. Pensées ──
    cache = CACHE_DIR / "pensees_pascal.txt"
    if do_download:
        raw = download(URLS["pensees"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_pensees(raw)

    # ── 3. The Everlasting Man ──
    cache = CACHE_DIR / "everlasting_man.txt"
    if do_download:
        raw = download(URLS["everlasting"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_everlasting(raw)

    # ── 4. St. Francis of Assisi ──
    cache = CACHE_DIR / "st_francis.txt"
    if do_download:
        raw = download(URLS["francis"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_francis(raw)

    # ── 5. The Didache ──
    cache = CACHE_DIR / "didache.htm"
    if do_download:
        raw = download(URLS["didache"], cache)
    else:
        raw = cache.read_text(encoding="utf-8")
    split_didache(raw)

    print("\n✅ Phase A: 5권 분할 완료!")


if __name__ == "__main__":
    main()
