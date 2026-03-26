#!/usr/bin/env python3
"""16차 도서 7권 분할 — 종교개혁 신앙고백서/교리문답 (CCEL 소스).

대상:
  1. Heidelberg Catechism — CCEL anonymous/heidelberg
  2. Westminster Confession — CCEL anonymous/westminster1
  3. Westminster Larger Catechism — CCEL anonymous/westminster2
  4. Westminster Shorter Catechism — CCEL anonymous/westminster3
  5. Augsburg Confession — CCEL schaff/creeds1 (extract)
  6. Belgic Confession — CCEL schaff/creeds1 (extract)
  7. Canons of Dort — CCEL schaff/creeds1 (extract)

사용법:
  python pipeline/scripts/split_books_batch16.py [--download]
"""

import json, re, sys
from pathlib import Path

BOOKS_DIR = Path("pipeline/sources/data/books")
CACHE_DIR = Path("/private/tmp/claude-501")
MAX_CHAPTER_WORDS = 8000
CCEL_BASE = "https://ccel.org/ccel"


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
    text = data.decode("utf-8", errors="replace")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    return text

def clean(text): return re.sub(r"\n{4,}", "\n\n\n", re.sub(r"_{5,}", "", text)).strip()

def save_ch(out_dir, num, title, body):
    out_dir.mkdir(parents=True, exist_ok=True)
    f = f"ch{num:02d}.txt"
    (out_dir / f).write_text(f"{title}\n\n{body.strip()}\n", encoding="utf-8")
    print(f"  {f}: {title[:60]} ({len(body.split())} words)")

def save_meta(out_dir, meta):
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

def split_para(text, max_w=MAX_CHAPTER_WORDS):
    if len(text.split()) <= max_w: return [text]
    paras = [p for p in text.split("\n\n") if p.strip()]
    chunks, cur, cw = [], [], 0
    for p in paras:
        pw = len(p.split())
        if cw + pw > max_w and cur:
            chunks.append("\n\n".join(cur)); cur, cw = [], 0
        cur.append(p); cw += pw
    if cur: chunks.append("\n\n".join(cur))
    return chunks or [text]

def process(chapters, out_dir, meta_base, title_map=None):
    cm = []
    for num, tl, body in chapters:
        title = (title_map or {}).get(num, f"제{num}장: {tl}" if tl else f"제{num}장")
        body = re.sub(r"\n{3,}", "\n\n", body)
        for pi, part in enumerate(split_para(body)):
            fn = len(cm) + 1
            sfx = f" ({pi+1}/{len(split_para(body))})" if len(split_para(body)) > 1 else ""
            ct = f"{title}{sfx}"
            save_ch(out_dir, fn, ct, part)
            cm.append({"num": fn, "title": ct, "file": f"ch{fn:02d}.txt"})
    save_meta(out_dir, {**meta_base, "chapters": cm})
    print(f"  총 {len(cm)}개 챕터 저장")


# ─── 1. Heidelberg Catechism ───

def split_heidelberg(raw):
    print("\n=== Heidelberg Catechism ===")
    text = clean(raw)
    out_dir = BOOKS_DIR / "heidelberg-catechism"

    # "Lord's Day" 섹션으로 분할 (52 Lord's Days)
    ld_pat = re.compile(r"\n\s*(LORD.?S\s+DAY\s+(\d+))\s*\n", re.IGNORECASE)
    matches = list(ld_pat.finditer(text))

    chapters = []
    if matches:
        for i, m in enumerate(matches):
            num = int(m.group(2))
            start = m.start()
            end = matches[i+1].start() if i+1 < len(matches) else len(text)
            body = text[start:end].strip()
            if len(body.split()) >= 30:
                chapters.append((num, f"주일 {num} (Lord's Day {num})", body))
    else:
        # Question 패턴으로 시도
        q_pat = re.compile(r"\n\s*(Q(?:uestion)?\.?\s*(\d+))\s*", re.IGNORECASE)
        qm = list(q_pat.finditer(text))
        # 10문항씩 묶기
        group_size = 10
        for gi in range(0, len(qm), group_size):
            batch = qm[gi:gi+group_size]
            start = batch[0].start()
            end = qm[gi+group_size].start() if gi+group_size < len(qm) else len(text)
            body = text[start:end].strip()
            num = gi // group_size + 1
            q_start = int(batch[0].group(2))
            q_end = int(batch[-1].group(2))
            chapters.append((num, f"문답 {q_start}-{q_end}", body))

    if not chapters:
        parts = split_para(text)
        chapters = [(i+1, "", p) for i, p in enumerate(parts)]

    process(chapters, out_dir, {
        "slug": "heidelberg-catechism",
        "title": "하이델베르크 교리문답",
        "title_original": "Heidelberg Catechism",
        "author": "자카리아스 우르시누스, 카스파르 올레비아누스",
        "author_original": "Zacharias Ursinus & Caspar Olevianus",
        "year": "1563",
        "source": "https://ccel.org/ccel/anonymous/heidelberg",
        "license": "public_domain",
        "note": "개혁교회의 3대 신앙고백서 중 하나. 129문답을 52주일로 나누어 교리를 가르치는 형식.",
    })


