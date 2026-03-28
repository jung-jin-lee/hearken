#!/usr/bin/env python3
"""Batch F 영어 도서 10권 — OpenAI 배치 제출 및 결과 배포.

사용법:
  python pipeline/scripts/submit_batch_f.py submit   # 배치 제출
  python pipeline/scripts/submit_batch_f.py check    # 상태 확인
  python pipeline/scripts/submit_batch_f.py fetch    # 완료된 것 배포
"""
import sys, json, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.batch.builder import build_jsonl
from pipeline.batch.downloader import download_and_parse
from pipeline.batch.submitter import check_batch_status, submit_batch
from pipeline.config import CONTENT_DIR, SOURCES_DATA_DIR
from pipeline.processors.structurer import save_json
from pipeline.prompts.book_processing import build_book_processing_request

SLUGS = [
    "luther-freedom-christian",
    "perkins-art-prophesying",
    "vincent-shorter-catechism",
    "fenelon-christian-perfection",
    "thomas-scott-force-truth",
    "meyer-abraham",
    "meyer-joseph",
    "chambers-still-higher",
    "desales-devout-life",
    "taylor-retrospect",
]

BATCH_LOG = Path("pipeline/scripts/bulk_batch_ids_batch_f.json")
BOOKS_DIR = SOURCES_DATA_DIR / "books"


def load_log() -> dict:
    if BATCH_LOG.exists():
        return json.loads(BATCH_LOG.read_text())
    return {}


def save_log(data: dict):
    BATCH_LOG.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_submit():
    log = load_log()
    for slug in SLUGS:
        if slug in log:
            print(f"[건너뜀] {slug} (이미 제출됨: {log[slug]})")
            continue

        meta_path = BOOKS_DIR / slug / "metadata.json"
        if not meta_path.exists():
            print(f"[스킵] {slug}: metadata.json 없음 (phase5_batch_f.py 먼저 실행)")
            continue

        meta = json.loads(meta_path.read_text())
        requests = []
        for ch_info in meta["chapters"]:
            ch_path = BOOKS_DIR / slug / ch_info["file"]
            if not ch_path.exists():
                continue
            text = ch_path.read_text(encoding="utf-8")
            req = build_book_processing_request(
                book_slug=slug,
                book_title=meta["title"],
                author=meta["author"],
                chapter_num=ch_info["num"],
                chapter_text=text,
            )
            requests.append(req)

        if not requests:
            print(f"[스킵] {slug}: 챕터 파일 없음")
            continue

        jsonl_path = build_jsonl(requests, f"book_{slug}")
        bid = submit_batch(jsonl_path, f"batch_f_{slug}")
        log[slug] = bid
        save_log(log)
        print(f"  ✅ {slug}: {bid} ({len(requests)}챕터)")

    print(f"\n배치 로그: {BATCH_LOG}")


def cmd_check():
    log = load_log()
    if not log:
        print("배치 로그 없음")
        return

    completed, in_progress, failed = 0, 0, 0
    for slug, bid in sorted(log.items()):
        s = check_batch_status(bid)
        st = s["status"]
        d, t = s.get("completed", 0), s.get("total", 0)
        if st == "completed":
            completed += 1
            print(f"  ✅ {slug:45s} 완료")
        elif st in ("failed", "expired", "cancelled"):
            failed += 1
            print(f"  ❌ {slug:45s} {st}")
        else:
            in_progress += 1
            print(f"  🔄 {slug:45s} {st:12s} {d}/{t}")

    print(f"\n✅ 완료: {completed}  🔄 진행중: {in_progress}  ❌ 실패: {failed}")


def cmd_fetch():
    log = load_log()
    if not log:
        print("배치 로그 없음")
        return

    fetched, skipped, pending = 0, 0, 0
    for slug, bid in sorted(log.items()):
        out_dir = CONTENT_DIR / "books" / slug
        if out_dir.exists() and list(out_dir.glob("*.json")):
            skipped += 1
            continue

        s = check_batch_status(bid)
        if s["status"] != "completed" or not s.get("output_file_id"):
            pending += 1
            print(f"  ⏳ {slug}: 아직 대기 중 ({s['status']})")
            continue

        meta_path = BOOKS_DIR / slug / "metadata.json"
        if not meta_path.exists():
            print(f"  ⚠️  {slug}: metadata.json 없음")
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
                "book_slug": slug,
                "book_title": meta["title"],
                "author": meta.get("author", ""),
                "chapter_num": ch_num,
                "chapter_title": ch_info.get("title", f"{ch_num}장"),
                **data,
            }
            save_json(output, out_dir / f"{ch_num:03d}.json")
            saved += 1

        errors = sum(1 for v in results.values() if "_error" in v)
        print(f"  📥 {slug}: {saved}챕터 저장, {errors}실패")
        fetched += 1

    print(f"\n완료: 신규 {fetched}권 배포, {skipped}권 이미 완료, {pending}권 대기중")


def main():
    p = argparse.ArgumentParser(description="Batch F 제출/확인/배포")
    p.add_argument("action", choices=["submit", "check", "fetch"])
    args = p.parse_args()

    if args.action == "submit":
        cmd_submit()
    elif args.action == "check":
        cmd_check()
    elif args.action == "fetch":
        cmd_fetch()


if __name__ == "__main__":
    main()
