#!/usr/bin/env python3
"""다중 소스에서 도서 텍스트를 다운로드하는 스크립트.

CCEL HTML, NewAdvent, Sacred Texts, Wikisource 등 HTML 소스를
스크래핑하여 plain text로 변환 후 기존 파이프라인에 연결.
"""

import json, re, os, sys, time
import urllib.request
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.scripts.bulk_processor import process_book, BOOKS_DIR

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Hearken project for visually impaired)"}
CACHE_DIR = Path("/private/tmp/claude-501")


def fetch(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers=UA)
        r = urllib.request.urlopen(req, timeout=timeout)
        return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None


def html_to_text(html):
    """HTML에서 순수 텍스트 추출."""
    t = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    t = re.sub(r'<style[^>]*>.*?</style>', '', t, flags=re.DOTALL)
    t = re.sub(r'<br\s*/?>', '\n', t, flags=re.IGNORECASE)
    t = re.sub(r'<p[^>]*>', '\n\n', t, flags=re.IGNORECASE)
    t = re.sub(r'<h\d[^>]*>', '\n\n', t, flags=re.IGNORECASE)
    t = re.sub(r'<[^>]+>', '', t)
    t = re.sub(r'&nbsp;', ' ', t)
    t = re.sub(r'&amp;', '&', t)
    t = re.sub(r'&lt;', '<', t)
    t = re.sub(r'&gt;', '>', t)
    t = re.sub(r'&#\d+;', '', t)
    t = re.sub(r'\n{4,}', '\n\n\n', t)
    return t.strip()


def fetch_multi_page(urls, delay=0.5):
    """여러 페이지를 연결하여 하나의 텍스트로 합침."""
    texts = []
    for url in urls:
        html = fetch(url)
        if html:
            texts.append(html_to_text(html))
        time.sleep(delay)
    return "\n\n".join(texts) if texts else None


def fetch_newadvent_range(base_id, start, end, delay=0.3):
    """NewAdvent fathers 페이지 범위 다운로드."""
    urls = []
    for i in range(start, end + 1):
        if i == 0:
            urls.append(f"https://www.newadvent.org/fathers/{base_id}.htm")
        else:
            urls.append(f"https://www.newadvent.org/fathers/{base_id}{i:02d}.htm")
    return fetch_multi_page(urls, delay)


# ─── 도서별 소스 매핑 ───
# 형식: slug -> (download_function, info_dict_override)

