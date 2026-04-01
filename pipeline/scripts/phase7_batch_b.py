#!/usr/bin/env python3
"""Phase 7 배치 B: 카테고리 68-69 (중세 서방 신비주의 10 + 필립 샤프 교회사 10) — 20권."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.scripts.phase5_utils import process_all

BOOKS = [
    # ── 카테고리 68: 중세 서방 신비주의 심화 (10권) ──
    {
        "slug": "bernard-on-loving-god",
        "title": "하나님 사랑에 관하여",
        "title_en": "On Loving God (De Diligendo Deo)",
        "author_kr": "클레르보의 버나드",
        "author_en": "Bernard of Clairvaux",
        "year": 1127,
    },
    {
        "slug": "bernard-sermons-song-v1",
        "title": "아가서 강해 제1권 (1-43편)",
        "title_en": "Sermons on the Song of Songs Vol.1 (Sermons 1–43)",
        "author_kr": "클레르보의 버나드",
        "author_en": "Bernard of Clairvaux",
        "year": 1135,
    },
    {
        "slug": "bernard-sermons-song-v2",
        "title": "아가서 강해 제2권 (44-86편)",
        "title_en": "Sermons on the Song of Songs Vol.2 (Sermons 44–86)",
        "author_kr": "클레르보의 버나드",
        "author_en": "Bernard of Clairvaux",
        "year": 1148,
    },
    {
        "slug": "bernard-steps-humility-pride",
        "title": "겸손과 교만의 계단",
        "title_en": "The Steps of Humility and Pride",
        "author_kr": "클레르보의 버나드",
        "author_en": "Bernard of Clairvaux",
        "year": 1124,
    },
    {
        "slug": "bonaventure-souls-journey",
        "title": "영혼의 하나님을 향한 여정",
        "title_en": "The Soul's Journey into God (Itinerarium Mentis in Deum)",
        "author_kr": "보나벤투라",
        "author_en": "Bonaventure",
        "year": 1259,
    },
    {
        "slug": "bonaventure-life-of-francis",
        "title": "성 프란체스코의 생애",
        "title_en": "The Life of St. Francis (Legenda Major)",
        "author_kr": "보나벤투라",
        "author_en": "Bonaventure",
        "year": 1263,
    },
    {
        "slug": "hilton-scale-of-perfection-v1",
        "title": "완전의 계단 제1권",
        "title_en": "The Scale of Perfection Vol.1",
        "author_kr": "월터 힐턴",
        "author_en": "Walter Hilton",
        "year": 1390,
    },
    {
        "slug": "hilton-scale-of-perfection-v2",
        "title": "완전의 계단 제2권",
        "title_en": "The Scale of Perfection Vol.2",
        "author_kr": "월터 힐턴",
        "author_en": "Walter Hilton",
        "year": 1395,
    },
    {
        "slug": "rolle-fire-of-love",
        "title": "사랑의 불꽃",
        "title_en": "The Fire of Love (Incendium Amoris)",
        "author_kr": "리처드 롤",
        "author_en": "Richard Rolle",
        "year": 1343,
    },
    {
        "slug": "ruysbroeck-adornment-spiritual-marriage",
        "title": "영적 결혼의 장식",
        "title_en": "The Adornment of the Spiritual Marriage",
        "author_kr": "얀 반 루이스브뢰크",
        "author_en": "Jan van Ruysbroeck",
        "year": 1335,
    },
    # ── 카테고리 69: 필립 샤프 교회사 시리즈 (10권) ──
    {
        "slug": "schaff-church-history-v1",
        "title": "기독교 교회사 제1권: 사도 시대",
        "title_en": "History of the Christian Church Vol.1: Apostolic Age",
        "author_kr": "필립 샤프",
        "author_en": "Philip Schaff",
        "year": 1858,
    },
    {
        "slug": "schaff-church-history-v2",
        "title": "기독교 교회사 제2권: 니케아 이전 시대",
        "title_en": "History of the Christian Church Vol.2: Ante-Nicene Age",
        "author_kr": "필립 샤프",
        "author_en": "Philip Schaff",
        "year": 1867,
    },
    {
        "slug": "schaff-church-history-v3",
        "title": "기독교 교회사 제3권: 니케아·후니케아 시대",
        "title_en": "History of the Christian Church Vol.3: Nicene & Post-Nicene Age",
        "author_kr": "필립 샤프",
        "author_en": "Philip Schaff",
        "year": 1867,
    },
    {
        "slug": "schaff-church-history-v4",
        "title": "기독교 교회사 제4권: 중세 전기",
        "title_en": "History of the Christian Church Vol.4: Mediæval Age to 1073",
        "author_kr": "필립 샤프",
        "author_en": "Philip Schaff",
        "year": 1867,
    },
    {
        "slug": "schaff-church-history-v5",
        "title": "기독교 교회사 제5권: 중세 중기",
        "title_en": "History of the Christian Church Vol.5: Middle Ages 1049–1294",
        "author_kr": "필립 샤프",
        "author_en": "Philip Schaff",
        "year": 1882,
    },
    {
        "slug": "schaff-church-history-v6",
        "title": "기독교 교회사 제6권: 종교개혁 직전",
        "title_en": "History of the Christian Church Vol.6: Middle Ages 1294–1517",
        "author_kr": "필립 샤프",
        "author_en": "Philip Schaff",
        "year": 1882,
    },
    {
        "slug": "schaff-church-history-v7",
        "title": "기독교 교회사 제7권: 독일 종교개혁",
        "title_en": "History of the Christian Church Vol.7: German Reformation",
        "author_kr": "필립 샤프",
        "author_en": "Philip Schaff",
        "year": 1888,
    },
    {
        "slug": "schaff-church-history-v8",
        "title": "기독교 교회사 제8권: 스위스 종교개혁",
        "title_en": "History of the Christian Church Vol.8: Swiss Reformation",
        "author_kr": "필립 샤프",
        "author_en": "Philip Schaff",
        "year": 1892,
    },
    {
        "slug": "schaff-creeds-christendom-v1",
        "title": "기독교의 신조들 제1권: 신조의 역사",
        "title_en": "The Creeds of Christendom Vol.1: History of Creeds",
        "author_kr": "필립 샤프",
        "author_en": "Philip Schaff",
        "year": 1877,
    },
    {
        "slug": "schaff-creeds-christendom-v2",
        "title": "기독교의 신조들 제2권: 헬라·라틴 신조",
        "title_en": "The Creeds of Christendom Vol.2: Greek & Latin Creeds (text + commentary)",
        "author_kr": "필립 샤프",
        "author_en": "Philip Schaff",
        "year": 1877,
    },
]

if __name__ == "__main__":
    process_all(BOOKS)