# ─── 2. Westminster Confession ───

def split_westminster_conf(raw):
    print("\n=== Westminster Confession of Faith ===")
    text = clean(raw)
    out_dir = BOOKS_DIR / "westminster-confession"

    # CHAPTER I. ~ CHAPTER XXXIII. 패턴
    # 또는 "Chapter I." 소문자 혼합
    ch_pat = re.compile(r"\n\s*(?:CHAPTER|Chapter)\s+([IVXLC]+|\d+)[.:]?\s*\n", re.IGNORECASE)
    matches = list(ch_pat.finditer(text))

    # 대안: "I. Of ..." 형태
    if not matches:
        ch_pat = re.compile(r"\n\s*([IVXLC]+)\.\s+(?:Of|The)\s+", re.IGNORECASE)
        matches = list(ch_pat.finditer(text))

    _ROMAN = {"I":1,"II":2,"III":3,"IV":4,"V":5,"VI":6,"VII":7,"VIII":8,"IX":9,"X":10,
              "XI":11,"XII":12,"XIII":13,"XIV":14,"XV":15,"XVI":16,"XVII":17,"XVIII":18,
              "XIX":19,"XX":20,"XXI":21,"XXII":22,"XXIII":23,"XXIV":24,"XXV":25,
              "XXVI":26,"XXVII":27,"XXVIII":28,"XXIX":29,"XXX":30,"XXXI":31,
              "XXXII":32,"XXXIII":33}

    chapters = []
    for i, m in enumerate(matches):
        raw_num = m.group(1).strip()
        num = _ROMAN.get(raw_num.upper(), 0) or int(raw_num) if raw_num.isdigit() else i+1
        start = m.start()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        body = text[start:end].strip()
        lines = body.split("\n", 4)
        tl = ""
        for line in lines[1:3]:
            s = line.strip()
            if s and not re.match(r"(?:CHAPTER|Chapter)\s", s): tl = s.rstrip("."); break
        if len(body.split()) >= 30:
            chapters.append((num, tl, body))

    if not chapters:
        parts = split_para(text)
        chapters = [(i+1, "", p) for i, p in enumerate(parts)]

    process(chapters, out_dir, {
        "slug": "westminster-confession",
        "title": "웨스트민스터 신앙고백서",
        "title_original": "The Westminster Confession of Faith",
        "author": "웨스트민스터 총회",
        "author_original": "Westminster Assembly",
        "year": "1646",
        "source": "https://ccel.org/ccel/anonymous/westminster1",
        "license": "public_domain",
        "note": "장로교회의 신앙적 기초를 이루는 가장 중요한 신앙고백서. 33장으로 구성된 체계적인 교리 선언문.",
    })


# ─── 3. Westminster Larger Catechism ───

def split_westminster_larger(raw):
    print("\n=== Westminster Larger Catechism ===")
    text = clean(raw)
    out_dir = BOOKS_DIR / "westminster-catechism-larger"

    # Question 1: 패턴으로 분할, 20문항씩 묶기
    q_pat = re.compile(r"\n\s*Question\s+(\d+)[.:]", re.IGNORECASE)
    matches = list(q_pat.finditer(text))

    chapters = []
    group_size = 20
    for gi in range(0, len(matches), group_size):
        batch = matches[gi:gi+group_size]
        start = batch[0].start()
        end = matches[gi+group_size].start() if gi+group_size < len(matches) else len(text)
        body = text[start:end].strip()
        num = gi // group_size + 1
        q_start = int(batch[0].group(1))
        q_end = int(batch[-1].group(1))
        chapters.append((num, f"문답 {q_start}-{q_end}", body))

    if not chapters:
        parts = split_para(text)
        chapters = [(i+1, "", p) for i, p in enumerate(parts)]

    process(chapters, out_dir, {
        "slug": "westminster-catechism-larger",
        "title": "웨스트민스터 대교리문답",
        "title_original": "The Westminster Larger Catechism",
        "author": "웨스트민스터 총회",
        "author_original": "Westminster Assembly",
        "year": "1648",
        "source": "https://ccel.org/ccel/anonymous/westminster2",
        "license": "public_domain",
        "note": "196문답으로 구성된 상세한 교리문답. 목사와 교사를 위한 깊이 있는 교리 교육 자료.",
    })


