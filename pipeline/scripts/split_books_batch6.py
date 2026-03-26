#!/usr/bin/env python3
"""3권 신규 도서 분할 스크립트.

- On the Incarnation of the Word (Athanasius)
- Of the Mortification of Sin in Believers (John Owen)
- A Serious Call to a Devout and Holy Life (William Law)

사용법:
  python pipeline/scripts/split_books_batch6.py
"""

import re
from pathlib import Path

BOOKS_DIR = Path("pipeline/sources/data/books")

# ─────────────────────────────────────────────
# 공통 유틸리티
# ─────────────────────────────────────────────

def clean_ccel_text(text: str) -> str:
    """CCEL 텍스트 공통 정리: 구분선 제거, 과도한 공백 정리."""
    text = re.sub(r"_{5,}", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def save_chapter(out_dir: Path, num: int, title: str, body: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"ch{num:02d}.txt"
    path.write_text(f"{title}\n\n{body.strip()}\n", encoding="utf-8")
    words = len(body.split())
    print(f"  ch{num:02d}.txt: {title[:60]} ({words} words)")


# ─────────────────────────────────────────────
# 1. On the Incarnation — Athanasius (9챕터)
# ─────────────────────────────────────────────

INCARNATION_TITLES = {
    1: "Creation and the Fall",
    2: "The Divine Dilemma and its Solution in the Incarnation",
    3: "The Divine Dilemma and its Solution — continued",
    4: "The Death of Christ",
    5: "The Resurrection",
    6: "Refutation of the Jews",
    7: "Refutation of the Gentiles",
    8: "Refutation of the Gentiles — continued",
    9: "Conclusion",
}

INCARNATION_METADATA = {
    "slug": "incarnation-word",
    "title": "말씀의 성육신에 관하여",
    "title_original": "On the Incarnation of the Word",
    "author": "아타나시우스 (Athanasius of Alexandria)",
    "author_original": "Athanasius of Alexandria",
    "year": "c. 318",
    "source": "https://www.ccel.org/ccel/a/athanasius/incarnation",
    "license": "public_domain",
    "note": "Early church father's foundational treatise on the Incarnation. 9 chapters.",
}


def split_incarnation():
    print("\n=== On the Incarnation (Athanasius) ===")
    raw = Path("/tmp/incarnation.txt").read_text(encoding="utf-8")
    raw = clean_ccel_text(raw)

    # 챕터 경계 분리
    parts = re.split(r"\nChapter (\d+)\n", raw)
    # parts[0] = header, parts[1]="1", parts[2]=ch1 body, ...

    out_dir = BOOKS_DIR / "incarnation-word"
    chapters_meta = []

    for i in range(1, len(parts), 2):
        num = int(parts[i])
        body_raw = parts[i + 1] if i + 1 < len(parts) else ""

        # 첫 줄 = 소제목 (skip), 실제 본문은 그 다음
        lines = body_raw.strip().split("\n")
        title = INCARNATION_TITLES.get(num, f"Chapter {num}")

        # 소제목 줄 제거 (이미 title 변수로 처리)
        if lines and lines[0].strip() in INCARNATION_TITLES.values():
            lines = lines[1:]
        body = "\n".join(lines).strip()

        save_chapter(out_dir, num, title, body)
        chapters_meta.append({"num": num, "title": title, "file": f"ch{num:02d}.txt"})

    # metadata.json 저장
    import json
    meta = {**INCARNATION_METADATA, "chapters": chapters_meta}
    (out_dir / "metadata.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 2. Mortification of Sin — John Owen (Preface + 14챕터)
# ─────────────────────────────────────────────

OWEN_CHAPTERS = {
    0: "Preface",
    1: "Chapter I — Foundation in Romans 8:13",
    2: "Chapter II — The Necessity of Mortification",
    3: "Chapter III — The Spirit as Sole Author of Mortification",
    4: "Chapter IV — The Usefulness of Mortification",
    5: "Chapter V — What Mortification Is Not",
    6: "Chapter VI — What Mortification Is",
    7: "Chapter VII — General Rules for Mortification",
    8: "Chapter VIII — Universal Sincerity Required",
    9: "Chapter IX — Particular Directions I",
    10: "Chapter X — Particular Directions II",
    11: "Chapter XI — Particular Directions III, IV, V",
    12: "Chapter XII — Particular Directions VI",
    13: "Chapter XIII — Particular Directions VII",
    14: "Chapter XIV — The Great Direction: Act Faith on Christ",
}

OWEN_METADATA = {
    "slug": "mortification-of-sin",
    "title": "죄의 죽임에 관하여",
    "title_original": "Of the Mortification of Sin in Believers",
    "author": "존 오웬 (John Owen)",
    "author_original": "John Owen",
    "year": "1656",
    "source": "https://www.ccel.org/ccel/o/owen/mort",
    "license": "public_domain",
    "note": "Puritan classic on the mortification of indwelling sin. Preface + 14 chapters.",
}


def split_mortification():
    print("\n=== Mortification of Sin (John Owen) ===")
    raw = Path("/tmp/mort_owen.txt").read_text(encoding="utf-8")
    raw = clean_ccel_text(raw)

    out_dir = BOOKS_DIR / "mortification-of-sin"
    chapters_meta = []

    # 챕터 경계 찾기
    # 형식: "                                   Chapter I.\n"
    pattern = re.compile(
        r"\n\s{10,}(Preface\.|Prefatory note\.|Chapter ([IVXLC]+)\.)\n",
        re.IGNORECASE,
    )

    roman_to_int = {
        "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
        "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10,
        "XI": 11, "XII": 12, "XIII": 13, "XIV": 14,
    }

    matches = list(pattern.finditer(raw))
    # Prefatory note와 Preface를 ch01 (Preface)으로 합침
    # Chapter I ~ XIV = ch02 ~ ch15

    def get_body(start_match, end_match):
        start = start_match.end()
        end = end_match.start() if end_match else len(raw)
        return raw[start:end].strip()

    # Preface = Prefatory note + Preface 합치기
    preface_matches = [m for m in matches if "note" in m.group(1).lower() or
                       m.group(1).lower().startswith("preface")]
    chapter_matches = [m for m in matches if "chapter" in m.group(1).lower()]

    # ch01: Preface (Prefatory note + Preface 합산)
    if preface_matches:
        first = preface_matches[0]
        # body = from first preface match to first chapter match
        end = chapter_matches[0] if chapter_matches else None
        body_start = first.end()
        body_end = end.start() if end else len(raw)
        body = raw[body_start:body_end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)
        save_chapter(out_dir, 1, "Preface and Prefatory Note", body)
        chapters_meta.append({"num": 1, "title": "Preface and Prefatory Note", "file": "ch01.txt"})

    # ch02 ~ ch15: Chapter I ~ XIV
    for idx, m in enumerate(chapter_matches):
        roman = m.group(2).upper() if m.group(2) else None
        if not roman:
            continue
        ch_num = roman_to_int.get(roman, idx + 1)
        file_num = ch_num + 1  # ch02 = Chapter I

        next_m = chapter_matches[idx + 1] if idx + 1 < len(chapter_matches) else None
        body = get_body(m, next_m)
        body = re.sub(r"\n{3,}", "\n\n", body)

        title = OWEN_CHAPTERS.get(ch_num, f"Chapter {roman}")
        save_chapter(out_dir, file_num, title, body)
        chapters_meta.append({"num": file_num, "title": title, "file": f"ch{file_num:02d}.txt"})

    # metadata.json
    import json
    meta = {**OWEN_METADATA, "chapters": sorted(chapters_meta, key=lambda x: x["num"])}
    (out_dir / "metadata.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# 3. A Serious Call — William Law (24챕터)
# ─────────────────────────────────────────────

SERIOUS_CALL_TITLES = {
    1:  "Chapter I — The Nature and Extent of Christian Devotion",
    2:  "Chapter II — Why Christians Fall Short of Devotion",
    3:  "Chapter III — The Danger of Not Intending Full Devotion",
    4:  "Chapter IV — We Can Please God Only by Right Intention",
    5:  "Chapter V — The Devotion of Those Free from Labour",
    6:  "Chapter VI — The Great Advantages of a Devout Life",
    7:  "Chapter VII — How Imprudent Use of Wealth Corrupts",
    8:  "Chapter VIII — How Wise Use of Wealth Leads to Devotion",
    9:  "Chapter IX — The Life of Miranda",
    10: "Chapter X — All Orders of People Called to Devotion",
    11: "Chapter XI — How Devotion Fills Life with Peace",
    12: "Chapter XII — The Happiness of a Life Devoted to God",
    13: "Chapter XIII — The Vanity of an Ordinary Life",
    14: "Chapter XIV — On Times and Hours of Prayer",
    15: "Chapter XV — On Chanting and Singing Psalms",
    16: "Chapter XVI — Devotions at Nine o'Clock (the Third Hour)",
    17: "Chapter XVII — The Difficulty of Humility",
    18: "Chapter XVIII — How Education Makes Humility Difficult",
    19: "Chapter XIX — On the Education of Daughters",
    20: "Chapter XX — Devotion at Noon (the Sixth Hour)",
    21: "Chapter XXI — The Necessity and Benefit of Intercession",
    22: "Chapter XXII — Devotion at Three o'Clock (the Ninth Hour)",
    23: "Chapter XXIII — On Evening Prayer and Self-Examination",
    24: "Chapter XXIV — The Excellency of a Devout Spirit",
}

SERIOUS_CALL_METADATA = {
    "slug": "serious-call",
    "title": "경건하고 거룩한 삶으로의 진지한 부름",
    "title_original": "A Serious Call to a Devout and Holy Life",
    "author": "윌리엄 로 (William Law)",
    "author_original": "William Law",
    "year": "1729",
    "source": "https://www.ccel.org/ccel/l/law/serious_call",
    "license": "public_domain",
    "note": "Classic of English devotional literature. 24 chapters on practical holiness.",
}


def split_serious_call():
    print("\n=== A Serious Call (William Law) ===")
    raw = Path("/tmp/serious_call.txt").read_text(encoding="utf-8")
    raw = clean_ccel_text(raw)

    out_dir = BOOKS_DIR / "serious-call"
    chapters_meta = []

    roman_map = {
        "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
        "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10,
        "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15,
        "XVI": 16, "XVII": 17, "XVIII": 18, "XIX": 19, "XX": 20,
        "XXI": 21, "XXII": 22, "XXIII": 23, "XXIV": 24,
    }

    pattern = re.compile(r"\n\s+CHAPTER ([IVXLC]+)\n", re.IGNORECASE)
    matches = list(pattern.finditer(raw))

    for idx, m in enumerate(matches):
        roman = m.group(1).upper()
        ch_num = roman_map.get(roman, idx + 1)

        next_m = matches[idx + 1] if idx + 1 < len(matches) else None
        start = m.end()
        end = next_m.start() if next_m else len(raw)
        body = raw[start:end].strip()
        body = re.sub(r"\n{3,}", "\n\n", body)

        title = SERIOUS_CALL_TITLES.get(ch_num, f"Chapter {roman}")
        save_chapter(out_dir, ch_num, title, body)
        chapters_meta.append({"num": ch_num, "title": title, "file": f"ch{ch_num:02d}.txt"})

    import json
    meta = {**SERIOUS_CALL_METADATA, "chapters": sorted(chapters_meta, key=lambda x: x["num"])}
    (out_dir / "metadata.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_dir / "raw.txt").write_text(raw, encoding="utf-8")
    print(f"  → {len(chapters_meta)}개 챕터 저장 완료")


# ─────────────────────────────────────────────
# main
# ─────────────────────────────────────────────

if __name__ == "__main__":
    split_incarnation()
    split_mortification()
    split_serious_call()
    print("\n✓ 3권 분할 완료!")
