#!/usr/bin/env python3
"""Phase 7 배치 E: 카테고리 74-75 (종교개혁 추가 문헌 10 + 헨리 알포드 신약 주석 6) — 16권."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.scripts.phase5_utils import process_all

BOOKS = [
    # ── 카테고리 74: 종교개혁 추가 문헌 (10권) ──
    {
        "slug": "zwingli-true-false-religion",
        "title": "참 종교와 거짓 종교에 관한 주석",
        "title_en": "Commentary on True and False Religion",
        "author_kr": "울리히 츠빙글리",
        "author_en": "Huldrych Zwingli",
        "year": 1525,
    },
    {
        "slug": "zwingli-selected-works",
        "title": "츠빙글리 선집 (세례론, 섭리론)",
        "title_en": "Selected Works of Zwingli (On Baptism, On Providence)",
        "author_kr": "울리히 츠빙글리",
        "author_en": "Huldrych Zwingli",
        "year": 1525,
    },
    {
        "slug": "bullinger-decades-v1",
        "title": "불링거 데케이드 제1권 (제1-2권)",
        "title_en": "The Decades of Bullinger Vol.1 (First & Second Decades)",
        "author_kr": "하인리히 불링거",
        "author_en": "Heinrich Bullinger",
        "year": 1549,
    },
    {
        "slug": "bullinger-decades-v2",
        "title": "불링거 데케이드 제2권 (제3-5권)",
        "title_en": "The Decades of Bullinger Vol.2 (Third to Fifth Decades)",
        "author_kr": "하인리히 불링거",
        "author_en": "Heinrich Bullinger",
        "year": 1551,
    },
    {
        "slug": "melanchthon-loci-communes",
        "title": "신학 공통 주제",
        "title_en": "Loci Communes (Common Places of Theology)",
        "author_kr": "필립 멜란히톤",
        "author_en": "Philip Melanchthon",
        "year": 1521,
    },
    {
        "slug": "melanchthon-apology-augsburg",
        "title": "아우크스부르크 신앙고백 변증",
        "title_en": "Apology of the Augsburg Confession",
        "author_kr": "필립 멜란히톤",
        "author_en": "Philip Melanchthon",
        "year": 1531,
    },
    {
        "slug": "tyndale-works-selected",
        "title": "틴데일 선집: 서문·기독인의 순종·모어에 대한 답변",
        "title_en": "Works of William Tyndale: Prologues, Obedience of a Christian Man, Answer to More",
        "author_kr": "윌리엄 틴데일",
        "author_en": "William Tyndale",
        "year": 1528,
    },
    {
        "slug": "cranmer-works-selected",
        "title": "크랜머 선집: 성례 교리 변호",
        "title_en": "Works of Thomas Cranmer: Defence of the True Doctrine of the Sacrament (sel.)",
        "author_kr": "토마스 크랜머",
        "author_en": "Thomas Cranmer",
        "year": 1550,
    },
    {
        "slug": "beza-life-of-calvin",
        "title": "칼빈의 생애",
        "title_en": "The Life of John Calvin",
        "author_kr": "테오도르 베자",
        "author_en": "Theodore Beza",
        "year": 1564,
    },
    {
        "slug": "oecolampadius-sermons-sel",
        "title": "외콜람파디우스 설교와 서신 (선집)",
        "title_en": "Sermons and Letters of Oecolampadius (selections)",
        "author_kr": "요하네스 외콜람파디우스",
        "author_en": "Johannes Oecolampadius",
        "year": 1525,
    },
    # ── 카테고리 75: 헨리 알포드 신약 주석 (6권) ──
    {
        "slug": "alford-greek-testament-v1",
        "title": "헬라어 신약 제1권: 사복음서",
        "title_en": "The Greek Testament Vol.1: The Four Gospels",
        "author_kr": "헨리 알포드",
        "author_en": "Henry Alford",
        "year": 1849,
    },
    {
        "slug": "alford-greek-testament-v2",
        "title": "헬라어 신약 제2권: 사도행전·로마서·고린도서",
        "title_en": "The Greek Testament Vol.2: Acts, Romans, Corinthians",
        "author_kr": "헨리 알포드",
        "author_en": "Henry Alford",
        "year": 1852,
    },
    {
        "slug": "alford-greek-testament-v3",
        "title": "헬라어 신약 제3권: 갈라디아서~빌레몬서",
        "title_en": "The Greek Testament Vol.3: Galatians – Philemon",
        "author_kr": "헨리 알포드",
        "author_en": "Henry Alford",
        "year": 1856,
    },
    {
        "slug": "alford-greek-testament-v4",
        "title": "헬라어 신약 제4권: 히브리서~요한계시록",
        "title_en": "The Greek Testament Vol.4: Hebrews – Revelation",
        "author_kr": "헨리 알포드",
        "author_en": "Henry Alford",
        "year": 1861,
    },
    {
        "slug": "alford-how-to-study-nt",
        "title": "신약 연구 방법",
        "title_en": "How to Study the New Testament (3 vols. abridged)",
        "author_kr": "헨리 알포드",
        "author_en": "Henry Alford",
        "year": 1866,
    },
    {
        "slug": "alford-year-of-praise",
        "title": "찬양의 해: 시편 운율 찬송",
        "title_en": "The Year of Praise: A Book of Hymns in the Metres of the Psalter",
        "author_kr": "헨리 알포드",
        "author_en": "Henry Alford",
        "year": 1867,
    },
]

if __name__ == "__main__":
    process_all(BOOKS)
