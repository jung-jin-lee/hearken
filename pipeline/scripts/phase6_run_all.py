#!/usr/bin/env python3
"""Phase 6 전체 배치 실행 스크립트 — 168권 (카테고리 48–65).

사용법:
  # 전체 실행
  python pipeline/scripts/phase6_run_all.py

  # 특정 배치만 실행 (예: a, c, e)
  python pipeline/scripts/phase6_run_all.py --batches a c e

  # 건너뛰기 없이 강제 재처리
  python pipeline/scripts/phase6_run_all.py --force
"""
import sys, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.scripts.phase6_batch_a import BOOKS as BOOKS_A
from pipeline.scripts.phase6_batch_b import BOOKS as BOOKS_B
from pipeline.scripts.phase6_batch_c import BOOKS as BOOKS_C
from pipeline.scripts.phase6_batch_d import BOOKS as BOOKS_D
from pipeline.scripts.phase6_batch_e import BOOKS as BOOKS_E
from pipeline.scripts.phase6_batch_f import BOOKS as BOOKS_F
from pipeline.scripts.phase6_batch_g import BOOKS as BOOKS_G
from pipeline.scripts.phase6_batch_h import BOOKS as BOOKS_H

BATCHES = {
    "a": ("카테고리 48–49: 선구적 개혁가 + 네덜란드 개혁주의", BOOKS_A),
    "b": ("카테고리 50–51: 대륙 교의학 + 스코틀랜드 언약도", BOOKS_B),
    "c": ("카테고리 52–53: 뉴잉글랜드 청교도 + 빅토리아 성경학", BOOKS_C),
    "d": ("카테고리 54–55: 프린스턴 정통주의 + 구약 주석", BOOKS_D),
    "e": ("카테고리 56–57: 기독교 시문학 + 19세기 설교가들", BOOKS_E),
    "f": ("카테고리 58–60: 침례교 + 프랑스·스위스 + 기독교 사회윤리", BOOKS_F),
    "g": ("카테고리 61–63: 독일 경건주의 + 스코틀랜드 자유교회 + 조직신학 보조", BOOKS_G),
    "h": ("카테고리 64–65: 미등록 개혁주의 설교자들 + 부흥 1차 사료", BOOKS_H),
}


def main():
    parser = argparse.ArgumentParser(description="Phase 6 배치 실행")
    parser.add_argument(
        "--batches", nargs="+", choices=list(BATCHES.keys()),
        help="실행할 배치 선택 (기본: 전체)"
    )
    parser.add_argument(
        "--force", action="store_true",
        help="이미 처리된 도서도 재처리"
    )
    args = parser.parse_args()

    selected = args.batches or list(BATCHES.keys())

    from pipeline.scripts.phase5_utils import process_all, BOOKS_DIR

    if args.force:
        # metadata.json 삭제하여 강제 재처리
        print("[강제 모드] 기존 metadata.json 삭제 후 재처리")

    grand_total = {"success": 0, "failed": 0, "skipped": 0}
    all_failed = []

    for key in selected:
        label, books = BATCHES[key]
        print(f"\n{'='*70}")
        print(f"  배치 {key.upper()} — {label}")
        print(f"  대상: {len(books)}권")
        print(f"{'='*70}")

        if args.force:
            for b in books:
                meta = BOOKS_DIR / b["slug"] / "metadata.json"
                if meta.exists():
                    meta.unlink()

        results, failed = process_all(books, delay=1.5)
        for k, v in results.items():
            grand_total[k] = grand_total.get(k, 0) + v
        all_failed.extend(failed)

    print(f"\n{'='*70}")
    print(f"  Phase 6 전체 완료")
    print(f"  성공: {grand_total['success']}  실패: {grand_total['failed']}  건너뜀: {grand_total['skipped']}")
    total = sum(grand_total.values())
    print(f"  처리 대상: {total}권")
    if all_failed:
        print(f"\n  실패 목록 ({len(all_failed)}권):")
        for slug in all_failed:
            print(f"    - {slug}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
