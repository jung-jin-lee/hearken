#!/usr/bin/env python3
"""도서 가공 파이프라인 테스트 — 《하나님의 임재 연습》으로 실행.

사용법:
  python -m pipeline.scripts.test_book_pilot build          # JSONL 생성만
  python -m pipeline.scripts.test_book_pilot submit          # 배치 제출
  python -m pipeline.scripts.test_book_pilot check BATCH_ID  # 상태 확인
  python -m pipeline.scripts.test_book_pilot download BATCH_ID  # 결과 다운로드+저장
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.batch.builder import build_jsonl
from pipeline.batch.downloader import download_and_parse
from pipeline.batch.submitter import check_batch_status, submit_batch
from pipeline.processors.structurer import save_json
from pipeline.prompts.book_processing import build_book_processing_request
from pipeline.config import CONTENT_DIR

BOOK_DIR = Path("pipeline/sources/data/books/practice-of-presence")
BOOK_SLUG = "practice-of-presence"
BOOK_TITLE = "하나님의 임재 연습"
AUTHOR = "로렌스 형제"


def load_metadata() -> dict:
    """도서 메타데이터를 로드한다."""
    meta_path = BOOK_DIR / "metadata.json"
    with open(meta_path, encoding="utf-8") as f:
        return json.load(f)


def build():
    """도서 가공 배치 JSONL을 생성한다."""
    meta = load_metadata()
    requests = []

    for ch_info in meta["chapters"]:
        ch_path = BOOK_DIR / ch_info["file"]
        if not ch_path.exists():
            print(f"  [경고] 파일 없음: {ch_path}")
            continue

        text = ch_path.read_text(encoding="utf-8")
        req = build_book_processing_request(
            book_slug=BOOK_SLUG,
            book_title=BOOK_TITLE,
            author=AUTHOR,
            chapter_num=ch_info["num"],
            chapter_text=text,
        )
        requests.append(req)

    path = build_jsonl(requests, f"book_{BOOK_SLUG}")
    print(f"\n총 {len(requests)}개 챕터, JSONL: {path}")
    print(f"예상 비용 (Batch API): ~${len(requests) * 0.03:.2f}")
    return path


def download_and_structure(batch_id: str):
    """결과를 다운로드하고 구조화하여 저장한다."""
    status = check_batch_status(batch_id)
    if not status["output_file_id"]:
        print(f"[오류] 아직 결과 파일이 없습니다. 상태: {status['status']}")
        return

    results = download_and_parse(status["output_file_id"], f"book_{BOOK_SLUG}")

    # 결과 저장
    meta = load_metadata()
    ch_map = {ch["num"]: ch for ch in meta["chapters"]}
    saved = 0

    for custom_id, data in results.items():
        if "_error" in data:
            print(f"  [실패] {custom_id}: {data['_error'][:80]}")
            continue

        # custom_id: "book-practice-of-presence-ch001"
        parts = custom_id.split("-ch")
        if len(parts) != 2:
            continue
        ch_num = int(parts[1])

        ch_info = ch_map.get(ch_num, {})
        output = {
            "book_slug": BOOK_SLUG,
            "book_title": BOOK_TITLE,
            "author": AUTHOR,
            "chapter_num": ch_num,
            "chapter_title": ch_info.get("title", f"{ch_num}장"),
            **data,
        }

        out_path = CONTENT_DIR / "books" / BOOK_SLUG / f"{ch_num:03d}.json"
        save_json(output, out_path)
        saved += 1

    total = len(results)
    errors = sum(1 for v in results.values() if "_error" in v)
    print(f"\n[결과] 전체: {total}, 성공: {saved}, 실패: {errors}")

    # 샘플 출력
    if saved > 0:
        sample_path = CONTENT_DIR / "books" / BOOK_SLUG / "001.json"
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
            print(f"\n[묵상]\n{sample.get('reflection', '')}")


def main():
    parser = argparse.ArgumentParser(
        description="《하나님의 임재 연습》 파이프라인 테스트"
    )
    parser.add_argument(
        "action",
        choices=["build", "submit", "check", "download"],
    )
    parser.add_argument("batch_id", nargs="?")
    args = parser.parse_args()

    if args.action == "build":
        build()

    elif args.action == "submit":
        path = build()
        bid = submit_batch(path, f"book_{BOOK_SLUG}")
        print(f"\n배치 제출 완료! ID: {bid}")
        print(f"\n다음 명령어:")
        print(f"  상태 확인:   python -m pipeline.scripts.test_book_pilot check {bid}")
        print(f"  결과 다운로드: python -m pipeline.scripts.test_book_pilot download {bid}")

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
        download_and_structure(args.batch_id)


if __name__ == "__main__":
    main()
