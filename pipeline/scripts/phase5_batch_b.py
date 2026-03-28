#!/usr/bin/env python3
"""Phase 5 Batch B: 카테고리 50-52 (성결운동, 선교자서전, 와츠/뉴턴) — 28권."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.scripts.phase5_utils import process_all

# ─── 카테고리 50: Phoebe Palmer & Holiness Movement (8권) ───

BOOKS_CAT50 = [
    {
        "slug": "palmer-way-of-holiness",
        "title": "성결의 길",
        "title_en": "The Way of Holiness",
        "author_kr": "피비 팔머",
        "author_en": "Phoebe Palmer",
        "year": 1843,
    },
    {
        "slug": "palmer-faith-and-effects",
        "title": "믿음과 그 열매",
        "title_en": "Faith and Its Effects",
        "author_kr": "피비 팔머",
        "author_en": "Phoebe Palmer",
        "year": 1848,
    },
    {
        "slug": "palmer-entire-devotion",
        "title": "하나님께 전적 헌신",
        "title_en": "Entire Devotion to God",
        "author_kr": "피비 팔머",
        "author_en": "Phoebe Palmer",
        "year": 1845,
    },
    {
        "slug": "palmer-promise-father",
        "title": "아버지의 약속",
        "title_en": "The Promise of the Father",
        "author_kr": "피비 팔머",
        "author_en": "Phoebe Palmer",
        "year": 1859,
    },
    {
        "slug": "finney-lectures-revivals",
        "title": "종교 부흥에 관한 강의",
        "title_en": "Lectures on Revivals of Religion",
        "author_kr": "찰스 피니",
        "author_en": "Charles G. Finney",
        "year": 1835,
        "gutenberg_id": 4998,
        "ccel_author": "finney",
        "ccel_work": "revivals",
    },
    {
        "slug": "finney-systematic-theology",
        "title": "핀니의 조직신학",
        "title_en": "Finneys Systematic Theology",
        "author_kr": "찰스 피니",
        "author_en": "Charles G. Finney",
        "year": 1846,
        "ccel_author": "finney",
        "ccel_work": "theology",
    },
    {
        "slug": "finney-lectures-christians",
        "title": "신앙인에게 보내는 강의",
        "title_en": "Lectures to Professing Christians",
        "author_kr": "찰스 피니",
        "author_en": "Charles G. Finney",
        "year": 1837,
    },
    {
        "slug": "finney-memoirs",
        "title": "핀니 자서전",
        "title_en": "Memoirs of Rev Charles G Finney",
        "author_kr": "찰스 피니",
        "author_en": "Charles G. Finney",
        "year": 1876,
        "gutenberg_id": 4097,
    },
]

# ─── 카테고리 51: J.G. Paton & Mission Autobiographies (12권) ───

BOOKS_CAT51 = [
    {
        "slug": "paton-autobiography-v1",
        "title": "페이튼 선교사 자서전 제1권",
        "title_en": "John G Paton Missionary to the New Hebrides Vol 1",
        "author_kr": "존 G. 페이튼",
        "author_en": "John G. Paton",
        "year": 1889,
        "gutenberg_id": 10736,
    },
    {
        "slug": "paton-autobiography-v2",
        "title": "페이튼 선교사 자서전 제2권",
        "title_en": "John G Paton Missionary to the New Hebrides Vol 2",
        "author_kr": "존 G. 페이튼",
        "author_en": "John G. Paton",
        "year": 1889,
        "gutenberg_id": 10737,
    },
    {
        "slug": "carmichael-things-as-they-are",
        "title": "있는 그대로: 남인도 선교 사역",
        "title_en": "Things as They Are Mission Work in Southern India",
        "author_kr": "에이미 카마이클",
        "author_en": "Amy Carmichael",
        "year": 1903,
    },
    {
        "slug": "carmichael-lotus-buds",
        "title": "연꽃 봉오리",
        "title_en": "Lotus Buds",
        "author_kr": "에이미 카마이클",
        "author_en": "Amy Carmichael",
        "year": 1909,
    },
    {
        "slug": "carmichael-gold-cord",
        "title": "황금 줄: 공동체 이야기",
        "title_en": "Gold Cord The Story of a Fellowship",
        "author_kr": "에이미 카마이클",
        "author_en": "Amy Carmichael",
        "year": 1932,
    },
    {
        "slug": "carmichael-edges-of-his-ways",
        "title": "그분의 길 가장자리",
        "title_en": "Edges of His Ways",
        "author_kr": "에이미 카마이클",
        "author_en": "Amy Carmichael",
        "year": 1955,
    },
    {
        "slug": "hyde-praying-hyde",
        "title": "기도하는 하이드",
        "title_en": "Praying Hyde",
        "author_kr": "프랜시스 맥가",
        "author_en": "Francis A. McGaw",
        "year": 1923,
    },
    {
        "slug": "geddie-mission-new-hebrides",
        "title": "뉴헤브리디스 선교 생애",
        "title_en": "Nineteen Years in Polynesia",
        "author_kr": "조지 터너",
        "author_en": "George Turner",
        "year": 1861,
    },
    {
        "slug": "slessor-mary-calabar",
        "title": "칼라바르의 메리 슬레서",
        "title_en": "Mary Slessor of Calabar Pioneer Missionary",
        "author_kr": "W.P. 리빙스턴",
        "author_en": "W. P. Livingstone",
        "year": 1915,
    },
    {
        "slug": "fraser-belts-of-gold",
        "title": "프레이저 선교 기록",
        "title_en": "Behind the Ranges Fraser of Lisuland",
        "author_kr": "J.O. 프레이저",
        "author_en": "J. O. Fraser",
        "year": 1944,
    },
    {
        "slug": "judson-life-letters-full",
        "title": "저드슨의 삶과 편지",
        "title_en": "The Life of Adoniram Judson",
        "author_kr": "에드워드 저드슨",
        "author_en": "Edward Judson",
        "year": 1883,
    },
    {
        "slug": "nevius-planting-churches",
        "title": "선교 교회 설립과 발전",
        "title_en": "The Planting and Development of Missionary Churches",
        "author_kr": "존 네비우스",
        "author_en": "John L. Nevius",
        "year": 1899,
    },
]

# ─── 카테고리 52: Isaac Watts & John Newton (8권) ───

BOOKS_CAT52 = [
    {
        "slug": "watts-hymns-spiritual-songs",
        "title": "찬송과 영적 노래",
        "title_en": "Hymns and Spiritual Songs",
        "author_kr": "이삭 와츠",
        "author_en": "Isaac Watts",
        "year": 1707,
        "gutenberg_id": 6830,
    },
    {
        "slug": "watts-psalms-david",
        "title": "다윗의 시편 모방",
        "title_en": "The Psalms of David Imitated",
        "author_kr": "이삭 와츠",
        "author_en": "Isaac Watts",
        "year": 1719,
    },
    {
        "slug": "watts-divine-songs-children",
        "title": "어린이를 위한 찬송",
        "title_en": "Divine Songs for Children",
        "author_kr": "이삭 와츠",
        "author_en": "Isaac Watts",
        "year": 1715,
        "gutenberg_id": 5958,
    },
    {
        "slug": "watts-improvement-of-mind",
        "title": "마음의 개선",
        "title_en": "The Improvement of the Mind",
        "author_kr": "이삭 와츠",
        "author_en": "Isaac Watts",
        "year": 1741,
        "gutenberg_id": 35135,
    },
    {
        "slug": "newton-cardiphonia",
        "title": "마음의 고백: 서신집",
        "title_en": "Cardiphonia or The Utterance of the Heart",
        "author_kr": "존 뉴턴",
        "author_en": "John Newton",
        "year": 1781,
        "ccel_author": "newton",
        "ccel_work": "cardiphonia",
    },
    {
        "slug": "newton-olney-hymns",
        "title": "올니 찬송가",
        "title_en": "Olney Hymns",
        "author_kr": "뉴턴 & 쿠퍼",
        "author_en": "John Newton",
        "year": 1779,
        "gutenberg_id": 18738,
    },
    {
        "slug": "newton-letters-select",
        "title": "존 뉴턴 서신 선집",
        "title_en": "Letters of John Newton",
        "author_kr": "존 뉴턴",
        "author_en": "John Newton",
        "year": 1780,
        "ccel_author": "newton",
        "ccel_work": "letters",
    },
    {
        "slug": "cowper-poems-select",
        "title": "윌리엄 쿠퍼 시 선집",
        "title_en": "The Poems of William Cowper",
        "author_kr": "윌리엄 쿠퍼",
        "author_en": "William Cowper",
        "year": 1782,
        "gutenberg_id": 3082,
    },
]

BOOKS = BOOKS_CAT50 + BOOKS_CAT51 + BOOKS_CAT52

if __name__ == "__main__":
    process_all(BOOKS, delay=1.5)