# ─── 4. Westminster Shorter Catechism ───

def split_westminster_shorter(raw):
    print("\n=== Westminster Shorter Catechism ===")
    text = clean(raw)
    out_dir = BOOKS_DIR / "westminster-catechism-shorter"

    # Q1: A1: 패턴 (Shorter Catechism CCEL 형식)
    q_pat = re.compile(r"\n\s*Q(\d+)[.:]", re.IGNORECASE)
    matches = list(q_pat.finditer(text))

    chapters = []
    group_size = 15
    for gi in range(0, len(matches), group_size):
        batch = matches[gi:gi+group_size]
        start = batch[0].start()
        end = matches[gi+group_size].start() if gi+group_size < len(matches) else len(text)
        body = text[start:end].strip()
        num = gi // group_size + 1
        q_start = int(batch[0].group(1))
        q_end = int(batch[-1].group(1))
        chapters.append((num, f"문답 {q_start}-{q_end}", body))

    if not chapters:
        parts = split_para(text)
        chapters = [(i+1, "", p) for i, p in enumerate(parts)]

    process(chapters, out_dir, {
        "slug": "westminster-catechism-shorter",
        "title": "웨스트민스터 소교리문답",
        "title_original": "The Westminster Shorter Catechism",
        "author": "웨스트민스터 총회",
        "author_original": "Westminster Assembly",
        "year": "1647",
        "source": "https://ccel.org/ccel/anonymous/westminster3",
        "license": "public_domain",
        "note": "107문답의 간결한 교리문답. '사람의 제일 되는 목적'(Q1)으로 시작하는 가장 유명한 교리문답서.",
    })


# ─── 5-7. Augsburg, Belgic, Dort — schaff/creeds1에서 추출 ───

def _extract_section(text, start_marker, end_markers):
    """텍스트에서 start_marker ~ end_markers 사이 구간 추출.
    end_markers는 줄 시작에서 매칭 (본문 내 참조 제외)."""
    start = re.search(start_marker, text, re.IGNORECASE)
    if not start: return ""
    # 서문/소개 건너뛰기: 시작점 이후 5000자부터 end marker 검색
    skip = 5000
    end_pos = len(text)
    for em in end_markers:
        # 줄 시작에서만 매칭하여 본문 내 참조와 구분
        line_em = r"^\s*" + em
        m = re.search(line_em, text[start.start()+skip:], re.IGNORECASE | re.MULTILINE)
        if m:
            end_pos = min(end_pos, start.start() + skip + m.start())
    return text[start.start():end_pos].strip()


def split_augsburg(raw):
    print("\n=== Augsburg Confession ===")
    text = clean(raw)
    # schaff/creeds3: "The Augsburg Confession. A.D. 1530." ~ next confession section
    section = _extract_section(text,
        r"The\s+Augsburg\s+Confession\.?\s+A\.?\s*D\.?\s*1530",
        [r"The\s+Formula\s+of\s+Concord", r"The\s+Belgic\s+Confession",
         r"The\s+Heidelberg", r"The\s+Second\s+Helvetic",
         r"THE\s+APOLOGY\s+OF\s+THE\s+AUGSBURG"])
    if not section or len(section.split()) < 100:
        # 대안: 넓은 매칭
        section = _extract_section(text, r"AUGSBURG\s+CONFESSION",
            [r"FORMULA\s+OF\s+CONCORD", r"BELGIC\s+CONFESSION"])
    if not section or len(section.split()) < 100:
        section = text
    out_dir = BOOKS_DIR / "augsburg-confession"

    # "ARTICLE I." 또는 "Art. I." 패턴으로 분할
    art_pat = re.compile(r"\n\s*(?:ARTICLE|Art\.?)\s+([IVXLC]+|\d+)\.?\s*[-—]?\s*", re.IGNORECASE)
    matches = list(art_pat.finditer(section))

    chapters = []
    if matches:
        for i, m in enumerate(matches):
            start = m.start()
            end = matches[i+1].start() if i+1 < len(matches) else len(section)
            body = section[start:end].strip()
            if len(body.split()) >= 15:
                chapters.append((i+1, "", body))

    if not chapters:
        parts = split_para(section)
        chapters = [(i+1, "", p) for i, p in enumerate(parts)]

    process(chapters, out_dir, {
        "slug": "augsburg-confession",
        "title": "아우크스부르크 신앙고백서",
        "title_original": "The Augsburg Confession",
        "author": "필립 멜란히톤",
        "author_original": "Philipp Melanchthon",
        "year": "1530",
        "source": "https://ccel.org/ccel/schaff/creeds1",
        "license": "public_domain",
        "note": "루터교회의 기초가 된 최초의 개신교 신앙고백서. 28조항으로 구성.",
    })


