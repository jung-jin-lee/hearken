#!/usr/bin/env python3
"""365일 매일 묵상 배치 생성 및 제출.

사용법:
  python -m pipeline.scripts.04_run_devotional build
  python -m pipeline.scripts.04_run_devotional submit
  python -m pipeline.scripts.04_run_devotional download BATCH_ID
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.batch.builder import build_jsonl
from pipeline.batch.downloader import download_and_parse
from pipeline.batch.submitter import check_batch_status, submit_batch
from pipeline.processors.structurer import structure_devotional
from pipeline.prompts.devotional import build_devotional_request
from pipeline.validators.schema_validator import validate_batch_results

# 365일 묵상 본문 배정 (월별 일수)
DAYS_IN_MONTH = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# 대표 묵상 구절 (실제로는 더 많은 구절 필요 — GPT에게 선정 위임)
DEVOTIONAL_VERSES = [
    # 각 (reference, text) 튜플 — 여기서는 reference만 제공하고
    # GPT가 본문을 포함하여 생성하도록 함
]


def build_devotional_batch():
    """365일 묵상 JSONL을 생성한다."""
    requests = []
    day_index = 0

    for month_idx, days in enumerate(DAYS_IN_MONTH):
        month = month_idx + 1
        for day in range(1, days + 1):
            # 묵상 구절은 GPT에게 적절한 구절 선택을 위임
            reference = f"[{month}월 {day}일에 적합한 성경 구절을 선택해주십시오]"
            verse_text = ""

            req = build_devotional_request(month, day, reference, verse_text)
            requests.append(req)
            day_index += 1

    return build_jsonl(requests, "devotional_365")


def main():
    parser = argparse.ArgumentParser(description="365일 묵상 배치")
    parser.add_argument("action", choices=["build", "submit", "check", "download"])
    parser.add_argument("batch_id", nargs="?")
    args = parser.parse_args()

    if args.action == "build":
        build_devotional_batch()
        return

    if args.action == "submit":
        path = Path("pipeline/batch/requests/devotional_365.jsonl")
        if path.exists():
            bid = submit_batch(path, "devotional_365")
            print(f"묵상 배치 ID: {bid}")
        return

    if args.action == "check":
        status = check_batch_status(args.batch_id)
        print(json.dumps(status, indent=2))
        return

    if args.action == "download":
        status = check_batch_status(args.batch_id)
        if not status["output_file_id"]:
            print("[오류] 아직 결과 파일이 없습니다.")
            return

        results = download_and_parse(status["output_file_id"], "devotional")
        report = validate_batch_results(results)
        print(f"\n[QA] 전체: {report['total']}, 성공: {report['valid']}, 실패: {report['invalid']}")
        structure_devotional(results)


if __name__ == "__main__":
    main()
