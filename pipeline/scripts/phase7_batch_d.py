#!/usr/bin/env python3
"""Phase 7 배치 D: 카테고리 72-73 (기도 고전 8 + 아나뱁티스트 원천 문헌 8) — 16권."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.scripts.phase5_utils import process_all

BOOKS = [
    # ── 카테고리 72: 기도 고전 (E.M. Bounds & Prayer Classics) (8권) ──
    {
        "slug": "bounds-power-through-prayer",
        "title": "기도를 통한 능력",
        "title_en": "Power Through Prayer",
        "author_kr": "E.M. 바운즈",
        "author_en": "E.M. Bounds",
        "year": 1912,
    },
    {
        "slug": "bounds-purpose-in-prayer",
        "title": "기도의 목적",
        "title_en": "Purpose in Prayer",
        "author_kr": "E.M. 바운즈",
        "author_en": "E.M. Bounds",
        "year": 1920,
    },
    {
        "slug": "bounds-prayer-and-praying-men",
        "title": "기도와 기도하는 사람들",
        "title_en": "Prayer and Praying Men",
        "author_kr": "E.M. 바운즈",
        "author_en": "E.M. Bounds",
        "year": 1921,
    },
    {
        "slug": "bounds-possibilities-of-prayer",
        "title": "기도의 가능성",
        "title_en": "The Possibilities of Prayer",
        "author_kr": "E.M. 바운즈",
        "author_en": "E.M. Bounds",
        "year": 1923,
    },
    {
        "slug": "bounds-weapon-of-prayer",
        "title": "무기로서의 기도",
        "title_en": "The Weapon of Prayer",
        "author_kr": "E.M. 바운즈",
        "author_en": "E.M. Bounds",
        "year": 1931,
    },
    {
        "slug": "bounds-necessity-of-prayer",
        "title": "기도의 필요성",
        "title_en": "The Necessity of Prayer",
        "author_kr": "E.M. 바운즈",
        "author_en": "E.M. Bounds",
        "year": 1929,
    },
    {
        "slug": "chadwick-path-of-prayer",
        "title": "기도의 길",
        "title_en": "The Path of Prayer",
        "author_kr": "새뮤얼 채드윅",
        "author_en": "Samuel Chadwick",
        "year": 1931,
    },
    {
        "slug": "gordon-quiet-talks-on-prayer",
        "title": "기도에 관한 조용한 이야기",
        "title_en": "Quiet Talks on Prayer",
        "author_kr": "S.D. 고든",
        "author_en": "S.D. Gordon",
        "year": 1904,
    },
    # ── 카테고리 73: 아나뱁티스트 원천 문헌 (8권) ──
    {
        "slug": "menno-simons-works-v1",
        "title": "메노 시몬스 전집 제1권: 기독교 교리의 기초",
        "title_en": "Complete Works of Menno Simons Vol.1: Foundation of Christian Doctrine",
        "author_kr": "메노 시몬스",
        "author_en": "Menno Simons",
        "year": 1541,
    },
    {
        "slug": "menno-simons-works-v2",
        "title": "메노 시몬스 전집 제2권: 참 기독교 신앙",
        "title_en": "Complete Works of Menno Simons Vol.2: True Christian Faith, Reply to False Accusations",
        "author_kr": "메노 시몬스",
        "author_en": "Menno Simons",
        "year": 1541,
    },
    {
        "slug": "hubmaier-writings",
        "title": "발타자르 후브마이어 선집 — 세례·속죄·자유의지",
        "title_en": "Balthasar Hubmaier: Theologian of Anabaptism — Selected Writings",
        "author_kr": "발타자르 후브마이어",
        "author_en": "Balthasar Hubmaier",
        "year": 1525,
    },
    {
        "slug": "schleitheim-confession",
        "title": "슐라이트하임 신앙고백과 역사적 배경",
        "title_en": "The Schleitheim Confession with Historical Context",
        "author_kr": "미하엘 자틀러 (저)",
        "author_en": "Michael Sattler (attr.)",
        "year": 1527,
    },
    {
        "slug": "martyrs-mirror-sel",
        "title": "순교자의 거울 (선집)",
        "title_en": "Martyrs Mirror: Selections (Nonresistant Christians)",
        "author_kr": "틸만 반 브라흐트",
        "author_en": "Thieleman van Braght",
        "year": 1660,
    },
    {
        "slug": "marpeck-writings-sel",
        "title": "필그람 마르펙 저술 선집",
        "title_en": "The Writings of Pilgram Marpeck: Admonition, Response (selections)",
        "author_kr": "필그람 마르펙",
        "author_en": "Pilgram Marpeck",
        "year": 1542,
    },
    {
        "slug": "riedemann-account-religion",
        "title": "우리의 종교·교리·신앙에 관한 설명",
        "title_en": "Account of Our Religion, Doctrine and Faith (Rechenschaft)",
        "author_kr": "페터 리데만",
        "author_en": "Peter Riedemann",
        "year": 1540,
    },
    {
        "slug": "ausbund-hymns-sel",
        "title": "아우스분트: 아나뱁티스트 찬송 (선집)",
        "title_en": "The Ausbund: Selected Anabaptist Hymns (1564 edition selections)",
        "author_kr": "다수 (아나뱁티스트)",
        "author_en": "Various (Anabaptist)",
        "year": 1564,
    },
]

if __name__ == "__main__":
    process_all(BOOKS)
