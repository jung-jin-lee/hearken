#!/usr/bin/env python3
"""p3b 매니페스트를 우선순위별 배치로 분할."""

import json
from pathlib import Path

P3B = Path("pipeline/scripts/books_manifest_p3b.json")
manifest = json.loads(P3B.read_text())
slugs_set = {b["slug"] for b in manifest}

# ─── 1순위 (1순위 중 p3a에 없는 것들) ───
priority1_slugs = [
    # 교회사 핵심 (p3a에 없는 것)
    "eusebius-martyrs-palestine",
    "socrates-church-history", "sozomen-church-history",
    "theodoret-church-history", "theodoret-religious-history",
    "sulpicius-life-martin", "sulpicius-sacred-history",
    # 종교개혁사
    "wylie-history-protestantism-v1", "wylie-history-protestantism-v2", "wylie-history-protestantism-v3",
    # Spurgeon New Park Street
    "spurgeon-new-park-v1", "spurgeon-new-park-v2", "spurgeon-new-park-v3",
    "spurgeon-new-park-v4", "spurgeon-new-park-v5", "spurgeon-new-park-v6",
    # Spurgeon Treasury v7
    "spurgeon-treasury-david-v7",
    # Spurgeon 기타
    "spurgeon-feathers-arrows", "spurgeon-according-to-promise", "spurgeon-come-ye-children",
    "spurgeon-christs-words-cross", "spurgeon-twelve-sermons-holy-spirit",
    "spurgeon-twelve-striking-sermons", "spurgeon-soul-winner",
    "spurgeon-eccentric-preachers",
    # JFB 주석 전체
    "jfb-genesis", "jfb-exodus", "jfb-leviticus-numbers", "jfb-deuteronomy-joshua",
    "jfb-judges-ruth-samuel", "jfb-kings-chronicles", "jfb-ezra-esther",
    "jfb-job", "jfb-psalms", "jfb-proverbs-ecclesiastes",
    "jfb-isaiah", "jfb-jeremiah-lamentations", "jfb-ezekiel-daniel", "jfb-minor-prophets",
    "jfb-matthew", "jfb-mark-luke", "jfb-john", "jfb-acts",
    "jfb-romans", "jfb-corinthians", "jfb-galatians-philemon", "jfb-hebrews-revelation",
    # 한국 선교
    "gale-korean-sketches", "gale-vanguard", "gale-korea-in-transition",
    "hulbert-passing-of-korea", "hulbert-history-korea",
    "jones-george-heber-korea", "baird-fifty-years-korea",
    "moffett-samuel-korean-mission", "blair-william-gold-in-korea",
    "mckenzie-korea-tragedy",
    # Morgan 복음서 강해
    "morgan-gospel-matthew", "morgan-gospel-mark", "morgan-gospel-luke",
    "morgan-gospel-john", "morgan-acts-of-apostles",
    # Chrysostom 강해 (p3a에 없는 것)
    "chrysostom-genesis-homilies-sel", "chrysostom-john-homilies-sel",
    # Rutherford 서신집
    "rutherford-letters-v1", "rutherford-letters-v2",
    # Korean revival
    "korean-revival-1907", "ross-john-korea",
]

