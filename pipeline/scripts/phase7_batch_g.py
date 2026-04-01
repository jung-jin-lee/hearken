#!/usr/bin/env python3
"""Phase 7 배치 G: 카테고리 78-79 (신앙과 과학 변증학 8 + 선교 역사 1차 사료 추가 8) — 16권."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.scripts.phase5_utils import process_all

BOOKS = [
    # ── 카테고리 78: 신앙과 과학 변증학 (8권) ──
    {
        "slug": "hodge-what-is-darwinism",
        "title": "다윈주의란 무엇인가?",
        "title_en": "What is Darwinism?",
        "author_kr": "찰스 호지",
        "author_en": "Charles Hodge",
        "year": 1874,
    },
    {
        "slug": "miller-footprints-of-creator",
        "title": "창조자의 발자국",
        "title_en": "The Footprints of the Creator",
        "author_kr": "휴 밀러",
        "author_en": "Hugh Miller",
        "year": 1849,
    },
    {
        "slug": "miller-testimony-of-rocks",
        "title": "바위의 증언 — 지질학과 성경 창조론",
        "title_en": "The Testimony of the Rocks",
        "author_kr": "휴 밀러",
        "author_en": "Hugh Miller",
        "year": 1857,
    },
    {
        "slug": "mccosh-method-divine-government",
        "title": "하나님의 통치 방법 — 신학적 자연주의",
        "title_en": "The Method of the Divine Government",
        "author_kr": "제임스 맥코시",
        "author_en": "James McCosh",
        "year": 1850,
    },
    {
        "slug": "mccosh-intuitions-of-mind",
        "title": "귀납법으로 탐구한 마음의 직관",
        "title_en": "The Intuitions of the Mind Inductively Investigated",
        "author_kr": "제임스 맥코시",
        "author_en": "James McCosh",
        "year": 1860,
    },
    {
        "slug": "dawson-origin-of-world",
        "title": "계시와 과학에 따른 세계의 기원",
        "title_en": "The Origin of the World According to Revelation and Science",
        "author_kr": "J.W. 도슨",
        "author_en": "J.W. Dawson",
        "year": 1877,
    },
    {
        "slug": "rawlinson-historical-evidence",
        "title": "홍수의 역사적 증거",
        "title_en": "Historical Evidence of the Mosaic Account of the Deluge",
        "author_kr": "조지 롤린슨",
        "author_en": "George Rawlinson",
        "year": 1876,
    },
    {
        "slug": "salmon-infallibility-of-church",
        "title": "교회의 무오성 — 로마 가톨릭 교황 무오설 비판",
        "title_en": "The Infallibility of the Church",
        "author_kr": "조지 살몬",
        "author_en": "George Salmon",
        "year": 1888,
    },
    # ── 카테고리 79: 선교 역사 1차 사료 추가 (8권) ──
    {
        "slug": "judson-adoniram-memoir",
        "title": "아도니람 저드슨 전기",
        "title_en": "Memoir of the Rev. Adoniram Judson",
        "author_kr": "프랜시스 웨일런드",
        "author_en": "Francis Wayland",
        "year": 1853,
    },
    {
        "slug": "zwemer-islam-challenge-to-faith",
        "title": "이슬람, 신앙에 대한 도전",
        "title_en": "Islam, a Challenge to Faith",
        "author_kr": "새뮤얼 즈워머",
        "author_en": "Samuel M. Zwemer",
        "year": 1907,
    },
    {
        "slug": "zwemer-moslem-world",
        "title": "무슬림 세계",
        "title_en": "The Moslem World (periodical selections)",
        "author_kr": "새뮤얼 즈워머",
        "author_en": "Samuel M. Zwemer",
        "year": 1920,
    },
    {
        "slug": "marsden-observations-nz",
        "title": "뉴질랜드 기독교 소개 관찰 기록",
        "title_en": "Observations on the Introduction of Christianity in New Zealand",
        "author_kr": "새뮤얼 마스든",
        "author_en": "Samuel Marsden",
        "year": 1838,
    },
    {
        "slug": "schwartz-life-letters",
        "title": "슈바르츠 선교사 생애와 서신",
        "title_en": "Life and Letters of Christian Friedrich Schwartz of Tanjore",
        "author_kr": "H.N. 피어슨",
        "author_en": "H.N. Pearson",
        "year": 1826,
    },
    {
        "slug": "carey-letters-memoir",
        "title": "윌리엄 캐리 서신집과 전기",
        "title_en": "Letters of William Carey with Biographical Notes",
        "author_kr": "유스테이스 캐리",
        "author_en": "Eustace Carey",
        "year": 1836,
    },
    {
        "slug": "moffat-missionary-labours",
        "title": "남아프리카 선교 사역과 풍경",
        "title_en": "Missionary Labours and Scenes in Southern Africa",
        "author_kr": "로버트 모팻",
        "author_en": "Robert Moffat",
        "year": 1842,
    },
    {
        "slug": "williams-missionary-enterprises",
        "title": "남태평양 선교 사업",
        "title_en": "Missionary Enterprises in the South Sea Islands",
        "author_kr": "존 윌리엄스",
        "author_en": "John Williams",
        "year": 1837,
    },
]

if __name__ == "__main__":
    process_all(BOOKS)
