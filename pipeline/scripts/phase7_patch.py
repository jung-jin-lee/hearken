#!/usr/bin/env python3
"""Phase 7 패치: 자동 검색 실패 도서에 CCEL 경로 / Archive 직접 URL 지정 재처리."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.scripts.phase5_utils import process_all, BOOKS_DIR

# 이미 성공한 도서는 건너뜀 (metadata.json 존재하면 skip)
BOOKS = [
    # ══════════════════════════════════════════════════════════════
    # 카테고리 66: 크리소스톰 — CCEL NPNF 제1시리즈
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "chrysostom-homilies-romans",
        "title": "로마서 강해 (32편)", "title_en": "Homilies on Romans (32 Homilies)",
        "author_kr": "요한 크리소스톰", "author_en": "John Chrysostom", "year": 391,
        "ccel_author": "schaff", "ccel_work": "npnf1-11",
    },
    {
        "slug": "chrysostom-homilies-1cor",
        "title": "고린도전서 강해 (44편)", "title_en": "Homilies on 1 Corinthians (44 Homilies)",
        "author_kr": "요한 크리소스톰", "author_en": "John Chrysostom", "year": 392,
        "ccel_author": "schaff", "ccel_work": "npnf1-12",
    },
    {
        "slug": "chrysostom-homilies-2cor",
        "title": "고린도후서 강해 (30편)", "title_en": "Homilies on 2 Corinthians (30 Homilies)",
        "author_kr": "요한 크리소스톰", "author_en": "John Chrysostom", "year": 393,
        "ccel_author": "schaff", "ccel_work": "npnf1-12",
    },
    {
        "slug": "chrysostom-homilies-galatians-ephesians",
        "title": "갈라디아서·에베소서 강해", "title_en": "Homilies on Galatians & Ephesians",
        "author_kr": "요한 크리소스톰", "author_en": "John Chrysostom", "year": 393,
        "ccel_author": "schaff", "ccel_work": "npnf1-13",
    },
    {
        "slug": "chrysostom-homilies-philippians-col-thess",
        "title": "빌립보서·골로새서·데살로니가서 강해",
        "title_en": "Homilies on Philippians, Colossians & Thessalonians",
        "author_kr": "요한 크리소스톰", "author_en": "John Chrysostom", "year": 394,
        "ccel_author": "schaff", "ccel_work": "npnf1-13",
    },
    {
        "slug": "chrysostom-on-priesthood",
        "title": "사제직에 관한 여섯 권의 책", "title_en": "Six Books on the Priesthood (De Sacerdotio)",
        "author_kr": "요한 크리소스톰", "author_en": "John Chrysostom", "year": 390,
        "ccel_author": "schaff", "ccel_work": "npnf1-09",
    },
    {
        "slug": "chrysostom-homilies-statues",
        "title": "동상에 관한 강해 (21편)", "title_en": "Homilies on the Statues (21 Homilies)",
        "author_kr": "요한 크리소스톰", "author_en": "John Chrysostom", "year": 387,
        "ccel_author": "schaff", "ccel_work": "npnf1-09",
    },
    {
        "slug": "chrysostom-letters-olympias",
        "title": "올림피아스 등에게 보낸 서신집", "title_en": "Letters of Chrysostom to Olympias and Others",
        "author_kr": "요한 크리소스톰", "author_en": "John Chrysostom", "year": 403,
        "ccel_author": "schaff", "ccel_work": "npnf1-09",
    },

    # ══════════════════════════════════════════════════════════════
    # 카테고리 67: 갑바도기아 교부들 — CCEL NPNF 제2시리즈
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "basil-on-holy-spirit",
        "title": "성령론", "title_en": "On the Holy Spirit (De Spiritu Sancto)",
        "author_kr": "가이사랴의 바실리우스", "author_en": "Basil of Caesarea", "year": 375,
        "ccel_author": "schaff", "ccel_work": "npnf2-08",
    },
    {
        "slug": "basil-hexaemeron",
        "title": "창조의 6일 강해 (9편)", "title_en": "Hexaemeron: Nine Homilies on Creation",
        "author_kr": "가이사랴의 바실리우스", "author_en": "Basil of Caesarea", "year": 370,
        "ccel_author": "schaff", "ccel_work": "npnf2-08",
    },
    {
        "slug": "basil-letters-selected",
        "title": "바실리우스 서신집 (선집)", "title_en": "Letters of Basil (selections — doctrinal & pastoral)",
        "author_kr": "가이사랴의 바실리우스", "author_en": "Basil of Caesarea", "year": 370,
        "ccel_author": "schaff", "ccel_work": "npnf2-08",
    },
    {
        "slug": "basil-ascetical-works",
        "title": "수도 규칙서: 장규·단규", "title_en": "The Ascetical Works: Long Rules & Short Rules",
        "author_kr": "가이사랴의 바실리우스", "author_en": "Basil of Caesarea", "year": 358,
        "direct_url": "https://archive.org/download/asceticworksofsa00basi/asceticworksofsa00basi_djvu.txt",
    },
    {
        "slug": "gregory-nyssa-life-of-moses",
        "title": "모세의 생애", "title_en": "The Life of Moses (De Vita Moysis)",
        "author_kr": "닛사의 그레고리우스", "author_en": "Gregory of Nyssa", "year": 390,
        "direct_url": "https://archive.org/download/lifeofmosesgreg00greg/lifeofmosesgreg00greg_djvu.txt",
    },
    {
        "slug": "gregory-nyssa-great-catechism",
        "title": "대교리 강해", "title_en": "The Great Catechetical Oration",
        "author_kr": "닛사의 그레고리우스", "author_en": "Gregory of Nyssa", "year": 385,
        "ccel_author": "schaff", "ccel_work": "npnf2-05",
    },
    {
        "slug": "gregory-nyssa-soul-resurrection",
        "title": "영혼과 부활 (마크리나와의 대화)", "title_en": "On the Soul and the Resurrection (Macrina Dialogue)",
        "author_kr": "닛사의 그레고리우스", "author_en": "Gregory of Nyssa", "year": 380,
        "ccel_author": "schaff", "ccel_work": "npnf2-05",
    },
    {
        "slug": "gregory-nazianzus-theological-orations",
        "title": "신학 강연 5편", "title_en": "The Five Theological Orations (Orations 27–31)",
        "author_kr": "나지안주스의 그레고리우스", "author_en": "Gregory of Nazianzus", "year": 380,
        "ccel_author": "schaff", "ccel_work": "npnf2-07",
    },
    {
        "slug": "gregory-nazianzus-orations-selected",
        "title": "선집 강연 (부활·오순절·바실리우스 추도사)",
        "title_en": "Selected Orations: On Easter, Pentecost, Basil's Eulogy",
        "author_kr": "나지안주스의 그레고리우스", "author_en": "Gregory of Nazianzus", "year": 381,
        "ccel_author": "schaff", "ccel_work": "npnf2-07",
    },
    {
        "slug": "gregory-nazianzus-carmina-sel",
        "title": "시와 자서전적 저술 선집", "title_en": "Carmina: Selected Poems and Autobiographical Writings",
        "author_kr": "나지안주스의 그레고리우스", "author_en": "Gregory of Nazianzus", "year": 382,
        "direct_url": "https://archive.org/download/worksofgregoryof00greg/worksofgregoryof00greg_djvu.txt",
    },

    # ══════════════════════════════════════════════════════════════
    # 카테고리 68: 중세 서방 신비주의
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "bernard-on-loving-god",
        "title": "하나님 사랑에 관하여", "title_en": "On Loving God (De Diligendo Deo)",
        "author_kr": "클레르보의 버나드", "author_en": "Bernard of Clairvaux", "year": 1127,
        "direct_url": "https://archive.org/download/onlovinggodberna00bern/onlovinggodberna00bern_djvu.txt",
    },
    {
        "slug": "bernard-sermons-song-v1",
        "title": "아가서 강해 제1권 (1-43편)", "title_en": "Sermons on the Song of Songs Vol.1 (Sermons 1–43)",
        "author_kr": "클레르보의 버나드", "author_en": "Bernard of Clairvaux", "year": 1135,
        "direct_url": "https://archive.org/download/sermonsonsongofo01bern/sermonsonsongofo01bern_djvu.txt",
    },
    {
        "slug": "bernard-sermons-song-v2",
        "title": "아가서 강해 제2권 (44-86편)", "title_en": "Sermons on the Song of Songs Vol.2 (Sermons 44–86)",
        "author_kr": "클레르보의 버나드", "author_en": "Bernard of Clairvaux", "year": 1148,
        "direct_url": "https://archive.org/download/sermonsonsongofo02bern/sermonsonsongofo02bern_djvu.txt",
    },
    {
        "slug": "bernard-steps-humility-pride",
        "title": "겸손과 교만의 계단", "title_en": "The Steps of Humility and Pride",
        "author_kr": "클레르보의 버나드", "author_en": "Bernard of Clairvaux", "year": 1124,
        "direct_url": "https://archive.org/download/stepsofhumilityb00bern/stepsofhumilityb00bern_djvu.txt",
    },
    {
        "slug": "bonaventure-souls-journey",
        "title": "영혼의 하나님을 향한 여정", "title_en": "The Soul's Journey into God (Itinerarium Mentis in Deum)",
        "author_kr": "보나벤투라", "author_en": "Bonaventure", "year": 1259,
        "direct_url": "https://archive.org/download/soulsjourneyinto00bona/soulsjourneyinto00bona_djvu.txt",
    },
    {
        "slug": "bonaventure-life-of-francis",
        "title": "성 프란체스코의 생애", "title_en": "The Life of St. Francis (Legenda Major)",
        "author_kr": "보나벤투라", "author_en": "Bonaventure", "year": 1263,
        "direct_url": "https://archive.org/download/lifeofstfrancis00bona/lifeofstfrancis00bona_djvu.txt",
    },
    {
        "slug": "hilton-scale-of-perfection-v1",
        "title": "완전의 계단 제1권", "title_en": "The Scale of Perfection Vol.1",
        "author_kr": "월터 힐턴", "author_en": "Walter Hilton", "year": 1390,
        "direct_url": "https://archive.org/download/scaleofperfectio01hilt/scaleofperfectio01hilt_djvu.txt",
    },
    {
        "slug": "hilton-scale-of-perfection-v2",
        "title": "완전의 계단 제2권", "title_en": "The Scale of Perfection Vol.2",
        "author_kr": "월터 힐턴", "author_en": "Walter Hilton", "year": 1395,
        "direct_url": "https://archive.org/download/scaleofperfectio02hilt/scaleofperfectio02hilt_djvu.txt",
    },
    {
        "slug": "rolle-fire-of-love",
        "title": "사랑의 불꽃", "title_en": "The Fire of Love (Incendium Amoris)",
        "author_kr": "리처드 롤", "author_en": "Richard Rolle", "year": 1343,
        "direct_url": "https://archive.org/download/fireofloveincend00roll/fireofloveincend00roll_djvu.txt",
    },

    # ══════════════════════════════════════════════════════════════
    # 카테고리 69: 필립 샤프 교회사 — Archive.org
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "schaff-church-history-v1",
        "title": "기독교 교회사 제1권: 사도 시대",
        "title_en": "History of the Christian Church Vol.1: Apostolic Age",
        "author_kr": "필립 샤프", "author_en": "Philip Schaff", "year": 1858,
        "direct_url": "https://archive.org/download/historyofchristia01scha/historyofchristia01scha_djvu.txt",
    },
    {
        "slug": "schaff-church-history-v2",
        "title": "기독교 교회사 제2권: 니케아 이전 시대",
        "title_en": "History of the Christian Church Vol.2: Ante-Nicene Age",
        "author_kr": "필립 샤프", "author_en": "Philip Schaff", "year": 1867,
        "direct_url": "https://archive.org/download/historyofchristia02scha/historyofchristia02scha_djvu.txt",
    },
    {
        "slug": "schaff-church-history-v3",
        "title": "기독교 교회사 제3권: 니케아·후니케아 시대",
        "title_en": "History of the Christian Church Vol.3: Nicene & Post-Nicene Age",
        "author_kr": "필립 샤프", "author_en": "Philip Schaff", "year": 1867,
        "direct_url": "https://archive.org/download/historyofchristia03scha/historyofchristia03scha_djvu.txt",
    },
    {
        "slug": "schaff-church-history-v4",
        "title": "기독교 교회사 제4권: 중세 전기",
        "title_en": "History of the Christian Church Vol.4: Mediæval Age to 1073",
        "author_kr": "필립 샤프", "author_en": "Philip Schaff", "year": 1867,
        "direct_url": "https://archive.org/download/historyofchristia04scha/historyofchristia04scha_djvu.txt",
    },
    {
        "slug": "schaff-church-history-v5",
        "title": "기독교 교회사 제5권: 중세 중기",
        "title_en": "History of the Christian Church Vol.5: Middle Ages 1049–1294",
        "author_kr": "필립 샤프", "author_en": "Philip Schaff", "year": 1882,
        "direct_url": "https://archive.org/download/historyofchristia05scha/historyofchristia05scha_djvu.txt",
    },
    {
        "slug": "schaff-church-history-v6",
        "title": "기독교 교회사 제6권: 종교개혁 직전",
        "title_en": "History of the Christian Church Vol.6: Middle Ages 1294–1517",
        "author_kr": "필립 샤프", "author_en": "Philip Schaff", "year": 1882,
        "direct_url": "https://archive.org/download/historyofchristia06scha/historyofchristia06scha_djvu.txt",
    },
    {
        "slug": "schaff-church-history-v7",
        "title": "기독교 교회사 제7권: 독일 종교개혁",
        "title_en": "History of the Christian Church Vol.7: German Reformation",
        "author_kr": "필립 샤프", "author_en": "Philip Schaff", "year": 1888,
        "direct_url": "https://archive.org/download/historyofchristia07scha/historyofchristia07scha_djvu.txt",
    },
    {
        "slug": "schaff-church-history-v8",
        "title": "기독교 교회사 제8권: 스위스 종교개혁",
        "title_en": "History of the Christian Church Vol.8: Swiss Reformation",
        "author_kr": "필립 샤프", "author_en": "Philip Schaff", "year": 1892,
        "direct_url": "https://archive.org/download/historyofchristia08scha/historyofchristia08scha_djvu.txt",
    },
    {
        "slug": "schaff-creeds-christendom-v1",
        "title": "기독교의 신조들 제1권: 신조의 역사",
        "title_en": "The Creeds of Christendom Vol.1: History of Creeds",
        "author_kr": "필립 샤프", "author_en": "Philip Schaff", "year": 1877,
        "direct_url": "https://archive.org/download/creedsofchristend01scha/creedsofchristend01scha_djvu.txt",
    },
    {
        "slug": "schaff-creeds-christendom-v2",
        "title": "기독교의 신조들 제2권: 헬라·라틴 신조",
        "title_en": "The Creeds of Christendom Vol.2: Greek & Latin Creeds (text + commentary)",
        "author_kr": "필립 샤프", "author_en": "Philip Schaff", "year": 1877,
        "direct_url": "https://archive.org/download/creedsofchristend02scha/creedsofchristend02scha_djvu.txt",
    },

    # ══════════════════════════════════════════════════════════════
    # 카테고리 70: 성공회 경건 고전
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "andrewes-preces-privatae",
        "title": "앤드류스 개인 기도서", "title_en": "Preces Privatae (Private Prayers)",
        "author_kr": "랜슬롯 앤드류스", "author_en": "Lancelot Andrewes", "year": 1648,
        "direct_url": "https://archive.org/download/precesprivataepr00andr/precesprivataepr00andr_djvu.txt",
    },
    {
        "slug": "hooker-laws-ecclesiastical-v1",
        "title": "교회 정치법 제1권 (제1-4서)",
        "title_en": "Laws of Ecclesiastical Polity Vol.1 (Books I–IV)",
        "author_kr": "리처드 후커", "author_en": "Richard Hooker", "year": 1594,
        "direct_url": "https://archive.org/download/lawsofecclesiast01hook/lawsofecclesiast01hook_djvu.txt",
    },
    {
        "slug": "hooker-laws-ecclesiastical-v2",
        "title": "교회 정치법 제2권 (제5-8서)",
        "title_en": "Laws of Ecclesiastical Polity Vol.2 (Books V–VIII)",
        "author_kr": "리처드 후커", "author_en": "Richard Hooker", "year": 1597,
        "direct_url": "https://archive.org/download/lawsofecclesiast02hook/lawsofecclesiast02hook_djvu.txt",
    },

    # ══════════════════════════════════════════════════════════════
    # 카테고리 71: 초기 감리교 신학
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "wesley-journal-v1",
        "title": "웨슬리 일기 제1권", "title_en": "Journal of John Wesley Vol.1 (1735–1745)",
        "author_kr": "존 웨슬리", "author_en": "John Wesley", "year": 1740,
        "direct_url": "https://archive.org/download/journalofrevjohn01wesl/journalofrevjohn01wesl_djvu.txt",
    },
    {
        "slug": "wesley-journal-v2",
        "title": "웨슬리 일기 제2권", "title_en": "Journal of John Wesley Vol.2 (1745–1760)",
        "author_kr": "존 웨슬리", "author_en": "John Wesley", "year": 1755,
        "direct_url": "https://archive.org/download/journalofrevjohn02wesl/journalofrevjohn02wesl_djvu.txt",
    },
    {
        "slug": "adam-clarke-commentary-nt-v1",
        "title": "클라크 신약 주석 제1권: 마태~사도행전",
        "title_en": "Clarke's Commentary on the New Testament Vol.1: Matt–Acts",
        "author_kr": "아담 클라크", "author_en": "Adam Clarke", "year": 1817,
        "direct_url": "https://archive.org/download/holybiblecontain01clar/holybiblecontain01clar_djvu.txt",
    },
    {
        "slug": "adam-clarke-commentary-nt-v2",
        "title": "클라크 신약 주석 제2권: 로마서~요한계시록",
        "title_en": "Clarke's Commentary on the New Testament Vol.2: Romans–Revelation",
        "author_kr": "아담 클라크", "author_en": "Adam Clarke", "year": 1817,
        "direct_url": "https://archive.org/download/holybiblecontain06clar/holybiblecontain06clar_djvu.txt",
    },
    {
        "slug": "charles-wesley-hymns-sacred-poems",
        "title": "찬송과 거룩한 시 전집", "title_en": "Hymns and Sacred Poems (Collected Edition)",
        "author_kr": "찰스 웨슬리", "author_en": "Charles Wesley", "year": 1740,
        "direct_url": "https://archive.org/download/hymnsandsacredpo00wesl/hymnsandsacredpo00wesl_djvu.txt",
    },
    {
        "slug": "fletcher-checks-antinomianism-v1",
        "title": "무율법주의 반박 제1권", "title_en": "Checks to Antinomianism Vol.1",
        "author_kr": "존 플레처", "author_en": "John Fletcher", "year": 1771,
        "direct_url": "https://archive.org/download/checkstoantinoml01flet/checkstoantinoml01flet_djvu.txt",
    },
    {
        "slug": "richard-watson-institutes-v1",
        "title": "감리교 신학 총론 제1권", "title_en": "Theological Institutes Vol.1",
        "author_kr": "리처드 왓슨", "author_en": "Richard Watson", "year": 1823,
        "direct_url": "https://archive.org/download/theologicalinsti01wats/theologicalinsti01wats_djvu.txt",
    },
    {
        "slug": "richard-watson-institutes-v2",
        "title": "감리교 신학 총론 제2권", "title_en": "Theological Institutes Vol.2",
        "author_kr": "리처드 왓슨", "author_en": "Richard Watson", "year": 1823,
        "direct_url": "https://archive.org/download/theologicalinsti02wats/theologicalinsti02wats_djvu.txt",
    },

    # ══════════════════════════════════════════════════════════════
    # 카테고리 72: 기도 고전 (E.M. Bounds)
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "bounds-power-through-prayer",
        "title": "기도를 통한 능력", "title_en": "Power Through Prayer",
        "author_kr": "E.M. 바운즈", "author_en": "E.M. Bounds", "year": 1912,
        "gutenberg_id": 4550,
    },
    {
        "slug": "bounds-purpose-in-prayer",
        "title": "기도의 목적", "title_en": "Purpose in Prayer",
        "author_kr": "E.M. 바운즈", "author_en": "E.M. Bounds", "year": 1920,
        "gutenberg_id": 4547,
    },
    {
        "slug": "bounds-prayer-and-praying-men",
        "title": "기도와 기도하는 사람들", "title_en": "Prayer and Praying Men",
        "author_kr": "E.M. 바운즈", "author_en": "E.M. Bounds", "year": 1921,
        "gutenberg_id": 13473,
    },
    {
        "slug": "bounds-possibilities-of-prayer",
        "title": "기도의 가능성", "title_en": "The Possibilities of Prayer",
        "author_kr": "E.M. 바운즈", "author_en": "E.M. Bounds", "year": 1923,
        "gutenberg_id": 4549,
    },
    {
        "slug": "bounds-weapon-of-prayer",
        "title": "무기로서의 기도", "title_en": "The Weapon of Prayer",
        "author_kr": "E.M. 바운즈", "author_en": "E.M. Bounds", "year": 1931,
        "gutenberg_id": 4548,
    },
    {
        "slug": "bounds-necessity-of-prayer",
        "title": "기도의 필요성", "title_en": "The Necessity of Prayer",
        "author_kr": "E.M. 바운즈", "author_en": "E.M. Bounds", "year": 1929,
        "gutenberg_id": 4546,
    },
    {
        "slug": "chadwick-path-of-prayer",
        "title": "기도의 길", "title_en": "The Path of Prayer",
        "author_kr": "새뮤얼 채드윅", "author_en": "Samuel Chadwick", "year": 1931,
        "direct_url": "https://archive.org/download/pathofprayersamue00chad/pathofprayersamue00chad_djvu.txt",
    },

    # ══════════════════════════════════════════════════════════════
    # 카테고리 73: 아나뱁티스트 원천 문헌
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "menno-simons-works-v1",
        "title": "메노 시몬스 전집 제1권: 기독교 교리의 기초",
        "title_en": "Complete Works of Menno Simons Vol.1: Foundation of Christian Doctrine",
        "author_kr": "메노 시몬스", "author_en": "Menno Simons", "year": 1541,
        "direct_url": "https://archive.org/download/completeworksofm01simo/completeworksofm01simo_djvu.txt",
    },
    {
        "slug": "menno-simons-works-v2",
        "title": "메노 시몬스 전집 제2권: 참 기독교 신앙",
        "title_en": "Complete Works of Menno Simons Vol.2: True Christian Faith, Reply to False Accusations",
        "author_kr": "메노 시몬스", "author_en": "Menno Simons", "year": 1541,
        "direct_url": "https://archive.org/download/completeworksofm02simo/completeworksofm02simo_djvu.txt",
    },
    {
        "slug": "hubmaier-writings",
        "title": "발타자르 후브마이어 선집 — 세례·속죄·자유의지",
        "title_en": "Balthasar Hubmaier: Theologian of Anabaptism — Selected Writings",
        "author_kr": "발타자르 후브마이어", "author_en": "Balthasar Hubmaier", "year": 1525,
        "direct_url": "https://archive.org/download/balthasarhubmaier00hubm/balthasarhubmaier00hubm_djvu.txt",
    },
    {
        "slug": "schleitheim-confession",
        "title": "슐라이트하임 신앙고백과 역사적 배경",
        "title_en": "The Schleitheim Confession with Historical Context",
        "author_kr": "미하엘 자틀러 (저)", "author_en": "Michael Sattler (attr.)", "year": 1527,
        "direct_url": "https://archive.org/download/schleitheimconfe00satt/schleitheimconfe00satt_djvu.txt",
    },
    {
        "slug": "martyrs-mirror-sel",
        "title": "순교자의 거울 (선집)", "title_en": "Martyrs Mirror: Selections (Nonresistant Christians)",
        "author_kr": "틸만 반 브라흐트", "author_en": "Thieleman van Braght", "year": 1660,
        "direct_url": "https://archive.org/download/martyrsmirrorsto00brag/martyrsmirrorsto00brag_djvu.txt",
    },
    {
        "slug": "marpeck-writings-sel",
        "title": "필그람 마르펙 저술 선집",
        "title_en": "The Writings of Pilgram Marpeck: Admonition, Response (selections)",
        "author_kr": "필그람 마르펙", "author_en": "Pilgram Marpeck", "year": 1542,
        "direct_url": "https://archive.org/download/writingsofpilgra00marp/writingsofpilgra00marp_djvu.txt",
    },
    {
        "slug": "riedemann-account-religion",
        "title": "우리의 종교·교리·신앙에 관한 설명",
        "title_en": "Account of Our Religion, Doctrine and Faith (Rechenschaft)",
        "author_kr": "페터 리데만", "author_en": "Peter Riedemann", "year": 1540,
        "direct_url": "https://archive.org/download/accountofourrel00ried/accountofourrel00ried_djvu.txt",
    },
    {
        "slug": "ausbund-hymns-sel",
        "title": "아우스분트: 아나뱁티스트 찬송 (선집)",
        "title_en": "The Ausbund: Selected Anabaptist Hymns (1564 edition selections)",
        "author_kr": "다수 (아나뱁티스트)", "author_en": "Various (Anabaptist)", "year": 1564,
        "direct_url": "https://archive.org/download/ausbunddasisteti00unkn/ausbunddasisteti00unkn_djvu.txt",
    },

    # ══════════════════════════════════════════════════════════════
    # 카테고리 74: 종교개혁 추가 문헌
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "zwingli-true-false-religion",
        "title": "참 종교와 거짓 종교에 관한 주석",
        "title_en": "Commentary on True and False Religion",
        "author_kr": "울리히 츠빙글리", "author_en": "Huldrych Zwingli", "year": 1525,
        "direct_url": "https://archive.org/download/commentaryontrue00zwin/commentaryontrue00zwin_djvu.txt",
    },
    {
        "slug": "zwingli-selected-works",
        "title": "츠빙글리 선집 (세례론, 섭리론)",
        "title_en": "Selected Works of Zwingli (On Baptism, On Providence)",
        "author_kr": "울리히 츠빙글리", "author_en": "Huldrych Zwingli", "year": 1525,
        "direct_url": "https://archive.org/download/selectedworksofu00zwin/selectedworksofu00zwin_djvu.txt",
    },
    {
        "slug": "bullinger-decades-v1",
        "title": "불링거 데케이드 제1권 (제1-2권)",
        "title_en": "The Decades of Bullinger Vol.1 (First & Second Decades)",
        "author_kr": "하인리히 불링거", "author_en": "Heinrich Bullinger", "year": 1549,
        "direct_url": "https://archive.org/download/decadesofheinric01bull/decadesofheinric01bull_djvu.txt",
    },
    {
        "slug": "bullinger-decades-v2",
        "title": "불링거 데케이드 제2권 (제3-5권)",
        "title_en": "The Decades of Bullinger Vol.2 (Third to Fifth Decades)",
        "author_kr": "하인리히 불링거", "author_en": "Heinrich Bullinger", "year": 1551,
        "direct_url": "https://archive.org/download/decadesofheinric02bull/decadesofheinric02bull_djvu.txt",
    },
    {
        "slug": "melanchthon-loci-communes",
        "title": "신학 공통 주제", "title_en": "Loci Communes (Common Places of Theology)",
        "author_kr": "필립 멜란히톤", "author_en": "Philip Melanchthon", "year": 1521,
        "direct_url": "https://archive.org/download/locicommunes00mela/locicommunes00mela_djvu.txt",
    },
    {
        "slug": "melanchthon-apology-augsburg",
        "title": "아우크스부르크 신앙고백 변증",
        "title_en": "Apology of the Augsburg Confession",
        "author_kr": "필립 멜란히톤", "author_en": "Philip Melanchthon", "year": 1531,
        "direct_url": "https://archive.org/download/apologyofaugsbur00mela/apologyofaugsbur00mela_djvu.txt",
    },
    {
        "slug": "tyndale-works-selected",
        "title": "틴데일 선집: 서문·기독인의 순종·모어에 대한 답변",
        "title_en": "Works of William Tyndale: Prologues, Obedience of a Christian Man, Answer to More",
        "author_kr": "윌리엄 틴데일", "author_en": "William Tyndale", "year": 1528,
        "direct_url": "https://archive.org/download/worksofwilliamty01tynd/worksofwilliamty01tynd_djvu.txt",
    },
    {
        "slug": "cranmer-works-selected",
        "title": "크랜머 선집: 성례 교리 변호",
        "title_en": "Works of Thomas Cranmer: Defence of the True Doctrine of the Sacrament (sel.)",
        "author_kr": "토마스 크랜머", "author_en": "Thomas Cranmer", "year": 1550,
        "direct_url": "https://archive.org/download/worksofthomasc01cran/worksofthomasc01cran_djvu.txt",
    },
    {
        "slug": "oecolampadius-sermons-sel",
        "title": "외콜람파디우스 설교와 서신 (선집)",
        "title_en": "Sermons and Letters of Oecolampadius (selections)",
        "author_kr": "요하네스 외콜람파디우스", "author_en": "Johannes Oecolampadius", "year": 1525,
        "direct_url": "https://archive.org/download/johannesoecolamp00oeco/johannesoecolamp00oeco_djvu.txt",
    },

    # ══════════════════════════════════════════════════════════════
    # 카테고리 75: 헨리 알포드 신약 주석
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "alford-greek-testament-v1",
        "title": "헬라어 신약 제1권: 사복음서",
        "title_en": "The Greek Testament Vol.1: The Four Gospels",
        "author_kr": "헨리 알포드", "author_en": "Henry Alford", "year": 1849,
        "direct_url": "https://archive.org/download/greektestamentw01alfo/greektestamentw01alfo_djvu.txt",
    },
    {
        "slug": "alford-greek-testament-v2",
        "title": "헬라어 신약 제2권: 사도행전·로마서·고린도서",
        "title_en": "The Greek Testament Vol.2: Acts, Romans, Corinthians",
        "author_kr": "헨리 알포드", "author_en": "Henry Alford", "year": 1852,
        "direct_url": "https://archive.org/download/greektestamentw02alfo/greektestamentw02alfo_djvu.txt",
    },
    {
        "slug": "alford-greek-testament-v3",
        "title": "헬라어 신약 제3권: 갈라디아서~빌레몬서",
        "title_en": "The Greek Testament Vol.3: Galatians – Philemon",
        "author_kr": "헨리 알포드", "author_en": "Henry Alford", "year": 1856,
        "direct_url": "https://archive.org/download/greektestamentw03alfo/greektestamentw03alfo_djvu.txt",
    },
    {
        "slug": "alford-greek-testament-v4",
        "title": "헬라어 신약 제4권: 히브리서~요한계시록",
        "title_en": "The Greek Testament Vol.4: Hebrews – Revelation",
        "author_kr": "헨리 알포드", "author_en": "Henry Alford", "year": 1861,
        "direct_url": "https://archive.org/download/greektestamentw04alfo/greektestamentw04alfo_djvu.txt",
    },
    {
        "slug": "alford-year-of-praise",
        "title": "찬양의 해: 시편 운율 찬송",
        "title_en": "The Year of Praise: A Book of Hymns in the Metres of the Psalter",
        "author_kr": "헨리 알포드", "author_en": "Henry Alford", "year": 1867,
        "direct_url": "https://archive.org/download/yearofpraisebook00alfo/yearofpraisebook00alfo_djvu.txt",
    },

    # ══════════════════════════════════════════════════════════════
    # 카테고리 76: 19세기 강해 설교자들
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "brooks-sermons-selected",
        "title": "필립스 브룩스 설교 선집", "title_en": "Sermons of Phillips Brooks (Selected Vol.1)",
        "author_kr": "필립스 브룩스", "author_en": "Phillips Brooks", "year": 1878,
        "direct_url": "https://archive.org/download/sermons00broo/sermons00broo_djvu.txt",
    },
    {
        "slug": "brooks-lectures-on-preaching",
        "title": "설교학 강의 (예일 강의)", "title_en": "Lectures on Preaching (Yale Lectures on Preaching)",
        "author_kr": "필립스 브룩스", "author_en": "Phillips Brooks", "year": 1877,
        "direct_url": "https://archive.org/download/lecturesonpreac00broogoog/lecturesonpreac00broogoog_djvu.txt",
    },
    {
        "slug": "maclaren-expositions-ot",
        "title": "성경 강해: 구약 (창세기~시편 선집)",
        "title_en": "Expositions of Holy Scripture: OT (Genesis – Psalms selections)",
        "author_kr": "알렉산더 맥라렌", "author_en": "Alexander Maclaren", "year": 1890,
        "direct_url": "https://archive.org/download/expositionsofhol01macl/expositionsofhol01macl_djvu.txt",
    },
    {
        "slug": "maclaren-expositions-nt-v1",
        "title": "성경 강해: 신약 제1권 (마태복음~사도행전)",
        "title_en": "Expositions of Holy Scripture: NT Vol.1 (Matthew – Acts)",
        "author_kr": "알렉산더 맥라렌", "author_en": "Alexander Maclaren", "year": 1900,
        "direct_url": "https://archive.org/download/expositionsofhol10macl/expositionsofhol10macl_djvu.txt",
    },
    {
        "slug": "maclaren-expositions-nt-v2",
        "title": "성경 강해: 신약 제2권 (로마서~요한계시록)",
        "title_en": "Expositions of Holy Scripture: NT Vol.2 (Romans – Revelation)",
        "author_kr": "알렉산더 맥라렌", "author_en": "Alexander Maclaren", "year": 1908,
        "direct_url": "https://archive.org/download/expositionsofhol16macl/expositionsofhol16macl_djvu.txt",
    },
    {
        "slug": "simeon-horae-homileticae-sel",
        "title": "강해 설교 선집 — 시므온의 강해",
        "title_en": "Horae Homileticae: Expository Discourses (selections)",
        "author_kr": "찰스 시므온", "author_en": "Charles Simeon", "year": 1819,
        "direct_url": "https://archive.org/download/horaehomiletica01sime/horaehomiletica01sime_djvu.txt",
    },
    {
        "slug": "dale-christian-doctrine",
        "title": "회중교회 원리 편람", "title_en": "Manual of Congregational Principles",
        "author_kr": "R.W. 데일", "author_en": "R.W. Dale", "year": 1884,
        "direct_url": "https://archive.org/download/manualofcongrega00dale/manualofcongrega00dale_djvu.txt",
    },
    {
        "slug": "cadman-ambassadors-for-god",
        "title": "하나님의 대사들", "title_en": "Ambassadors for God",
        "author_kr": "S. 파크스 캐드먼", "author_en": "S. Parkes Cadman", "year": 1920,
        "direct_url": "https://archive.org/download/ambassadorsforge00cadm/ambassadorsforge00cadm_djvu.txt",
    },

    # ══════════════════════════════════════════════════════════════
    # 카테고리 77: 기독교 순교·박해 역사
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "foxe-acts-monuments-v1",
        "title": "순교자 열전 제1권: 초대교회~위클리프",
        "title_en": "Foxe's Acts and Monuments Vol.1: Early Church to Wycliffe",
        "author_kr": "존 폭스", "author_en": "John Foxe", "year": 1563,
        "direct_url": "https://archive.org/download/actsandmonuments01foxe/actsandmonuments01foxe_djvu.txt",
    },
    {
        "slug": "foxe-acts-monuments-v2",
        "title": "순교자 열전 제2권: 롤라드파~메리 여왕 이전",
        "title_en": "Foxe's Acts and Monuments Vol.2: Lollards to Pre-Marian England",
        "author_kr": "존 폭스", "author_en": "John Foxe", "year": 1563,
        "direct_url": "https://archive.org/download/actsandmonuments02foxe/actsandmonuments02foxe_djvu.txt",
    },
    {
        "slug": "foxe-acts-monuments-v3",
        "title": "순교자 열전 제3권: 메리 여왕 시대 순교자들",
        "title_en": "Foxe's Acts and Monuments Vol.3: Marian Martyrs 1555–1558",
        "author_kr": "존 폭스", "author_en": "John Foxe", "year": 1563,
        "direct_url": "https://archive.org/download/actsandmonuments03foxe/actsandmonuments03foxe_djvu.txt",
    },
    {
        "slug": "crespin-martyrs-france",
        "title": "프랑스 순교자들 (선집)", "title_en": "Book of Martyrs of France (Livre des Martyrs, selections)",
        "author_kr": "장 크레스팽", "author_en": "Jean Crespin", "year": 1554,
        "direct_url": "https://archive.org/download/bookofmartyrsfra00cres/bookofmartyrsfra00cres_djvu.txt",
    },
    {
        "slug": "vermigli-common-places-sel",
        "title": "피터 마르티르 베르밀리 공통 주제 (선집)",
        "title_en": "Common Places of Peter Martyr Vermigli (selections)",
        "author_kr": "피터 마르티르 베르밀리", "author_en": "Peter Martyr Vermigli", "year": 1576,
        "direct_url": "https://archive.org/download/commonplacesofpe00verm/commonplacesofpe00verm_djvu.txt",
    },
    {
        "slug": "gillies-historical-collections",
        "title": "부흥 기록 역사 모음", "title_en": "Historical Collections of Accounts of Revival",
        "author_kr": "존 길리스", "author_en": "John Gillies", "year": 1754,
        "direct_url": "https://archive.org/download/historicalcollec00gill/historicalcollec00gill_djvu.txt",
    },
    {
        "slug": "brown-john-self-interpreting-bible",
        "title": "자기 해석 성경 — 순교자 주석 포함",
        "title_en": "The Self-Interpreting Bible with Notes on Martyrs",
        "author_kr": "존 브라운", "author_en": "John Brown", "year": 1778,
        "direct_url": "https://archive.org/download/selfinterpretingb01brow/selfinterpretingb01brow_djvu.txt",
    },

    # ══════════════════════════════════════════════════════════════
    # 카테고리 78: 신앙과 과학 변증학
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "hodge-what-is-darwinism",
        "title": "다윈주의란 무엇인가?", "title_en": "What is Darwinism?",
        "author_kr": "찰스 호지", "author_en": "Charles Hodge", "year": 1874,
        "gutenberg_id": 9155,
    },
    {
        "slug": "rawlinson-historical-evidence",
        "title": "홍수의 역사적 증거",
        "title_en": "Historical Evidence of the Mosaic Account of the Deluge",
        "author_kr": "조지 롤린슨", "author_en": "George Rawlinson", "year": 1876,
        "direct_url": "https://archive.org/download/historicalevidenc00rawl/historicalevidenc00rawl_djvu.txt",
    },

    # ══════════════════════════════════════════════════════════════
    # 카테고리 79: 선교 역사 1차 사료
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "zwemer-islam-challenge-to-faith",
        "title": "이슬람, 신앙에 대한 도전", "title_en": "Islam, a Challenge to Faith",
        "author_kr": "새뮤얼 즈워머", "author_en": "Samuel M. Zwemer", "year": 1907,
        "direct_url": "https://archive.org/download/islamchallengetof00zwem/islamchallengetof00zwem_djvu.txt",
    },
    {
        "slug": "zwemer-moslem-world",
        "title": "무슬림 세계", "title_en": "The Moslem World (periodical selections)",
        "author_kr": "새뮤얼 즈워머", "author_en": "Samuel M. Zwemer", "year": 1920,
        "direct_url": "https://archive.org/download/moslemworld00zwem/moslemworld00zwem_djvu.txt",
    },
    {
        "slug": "marsden-observations-nz",
        "title": "뉴질랜드 기독교 소개 관찰 기록",
        "title_en": "Observations on the Introduction of Christianity in New Zealand",
        "author_kr": "새뮤얼 마스든", "author_en": "Samuel Marsden", "year": 1838,
        "direct_url": "https://archive.org/download/observationsonin00mars/observationsonin00mars_djvu.txt",
    },
    {
        "slug": "schwartz-life-letters",
        "title": "슈바르츠 선교사 생애와 서신",
        "title_en": "Life and Letters of Christian Friedrich Schwartz of Tanjore",
        "author_kr": "H.N. 피어슨", "author_en": "H.N. Pearson", "year": 1826,
        "direct_url": "https://archive.org/download/memorirsoftheli00schwgoog/memorirsoftheli00schwgoog_djvu.txt",
    },
    {
        "slug": "carey-letters-memoir",
        "title": "윌리엄 캐리 서신집과 전기",
        "title_en": "Letters of William Carey with Biographical Notes",
        "author_kr": "유스테이스 캐리", "author_en": "Eustace Carey", "year": 1836,
        "direct_url": "https://archive.org/download/memoirrevwilliam00care/memoirrevwilliam00care_djvu.txt",
    },

    # ══════════════════════════════════════════════════════════════
    # 카테고리 80: 교회사 보조 명저
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "mosheim-ecclesiastical-history-v1",
        "title": "교회사 총론 제1권: 고대·중세",
        "title_en": "Institutes of Ecclesiastical History Vol.1 (Ancient & Medieval)",
        "author_kr": "요한 로렌츠 모스하임", "author_en": "J.L. von Mosheim", "year": 1755,
        "direct_url": "https://archive.org/download/institutesofeccl01mosh/institutesofeccl01mosh_djvu.txt",
    },
    {
        "slug": "mosheim-ecclesiastical-history-v2",
        "title": "교회사 총론 제2권: 근대",
        "title_en": "Institutes of Ecclesiastical History Vol.2 (Modern)",
        "author_kr": "요한 로렌츠 모스하임", "author_en": "J.L. von Mosheim", "year": 1755,
        "direct_url": "https://archive.org/download/institutesofeccl02mosh/institutesofeccl02mosh_djvu.txt",
    },
    {
        "slug": "kurtz-church-history-v1",
        "title": "교회사 제1권: 사도 시대~종교개혁 이전",
        "title_en": "Church History Vol.1: Apostolic Age to Pre-Reformation",
        "author_kr": "요한 쿠르츠", "author_en": "Johann Kurtz", "year": 1860,
        "direct_url": "https://archive.org/download/churchhistoryv01kurt/churchhistoryv01kurt_djvu.txt",
    },
    {
        "slug": "kurtz-church-history-v2",
        "title": "교회사 제2권: 종교개혁~근대",
        "title_en": "Church History Vol.2: Reformation to Modern Age",
        "author_kr": "요한 쿠르츠", "author_en": "Johann Kurtz", "year": 1860,
        "direct_url": "https://archive.org/download/churchhistoryv02kurt/churchhistoryv02kurt_djvu.txt",
    },
    {
        "slug": "doddridge-family-expositor-v1",
        "title": "가정 성경 강해 제1권: 마태복음~사도행전",
        "title_en": "The Family Expositor Vol.1: NT Paraphrase (Matt–Acts)",
        "author_kr": "필립 도드리지", "author_en": "Philip Doddridge", "year": 1739,
        "direct_url": "https://archive.org/download/familyexpositor01dodd/familyexpositor01dodd_djvu.txt",
    },
    {
        "slug": "doddridge-family-expositor-v2",
        "title": "가정 성경 강해 제2권: 로마서~요한계시록",
        "title_en": "The Family Expositor Vol.2: NT Paraphrase (Romans–Revelation)",
        "author_kr": "필립 도드리지", "author_en": "Philip Doddridge", "year": 1756,
        "direct_url": "https://archive.org/download/familyexpositor02dodd/familyexpositor02dodd_djvu.txt",
    },
]

if __name__ == "__main__":
    process_all(BOOKS, delay=1.5)