def get_source_map():
    """각 도서의 다운로드 소스를 정의."""
    sources = {}

    # === 초대교회 & 중세 (NewAdvent) ===
    # Anselm
    sources["anselm-proslogion"] = {
        "type": "newadvent_multi",
        "urls": [f"https://www.newadvent.org/fathers/10011{i:02d}.htm" for i in range(1, 27)],
    }
    sources["anselm-cur-deus-homo"] = {
        "type": "newadvent_multi",
        "urls": [f"https://www.newadvent.org/fathers/10012{i:02d}.htm" for i in range(1, 25)],
    }
    # Bernard - Steps of Humility
    sources["bernard-steps-humility"] = {
        "type": "newadvent_multi",
        "urls": [f"https://www.newadvent.org/fathers/40020{i}.htm" for i in range(1, 8)],
    }
    # Bernard - Song of Songs (homilies)
    sources["bernard-song-of-songs"] = {
        "type": "newadvent_multi",
        "urls": [f"https://www.newadvent.org/fathers/4803{i:02d}.htm" for i in range(1, 21)],
    }
    # Bernard - Grace and Free Will
    sources["bernard-grace-free-will"] = {
        "type": "newadvent_multi",
        "urls": [f"https://www.newadvent.org/fathers/4801{i:02d}.htm" for i in range(1, 15)],
    }
    # Bonaventure - Life of Francis
    sources["bonaventure-life-francis"] = {
        "type": "newadvent_multi",
        "urls": [f"https://www.newadvent.org/fathers/48070{i}.htm" for i in range(1, 16)],
    }
    # Catherine of Genoa
    sources["catherine-genoa-purgation"] = {
        "type": "newadvent_multi",
        "urls": [f"https://www.newadvent.org/fathers/3507{i:02d}.htm" for i in range(1, 20)],
    }

    # === Gutenberg 확인된 것들 ===
    gutenberg_ids = {
        "calvin-golden-booklet": 17845,
        "edwards-original-sin": 57829,
        "edwards-charity-its-fruits": 73337,
        "brainerd-diary": 7960,
        "brainerd-life-diary": 7960,
        "newton-letters": 41877,
        "ryle-old-paths": 36673,
        "ryle-expository-thoughts-v2": 56017,  # Mark
        "ryle-expository-thoughts-v3": 56019,  # Luke vol 1
        "ryle-expository-thoughts-v4": 56020,  # John vol 1
        "meyer-elijah": 73479,
        "mcheyne-memoir": 48816,
        "livingstone-last-journals": 19640,
        "carey-biography": 71929,
        "pink-attributes-god": 65847,
        "edwards-history-redemption": 22098,
        "edwards-narrative-conversions": 72621,
        "edwards-true-virtue": 71970,
        "edwards-end-creation": 71970,
        "owen-holy-spirit": 64841,
        "baxter-call-unconverted": 14660,
        "flavel-mystery-providence": 66502,
        "brooks-precious-remedies": 68158,
        "burroughs-rare-jewel": 67786,
        "sibbes-bruised-reed": 67975,
        "boston-human-nature": 70290,
        "gurnall-christian-armour-v1": 65612,
        "murray-holiest-of-all": 25869,
        "murray-spirit-of-christ": 25866,
        "murray-key-missionary-problem": 67124,
        "meyer-shepherd-psalm": 72485,
        "meyer-moses": 73480,
        "whyte-bunyan-characters": 69050,
        "whyte-bible-characters-v1": 69052,
        "whyte-bible-characters-v2": 69053,
        "maclaren-sermons-v1": 71600,
        "maclaren-sermons-v2": 71601,
        "pink-sermon-mount": 66847,
        "gill-body-divinity": 69990,
        "hodge-commentary-romans": 67500,
        "charnock-existence-attributes-v1": 65300,
        "charnock-existence-attributes-v2": 65301,
        "catherine-booth-aggressive": 13275,
        "phoebe-palmer-way-holiness": 70818,
        "erasmus-enchiridion": 70497,
        "tyndale-obedience": 60003,
        "cranmer-homilies": 62592,
    }
    for slug, eid in gutenberg_ids.items():
        sources[slug] = {
            "type": "gutenberg",
            "url": f"https://www.gutenberg.org/cache/epub/{eid}/pg{eid}.txt",
            "source_type": "gutenberg",
        }

    # === Archive.org 올바른 identifier ===
    archive_ids = {
        "calvin-secret-providence": "secretprovidencofgod00calv",
        "taylor-growth-soul": "hudsontaylorsgro00tayl",
        "taylor-growth-work": "hudsontaylorgrow00tayl",
        "studd-ct": "in.ernet.dli.2015.76250",
        "kierkegaard-works-love": "in.ernet.dli.2015.187384",
        "kierkegaard-training-christianity": "traininginchrist00kieruoft",
        "fletcher-checks": "checkstoantinomi01fletuoft",
        "toplady-writings": "worksofaugustumt00topluoft",
        "morrison-robert": "memoirsoflifean02morrgoog",
        "mackay-uganda": "mackayofuganda00mackuoft",
        "strong-systematic-sel": "systematictheolo01stro",
        "warfield-inspiration": "revelationinspi00warfgoog",
        "dabney-systematic-sel": "systematictheolo00dabn",
        "bengel-gnomon-sel": "gnomonofnewtesta01beng",
        "goodwin-heart-of-christ": "heartofchristinh00good",
        "goodwin-child-of-light": "childoflightwalking00good",
        "burroughs-evil-evils": "evilofevils00burruoft",
        "burroughs-gospel-worship": "gospelworshipor00burruoft",
        "gurnall-christian-armour-v2": "christianincompl02gurn",
        "gurnall-christian-armour-v3": "christianincompl03gurn",
        "sibbes-soul-conflict": "soulsconflictand00sibb",
        "perkins-golden-chain": "goldenechaineor00perk",
        "swinnock-christian-mans-calling": "worksofgeorgesw01swin",
        "mcheyne-daily-readings": "dailybreadbeings00mche",
        "baxter-christian-directory-sel": "christiandirecto01baxt",
        "brooks-heaven-on-earth": "heavenonearth00broo",
        "brooks-mute-christian": "mutechristianun00broo",
        "denney-death-of-christ": "deathofchrist00denn",
        "dale-atonement": "atonement00dale",
        "morgan-crises-christ": "crisesofchrist00morg",
        "morgan-parables-kingdom": "parableskingdom00morg",
        "morgan-great-physician": "greatphysician00morg",
        "pierson-living-oracles": "livingoracles00pier",
        "simpson-holy-spirit": "holyspirit00simp",
        "simpson-four-gospels": "christinfourgosp00simp",
        "liddon-sermons": "someelementsofreli00lidd",
        "parker-peoples-bible-sel": "peoplesbible01park",
        "moule-veni-creator": "venicreator00moul",
        "josephine-butler-life": "personalreminisce00butl",
        "george-macdonald-anthology": "georgemacdonalda00lewi",
        "bonar-hymns-faith": "hymnsfaithhope00bona",
        "kagawa-love-law": "lovethelawoflife00kaga",
        "appenzeller-korea": "henrygerharappen00grif",
        "watchman-nee-spiritual-man-sel": "spiritualman01nee",
        "watchman-nee-normal-christian": "normalchristianl00neew",
        "shedd-dogmatic-sel": "dogmatictheolog01shed",
        "gill-commentary-romans": "expositionofenti06gill",
    }
    for slug, ident in archive_ids.items():
        fn = ident
        # Indian DLI identifiers have different filenames
        if ident.startswith("in.ernet"):
            parts = ident.split(".")
            fn = f"{parts[-1]}"
        sources[slug] = {
            "type": "archive",
            "url": f"https://archive.org/download/{ident}/{ident}_djvu.txt",
            "source_type": "archive",
        }

    # === CCEL HTML 스크래핑 ===
    # Havergal works
    sources["havergal-my-king"] = {
        "type": "ccel_html",
        "url": "https://ccel.org/ccel/h/havergal/myking/myking",
    }

    # Remaining items that are harder to find
    # These will be skipped for now
    skip_list = [
        "eckhart-sermons",  # Very rare in English PD
        "catherine-genoa-dialogue",  # Rare
        "richard-rolle-mending",  # Very rare
        "kempe-book",  # Only modern editions
        "pseudo-dionysius",  # Complex
        "hugh-st-victor-sacraments",  # Very rare
        "peter-lombard-sentences-sel",  # Very rare
        "zwingli-writings",  # Limited availability
        "melanchthon-loci",  # Limited availability
        "tyndale-wicked-mammon",  # Rare
        "toplady-hymns-writings",  # Rare collection
        "wesley-hymns-select",  # Need compilation
        "crosby-fanny-hymns",  # Need compilation
        "missionary-hymns",  # Need compilation
        "fidelia-fiske",  # Rare biography
        "chalmers-james",  # Rare biography
        "hildegard-scivias-sel",  # Complex medieval text
        "birgitta-revelations-sel",  # Very rare
        "mechthild-flowing-light",  # Very rare
    ]

    return sources, skip_list