def split_belgic(raw):
    print("\n=== Belgic Confession ===")
    text = clean(raw)
    section = _extract_section(text,
        r"The\s+Belgic\s+Confession\.?\s+A\.?\s*D\.?\s*1561",
        [r"The\s+Canons\s+of\s+(?:the\s+Synod\s+of\s+)?Dort",
         r"The\s+Heidelberg\s+Catechism",
         r"The\s+Second\s+Helvetic", r"The\s+Westminster"])
    if not section or len(section.split()) < 100:
        section = _extract_section(text, r"BELGIC\s+CONFESSION",
            [r"CANONS\s+OF\s+DORT", r"HEIDELBERG\s+CATECHISM"])
    if not section or len(section.split()) < 100: section = text
    out_dir = BOOKS_DIR / "belgic-confession"

    art_pat = re.compile(r"\n\s*(?:ARTICLE|Art\.?)\s+([IVXLC]+|\d+)", re.IGNORECASE)
    matches = list(art_pat.finditer(section))

    chapters = []
    if matches:
        for i, m in enumerate(matches):
            start = m.start()
            end = matches[i+1].start() if i+1 < len(matches) else len(section)
            body = section[start:end].strip()
            if len(body.split()) >= 15:
                chapters.append((i+1, "", body))

    if not chapters:
        parts = split_para(section)
        chapters = [(i+1, "", p) for i, p in enumerate(parts)]

    process(chapters, out_dir, {
        "slug": "belgic-confession",
        "title": "벨기에 신앙고백서",
        "title_original": "The Belgic Confession",
        "author": "기도 드 브레",
        "author_original": "Guido de Brès",
        "year": "1561",
        "source": "https://ccel.org/ccel/schaff/creeds1",
        "license": "public_domain",
        "note": "개혁교회의 3대 신앙고백서 중 하나. 37조항으로 기독교 신앙의 핵심을 고백.",
    })


def split_dort(raw):
    print("\n=== Canons of Dort ===")
    text = clean(raw)
    section = _extract_section(text,
        r"The\s+Canons\s+of\s+(?:the\s+Synod\s+of\s+)?Dort\.?\s+A\.?\s*D",
        [r"The\s+Heidelberg\s+Catechism", r"The\s+Westminster",
         r"The\s+Second\s+Helvetic", r"The\s+Belgic"])
    if not section: section = text
    out_dir = BOOKS_DIR / "canons-of-dort"

    # Head/Article 패턴 또는 FIRST/SECOND HEAD
    head_pat = re.compile(r"\n\s*((?:FIRST|SECOND|THIRD|FOURTH|FIFTH)\s+(?:HEAD|POINT|ARTICLE))", re.IGNORECASE)
    matches = list(head_pat.finditer(section))

    chapters = []
    if matches:
        for i, m in enumerate(matches):
            start = m.start()
            end = matches[i+1].start() if i+1 < len(matches) else len(section)
            body = section[start:end].strip()
            chapters.append((i+1, m.group(1).strip().title(), body))

    if not chapters:
        parts = split_para(section)
        chapters = [(i+1, "", p) for i, p in enumerate(parts)]

    process(chapters, out_dir, {
        "slug": "canons-of-dort",
        "title": "도르트 신경",
        "title_original": "Canons of the Synod of Dort",
        "author": "도르트 총회",
        "author_original": "Synod of Dort",
        "year": "1619",
        "source": "https://ccel.org/ccel/schaff/creeds1",
        "license": "public_domain",
        "note": "개혁교회의 3대 신앙고백서 중 하나. 5대 교리(TULIP)를 체계적으로 정리한 문서.",
    })


# ─── 다운로드/실행 ───

DOWNLOADS = [
    ("anonymous", "heidelberg", "heidelberg.txt", split_heidelberg),
    ("anonymous", "westminster3", "westminster3.txt", split_westminster_conf),
    ("anonymous", "westminster2", "westminster2.txt", split_westminster_larger),
    ("anonymous", "westminster1", "westminster1.txt", split_westminster_shorter),
    # 아래 3권은 모두 schaff/creeds3에서 추출
    ("schaff", "creeds3", "schaff-creeds3.txt", split_augsburg),
    ("schaff", "creeds3", "schaff-creeds3.txt", split_belgic),
    ("schaff", "creeds3", "schaff-creeds3.txt", split_dort),
]


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
            print(f"\n[건너뜀] {filename} — --download 플래그 필요")
            continue
        split_fn(raw)

    print("\n" + "=" * 60)
    print("16차 배치 처리 완료! (신앙고백서 7권)")


if __name__ == "__main__":
    main()
