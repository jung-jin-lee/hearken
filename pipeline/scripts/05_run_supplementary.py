#!/usr/bin/env python3
"""인물/주제/주요구절 배치 생성 및 제출.

사용법:
  python -m pipeline.scripts.05_run_supplementary build
  python -m pipeline.scripts.05_run_supplementary submit
  python -m pipeline.scripts.05_run_supplementary download BATCH_ID
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.batch.builder import build_jsonl
from pipeline.batch.downloader import download_and_parse
from pipeline.batch.submitter import check_batch_status, submit_batch
from pipeline.config import BIBLE_CHARACTERS, BIBLE_TOPICS, KEY_VERSE_REFERENCES
from pipeline.processors.structurer import (
    structure_characters,
    structure_key_verses,
    structure_topics,
)
from pipeline.prompts.character import build_character_request
from pipeline.prompts.key_verse import build_key_verse_request
from pipeline.prompts.topic import build_topic_request
from pipeline.validators.schema_validator import validate_batch_results


def build_all():
    """인물/주제/주요구절 JSONL을 생성한다."""
    # 인물
    char_requests = [build_character_request(name) for name in BIBLE_CHARACTERS]
    build_jsonl(char_requests, "characters")

    # 주제
    topic_requests = [build_topic_request(topic) for topic in BIBLE_TOPICS]
    build_jsonl(topic_requests, "topics")

    # 주요 구절
    verse_requests = [build_key_verse_request(ref) for ref in KEY_VERSE_REFERENCES]
    build_jsonl(verse_requests, "key_verses")


def main():
    parser = argparse.ArgumentParser(description="보충 콘텐츠 배치")
    parser.add_argument("action", choices=["build", "submit", "check", "download"])
    parser.add_argument("batch_id", nargs="?")
    parser.add_argument("--type", choices=["characters", "topics", "key_verses", "all"],
                        default="all")
    args = parser.parse_args()

    if args.action == "build":
        build_all()
        return

    if args.action == "submit":
        req_dir = Path("pipeline/batch/requests")
        targets = (
            ["characters", "topics", "key_verses"]
            if args.type == "all"
            else [args.type]
        )
        for name in targets:
            path = req_dir / f"{name}.jsonl"
            if path.exists():
                bid = submit_batch(path, name)
                print(f"{name} 배치 ID: {bid}")
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

        results = download_and_parse(status["output_file_id"], "supplementary")
        report = validate_batch_results(results)
        print(f"\n[QA] 전체: {report['total']}, 성공: {report['valid']}, 실패: {report['invalid']}")

        structure_characters(results)
        structure_topics(results)
        structure_key_verses(results)


if __name__ == "__main__":
    main()
