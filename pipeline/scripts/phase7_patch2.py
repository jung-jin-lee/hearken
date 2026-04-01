#!/usr/bin/env python3
"""Phase 7 패치 2: 잘못된 CCEL 경로 수정 및 대안 archive.org 식별자 적용.

패치 1에서 실패한 81권 중 확인된 44권을 처리.
- CCEL NPNF 경로 → archive.org 직접 URL로 교체
- archive.org 식별자 수정 (0000 vs 00 패턴 등)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.scripts.phase5_utils import process_all

BOOKS = [
    # ══════════════════════════════════════════════════════════════
    # 카테고리 66: 크리소스톰 — archive.org 직접 URL
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "chrysostom-homilies-1cor",
        "title": "고린도전서 강해 (44편)", "title_en": "Homilies on 1 Corinthians (44 Homilies)",
        "author_kr": "요한 크리소스톰", "author_en": "John Chrysostom", "year": 392,
        "direct_url": "https://archive.org/download/homiliessjohnch00keblgoog/homiliessjohnch00keblgoog_djvu.txt",
    },
    {
        "slug": "chrysostom-homilies-2cor",
        "title": "고린도후서 강해 (30편)", "title_en": "Homilies on 2 Corinthians (30 Homilies)",
        "author_kr": "요한 크리소스톰", "author_en": "John Chrysostom", "year": 393,
        "direct_url": "https://archive.org/download/homiliesofsjohnc27john/homiliesofsjohnc27john_djvu.txt",
    },
    {
        "slug": "chrysostom-homilies-galatians-ephesians",
        "title": "갈라디아서·에베소서 강해", "title_en": "Homilies on Galatians & Ephesians",
        "author_kr": "요한 크리소스톰", "author_en": "John Chrysostom", "year": 393,
        "direct_url": "https://archive.org/download/commentaryonepis06john/commentaryonepis06john_djvu.txt",
    },
    {
        "slug": "chrysostom-homilies-philippians-col-thess",
        "title": "빌립보서·골로새서·데살로니가서 강해",
        "title_en": "Homilies on Philippians, Colossians & Thessalonians",
        "author_kr": "요한 크리소스톰", "author_en": "John Chrysostom", "year": 394,
        "direct_url": "https://archive.org/download/30ALibraryOfFathersOfTheHolyCatholicV30/30ALibraryOfFathersOfTheHolyCatholicV30_djvu.txt",
    },
    {
        "slug": "chrysostom-on-priesthood",
        "title": "사제직에 관한 여섯 권의 책", "title_en": "Six Books on the Priesthood (De Sacerdotio)",
        "author_kr": "요한 크리소스톰", "author_en": "John Chrysostom", "year": 390,
        "direct_url": "https://archive.org/download/onpriesthood00unkngoog/onpriesthood00unkngoog_djvu.txt",
    },
    {
        "slug": "chrysostom-homilies-statues",
        "title": "안티오키아 백성에게 보내는 강해 (조각상에 대하여)",
        "title_en": "Homilies on the Statues (To the People of Antioch)",
        "author_kr": "요한 크리소스톰", "author_en": "John Chrysostom", "year": 387,
        "direct_url": "https://archive.org/download/33ALibraryOfFathersOfTheHolyCatholicV33/33ALibraryOfFathersOfTheHolyCatholicV33_djvu.txt",
    },
    # ══════════════════════════════════════════════════════════════
    # 카테고리 67: 갑바도기아 교부들 — archive.org 직접 URL
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "basil-on-holy-spirit",
        "title": "성령에 대하여", "title_en": "On the Holy Spirit (De Spiritu Sancto)",
        "author_kr": "가이사랴의 바실리우스", "author_en": "Basil of Caesarea", "year": 375,
        "direct_url": "https://archive.org/download/bookofsaintbasil00basi/bookofsaintbasil00basi_djvu.txt",
    },
    {
        "slug": "basil-ascetical-works",
        "title": "금욕적 작품들 (긴 규칙과 짧은 규칙 포함)",
        "title_en": "Ascetical Works (Long Rules & Short Rules)",
        "author_kr": "가이사랴의 바실리우스", "author_en": "Basil of Caesarea", "year": 360,
        "direct_url": "https://archive.org/download/asceticworksofsa0000basi/asceticworksofsa0000basi_djvu.txt",
    },
    {
        "slug": "gregory-nazianzus-theological-orations",
        "title": "신학적 강론 다섯 편", "title_en": "Five Theological Orations",
        "author_kr": "나지안주스의 그레고리우스", "author_en": "Gregory of Nazianzus", "year": 380,
        "direct_url": "https://archive.org/download/fivetheologicalo00greg_0/fivetheologicalo00greg_0_djvu.txt",
    },
    {
        "slug": "gregory-nazianzus-orations-selected",
        "title": "강론 선집 (제2·7·10·14·21·43강론)",
        "title_en": "Selected Orations (Orations 2, 7, 10, 14, 21, 43)",
        "author_kr": "나지안주스의 그레고리우스", "author_en": "Gregory of Nazianzus", "year": 380,
        "direct_url": "https://archive.org/download/niceneandpostnic05unknuoft/niceneandpostnic05unknuoft_djvu.txt",
    },
    # ══════════════════════════════════════════════════════════════
    # 카테고리 68: 중세 서방 신비주의
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "bernard-on-loving-god",
        "title": "하나님을 사랑함에 대하여", "title_en": "On Loving God (De Diligendo Deo)",
        "author_kr": "클레르보의 베르나르", "author_en": "Bernard of Clairvaux", "year": 1128,
        "direct_url": "https://archive.org/download/on-loving-god-by-saint-bernard-of-clairvaux/on-loving-god-by-saint-bernard-of-clairvaux_djvu.txt",
    },
    {
        "slug": "bernard-steps-humility-pride",
        "title": "겸손과 교만의 단계들", "title_en": "The Steps of Humility and Pride",
        "author_kr": "클레르보의 베르나르", "author_en": "Bernard of Clairvaux", "year": 1120,
        "direct_url": "https://archive.org/download/MN41533ucmf_0/MN41533ucmf_0_djvu.txt",
    },
    {
        "slug": "bernard-sermons-song-v1",
        "title": "아가 강해 설교 제1권", "title_en": "Sermons on the Song of Songs Vol.1",
        "author_kr": "클레르보의 베르나르", "author_en": "Bernard of Clairvaux", "year": 1135,
        "direct_url": "https://archive.org/download/stbernardssermon02bern/stbernardssermon02bern_djvu.txt",
    },
    {
        "slug": "hilton-scale-of-perfection-v1",
        "title": "완전의 계단 제1권", "title_en": "The Scale of Perfection Vol.1",
        "author_kr": "월터 힐튼", "author_en": "Walter Hilton", "year": 1395,
        "direct_url": "https://archive.org/download/scaleofperfectio0000walt_d2u3/scaleofperfectio0000walt_d2u3_djvu.txt",
    },
    {
        "slug": "rolle-fire-of-love",
        "title": "사랑의 불길 (Incendium Amoris)", "title_en": "The Fire of Love (Incendium Amoris)",
        "author_kr": "리처드 롤", "author_en": "Richard Rolle", "year": 1343,
        "direct_url": "https://archive.org/download/fireoflovemendin00roll/fireoflovemendin00roll_djvu.txt",
    },
    # ══════════════════════════════════════════════════════════════
    # 카테고리 69: 필립 샤프 교회사 및 신조집
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "schaff-church-history-v1",
        "title": "기독교 교회사 제1권: 사도 시대", "title_en": "History of the Christian Church Vol.1 (Apostolic Age)",
        "author_kr": "필립 샤프", "author_en": "Philip Schaff", "year": 1882,
        "direct_url": "https://archive.org/download/historyofchristi0007scha_m7h8/historyofchristi0007scha_m7h8_djvu.txt",
    },
    {
        "slug": "schaff-church-history-v2",
        "title": "기독교 교회사 제2권: 니케아 이전 기독교", "title_en": "History of the Christian Church Vol.2 (Ante-Nicene)",
        "author_kr": "필립 샤프", "author_en": "Philip Schaff", "year": 1883,
        "direct_url": "https://archive.org/download/historyofchristi02scha/historyofchristi02scha_djvu.txt",
    },
    {
        "slug": "schaff-church-history-v3",
        "title": "기독교 교회사 제3권: 니케아 및 후니케아 시대", "title_en": "History of the Christian Church Vol.3 (Nicene and Post-Nicene)",
        "author_kr": "필립 샤프", "author_en": "Philip Schaff", "year": 1884,
        "direct_url": "https://archive.org/download/historyofchristi03scha/historyofchristi03scha_djvu.txt",
    },
    {
        "slug": "schaff-church-history-v4",
        "title": "기독교 교회사 제4권: 중세 기독교", "title_en": "History of the Christian Church Vol.4 (Medieval Christianity)",
        "author_kr": "필립 샤프", "author_en": "Philip Schaff", "year": 1885,
        "direct_url": "https://archive.org/download/christianchurchh04schauoft/christianchurchh04schauoft_djvu.txt",
    },
    {
        "slug": "schaff-church-history-v6",
        "title": "기독교 교회사 제6권: 중세 기독교 II", "title_en": "History of the Christian Church Vol.6 (Middle Ages to Reformation)",
        "author_kr": "필립 샤프", "author_en": "Philip Schaff", "year": 1888,
        "direct_url": "https://archive.org/download/historyofchristi188402scha/historyofchristi188402scha_djvu.txt",
    },
    {
        "slug": "schaff-church-history-v7",
        "title": "기독교 교회사 제7권: 독일 종교개혁", "title_en": "History of the Christian Church Vol.7 (German Reformation)",
        "author_kr": "필립 샤프", "author_en": "Philip Schaff", "year": 1889,
        "direct_url": "https://archive.org/download/historyofchristi07scha/historyofchristi07scha_djvu.txt",
    },
    {
        "slug": "schaff-church-history-v8",
        "title": "기독교 교회사 제8권: 스위스 종교개혁 및 현대", "title_en": "History of the Christian Church Vol.8 (Swiss Reformation & Modern)",
        "author_kr": "필립 샤프", "author_en": "Philip Schaff", "year": 1892,
        "direct_url": "https://archive.org/download/historyofchristi0007phil_e4c2/historyofchristi0007phil_e4c2_djvu.txt",
    },
    {
        "slug": "schaff-creeds-christendom-v1",
        "title": "기독교 신조집 제1권: 역사", "title_en": "Creeds of Christendom Vol.1 (History of Creeds)",
        "author_kr": "필립 샤프", "author_en": "Philip Schaff", "year": 1877,
        "direct_url": "https://archive.org/download/creedschristendo01scha/creedschristendo01scha_djvu.txt",
    },
    {
        "slug": "schaff-creeds-christendom-v2",
        "title": "기독교 신조집 제2권: 그리스·로마 신조", "title_en": "Creeds of Christendom Vol.2 (Greek & Latin Creeds)",
        "author_kr": "필립 샤프", "author_en": "Philip Schaff", "year": 1877,
        "direct_url": "https://archive.org/download/creedschristendo02scha/creedschristendo02scha_djvu.txt",
    },
    # ══════════════════════════════════════════════════════════════
    # 카테고리 70: 성공회 경건 고전
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "hooker-laws-ecclesiastical-v1",
        "title": "교회 치리법 제1-4권", "title_en": "Laws of Ecclesiastical Polity Books 1-4",
        "author_kr": "리처드 후커", "author_en": "Richard Hooker", "year": 1594,
        "direct_url": "https://archive.org/download/worksofthatlea01hook/worksofthatlea01hook_djvu.txt",
    },
    {
        "slug": "hooker-laws-ecclesiastical-v2",
        "title": "교회 치리법 제5-8권", "title_en": "Laws of Ecclesiastical Polity Books 5-8",
        "author_kr": "리처드 후커", "author_en": "Richard Hooker", "year": 1597,
        "direct_url": "https://archive.org/download/worksofthatlea02hook/worksofthatlea02hook_djvu.txt",
    },
    {
        "slug": "andrewes-preces-privatae",
        "title": "사적 기도 (Preces Privatae)", "title_en": "Preces Privatae (Private Devotions)",
        "author_kr": "랜슬롯 앤드루스", "author_en": "Lancelot Andrewes", "year": 1648,
        "direct_url": "https://archive.org/download/a676964500andruoft/a676964500andruoft_djvu.txt",
    },
    # ══════════════════════════════════════════════════════════════
    # 카테고리 71: 초기 감리교 신학
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "adam-clarke-commentary-nt-v2",
        "title": "클라크 성경 주석: 신약 제2권 (로마서~계시록)",
        "title_en": "Clarke's Commentary on NT Vol.2 (Romans–Revelation)",
        "author_kr": "아담 클라크", "author_en": "Adam Clarke", "year": 1817,
        "direct_url": "https://archive.org/download/holybiblecontain05unse/holybiblecontain05unse_djvu.txt",
    },
    {
        "slug": "charles-wesley-hymns-sacred-poems",
        "title": "찬송과 성시 모음집", "title_en": "Hymns and Sacred Poems (Collected)",
        "author_kr": "찰스 웨슬리", "author_en": "Charles Wesley", "year": 1749,
        "direct_url": "https://archive.org/download/poeticalworksofj0004wesl/poeticalworksofj0004wesl_djvu.txt",
    },
    # ══════════════════════════════════════════════════════════════
    # 카테고리 72: 기도 고전
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "bounds-prayer-and-praying-men",
        "title": "기도하는 사람들 — 기도의 사도들", "title_en": "Prayer and Praying Men",
        "author_kr": "E.M. 바운즈", "author_en": "E.M. Bounds", "year": 1921,
        "gutenberg_id": 13476,
    },
    # ══════════════════════════════════════════════════════════════
    # 카테고리 73: 아나뱁티스트 원천 문헌
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "martyrs-mirror-sel",
        "title": "순교자의 거울 (선집)", "title_en": "The Bloody Theatre or Martyrs Mirror (selections)",
        "author_kr": "티엘만 얀 판 브라흐트", "author_en": "Thieleman J. van Braght", "year": 1660,
        "gutenberg_id": 65855,
    },
    # ══════════════════════════════════════════════════════════════
    # 카테고리 75: 헨리 알포드 신약 주석
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "alford-greek-testament-v1",
        "title": "헨리 알포드 그리스어 신약 제1권 (복음서)", "title_en": "Alford's Greek New Testament Vol.1 (Gospels)",
        "author_kr": "헨리 알포드", "author_en": "Henry Alford", "year": 1849,
        "direct_url": "https://archive.org/download/greektestament00alfogoog/greektestament00alfogoog_djvu.txt",
    },
    # ══════════════════════════════════════════════════════════════
    # 카테고리 76: 19세기 강해 설교자들
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "simeon-horae-homileticae-sel",
        "title": "강해 설교 선집 — 시므온의 강해", "title_en": "Horae Homileticae: Expository Discourses (selections)",
        "author_kr": "찰스 시므온", "author_en": "Charles Simeon", "year": 1819,
        "direct_url": "https://archive.org/download/horaehomiletica01sime/horaehomiletica01sime_djvu.txt",
    },
    {
        "slug": "dale-christian-doctrine",
        "title": "회중교회 원리 편람", "title_en": "Manual of Congregational Principles",
        "author_kr": "R.W. 데일", "author_en": "R.W. Dale", "year": 1884,
        "direct_url": "https://archive.org/download/amanualofcongreg00daleuoft/amanualofcongreg00daleuoft_djvu.txt",
    },
    {
        "slug": "cadman-ambassadors-for-god",
        "title": "하나님의 대사들", "title_en": "Ambassadors for God",
        "author_kr": "S. 파크스 캐드먼", "author_en": "S. Parkes Cadman", "year": 1920,
        "direct_url": "https://archive.org/download/ambassadorsofgod0000spar_f8x8/ambassadorsofgod0000spar_f8x8_djvu.txt",
    },
    # ══════════════════════════════════════════════════════════════
    # 카테고리 77: 기독교 순교·박해 역사
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "foxe-acts-monuments-v1",
        "title": "순교자 열전 제1권: 초대교회~위클리프",
        "title_en": "Foxe's Acts and Monuments Vol.1: Early Church to Wycliffe",
        "author_kr": "존 폭스", "author_en": "John Foxe", "year": 1563,
        "direct_url": "https://archive.org/download/actsmonumentsofj01foxe/actsmonumentsofj01foxe_djvu.txt",
    },
    {
        "slug": "foxe-acts-monuments-v2",
        "title": "순교자 열전 제2권: 롤라드파~메리 여왕 이전",
        "title_en": "Foxe's Acts and Monuments Vol.2: Lollards to Pre-Marian England",
        "author_kr": "존 폭스", "author_en": "John Foxe", "year": 1563,
        "direct_url": "https://archive.org/download/actsmonumentsofj02foxe/actsmonumentsofj02foxe_djvu.txt",
    },
    {
        "slug": "foxe-acts-monuments-v3",
        "title": "순교자 열전 제3권: 메리 여왕 시대 순교자들",
        "title_en": "Foxe's Acts and Monuments Vol.3: Marian Martyrs 1555–1558",
        "author_kr": "존 폭스", "author_en": "John Foxe", "year": 1563,
        "direct_url": "https://archive.org/download/actsmonumentsofj03foxe/actsmonumentsofj03foxe_djvu.txt",
    },
    # ══════════════════════════════════════════════════════════════
    # 카테고리 74: 종교개혁 추가 문헌
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "tyndale-works-selected",
        "title": "틴데일 선집: 서문·기독인의 순종·모어에 대한 답변",
        "title_en": "Works of William Tyndale: Prologues, Obedience of a Christian Man, Answer to More",
        "author_kr": "윌리엄 틴데일", "author_en": "William Tyndale", "year": 1528,
        "direct_url": "https://archive.org/download/The_Works_of_the_English_Reformers/The_Works_of_the_English_Reformers_djvu.txt",
    },
    # ══════════════════════════════════════════════════════════════
    # 카테고리 78: 신앙과 과학 변증학
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "rawlinson-historical-evidence",
        "title": "홍수의 역사적 증거", "title_en": "Historical Evidence of the Mosaic Account of the Deluge",
        "author_kr": "조지 롤린슨", "author_en": "George Rawlinson", "year": 1876,
        "direct_url": "https://archive.org/download/historicaleviden00rawl/historicaleviden00rawl_djvu.txt",
    },
    # ══════════════════════════════════════════════════════════════
    # 카테고리 80: 교회사 보조 명저
    # ══════════════════════════════════════════════════════════════
    {
        "slug": "kurtz-church-history-v1",
        "title": "교회사 제1권: 사도 시대~종교개혁 이전",
        "title_en": "Church History Vol.1: Apostolic Age to Pre-Reformation",
        "author_kr": "요한 쿠르츠", "author_en": "Johann Kurtz", "year": 1860,
        "direct_url": "https://archive.org/download/churchhistory01kurt/churchhistory01kurt_djvu.txt",
    },
    {
        "slug": "kurtz-church-history-v2",
        "title": "교회사 제2권: 종교개혁~근대",
        "title_en": "Church History Vol.2: Reformation to Modern Age",
        "author_kr": "요한 쿠르츠", "author_en": "Johann Kurtz", "year": 1860,
        "direct_url": "https://archive.org/download/churchhistory02kurt/churchhistory02kurt_djvu.txt",
    },
    {
        "slug": "doddridge-family-expositor-v1",
        "title": "가정 성경 강해 제1권: 마태복음~사도행전",
        "title_en": "The Family Expositor Vol.1: NT Paraphrase (Matt–Acts)",
        "author_kr": "필립 도드리지", "author_en": "Philip Doddridge", "year": 1739,
        "direct_url": "https://archive.org/download/familyexpositoro00dodd/familyexpositoro00dodd_djvu.txt",
    },
    {
        "slug": "doddridge-family-expositor-v2",
        "title": "가정 성경 강해 제2권: 로마서~요한계시록",
        "title_en": "The Family Expositor Vol.2: NT Paraphrase (Romans–Revelation)",
        "author_kr": "필립 도드리지", "author_en": "Philip Doddridge", "year": 1756,
        "direct_url": "https://archive.org/download/familyexpositoro02dodd/familyexpositoro02dodd_djvu.txt",
    },
]

if __name__ == "__main__":
    process_all(BOOKS, delay=1.5)
