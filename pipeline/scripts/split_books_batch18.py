#!/usr/bin/env python3
"""18차 도서 8권 분할 — 나머지 1순위 (Gutenberg + CCEL).

대상:
  1. Luther Works Vol.I (Address to Nobility, Babylonian Captivity 등) — Gutenberg #31604
  2. Luther Epistle Sermons Vol.3 — Gutenberg #30619
  3. Spurgeon Treasury of David Vol.1 — CCEL treasury1
  4. Spurgeon Sermons Vol.2 — CCEL sermons02
  5. Spurgeon Sermons Vol.3 — CCEL sermons03
  6. Moody Sermons (Wondrous Love) — Gutenberg #33520
  7. Watson All Things for Good — CCEL watson/cordial
  8. Moody Overcoming Life extras (Weighed and Wanting) — Gutenberg #33340

사용법:
  python pipeline/scripts/split_books_batch18.py [--download]
"""

import json, re, sys
from pathlib import Path

BOOKS_DIR = Path("pipeline/sources/data/books")
CACHE_DIR = Path("/private/tmp/claude-501")
MAX_CHAPTER_WORDS = 8000


def _gurl(eid): return f"https://www.gutenberg.org/cache/epub/{eid}/pg{eid}.txt"
def _curl(a, w): return f"https://ccel.org/ccel/{a[0]}/{a}/{w}/cache/{w}.txt"

def download(url, dest):
    import urllib.request
    if dest.exists() and dest.stat().st_size > 500:
        print(f"  [캐시] {dest.name}"); return dest.read_text(encoding="utf-8")
    print(f"  [다운로드] {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r: data = r.read()
    except Exception as e:
        print(f"  [에러] {e}"); return None
    text = data.decode("utf-8", errors="replace")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8"); return text

def clean(t): return re.sub(r"\n{4,}","\n\n\n", re.sub(r"_{5,}","",t)).strip()
def extract_gut(t):
    for s in ["*** START OF THE PROJECT GUTENBERG","*** START OF THIS PROJECT GUTENBERG"]:
        i=t.find(s)
        if i!=-1: t=t[i:].split("\n",1)[1] if "\n" in t[i:] else t[i:]; break
    for e in ["*** END OF THE PROJECT GUTENBERG","*** END OF THIS PROJECT GUTENBERG","End of the Project Gutenberg","End of Project Gutenberg"]:
        i=t.find(e)
        if i!=-1: t=t[:i]; break
    return t.strip()
def strip_ccel(t):
    for mk in ["Generated on","This document has been generated"]:
        i=t.find(mk)
        if i!=-1 and i<2000:
            nl=t[i:].find("\n\n")
            if nl!=-1: t=t[i+nl:].strip(); break
    return t

def save_ch(d,n,t,b):
    d.mkdir(parents=True, exist_ok=True)
    f=f"ch{n:02d}.txt"; (d/f).write_text(f"{t}\n\n{b.strip()}\n",encoding="utf-8")
    print(f"  {f}: {t[:60]} ({len(b.split())} words)")
def save_meta(d,m):
    d.mkdir(parents=True, exist_ok=True)
    (d/"metadata.json").write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding="utf-8")
def split_para(t,mx=MAX_CHAPTER_WORDS):
    if len(t.split())<=mx: return [t]
    ps=[p for p in t.split("\n\n") if p.strip()]; cks,cur,cw=[],[],0
    for p in ps:
        pw=len(p.split())
        if cw+pw>mx and cur: cks.append("\n\n".join(cur)); cur,cw=[],0
        cur.append(p); cw+=pw
    if cur: cks.append("\n\n".join(cur))
    return cks or [t]

_R={"I":1,"II":2,"III":3,"IV":4,"V":5,"VI":6,"VII":7,"VIII":8,"IX":9,"X":10,
    "XI":11,"XII":12,"XIII":13,"XIV":14,"XV":15,"XVI":16,"XVII":17,"XVIII":18,
    "XIX":19,"XX":20,"XXI":21,"XXII":22,"XXIII":23,"XXIV":24,"XXV":25,
    "XXVI":26,"XXVII":27,"XXVIII":28,"XXIX":29,"XXX":30}

