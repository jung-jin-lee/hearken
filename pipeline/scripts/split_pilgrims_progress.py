#!/usr/bin/env python3
"""천로역정 원문을 여정 단계별 챕터로 분할하고 metadata.json을 생성한다.

사용법:
  python -m pipeline.scripts.split_pilgrims_progress
"""

import json
import re
from pathlib import Path

RAW_FILE = Path("pipeline/sources/data/books/pilgrims-progress-raw.txt")
OUT_DIR = Path("pipeline/sources/data/books/pilgrims-progress")

# 여정 단계별 챕터 정의: (챕터번호, 제목, 시작섹션, 끝섹션)
CHAPTERS = [
    (1, "저자의 변론 (The Author's Apology)", 1, 9),
    (2, "멸망의 도시를 떠나다 (The City of Destruction)", 10, 18),
    (3, "고집쟁이와 유순이 (Obstinate and Pliable)", 19, 28),
    (4, "낙심의 늪 (The Slough of Despond)", 29, 36),
    (5, "세속적 현자 (Mr. Worldly Wiseman)", 37, 54),
    (6, "좁은 문 (The Wicket-Gate)", 55, 68),
    (7, "해석자의 집 (The House of the Interpreter)", 69, 91),
    (8, "십자가와 짐을 벗다 (The Cross and the Burden)", 92, 103),
    (9, "어려움의 언덕 (The Hill Difficulty)", 104, 117),
    (10, "아름다운 궁전 (The Palace Beautiful)", 118, 140),
    (11, "겸손의 골짜기와 아볼루온 (Valley of Humiliation & Apollyon)", 141, 158),
    (12, "사망의 그늘의 골짜기 (Valley of the Shadow of Death)", 159, 174),
    (13, "신실이와의 동행 (Faithful as Companion)", 175, 205),
    (14, "수다쟁이 (Talkative)", 206, 230),
    (15, "허영의 시장 (Vanity Fair)", 231, 262),
    (16, "신실이의 순교와 소망이 (Faithful's Martyrdom & Hopeful)", 263, 280),
    (17, "이득 씨와 뒷길 초원 (By-ends & By-path Meadow)", 281, 295),
    (18, "의심의 성과 절망의 거인 (Doubting Castle & Giant Despair)", 296, 310),
    (19, "기쁨의 산 (The Delectable Mountains)", 311, 327),
    (20, "아첨꾼과 무지 (The Flatterer & Ignorance)", 328, 355),
    (21, "무신론자와 마법의 땅 (Atheist & The Enchanted Ground)", 356, 381),
    (22, "뷸라 땅 (The Land of Beulah)", 382, 392),
    (23, "죽음의 강과 천성 (The River of Death & The Celestial City)", 393, 405),
]


def load_raw_text() -> str:
    """원문 텍스트를 로드한다."""
    text = RAW_FILE.read_text(encoding="utf-8")
    # Gutenberg 머리글/꼬리글 제거
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    start_idx = text.find(start_marker)
    if start_idx != -1:
        start_idx = text.index("\n", start_idx) + 1
    else:
        start_idx = 0
    end_idx = text.find(end_marker)
    if end_idx == -1:
        end_idx = len(text)
    return text[start_idx:end_idx].strip()


def split_into_sections(text: str) -> dict[int, str]:
    """텍스트를 {N} 섹션 번호 기준으로 분할한다."""
    pattern = re.compile(r"^\{(\d+)\}\s*", re.MULTILINE)
    matches = list(pattern.finditer(text))
    sections = {}
    for i, m in enumerate(matches):
        num = int(m.group(1))
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[num] = text[start:end].strip()
    return sections


def extract_chapter(sections: dict[int, str], start: int, end: int) -> str:
    """지정된 섹션 범위의 텍스트를 합친다."""
    parts = []
    for num in range(start, end + 1):
        if num in sections:
            parts.append(sections[num])
    return "\n\n".join(parts)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("원문 로드 중...")
    text = load_raw_text()

    print("섹션 분할 중...")
    sections = split_into_sections(text)
    print(f"  총 {len(sections)}개 섹션 발견")

    # 챕터별 파일 생성
    metadata_chapters = []
    for ch_num, title, start_sec, end_sec in CHAPTERS:
        ch_text = extract_chapter(sections, start_sec, end_sec)
        filename = f"ch{ch_num:02d}.txt"
        out_path = OUT_DIR / filename
        out_path.write_text(ch_text, encoding="utf-8")

        word_count = len(ch_text.split())
        print(f"  ch{ch_num:02d}: {title} (§{start_sec}-{end_sec}, {word_count} words)")

        metadata_chapters.append({
            "num": ch_num,
            "title": title,
            "file": filename,
            "sections": f"{start_sec}-{end_sec}",
        })

    # metadata.json 생성
    metadata = {
        "slug": "pilgrims-progress",
        "title": "천로역정",
        "title_original": "The Pilgrim's Progress from This World to That Which Is to Come",
        "author": "존 번연 (John Bunyan)",
        "author_original": "John Bunyan",
        "year": "1678",
        "source": "https://www.gutenberg.org/ebooks/131",
        "license": "public_domain",
        "note": "Part One only. 405 sections split into 23 chapters by journey stage.",
        "chapters": metadata_chapters,
    }

    meta_path = OUT_DIR / "metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"\n완료! {len(CHAPTERS)}개 챕터 생성됨")
    print(f"  출력: {OUT_DIR}")
    print(f"  메타데이터: {meta_path}")


if __name__ == "__main__":
    main()
