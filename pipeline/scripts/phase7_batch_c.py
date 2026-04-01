#!/usr/bin/env python3
"""Phase 7 배치 C: 카테고리 70-71 (성공회 경건 고전 10 + 초기 감리교 신학 10) — 20권."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.scripts.phase5_utils import process_all

BOOKS = [
    # ── 카테고리 70: 성공회 경건 고전 (10권) ──
    {
        "slug": "taylor-holy-living",
        "title": "거룩한 삶의 규칙과 실천",
        "title_en": "The Rule and Exercises of Holy Living",
        "author_kr": "제레미 테일러",
        "author_en": "Jeremy Taylor",
        "year": 1650,
    },
    {
        "slug": "taylor-holy-dying",
        "title": "거룩한 죽음의 규칙과 실천",
        "title_en": "The Rule and Exercises of Holy Dying",
        "author_kr": "제레미 테일러",
        "author_en": "Jeremy Taylor",
        "year": 1651,
    },
    {
        "slug": "taylor-liberty-of-prophesying",
        "title": "예언의 자유 — 관용의 신학",
        "title_en": "The Liberty of Prophesying",
        "author_kr": "제레미 테일러",
        "author_en": "Jeremy Taylor",
        "year": 1647,
    },
    {
        "slug": "andrewes-preces-privatae",
        "title": "앤드류스 개인 기도서",
        "title_en": "Preces Privatae (Private Prayers)",
        "author_kr": "랜슬롯 앤드류스",
        "author_en": "Lancelot Andrewes",
        "year": 1648,
    },
    {
        "slug": "andrewes-sermons-nativity",
        "title": "성탄절 설교 17편",
        "title_en": "Seventeen Sermons on the Nativity",
        "author_kr": "랜슬롯 앤드류스",
        "author_en": "Lancelot Andrewes",
        "year": 1611,
    },
    {
        "slug": "hooker-laws-ecclesiastical-v1",
        "title": "교회 정치법 제1권 (제1-4서)",
        "title_en": "Laws of Ecclesiastical Polity Vol.1 (Books I–IV)",
        "author_kr": "리처드 후커",
        "author_en": "Richard Hooker",
        "year": 1594,
    },
    {
        "slug": "hooker-laws-ecclesiastical-v2",
        "title": "교회 정치법 제2권 (제5-8서)",
        "title_en": "Laws of Ecclesiastical Polity Vol.2 (Books V–VIII)",
        "author_kr": "리처드 후커",
        "author_en": "Richard Hooker",
        "year": 1597,
    },
    {
        "slug": "fuller-holy-state",
        "title": "거룩한 상태와 세속적 상태",
        "title_en": "The Holy State and the Profane State",
        "author_kr": "토마스 풀러",
        "author_en": "Thomas Fuller",
        "year": 1642,
    },
    {
        "slug": "hammond-practical-catechism",
        "title": "실천적 교리문답",
        "title_en": "A Practical Catechism",
        "author_kr": "헨리 해먼드",
        "author_en": "Henry Hammond",
        "year": 1644,
    },
    {
        "slug": "wilson-sacra-privata",
        "title": "개인 묵상과 기도",
        "title_en": "Sacra Privata: Private Meditations and Prayers",
        "author_kr": "토마스 윌슨",
        "author_en": "Thomas Wilson",
        "year": 1781,
    },
    # ── 카테고리 71: 초기 감리교 신학 명저 (10권) ──
    {
        "slug": "wesley-standard-sermons-v2",
        "title": "웨슬리 표준 설교집 제2권",
        "title_en": "Standard Sermons of John Wesley Vol.2 (Sermons 30–53)",
        "author_kr": "존 웨슬리",
        "author_en": "John Wesley",
        "year": 1760,
    },
    {
        "slug": "wesley-journal-v1",
        "title": "웨슬리 일기 제1권",
        "title_en": "Journal of John Wesley Vol.1 (1735–1745)",
        "author_kr": "존 웨슬리",
        "author_en": "John Wesley",
        "year": 1740,
    },
    {
        "slug": "wesley-journal-v2",
        "title": "웨슬리 일기 제2권",
        "title_en": "Journal of John Wesley Vol.2 (1745–1760)",
        "author_kr": "존 웨슬리",
        "author_en": "John Wesley",
        "year": 1755,
    },
    {
        "slug": "adam-clarke-commentary-nt-v1",
        "title": "클라크 신약 주석 제1권: 마태~사도행전",
        "title_en": "Clarke's Commentary on the New Testament Vol.1: Matt–Acts",
        "author_kr": "아담 클라크",
        "author_en": "Adam Clarke",
        "year": 1817,
    },
    {
        "slug": "adam-clarke-commentary-nt-v2",
        "title": "클라크 신약 주석 제2권: 로마서~요한계시록",
        "title_en": "Clarke's Commentary on the New Testament Vol.2: Romans–Revelation",
        "author_kr": "아담 클라크",
        "author_en": "Adam Clarke",
        "year": 1817,
    },
    {
        "slug": "charles-wesley-hymns-sacred-poems",
        "title": "찬송과 거룩한 시 전집",
        "title_en": "Hymns and Sacred Poems (Collected Edition)",
        "author_kr": "찰스 웨슬리",
        "author_en": "Charles Wesley",
        "year": 1740,
    },
    {
        "slug": "fletcher-appeal-common-sense",
        "title": "사실과 상식에 대한 호소",
        "title_en": "An Appeal to Matter of Fact and Common Sense",
        "author_kr": "존 플레처",
        "author_en": "John Fletcher",
        "year": 1772,
    },
    {
        "slug": "fletcher-checks-antinomianism-v1",
        "title": "무율법주의 반박 제1권",
        "title_en": "Checks to Antinomianism Vol.1",
        "author_kr": "존 플레처",
        "author_en": "John Fletcher",
        "year": 1771,
    },
    {
        "slug": "richard-watson-institutes-v1",
        "title": "감리교 신학 총론 제1권",
        "title_en": "Theological Institutes Vol.1",
        "author_kr": "리처드 왓슨",
        "author_en": "Richard Watson",
        "year": 1823,
    },
    {
        "slug": "richard-watson-institutes-v2",
        "title": "감리교 신학 총론 제2권",
        "title_en": "Theological Institutes Vol.2",
        "author_kr": "리처드 왓슨",
        "author_en": "Richard Watson",
        "year": 1823,
    },
]

if __name__ == "__main__":
    process_all(BOOKS)
