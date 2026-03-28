#!/usr/bin/env python3
"""Archive.org 접근 불가 4권 — OpenAI 직접 생성.

원문 텍스트를 가져오지 못한 책들의 핵심 내용을
OpenAI API로 한국어로 직접 생성.

사용법:
  python pipeline/scripts/add_missing_english_books.py
"""
import sys, json, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.config import CONTENT_DIR, OPENAI_API_KEY, MODEL
import openai

SYSTEM_PROMPT = (
    "당신은 기독교 고전 문헌 전문가입니다. "
    "주어진 책의 실제 신학적 내용과 저자의 논지를 충실히 재현합니다. "
    "원문의 핵심 가르침을 한국어로 자연스럽고 정확하게 전달하십시오. "
    "시각장애인이 음성으로 듣기 좋은 문체로 작성하십시오."
)

BOOKS = [
    {
        "slug": "perkins-art-prophesying",
        "title": "예언하는 기술",
        "author": "윌리엄 퍼킨스",
        "title_en": "The Art of Prophesying",
        "author_en": "William Perkins (1592)",
        "background": (
            "윌리엄 퍼킨스(1558-1602)는 청교도 신학의 아버지로 불립니다. "
            "《예언하는 기술》(The Art of Prophesying, 1592)은 성경적 설교학의 기초를 놓은 최초의 체계적 설교학 교과서입니다. "
            "설교는 성경 본문의 바른 해석과 적용에서 출발해야 한다는 그의 원칙은 "
            "이후 청교도 설교 전통 전체에 영향을 미쳤습니다."
        ),
        "chapters": [
            {"num": 1, "title": "설교의 정의와 목적", "context": "설교란 무엇인가, 왜 하나님은 설교를 선택하셨는가"},
            {"num": 2, "title": "성경 해석의 원칙", "context": "성경을 올바르게 읽고 해석하는 방법론"},
            {"num": 3, "title": "교리의 발견과 증명", "context": "본문에서 교리를 끌어내고 입증하는 방법"},
            {"num": 4, "title": "적용의 방법", "context": "교리를 회중의 삶에 구체적으로 적용하는 법"},
            {"num": 5, "title": "설교자의 기억과 전달", "context": "설교 준비와 전달에서의 실천적 지침"},
        ],
    },
    {
        "slug": "meyer-abraham",
        "title": "아브라함: 믿음의 순종",
        "author": "F.B. 메이어",
        "title_en": "Abraham: Or the Obedience of Faith",
        "author_en": "F.B. Meyer (1897)",
        "background": (
            "F.B. 메이어(1847-1929)는 19세기 영국의 저명한 설교자이자 영성 작가입니다. "
            "구약 인물 묵상 시리즈 중 하나인 《아브라함: 믿음의 순종》은 "
            "아브라함의 생애를 통해 하나님의 부르심과 믿음의 순종, 시험과 연단, "
            "하나님의 신실하심을 따뜻하고 실천적으로 묵상합니다."
        ),
        "chapters": [
            {"num": 1, "title": "하나님의 부르심", "context": "갈대아 우르에서의 부르심, 믿음으로 떠나는 아브라함"},
            {"num": 2, "title": "믿음과 연단의 길", "context": "가나안 정착과 기근, 믿음이 시험받는 과정"},
            {"num": 3, "title": "약속과 인내", "context": "이삭 탄생 약속, 오랜 기다림 속의 신뢰"},
            {"num": 4, "title": "모리아 산의 순종", "context": "이삭을 드리는 극한의 믿음과 하나님의 공급"},
            {"num": 5, "title": "믿음의 사람의 유산", "context": "아브라함이 남긴 믿음의 본, 우리를 향한 적용"},
        ],
    },
    {
        "slug": "meyer-joseph",
        "title": "요셉: 고난이 빚은 인격",
        "author": "F.B. 메이어",
        "title_en": "Joseph: Beloved-Hated-Exalted",
        "author_en": "F.B. Meyer (1897)",
        "background": (
            "F.B. 메이어의 요셉 묵상은 창세기 37-50장의 요셉 이야기를 통해 "
            "하나님의 섭리와 고난의 의미, 용서와 화해의 능력을 탐구합니다. "
            "형제들에게 팔려 노예가 되고 억울하게 감옥에 갔지만, "
            "결국 총리가 된 요셉의 삶에서 하나님의 선하신 손길을 발견합니다."
        ),
        "chapters": [
            {"num": 1, "title": "사랑받는 아들과 꿈", "context": "요셉의 꿈과 형제들의 시기, 버림받음의 고통"},
            {"num": 2, "title": "노예와 감옥의 길", "context": "보디발의 집과 억울한 감옥살이, 고난 속의 하나님"},
            {"num": 3, "title": "하나님의 시간", "context": "꿈의 해석과 파라오 앞에 서기까지의 과정"},
            {"num": 4, "title": "용서의 능력", "context": "형제들과의 재회, 용서와 화해의 눈물"},
            {"num": 5, "title": "섭리의 고백", "context": "요셉의 최후 고백: 악을 선으로 바꾸시는 하나님"},
        ],
    },
    {
        "slug": "chambers-still-higher",
        "title": "더 높은 곳을 향하여",
        "author": "오스왈드 챔버스",
        "title_en": "Still Higher for His Highest",
        "author_en": "Oswald Chambers (1927)",
        "background": (
            "오스왈드 챔버스(1874-1917)는 《주님은 나의 최고봉》(My Utmost for His Highest)으로 유명한 "
            "20세기 초의 탁월한 묵상 작가입니다. "
            "《더 높은 곳을 향하여》는 그의 설교와 강의에서 발췌한 묵상 모음으로, "
            "온전한 헌신과 성화, 그리스도와의 연합을 향한 여정을 다룹니다."
        ),
        "chapters": [
            {"num": 1, "title": "온전한 헌신의 부르심", "context": "하나님께 완전히 드리는 삶, 절반의 헌신이 아닌 전부"},
            {"num": 2, "title": "성령과 성화", "context": "성화는 인간의 노력이 아닌 성령의 역사임"},
            {"num": 3, "title": "그리스도의 십자가", "context": "십자가는 우리의 옛 자아가 죽는 곳"},
            {"num": 4, "title": "기도의 학교", "context": "기도는 기술이 아니라 하나님과의 관계"},
            {"num": 5, "title": "순종의 비밀", "context": "순종은 이해 후가 아니라 먼저 순종하는 것"},
        ],
    },
]


