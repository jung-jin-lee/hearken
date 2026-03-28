#!/usr/bin/env python3
"""Phase 5 번역 결과 다운로드 및 content/books 배포.

사용법:
  python pipeline/scripts/fetch_and_deploy_p5.py          # 완료된 것만 fetch
  python pipeline/scripts/fetch_and_deploy_p5.py --check  # 상태만 확인
"""
import sys, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

BATCH_LOG = Path("pipeline/scripts/bulk_batch_ids_p5.json")


def cmd_check():
    from pipeline.batch.submitter import check_batch_status
    import json

    if not BATCH_LOG.exists():
        print("배치 로그 없음"); return

    batch_ids = json.loads(BATCH_LOG.read_text())
    completed, in_progress, failed = 0, 0, 0
    for slug, bid in sorted(batch_ids.items()):
        if not bid.startswith("batch_"):
            continue
        s = check_batch_status(bid)
        st = s["status"]
        d, t = s.get("completed", 0), s.get("total", 0)
        if st == "completed":
            completed += 1
        elif st in ("failed", "expired", "cancelled"):
            failed += 1
            print(f"  ❌ {slug:45s} {st}")
        else:
            in_progress += 1
            print(f"  🔄 {slug:45s} {st:12s} {d}/{t}")

    print(f"\n✅ 완료: {completed}  🔄 진행중: {in_progress}  ❌ 실패: {failed}  합계: {len(batch_ids)}")


def cmd_fetch():
    from pipeline.batch.submitter import check_batch_status
    from pipeline.batch.downloader import download_and_parse
    from pipeline.processors.structurer import save_json
    from pipeline.config import CONTENT_DIR, SOURCES_DATA_DIR
    import json

    if not BATCH_LOG.exists():
        print("배치 로그 없음"); return

    batch_ids = json.loads(BATCH_LOG.read_text())
    fetched, skipped, pending = 0, 0, 0

    for slug, bid in sorted(batch_ids.items()):
        if not bid.startswith("batch_"):
            continue

        out_dir = CONTENT_DIR / "books" / slug
        if out_dir.exists() and list(out_dir.glob("*.json")):
            skipped += 1
            continue

        s = check_batch_status(bid)
        if s["status"] != "completed" or not s.get("output_file_id"):
            pending += 1
            continue

        meta_path = SOURCES_DATA_DIR / "books" / slug / "metadata.json"
        if not meta_path.exists():
            print(f"  ⚠️  {slug}: metadata.json 없음 - 건너뜀")
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


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true", help="상태 확인만")
    args = p.parse_args()

    if args.check:
        cmd_check()
    else:
        print("=== 상태 확인 ===")
        cmd_check()
        print("\n=== 완료된 배치 fetch ===")
        cmd_fetch()
