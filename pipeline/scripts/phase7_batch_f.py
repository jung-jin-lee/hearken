#!/usr/bin/env python3
"""Phase 7 배치 F: 카테고리 76-77 (19세기 강해 설교자들 12 + 기독교 순교·박해 역사 8) — 20권."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.scripts.phase5_utils import process_all

BOOKS = [
    # ── 카테고리 76: 19세기 강해 설교자들 (12권) ──
    {
        "slug": "robertson-sermons-v1",
        "title": "F.W. 로버트슨 설교집 제1권",
        "title_en": "Sermons of F.W. Robertson Vol.1 (Series 1–2)",
        "author_kr": "F.W. 로버트슨",
        "author_en": "F.W. Robertson",
        "year": 1855,
    },
    {
        "slug": "robertson-sermons-v2",
        "title": "F.W. 로버트슨 설교집 제2권",
        "title_en": "Sermons of F.W. Robertson Vol.2 (Series 3–4)",
        "author_kr": "F.W. 로버트슨",
        "author_en": "F.W. Robertson",
        "year": 1855,
    },
    {
        "slug": "brooks-sermons-selected",
        "title": "필립스 브룩스 설교 선집",
        "title_en": "Sermons of Phillips Brooks (Selected Vol.1)",
        "author_kr": "필립스 브룩스",
        "author_en": "Phillips Brooks",
        "year": 1878,
    },
    {
        "slug": "brooks-lectures-on-preaching",
        "title": "설교학 강의 (예일 강의)",
        "title_en": "Lectures on Preaching (Yale Lectures on Preaching)",
        "author_kr": "필립스 브룩스",
        "author_en": "Phillips Brooks",
        "year": 1877,
    },
    {
        "slug": "maclaren-expositions-ot",
        "title": "성경 강해: 구약 (창세기~시편 선집)",
        "title_en": "Expositions of Holy Scripture: OT (Genesis – Psalms selections)",
        "author_kr": "알렉산더 맥라렌",
        "author_en": "Alexander Maclaren",
        "year": 1890,
    },
    {
        "slug": "maclaren-expositions-nt-v1",
        "title": "성경 강해: 신약 제1권 (마태복음~사도행전)",
        "title_en": "Expositions of Holy Scripture: NT Vol.1 (Matthew – Acts)",
        "author_kr": "알렉산더 맥라렌",
        "author_en": "Alexander Maclaren",
        "year": 1900,
    },
    {
        "slug": "maclaren-expositions-nt-v2",
        "title": "성경 강해: 신약 제2권 (로마서~요한계시록)",
        "title_en": "Expositions of Holy Scripture: NT Vol.2 (Romans – Revelation)",
        "author_kr": "알렉산더 맥라렌",
        "author_en": "Alexander Maclaren",
        "year": 1908,
    },
    {
        "slug": "simeon-horae-homileticae-sel",
        "title": "강해 설교 선집 — 시므온의 강해",
        "title_en": "Horae Homileticae: Expository Discourses (selections)",
        "author_kr": "찰스 시므온",
        "author_en": "Charles Simeon",
        "year": 1819,
    },
    {
        "slug": "dale-atonement",
        "title": "속죄론 강의",
        "title_en": "The Atonement (Congregational Lectures)",
        "author_kr": "R.W. 데일",
        "author_en": "R.W. Dale",
        "year": 1875,
    },
    {
        "slug": "dale-christian-doctrine",
        "title": "회중교회 원리 편람",
        "title_en": "Manual of Congregational Principles",
        "author_kr": "R.W. 데일",
        "author_en": "R.W. Dale",
        "year": 1884,
    },
    {
        "slug": "cox-salvator-mundi",
        "title": "세상의 구원자 — 보편 구원론 비판적 연구",
        "title_en": "Salvator Mundi: Is Christ the Saviour of All Men?",
        "author_kr": "새뮤얼 콕스",
        "author_en": "Samuel Cox",
        "year": 1877,
    },
    {
        "slug": "cadman-ambassadors-for-god",
        "title": "하나님의 대사들",
        "title_en": "Ambassadors for God",
        "author_kr": "S. 파크스 캐드먼",
        "author_en": "S. Parkes Cadman",
        "year": 1920,
    },
    # ── 카테고리 77: 기독교 순교·박해 역사 (8권) ──
    {
        "slug": "foxe-acts-monuments-v1",
        "title": "순교자 열전 제1권: 초대교회~위클리프",
        "title_en": "Foxe's Acts and Monuments Vol.1: Early Church to Wycliffe",
        "author_kr": "존 폭스",
        "author_en": "John Foxe",
        "year": 1563,
    },
    {
        "slug": "foxe-acts-monuments-v2",
        "title": "순교자 열전 제2권: 롤라드파~메리 여왕 이전",
        "title_en": "Foxe's Acts and Monuments Vol.2: Lollards to Pre-Marian England",
        "author_kr": "존 폭스",
        "author_en": "John Foxe",
        "year": 1563,
    },
    {
        "slug": "foxe-acts-monuments-v3",
        "title": "순교자 열전 제3권: 메리 여왕 시대 순교자들",
        "title_en": "Foxe's Acts and Monuments Vol.3: Marian Martyrs 1555–1558",
        "author_kr": "존 폭스",
        "author_en": "John Foxe",
        "year": 1563,
    },
    {
        "slug": "crespin-martyrs-france",
        "title": "프랑스 순교자들 (선집)",
        "title_en": "Book of Martyrs of France (Livre des Martyrs, selections)",
        "author_kr": "장 크레스팽",
        "author_en": "Jean Crespin",
        "year": 1554,
    },
    {
        "slug": "vermigli-common-places-sel",
        "title": "피터 마르티르 베르밀리 공통 주제 (선집)",
        "title_en": "Common Places of Peter Martyr Vermigli (selections)",
        "author_kr": "피터 마르티르 베르밀리",
        "author_en": "Peter Martyr Vermigli",
        "year": 1576,
    },
    {
        "slug": "wodrow-sufferings-church-sel",
        "title": "스코틀랜드 교회 수난사 (선집)",
        "title_en": "History of the Sufferings of the Church of Scotland (selections)",
        "author_kr": "로버트 우드로우",
        "author_en": "Robert Wodrow",
        "year": 1721,
    },
    {
        "slug": "gillies-historical-collections",
        "title": "부흥 기록 역사 모음",
        "title_en": "Historical Collections of Accounts of Revival",
        "author_kr": "존 길리스",
        "author_en": "John Gillies",
        "year": 1754,
    },
    {
        "slug": "brown-john-self-interpreting-bible",
        "title": "자기 해석 성경 — 순교자 주석 포함",
        "title_en": "The Self-Interpreting Bible with Notes on Martyrs",
        "author_kr": "존 브라운",
        "author_en": "John Brown",
        "year": 1778,
    },
]

if __name__ == "__main__":
    process_all(BOOKS)