def process(chs, d, mb):
    cm=[]
    for num, tl, body in chs:
        title = f"제{num}장: {tl}" if tl else f"제{num}장"
        body = re.sub(r"\n{3,}","\n\n",body)
        for pi,p in enumerate(split_para(body)):
            fn=len(cm)+1; sfx=f" ({pi+1}/{len(split_para(body))})" if len(split_para(body))>1 else ""
            ct=f"{title}{sfx}"; save_ch(d,fn,ct,p)
            cm.append({"num":fn,"title":ct,"file":f"ch{fn:02d}.txt"})
    save_meta(d, {**mb, "chapters":cm}); print(f"  총 {len(cm)}개 챕터 저장")

def find_chapters(text, min_w=50):
    """CHAPTER 마커로 분할."""
    pat=re.compile(r"\n\s*CHAPTER\s+([IVXLC]+|\d+)\.?\s*\n",re.IGNORECASE)
    ms=list(pat.finditer(text))
    ch1=[m for m in ms if (_R.get(m.group(1).upper(),0)==1 or m.group(1)=="1")]
    if len(ch1)>=2: ms=[m for m in ms if m.start()>=ch1[1].start()]
    chs=[]
    for i,m in enumerate(ms):
        raw=m.group(1).strip(); num=_R.get(raw.upper(),0) or (int(raw) if raw.isdigit() else i+1)
        s,e=m.start(), ms[i+1].start() if i+1<len(ms) else len(text)
        body=text[s:e].strip()
        lines=body.split("\n",5); tl=""
        for l in lines[1:4]:
            x=l.strip()
            if x and not re.match(r"CHAPTER\s",x,re.IGNORECASE): tl=x.rstrip("."); break
        if len(body.split())>=min_w: chs.append((num,tl,body))
    return chs


# ─── 1. Luther Works Vol.I — extract sub-works ───

def split_luther_works(raw):
    if not raw: return
    print("\n=== Luther Works Vol.I ===")
    text = clean(extract_gut(raw))

    # Extract individual works
    works = [
        ("luther-address-nobility", "독일 기독교 귀족에게",
         "To the Christian Nobility of the German Nation",
         r"TO THE CHRISTIAN NOBILITY", r"(?:THE BABYLONIAN|A TREATISE ON)",
         "1520", "독일 귀족들에게 교회 개혁을 촉구한 루터의 세 대작 중 하나."),
        ("luther-babylonian-captivity", "교회의 바빌론 포로",
         "The Babylonian Captivity of the Church",
         r"(?:THE\s+)?BABYLONIAN\s+CAPTIVITY", r"(?:A TREATISE ON|CONCERNING\s+CHRISTIAN)",
         "1520", "중세 성례전 체계를 비판한 루터의 혁명적 저작. 세 대작 중 두 번째."),
    ]

    for slug, title_kr, title_en, start_pat, end_pat, year, note in works:
        start_m = re.search(start_pat, text, re.IGNORECASE)
        if not start_m:
            print(f"  [{slug}] 시작점 찾기 실패"); continue
        end_m = re.search(end_pat, text[start_m.start()+5000:], re.IGNORECASE)
        end_pos = start_m.start()+5000+end_m.start() if end_m else len(text)
        section = text[start_m.start():end_pos].strip()

        if len(section.split()) < 100:
            print(f"  [{slug}] 내용 부족 ({len(section.split())} words)"); continue

        out_dir = BOOKS_DIR / slug
        parts = split_para(section)
        chs = [(i+1, "", p) for i, p in enumerate(parts)]
        process(chs, out_dir, {
            "slug": slug, "title": title_kr, "title_original": title_en,
            "author": "마르틴 루터 (Martin Luther)", "author_original": "Martin Luther",
            "year": year, "source": "https://www.gutenberg.org/ebooks/31604",
            "license": "public_domain", "note": note,
        })


