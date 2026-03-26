#!/usr/bin/env python3
"""KorRV.txt를 파이프라인이 기대하는 형식으로 변환하고 장별 캐시에 저장한다.

입력 형식:  ### Genesis / [1:1] 태초에 하나님이...
출력 형식:  창세기 1:1 태초에 하나님이...

사용법:
  python -m pipeline.scripts.convert_korRV /tmp/KorRV.txt
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.sources.bible_kr import save_chapter_text

# 영문 책이름 → (book_id, 한글이름) 매핑
BOOK_MAP = {
    "Genesis": ("genesis", "창세기"),
    "Exodus": ("exodus", "출애굽기"),
    "Leviticus": ("leviticus", "레위기"),
    "Numbers": ("numbers", "민수기"),
    "Deuteronomy": ("deuteronomy", "신명기"),
    "Joshua": ("joshua", "여호수아"),
    "Judges": ("judges", "사사기"),
    "Ruth": ("ruth", "룻기"),
    "I Samuel": ("1samuel", "사무엘상"),
    "II Samuel": ("2samuel", "사무엘하"),
    "I Kings": ("1kings", "열왕기상"),
    "II Kings": ("2kings", "열왕기하"),
    "I Chronicles": ("1chronicles", "역대상"),
    "II Chronicles": ("2chronicles", "역대하"),
    "Ezra": ("ezra", "에스라"),
    "Nehemiah": ("nehemiah", "느헤미야"),
    "Esther": ("esther", "에스더"),
    "Job": ("job", "욥기"),
    "Psalms": ("psalms", "시편"),
    "Proverbs": ("proverbs", "잠언"),
    "Ecclesiastes": ("ecclesiastes", "전도서"),
    "Song of Solomon": ("songofsolomon", "아가"),
    "Isaiah": ("isaiah", "이사야"),
    "Jeremiah": ("jeremiah", "예레미야"),
    "Lamentations": ("lamentations", "예레미야애가"),
    "Ezekiel": ("ezekiel", "에스겔"),
    "Daniel": ("daniel", "다니엘"),
    "Hosea": ("hosea", "호세아"),
    "Joel": ("joel", "요엘"),
    "Amos": ("amos", "아모스"),
    "Obadiah": ("obadiah", "오바댜"),
    "Jonah": ("jonah", "요나"),
    "Micah": ("micah", "미가"),
    "Nahum": ("nahum", "나훔"),
    "Habakkuk": ("habakkuk", "하박국"),
    "Zephaniah": ("zephaniah", "스바냐"),
    "Haggai": ("haggai", "학개"),
    "Zechariah": ("zechariah", "스가랴"),
    "Malachi": ("malachi", "말라기"),
    "Matthew": ("matthew", "마태복음"),
    "Mark": ("mark", "마가복음"),
    "Luke": ("luke", "누가복음"),
    "John": ("john", "요한복음"),
    "Acts": ("acts", "사도행전"),
    "Romans": ("romans", "로마서"),
    "I Corinthians": ("1corinthians", "고린도전서"),
    "II Corinthians": ("2corinthians", "고린도후서"),
    "Galatians": ("galatians", "갈라디아서"),
    "Ephesians": ("ephesians", "에베소서"),
    "Philippians": ("philippians", "빌립보서"),
    "Colossians": ("colossians", "골로새서"),
    "I Thessalonians": ("1thessalonians", "데살로니가전서"),
    "II Thessalonians": ("2thessalonians", "데살로니가후서"),
    "I Timothy": ("1timothy", "디모데전서"),
    "II Timothy": ("2timothy", "디모데후서"),
    "Titus": ("titus", "디도서"),
    "Philemon": ("philemon", "빌레몬서"),
    "Hebrews": ("hebrews", "히브리서"),
    "James": ("james", "야고보서"),
    "I Peter": ("1peter", "베드로전서"),
    "II Peter": ("2peter", "베드로후서"),
    "I John": ("1john", "요한1서"),
    "II John": ("2john", "요한2서"),
    "III John": ("3john", "요한3서"),
    "Jude": ("jude", "유다서"),
    "Revelation of John": ("revelation", "요한계시록"),
}


def convert_and_save(input_path: Path) -> None:
    """KorRV.txt를 파싱하여 장별 캐시 파일로 저장한다."""
    text = input_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    current_book_id = None
    current_book_kr = None
    # {chapter_num: [(verse_num, text), ...]}
    chapters: dict[int, list[str]] = {}

    total_saved = 0

    def flush_chapters():
        nonlocal total_saved
        if not current_book_id or not chapters:
            return
        for ch_num in sorted(chapters.keys()):
            verses = chapters[ch_num]
            chapter_text = "\n".join(verses)
            save_chapter_text(current_book_id, ch_num, chapter_text)
            total_saved += 1

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 책 헤더
        if line.startswith("### "):
            flush_chapters()
            chapters = {}
            book_name = line[4:].strip()
            mapping = BOOK_MAP.get(book_name)
            if mapping:
                current_book_id, current_book_kr = mapping
            else:
                print(f"[경고] 매핑 없음: {book_name}")
                current_book_id = None
                current_book_kr = None
            continue

        # 절 파싱: [1:1] 본문
        match = re.match(r"\[(\d+):(\d+)\]\s+(.+)", line)
        if match and current_book_id:
            chapter = int(match.group(1))
            verse = int(match.group(2))
            text = match.group(3).strip()

            if chapter not in chapters:
                chapters[chapter] = []
            chapters[chapter].append(f"{verse} {text}")

    # 마지막 책 flush
    flush_chapters()

    print(f"\n[완료] {total_saved}장 저장됨")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python -m pipeline.scripts.convert_korRV <KorRV.txt 경로>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"[오류] 파일 없음: {input_path}")
        sys.exit(1)

    convert_and_save(input_path)
