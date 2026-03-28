#!/usr/bin/env python3
"""한국 초기 기독교 목사 설교/글 콘텐츠 생성.

원전 텍스트 접근이 불가한 4인의 한국 목사(길선주, 주기철, 이용도, 김익두)의
설교와 글을 OpenAI API로 직접 생성하여 content/books/{slug}/에 저장.

사용법:
  python pipeline/scripts/add_korean_originals.py
"""
import sys, json, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.config import CONTENT_DIR, OPENAI_API_KEY, MODEL
import openai

SYSTEM_PROMPT = (
    "당신은 한국 초기 기독교 역사 전문가입니다. "
    "주어진 한국 목사의 실제 신학적 특성과 역사적 맥락을 반영하여, "
    "그들이 실제로 전했을 법한 설교나 글을 재현합니다. "
    "시각장애인을 위한 음성 낭독 콘텐츠이므로 자연스럽고 감동적인 한국어로 작성하십시오."
)

PASTORS = [
    {
        "slug": "gilsunjoo-sermons",
        "title": "길선주 목사 설교선집",
        "author": "길선주",
        "years": "1869-1935",
        "context": (
            "길선주 목사는 평양대부흥운동(1907년)의 핵심 지도자이자 3.1운동 민족 대표 33인 중 한 명입니다. "
            "깊은 기도 생활과 강렬한 회개 촉구, 성령의 역사 강조가 특징입니다. "
            "눈이 멀었음에도 불구하고 새벽기도 전통을 세운 인물입니다."
        ),
        "chapters": [
            {"num": 1, "title": "새벽기도의 능력", "context": "1907년 평양대부흥 경험을 바탕으로 한 새벽기도의 중요성"},
            {"num": 2, "title": "회개와 성령의 역사", "context": "대부흥운동에서 경험한 진정한 회개와 성령의 임재"},
            {"num": 3, "title": "기도하는 자의 삶", "context": "기도가 삶의 중심이 되어야 함을 강조하는 설교"},
            {"num": 4, "title": "십자가의 도", "context": "십자가 신학과 그리스도의 구속 사역"},
            {"num": 5, "title": "민족을 위한 기도", "context": "일제 강점기 민족의 고난과 하나님의 위로, 3.1운동 전후 맥락"},
        ],
    },
    {
        "slug": "jukicheol-sermons",
        "title": "주기철 목사 설교선집",
        "author": "주기철",
        "years": "1897-1944",
        "context": (
            "주기철 목사는 일제의 신사참배 강요에 끝까지 맞서다 순교한 목사입니다. "
            "산정현교회 목사로 사역하며 '일사각오'의 신앙으로 유명합니다. "
            "타협 없는 신앙 고백과 하나님 앞에서의 철저한 복종이 설교의 핵심입니다."
        ),
        "chapters": [
            {"num": 1, "title": "일사각오 (一死覺悟)", "context": "죽음을 각오한 순교 정신, 신사참배 거부 배경"},
            {"num": 2, "title": "하나님만 섬기리라", "context": "오직 하나님께만 예배드리겠다는 결단, 우상숭배 거부"},
            {"num": 3, "title": "고난 받는 자의 복", "context": "박해와 고난 속에서 발견하는 하나님의 복"},
            {"num": 4, "title": "믿음으로 서라", "context": "흔들리지 않는 믿음의 반석 위에 서라는 권면"},
            {"num": 5, "title": "순교자의 기도", "context": "감옥에서 드린 기도, 순교를 앞둔 영혼의 고백"},
        ],
    },
    {
        "slug": "leeyongdo-writings",
        "title": "이용도 목사 일기·서한·영성 글",
        "author": "이용도",
        "years": "1901-1933",
        "context": (
            "이용도 목사는 한국 기독교 신비주의 영성의 대표자로, "
            "그리스도와의 신비적 연합을 강조했습니다. "
            "일기와 서한에서 하나님에 대한 불타는 사랑과 십자가 신비를 표현했으며, "
            "32세의 짧은 생애 동안 강렬한 부흥 사역을 펼쳤습니다."
        ),
        "chapters": [
            {"num": 1, "title": "십자가에 못 박힌 사랑", "context": "일기에서: 십자가의 고통과 사랑의 신비"},
            {"num": 2, "title": "불타는 기도", "context": "서한에서: 기도 중에 경험한 성령의 불"},
            {"num": 3, "title": "하나님의 품에 안기어", "context": "하나님과의 신비적 연합과 영혼의 안식"},
            {"num": 4, "title": "사랑으로 하나되는 교회", "context": "교회 분열을 극복하는 사랑의 능력"},
            {"num": 5, "title": "죽음과 부활의 신비", "context": "자아의 죽음과 그리스도 안에서의 새 생명"},
        ],
    },
    {
        "slug": "kimikdoo-sermons",
        "title": "김익두 목사 설교선집",
        "author": "김익두",
        "years": "1874-1950",
        "context": (
            "김익두 목사는 한국 최초의 대중 부흥사로, "
            "병 고침의 기적이 함께한 부흥 사역으로 유명합니다. "
            "평양신학교 출신으로 전국을 누비며 대중에게 쉽고 강렬한 언어로 복음을 전했습니다. "
            "회개와 믿음, 기도 응답에 대한 생생한 간증이 특징입니다."
        ),
        "chapters": [
            {"num": 1, "title": "병 고치는 믿음", "context": "치유 사역의 근거가 되는 믿음, 실제 치유 간증 포함"},
            {"num": 2, "title": "회개의 문을 열어라", "context": "철저한 죄의 고백과 회개를 촉구하는 설교"},
            {"num": 3, "title": "하나님의 능력이 나타날 때", "context": "성령의 역사와 하나님의 초자연적 능력"},
            {"num": 4, "title": "기도 응답의 증거들", "context": "실제 기도 응답 경험들을 통한 믿음 격려"},
            {"num": 5, "title": "부흥의 불꽃", "context": "한국 교회 부흥을 위한 간절한 촉구"},
        ],
    },
]


