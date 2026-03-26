#!/usr/bin/env python3
"""books_manifest.json의 깨진 URL을 자동으로 수정하는 스크립트.

1. CCEL 작가 페이지에서 실제 텍스트 파일 URL 탐색
2. Archive.org 검색 API로 올바른 identifier 탐색
3. Gutenberg 검색으로 ebook ID 탐색
"""

import json, re, os, time, sys
import urllib.request
import urllib.parse
from pathlib import Path

MANIFEST = Path("pipeline/scripts/books_manifest.json")
BOOKS_DIR = Path("pipeline/sources/data/books")

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Hearken project)"}


def fetch(url, timeout=15):
    """URL에서 텍스트를 가져온다."""
    try:
        req = urllib.request.Request(url, headers=UA)
        r = urllib.request.urlopen(req, timeout=timeout)
        return r.read().decode("utf-8", errors="replace")
    except Exception:
        return None


def check_url(url, timeout=10):
    """URL이 200을 반환하는지 확인한다."""
    try:
        req = urllib.request.Request(url, headers=UA, method="HEAD")
        r = urllib.request.urlopen(req, timeout=timeout)
        return r.status == 200
    except Exception:
        return False


def find_ccel_text_url(author_id, work_hint):
    """CCEL 작가 페이지에서 텍스트 파일 URL을 찾는다."""
    # CCEL 작가 페이지에서 작품 목록 가져오기
    page = fetch(f"https://ccel.org/ccel/{author_id}")
    if not page:
        return None

    # 작품 링크 추출: /ccel/{author}/{work}/{work}
    works = re.findall(r'/ccel/' + author_id + r'/(\w+)/\1', page)
    if not works:
        # 대안 패턴
        works = re.findall(r'/ccel/' + author_id + r'/(\w+)', page)

    works = list(set(works))

    # work_hint와 매칭 시도
    for w in works:
        if work_hint in w or w in work_hint:
            # 텍스트 URL 테스트
            first_letter = author_id[0]
            txt_url = f"https://ccel.org/ccel/{first_letter}/{author_id}/{w}/cache/{w}.txt"
            if check_url(txt_url):
                return txt_url

    # 전체 작품에서 순차 테스트
    for w in works:
        first_letter = author_id[0]
        txt_url = f"https://ccel.org/ccel/{first_letter}/{author_id}/{w}/cache/{w}.txt"
        if check_url(txt_url):
            return txt_url

    return None


def search_archive(title, author=""):
    """Archive.org 검색 API로 텍스트 identifier를 찾는다."""
    query = f"{title} {author}".strip()
    params = urllib.parse.urlencode({
        "q": query,
        "fl[]": "identifier,title",
        "rows": 5,
        "page": 1,
        "output": "json",
        "mediatype": "texts",
    })
    url = f"https://archive.org/advancedsearch.php?{params}"
    text = fetch(url)
    if not text:
        return None

    try:
        data = json.loads(text)
        docs = data.get("response", {}).get("docs", [])
        for doc in docs:
            ident = doc.get("identifier", "")
            # _djvu.txt URL 구성 및 테스트
            djvu_url = f"https://archive.org/download/{ident}/{ident}_djvu.txt"
            # HEAD check 대신 identifier만 반환 (503이 일시적일 수 있으므로)
            return djvu_url
    except Exception:
        pass
    return None


def search_gutenberg(title, author=""):
    """Gutenberg 검색으로 ebook ID를 찾는다."""
    query = urllib.parse.quote(f"{title} {author}".strip())
    url = f"https://www.gutenberg.org/ebooks/search/?query={query}&submit_search=Search"
    page = fetch(url)
    if not page:
        return None

    # ebook ID 추출
    matches = re.findall(r'/ebooks/(\d+)', page)
    if matches:
        ebook_id = matches[0]
        txt_url = f"https://www.gutenberg.org/cache/epub/{ebook_id}/pg{ebook_id}.txt"
        if check_url(txt_url):
            return txt_url
    return None


