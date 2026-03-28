#!/usr/bin/env python3
"""Phase 5 도서 콘텐츠 확보 공용 유틸리티.

Gutenberg, CCEL, Archive.org에서 도서 텍스트를 다운로드하고
챕터 분할 + metadata.json 생성.
"""

import json, re, os, sys, time
import urllib.request
import urllib.parse
from pathlib import Path

BOOKS_DIR = Path("pipeline/sources/data/books")
CACHE_DIR = Path("/private/tmp/claude-501")
MAX_CHAPTER_WORDS = 8000
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Hearken/Phase5 visually-impaired project)"}

CACHE_DIR.mkdir(parents=True, exist_ok=True)


# ─── 다운로드 함수 ───

def download(url, dest, timeout=120):
    """URL에서 텍스트 다운로드, 캐시 활용."""
    if dest.exists() and dest.stat().st_size > 500:
        print(f"  [캐시] {dest.name}")
        return dest.read_text(encoding="utf-8", errors="replace")
    print(f"  [다운로드] {url}")
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
        text = data.decode("utf-8", errors="replace")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        return text
    except Exception as e:
        print(f"  [에러] {e}")
        return None


def gutenberg_url(eid):
    """Gutenberg 텍스트 URL."""
    return f"https://www.gutenberg.org/cache/epub/{eid}/pg{eid}.txt"


def gutenberg_url_alt(eid):
    """Gutenberg 대체 URL (UTF-8)."""
    return f"https://www.gutenberg.org/files/{eid}/{eid}-0.txt"


def ccel_url(author, work):
    """CCEL 텍스트 캐시 URL."""
    return f"https://ccel.org/ccel/{author}/{work}/cache/{work}.txt"


def ccel_url_alt(author, work):
    """CCEL HTML URL."""
    return f"https://www.ccel.org/ccel/{author}/{work}/{work}.html"


def archive_search(title, author="", max_results=5):
    """Archive.org에서 도서 검색, identifier 목록 반환."""
    words = title.split()[:6]
    q_title = " ".join(words)
    q = f'title:({q_title})'
    if author:
        author_clean = author.split("(")[0].split(",")[0].strip()
        q += f' AND creator:({author_clean})'
    q += ' AND mediatype:(texts)'
    url = (
        f"https://archive.org/advancedsearch.php?"
        f"q={urllib.parse.quote(q)}&fl[]=identifier&rows={max_results}&output=json"
    )
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
        docs = data.get("response", {}).get("docs", [])
        return [d["identifier"] for d in docs]
    except Exception as e:
        print(f"  [Archive 검색 에러] {e}")
        return []


def archive_download_text(identifier, slug):
    """Archive.org에서 텍스트 파일 다운로드 시도."""
    patterns = [
        f"https://archive.org/download/{identifier}/{identifier}_djvu.txt",
        f"https://archive.org/download/{identifier}/{identifier}.txt",
    ]
    for url in patterns:
        cache = CACHE_DIR / f"{slug}_archive.txt"
        text = download(url, cache)
        if text and len(text) > 1000:
            return text, f"https://archive.org/details/{identifier}"
        # 캐시 파일이 너무 작으면 삭제하고 다음 패턴 시도
        if cache.exists() and cache.stat().st_size < 1000:
            cache.unlink()
    return None, None


# ─── 텍스트 정리 함수 ───

def clean(t):
    return re.sub(r"\n{4,}", "\n\n\n", re.sub(r"_{5,}", "", t)).strip()


def extract_gut(t):
    """Gutenberg 헤더/푸터 제거."""
    for s in ["*** START OF THE PROJECT GUTENBERG", "*** START OF THIS PROJECT GUTENBERG"]:
        i = t.find(s)
        if i != -1:
            t = t[i:].split("\n", 1)[1] if "\n" in t[i:] else t[i:]
            break
    for e in ["*** END OF THE PROJECT GUTENBERG", "*** END OF THIS PROJECT GUTENBERG",
              "End of the Project Gutenberg", "End of Project Gutenberg"]:
        i = t.find(e)
        if i != -1:
            t = t[:i]
            break
    return t.strip()


def strip_ccel(t):
    """CCEL 헤더 제거."""
    for mk in ["Generated on", "This document has been generated"]:
        i = t.find(mk)
        if i != -1 and i < 2000:
            nl = t[i:].find("\n\n")
            if nl != -1:
                t = t[i + nl:].strip()
                break
    return t


def strip_archive(t):
    """Archive.org OCR 아티팩트 정리."""
    # 공통 Archive.org 헤더 패턴 제거
    for mk in ["Full text of", "Digitized by Google", "UNIVERSITY OF", "Digitized by"]:
        i = t.find(mk)
        if i != -1 and i < 3000:
            nl = t[i:].find("\n\n")
            if nl != -1:
                t = t[i + nl:].strip()
    return t


# ─── 챕터 분할 ───