def download_and_process(slug, source_info, manifest_info):
    """소스에서 다운로드하고 파이프라인에 연결."""
    stype = source_info["type"]
    cache = CACHE_DIR / f"{slug}.txt"

    # 이미 처리됨
    if (BOOKS_DIR / slug / "metadata.json").exists():
        return True

    text = None

    if stype == "gutenberg":
        raw = fetch(source_info["url"])
        if raw and len(raw) > 500:
            cache.write_text(raw, encoding="utf-8")
            text = raw
            manifest_info["source_type"] = "gutenberg"
            manifest_info["url"] = source_info["url"]

    elif stype == "archive":
        raw = fetch(source_info["url"], timeout=30)
        if raw and len(raw) > 500:
            cache.write_text(raw, encoding="utf-8")
            text = raw
            manifest_info["source_type"] = "archive"
            manifest_info["url"] = source_info["url"]

    elif stype == "newadvent_multi":
        parts = []
        for url in source_info["urls"]:
            html = fetch(url)
            if html:
                parts.append(html_to_text(html))
            time.sleep(0.3)
        if parts:
            text = "\n\n---\n\n".join(parts)
            cache.write_text(text, encoding="utf-8")
            manifest_info["source_type"] = "newadvent"
            manifest_info["url"] = source_info["urls"][0]

    elif stype == "ccel_html":
        html = fetch(source_info["url"])
        if html:
            text = html_to_text(html)
            cache.write_text(text, encoding="utf-8")

    if text and len(text) > 200:
        process_book(text, manifest_info)
        return True

    return False


def main():
    manifest = json.loads(Path("pipeline/scripts/books_manifest.json").read_text())
    sources, skip_list = get_source_map()
    content_dir = Path("content/books")

    # manifest를 dict로
    manifest_dict = {x["slug"]: x for x in manifest}

    done, fail, skipped = 0, 0, 0

    for slug, src in sources.items():
        if slug in skip_list:
            skipped += 1
            continue

        # 이미 콘텐츠가 있으면 건너뜀
        if (content_dir / slug).exists() and list((content_dir / slug).glob("*.json")):
            continue

        info = manifest_dict.get(slug)
        if not info:
            continue

        print(f"[{done+fail+1}] {slug} ({src['type']})", end=" ")

        if download_and_process(slug, src, info):
            done += 1
        else:
            print(f"❌ 실패")
            fail += 1

    # manifest 저장 (URL 업데이트 반영)
    updated = [manifest_dict[x["slug"]] if x["slug"] in manifest_dict else x for x in manifest]
    Path("pipeline/scripts/books_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2)
    )

    print(f"\n=== 결과 ===")
    print(f"성공: {done}, 실패: {fail}, 건너뜀: {skipped}")
    print(f"스킵 목록 ({len(skip_list)}권): 희귀 텍스트로 추후 개별 조사 필요")


if __name__ == "__main__":
    main()