# ─── CCEL author → work ID 매핑 (수동 조사 기반) ───
# CCEL 텍스트 URL 형식: /ccel/{letter}/{author}/{work}/cache/{work}.txt
CCEL_MANUAL_MAP = {
    # 이미 존재하는 CCEL 대용량 볼륨에서 추출 가능한 것들
    # Edwards works - CCEL에는 개별 저작이 있을 수 있음
    "edwards-original-sin": ("https://ccel.org/ccel/e/edwards/works1/cache/works1.txt", "ccel"),
    "edwards-charity-its-fruits": ("https://ccel.org/ccel/e/edwards/works1/cache/works1.txt", "ccel"),
}

# ─── Gutenberg ebook ID 매핑 (확인된 것만) ───
GUTENBERG_MAP = {
    "ryle-practical-religion": 38162,
}


def main():
    manifest = json.loads(MANIFEST.read_text())
    sources = set(d for d in os.listdir(BOOKS_DIR) if not d.endswith(".txt"))

    # 미처리 항목만
    pending = [x for x in manifest if x["slug"] not in sources]
    print(f"미처리 항목: {len(pending)}")

    fixed = 0
    failed_slugs = []

    for i, info in enumerate(pending):
        slug = info["slug"]
        old_url = info["url"]
        source_type = info.get("source_type", "")

        print(f"\n[{i+1}/{len(pending)}] {slug} ({source_type})")

        new_url = None
        new_type = source_type

        # 1. 수동 매핑 확인
        if slug in CCEL_MANUAL_MAP:
            new_url, new_type = CCEL_MANUAL_MAP[slug]
            print(f"  → 수동 매핑: {new_url}")
        elif slug in GUTENBERG_MAP:
            eid = GUTENBERG_MAP[slug]
            new_url = f"https://www.gutenberg.org/cache/epub/{eid}/pg{eid}.txt"
            new_type = "gutenberg"
            print(f"  → Gutenberg #{eid}")

        # 2. 기존 URL 테스트
        if not new_url and old_url and old_url != "unknown":
            if check_url(old_url):
                print(f"  → 기존 URL 유효!")
                continue  # 수정 불필요

        # 3. CCEL 작가 페이지 탐색
        if not new_url and source_type == "ccel":
            m = re.search(r'/ccel/\w/(\w+)/(\w+)/', old_url)
            if m:
                author_id, work_id = m.group(1), m.group(2)
                print(f"  CCEL 탐색: {author_id}/{work_id}")
                result = find_ccel_text_url(author_id, work_id)
                if result:
                    new_url = result
                    print(f"  → CCEL 발견: {new_url}")
                time.sleep(0.5)  # rate limit

        # 4. Gutenberg 검색
        if not new_url:
            title_en = info.get("title_en", "")
            author_en = info.get("author_en", "")
            if title_en:
                print(f"  Gutenberg 검색: {title_en}")
                result = search_gutenberg(title_en, author_en)
                if result:
                    new_url = result
                    new_type = "gutenberg"
                    print(f"  → Gutenberg 발견: {new_url}")
                time.sleep(0.5)

        # 5. Archive.org 검색
        if not new_url:
            title_en = info.get("title_en", "")
            author_en = info.get("author_en", "")
            if title_en:
                print(f"  Archive.org 검색: {title_en}")
                result = search_archive(title_en, author_en)
                if result:
                    new_url = result
                    new_type = "archive"
                    print(f"  → Archive.org 발견: {new_url}")
                time.sleep(0.5)

        # 결과 적용
        if new_url:
            # manifest 업데이트
            for entry in manifest:
                if entry["slug"] == slug:
                    entry["url"] = new_url
                    entry["source_type"] = new_type
                    break
            fixed += 1
        else:
            print(f"  ❌ URL을 찾을 수 없음")
            failed_slugs.append(slug)

    # manifest 저장
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"\n\n=== 결과 ===")
    print(f"수정됨: {fixed}")
    print(f"실패: {len(failed_slugs)}")
    if failed_slugs:
        print(f"실패 목록: {failed_slugs}")


if __name__ == "__main__":
    main()
