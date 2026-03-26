#!/usr/bin/env python3
"""전체 콘텐츠 QA 실행 및 매니페스트 생성.

사용법:
  python -m pipeline.scripts.07_run_qa
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.config import CONTENT_DIR
from pipeline.processors.indexer import save_manifest


def count_files(directory: Path, pattern: str = "*.json") -> int:
    """디렉토리 내 파일 수를 세다."""
    if not directory.exists():
        return 0
    return len(list(directory.rglob(pattern)))


def check_accessibility_language(directory: Path) -> list[dict]:
    """시각 은유 표현을 탐지한다."""
    visual_terms = [
        "보세요", "살펴보면", "눈에 띄는", "한눈에", "보이는",
        "눈여겨", "보시면", "눈길을", "시선을", "바라보면",
    ]
    issues = []

    for json_file in directory.rglob("*.json"):
        try:
            with open(json_file, encoding="utf-8") as f:
                content = f.read()
            for term in visual_terms:
                if term in content:
                    issues.append({
                        "file": str(json_file.relative_to(CONTENT_DIR)),
                        "term": term,
                    })
        except Exception:
            pass

    return issues


def main():
    print("=" * 60)
    print("  Hearken 콘텐츠 QA 리포트")
    print("=" * 60)

    # 1. 파일 카운트
    print("\n[1] 콘텐츠 파일 수")
    counts = {
        "성경 해설": count_files(CONTENT_DIR / "bible" / "commentary"),
        "성경 개론": count_files(CONTENT_DIR / "bible" / "introductions"),
        "인물 해설": count_files(CONTENT_DIR / "bible" / "characters"),
        "주제 가이드": count_files(CONTENT_DIR / "bible" / "topics"),
        "매일 묵상": count_files(CONTENT_DIR / "devotional"),
        "도서": count_files(CONTENT_DIR / "books"),
    }

    for name, count in counts.items():
        status = "OK" if count > 0 else "없음"
        print(f"  {name}: {count}개 [{status}]")

    # 2. 접근성 언어 체크
    print("\n[2] 접근성 언어 체크 (시각 은유 탐지)")
    issues = check_accessibility_language(CONTENT_DIR)
    if issues:
        print(f"  {len(issues)}건 발견:")
        for issue in issues[:10]:
            print(f"    - {issue['file']}: '{issue['term']}'")
        if len(issues) > 10:
            print(f"    ... 외 {len(issues) - 10}건")
    else:
        print("  시각 은유 표현 없음 [OK]")

    # 3. 매니페스트 생성
    print("\n[3] 매니페스트 생성")
    manifest_path = save_manifest()
    print(f"  저장: {manifest_path}")

    print("\n" + "=" * 60)
    print("  QA 완료")
    print("=" * 60)


if __name__ == "__main__":
    main()
