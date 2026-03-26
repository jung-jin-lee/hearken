"""Batch API 결과 다운로드 및 파싱."""

import json
from pathlib import Path

from openai import OpenAI

from pipeline.config import BATCH_RESULTS_DIR, OPENAI_API_KEY


def get_client() -> OpenAI:
    """OpenAI 클라이언트를 생성한다."""
    return OpenAI(api_key=OPENAI_API_KEY)


def download_batch_results(output_file_id: str,
                           output_name: str) -> Path:
    """배치 결과 파일을 다운로드한다.

    Args:
        output_file_id: OpenAI 파일 ID
        output_name: 저장할 파일 이름 (확장자 제외)

    Returns:
        다운로드된 파일 경로
    """
    client = get_client()
    content = client.files.content(output_file_id)

    output_path = BATCH_RESULTS_DIR / f"{output_name}_results.jsonl"
    output_path.write_bytes(content.content)
    print(f"[다운로드] {output_path.name} 저장 완료")
    return output_path


def parse_batch_results(results_path: Path) -> dict[str, dict]:
    """배치 결과 JSONL을 파싱하여 custom_id → 결과 딕셔너리로 반환한다.

    Returns:
        {custom_id: parsed_json_content} 딕셔너리.
        파싱 실패 시 해당 항목의 값은 {"_error": error_message}
    """
    results = {}

    with open(results_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            row = json.loads(line)
            custom_id = row.get("custom_id", "unknown")

            # 응답 추출
            response = row.get("response", {})
            if response.get("status_code") != 200:
                results[custom_id] = {
                    "_error": f"HTTP {response.get('status_code')}: "
                              f"{response.get('body', {}).get('error', {}).get('message', 'unknown')}"
                }
                continue

            # 메시지 내용 추출
            try:
                body = response["body"]
                content = body["choices"][0]["message"]["content"]
                parsed = json.loads(content)
                results[custom_id] = parsed
            except (KeyError, IndexError, json.JSONDecodeError) as e:
                results[custom_id] = {"_error": f"파싱 실패: {e}"}

    total = len(results)
    errors = sum(1 for v in results.values() if "_error" in v)
    print(f"[파싱] {results_path.name}: {total}개 중 {total - errors}개 성공, {errors}개 실패")

    return results


def download_and_parse(output_file_id: str,
                       output_name: str) -> dict[str, dict]:
    """다운로드와 파싱을 한 번에 수행한다."""
    path = download_batch_results(output_file_id, output_name)
    return parse_batch_results(path)
