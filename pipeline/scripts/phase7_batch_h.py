#!/usr/bin/env python3
"""Phase 7 배치 H: 카테고리 80 (교회사 보조 명저) — 10권."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.scripts.phase5_utils import process_all

BOOKS = [
    # ── 카테고리 80: 교회사 보조 명저 (10권) ──
    {
        "slug": "neander-church-history-v1",
        "title": "기독교 역사 총론 제1권: 사도 시대",
        "title_en": "General History of the Christian Religion Vol.1 (Apostolic Age)",
        "author_kr": "요한 노이안더",
        "author_en": "Johann Neander",
        "year": 1842,
    },
    {
        "slug": "neander-church-history-v2",
        "title": "기독교 역사 총론 제2권: 2-4세기",
        "title_en": "General History of the Christian Religion Vol.2 (2nd–4th Century)",
        "author_kr": "요한 노이안더",
        "author_en": "Johann Neander",
        "year": 1845,
    },
    {
        "slug": "mosheim-ecclesiastical-history-v1",
        "title": "교회사 총론 제1권: 고대·중세",
        "title_en": "Institutes of Ecclesiastical History Vol.1 (Ancient & Medieval)",
        "author_kr": "요한 로렌츠 모스하임",
        "author_en": "J.L. von Mosheim",
        "year": 1755,
    },
    {
        "slug": "mosheim-ecclesiastical-history-v2",
        "title": "교회사 총론 제2권: 근대",
        "title_en": "Institutes of Ecclesiastical History Vol.2 (Modern)",
        "author_kr": "요한 로렌츠 모스하임",
        "author_en": "J.L. von Mosheim",
        "year": 1755,
    },
    {
        "slug": "kurtz-church-history-v1",
        "title": "교회사 제1권: 사도 시대~종교개혁 이전",
        "title_en": "Church History Vol.1: Apostolic Age to Pre-Reformation",
        "author_kr": "요한 쿠르츠",
        "author_en": "Johann Kurtz",
        "year": 1860,
    },
    {
        "slug": "kurtz-church-history-v2",
        "title": "교회사 제2권: 종교개혁~근대",
        "title_en": "Church History Vol.2: Reformation to Modern Age",
        "author_kr": "요한 쿠르츠",
        "author_en": "Johann Kurtz",
        "year": 1860,
    },
    {
        "slug": "hurst-history-rationalism",
        "title": "합리주의의 역사 — 계몽주의와 기독교",
        "title_en": "The History of Rationalism",
        "author_kr": "존 F. 허스트",
        "author_en": "John F. Hurst",
        "year": 1865,
    },
    {
        "slug": "doddridge-rise-and-progress",
        "title": "영혼 안에서의 종교의 발생과 성장",
        "title_en": "The Rise and Progress of Religion in the Soul",
        "author_kr": "필립 도드리지",
        "author_en": "Philip Doddridge",
        "year": 1745,
    },
    {
        "slug": "doddridge-family-expositor-v1",
        "title": "가정 성경 강해 제1권: 마태복음~사도행전",
        "title_en": "The Family Expositor Vol.1: NT Paraphrase (Matt–Acts)",
        "author_kr": "필립 도드리지",
        "author_en": "Philip Doddridge",
        "year": 1739,
    },
    {
        "slug": "doddridge-family-expositor-v2",
        "title": "가정 성경 강해 제2권: 로마서~요한계시록",
        "title_en": "The Family Expositor Vol.2: NT Paraphrase (Romans–Revelation)",
        "author_kr": "필립 도드리지",
        "author_en": "Philip Doddridge",
        "year": 1756,
    },
]

if __name__ == "__main__":
    process_all(BOOKS)