# ─── 2. Luther Epistle Sermons ───

def split_luther_sermons(raw):
    if not raw: return
    print("\n=== Luther Epistle Sermons Vol.3 ===")
    text = clean(extract_gut(raw))
    out_dir = BOOKS_DIR / "luther-sermons-select"

    chs = find_chapters(text)
    if not chs:
        # SERMON 패턴
        pat = re.compile(r"\n\s*(?:SERMON|EPISTLE)\s.*?\n", re.IGNORECASE)
        ms = list(pat.finditer(text))
        for i,m in enumerate(ms):
            s,e = m.start(), ms[i+1].start() if i+1<len(ms) else len(text)
            body = text[s:e].strip()
            if len(body.split())>=100:
                chs.append((len(chs)+1, m.group().strip()[:50], body))
    if not chs:
        parts = split_para(text)
        chs = [(i+1,"",p) for i,p in enumerate(parts)]

    process(chs, out_dir, {
        "slug": "luther-sermons-select", "title": "루터 설교선집",
        "title_original": "Epistle Sermons, Vol. 3: Trinity Sunday to Advent",
        "author": "마르틴 루터 (Martin Luther)", "author_original": "Martin Luther",
        "year": "~1530", "source": "https://www.gutenberg.org/ebooks/30619",
        "license": "public_domain",
        "note": "루터의 서신 설교집 제3권. 삼위일체 주일부터 대림절까지의 교회력 설교 모음.",
    })


# ─── 3-5. Spurgeon CCEL additional ───

def split_ccel_generic(raw, slug, title_kr, title_en, author_kr, author_en, year, source, note):
    if not raw: return
    print(f"\n=== {title_en} ===")
    text = clean(strip_ccel(raw))
    out_dir = BOOKS_DIR / slug

    chs = find_chapters(text)
    if not chs:
        # SERMON/LECTURE 패턴
        pat = re.compile(r"\n\s*(?:SERMON|LECTURE|PSALM)\s+([IVXLC]+|\d+)\.?\s*\n", re.IGNORECASE)
        ms = list(pat.finditer(text))
        for i,m in enumerate(ms):
            raw_n=m.group(1).strip()
            num=_R.get(raw_n.upper(),0) or (int(raw_n) if raw_n.isdigit() else i+1)
            s,e=m.start(), ms[i+1].start() if i+1<len(ms) else len(text)
            body=text[s:e].strip()
            if len(body.split())>=50: chs.append((num,"",body))
    if not chs:
        parts = split_para(text)
        chs = [(i+1,"",p) for i,p in enumerate(parts)]

    process(chs, out_dir, {
        "slug": slug, "title": title_kr, "title_original": title_en,
        "author": author_kr, "author_original": author_en,
        "year": year, "source": source, "license": "public_domain", "note": note,
    })


# ─── 6. Moody Sermons (Wondrous Love) ───

def split_moody_sermons(raw):
    if not raw: return
    print("\n=== Wondrous Love (D.L. Moody Sermons) ===")
    text = clean(extract_gut(raw))
    out_dir = BOOKS_DIR / "moody-sermons-select"

    chs = find_chapters(text)
    if not chs:
        parts = split_para(text)
        chs = [(i+1,"",p) for i,p in enumerate(parts)]

    process(chs, out_dir, {
        "slug": "moody-sermons-select", "title": "무디 설교선집",
        "title_original": "Wondrous Love, and Other Gospel Addresses",
        "author": "드와이트 무디 (D.L. Moody)", "author_original": "D.L. Moody",
        "year": "1876", "source": "https://www.gutenberg.org/ebooks/33520",
        "license": "public_domain",
        "note": "무디의 복음 메시지 모음. 하나님의 놀라운 사랑을 중심으로 한 대중 전도 설교집.",
    })


# ─── 7. Watson All Things for Good ───

