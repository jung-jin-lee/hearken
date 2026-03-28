#!/usr/bin/env python3
"""Phase 5 재시도: Archive.org 직접 식별자로 실패 도서 재다운로드.

1차 배치에서 실패한 도서 중 Archive.org 검색으로 식별자를 확보한 건들.
"""
import sys, json, re, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.scripts.phase5_utils import (
    BOOKS_DIR, CACHE_DIR, download, clean, extract_gut, strip_archive,
    find_chapters, split_para, process_book,
)

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Hearken/Phase5 visually-impaired project)"}


def archive_dl(identifier, slug):
    """Archive.org에서 직접 다운로드 시도 (여러 패턴)."""
    patterns = [
        f"https://archive.org/download/{identifier}/{identifier}_djvu.txt",
        f"https://archive.org/download/{identifier}/{identifier}.txt",
    ]
    for url in patterns:
        cache = CACHE_DIR / f"{slug}_retry.txt"
        text = download(url, cache)
        if text and len(text) > 1000:
            return text, url
        if cache.exists() and cache.stat().st_size < 1000:
            cache.unlink()
    return None, None


# ─── 실패 도서 + 직접 Archive.org 식별자 매핑 ───

RETRY_BOOKS = [
    # === Adam Clarke Commentary (8권) — 직접 식별자 ===
    {
        "slug": "clarke-commentary-ot-v2",
        "title": "아담 클라크 주석: 역사서",
        "title_en": "Adam Clarkes Commentary Vol 2 Historical Books",
        "author_kr": "아담 클라크", "author_en": "Adam Clarke", "year": "1832",
        "identifiers": ["holybiblecontai184602clar", "holybible02clargoog",
                        "in.ernet.dli.2015.218309"],
    },
    {
        "slug": "clarke-commentary-ot-v3",
        "title": "아담 클라크 주석: 시가서",
        "title_en": "Adam Clarkes Commentary Vol 3 Poetical Books",
        "author_kr": "아담 클라크", "author_en": "Adam Clarke", "year": "1832",
        "identifiers": ["holybiblecontai03clar", "in.ernet.dli.2015.218315"],
    },
    {
        "slug": "clarke-commentary-ot-v4",
        "title": "아담 클라크 주석: 대선지서",
        "title_en": "Adam Clarkes Commentary Vol 4 Major Prophets",
        "author_kr": "아담 클라크", "author_en": "Adam Clarke", "year": "1832",
        "identifiers": ["holybiblecontai04clar"],
    },
    {
        "slug": "clarke-commentary-ot-v5",
        "title": "아담 클라크 주석: 소선지서",
        "title_en": "Adam Clarkes Commentary Vol 5 Minor Prophets",
        "author_kr": "아담 클라크", "author_en": "Adam Clarke", "year": "1832",
        "identifiers": ["holybiblewithac06unkngoog"],
    },
    {
        "slug": "clarke-commentary-nt-v1",
        "title": "아담 클라크 주석: 복음서",
        "title_en": "Adam Clarkes Commentary Gospels",
        "author_kr": "아담 클라크", "author_en": "Adam Clarke", "year": "1832",
        "identifiers": ["commentaryonholy0001clar", "commentaryonholy00clar"],
    },
    {
        "slug": "clarke-commentary-nt-v2",
        "title": "아담 클라크 주석: 사도행전~로마서",
        "title_en": "Adam Clarkes Commentary Acts Romans",
        "author_kr": "아담 클라크", "author_en": "Adam Clarke", "year": "1832",
        "identifiers": ["holybiblecontain0002adam_o2k6"],
    },
    {
        "slug": "clarke-commentary-nt-v3",
        "title": "아담 클라크 주석: 서신서",
        "title_en": "Adam Clarkes Commentary Epistles",
        "author_kr": "아담 클라크", "author_en": "Adam Clarke", "year": "1832",
        "identifiers": ["holybiblecontain0000unse_u6t6"],
    },
    {
        "slug": "clarke-commentary-nt-v4",
        "title": "아담 클라크 주석: 요한계시록",
        "title_en": "Adam Clarkes Commentary Revelation",
        "author_kr": "아담 클라크", "author_en": "Adam Clarke", "year": "1832",
        "identifiers": ["holybiblecontai00clargoog"],
    },

    # === 기타 주요 실패 도서 ===
    {
        "slug": "hyde-praying-hyde",
        "title": "기도하는 하이드",
        "title_en": "Praying Hyde",
        "author_kr": "프랜시스 맥가", "author_en": "Francis A. McGaw", "year": "1923",
        "identifiers": ["PrayingHyde-JohnHydesPrayerLife-ByFrancisMcgaw",
                        "prayinghyde00mcga",
                        "APresentDayChallengeToPrayer-PrayingJohnHyde-WrittenByCaptainE"],
    },
    {
        "slug": "mcheyne-sermons-select",
        "title": "로버트 머리 맥체인 설교 선집",
        "title_en": "Sermons of Robert Murray McCheyne",
        "author_kr": "로버트 머리 맥체인", "author_en": "Robert Murray McCheyne", "year": "1848",
        "identifiers": ["sermonsofrevrobe00mcheiala", "sermonsofrevrobe00mche",
                        "sermonsofrevrobe0000mche"],
    },
    {
        "slug": "bonar-diary-life",
        "title": "앤드류 보나르 일기와 생애",
        "title_en": "Andrew Bonar Diary and Life",
        "author_kr": "마조리 보나르", "author_en": "Marjory Bonar", "year": "1893",
        "identifiers": ["andrewabonarddd00bonagoog"],
    },
    {
        "slug": "strong-exhaustive-concordance",
        "title": "스트롱의 완전 일치",
        "title_en": "Strongs Exhaustive Concordance",
        "author_kr": "제임스 스트롱", "author_en": "James Strong", "year": "1890",
        "identifiers": ["exhaustiveconcordancebibleetc.13.compconc.p1341262.dicthebgrk.jamesstronglld.ny.1890.as"],
    },
    {
        "slug": "thayers-greek-lexicon",
        "title": "세이어 신약 헬라어-영어 사전",
        "title_en": "Thayers Greek-English Lexicon",
        "author_kr": "조셉 세이어", "author_en": "Joseph Henry Thayer", "year": "1889",
        "identifiers": ["greekenglishlexi00grimuoft"],
    },
    {
        "slug": "charnock-existence-attributes",
        "title": "하나님의 존재와 속성",
        "title_en": "Discourses on the Existence and Attributes of God",
        "author_kr": "스티븐 차녹", "author_en": "Stephen Charnock", "year": "1682",
        "identifiers": ["bim_eighteenth-century_discourses-upon-the-exis_charnock-stephen_1797"],
    },
    {
        "slug": "watson-all-things-for-good",
        "title": "만사가 합력하여 선을 이루리라",
        "title_en": "All Things for Good A Divine Cordial",
        "author_kr": "토마스 왓슨", "author_en": "Thomas Watson", "year": "1663",
        "identifiers": ["divinecordialrom00wats", "allthingsforgood00wats"],
    },
    # Korea Mission Field (선집으로 처리)
    {
        "slug": "swallen-mission-field-korea",
        "title": "한국 선교 전장 (선집)",
        "title_en": "The Korea Mission Field",
        "author_kr": "Various", "author_en": "Various missionaries", "year": "1910",
        "identifiers": ["korea-mission-field_1907-02_3_2", "korea-mission-field_1911-07-01_7_7",
                        "korea-mission-field_1907-08_3_8"],
    },
    {
        "slug": "leighton-commentary-1peter",
        "title": "베드로전서 주석",
        "title_en": "Commentary on First Peter by Robert Leighton",
        "author_kr": "로버트 레이턴", "author_en": "Robert Leighton", "year": "1693",
        "identifiers": ["practicalcommen00leigoog", "wholeworksofmost00leig",
                        "selectworksofar00leig"],
    },
]