def split_para(t, mx=MAX_CHAPTER_WORDS):
    if len(t.split()) <= mx:
        return [t]
    ps = [p for p in t.split("\n\n") if p.strip()]
    cks, cur, cw = [], [], 0
    for p in ps:
        pw = len(p.split())
        if cw + pw > mx and cur:
            cks.append("\n\n".join(cur))
            cur, cw = [], 0
        cur.append(p)
        cw += pw
    if cur:
        cks.append("\n\n".join(cur))
    return cks or [t]


_R = {r: i for i, r in enumerate(
    ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
     "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX",
     "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX",
     "XXXI", "XXXII", "XXXIII", "XXXIV", "XXXV", "XXXVI", "XXXVII", "XXXVIII", "XXXIX", "XL"]
)}


def find_chapters(text, min_w=50):
    """여러 패턴으로 챕터 구조 탐지."""
    patterns = [
        r"\n\s*CHAPTER\s+([IVXLC]+|\d+)\.?\s*\n",
        r"\n\s*Chapter\s+([IVXLC]+|\d+)\.?\s*\n",
        r"\n\s*SERMON\s+([IVXLC]+|\d+)\.?\s*\n",
        r"\n\s*Sermon\s+([IVXLC]+|\d+)\.?\s*\n",
        r"\n\s*LETTER\s+([IVXLC]+|\d+)\.?\s*\n",
        r"\n\s*Letter\s+([IVXLC]+|\d+)\.?\s*\n",
        r"\n\s*LECTURE\s+([IVXLC]+|\d+)\.?\s*\n",
        r"\n\s*Lecture\s+([IVXLC]+|\d+)\.?\s*\n",
        r"\n\s*PART\s+([IVXLC]+|\d+)\.?\s*\n",
        r"\n\s*Part\s+([IVXLC]+|\d+)\.?\s*\n",
        r"\n\s*SECTION\s+([IVXLC]+|\d+)\.?\s*\n",
        r"\n\s*BOOK\s+([IVXLC]+|\d+)\.?\s*\n",
    ]
    for pat_str in patterns:
        pat = re.compile(pat_str)
        ms = list(pat.finditer(text))
        if len(ms) >= 3:
            chs = _extract_chapters(text, ms, min_w)
            if chs:
                return chs
    return []


def _extract_chapters(text, ms, min_w):
    """매치 목록에서 챕터 추출."""
    # 중복 Chapter I 제거 (서문과 본문)
    ch1 = [m for m in ms if (_R.get(m.group(1).upper(), 0) == 1 or m.group(1) == "1")]
    if len(ch1) >= 2:
        ms = [m for m in ms if m.start() >= ch1[-1].start()]

    chs = []
    for i, m in enumerate(ms):
        raw = m.group(1).strip()
        num = _R.get(raw.upper(), 0) or (int(raw) if raw.isdigit() else i + 1)
        s, e = m.start(), ms[i + 1].start() if i + 1 < len(ms) else len(text)
        body = text[s:e].strip()
        lines = body.split("\n", 5)
        tl = ""
        for l in lines[1:4]:
            x = l.strip()
            if x and not re.match(
                r"(CHAPTER|SERMON|LETTER|LECTURE|PART|SECTION|BOOK)\s", x, re.IGNORECASE
            ):
                tl = x.rstrip(".")
                break
        if len(body.split()) >= min_w:
            chs.append((num, tl, body))
    return chs


# ─── 도서 처리 ───

