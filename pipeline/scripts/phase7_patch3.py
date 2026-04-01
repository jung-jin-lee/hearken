#!/usr/bin/env python3
"""Phase 7 패치 3: 추가 발견된 archive.org 식별자."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.scripts.phase5_utils import process_all

BOOKS = [
    {
        "slug": "chrysostom-letters-olympias",
        "title": "올림피아스에게 보내는 편지들", "title_en": "Letters to Olympias",
        "author_kr": "요한 크리소스톰", "author_en": "John Chrysostom", "year": 407,
        "direct_url": "https://archive.org/download/aselectlibraryn10augugoog/aselectlibraryn10augugoog_djvu.txt",
    },
    {
        "slug": "schaff-church-history-v5",
        "title": "기독교 교회사 제5권: 중세 초기 기독교",
        "title_en": "History of the Christian Church Vol.5 (Early Medieval)",
        "author_kr": "필립 샤프", "author_en": "Philip Schaff", "year": 1887,
        "direct_url": "https://archive.org/download/historyofchristi05schauoft/historyofchristi05schauoft_djvu.txt",
    },
    {
        "slug": "bullinger-decades-v1",
        "title": "십년설교집 제1-2데케이드", "title_en": "The Decades Vol.1 (Decades I-II)",
        "author_kr": "하인리히 불링거", "author_en": "Heinrich Bullinger", "year": 1549,
        "direct_url": "https://archive.org/download/fiftiegodlielear00bull/fiftiegodlielear00bull_djvu.txt",
    },
    {
        "slug": "alford-year-of-praise",
        "title": "찬양의 해 — 교회력을 위한 찬송과 곡",
        "title_en": "The Year of Praise: Hymns with Tunes for the Church Year",
        "author_kr": "헨리 알포드", "author_en": "Henry Alford", "year": 1867,
        "direct_url": "https://archive.org/download/yearpraisebeing00jonegoog/yearpraisebeing00jonegoog_djvu.txt",
    },
    {
        "slug": "simeon-horae-homileticae-sel",
        "title": "강해 설교 선집 — 시므온의 강해", "title_en": "Horae Homileticae: Expository Discourses (selections)",
        "author_kr": "찰스 시므온", "author_en": "Charles Simeon", "year": 1819,
        "direct_url": "https://archive.org/download/horaehomiletica01sime/horaehomiletica01sime_djvu.txt",
    },
]

if __name__ == "__main__":
    process_all(BOOKS, delay=2.0)