def split_watson_cordial(raw):
    if not raw: return
    split_ccel_generic(raw, "watson-all-things-good",
        "합력하여 선을 이루시는 하나님", "All Things for Good (A Divine Cordial)",
        "토마스 왓슨 (Thomas Watson)", "Thomas Watson", "1663",
        "https://ccel.org/ccel/watson/cordial",
        "로마서 8:28에 기초한 왓슨의 대표적 위로 서적. 고난 중 하나님의 선하신 섭리를 확신케 하는 고전.")


# ─── 8. Moody Weighed and Wanting ───

def split_moody_weighed(raw):
    if not raw: return
    print("\n=== Weighed and Wanting (D.L. Moody) ===")
    text = clean(extract_gut(raw))
    out_dir = BOOKS_DIR / "moody-weighed-wanting"

    chs = find_chapters(text)
    if not chs:
        parts = split_para(text)
        chs = [(i+1,"",p) for i,p in enumerate(parts)]

    process(chs, out_dir, {
        "slug": "moody-weighed-wanting", "title": "저울에 달아 부족함이 있느니라",
        "title_original": "Weighed and Wanting: Addresses on the Ten Commandments",
        "author": "드와이트 무디 (D.L. Moody)", "author_original": "D.L. Moody",
        "year": "1898", "source": "https://www.gutenberg.org/ebooks/33340",
        "license": "public_domain",
        "note": "무디가 십계명을 하나씩 풀어 설교한 실용적 도덕 강해 시리즈.",
    })


# ─── DOWNLOADS ───

DOWNLOADS = [
    # (url, cache_file, split_fn)
    (_gurl(31604), "luther-works-v1.txt", split_luther_works),
    (_gurl(30619), "luther-sermons-v3.txt", split_luther_sermons),
    (_curl("spurgeon","treasury1"), "spurgeon-treasury1.txt",
     lambda r: split_ccel_generic(r, "spurgeon-treasury-david-v1",
         "시편 강해 보물 제1권", "The Treasury of David, Vol.1",
         "찰스 스펄전 (C.H. Spurgeon)", "C.H. Spurgeon", "1870",
         "https://ccel.org/ccel/spurgeon/treasury1",
         "스펄전의 필생의 역작. 시편 전체에 대한 방대한 강해와 묵상, 해설 모음.")),
    (_curl("spurgeon","sermons02"), "spurgeon-sermons02.txt",
     lambda r: split_ccel_generic(r, "spurgeon-sermons-v2",
         "스펄전 설교집 제2권", "Spurgeon's Sermons Volume 02 (1856)",
         "찰스 스펄전 (C.H. Spurgeon)", "C.H. Spurgeon", "1856",
         "https://ccel.org/ccel/spurgeon/sermons02",
         "스펄전 설교집 제2권. 22세 청년 목사의 힘있는 설교 모음.")),
    (_curl("spurgeon","sermons03"), "spurgeon-sermons03.txt",
     lambda r: split_ccel_generic(r, "spurgeon-sermons-v3",
         "스펄전 설교집 제3권", "Spurgeon's Sermons Volume 03 (1857)",
         "찰스 스펄전 (C.H. Spurgeon)", "C.H. Spurgeon", "1857",
         "https://ccel.org/ccel/spurgeon/sermons03",
         "스펄전 설교집 제3권. 메트로폴리탄 태버내클 사역 초기의 설교 모음.")),
    (_gurl(33520), "moody-wondrous-love.txt", split_moody_sermons),
    (_curl("watson","cordial"), "watson-cordial.txt", split_watson_cordial),
    (_gurl(33340), "moody-weighed.txt", split_moody_weighed),
]


def main():
    do_dl = "--download" in sys.argv
    for url, fname, fn in DOWNLOADS:
        cache = CACHE_DIR / fname
        if do_dl:
            raw = download(url, cache)
        elif cache.exists():
            raw = cache.read_text(encoding="utf-8")
        else:
            print(f"\n[건너뜀] {fname}"); continue
        if raw: fn(raw)
    print("\n" + "="*60 + "\n18차 배치 처리 완료! (8권)")

if __name__ == "__main__":
    main()
