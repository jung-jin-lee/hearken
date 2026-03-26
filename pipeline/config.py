"""프로젝트 설정 및 상수 정의."""

import os
from pathlib import Path

from dotenv import load_dotenv

# 경로
PROJECT_ROOT = Path(__file__).parent.parent
PIPELINE_DIR = PROJECT_ROOT / "pipeline"
CONTENT_DIR = PROJECT_ROOT / "content"
SOURCES_DATA_DIR = PIPELINE_DIR / "sources" / "data"
BATCH_REQUESTS_DIR = PIPELINE_DIR / "batch" / "requests"
BATCH_RESULTS_DIR = PIPELINE_DIR / "batch" / "results"

# .env 로드
load_dotenv(PROJECT_ROOT / ".env")

# OpenAI
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
MODEL = "gpt-5.4"
BATCH_MODEL = "gpt-5.4"  # Batch API에서 사용할 모델

# 생성 파라미터
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2000

# 성경 구조 (개역한글)
BIBLE_BOOKS = [
    # 구약 (39권)
    {"id": "genesis", "kr": "창세기", "chapters": 50, "testament": "old"},
    {"id": "exodus", "kr": "출애굽기", "chapters": 40, "testament": "old"},
    {"id": "leviticus", "kr": "레위기", "chapters": 27, "testament": "old"},
    {"id": "numbers", "kr": "민수기", "chapters": 36, "testament": "old"},
    {"id": "deuteronomy", "kr": "신명기", "chapters": 34, "testament": "old"},
    {"id": "joshua", "kr": "여호수아", "chapters": 24, "testament": "old"},
    {"id": "judges", "kr": "사사기", "chapters": 21, "testament": "old"},
    {"id": "ruth", "kr": "룻기", "chapters": 4, "testament": "old"},
    {"id": "1samuel", "kr": "사무엘상", "chapters": 31, "testament": "old"},
    {"id": "2samuel", "kr": "사무엘하", "chapters": 24, "testament": "old"},
    {"id": "1kings", "kr": "열왕기상", "chapters": 22, "testament": "old"},
    {"id": "2kings", "kr": "열왕기하", "chapters": 25, "testament": "old"},
    {"id": "1chronicles", "kr": "역대상", "chapters": 29, "testament": "old"},
    {"id": "2chronicles", "kr": "역대하", "chapters": 36, "testament": "old"},
    {"id": "ezra", "kr": "에스라", "chapters": 10, "testament": "old"},
    {"id": "nehemiah", "kr": "느헤미야", "chapters": 13, "testament": "old"},
    {"id": "esther", "kr": "에스더", "chapters": 10, "testament": "old"},
    {"id": "job", "kr": "욥기", "chapters": 42, "testament": "old"},
    {"id": "psalms", "kr": "시편", "chapters": 150, "testament": "old"},
    {"id": "proverbs", "kr": "잠언", "chapters": 31, "testament": "old"},
    {"id": "ecclesiastes", "kr": "전도서", "chapters": 12, "testament": "old"},
    {"id": "songofsolomon", "kr": "아가", "chapters": 8, "testament": "old"},
    {"id": "isaiah", "kr": "이사야", "chapters": 66, "testament": "old"},
    {"id": "jeremiah", "kr": "예레미야", "chapters": 52, "testament": "old"},
    {"id": "lamentations", "kr": "예레미야애가", "chapters": 5, "testament": "old"},
    {"id": "ezekiel", "kr": "에스겔", "chapters": 48, "testament": "old"},
    {"id": "daniel", "kr": "다니엘", "chapters": 12, "testament": "old"},
    {"id": "hosea", "kr": "호세아", "chapters": 14, "testament": "old"},
    {"id": "joel", "kr": "요엘", "chapters": 3, "testament": "old"},
    {"id": "amos", "kr": "아모스", "chapters": 9, "testament": "old"},
    {"id": "obadiah", "kr": "오바댜", "chapters": 1, "testament": "old"},
    {"id": "jonah", "kr": "요나", "chapters": 4, "testament": "old"},
    {"id": "micah", "kr": "미가", "chapters": 7, "testament": "old"},
    {"id": "nahum", "kr": "나훔", "chapters": 3, "testament": "old"},
    {"id": "habakkuk", "kr": "하박국", "chapters": 3, "testament": "old"},
    {"id": "zephaniah", "kr": "스바냐", "chapters": 3, "testament": "old"},
    {"id": "haggai", "kr": "학개", "chapters": 2, "testament": "old"},
    {"id": "zechariah", "kr": "스가랴", "chapters": 14, "testament": "old"},
    {"id": "malachi", "kr": "말라기", "chapters": 4, "testament": "old"},
    # 신약 (27권)
    {"id": "matthew", "kr": "마태복음", "chapters": 28, "testament": "new"},
    {"id": "mark", "kr": "마가복음", "chapters": 16, "testament": "new"},
    {"id": "luke", "kr": "누가복음", "chapters": 24, "testament": "new"},
    {"id": "john", "kr": "요한복음", "chapters": 21, "testament": "new"},
    {"id": "acts", "kr": "사도행전", "chapters": 28, "testament": "new"},
    {"id": "romans", "kr": "로마서", "chapters": 16, "testament": "new"},
    {"id": "1corinthians", "kr": "고린도전서", "chapters": 16, "testament": "new"},
    {"id": "2corinthians", "kr": "고린도후서", "chapters": 13, "testament": "new"},
    {"id": "galatians", "kr": "갈라디아서", "chapters": 6, "testament": "new"},
    {"id": "ephesians", "kr": "에베소서", "chapters": 6, "testament": "new"},
    {"id": "philippians", "kr": "빌립보서", "chapters": 4, "testament": "new"},
    {"id": "colossians", "kr": "골로새서", "chapters": 4, "testament": "new"},
    {"id": "1thessalonians", "kr": "데살로니가전서", "chapters": 5, "testament": "new"},
    {"id": "2thessalonians", "kr": "데살로니가후서", "chapters": 3, "testament": "new"},
    {"id": "1timothy", "kr": "디모데전서", "chapters": 6, "testament": "new"},
    {"id": "2timothy", "kr": "디모데후서", "chapters": 4, "testament": "new"},
    {"id": "titus", "kr": "디도서", "chapters": 3, "testament": "new"},
    {"id": "philemon", "kr": "빌레몬서", "chapters": 1, "testament": "new"},
    {"id": "hebrews", "kr": "히브리서", "chapters": 13, "testament": "new"},
    {"id": "james", "kr": "야고보서", "chapters": 5, "testament": "new"},
    {"id": "1peter", "kr": "베드로전서", "chapters": 5, "testament": "new"},
    {"id": "2peter", "kr": "베드로후서", "chapters": 3, "testament": "new"},
    {"id": "1john", "kr": "요한1서", "chapters": 5, "testament": "new"},
    {"id": "2john", "kr": "요한2서", "chapters": 1, "testament": "new"},
    {"id": "3john", "kr": "요한3서", "chapters": 1, "testament": "new"},
    {"id": "jude", "kr": "유다서", "chapters": 1, "testament": "new"},
    {"id": "revelation", "kr": "요한계시록", "chapters": 22, "testament": "new"},
]

