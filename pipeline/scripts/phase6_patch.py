#!/usr/bin/env python3
"""Phase 6 패치: 자동 검색 실패 도서에 직접 URL 지정 재처리."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.scripts.phase5_utils import process_all, BOOKS_DIR

BOOKS = [
    # ── 라이트풋 주석 시리즈 (J.B. Lightfoot) ──
    {
        "slug": "lightfoot-galatians",
        "title": "갈라디아서 주석", "title_en": "Commentary on Galatians",
        "author_kr": "J.B. 라이트풋", "author_en": "J.B. Lightfoot", "year": 1865,
        "direct_url": "https://archive.org/download/saintpaulsepistle00light/saintpaulsepistle00light_djvu.txt",
    },
    {
        "slug": "lightfoot-philippians",
        "title": "빌립보서 주석", "title_en": "Commentary on Philippians",
        "author_kr": "J.B. 라이트풋", "author_en": "J.B. Lightfoot", "year": 1868,
        "direct_url": "https://archive.org/download/saintpaulsepistle00ligh_0/saintpaulsepistle00ligh_0_djvu.txt",
    },
    {
        "slug": "lightfoot-colossians-philemon",
        "title": "골로새서·빌레몬서 주석", "title_en": "Commentary on Colossians & Philemon",
        "author_kr": "J.B. 라이트풋", "author_en": "J.B. Lightfoot", "year": 1875,
        "direct_url": "https://archive.org/download/epistlestocoloss00ligh/epistlestocoloss00ligh_djvu.txt",
    },
    {
        "slug": "lightfoot-apostolic-fathers-v1",
        "title": "사도교부 제1권: 클레멘트", "title_en": "The Apostolic Fathers Vol.1: Clement",
        "author_kr": "J.B. 라이트풋", "author_en": "J.B. Lightfoot", "year": 1869,
        "direct_url": "https://archive.org/download/apostolicfathers01ligh/apostolicfathers01ligh_djvu.txt",
    },

    # ── 웨스트콧 주석 시리즈 (B.F. Westcott) ──
    {
        "slug": "westcott-gospel-john",
        "title": "요한복음 주석", "title_en": "The Gospel According to St. John",
        "author_kr": "B.F. 웨스트콧", "author_en": "B.F. Westcott", "year": 1882,
        "direct_url": "https://archive.org/download/gospelaccordingt00westuoft/gospelaccordingt00westuoft_djvu.txt",
    },
    {
        "slug": "westcott-epistle-hebrews",
        "title": "히브리서 주석", "title_en": "The Epistle to the Hebrews",
        "author_kr": "B.F. 웨스트콧", "author_en": "B.F. Westcott", "year": 1889,
        "direct_url": "https://archive.org/download/epistletohebrews00westuoft/epistletohebrews00westuoft_djvu.txt",
    },
    {
        "slug": "westcott-epistles-john",
        "title": "요한서신 주석", "title_en": "The Epistles of St. John",
        "author_kr": "B.F. 웨스트콧", "author_en": "B.F. Westcott", "year": 1883,
        "direct_url": "https://archive.org/download/epistlesofjohn00westuoft/epistlesofjohn00westuoft_djvu.txt",
    },

    # ── 고데 주석 시리즈 (F.B. Godet) ──
    {
        "slug": "godet-commentary-john-v1",
        "title": "요한복음 주석 제1권", "title_en": "Commentary on John Vol.1",
        "author_kr": "F.B. 고데", "author_en": "F.B. Godet", "year": 1877,
        "direct_url": "https://archive.org/download/commentaryongos01gode/commentaryongos01gode_djvu.txt",
    },
    {
        "slug": "godet-commentary-john-v2",
        "title": "요한복음 주석 제2권", "title_en": "Commentary on John Vol.2",
        "author_kr": "F.B. 고데", "author_en": "F.B. Godet", "year": 1877,
        "direct_url": "https://archive.org/download/commentaryongos02gode/commentaryongos02gode_djvu.txt",
    },
    {
        "slug": "godet-commentary-romans",
        "title": "로마서 주석", "title_en": "Commentary on Romans",
        "author_kr": "F.B. 고데", "author_en": "F.B. Godet", "year": 1879,
        "direct_url": "https://archive.org/download/commentaryonepi01godegoog/commentaryonepi01godegoog_djvu.txt",
    },
    {
        "slug": "godet-commentary-1cor",
        "title": "고린도전서 주석", "title_en": "Commentary on 1 Corinthians",
        "author_kr": "F.B. 고데", "author_en": "F.B. Godet", "year": 1886,
        "direct_url": "https://archive.org/download/commentaryonfirs01gode/commentaryonfirs01gode_djvu.txt",
    },
    {
        "slug": "godet-commentary-luke",
        "title": "누가복음 주석", "title_en": "Commentary on Luke",
        "author_kr": "F.B. 고데", "author_en": "F.B. Godet", "year": 1875,
        "direct_url": "https://archive.org/download/commentaryongos00gode/commentaryongos00gode_djvu.txt",
    },

    # ── 호지 조직신학 (Charles Hodge) ──
    {
        "slug": "hodge-systematic-theology-v1",
        "title": "조직신학 제1권: 신론", "title_en": "Systematic Theology Vol.1",
        "author_kr": "찰스 호지", "author_en": "Charles Hodge", "year": 1872,
        "direct_url": "https://archive.org/download/systematictheolo01hodg/systematictheolo01hodg_djvu.txt",
    },
    {
        "slug": "hodge-systematic-theology-v2",
        "title": "조직신학 제2권: 인간론·구원론", "title_en": "Systematic Theology Vol.2",
        "author_kr": "찰스 호지", "author_en": "Charles Hodge", "year": 1872,
        "direct_url": "https://archive.org/download/systematictheolo02hodg/systematictheolo02hodg_djvu.txt",
    },
    {
        "slug": "hodge-systematic-theology-v3",
        "title": "조직신학 제3권: 교회론·종말론", "title_en": "Systematic Theology Vol.3",
        "author_kr": "찰스 호지", "author_en": "Charles Hodge", "year": 1872,
        "direct_url": "https://archive.org/download/systematictheolo03hodg/systematictheolo03hodg_djvu.txt",
    },

    # ── A.A. 호지 ──
    {
        "slug": "aa-hodge-outlines-theology",
        "title": "신학 개요", "title_en": "Outlines of Theology",
        "author_kr": "A.A. 호지", "author_en": "A.A. Hodge", "year": 1879,
        "direct_url": "https://archive.org/download/outlinesoftheolo00hodg/outlinesoftheolo00hodg_djvu.txt",
    },

    # ── 워필드 (B.B. Warfield) ──
    {
        "slug": "warfield-plan-of-salvation",
        "title": "구원의 계획", "title_en": "The Plan of Salvation",
        "author_kr": "B.B. 워필드", "author_en": "B.B. Warfield", "year": 1915,
        "direct_url": "https://archive.org/download/planofsalvation00warf/planofsalvation00warf_djvu.txt",
    },
    {
        "slug": "warfield-lord-of-glory",
        "title": "영광의 주님", "title_en": "The Lord of Glory",
        "author_kr": "B.B. 워필드", "author_en": "B.B. Warfield", "year": 1907,
        "direct_url": "https://archive.org/download/lordofglory00warf/lordofglory00warf_djvu.txt",
    },
    {
        "slug": "warfield-faith-and-life",
        "title": "신앙과 생활", "title_en": "Faith and Life",
        "author_kr": "B.B. 워필드", "author_en": "B.B. Warfield", "year": 1916,
        "direct_url": "https://archive.org/download/faithandlife00warf/faithandlife00warf_djvu.txt",
    },

    # ── 델리취 주석 (Franz Delitzsch) ──
    {
        "slug": "delitzsch-psalms-v1",
        "title": "시편 주석 제1권", "title_en": "Commentary on Psalms Vol.1",
        "author_kr": "프란츠 델리취", "author_en": "Franz Delitzsch", "year": 1871,
        "direct_url": "https://archive.org/download/biblicalcomment08keiluoft/biblicalcomment08keiluoft_djvu.txt",
    },
    {
        "slug": "delitzsch-psalms-v2",
        "title": "시편 주석 제2권", "title_en": "Commentary on Psalms Vol.2",
        "author_kr": "프란츠 델리취", "author_en": "Franz Delitzsch", "year": 1871,
        "direct_url": "https://archive.org/download/biblicalcomment09keiluoft/biblicalcomment09keiluoft_djvu.txt",
    },
    {
        "slug": "delitzsch-isaiah-v1",
        "title": "이사야 주석 제1권", "title_en": "Commentary on Isaiah Vol.1",
        "author_kr": "프란츠 델리취", "author_en": "Franz Delitzsch", "year": 1867,
        "direct_url": "https://archive.org/download/biblicalcomment12keiluoft/biblicalcomment12keiluoft_djvu.txt",
    },
    {
        "slug": "delitzsch-isaiah-v2",
        "title": "이사야 주석 제2권", "title_en": "Commentary on Isaiah Vol.2",
        "author_kr": "프란츠 델리취", "author_en": "Franz Delitzsch", "year": 1867,
        "direct_url": "https://archive.org/download/biblicalcomment13keiluoft/biblicalcomment13keiluoft_djvu.txt",
    },

    # ── 카일 주석 (C.F. Keil) ──
    {
        "slug": "keil-daniel",
        "title": "다니엘서 주석", "title_en": "Commentary on Daniel",
        "author_kr": "C.F. 카일", "author_en": "C.F. Keil", "year": 1877,
        "direct_url": "https://archive.org/download/biblicalcomment23keiluoft/biblicalcomment23keiluoft_djvu.txt",
    },
    {
        "slug": "keil-minor-prophets-v1",
        "title": "소선지서 주석 제1권", "title_en": "Commentary on Minor Prophets Vol.1",
        "author_kr": "C.F. 카일", "author_en": "C.F. Keil", "year": 1868,
        "direct_url": "https://archive.org/download/biblicalcomment24keiluoft/biblicalcomment24keiluoft_djvu.txt",
    },
    {
        "slug": "keil-minor-prophets-v2",
        "title": "소선지서 주석 제2권", "title_en": "Commentary on Minor Prophets Vol.2",
        "author_kr": "C.F. 카일", "author_en": "C.F. Keil", "year": 1868,
        "direct_url": "https://archive.org/download/biblicalcomment25keiluoft/biblicalcomment25keiluoft_djvu.txt",
    },

    # ── J.A. 알렉산더 (Joseph Addison Alexander) ──
    {
        "slug": "ja-alexander-isaiah-v1",
        "title": "이사야 주석 제1권", "title_en": "Commentary on Isaiah Vol.1",
        "author_kr": "조셉 애디슨 알렉산더", "author_en": "Joseph Addison Alexander", "year": 1846,
        "direct_url": "https://archive.org/download/commentaryonproph01alex/commentaryonproph01alex_djvu.txt",
    },
    {
        "slug": "ja-alexander-isaiah-v2",
        "title": "이사야 주석 제2권", "title_en": "Commentary on Isaiah Vol.2",
        "author_kr": "조셉 애디슨 알렉산더", "author_en": "Joseph Addison Alexander", "year": 1846,
        "direct_url": "https://archive.org/download/commentaryonproph02alex/commentaryonproph02alex_djvu.txt",
    },

    # ── 기독교 시문학 (허버트, 던) ──
    {
        "slug": "herbert-country-parson",
        "title": "성직자의 삶", "title_en": "A Priest to the Temple (The Country Parson)",
        "author_kr": "조지 허버트", "author_en": "George Herbert", "year": 1652,
        "gutenberg_id": 15646,
    },
    {
        "slug": "donne-divine-poems",
        "title": "신성한 시와 거룩한 소네트", "title_en": "Divine Poems and Holy Sonnets",
        "author_kr": "존 던", "author_en": "John Donne", "year": 1633,
        "gutenberg_id": 16269,
    },
    {
        "slug": "rossetti-verses",
        "title": "시편: 성인으로 부르심을 받아", "title_en": "Verses",
        "author_kr": "크리스티나 로세티", "author_en": "Christina Rossetti", "year": 1893,
        "gutenberg_id": 11739,
    },
    {
        "slug": "thompson-hound-of-heaven",
        "title": "천국의 사냥개와 기타 시", "title_en": "The Hound of Heaven and Other Poems",
        "author_kr": "프란시스 톰슨", "author_en": "Francis Thompson", "year": 1893,
        "gutenberg_id": 6446,
    },

    # ── 와이트 성경 인물론 (Alexander Whyte) ──
    {
        "slug": "whyte-bible-characters-v3",
        "title": "성경 인물론 제3권", "title_en": "Bible Characters Vol.3",
        "author_kr": "알렉산더 와이트", "author_en": "Alexander Whyte", "year": 1900,
        "direct_url": "https://archive.org/download/biblecharacters03whytgoog/biblecharacters03whytgoog_djvu.txt",
    },
    {
        "slug": "whyte-bible-characters-v4",
        "title": "성경 인물론 제4권", "title_en": "Bible Characters Vol.4",
        "author_kr": "알렉산더 와이트", "author_en": "Alexander Whyte", "year": 1906,
        "direct_url": "https://archive.org/download/biblecharacters04whytgoog/biblecharacters04whytgoog_djvu.txt",
    },

    # ── 드럼먼드 / 파커 / 맥그레거 / 조웨트 ──
    {
        "slug": "drummond-new-evangelism",
        "title": "새 복음전도와 기타 논문", "title_en": "The New Evangelism and Other Papers",
        "author_kr": "헨리 드럼먼드", "author_en": "Henry Drummond", "year": 1899,
        "gutenberg_id": 11991,
    },
    {
        "slug": "parker-city-temple-v1",
        "title": "시티 템플 설교집 제1권", "title_en": "City Temple Sermons Vol.1",
        "author_kr": "조지프 파커", "author_en": "Joseph Parker", "year": 1886,
        "direct_url": "https://archive.org/download/citytemplepulpit01park/citytemplepulpit01park_djvu.txt",
    },
    {
        "slug": "macgregor-making-of-man",
        "title": "사람의 형성", "title_en": "The Making of a Man",
        "author_kr": "W.M. 맥그레거", "author_en": "W.M. Macgregor", "year": 1927,
        "direct_url": "https://archive.org/download/makingofman00macg/makingofman00macg_djvu.txt",
    },

    # ── 침례교 (풀러, 길, 홀) ──
    {
        "slug": "fuller-complete-works-sel",
        "title": "전집 (선집)", "title_en": "Complete Works (selections)",
        "author_kr": "앤드류 풀러", "author_en": "Andrew Fuller", "year": 1836,
        "direct_url": "https://archive.org/download/worksandrewfulle01full/worksandrewfulle01full_djvu.txt",
    },
    {
        "slug": "gill-body-divinity-sel",
        "title": "신학총론 (선집)", "title_en": "A Body of Divinity (selections)",
        "author_kr": "존 길", "author_en": "John Gill", "year": 1769,
        "direct_url": "https://archive.org/download/bodyofdivinity00gill/bodyofdivinity00gill_djvu.txt",
    },
    {
        "slug": "hall-robert-works-sel",
        "title": "로버트 홀 전집 (선집)", "title_en": "Works of Robert Hall (selections)",
        "author_kr": "로버트 홀", "author_en": "Robert Hall", "year": 1839,
        "gutenberg_id": 30154,
    },

    # ── 모노 / 말란 / 비네 / 메를 도비녜 ──
    {
        "slug": "monod-farewell-sermons",
        "title": "아돌프 모노 고별 설교집", "title_en": "Farewell Sermons of Adolphe Monod",
        "author_kr": "아돌프 모노", "author_en": "Adolphe Monod", "year": 1856,
        "direct_url": "https://archive.org/download/adolphemonodfarew00mono/adolphemonodfarew00mono_djvu.txt",
    },
    {
        "slug": "monod-living-for-god",
        "title": "하나님을 위한 삶", "title_en": "Living for God (Sermons)",
        "author_kr": "아돌프 모노", "author_en": "Adolphe Monod", "year": 1849,
        "direct_url": "https://archive.org/download/adolphemonodlivi00mono/adolphemonodlivi00mono_djvu.txt",
    },
    {
        "slug": "malan-sermons-letters",
        "title": "체사르 말란 설교와 서신", "title_en": "Sermons and Letters of César Malan",
        "author_kr": "체사르 말란", "author_en": "César Malan", "year": 1865,
        "direct_url": "https://archive.org/download/lifeworksrevcsad00mala/lifeworksrevcsad00mala_djvu.txt",
    },
    {
        "slug": "vinet-homiletics",
        "title": "설교학", "title_en": "Homiletics",
        "author_kr": "알렉상드르 비네", "author_en": "Alexandre Vinet", "year": 1853,
        "direct_url": "https://archive.org/download/homileticsortheo00vine/homileticsortheo00vine_djvu.txt",
    },
    {
        "slug": "merle-biographies-sel",
        "title": "인물 연구", "title_en": "Biographical Studies",
        "author_kr": "J.H. 메를 도비녜", "author_en": "J.H. Merle d'Aubigné", "year": 1870,
        "direct_url": "https://archive.org/download/biographicalstud00merl/biographicalstud00merl_djvu.txt",
    },

    # ── 찰머스 ──
    {
        "slug": "chalmers-christian-social-economy",
        "title": "대도시의 기독교·시민 경제", "title_en": "On the Christian and Civic Economy",
        "author_kr": "토마스 찰머스", "author_en": "Thomas Chalmers", "year": 1821,
        "direct_url": "https://archive.org/download/christiancivicev01chal/christiancivicev01chal_djvu.txt",
    },

    # ── 경건주의 / 자유교회 / 조직신학 보조 ──
    {
        "slug": "francke-autobiography",
        "title": "프랑케 자서전", "title_en": "Autobiography of A.H. Francke",
        "author_kr": "아우구스트 헤르만 프랑케", "author_en": "August Hermann Francke", "year": 1727,
        "direct_url": "https://archive.org/download/augusthermanfran00fran/augusthermanfran00fran_djvu.txt",
    },
    {
        "slug": "zinzendorf-nine-lectures",
        "title": "종교의 주요 주제에 관한 아홉 강의", "title_en": "Nine Public Lectures",
        "author_kr": "니콜라우스 폰 친첸도르프", "author_en": "Nikolaus von Zinzendorf", "year": 1748,
        "direct_url": "https://archive.org/download/ninepubliclectur00zinz/ninepubliclectur00zinz_djvu.txt",
    },
    {
        "slug": "tersteegen-quiet-way-sel",
        "title": "조용한 길 (선집)", "title_en": "The Quiet Way (selections)",
        "author_kr": "게르하르트 테르스테겐", "author_en": "Gerhard Tersteegen", "year": 1769,
        "direct_url": "https://archive.org/download/quietwaytransla00ters/quietwaytransla00ters_djvu.txt",
    },
    {
        "slug": "bengel-ordered-life",
        "title": "질서 잡힌 삶", "title_en": "Ordered Life",
        "author_kr": "요한 알브레흐트 벵겔", "author_en": "Johann Albrecht Bengel", "year": 1759,
        "direct_url": "https://archive.org/download/orderedlifeletters00beng/orderedlifeletters00beng_djvu.txt",
    },
    {
        "slug": "duncan-colloquia-peripatetica",
        "title": "소요하며 나눈 대화", "title_en": "Colloquia Peripatetica",
        "author_kr": "존 랍비 던컨", "author_en": "John \"Rabbi\" Duncan", "year": 1870,
        "direct_url": "https://archive.org/download/colloquiaperipat00dunc/colloquiaperipat00dunc_djvu.txt",
    },
    {
        "slug": "forsyth-cruciality-cross",
        "title": "십자가의 결정적 의미", "title_en": "The Cruciality of the Cross",
        "author_kr": "P.T. 포르시스", "author_en": "P.T. Forsyth", "year": 1909,
        "direct_url": "https://archive.org/download/crucialityofcros00fors/crucialityofcros00fors_djvu.txt",
    },
    {
        "slug": "moule-romans-devotional",
        "title": "로마서 강해", "title_en": "The Epistle of Paul to the Romans",
        "author_kr": "핸들리 C.G. 무울", "author_en": "Handley C.G. Moule", "year": 1894,
        "direct_url": "https://archive.org/download/epistleofpaultoro00moul/epistleofpaultoro00moul_djvu.txt",
    },
    {
        "slug": "moule-philippian-studies",
        "title": "빌립보서 연구", "title_en": "Philippian Studies",
        "author_kr": "핸들리 C.G. 무울", "author_en": "Handley C.G. Moule", "year": 1897,
        "direct_url": "https://archive.org/download/philippianstudi00moul/philippianstudi00moul_djvu.txt",
    },
    {
        "slug": "stewart-life-in-christ",
        "title": "그리스도 안의 사람", "title_en": "A Man in Christ",
        "author_kr": "제임스 S. 스튜어트", "author_en": "James S. Stewart", "year": 1935,
        "direct_url": "https://archive.org/download/maninchrist00stew/maninchrist00stew_djvu.txt",
    },
    {
        "slug": "denny-atonement",
        "title": "속죄의 기독교 교리", "title_en": "The Christian Doctrine of Atonement",
        "author_kr": "로버트 윌리엄 데일", "author_en": "Robert William Dale", "year": 1875,
        "direct_url": "https://archive.org/download/atonement00dale/atonement00dale_djvu.txt",
    },

    # ── 맨턴 / 채녹 / 굿윈 ──
    {
        "slug": "manton-119th-psalm-v1",
        "title": "시편 119편 강해 제1권", "title_en": "An Exposition of Psalm 119 Vol.1",
        "author_kr": "토마스 맨턴", "author_en": "Thomas Manton", "year": 1681,
        "direct_url": "https://archive.org/download/expositionofpsalm01mant/expositionofpsalm01mant_djvu.txt",
    },
    {
        "slug": "manton-119th-psalm-v2",
        "title": "시편 119편 강해 제2권", "title_en": "An Exposition of Psalm 119 Vol.2",
        "author_kr": "토마스 맨턴", "author_en": "Thomas Manton", "year": 1681,
        "direct_url": "https://archive.org/download/expositionofpsalm02mant/expositionofpsalm02mant_djvu.txt",
    },
    {
        "slug": "charnock-works-regeneration",
        "title": "전집: 중생론", "title_en": "The Works: On Regeneration",
        "author_kr": "스티븐 채녹", "author_en": "Stephen Charnock", "year": 1840,
        "direct_url": "https://archive.org/download/worksofstephench01char/worksofstephench01char_djvu.txt",
    },
    {
        "slug": "goodwin-works-sel-v1",
        "title": "전집 제1권: 칭의 신앙", "title_en": "Works of Thomas Goodwin Vol.1",
        "author_kr": "토마스 굿윈", "author_en": "Thomas Goodwin", "year": 1681,
        "direct_url": "https://archive.org/download/worksofthomasgoo01good/worksofthomasgoo01good_djvu.txt",
    },
    {
        "slug": "goodwin-works-sel-v2",
        "title": "전집 제2권: 성령의 사역", "title_en": "Works of Thomas Goodwin Vol.2",
        "author_kr": "토마스 굿윈", "author_en": "Thomas Goodwin", "year": 1681,
        "direct_url": "https://archive.org/download/worksofthomasgoo02good/worksofthomasgoo02good_djvu.txt",
    },

    # ── 부흥 1차 사료 ──
    {
        "slug": "mcculloch-cambuslang-revival",
        "title": "캠버스랭 부흥 간증록", "title_en": "Cambuslang Revival Testimonies",
        "author_kr": "윌리엄 맥컬로크", "author_en": "William McCulloch", "year": 1742,
        "direct_url": "https://archive.org/download/workofgodincambu00mccu/workofgodincambu00mccu_djvu.txt",
    },
    {
        "slug": "payson-memoir-letters",
        "title": "에드워드 페이슨 회고록", "title_en": "Memoir and Letters of Edward Payson",
        "author_kr": "에이사 커밍스 (편)", "author_en": "Asa Cummings (ed.)", "year": 1830,
        "direct_url": "https://archive.org/download/memoirofrevdedwa00paysgoog/memoirofrevdedwa00paysgoog_djvu.txt",
    },
    {
        "slug": "duff-india-missions-sel",
        "title": "인도와 인도 선교", "title_en": "India and India Missions",
        "author_kr": "알렉산더 더프", "author_en": "Alexander Duff", "year": 1839,
        "direct_url": "https://archive.org/download/indiaindiaindiam00duff/indiaindiaindiam00duff_djvu.txt",
    },
    {
        "slug": "mackay-hero-uganda",
        "title": "우간다의 영웅 맥케이", "title_en": "Mackay of Uganda",
        "author_kr": "A.M. 맥케이의 누이", "author_en": "A.M. Mackay's Sister", "year": 1890,
        "gutenberg_id": 11862,
    },
]


def main():
    from pipeline.scripts.phase5_utils import process_all
    results, failed = process_all(BOOKS, delay=1.5)
    print(f"\n패치 결과: 성공 {results['success']}, 실패 {results['failed']}, 건너뜀 {results['skipped']}")
    if failed:
        print("남은 실패 목록:")
        for s in failed:
            print(f"  - {s}")


if __name__ == "__main__":
    main()
