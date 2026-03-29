#!/usr/bin/env python3
"""Phase 6 배치 H: 카테고리 64-65 (미등록 개혁주의 설교자들, 부흥과 영성 1차 사료) — 19권."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.scripts.phase5_utils import process_all

BOOKS = [
    # ── 카테고리 64: 미등록 개혁주의 설교자들 (9권) ──
    {
        "slug": "manton-james-commentary",
        "title": "야고보서 주석 (전체)",
        "title_en": "Commentary on James (complete)",
        "author_kr": "토마스 맨턴",
        "author_en": "Thomas Manton",
        "year": 1651,
    },
    {
        "slug": "manton-119th-psalm-v1",
        "title": "시편 119편 강해 제1권",
        "title_en": "An Exposition of Psalm 119 Vol.1",
        "author_kr": "토마스 맨턴",
        "author_en": "Thomas Manton",
        "year": 1681,
    },
    {
        "slug": "manton-119th-psalm-v2",
        "title": "시편 119편 강해 제2권",
        "title_en": "An Exposition of Psalm 119 Vol.2",
        "author_kr": "토마스 맨턴",
        "author_en": "Thomas Manton",
        "year": 1681,
    },
    {
        "slug": "charnock-works-regeneration",
        "title": "전집: 중생론",
        "title_en": "The Works: On Regeneration",
        "author_kr": "스티븐 채녹",
        "author_en": "Stephen Charnock",
        "year": 1840,
    },
    {
        "slug": "goodwin-works-sel-v1",
        "title": "전집 제1권: 칭의 신앙",
        "title_en": "Works of Thomas Goodwin Vol.1: On the Object and Acts of Justifying Faith",
        "author_kr": "토마스 굿윈",
        "author_en": "Thomas Goodwin",
        "year": 1681,
    },
    {
        "slug": "goodwin-works-sel-v2",
        "title": "전집 제2권: 성령의 사역",
        "title_en": "Works of Thomas Goodwin Vol.2: On the Work of the Holy Spirit",
        "author_kr": "토마스 굿윈",
        "author_en": "Thomas Goodwin",
        "year": 1681,
    },
    {
        "slug": "howe-blessedness-righteous",
        "title": "의인의 복됨",
        "title_en": "The Blessedness of the Righteous",
        "author_kr": "존 하우",
        "author_en": "John Howe",
        "year": 1668,
    },
    {
        "slug": "howe-redeemer-tears",
        "title": "잃어버린 영혼들을 향한 구속자의 눈물",
        "title_en": "The Redeemer's Tears Wept over Lost Souls",
        "author_kr": "존 하우",
        "author_en": "John Howe",
        "year": 1684,
    },
    {
        "slug": "swinnock-heaven-and-hell",
        "title": "천국과 지옥의 요약",
        "title_en": "Heaven and Hell Epitomized",
        "author_kr": "조지 스위넉",
        "author_en": "George Swinnock",
        "year": 1670,
    },
    # ── 카테고리 65: 부흥과 영성 1차 사료 (10권) ──
    {
        "slug": "robe-kilsyth-revival",
        "title": "킬시스 부흥의 기록",
        "title_en": "Narratives of the Extraordinary Work of the Spirit of God at Kilsyth",
        "author_kr": "제임스 로브",
        "author_en": "James Robe",
        "year": 1742,
    },
    {
        "slug": "mcculloch-cambuslang-revival",
        "title": "캠버스랭 부흥 간증록 (선집)",
        "title_en": "Cambuslang Revival Testimonies (selections)",
        "author_kr": "윌리엄 맥컬로크",
        "author_en": "William McCulloch",
        "year": 1742,
    },
    {
        "slug": "payson-memoir-letters",
        "title": "에드워드 페이슨 회고록",
        "title_en": "Memoir and Letters of Edward Payson",
        "author_kr": "에이사 커밍스 (편)",
        "author_en": "Asa Cummings (ed.)",
        "year": 1830,
    },
    {
        "slug": "martyn-journals-letters",
        "title": "헨리 마틴 일기와 서신",
        "title_en": "Journals and Letters of Henry Martyn",
        "author_kr": "헨리 마틴",
        "author_en": "Henry Martyn",
        "year": 1837,
    },
    {
        "slug": "judson-memoir",
        "title": "앤 저드슨 전기",
        "title_en": "Memoir of Mrs. Ann H. Judson",
        "author_kr": "제임스 D. 놀스 (편)",
        "author_en": "James D. Knowles (ed.)",
        "year": 1829,
    },
    {
        "slug": "duff-india-missions-sel",
        "title": "인도와 인도 선교 (선집)",
        "title_en": "India and India Missions (selections)",
        "author_kr": "알렉산더 더프",
        "author_en": "Alexander Duff",
        "year": 1839,
    },
    {
        "slug": "paton-autobiography-v1",
        "title": "존 G. 페이튼 자서전 제1권",
        "title_en": "John G. Paton Autobiography Vol.1",
        "author_kr": "존 G. 페이튼",
        "author_en": "John G. Paton",
        "year": 1889,
    },
    {
        "slug": "paton-autobiography-v2",
        "title": "존 G. 페이튼 자서전 제2권",
        "title_en": "John G. Paton Autobiography Vol.2",
        "author_kr": "존 G. 페이튼",
        "author_en": "John G. Paton",
        "year": 1889,
    },
    {
        "slug": "gilmour-among-mongols",
        "title": "몽골인들 사이에서",
        "title_en": "Among the Mongols",
        "author_kr": "제임스 길무어",
        "author_en": "James Gilmour",
        "year": 1882,
    },
    {
        "slug": "mackay-hero-uganda",
        "title": "우간다의 영웅 맥케이",
        "title_en": "Mackay of Uganda (biography)",
        "author_kr": "A.M. 맥케이의 누이",
        "author_en": "A.M. Mackay's Sister",
        "year": 1890,
    },
]

if __name__ == "__main__":
    process_all(BOOKS)
