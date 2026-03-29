#!/usr/bin/env python3
"""Phase 6 배치 G: 카테고리 61-63 (독일 경건주의, 스코틀랜드 자유교회, 조직신학 보조) — 20권."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.scripts.phase5_utils import process_all

BOOKS = [
    # ── 카테고리 61: 독일 경건주의 창시 문헌 (6권) ──
    {
        "slug": "spener-pia-desideria",
        "title": "경건한 소망",
        "title_en": "Pia Desideria (Pious Desires)",
        "author_kr": "필리프 야코프 슈페너",
        "author_en": "Philip Jakob Spener",
        "year": 1675,
    },
    {
        "slug": "francke-autobiography",
        "title": "프랑케 자서전",
        "title_en": "Autobiography of A.H. Francke",
        "author_kr": "아우구스트 헤르만 프랑케",
        "author_en": "August Hermann Francke",
        "year": 1727,
    },
    {
        "slug": "francke-guide-scripture",
        "title": "성경 읽기 안내",
        "title_en": "A Guide to the Reading of Holy Scripture",
        "author_kr": "아우구스트 헤르만 프랑케",
        "author_en": "August Hermann Francke",
        "year": 1693,
    },
    {
        "slug": "zinzendorf-nine-lectures",
        "title": "종교의 주요 주제에 관한 아홉 강의",
        "title_en": "Nine Public Lectures on Important Subjects in Religion",
        "author_kr": "니콜라우스 폰 친첸도르프",
        "author_en": "Nikolaus von Zinzendorf",
        "year": 1748,
    },
    {
        "slug": "tersteegen-quiet-way-sel",
        "title": "조용한 길: 서신과 저술 (선집)",
        "title_en": "The Quiet Way: Letters and Writings (selections)",
        "author_kr": "게르하르트 테르스테겐",
        "author_en": "Gerhard Tersteegen",
        "year": 1769,
    },
    {
        "slug": "bengel-ordered-life",
        "title": "질서 잡힌 삶: 서신과 일기 (선집)",
        "title_en": "Ordered Life: Letters and Journal (selections)",
        "author_kr": "요한 알브레흐트 벵겔",
        "author_en": "Johann Albrecht Bengel",
        "year": 1759,
    },
    # ── 카테고리 62: 스코틀랜드 자유교회 신학 (7권) ──
    {
        "slug": "duncan-colloquia-peripatetica",
        "title": "소요하며 나눈 대화",
        "title_en": "Colloquia Peripatetica (Rich Gleanings)",
        "author_kr": "존 랍비 던컨",
        "author_en": 'John "Rabbi" Duncan',
        "year": 1870,
    },
    {
        "slug": "denney-death-of-christ",
        "title": "그리스도의 죽음",
        "title_en": "The Death of Christ",
        "author_kr": "제임스 데니",
        "author_en": "James Denney",
        "year": 1902,
    },
    {
        "slug": "denney-atonement-modern-mind",
        "title": "속죄와 현대적 이해",
        "title_en": "The Atonement and the Modern Mind",
        "author_kr": "제임스 데니",
        "author_en": "James Denney",
        "year": 1903,
    },
    {
        "slug": "forsyth-cruciality-cross",
        "title": "십자가의 결정적 의미",
        "title_en": "The Cruciality of the Cross",
        "author_kr": "P.T. 포르시스",
        "author_en": "P.T. Forsyth",
        "year": 1909,
    },
    {
        "slug": "forsyth-soul-of-prayer",
        "title": "기도의 영혼",
        "title_en": "The Soul of Prayer",
        "author_kr": "P.T. 포르시스",
        "author_en": "P.T. Forsyth",
        "year": 1916,
    },
    {
        "slug": "bruce-training-twelve",
        "title": "열두 제자 훈련",
        "title_en": "The Training of the Twelve",
        "author_kr": "알렉산더 발메인 브루스",
        "author_en": "Alexander Balmain Bruce",
        "year": 1871,
    },
    {
        "slug": "caird-gospel-of-saint-luke",
        "title": "누가복음 주석",
        "title_en": "Commentary on the Gospel of Luke",
        "author_kr": "조지 브래드퍼드 카드",
        "author_en": "George Bradford Caird",
        "year": 1899,
    },
    # ── 카테고리 63: 조직신학 보조 명저 (7권) ──
    {
        "slug": "moule-romans-devotional",
        "title": "로마서 강해 (성경 강해 시리즈)",
        "title_en": "The Epistle of Paul to the Romans (Expositor's Bible)",
        "author_kr": "핸들리 C.G. 무울",
        "author_en": "Handley C.G. Moule",
        "year": 1894,
    },
    {
        "slug": "moule-philippian-studies",
        "title": "빌립보서 연구",
        "title_en": "Philippian Studies",
        "author_kr": "핸들리 C.G. 무울",
        "author_en": "Handley C.G. Moule",
        "year": 1897,
    },
    {
        "slug": "orr-christian-view-of-god",
        "title": "하나님과 세계에 대한 기독교적 관점",
        "title_en": "The Christian View of God and the World",
        "author_kr": "제임스 오르",
        "author_en": "James Orr",
        "year": 1893,
    },
    {
        "slug": "orr-progress-dogma",
        "title": "교의학의 발전",
        "title_en": "The Progress of Dogma",
        "author_kr": "제임스 오르",
        "author_en": "James Orr",
        "year": 1901,
    },
    {
        "slug": "stewart-life-in-christ",
        "title": "그리스도 안의 사람",
        "title_en": "A Man in Christ",
        "author_kr": "제임스 S. 스튜어트",
        "author_en": "James S. Stewart",
        "year": 1935,
    },
    {
        "slug": "denny-atonement",
        "title": "속죄의 기독교 교리",
        "title_en": "The Christian Doctrine of Atonement",
        "author_kr": "로버트 윌리엄 데일",
        "author_en": "Robert William Dale",
        "year": 1875,
    },
    {
        "slug": "dale-romans-lectures",
        "title": "유대 성전과 기독교 교회 (선집)",
        "title_en": "The Jewish Temple and the Christian Church (sel.)",
        "author_kr": "로버트 윌리엄 데일",
        "author_en": "Robert William Dale",
        "year": 1865,
    },
]

if __name__ == "__main__":
    process_all(BOOKS)
