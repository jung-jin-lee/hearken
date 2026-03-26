#!/usr/bin/env python3
"""범용 도서 가공 파이프라인 — metadata.json 기반으로 모든 도서에 사용 가능.

사용법:
  python -m pipeline.scripts.run_book build   pilgrims-progress
  python -m pipeline.scripts.run_book submit  pilgrims-progress
  python -m pipeline.scripts.run_book check   pilgrims-progress BATCH_ID
  python -m pipeline.scripts.run_book download pilgrims-progress BATCH_ID
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.batch.builder import build_jsonl
from pipeline.batch.downloader import download_and_parse
from pipeline.batch.submitter import check_batch_status, submit_batch
from pipeline.config import CONTENT_DIR
from pipeline.processors.structurer import save_json
from pipeline.prompts.book_processing import build_book_processing_request

BOOKS_DIR = Path("pipeline/sources/data/books")


def load_metadata(slug: str) -> dict:
    """도서 메타데이터를 로드한다."""
    meta_path = BOOKS_DIR / slug / "metadata.json"
    if not meta_path.exists():
        print(f"[오류] 메타데이터 없음: {meta_path}")
        sys.exit(1)
    with open(meta_path, encoding="utf-8") as f:
        return json.load(f)


def build(slug: str) -> Path:
    """도서 가공 배치 JSONL을 생성한다."""
    meta = load_metadata(slug)
    book_dir = BOOKS_DIR / slug
    requests = []

    print(f"\n《{meta['title']}》 ({meta['author']}) 배치 생성 중...")
    for ch_info in meta["chapters"]:
        ch_path = book_dir / ch_info["file"]
        if not ch_path.exists():
            print(f"  [경고] 파일 없음: {ch_path}")
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

    path = build_jsonl(requests, f"book_{slug}")
    print(f"\n총 {len(requests)}개 챕터, JSONL: {path}")
    print(f"예상 비용 (Batch API): ~${len(requests) * 0.03:.2f}")
    return path


def download_and_structure(slug: str, batch_id: str):
    """결과를 다운로드하고 구조화하여 저장한다."""
    meta = load_metadata(slug)
    status = check_batch_status(batch_id)
    if not status["output_file_id"]:
        print(f"[오류] 아직 결과 파일이 없습니다. 상태: {status['status']}")
        return

    results = download_and_parse(status["output_file_id"], f"book_{slug}")

    ch_map = {ch["num"]: ch for ch in meta["chapters"]}
    out_dir = CONTENT_DIR / "books" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    saved = 0

    for custom_id, data in results.items():
        if "_error" in data:
            print(f"  [실패] {custom_id}: {data['_error'][:80]}")
            continue

        parts = custom_id.rsplit("-ch", 1)
        if len(parts) != 2:
            continue
        ch_num = int(parts[1])

        ch_info = ch_map.get(ch_num, {})
        output = {
            "book_slug": slug,
            "book_title": meta["title"],
            "author": meta["author"],
            "chapter_num": ch_num,
            "chapter_title": ch_info.get("title", f"{ch_num}장"),
            **data,
        }

        out_path = out_dir / f"{ch_num:03d}.json"
        save_json(output, out_path)
        saved += 1

    total = len(results)
    errors = sum(1 for v in results.values() if "_error" in v)
    print(f"\n[결과] 전체: {total}, 성공: {saved}, 실패: {errors}")

    # 샘플 출력
    if saved > 0:
        sample_path = out_dir / "001.json"
        if sample_path.exists():
            with open(sample_path, encoding="utf-8") as f:
                sample = json.load(f)
            print(f"\n{'='*60}")
            print(f"[샘플] {sample.get('chapter_title', '1장')}")
            print(f"{'='*60}")
            print(f"\n[현대어 번역]\n{sample.get('modern_translation', '')[:500]}")
            print(f"\n[요약]\n{sample.get('summary', '')}")
            print(f"\n[핵심 포인트]")
            for kp in sample.get("key_points", []):
                print(f"  - {kp}")


def main():
    parser = argparse.ArgumentParser(description="범용 도서 가공 파이프라인")
    parser.add_argument("action", choices=["build", "submit", "check", "download"])
    parser.add_argument("slug", help="도서 slug (예: pilgrims-progress)")
    parser.add_argument("batch_id", nargs="?")
    args = parser.parse_args()

    if args.action == "build":
        build(args.slug)

    elif args.action == "submit":
        path = build(args.slug)
        bid = submit_batch(path, f"book_{args.slug}")
        print(f"\n배치 제출 완료! ID: {bid}")
        print(f"\n다음 명령어:")
        print(f"  상태 확인:   python -m pipeline.scripts.run_book check {args.slug} {bid}")
        print(f"  결과 다운로드: python -m pipeline.scripts.run_book download {args.slug} {bid}")

    elif args.action == "check":
        if not args.batch_id:
            print("batch_id가 필요합니다.")
            return
        status = check_batch_status(args.batch_id)
        print(json.dumps(status, indent=2, ensure_ascii=False))

    elif args.action == "download":
        if not args.batch_id:
            print("batch_id가 필요합니다.")
            return
        download_and_structure(args.slug, args.batch_id)


if __name__ == "__main__":
    main()