def build_prompt(book: dict, chapter: dict) -> str:
    return f"""다음 기독교 고전의 내용을 재현해 주세요.

책 정보:
- 제목: {book['title_en']}
- 저자: {book['author_en']}
- 배경: {book['background']}

생성할 내용:
- 제목: {chapter['title']}
- 맥락: {chapter['context']}

다음 JSON 형식으로 응답하십시오:
{{
  "chapter_title": "{chapter['title']}",
  "modern_translation": "이 장의 핵심 내용을 한국어로 풍성하게 서술 (1500-2500자, 실제 책의 내용처럼)",
  "summary": "핵심 내용 요약 (200-300자)",
  "key_points": ["핵심 포인트 3-5개"],
  "difficult_terms": [
    {{"term": "신학/역사적 용어", "explanation": "쉬운 설명"}}
  ],
  "reflection": "독자가 묵상할 점 (100-200자)"
}}

주의사항:
- modern_translation은 실제 책의 해당 장 내용처럼 풍부하게 작성하세요
- 해당 저자의 신학적 특성과 문체를 반영하세요
- difficult_terms는 2-4개 포함하세요"""


def generate_chapter(client: openai.OpenAI, book: dict, chapter: dict) -> dict | None:
    prompt = build_prompt(book, chapter)
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        print(f"    [에러] {e}")
        return None


def process_book(client: openai.OpenAI, book: dict):
    slug = book["slug"]
    out_dir = CONTENT_DIR / "books" / slug

    if out_dir.exists() and list(out_dir.glob("*.json")):
        print(f"  [건너뜀] {slug} (이미 존재)")
        return "skipped"

    out_dir.mkdir(parents=True, exist_ok=True)
    saved = 0

    for chapter in book["chapters"]:
        num = chapter["num"]
        title = chapter["title"]
        print(f"    [{num}/{len(book['chapters'])}] {title} 생성 중...")

        data = generate_chapter(client, book, chapter)
        if data is None:
            print(f"    [실패] {title}")
            continue

        output = {
            "book_slug": slug,
            "book_title": book["title"],
            "author": book["author"],
            "chapter_num": num,
            "chapter_title": data.get("chapter_title", title),
            "modern_translation": data.get("modern_translation", ""),
            "summary": data.get("summary", ""),
            "key_points": data.get("key_points", []),
            "difficult_terms": data.get("difficult_terms", []),
            "reflection": data.get("reflection", ""),
        }

        out_path = out_dir / f"{num:03d}.json"
        out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
        saved += 1
        print(f"    ✅ {out_path.name}")
        time.sleep(1.0)

    print(f"  ✅ {slug}: {saved}챕터 완료")
    return "success"


def main():
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY 없음")
        sys.exit(1)

    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    results = {"success": 0, "skipped": 0}

    for i, book in enumerate(BOOKS, 1):
        print(f"\n[{i}/{len(BOOKS)}] {book['slug']} — {book['title']}")
        status = process_book(client, book)
        results[status] = results.get(status, 0) + 1

    print(f"\n{'='*60}")
    print(f"성공: {results.get('success',0)}, 건너뜀: {results.get('skipped',0)}")


if __name__ == "__main__":
    main()
