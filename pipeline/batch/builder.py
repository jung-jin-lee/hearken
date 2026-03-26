"""프롬프트 요청들을 .jsonl 파일로 변환하는 빌더."""

import json
from pathlib import Path

from pipeline.config import BATCH_REQUESTS_DIR


def build_jsonl(requests: list[dict], output_name: str) -> Path:
    """요청 목록을 .jsonl 파일로 저장한다.

    Args:
        requests: build_request()로 생성된 딕셔너리 리스트
        output_name: 출력 파일 이름 (확장자 제외)

    Returns:
        생성된 .jsonl 파일 경로
    """
    output_path = BATCH_REQUESTS_DIR / f"{output_name}.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for req in requests:
            f.write(json.dumps(req, ensure_ascii=False) + "\n")

    print(f"[빌더] {output_path.name}: {len(requests)}개 요청 생성 완료")
    return output_path


def load_jsonl(path: Path) -> list[dict]:
    """JSONL 파일을 읽어 딕셔너리 리스트로 반환한다."""
    results = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                results.append(json.loads(line))
    return results
