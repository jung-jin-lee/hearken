#!/usr/bin/env python3
"""범용 대량 도서 처리기.

books_manifest.json에서 도서 목록을 읽고 일괄 다운로드/분할/제출/다운로드 처리.

사용법:
  python pipeline/scripts/bulk_processor.py download   # 텍스트 다운로드 + 분할
  python pipeline/scripts/bulk_processor.py submit      # Batch API 제출
  python pipeline/scripts/bulk_processor.py check       # 상태 확인
  python pipeline/scripts/bulk_processor.py fetch       # 완료된 결과 다운로드
  python pipeline/scripts/bulk_processor.py status      # 전체 현황
"""

import json, re, sys, os, argparse
from pathlib import Path

BOOKS_DIR = Path("pipeline/sources/data/books")
CACHE_DIR = Path("/private/tmp/claude-501")
MANIFEST = Path("pipeline/scripts/books_manifest.json")
BATCH_LOG = Path("pipeline/scripts/bulk_batch_ids.json")
MAX_CHAPTER_WORDS = 8000


def _parse_args():
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("command", nargs="?")
    p.add_argument("--manifest", type=Path)
    p.add_argument("--batch-log", type=Path)
    args, _ = p.parse_known_args()
    return args


# ─── 유틸리티 ───

def dl(url, dest):
    import urllib.request
    if dest.exists() and dest.stat().st_size > 500:
        return dest.read_text(encoding="utf-8")
    print(f"  [다운로드] {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=180) as r:
            data = r.read()
    except Exception as e:
        print(f"  [에러] {e}"); return None
    text = data.decode("utf-8", errors="replace")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    return text

def clean(t):
    return re.sub(r"\n{4,}", "\n\n\n", re.sub(r"_{5,}", "", t)).strip()

def extract_gut(t):
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
    for mk in ["Generated on", "This document has been generated"]:
        i = t.find(mk)
        if i != -1 and i < 2000:
            nl = t[i:].find("\n\n")
            if nl != -1:
                t = t[i + nl:].strip()
                break
    return t

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
     "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX"]
)}

def find_chapters(text, min_w=50):
    pat = re.compile(r"\n\s*CHAPTER\s+([IVXLC]+|\d+)\.?\s*\n", re.IGNORECASE)
    ms = list(pat.finditer(text))
    ch1 = [m for m in ms if (_R.get(m.group(1).upper(), 0) == 1 or m.group(1) == "1")]
    if len(ch1) >= 2:
        ms = [m for m in ms if m.start() >= ch1[1].start()]
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
            if x and not re.match(r"CHAPTER\s", x, re.IGNORECASE):
                tl = x.rstrip(".")
                break
        if len(body.split()) >= min_w:
            chs.append((num, tl, body))
    return chs