def process_retry():
    total = len(RETRY_BOOKS)
    success, fail, skip = 0, 0, 0
    failed_list = []

    for i, info in enumerate(RETRY_BOOKS, 1):
        slug = info["slug"]
        print(f"\n[{i}/{total}] {slug} — {info['title']}")

        # 이미 처리 완료?
        meta_path = BOOKS_DIR / slug / "metadata.json"
        if meta_path.exists():
            print(f"  [건너뜀] 이미 존재")
            skip += 1
            continue

        raw = None
        source_url = ""

        for ident in info.get("identifiers", []):
            text, url = archive_dl(ident, slug)
            if text:
                raw = text
                source_url = url
                break
            time.sleep(1)

        if raw and len(raw) > 1000:
            info["source_url"] = source_url
            process_book(raw, info, "archive")
            success += 1
        else:
            print(f"  ❌ {slug}: 모든 식별자 실패")
            fail += 1
            failed_list.append(slug)

        time.sleep(1.5)

    print(f"\n{'='*60}")
    print(f"재시도 결과: 성공 {success}, 실패 {fail}, 건너뜀 {skip}, 전체 {total}")
    if failed_list:
        print(f"여전히 실패:")
        for s in failed_list:
            print(f"  - {s}")


if __name__ == "__main__":
    process_retry()