# ─── 2순위 ───
priority2_slugs = [
    # NPNF/ANF 확장 (p3a에 없는 것)
    "anf-vol1-justin-remains", "anf-vol1-tatian", "anf-vol1-athenagoras",
    "anf-vol2-clement-misc", "anf-vol3-tertullian-v2", "anf-vol3-tertullian-v3",
    "anf-vol4-tertullian-v4", "anf-vol4-minucius-felix", "anf-vol4-commodian",
    "anf-vol5-hippolytus", "anf-vol5-novatian",
    "anf-vol6-gregory-thaumaturgus", "anf-vol6-dionysius-alex",
    "anf-vol6-methodius", "anf-vol6-arnobius",
    "anf-vol7-venantius", "anf-vol7-apostolic-constitutions",
    # NPNF1 (p3a에 없는 것)
    "npnf1-vol1-augustine-confessions-full", "npnf1-vol1-augustine-letters-sel",
    "npnf1-vol2-city-of-god-v2",
    "npnf1-vol10-chrysostom-matthew-v2", "npnf1-vol13-chrysostom-galatians",
    # NPNF2 (p3a에 없는 것)
    "npnf2-vol1-eusebius-extra", "npnf2-vol2-socrates-sozomen-extra",
    "npnf2-vol3-theodoret-extra", "npnf2-vol5-gregory-nyssa-extra2",
    "npnf2-vol7-cyril-gregory-extra", "npnf2-vol8-basil-extra2",
    "npnf2-vol9-john-damascene-extra", "npnf2-vol10-ambrose-extra",
    "npnf2-vol11-sulpicius-cassian-extra", "npnf2-vol12-leo-gregory-great-extra",
    "npnf2-vol14-excursus",
    # Augustine 추가
    "augustine-de-trinitate-full", "augustine-retractions", "augustine-soliloquies",
    "augustine-free-will", "augustine-catechizing-uninstructed", "augustine-continence",
    # Spurgeon MTP
    "spurgeon-sermons-v4", "spurgeon-sermons-v5", "spurgeon-sermons-v6",
    "spurgeon-sermons-v7", "spurgeon-sermons-v8", "spurgeon-sermons-v9",
    "spurgeon-sermons-v10", "spurgeon-sermons-v11", "spurgeon-sermons-v12",
    "spurgeon-sermons-v13", "spurgeon-sermons-v14", "spurgeon-sermons-v15",
    # K&D 구약 주석
    "kd-genesis", "kd-exodus-leviticus", "kd-numbers-deuteronomy",
    "kd-joshua-judges-ruth", "kd-samuel", "kd-kings",
    "kd-chronicles-ezra-nehemiah", "kd-esther-job", "kd-psalms",
    "kd-proverbs-song", "kd-isaiah", "kd-jeremiah-lamentations",
    "kd-ezekiel-daniel", "kd-minor-prophets",
    # Expositor's Bible
    "expositors-bible-genesis", "expositors-bible-exodus", "expositors-bible-psalms",
    "expositors-bible-isaiah", "expositors-bible-john", "expositors-bible-acts",
    "expositors-bible-romans", "expositors-bible-corinthians",
    "expositors-bible-ephesians", "expositors-bible-hebrews", "expositors-bible-revelation",
    # 동방교회 핵심
    "sayings-desert-fathers", "john-climacus-ladder", "evagrius-praktikos",
    "palladius-lausiac-history", "ephrem-syrian-hymns-sel",
    "cyril-jerusalem-catechetical", "way-of-pilgrim",
    "philokalia-sel-v1", "philokalia-sel-v2",
    # 청교도 추가
    "shepard-sound-believer", "shepard-sincere-convert",
    "goodwin-patience-saints", "goodwin-glory-gospel", "goodwin-return-of-prayers",
    "goodwin-works-sel", "brooks-unsearchable-riches", "brooks-apples-gold",
    "watson-doctrine-of-repentance", "watson-godly-mans-picture",
    "boston-covenant-of-grace", "sibbes-fountain-sealed", "sibbes-glorious-freedom",
    "burroughs-gospel-reconciliation", "perkins-art-prophesying",
    "rutherford-lex-rex-sel", "love-christopher-scottish-worthies",
    "owen-biblical-theology-sel",
    "flavel-sacramental-meditations",
    # 여성 신앙인
    "booth-catherine-female-ministry", "carmichael-kohila",
    "guyon-spiritual-progress", "julian-norwich-revelations-full",
    "catherine-siena-letters-sel", "rossetti-face-of-deep",
    "smith-unselfishness-of-god",
]

# 필터: 실제 매니페스트에 있는 것만
p1 = [s for s in priority1_slugs if s in slugs_set]
p2 = [s for s in priority2_slugs if s in slugs_set]
p1_p2 = set(p1 + p2)
p3 = [b["slug"] for b in manifest if b["slug"] not in p1_p2]

print(f"1순위: {len(p1)}권")
print(f"2순위: {len(p2)}권")
print(f"3순위: {len(p3)}권")
print(f"합계: {len(p1) + len(p2) + len(p3)}권")

# 매니페스트를 우선순위별로 분리
slug_to_entry = {b["slug"]: b for b in manifest}

for name, slugs in [("p3b_batch1", p1), ("p3b_batch2", p2), ("p3b_batch3", p3)]:
    entries = [slug_to_entry[s] for s in slugs if s in slug_to_entry]
    out = Path(f"pipeline/scripts/books_manifest_{name}.json")
    out.write_text(json.dumps(entries, ensure_ascii=False, indent=2))
    print(f"  {out}: {len(entries)}권")
