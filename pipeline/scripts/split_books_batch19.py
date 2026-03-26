#!/usr/bin/env python3
"""19차 도서 15권 분할 — 2순위 Part A (Gutenberg + CCEL).

대상:
  변증학: Chesterton 5권 (Gutenberg)
  선교전기: Livingstone, Paton (Gutenberg)
  F.B. Meyer 2권 (CCEL)
  청교도: Flavel 3권 (CCEL)
  교부: Athanasius, Basil, Gregory Nyssa (CCEL NPNF)

사용법:
  python pipeline/scripts/split_books_batch19.py [--download]
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
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
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
    (d/f"ch{n:02d}.txt").write_text(f"{t}\n\n{b.strip()}\n",encoding="utf-8")
    print(f"  ch{n:02d}.txt: {t[:55]} ({len(b.split())} words)")

def save_meta(d,m):
    d.mkdir(parents=True, exist_ok=True)
    (d/"metadata.json").write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding="utf-8")

def split_para(t, mx=MAX_CHAPTER_WORDS):
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

def find_chapters(text, min_w=50):
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

def process(chs, d, mb):
    cm=[]
    for num,tl,body in chs:
        title=f"제{num}장: {tl}" if tl else f"제{num}장"
        body=re.sub(r"\n{3,}","\n\n",body)
        for pi,p in enumerate(split_para(body)):
            fn=len(cm)+1
            sfx=f" ({pi+1}/{len(split_para(body))})" if len(split_para(body))>1 else ""
            ct=f"{title}{sfx}"; save_ch(d,fn,ct,p)
            cm.append({"num":fn,"title":ct,"file":f"ch{fn:02d}.txt"})
    save_meta(d,{**mb,"chapters":cm}); print(f"  총 {len(cm)}개 챕터 저장")


def split_generic(raw, slug, title_kr, title_en, author_kr, author_en, year, source, note, is_gut=False):
    if not raw: return
    print(f"\n=== {title_en} ===")
    text = clean(extract_gut(raw)) if is_gut else clean(strip_ccel(raw))
    out_dir = BOOKS_DIR / slug
    chs = find_chapters(text)
    if not chs:
        parts = split_para(text)
        chs = [(i+1,"",p) for i,p in enumerate(parts)]
    process(chs, out_dir, {
        "slug":slug,"title":title_kr,"title_original":title_en,
        "author":author_kr,"author_original":author_en,
        "year":year,"source":source,"license":"public_domain","note":note,
    })


# ─── BOOK DEFINITIONS ───

BOOKS = [
    # Chesterton (Gutenberg)
    {"slug":"chesterton-whats-wrong","title":"세상에 무엇이 잘못되었는가","title_en":"What's Wrong with the World",
     "author_kr":"G.K. 체스터턴","author_en":"G.K. Chesterton","year":"1910",
     "url":_gurl(1717),"gut":True,
     "note":"체스터턴의 사회비평서. 가정, 교육, 여성 문제에 대한 기독교적 관점의 날카로운 분석."},
    {"slug":"chesterton-tremendous-trifles","title":"엄청난 사소한 것들","title_en":"Tremendous Trifles",
     "author_kr":"G.K. 체스터턴","author_en":"G.K. Chesterton","year":"1909",
     "url":_gurl(8092),"gut":True,
     "note":"체스터턴의 수필집. 일상의 사소한 것에서 발견하는 경이로움과 신비를 그린 명에세이 모음."},
    {"slug":"chesterton-ball-cross","title":"공과 십자가","title_en":"The Ball and the Cross",
     "author_kr":"G.K. 체스터턴","author_en":"G.K. Chesterton","year":"1910",
     "url":_gurl(5265),"gut":True,
     "note":"무신론자와 가톨릭 신자의 논쟁을 통해 신앙과 이성의 관계를 탐구하는 소설."},
    {"slug":"chesterton-father-brown-v1","title":"브라운 신부의 순수","title_en":"The Innocence of Father Brown",
     "author_kr":"G.K. 체스터턴","author_en":"G.K. Chesterton","year":"1911",
     "url":_gurl(204),"gut":True,
     "note":"브라운 신부 추리소설 시리즈 제1권. 범죄 속에서 인간 영혼의 본질을 통찰하는 사제 탐정."},
    {"slug":"chesterton-manalive","title":"살아있는 사나이","title_en":"Manalive",
     "author_kr":"G.K. 체스터턴","author_en":"G.K. Chesterton","year":"1912",
     "url":_gurl(1718),"gut":True,
     "note":"평범한 삶의 경이로움을 재발견하게 하는 체스터턴의 유쾌한 소설."},

    # Missionaries (Gutenberg)
    {"slug":"livingstone-travels","title":"남아프리카 선교 여행","title_en":"Missionary Travels and Researches in South Africa",
     "author_kr":"데이비드 리빙스턴","author_en":"David Livingstone","year":"1857",
     "url":_gurl(1039),"gut":True,
     "note":"리빙스턴의 아프리카 선교 탐험 기록. 기독교 선교와 문명화의 선구적 여정을 담은 고전."},
    {"slug":"paton-autobiography","title":"존 페이턴 자서전","title_en":"The Story of John G. Paton",
     "author_kr":"존 패이턴","author_en":"John G. Paton","year":"1889",
     "url":_gurl(28025),"gut":True,
     "note":"남태평양 식인종 사이에서 30년간 사역한 선교사의 놀라운 자서전."},

    # F.B. Meyer (CCEL)
    {"slug":"meyer-way-into-holiest","title":"지성소로 가는 길","title_en":"The Way Into the Holiest",
     "author_kr":"F.B. 마이어","author_en":"F.B. Meyer","year":"1893",
     "url":_curl("meyer","into_holiest"),"gut":False,
     "note":"히브리서 강해. 그리스도를 통해 하나님의 임재로 나아가는 길을 안내하는 영성 고전."},
    {"slug":"meyer-christian-living","title":"하나님의 인도","title_en":"The Secret of Guidance",
     "author_kr":"F.B. 마이어","author_en":"F.B. Meyer","year":"1896",
     "url":_curl("meyer","guidance"),"gut":False,
     "note":"하나님의 뜻을 분별하고 인도받는 삶에 대한 마이어의 실용적 안내서."},

    # Flavel (CCEL)
    {"slug":"flavel-fountain-life","title":"생명의 샘","title_en":"The Fountain of Life",
     "author_kr":"존 플라벨 (John Flavel)","author_en":"John Flavel","year":"1671",
     "url":_curl("flavel","fountain"),"gut":False,
     "note":"그리스도의 중보자 사역을 42편의 설교로 풀어낸 청교도 그리스도론의 보물."},
    {"slug":"flavel-method-grace","title":"은혜의 방법","title_en":"The Method of Grace",
     "author_kr":"존 플라벨 (John Flavel)","author_en":"John Flavel","year":"1681",
     "url":_curl("flavel","grace"),"gut":False,
     "note":"성령의 역사로 그리스도가 영혼에 적용되는 과정을 다룬 청교도 구원론의 핵심 저작."},
    {"slug":"flavel-christ-altogether-lovely","title":"완전히 사랑스러우신 그리스도",
     "title_en":"Christ Altogether Lovely",
     "author_kr":"존 플라벨 (John Flavel)","author_en":"John Flavel","year":"1680",
     "url":_curl("flavel","lovely"),"gut":False,
     "note":"아가서 5:16을 기반으로 그리스도의 아름다움을 묘사한 감동적인 설교."},

    # NPNF Patristic (CCEL) - 3 key volumes
    {"slug":"athanasius-life-antony","title":"안토니우스의 생애 / 성육신론",
     "title_en":"Select Works of Athanasius (NPNF2 Vol.4)",
     "author_kr":"아타나시우스","author_en":"Athanasius of Alexandria","year":"~360",
     "url":_curl("schaff","npnf204"),"gut":False,
     "note":"아타나시우스의 주요 저작 선집. 안토니우스의 생애와 성육신론 등 초대교회 핵심 문헌."},
    {"slug":"basil-holy-spirit","title":"바실 대제 저작 선집",
     "title_en":"Select Works of Basil the Great (NPNF2 Vol.8)",
     "author_kr":"바실 대제 (Basil the Great)","author_en":"Basil the Great","year":"~375",
     "url":_curl("schaff","npnf208"),"gut":False,
     "note":"바실 대제의 성령론, 6일 창조 강해, 서신 선집. 카파도키아 교부의 핵심 저작."},
    {"slug":"gregory-nyssa-select","title":"닛사의 그레고리 저작 선집",
     "title_en":"Select Works of Gregory of Nyssa (NPNF2 Vol.5)",
     "author_kr":"닛사의 그레고리","author_en":"Gregory of Nyssa","year":"~385",
     "url":_curl("schaff","npnf205"),"gut":False,
     "note":"닛사의 그레고리 주요 저작. 모세의 생애, 대교리문답, 영혼과 부활에 관하여 등 수록."},
]


def main():
    do_dl = "--download" in sys.argv
    for info in BOOKS:
        fname = f"{info['slug']}.txt"
        cache = CACHE_DIR / fname
        if do_dl:
            raw = download(info["url"], cache)
        elif cache.exists():
            raw = cache.read_text(encoding="utf-8")
        else:
            print(f"\n[건너뜀] {fname}"); continue
        if raw:
            split_generic(raw, info["slug"], info["title"], info["title_en"],
                          info["author_kr"], info["author_en"], info["year"],
                          info["url"], info["note"], info.get("gut",False))

    print("\n" + "="*60 + "\n19차 배치 처리 완료! (2순위 Part A, 15권)")


if __name__ == "__main__":
    main()
