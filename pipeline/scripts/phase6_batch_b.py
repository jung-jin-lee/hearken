#!/usr/bin/env python3
"""Phase 6 배치 B: 카테고리 50-51 (대륙 개혁 교의학, 스코틀랜드 언약도 신학) — 18권."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.scripts.phase5_utils import process_all

BOOKS = [
    # ── 카테고리 50: 대륙 개혁 교의학 (8권) ──
    {
        "slug": "turretin-elenctic-v1",
        "title": "논쟁신학원론 제1권: 신론",
        "title_en": "Institutes of Elenctic Theology Vol.1",
        "author_kr": "프란시스 투레틴",
        "author_en": "Francis Turretin",
        "year": 1679,
    },
    {
        "slug": "turretin-elenctic-v2",
        "title": "논쟁신학원론 제2권: 기독론·구원론",
        "title_en": "Institutes of Elenctic Theology Vol.2",
        "author_kr": "프란시스 투레틴",
        "author_en": "Francis Turretin",
        "year": 1682,
    },
    {
        "slug": "turretin-elenctic-v3",
        "title": "논쟁신학원론 제3권: 성례·종말론",
        "title_en": "Institutes of Elenctic Theology Vol.3",
        "author_kr": "프란시스 투레틴",
        "author_en": "Francis Turretin",
        "year": 1685,
    },
    {
        "slug": "de-moor-commentary-v1",
        "title": "마르크 요강 주석 제1권 (선집)",
        "title_en": "Commentary on Marck's Compendium Vol.1 (sel.)",
        "author_kr": "베르나르디누스 데 무어",
        "author_en": "Bernardinus de Moor",
        "year": 1761,
    },
    {
        "slug": "ridgley-body-divinity-v1",
        "title": "신학총론 제1권",
        "title_en": "A Body of Divinity Vol.1",
        "author_kr": "토마스 리들리",
        "author_en": "Thomas Ridgeley",
        "year": 1731,
    },
    {
        "slug": "ridgley-body-divinity-v2",
        "title": "신학총론 제2권",
        "title_en": "A Body of Divinity Vol.2",
        "author_kr": "토마스 리들리",
        "author_en": "Thomas Ridgeley",
        "year": 1731,
    },
    {
        "slug": "pictet-christian-theology-sel",
        "title": "기독교 신학 (선집)",
        "title_en": "Christian Theology (selections)",
        "author_kr": "베네딕트 피크테",
        "author_en": "Benedict Pictet",
        "year": 1696,
    },
    {
        "slug": "leydekker-medulla-sel",
        "title": "신학의 정수 (선집)",
        "title_en": "Medulla Theologiae (selections)",
        "author_kr": "멜키오르 레이데케르",
        "author_en": "Melchior Leydekker",
        "year": 1688,
    },
    # ── 카테고리 51: 스코틀랜드 언약도 신학 (10권) ──
    {
        "slug": "durham-christ-crucified",
        "title": "그리스도의 십자가 — 이사야 53장 강해",
        "title_en": "Christ Crucified — Isaiah 53 Expounded",
        "author_kr": "제임스 더럼",
        "author_en": "James Durham",
        "year": 1683,
    },
    {
        "slug": "durham-law-unsealed",
        "title": "계명의 봉인을 떼다",
        "title_en": "The Law Unsealed — Ten Commandments",
        "author_kr": "제임스 더럼",
        "author_en": "James Durham",
        "year": 1675,
    },
    {
        "slug": "durham-song-of-solomon",
        "title": "아가서 강해",
        "title_en": "Clavis Cantici — Song of Solomon",
        "author_kr": "제임스 더럼",
        "author_en": "James Durham",
        "year": 1668,
    },
    {
        "slug": "dickson-psalms-commentary",
        "title": "시편 간략 주석",
        "title_en": "A Brief Exposition of the Psalms",
        "author_kr": "데이비드 딕슨",
        "author_en": "David Dickson",
        "year": 1653,
    },
    {
        "slug": "dickson-truths-victory",
        "title": "진리의 오류에 대한 승리",
        "title_en": "Truth's Victory Over Error",
        "author_kr": "데이비드 딕슨",
        "author_en": "David Dickson",
        "year": 1684,
    },
    {
        "slug": "gillespie-aarons-rod",
        "title": "아론의 싹 난 지팡이",
        "title_en": "Aaron's Rod Blossoming",
        "author_kr": "조지 길레스피",
        "author_en": "George Gillespie",
        "year": 1646,
    },
    {
        "slug": "henderson-government-church",
        "title": "스코틀랜드 교회의 치리와 질서",
        "title_en": "The Government and Order of the Church of Scotland",
        "author_kr": "알렉산더 헨더슨",
        "author_en": "Alexander Henderson",
        "year": 1641,
    },
    {
        "slug": "gray-spiritual-warfare",
        "title": "섭리의 신비",
        "title_en": "The Mystery of Providence (Scots ed.)",
        "author_kr": "앤드류 그레이",
        "author_en": "Andrew Gray",
        "year": 1669,
    },
    {
        "slug": "halyburton-memoirs",
        "title": "홀리버턴 회고록",
        "title_en": "Memoirs of Thomas Halyburton",
        "author_kr": "토마스 할리버턴",
        "author_en": "Thomas Halyburton",
        "year": 1715,
    },
    {
        "slug": "willison-sacramental-directory",
        "title": "성례 안내서",
        "title_en": "A Sacramental Directory",
        "author_kr": "존 윌리슨",
        "author_en": "John Willison",
        "year": 1716,
    },
]

if __name__ == "__main__":
    process_all(BOOKS)
