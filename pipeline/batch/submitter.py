"""OpenAI Batch API 제출 및 상태 폴링."""

import time
from pathlib import Path

from openai import OpenAI

from pipeline.config import OPENAI_API_KEY


def get_client() -> OpenAI:
    """OpenAI 클라이언트를 생성한다."""
    return OpenAI(api_key=OPENAI_API_KEY)


def submit_batch(jsonl_path: Path, description: str = "") -> str:
    """JSONL 파일을 Batch API에 제출한다.

    Args:
        jsonl_path: .jsonl 파일 경로
        description: 배치 설명

    Returns:
        batch_id 문자열
    """
    client = get_client()

    # 1. 파일 업로드
    with open(jsonl_path, "rb") as f:
        uploaded_file = client.files.create(file=f, purpose="batch")
    print(f"[제출] 파일 업로드 완료: {uploaded_file.id}")

    # 2. 배치 생성
    batch = client.batches.create(
        input_file_id=uploaded_file.id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={"description": description or jsonl_path.stem},
    )
    print(f"[제출] 배치 생성 완료: {batch.id} (상태: {batch.status})")
    return batch.id


def check_batch_status(batch_id: str) -> dict:
    """배치 상태를 확인한다.

    Returns:
        {"status": str, "completed": int, "failed": int, "total": int,
         "output_file_id": str | None}
    """
    client = get_client()
    batch = client.batches.retrieve(batch_id)

    counts = batch.request_counts
    return {
        "status": batch.status,
        "completed": counts.completed if counts else 0,
        "failed": counts.failed if counts else 0,
        "total": counts.total if counts else 0,
        "output_file_id": batch.output_file_id,
        "error_file_id": batch.error_file_id,
    }


def wait_for_batch(batch_id: str, poll_interval: int = 60) -> dict:
    """배치가 완료될 때까지 폴링한다.

    Args:
        batch_id: 배치 ID
        poll_interval: 폴링 간격 (초)

    Returns:
        최종 상태 딕셔너리
    """
    terminal_statuses = {"completed", "failed", "expired", "cancelled"}

    while True:
        status = check_batch_status(batch_id)
        completed = status["completed"]
        total = status["total"]
        pct = (completed / total * 100) if total > 0 else 0

        print(
            f"[폴링] {batch_id}: {status['status']} "
            f"({completed}/{total}, {pct:.1f}%)"
        )

        if status["status"] in terminal_statuses:
            return status

        time.sleep(poll_interval)
