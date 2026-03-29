#!/usr/bin/env python3
"""Phase 6 Batch API 모니터 — 20분 주기 폴링 + 완료 시 자동 다운로드.

bulk_batch_ids_p6.json 을 읽어 미완료 배치를 20분마다 폴링하고,
완료된 배치는 즉시 content/books/{slug}/ 에 저장한다.
모든 배치가 완료되거나 --once 플래그가 있으면 종료한다.

사용법:
  python pipeline/scripts/phase6_monitor.py           # 루프 모드 (기본)
  python pipeline/scripts/phase6_monitor.py --once    # 1회만 체크
  python pipeline/scripts/phase6_monitor.py --interval 10  # 10분 간격
"""
import sys, json, time, argparse
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

BOOKS_DIR = Path("pipeline/sources/data/books")
BATCH_LOG = Path("pipeline/scripts/bulk_batch_ids_p6.json")
TERMINAL = {"completed", "failed", "expired", "cancelled"}


def ts():
    return datetime.now().strftime("%H:%M:%S")


def fetch_one(slug: str, bid: str, status_info: dict) -> bool:
    """완료된 배치 1개 다운로드. 성공 여부 반환."""
    from pipeline.batch.downloader import download_and_parse
    from pipeline.processors.structurer import save_json
    from pipeline.config import CONTENT_DIR

    output_file_id = status_info.get("output_file_id")
    if not output_file_id:
        print(f"  ⚠️  {slug}: output_file_id 없음")
        return False

    meta_path = BOOKS_DIR / slug / "metadata.json"
    if not meta_path.exists():
        print(f"  ⚠️  {slug}: metadata.json 없음")
        return False

    meta = json.loads(meta_path.read_text())
    out_dir = CONTENT_DIR / "books" / slug

    # 이미 있으면 건너뜀
    if out_dir.exists() and list(out_dir.glob("*.json")):
        print(f"  [건너뜀] {slug} (이미 다운로드됨)")
        return True

    try:
        results = download_and_parse(output_file_id, f"p6_book_{slug}")
    except Exception as e:
        print(f"  ❌ {slug} 다운로드 실패: {e}")
        return False

    ch_map = {ch["num"]: ch for ch in meta["chapters"]}
    out_dir.mkdir(parents=True, exist_ok=True)
    saved = errors = 0

    for cid, data in results.items():
        if "_error" in data:
            errors += 1
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

    print(f"  📥 {slug}: {saved}챕터 저장, {errors}오류")
    return saved > 0


def check_and_fetch(batch_ids: dict) -> tuple[int, int, int]:
    """전체 배치 상태 확인 + 완료분 다운로드.

    Returns:
        (completed_count, pending_count, failed_count)
    """
    from pipeline.batch.submitter import check_batch_status
    from pipeline.config import CONTENT_DIR

    done = pending = failed = 0

    for slug, bid in sorted(batch_ids.items()):
        if not bid.startswith("batch_"):
            continue

        # 이미 content 있으면 skip
        out_dir = CONTENT_DIR / "books" / slug
        if out_dir.exists() and list(out_dir.glob("*.json")):
            done += 1
            continue

        try:
            s = check_batch_status(bid)
        except Exception as e:
            print(f"  ⚠️  {slug}: 상태 확인 실패 ({e})")
            pending += 1
            continue

        st = s["status"]
        c, t = s.get("completed", 0), s.get("total", 0)

        if st == "completed":
            print(f"  ✅ {slug}: completed ({c}/{t}) → 다운로드 중")
            fetch_one(slug, bid, s)
            done += 1
        elif st in ("failed", "expired", "cancelled"):
            print(f"  ❌ {slug}: {st}")
            failed += 1
        else:
            pct = f"{c/t*100:.0f}%" if t else "?%"
            print(f"  🔄 {slug}: {st} ({c}/{t} {pct})")
            pending += 1

    return done, pending, failed


def main():
    parser = argparse.ArgumentParser(description="Phase 6 Batch 모니터")
    parser.add_argument("--once", action="store_true", help="1회만 체크하고 종료")
    parser.add_argument("--interval", type=int, default=20, help="폴링 간격 (분, 기본 20)")
    args = parser.parse_args()

    interval_sec = args.interval * 60

    if not BATCH_LOG.exists():
        print(f"배치 로그 없음: {BATCH_LOG}")
        print("먼저 phase6_submit.py 를 실행하세요.")
        sys.exit(1)

    round_num = 0
    while True:
        round_num += 1
        batch_ids = json.loads(BATCH_LOG.read_text())
        total = sum(1 for v in batch_ids.values() if v.startswith("batch_"))

        print(f"\n{'='*60}")
        print(f"[{ts()}] 라운드 {round_num} — 총 {total}개 배치 확인")
        print(f"{'='*60}")

        done, pending, failed = check_and_fetch(batch_ids)

        print(f"\n  완료: {done} | 진행중: {pending} | 실패/만료: {failed}")

        if args.once:
            break

        if pending == 0:
            print(f"\n[{ts()}] 모든 배치 처리 완료. 모니터 종료.")
            break

        next_check = datetime.fromtimestamp(time.time() + interval_sec).strftime("%H:%M")
        print(f"\n[{ts()}] {pending}개 진행중. {args.interval}분 후({next_check}) 재확인...")
        time.sleep(interval_sec)


if __name__ == "__main__":
    main()