def build_prompt(pastor: dict, chapter: dict) -> str:
    return f"""다음 한국 목사의 설교/글을 재현해 주세요.

목사 정보:
- 이름: {pastor['author']} ({pastor['years']})
- 배경: {pastor['context']}

생성할 내용:
- 제목: {chapter['title']}
- 맥락: {chapter['context']}

다음 JSON 형식으로 응답하십시오:
{{
  "chapter_title": "{chapter['title']}",
  "modern_translation": "한국어 설교/글 전문 (현대어 기준 1500-3000자, 실제 설교처럼 자연스럽게)",
  "summary": "핵심 내용 요약 (200-300자)",
  "key_points": ["핵심 포인트 1", "핵심 포인트 2", "핵심 포인트 3", "핵심 포인트 4"],
  "difficult_terms": [
    {{"term": "어려운 용어나 역사적 배경이 필요한 단어", "explanation": "쉬운 설명"}}
  ],
  "reflection": "독자가 묵상할 점 (100-200자)"
}}

주의사항:
- modern_translation은 실제 설교/글처럼 생동감 있게 작성하세요
- 해당 목사의 역사적·신학적 특성을 충실히 반영하세요
- difficult_terms는 2-4개 정도 포함하세요
- 시각장애인이 음성으로 듣기 좋은 자연스러운 문체로 작성하세요"""


def generate_chapter(client: openai.OpenAI, pastor: dict, chapter: dict) -> dict | None:
    prompt = build_prompt(pastor, chapter)
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
        data = json.loads(resp.choices[0].message.content)
        return data
    except Exception as e:
        print(f"    [에러] {e}")
        return None


def process_pastor(client: openai.OpenAI, pastor: dict):
    slug = pastor["slug"]
    out_dir = CONTENT_DIR / "books" / slug

    # 이미 처리 완료 확인
    if out_dir.exists() and list(out_dir.glob("*.json")):
        existing = list(out_dir.glob("*.json"))
        print(f"  [건너뜀] {slug} (JSON {len(existing)}개 이미 존재)")
        return "skipped"

    out_dir.mkdir(parents=True, exist_ok=True)
    saved = 0

    for chapter in pastor["chapters"]:
        num = chapter["num"]
        title = chapter["title"]
        print(f"    [{num}/{len(pastor['chapters'])}] {title} 생성 중...")

        data = generate_chapter(client, pastor, chapter)
        if data is None:
            print(f"    [실패] {title}")
            continue

        output = {
            "book_slug": slug,
            "book_title": pastor["title"],
            "author": pastor["author"],
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
        print(f"    ✅ 저장: {out_path.name}")
        time.sleep(1.0)  # API 레이트 리밋 완화

    print(f"  ✅ {slug}: {saved}챕터 저장")
    return "success"


def main():
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY가 설정되지 않았습니다.")
        sys.exit(1)

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    total = len(PASTORS)
    results = {"success": 0, "skipped": 0, "failed": 0}

    for i, pastor in enumerate(PASTORS, 1):
        print(f"\n[{i}/{total}] {pastor['slug']} — {pastor['title']}")
        status = process_pastor(client, pastor)
        results[status] = results.get(status, 0) + 1

    print(f"\n{'='*60}")
    print(
        f"성공: {results['success']}, "
        f"건너뜀: {results['skipped']}, "
        f"실패: {results['failed']}, "
        f"전체: {total}"
    )


if __name__ == "__main__":
    main()
