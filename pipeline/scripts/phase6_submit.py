#!/usr/bin/env python3
"""Phase 6 도서 Batch API 제출.

pipeline/sources/data/books/{slug}/metadata.json 이 존재하는
Phase 6 도서를 OpenAI Batch API에 제출하고
bulk_batch_ids_p6.json 에 배치 ID를 저장한다.

사용법:
  python pipeline/scripts/phase6_submit.py           # 제출 (미완료분만)
  python pipeline/scripts/phase6_submit.py --dry-run # 제출 없이 대상 확인
"""
import sys, json, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.config import CONTENT_DIR
from pipeline.scripts.phase6_batch_a import BOOKS as BOOKS_A
from pipeline.scripts.phase6_batch_b import BOOKS as BOOKS_B
from pipeline.scripts.phase6_batch_c import BOOKS as BOOKS_C
from pipeline.scripts.phase6_batch_d import BOOKS as BOOKS_D
from pipeline.scripts.phase6_batch_e import BOOKS as BOOKS_E
from pipeline.scripts.phase6_batch_f import BOOKS as BOOKS_F
from pipeline.scripts.phase6_batch_g import BOOKS as BOOKS_G
from pipeline.scripts.phase6_batch_h import BOOKS as BOOKS_H

BOOKS_DIR = Path("pipeline/sources/data/books")
BATCH_LOG = Path("pipeline/scripts/bulk_batch_ids_p6.json")

ALL_P6_BOOKS = (
    BOOKS_A + BOOKS_B + BOOKS_C + BOOKS_D +
    BOOKS_E + BOOKS_F + BOOKS_G + BOOKS_H
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="제출 없이 대상만 출력")
    args = parser.parse_args()

    from pipeline.batch.builder import build_jsonl
    from pipeline.batch.submitter import submit_batch
    from pipeline.prompts.book_processing import build_book_processing_request

    # 기존 배치 ID 로드
    batch_ids: dict = {}
    if BATCH_LOG.exists():
        batch_ids = json.loads(BATCH_LOG.read_text())

    submitted = skipped_done = skipped_no_source = 0
    targets = []

    for info in ALL_P6_BOOKS:
        slug = info["slug"]

        # 이미 제출됨?
        if slug in batch_ids:
            skipped_done += 1
            continue

        # 이미 content 있음?
        content_dir = CONTENT_DIR / "books" / slug
        if content_dir.exists() and list(content_dir.glob("*.json")):
            skipped_done += 1
            continue

        # 소스(metadata) 없음?
        meta_path = BOOKS_DIR / slug / "metadata.json"
        if not meta_path.exists():
            skipped_no_source += 1
            continue

        targets.append((slug, meta_path))

    print(f"제출 대상: {len(targets)}권 | 건너뜀(완료): {skipped_done} | 소스없음: {skipped_no_source}")
    if args.dry_run:
        for slug, _ in targets:
            print(f"  📋 {slug}")
        return

    for i, (slug, meta_path) in enumerate(targets, 1):
        meta = json.loads(meta_path.read_text())
        book_dir = BOOKS_DIR / slug
        requests = []

        for ch in meta["chapters"]:
            ch_path = book_dir / ch["file"]
            if not ch_path.exists():
                continue
            text = ch_path.read_text(encoding="utf-8")
            req = build_book_processing_request(
                book_slug=slug,
                book_title=meta["title"],
                author=meta.get("author", ""),
                chapter_num=ch["num"],
                chapter_text=text,
            )
            requests.append(req)

        if not requests:
            print(f"  ⚠️  {slug}: 챕터 없음, 건너뜀")
            continue

        print(f"\n[{i}/{len(targets)}] {slug} ({len(requests)}챕터)")
        path = build_jsonl(requests, f"p6_book_{slug}")
        bid = submit_batch(path, f"p6_{slug}")
        batch_ids[slug] = bid
        submitted += 1
        print(f"  📤 → {bid}")

        # 매 제출 후 즉시 저장
        BATCH_LOG.write_text(json.dumps(batch_ids, indent=2, ensure_ascii=False))

    print(f"\n{'='*60}")
    print(f"제출 완료: {submitted}권")
    print(f"배치 ID 저장: {BATCH_LOG}")


if __name__ == "__main__":
    main()