def process_book(raw, info):
    """단일 도서 처리: 텍스트 → 챕터 분할 → 파일 저장."""
    slug = info["slug"]
    is_gut = info.get("source_type") == "gutenberg"

    text = clean(extract_gut(raw)) if is_gut else clean(strip_ccel(raw))
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
            sfx = f" ({pi+1}/{len(split_para(body))})" if len(split_para(body)) > 1 else ""
            ct = f"{title}{sfx}"
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / f"ch{fn:02d}.txt").write_text(f"{ct}\n\n{p.strip()}\n", encoding="utf-8")
            cm.append({"num": fn, "title": ct, "file": f"ch{fn:02d}.txt"})

    meta = {
        "slug": slug,
        "title": info["title"],
        "title_original": info["title_en"],
        "author": info["author_kr"],
        "author_original": info["author_en"],
        "year": info.get("year", ""),
        "source": info["url"],
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


# ─── 명령어 ───

def cmd_download():
    """매니페스트의 모든 도서를 다운로드하고 분할."""
    manifest = json.loads(MANIFEST.read_text())
    total, done, skipped = len(manifest), 0, 0

    for info in manifest:
        slug = info["slug"]
        # 이미 소스가 있으면 건너뜀
        meta_path = BOOKS_DIR / slug / "metadata.json"
        if meta_path.exists():
            skipped += 1
            continue

        cache = CACHE_DIR / f"{slug}.txt"
        raw = dl(info["url"], cache)
        if raw:
            process_book(raw, info)
            done += 1
        else:
            skipped += 1

    print(f"\n처리: {done}, 건너뜀: {skipped}, 전체: {total}")


def cmd_submit():
    """분할된 도서를 Batch API에 제출."""
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from pipeline.batch.builder import build_jsonl
    from pipeline.batch.submitter import submit_batch
    from pipeline.prompts.book_processing import build_book_processing_request
    from pipeline.config import CONTENT_DIR

    manifest = json.loads(MANIFEST.read_text())
    batch_ids = {}
    if BATCH_LOG.exists():
        batch_ids = json.loads(BATCH_LOG.read_text())

    submitted = 0
    for info in manifest:
        slug = info["slug"]
        # 이미 제출됨 또는 이미 콘텐츠 있음
        if slug in batch_ids:
            continue
        content_dir = CONTENT_DIR / "books" / slug
        if content_dir.exists() and list(content_dir.glob("*.json")):
            continue

        meta_path = BOOKS_DIR / slug / "metadata.json"
        if not meta_path.exists():
            continue

        meta = json.loads(meta_path.read_text())
        book_dir = BOOKS_DIR / slug
        requests = []
        for ch in meta["chapters"]:
            ch_path = book_dir / ch["file"]
            if not ch_path.exists():
                continue
            text = ch_path.read_text(encoding="utf-8")
            req = build_book_processing_request(
                book_slug=slug, book_title=meta["title"],
                author=meta["author"], chapter_num=ch["num"],
                chapter_text=text,
            )
            requests.append(req)

        if not requests:
            continue

        path = build_jsonl(requests, f"book_{slug}")
        bid = submit_batch(path, f"book_{slug}")
        batch_ids[slug] = bid
        submitted += 1
        print(f"  📤 {slug}: {len(requests)}챕터 → {bid}")

        # 중간 저장
        BATCH_LOG.write_text(json.dumps(batch_ids, indent=2))

    BATCH_LOG.write_text(json.dumps(batch_ids, indent=2))
    print(f"\n제출: {submitted}권")


def cmd_check():
    """배치 상태 확인."""
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from pipeline.batch.submitter import check_batch_status

    if not BATCH_LOG.exists():
        print("배치 로그 없음"); return

    batch_ids = json.loads(BATCH_LOG.read_text())
    completed, pending = 0, 0
    for slug, bid in batch_ids.items():
        if not bid.startswith("batch_"):
            continue
        s = check_batch_status(bid)
        st = s["status"]
        d, t = s.get("completed", 0), s.get("total", 0)
        if st == "completed":
            completed += 1
        else:
            pending += 1
            print(f"  🔄 {slug:40s} {st:12s} {d}/{t}")

    print(f"\n✅ 완료: {completed}, 🔄 진행중: {pending}")


def cmd_fetch():
    """완료된 배치 결과 다운로드."""
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from pipeline.batch.submitter import check_batch_status
    from pipeline.batch.downloader import download_and_parse
    from pipeline.processors.structurer import save_json
    from pipeline.config import CONTENT_DIR

    if not BATCH_LOG.exists():
        print("배치 로그 없음"); return

    batch_ids = json.loads(BATCH_LOG.read_text())
    fetched = 0

    for slug, bid in batch_ids.items():
        if not bid.startswith("batch_"):
            continue
        out_dir = CONTENT_DIR / "books" / slug
        if out_dir.exists() and list(out_dir.glob("*.json")):
            continue

        s = check_batch_status(bid)
        if s["status"] != "completed" or not s.get("output_file_id"):
            continue

        meta_path = BOOKS_DIR / slug / "metadata.json"
        if not meta_path.exists():
            continue
        meta = json.loads(meta_path.read_text())

        results = download_and_parse(s["output_file_id"], f"book_{slug}")
        ch_map = {ch["num"]: ch for ch in meta["chapters"]}
        out_dir.mkdir(parents=True, exist_ok=True)
        saved = 0
        for cid, data in results.items():
            if "_error" in data:
                continue
            parts = cid.rsplit("-ch", 1)
            if len(parts) != 2:
                continue
            ch_num = int(parts[1])
            ch_info = ch_map.get(ch_num, {})
            output = {
                "book_slug": slug, "book_title": meta["title"],
                "author": meta.get("author", ""), "chapter_num": ch_num,
                "chapter_title": ch_info.get("title", f"{ch_num}장"),
                **data,
            }
            save_json(output, out_dir / f"{ch_num:03d}.json")
            saved += 1

        errors = sum(1 for v in results.values() if "_error" in v)
        print(f"  📥 {slug}: {saved} 성공, {errors} 실패")
        fetched += 1

    print(f"\n다운로드: {fetched}권")


def cmd_status():
    """전체 현황."""
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else []
    from pathlib import Path as P
    content_dir = P("content/books")
    source_dir = BOOKS_DIR

    total_catalog = len(manifest)
    has_source = sum(1 for i in manifest if (source_dir / i["slug"] / "metadata.json").exists())
    has_content = sum(1 for i in manifest if (content_dir / i["slug"]).exists() and list((content_dir / i["slug"]).glob("*.json")))

    print(f"매니페스트: {total_catalog}권")
    print(f"소스 준비: {has_source}권")
    print(f"콘텐츠 완료: {has_content}권")
    print(f"미처리: {total_catalog - has_content}권")


if __name__ == "__main__":
    args = _parse_args()
    if not args.command:
        print("사용법: bulk_processor.py [download|submit|check|fetch|status] [--manifest PATH] [--batch-log PATH]")
        sys.exit(1)

    if args.manifest:
        MANIFEST = args.manifest
    if args.batch_log:
        BATCH_LOG = args.batch_log

    cmd = args.command
    {"download": cmd_download, "submit": cmd_submit, "check": cmd_check,
     "fetch": cmd_fetch, "status": cmd_status}[cmd]()
