#!/usr/bin/env python3
"""실패한 4권 대체 소스 처리."""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.scripts.phase5_utils import (
    BOOKS_DIR, CACHE_DIR, download, clean, strip_archive, process_book
)

BOOKS = [
    {
        "slug": "perkins-art-prophesying",
        "title": "예언하는 기술",
        "title_en": "The Art of Prophesying",
        "author_kr": "윌리엄 퍼킨스",
        "author_en": "William Perkins",
        "year": 1592,
        "note": "청교도 설교학의 기초. 성경 중심 설교 방법론을 체계화한 최초의 설교학 교과서.",
        "ids": [
            "artofprophesying00perk",
            "artprophesying00perk",
            "0226660079",
        ],
    },
    {
        "slug": "meyer-abraham",
        "title": "아브라함: 믿음의 순종",
        "title_en": "Abraham: Or the Obedience of Faith",
        "author_kr": "F.B. 메이어",
        "author_en": "F. B. Meyer",
        "year": 1897,
        "note": "메이어의 구약 인물 시리즈.",
        "ids": [
            "abrahamorobedien0000meye",
            "lifeofabrahamobe0000meye",
            "abrahamorobedien00fbme",
        ],
    },
    {
        "slug": "meyer-joseph",
        "title": "요셉: 고난이 빚은 인격",
        "title_en": "Joseph: Beloved-Hated-Exalted",
        "author_kr": "F.B. 메이어",
        "author_en": "F. B. Meyer",
        "year": 1897,
        "note": "메이어의 요셉 이야기 명상.",
        "ids": [
            "josephbelovedhat0000meye",
            "josephbelovedhat00meye",
        ],
    },
    {
        "slug": "chambers-still-higher",
        "title": "더 높은 곳을 향하여",
        "title_en": "Still Higher for His Highest",
        "author_kr": "오스왈드 챔버스",
        "author_en": "Oswald Chambers",
        "year": 1927,
        "note": "오스왈드 챔버스의 묵상 모음. 주님은 나의 최고봉 자매편.",
        "ids": [
            "utterancesofgod00cham",
            "mysticallyunion00cham",
            "chambersstillhig0000cham",
        ],
    },
]


def try_archive(slug, ids):
    for ident in ids:
        for ext in ["_djvu.txt", ".txt"]:
            url = f"https://archive.org/download/{ident}/{ident}{ext}"
            cache = CACHE_DIR / f"{slug}_{ident[:18]}{ext}"
            print(f"  시도: {url[:75]}")
            raw = download(url, cache, timeout=90)
            if raw and len(raw) > 3000:
                return raw, f"https://archive.org/details/{ident}"
            time.sleep(0.5)
    return None, None


def main():
    for info in BOOKS:
        slug = info["slug"]
        if (BOOKS_DIR / slug / "metadata.json").exists():
            print(f"[건너뜀] {slug}")
            continue

        print(f"\n[처리] {slug} — {info['title']}")
        raw, src = try_archive(slug, info["ids"])

        if raw:
            info["source_url"] = src
            count = process_book(raw, info, "archive")
            print(f"  ✅ {slug}: {count}챕터")
        else:
            print(f"  ❌ {slug}: 모든 소스 실패")

    print("\n=== 완료 ===")
    print("현재 처리된 책:")
    for info in BOOKS:
        exists = (BOOKS_DIR / info["slug"] / "metadata.json").exists()
        print(f"  {'✅' if exists else '❌'} {info['slug']}")


if __name__ == "__main__":
    main()
