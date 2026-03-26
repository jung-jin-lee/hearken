#!/usr/bin/env python3
"""파일럿 배치: 창세기 1~10장으로 품질 테스트.

사용법:
  python -m pipeline.scripts.02_run_pilot
  python -m pipeline.scripts.02_run_pilot --submit   # 배치 제출
  python -m pipeline.scripts.02_run_pilot --check BATCH_ID   # 상태 확인
  python -m pipeline.scripts.02_run_pilot --download BATCH_ID  # 결과 다운로드
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.batch.builder import build_jsonl
from pipeline.batch.downloader import download_and_parse
from pipeline.batch.submitter import check_batch_status, submit_batch, wait_for_batch
from pipeline.config import BIBLE_BOOKS
from pipeline.prompts.bible_commentary import build_commentary_request
from pipeline.sources.bible_kr import load_chapter_from_file
from pipeline.validators.schema_validator import validate_batch_results


def build_pilot():
    """파일럿 배치 JSONL을 생성한다."""
    genesis = next(b for b in BIBLE_BOOKS if b["id"] == "genesis")
    requests = []

    for ch in range(1, 11):
        text = load_chapter_from_file("genesis", ch)
        if not text:
            text = f"[창세기 {ch}장 텍스트 - 소스 수집 후 교체 필요]"

        req = build_commentary_request("genesis", "창세기", ch, text)
        requests.append(req)

    path = build_jsonl(requests, "pilot_genesis_1-10")
    return path


def main():
    parser = argparse.ArgumentParser(description="파일럿 배치 실행")
    parser.add_argument("--submit", action="store_true", help="배치 제출")
    parser.add_argument("--check", type=str, help="배치 상태 확인 (batch_id)")
    parser.add_argument("--download", type=str, help="결과 다운로드 (batch_id)")
    parser.add_argument("--wait", type=str, help="완료까지 대기 (batch_id)")
    args = parser.parse_args()

    if args.check:
        status = check_batch_status(args.check)
        print(json.dumps(status, indent=2))
        return

    if args.wait:
        status = wait_for_batch(args.wait)
        print(json.dumps(status, indent=2))
        return

    if args.download:
        status = check_batch_status(args.download)
        if not status["output_file_id"]:
            print("[오류] 아직 결과 파일이 없습니다.")
            return

        results = download_and_parse(status["output_file_id"], "pilot")
        report = validate_batch_results(results)
        print(f"\n[QA 결과]")
        print(f"  전체: {report['total']}")
        print(f"  성공: {report['valid']}")
        print(f"  실패: {report['invalid']}")
        for err in report["errors"]:
            print(f"  - {err['custom_id']}: {err['error'][:100]}")

        # 샘플 출력
        for cid, data in list(results.items())[:2]:
            if "_error" not in data:
                print(f"\n[샘플] {cid}:")
                print(json.dumps(data, ensure_ascii=False, indent=2)[:500])
        return

    # 기본: JSONL 빌드
    path = build_pilot()
    print(f"\n파일럿 JSONL 생성: {path}")

    if args.submit:
        batch_id = submit_batch(path, "pilot_genesis_1-10")
        print(f"\n배치 제출 완료! ID: {batch_id}")
        print(f"상태 확인: python -m pipeline.scripts.02_run_pilot --check {batch_id}")
        print(f"결과 다운로드: python -m pipeline.scripts.02_run_pilot --download {batch_id}")


if __name__ == "__main__":
    main()
