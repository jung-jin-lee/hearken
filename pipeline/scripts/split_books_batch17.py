#!/usr/bin/env python3
"""17차 도서 13권 분할 — Ryle, Murray, Spurgeon 추가, Calvin (CCEL 소스).

대상:
  1. Holiness (J.C. Ryle) — CCEL ryle/holiness
  2. Expository Thoughts: Matthew (J.C. Ryle) — CCEL ryle/matthew
  3. Two Bears (J.C. Ryle) — CCEL ryle/twobears
  4. The Upper Room (J.C. Ryle) — CCEL ryle/upper_room
  5. With Christ in School of Prayer (Andrew Murray) — CCEL murray/prayer
  6. Working for God (Andrew Murray) — CCEL murray/working
  7. The Two Covenants (Andrew Murray) — CCEL murray/covenants
  8. Spurgeon's Sermons Vol.1 (C.H. Spurgeon) — CCEL spurgeon/sermons01
  9. Morning & Evening (C.H. Spurgeon) — CCEL spurgeon/morneve
  10. The Salt-Cellars (C.H. Spurgeon) — CCEL spurgeon/proverbs
  11. Till He Come (C.H. Spurgeon) — CCEL spurgeon/till_he_come
  12. Commentary on Romans (John Calvin) — CCEL calvin/calcom36
  13. Commentary on Psalms Vol.1 (John Calvin) — CCEL calvin/calcom39

사용법:
  python pipeline/scripts/split_books_batch17.py [--download]
"""

import json, re, sys
from pathlib import Path

BOOKS_DIR = Path("pipeline/sources/data/books")
CACHE_DIR = Path("/private/tmp/claude-501")
MAX_CHAPTER_WORDS = 8000
CCEL_BASE = "https://ccel.org/ccel"


def _ccel_url(a, w): return f"{CCEL_BASE}/{a[0]}/{a}/{w}/cache/{w}.txt"