def process_book(raw, info, source_type="auto"):
    """단일 도서: 텍스트 → 챕터 분할 → 파일 저장."""
    slug = info["slug"]

    # 텍스트 정리
    if source_type == "gutenberg":
        text = clean(extract_gut(raw))
    elif source_type == "ccel":
        text = clean(strip_ccel(raw))
    elif source_type == "archive":
        text = clean(strip_archive(raw))
    else:
        # 자동 감지
        if "PROJECT GUTENBERG" in raw[:5000]:
            text = clean(extract_gut(raw))
        elif "Generated on" in raw[:2000] or "ccel.org" in raw[:2000]:
            text = clean(strip_ccel(raw))
        else:
            text = clean(raw)

    out_dir = BOOKS_DIR / slug
    chs = find_chapters(text)
    if not chs:
        parts = split_para(text)
        chs = [(i + 1, "", p) for i, p in enumerate(parts)]

    cm = []
    for num, tl, body in chs:
        title = f"제{num}장: {tl}" if tl else f"제{num}장"
        body = re.sub(r"\n{3,}", "\n\n", body)
        for pi, p in enumerate(split_para(body)):
            fn = len(cm) + 1
            parts_count = len(split_para(body))
            sfx = f" ({pi+1}/{parts_count})" if parts_count > 1 else ""
            ct = f"{title}{sfx}"
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / f"ch{fn:02d}.txt").write_text(f"{ct}\n\n{p.strip()}\n", encoding="utf-8")
            cm.append({"num": fn, "title": ct, "file": f"ch{fn:02d}.txt"})

    meta = {
        "slug": slug,
        "title": info["title"],
        "title_original": info["title_en"],
        "author": info["author_kr"],
        "author_original": info.get("author_en", ""),
        "year": info.get("year", ""),
        "source": info.get("source_url", ""),
        "license": "public_domain",
        "note": info.get("note", ""),
        "chapters": cm,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "metadata.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"  ✅ {slug}: {len(cm)}챕터")
    return len(cm)


# ─── 통합 다운로드 + 처리 ───

def try_download(info, delay=1.0):
    """도서의 여러 소스를 시도하여 다운로드 + 처리."""
    slug = info["slug"]

    # 이미 처리 완료?
    meta_path = BOOKS_DIR / slug / "metadata.json"
    if meta_path.exists():
        print(f"  [건너뜀] {slug} (이미 존재)")
        return "skipped"

    raw = None
    source_type = "auto"
    source_url = ""

    # 1. Gutenberg (ID가 있으면)
    if info.get("gutenberg_id"):
        gid = info["gutenberg_id"]
        for url_fn in [gutenberg_url, gutenberg_url_alt]:
            url = url_fn(gid)
            cache = CACHE_DIR / f"{slug}_gut.txt"
            raw = download(url, cache)
            if raw and len(raw) > 1000 and "PROJECT GUTENBERG" in raw[:5000].upper():
                source_type = "gutenberg"
                source_url = url
                break
            if cache.exists() and cache.stat().st_size < 1000:
                cache.unlink()
                raw = None
        time.sleep(0.5)

    # 2. CCEL (경로가 있으면)
    if not raw and info.get("ccel_author") and info.get("ccel_work"):
        url = ccel_url(info["ccel_author"], info["ccel_work"])
        cache = CACHE_DIR / f"{slug}_ccel.txt"
        raw = download(url, cache)
        if raw and len(raw) > 500:
            source_type = "ccel"
            source_url = url
        else:
            # HTML 버전 시도
            url2 = ccel_url_alt(info["ccel_author"], info["ccel_work"])
            cache2 = CACHE_DIR / f"{slug}_ccel_html.txt"
            raw = download(url2, cache2)
            if raw and len(raw) > 500:
                # HTML → text
                raw = _html_to_text(raw)
                source_type = "ccel"
                source_url = url2
            else:
                raw = None
        time.sleep(0.5)

    # 3. Archive.org 검색
    if not raw:
        title_en = info.get("title_en", "")
        author_en = info.get("author_en", "")
        identifiers = archive_search(title_en, author_en)
        for ident in identifiers[:3]:
            text, src_url = archive_download_text(ident, slug)
            if text and len(text) > 1000:
                raw = text
                source_type = "archive"
                source_url = src_url
                break
            time.sleep(0.5)
        time.sleep(delay)

    # 4. 직접 URL
    if not raw and info.get("direct_url"):
        cache = CACHE_DIR / f"{slug}_direct.txt"
        raw = download(info["direct_url"], cache)
        if raw and len(raw) > 500:
            source_url = info["direct_url"]

    if raw and len(raw) > 500:
        info["source_url"] = source_url
        count = process_book(raw, info, source_type)
        return "success"
    else:
        print(f"  ❌ {slug}: 소스를 찾을 수 없음")
        return "failed"


def _html_to_text(html):
    """HTML → 텍스트 변환."""
    t = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    t = re.sub(r'<style[^>]*>.*?</style>', '', t, flags=re.DOTALL)
    t = re.sub(r'<br\s*/?>', '\n', t, flags=re.IGNORECASE)
    t = re.sub(r'<p[^>]*>', '\n\n', t, flags=re.IGNORECASE)
    t = re.sub(r'<h\d[^>]*>', '\n\n', t, flags=re.IGNORECASE)
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'&nbsp;', ' ', t)
    t = re.sub(r'&amp;', '&', t)
    t = re.sub(r'&lt;', '<', t)
    t = re.sub(r'&gt;', '>', t)
    t = re.sub(r'&#\d+;', '', t)
    t = re.sub(r'\n{4,}', '\n\n\n', t)
    return t.strip()


def process_all(books, delay=1.5):
    """모든 도서 일괄 처리."""
    total = len(books)
    results = {"success": 0, "failed": 0, "skipped": 0}
    failed_books = []

    for i, info in enumerate(books, 1):
        print(f"\n[{i}/{total}] {info['slug']} — {info['title']}")
        status = try_download(info, delay)
        results[status] = results.get(status, 0) + 1
        if status == "failed":
            failed_books.append(info["slug"])

    print(f"\n{'='*60}")
    print(f"성공: {results['success']}, 실패: {results['failed']}, "
          f"건너뜀: {results['skipped']}, 전체: {total}")
    if failed_books:
        print(f"실패 목록:")
        for slug in failed_books:
            print(f"  - {slug}")
    return results, failed_books