TOTAL_CHAPTERS = sum(b["chapters"] for b in BIBLE_BOOKS)  # 1,189

# 성경 인물 50인
BIBLE_CHARACTERS = [
    "아담", "노아", "아브라함", "사라", "이삭", "야곱", "요셉", "모세",
    "아론", "여호수아", "드보라", "기드온", "삼손", "룻", "사무엘", "다윗",
    "솔로몬", "엘리야", "엘리사", "이사야", "예레미야", "에스겔", "다니엘",
    "호세아", "요나", "에스더", "느헤미야", "에스라", "욥", "마리아",
    "요셉(마리아의 남편)", "세례 요한", "베드로", "안드레", "야고보", "요한",
    "마태", "도마", "바울", "바나바", "실라", "디모데", "브리스길라",
    "아굴라", "루디아", "스데반", "빌립", "막달라 마리아", "마르다", "나사로",
]

# 30개 주제
BIBLE_TOPICS = [
    "기도", "믿음", "사랑", "소망", "은혜", "구원", "회개", "용서",
    "성령", "예배", "감사", "겸손", "인내", "평화", "기쁨", "지혜",
    "순종", "제자도", "전도", "치유", "고난", "위로", "축복", "공의",
    "자비", "창조", "부활", "재림", "천국", "섬김",
]

# 주요 구절 500선에서 사용할 상위 구절 목록 (일부 시작점)
KEY_VERSE_REFERENCES = [
    "창세기 1:1", "창세기 12:1-3", "출애굽기 20:1-17", "신명기 6:4-5",
    "여호수아 1:9", "시편 23:1-6", "시편 46:10", "시편 119:105",
    "잠언 3:5-6", "이사야 40:31", "이사야 53:5", "예레미야 29:11",
    "마태복음 5:3-12", "마태복음 6:9-13", "마태복음 11:28-30", "마태복음 28:19-20",
    "요한복음 1:1", "요한복음 3:16", "요한복음 14:6", "요한복음 15:5",
    "로마서 3:23", "로마서 5:8", "로마서 8:28", "로마서 8:38-39",
    "로마서 12:1-2", "고린도전서 13:4-7", "고린도후서 5:17", "갈라디아서 2:20",
    "갈라디아서 5:22-23", "에베소서 2:8-9", "빌립보서 4:6-7", "빌립보서 4:13",
    "골로새서 3:23", "히브리서 11:1", "히브리서 12:1-2", "야고보서 1:2-4",
    "베드로전서 5:7", "요한1서 4:8", "요한계시록 21:4",
    # ... 나머지는 GPT로 생성 시 자동 선정
]

# 디렉토리 초기화
for d in [CONTENT_DIR, SOURCES_DATA_DIR, BATCH_REQUESTS_DIR, BATCH_RESULTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

for book in BIBLE_BOOKS:
    (CONTENT_DIR / "bible" / "commentary" / book["id"]).mkdir(parents=True, exist_ok=True)