def download(url, dest):
    import urllib.request
    if dest.exists() and dest.stat().st_size > 500:
        print(f"  [캐시] {dest.name}"); return dest.read_text(encoding="utf-8")
    print(f"  [다운로드] {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r: data = r.read()
    text = data.decode("utf-8", errors="replace")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8"); return text

def clean(t): return re.sub(r"\n{4,}", "\n\n\n", re.sub(r"_{5,}", "", t)).strip()

def save_ch(d, n, t, b):
    d.mkdir(parents=True, exist_ok=True)
    f = f"ch{n:02d}.txt"
    (d/f).write_text(f"{t}\n\n{b.strip()}\n", encoding="utf-8")
    print(f"  {f}: {t[:60]} ({len(b.split())} words)")

def save_meta(d, m):
    d.mkdir(parents=True, exist_ok=True)
    (d/"metadata.json").write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")

def split_para(t, mx=MAX_CHAPTER_WORDS):
    if len(t.split()) <= mx: return [t]
    ps = [p for p in t.split("\n\n") if p.strip()]
    cks, cur, cw = [], [], 0
    for p in ps:
        pw = len(p.split())
        if cw+pw > mx and cur: cks.append("\n\n".join(cur)); cur, cw = [], 0
        cur.append(p); cw += pw
    if cur: cks.append("\n\n".join(cur))
    return cks or [t]

_ROMAN = {"I":1,"II":2,"III":3,"IV":4,"V":5,"VI":6,"VII":7,"VIII":8,"IX":9,"X":10,
          "XI":11,"XII":12,"XIII":13,"XIV":14,"XV":15,"XVI":16,"XVII":17,"XVIII":18,
          "XIX":19,"XX":20,"XXI":21,"XXII":22,"XXIII":23,"XXIV":24,"XXV":25,
          "XXVI":26,"XXVII":27,"XXVIII":28,"XXIX":29,"XXX":30}

def _strip_ccel(t):
    for mk in ["Generated on", "This document has been generated", "This document is from"]:
        i = t.find(mk)
        if i != -1 and i < 2000:
            nl = t[i:].find("\n\n")
            if nl != -1: t = t[i+nl:].strip(); break
    return t

def _split_chapters(text, min_w=50):
    """CHAPTER I/1 마커로 분할."""
    pat = re.compile(r"\n\s*CHAPTER\s+([IVXLC]+|\d+)\.?\s*\n", re.IGNORECASE)
    ms = list(pat.finditer(text))
    # TOC 중복 제거
    ch1 = [m for m in ms if (_ROMAN.get(m.group(1).upper(), 0) == 1 or m.group(1) == "1")]
    if len(ch1) >= 2:
        ms = [m for m in ms if m.start() >= ch1[1].start()]
    chs = []
    for i, m in enumerate(ms):
        raw = m.group(1).strip()
        num = _ROMAN.get(raw.upper(), 0) or (int(raw) if raw.isdigit() else i+1)
        s, e = m.start(), ms[i+1].start() if i+1 < len(ms) else len(text)
        body = text[s:e].strip()
        lines = body.split("\n", 5)
        tl = ""
        for l in lines[1:4]:
            x = l.strip()
            if x and not re.match(r"CHAPTER\s", x, re.IGNORECASE): tl = x.rstrip("."); break
        if len(body.split()) >= min_w: chs.append((num, tl, body))
    return chs

def process(chs, d, mb, tm=None):
    cm = []
    for num, tl, body in chs:
        title = (tm or {}).get(num, f"제{num}장: {tl}" if tl else f"제{num}장")
        body = re.sub(r"\n{3,}", "\n\n", body)
        parts = split_para(body)
        for pi, p in enumerate(parts):
            fn = len(cm)+1; sfx = f" ({pi+1}/{len(parts)})" if len(parts)>1 else ""
            ct = f"{title}{sfx}"; save_ch(d, fn, ct, p)
            cm.append({"num":fn, "title":ct, "file":f"ch{fn:02d}.txt"})
    save_meta(d, {**mb, "chapters": cm}); print(f"  총 {len(cm)}개 챕터 저장")


# ─── BOOK DEFINITIONS ───

BOOKS = [
    # Ryle
    {"slug":"ryle-holiness", "ccel":"ryle/holiness", "title":"거룩",
     "title_orig":"Holiness: Its Nature, Hindrances, Difficulties, and Roots",
     "author":"존 라일 (J.C. Ryle)", "author_orig":"J.C. Ryle", "year":"1877",
     "note":"라일 주교의 대표작. 성화의 본질과 실천적 경건을 다룬 복음주의 경건의 고전."},
    {"slug":"ryle-expository-matthew", "ccel":"ryle/matthew", "title":"마태복음 강해",
     "title_orig":"Expository Thoughts on the Gospels: Matthew",
     "author":"존 라일 (J.C. Ryle)", "author_orig":"J.C. Ryle", "year":"1856",
     "note":"라일의 복음서 강해 시리즈 제1권. 마태복음을 구절별로 명쾌하게 해설."},
    {"slug":"ryle-two-bears", "ccel":"ryle/twobears", "title":"두 마리 곰",
     "title_orig":"Two Bears",
     "author":"존 라일 (J.C. Ryle)", "author_orig":"J.C. Ryle", "year":"1870",
     "note":"라일의 어린이/청소년을 위한 성경 이야기 모음."},
    {"slug":"ryle-upper-room", "ccel":"ryle/upper_room", "title":"다락방",
     "title_orig":"The Upper Room",
     "author":"존 라일 (J.C. Ryle)", "author_orig":"J.C. Ryle", "year":"1888",
     "note":"요한복음 14-17장에 대한 라일의 강해. 예수님의 고별 설교와 대제사장의 기도를 해설."},
    # Murray
    {"slug":"murray-school-prayer", "ccel":"murray/prayer", "title":"기도의 학교에서 그리스도와 함께",
     "title_orig":"With Christ in the School of Prayer",
     "author":"앤드류 머레이 (Andrew Murray)", "author_orig":"Andrew Murray", "year":"1885",
     "note":"기도에 관한 머레이의 가장 유명한 저작. 주기도문과 예수님의 기도 교훈을 31과로 해설."},
    {"slug":"murray-working-god", "ccel":"murray/working", "title":"하나님을 위해 일하기",
     "title_orig":"Working for God",
     "author":"앤드류 머레이 (Andrew Murray)", "author_orig":"Andrew Murray", "year":"1901",
     "note":"기독교인의 봉사와 사역의 삶에 대한 실용적 안내서."},
    {"slug":"murray-two-covenants", "ccel":"murray/covenants", "title":"두 언약",
     "title_orig":"The Two Covenants",
     "author":"앤드류 머레이 (Andrew Murray)", "author_orig":"Andrew Murray", "year":"1898",
     "note":"구약과 신약의 두 언약의 본질과 관계를 탐구한 성경 신학 저작."},
    # Spurgeon additional
    {"slug":"spurgeon-sermons-v1", "ccel":"spurgeon/sermons01", "title":"스펄전 설교집 제1권",
     "title_orig":"Spurgeon's Sermons Volume 01 (1855)",
     "author":"찰스 스펄전 (C.H. Spurgeon)", "author_orig":"C.H. Spurgeon", "year":"1855",
     "note":"스펄전의 첫 번째 설교 모음집. 21세에 시작한 런던 사역 초기의 열정적인 설교들."},
    {"slug":"spurgeon-morning-evening", "ccel":"spurgeon/morneve", "title":"아침과 저녁",
     "title_orig":"Morning and Evening: Daily Readings",
     "author":"찰스 스펄전 (C.H. Spurgeon)", "author_orig":"C.H. Spurgeon", "year":"1866",
     "note":"스펄전의 365일 아침저녁 묵상집. 매일 아침과 저녁 각각의 묵상문을 제공."},
    {"slug":"spurgeon-salt-cellars", "ccel":"spurgeon/proverbs", "title":"소금 단지",
     "title_orig":"The Salt-Cellars: Being a Collection of Proverbs",
     "author":"찰스 스펄전 (C.H. Spurgeon)", "author_orig":"C.H. Spurgeon", "year":"1889",
     "note":"스펄전이 수집한 속담과 격언 모음. 지혜 문학에 대한 스펄전의 사랑을 보여주는 독특한 저작."},
    {"slug":"spurgeon-till-he-come", "ccel":"spurgeon/till_he_come", "title":"그가 오실 때까지",
     "title_orig":"Till He Come: Communion Meditations and Addresses",
     "author":"찰스 스펄전 (C.H. Spurgeon)", "author_orig":"C.H. Spurgeon", "year":"1896",
     "note":"성만찬 묵상과 강해 모음. 그리스도의 재림을 기다리며 드리는 성찬 예배의 의미를 탐구."},
    # Calvin
    {"slug":"calvin-commentary-romans", "ccel":"calvin/calcom36", "title":"로마서 주석",
     "title_orig":"Commentary on Romans",
     "author":"존 칼빈 (John Calvin)", "author_orig":"John Calvin", "year":"1540",
     "note":"칼빈의 로마서 주석. 칼빈 신학의 핵심이 담긴 가장 중요한 성경 주석 중 하나."},
    {"slug":"calvin-commentary-psalms-v1", "ccel":"calvin/calcom39", "title":"시편 주석 제1권",
     "title_orig":"Commentary on the Psalms, Volume 1",
     "author":"존 칼빈 (John Calvin)", "author_orig":"John Calvin", "year":"1557",
     "note":"칼빈의 시편 주석 제1권. 시편 1-35편에 대한 상세한 강해와 적용."},
]


def split_generic(raw, info):
    slug = info["slug"]
    print(f"\n=== {info['title_orig']} ===")
    text = clean(_strip_ccel(raw))
    out_dir = BOOKS_DIR / slug

    chapters = _split_chapters(text)

    # CHAPTER 마커가 없으면 다른 패턴 시도
    if not chapters:
        # SERMON / LECTURE 패턴
        sermon_pat = re.compile(r"\n\s*(?:SERMON|LECTURE|LESSON)\s+([IVXLC]+|\d+)\.?\s*\n", re.IGNORECASE)
        sm = list(sermon_pat.finditer(text))
        if sm:
            for i, m in enumerate(sm):
                raw_n = m.group(1).strip()
                num = _ROMAN.get(raw_n.upper(), 0) or (int(raw_n) if raw_n.isdigit() else i+1)
                s, e = m.start(), sm[i+1].start() if i+1 < len(sm) else len(text)
                body = text[s:e].strip()
                lines = body.split("\n", 4)
                tl = ""
                for l in lines[1:3]:
                    x = l.strip()
                    if x and not re.match(r"(?:SERMON|LECTURE|LESSON)\s", x, re.IGNORECASE):
                        tl = x.rstrip("."); break
                if len(body.split()) >= 50:
                    chapters.append((num, tl, body))

    if not chapters:
        # 전체 분할
        parts = split_para(text)
        chapters = [(i+1, "", p) for i, p in enumerate(parts)]

    process(chapters, out_dir, {
        "slug": slug,
        "title": info["title"],
        "title_original": info["title_orig"],
        "author": info["author"],
        "author_original": info["author_orig"],
        "year": info["year"],
        "source": f"https://ccel.org/ccel/{info['ccel'].split('/')[0]}/{info['ccel'].split('/')[1]}",
        "license": "public_domain",
        "note": info["note"],
    })


# ─── DOWNLOAD & EXECUTE ───

def main():
    do_dl = "--download" in sys.argv
    for info in BOOKS:
        parts = info["ccel"].split("/")
        author, work = parts[0], parts[1]
        fname = f"{author}-{work}.txt"
        cache = CACHE_DIR / fname
        url = _ccel_url(author, work)
        if do_dl:
            try:
                raw = download(url, cache)
            except Exception as e:
                print(f"\n[에러] {fname}: {e}"); continue
        elif cache.exists():
            raw = cache.read_text(encoding="utf-8")
        else:
            print(f"\n[건너뜀] {fname} — --download 필요"); continue
        split_generic(raw, info)
    print("\n" + "=" * 60)
    print("17차 배치 처리 완료! (13권)")


if __name__ == "__main__":
    main()
