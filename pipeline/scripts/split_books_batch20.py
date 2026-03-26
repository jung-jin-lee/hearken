#!/usr/bin/env python3
"""20차 도서 12권 분할 — 2순위 Part B (NPNF 교부 + Gutenberg 선교/변증).

대상:
  NPNF 교부:
  1. Gregory of Nazianzus (NPNF2 Vol.7)
  2. Augustine Select Works (NPNF1 Vol.3)
  3. Chrysostom: Homilies on Matthew sel. (NPNF1 Vol.10)
  4. Ambrose Select Works (NPNF2 Vol.10)
  5. Leo the Great & Gregory the Great (NPNF2 Vol.12)

  Gutenberg:
  6. Paley: Evidences of Christianity (#22856 or search)
  7. Butler: Fifteen Sermons (#2091 or search)
  8. Chesterton: Father Brown Wisdom (#223)
  9. Finney: Lectures on Revival
  10. Kierkegaard: Purity of Heart

  Gutenberg 추가 선교:
  11. Carey: An Enquiry into Obligations
  12. Hudson Taylor Spiritual Secret

사용법:
  python pipeline/scripts/split_books_batch20.py [--download]
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
        with urllib.request.urlopen(req, timeout=180) as r: data = r.read()
    except Exception as e:
        print(f"  [에러] {e}"); return None
    text = data.decode("utf-8", errors="replace")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8"); return text

def clean(t): return re.sub(r"\n{4,}","\n\n\n",re.sub(r"_{5,}","",t)).strip()
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
            fn=len(cm)+1; sfx=f" ({pi+1}/{len(split_para(body))})" if len(split_para(body))>1 else ""
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

BOOKS = [
    # NPNF 교부
    {"slug":"gregory-naz-theological","title":"나지안주스의 그레고리 신학 강론",
     "title_en":"Select Orations of Gregory Nazianzen (NPNF2 Vol.7)",
     "author_kr":"나지안주스의 그레고리","author_en":"Gregory of Nazianzus","year":"~380",
     "url":_curl("schaff","npnf207"),"gut":False,
     "note":"카파도키아 3교부 중 한 명. '신학자'라는 칭호를 받은 그레고리의 다섯 신학 강론 등 수록."},
    {"slug":"augustine-enchiridion","title":"아우구스티누스 선집 (NPNF1 Vol.3)",
     "title_en":"Select Works of Augustine (NPNF1 Vol.3)",
     "author_kr":"아우구스티누스","author_en":"Augustine of Hippo","year":"~420",
     "url":_curl("schaff","npnf103"),"gut":False,
     "note":"아우구스티누스의 주요 저작 선집. 엔키리디온, 기독교 교리론, 삼위일체론 선집 등 수록."},
    {"slug":"chrysostom-matthew-select","title":"크리소스톰 마태복음 강해 선집",
     "title_en":"Homilies on Matthew (NPNF1 Vol.10)",
     "author_kr":"요한 크리소스톰","author_en":"John Chrysostom","year":"~390",
     "url":_curl("schaff","npnf110"),"gut":False,
     "note":"'황금의 입' 크리소스톰의 마태복음 강해. 초대교회 최고의 설교자의 성경 해석."},
    {"slug":"ambrose-select","title":"암브로시우스 선집",
     "title_en":"Select Works of Ambrose (NPNF2 Vol.10)",
     "author_kr":"암브로시우스","author_en":"Ambrose of Milan","year":"~390",
     "url":_curl("schaff","npnf210"),"gut":False,
     "note":"밀라노의 암브로시우스 주요 저작. 성직자의 의무, 성령론 등 서방교회 핵심 문헌."},
    {"slug":"leo-gregory-great","title":"레오/그레고리 대교황 선집",
     "title_en":"Leo the Great & Gregory the Great (NPNF2 Vol.12)",
     "author_kr":"레오 대교황, 그레고리 대교황","author_en":"Leo & Gregory the Great","year":"~450/600",
     "url":_curl("schaff","npnf212"),"gut":False,
     "note":"레오 대교황의 설교 선집과 그레고리 대교황의 사목 규칙. 초대교회 지도력의 정수."},

    # Gutenberg 변증학/선교
    {"slug":"chesterton-father-brown-v2","title":"브라운 신부의 지혜",
     "title_en":"The Wisdom of Father Brown",
     "author_kr":"G.K. 체스터턴","author_en":"G.K. Chesterton","year":"1914",
     "url":_gurl(223),"gut":True,
     "note":"브라운 신부 추리소설 시리즈 제2권. 범죄와 인간 본성에 대한 신부의 깊은 통찰."},
    {"slug":"pascal-provincial-letters","title":"시골 친구에게 보내는 편지",
     "title_en":"The Provincial Letters",
     "author_kr":"블레즈 파스칼","author_en":"Blaise Pascal","year":"1657",
     "url":_gurl(46921),"gut":True,
     "note":"파스칼이 예수회의 도덕 이완주의를 비판한 서신. 프랑스 산문의 걸작."},
    {"slug":"tolstoy-kingdom-god","title":"하나님의 나라는 너희 안에 있다",
     "title_en":"The Kingdom of God Is Within You",
     "author_kr":"레프 톨스토이","author_en":"Leo Tolstoy","year":"1894",
     "url":_gurl(4602),"gut":True,
     "note":"톨스토이의 기독교 비폭력 사상의 핵심 저작. 간디에게도 큰 영향을 미친 책."},
    {"slug":"kierkegaard-purity-heart","title":"마음의 순결",
     "title_en":"Purity of Heart Is to Will One Thing",
     "author_kr":"쇠렌 키에르케고르","author_en":"Søren Kierkegaard","year":"1847",
     "url":_gurl(53017),"gut":True,
     "note":"키에르케고르의 영적 강연. 순결한 마음으로 단 하나를 원하는 것의 의미를 탐구."},

    # Gutenberg 선교 전기 추가
    {"slug":"carey-enquiry","title":"기독교인의 의무에 관한 탐구",
     "title_en":"An Enquiry into the Obligations of Christians",
     "author_kr":"윌리엄 캐리","author_en":"William Carey","year":"1792",
     "url":_gurl(11449),"gut":True,
     "note":"근대 선교운동의 시작점이 된 캐리의 역사적 소책자. 이방인 선교의 의무를 논증."},
    {"slug":"taylor-spiritual-secret","title":"허드슨 테일러의 영적 비결",
     "title_en":"Hudson Taylor's Spiritual Secret",
     "author_kr":"하워드 & 제럴딘 테일러","author_en":"Howard & Geraldine Taylor","year":"1932",
     "url":_gurl(23891),"gut":True,
     "note":"중국 내지 선교회 창설자 허드슨 테일러의 영적 성장과 믿음의 삶을 기록한 전기."},
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
    print("\n" + "="*60 + "\n20차 배치 처리 완료! (2순위 Part B, 12권)")

if __name__ == "__main__":
    main()
