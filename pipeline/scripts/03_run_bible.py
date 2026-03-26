#!/usr/bin/env python3
"""성경 장별 해설 + 66권 개론 전체 배치 생성 및 제출.

사용법:
  python -m pipeline.scripts.03_run_bible build          # JSONL 생성
  python -m pipeline.scripts.03_run_bible submit          # 배치 제출
  python -m pipeline.scripts.03_run_bible check BATCH_ID  # 상태 확인
  python -m pipeline.scripts.03_run_bible download BATCH_ID  # 결과 다운로드+저장
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.batch.builder import build_jsonl
from pipeline.batch.downloader import download_and_parse
from pipeline.batch.submitter import check_batch_status, submit_batch
from pipeline.config import BIBLE_BOOKS
from pipeline.processors.structurer import structure_book_intros, structure_commentary
from pipeline.prompts.bible_commentary import build_commentary_request
from pipeline.prompts.book_intro import build_book_intro_request
from pipeline.sources.bible_kr import get_all_chapters, load_chapter_from_file
from pipeline.validators.schema_validator import validate_batch_results


def build_commentary_batch():
    """장별 해설 JSONL을 생성한다."""
    chapters = get_all_chapters()
    requests = []

    for info in chapters:
        text = load_chapter_from_file(info["book_id"], info["chapter"])
        if not text:
            text = f"[{info['book_kr']} {info['chapter']}장]"

        req = build_commentary_request(
            info["book_id"], info["book_kr"], info["chapter"], text
        )
        requests.append(req)

    return build_jsonl(requests, "bible_commentary_all")


def build_intro_batch():
    """66권 개론 JSONL을 생성한다."""
    requests = []
    for book in BIBLE_BOOKS:
        req = build_book_intro_request(
            book["id"], book["kr"], book["chapters"], book["testament"]
        )
        requests.append(req)

    return build_jsonl(requests, "bible_introductions")


def main():
    parser = argparse.ArgumentParser(description="성경 해설 배치")
    parser.add_argument("action", choices=["build", "submit", "check", "download"])
    parser.add_argument("batch_id", nargs="?", help="배치 ID (check/download에 필요)")
    parser.add_argument("--type", choices=["commentary", "intro", "all"], default="all")
    args = parser.parse_args()

    if args.action == "build":
        if args.type in ("commentary", "all"):
            build_commentary_batch()
        if args.type in ("intro", "all"):
            build_intro_batch()
        return

    if args.action == "submit":
        if args.type in ("commentary", "all"):
            path = Path("pipeline/batch/requests/bible_commentary_all.jsonl")
            if path.exists():
                bid = submit_batch(path, "bible_commentary_all")
                print(f"해설 배치 ID: {bid}")

        if args.type in ("intro", "all"):
            path = Path("pipeline/batch/requests/bible_introductions.jsonl")
            if path.exists():
                bid = submit_batch(path, "bible_introductions")
                print(f"개론 배치 ID: {bid}")
        return

    if args.action == "check":
        if not args.batch_id:
            print("batch_id가 필요합니다.")
            return
        status = check_batch_status(args.batch_id)
        print(json.dumps(status, indent=2))
        return

    if args.action == "download":
        if not args.batch_id:
            print("batch_id가 필요합니다.")
            return
        status = check_batch_status(args.batch_id)
        if not status["output_file_id"]:
            print("[오류] 아직 결과 파일이 없습니다.")
            return

        results = download_and_parse(status["output_file_id"], "bible")

        # QA
        report = validate_batch_results(results)
        print(f"\n[QA] 전체: {report['total']}, 성공: {report['valid']}, 실패: {report['invalid']}")

        # 구조화 저장
        structure_commentary(results)
        structure_book_intros(results)


if __name__ == "__main__":
    main()
